from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import os
import traceback
from analyzer import AcademicAnalyzer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# تفعيل CORS بشكل كامل
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
FRONTEND_FOLDER = '../frontend'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max


@app.route('/')
def index():
    """Serve the main HTML page"""
    index_path = os.path.join(FRONTEND_FOLDER, 'index.html')
    return send_file(index_path)


@app.route('/style.css')
def style():
    """Serve the CSS file"""
    css_path = os.path.join(FRONTEND_FOLDER, 'style.css')
    return send_file(css_path, mimetype='text/css')


@app.route('/app.js')
def app_js():
    """Serve the JavaScript file"""
    js_path = os.path.join(FRONTEND_FOLDER, 'app.js')
    return send_file(js_path, mimetype='application/javascript')


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Academic Analytics System Running'})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        if 'gradebook' not in request.files or 'analytics' not in request.files:
            return jsonify({'error': 'يرجى رفع كلا الملفين: Gradebook و Analytics'}), 400

        gradebook_file = request.files['gradebook']
        analytics_file = request.files['analytics']

        if gradebook_file.filename == '' or analytics_file.filename == '':
            return jsonify({'error': 'لم يتم اختيار الملفات'}), 400

        # Save uploaded files
        gradebook_path = os.path.join(UPLOAD_FOLDER, 'gradebook.xlsx')
        analytics_path = os.path.join(UPLOAD_FOLDER, 'analytics.xlsx')
        gradebook_file.save(gradebook_path)
        analytics_file.save(analytics_path)

        # Run analysis
        analyzer = AcademicAnalyzer(gradebook_path, analytics_path)
        report = analyzer.generate_full_report()

        return jsonify(report)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'خطأ في التحليل: {str(e)}'}), 500


@app.route('/api/download-report', methods=['POST'])
def download_report():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'لا توجد بيانات للتنزيل'}), 400

        gradebook_path = os.path.join(UPLOAD_FOLDER, 'gradebook.xlsx')
        analytics_path = os.path.join(UPLOAD_FOLDER, 'analytics.xlsx')

        if not os.path.exists(gradebook_path) or not os.path.exists(analytics_path):
            return jsonify({'error': 'يرجى رفع الملفات أولاً'}), 400

        analyzer = AcademicAnalyzer(gradebook_path, analytics_path)
        report_path = analyzer.export_excel_report(REPORTS_FOLDER)

        return send_file(
            report_path,
            as_attachment=True,
            download_name='academic_analytics_report.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'خطأ في التنزيل: {str(e)}'}), 500


@app.route('/api/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        if not data or 'student_id' not in data or 'student_name' not in data or 'risk_level' not in data or 'recommendations' not in data:
            return jsonify({'error': 'بيانات غير كاملة'}), 400

        student_id = data['student_id']
        student_name = data['student_name']
        risk_level = data['risk_level']
        recommendations = data['recommendations']

        # بيانات البريد المرسل مخزنة في ملف backend/.env أو متغيرات البيئة
        sender_email = os.environ.get('MAIL_SENDER')
        sender_password = os.environ.get('MAIL_PASSWORD')
        smtp_host = os.environ.get('MAIL_HOST', 'smtp.gmail.com')
        smtp_port = os.environ.get('MAIL_PORT', '587')
        smtp_secure = os.environ.get('MAIL_SECURE', 'starttls')

        if not sender_email or not sender_password:
            return jsonify({'error': 'لم يتم إعداد بريد المرسل أو كلمة المرور في backend/.env.'}), 500

        gradebook_path = os.path.join(UPLOAD_FOLDER, 'gradebook.xlsx')
        analytics_path = os.path.join(UPLOAD_FOLDER, 'analytics.xlsx')

        if not os.path.exists(gradebook_path) or not os.path.exists(analytics_path):
            return jsonify({'error': 'يرجى رفع الملفات أولاً'}), 400

        analyzer = AcademicAnalyzer(gradebook_path, analytics_path)
        success, message = analyzer.send_email_notification(student_id, student_name, risk_level, recommendations, sender_email, sender_password, smtp_host, smtp_port, smtp_secure)

        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'خطأ في إرسال البريد: {str(e)}'}), 500
        traceback.print_exc()
        return jsonify({'error': f'خطأ في توليد التقرير: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
