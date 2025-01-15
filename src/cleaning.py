from . import files_import

def clean_data_from_jsons_folder(folder_path):
    # הפעלת הפונקציה לעיבוד התיקייה
    results = files_import.process_folder(folder_path)

    # ניקוי הנתונים
    for student in results:
        if 'data' in student:
           # סינון הנתונים כך שלא יכילו ערכים עם המפתח 'null'
            student['data'] = [obj for obj in student['data'] if 'null' not in obj]
        if 'record_count' in student:
            # update relevant record_count
            student['record_count'] = len(student['data'])

    # החזרת המידע הנקי
    return results