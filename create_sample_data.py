import pandas as pd
import os

# إنشاء مجلد sample_data
os.makedirs('sample_data', exist_ok=True)

# البيانات التجريبية لملف Gradebook
gradebook_data = {
    'Student Name': ['محمد علي', 'فاطمة أحمد', 'علي محمود', 'نور السيد', 'هناء حسن', 'خالد عمر', 'مريم صالح', 'أحمد جمال'],
    'Test 1': [85, 92, 78, 88, 95, 72, 89, 91],
    'Test 2': [90, 88, 82, 85, 92, 75, 87, 93],
    'Quiz 1': [88, 90, 80, 87, 94, 73, 88, 89],
    'Quiz 2': [87, 91, 79, 86, 93, 74, 90, 92],
    'Final Exam': [89, 94, 81, 88, 96, 76, 91, 94],
    'Total Grade': [87.8, 91, 80, 86.8, 94, 74, 89.2, 91.8]
}

# البيانات التجريبية لملف Analytics
analytics_data = {
    'Student Name': ['محمد علي', 'فاطمة أحمد', 'علي محمود', 'نور السيد', 'هناء حسن', 'خالد عمر', 'مريم صالح', 'أحمد جمال'],
    'Missed Deadlines': [1, 0, 4, 2, 0, 6, 1, 0],
    'Hours Spent': [6.5, 9, 3, 7, 10, 2, 8, 9.5],
    'Days Since Access': [2, 1, 8, 3, 1, 15, 2, 1]
}

# إنشاء DataFrames
df_gradebook = pd.DataFrame(gradebook_data)
df_analytics = pd.DataFrame(analytics_data)

# حفظ في Excel
df_gradebook.to_excel('sample_data/Gradebook_Sample.xlsx', index=False, engine='openpyxl')
df_analytics.to_excel('sample_data/Analytics_Sample.xlsx', index=False, engine='openpyxl')

print('✓ تم إنشاء الملفات بنجاح!')
print('✓ Gradebook_Sample.xlsx')
print('✓ Analytics_Sample.xlsx')
print('')
print('الملفات موجودة في: e:\\dryasserkiro\\sample_data\\')
