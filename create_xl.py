#%%
import pandas as pd
import os
from src import files_import
from src import to_csv
from openpyxl import Workbook
#%%
# Define the folder containing the files
EMA_dictionary = "data/StudentLife/dataset/EMA"
mood_directory_path = "data/StudentLife/dataset/EMA/response/Mood"
mood1_directory_path = "data/StudentLife/dataset/EMA/response/Mood 1"
mood2_directory_path = "data/StudentLife/dataset/EMA/response/Mood 2"
exercise_directory_path = "data/StudentLife/dataset/EMA/response/Exercise"
stress_directory_path = "data/StudentLife/dataset/EMA/response/Stress"
social_directory_path = "data/StudentLife/dataset/EMA/response/Social"
sleep_directory_path = "data/StudentLife/dataset/EMA/response/Sleep"
activity_directory_path = "data/StudentLife/dataset/EMA/response/Activity"


# Define single file paths
grades_file_path = "data/StudentLife/dataset/education/grades.csv"

# List of datasets and their directory paths
survey_datasets = {
    "Mood": {'Path' : mood_directory_path, 'Important_Column' : 'happyornot'},
    "Mood1":  {'Path' : mood1_directory_path, 'Important_Column' : 'tomorrow'},
    "Mood2":  {'Path' : mood2_directory_path, 'Important_Column' : 'how'},
    "Exercise":  {'Path' : exercise_directory_path, 'Important_Column' : 'have'},
    "Stress":  {'Path' : stress_directory_path, 'Important_Column' : 'level'},
    "Social":  {'Path' : social_directory_path, 'Important_Column' : 'number'},
    "Sleep":  {'Path' : sleep_directory_path, 'Important_Column' : 'hour'},
    "Activity":  {'Path' : activity_directory_path, 'Important_Column' : 'working'},
}

file_name ="output.xlsx"

semester_length_in_days = 65
#%%

# Check if the file exists
if os.path.exists(file_name):
    os.remove(file_name)  # Delete the file if it exists
    print(f"Deleted existing file: {file_name}")

# Create an empty .xlsx file
wb = Workbook()
wb.save(file_name)  # Save the empty workbook to the specified file name
print(f"Created new empty file: {file_name}")


#%%
all_data = {}
for survey, dictionary in survey_datasets.items():
    combined_data = to_csv.folder_to_csv(dictionary['Path'], dictionary['Important_Column'], 0)
    all_data[survey] = combined_data
#%%
combined_csv = {}

#uids = [f"u{i:02d}" for i in range(0, 60)]
#user_df = pd.DataFrame({"User": uids}) 
#combined_csv['User'] = uids


# קריאת הקובץ
df = pd.read_excel(file_name)

# יצירת רשימת המשתתפים
uids = [f"u{i:02d}" for i in range(0, 60)]

# בדיקה שהעמודה 'uid' קיימת
if 'User' in df.columns:
    df['User'] = uids  # מחליפים את הערכים בעמודה הקיימת
else:
    df.insert(0, 'User', uids)  # מוסיפים את העמודה כעמודה ראשונה

# שמירת הקובץ
df.to_excel(file_name, index=False)

print("The file has been successfully updated!")
#%%

# Transformation dictionaries
# if data saved as a range, mapping to midpoint
social_mapping = {
    1:2, 2:7, 3:15, 4:30, 5:75, 6:150
}
stress_mapping = {
    1:3, 2:4, 3:5, 4:2, 5:1
}

# Mapping the data
stress_data= all_data['Stress']
all_data['Stress']['stress_level'] = stress_data['level'].map(stress_mapping)

social_data= all_data['Social']
all_data['Social']['number_of_people'] = social_data['number'].map(social_mapping)


average_social = all_data['Social'].groupby('User')['number_of_people'].mean()
average_stress = all_data['Stress'].groupby('User')['stress_level'].mean()
combined_csv['number_of_people'] = average_social
combined_csv['avg_stress_level'] = average_stress

#%%
######################################
#
#               Exercise
#
######################################

# Transformation dictionaries
exercise_mapping = {
    1:0, 2:15, 3:45, 4:75, 5:110
}
# Mapping the data
exercise_data= all_data['Exercise']
exercise_data['exercise_time'] = exercise_data['exercise'].map(exercise_mapping)
exercise_data['walk_time'] = exercise_data['walk'].map(exercise_mapping)
average_exercise_time = exercise_data.groupby('User')['exercise_time'].mean()
average_walk_time = exercise_data.groupby('User')['walk_time'].mean()
exercise_amount = exercise_data[exercise_data['have'] == 1].groupby('User')['have'].sum()
exercise_avg_per_day = exercise_amount/semester_length_in_days

combined_csv['amount_of_workouts'] = exercise_amount
combined_csv['avg_workout_per_day'] = exercise_avg_per_day
combined_csv['avg_workout_time'] = average_exercise_time
combined_csv['avg_walk_time'] = average_walk_time
#%%
sleep_hour_mapping = {
    1:2, 2:3.5, 3:4, 4:4.5, 5:5, 6:5.5, 7:6, 8:6.5, 9:7, 10:7.5, 11:8, 12:8.5, 13:9, 14:9.5, 15:10, 16:10.5, 17:11, 18:11.5, 19:12
}
sleep_rate_mapping = {
    1:4, 2:3, 3:2, 4:1
}

sleep_data = all_data['Sleep']
sleep_data['sleep_hours'] = sleep_data['hour'].map(sleep_hour_mapping)
sleep_data['sleep_rate'] = sleep_data['rate'].map(sleep_rate_mapping)

average_sleep_hours = sleep_data.groupby('User')['sleep_hours'].mean()
average_sleep_rating = sleep_data.groupby('User')['sleep_rate'].mean()

combined_csv['avg_sleep_hours'] = average_sleep_hours
combined_csv['avg_sleep_rating'] = average_sleep_rating
#%%
sad_happy_data = all_data['Mood']
feeling_data = all_data['Mood2']

# Cleaning the data
sad_happy_data = sad_happy_data.dropna(subset=['happy'])
sad_happy_data.loc[sad_happy_data['happyornot'] == 2, 'happy'] = 0
sad_happy_data = sad_happy_data.dropna(subset=['sad'])
sad_happy_data.loc[sad_happy_data['sadornot'] == 2, 'sad'] = 0

# Analysing 
average_happy_rating = sad_happy_data.groupby('User')['happy'].mean()
average_sad_rating = sad_happy_data.groupby('User')['sad'].mean()

total_mood_entries = feeling_data.groupby('User')['how'].sum()
happy_entry_sum = feeling_data[feeling_data['how'] == 1].groupby('User')['how'].sum()
sad_entry_sum = feeling_data[feeling_data['how'] == 3].groupby('User')['how'].sum()
stressed_entry_sum = feeling_data[feeling_data['how'] == 2].groupby('User')['how'].sum()


# Adding to combined df
combined_csv['avg_happy_rating'] = average_happy_rating
combined_csv['avg_sad_rating'] = average_sad_rating
combined_csv['happy_percentage'] = (happy_entry_sum/total_mood_entries)*100
combined_csv['sad_percentage'] = (sad_entry_sum/total_mood_entries)*100
combined_csv['stressed_percentage'] = (stressed_entry_sum/total_mood_entries)*100
#%%
percentage_spent_mapping = {
    1:5, 2:18, 3:38, 4:63, 5:88
}
time_spent_data = all_data['Activity']

time_spent_data['alone_working'] = time_spent_data['working'].map(percentage_spent_mapping)
time_spent_data['alone_relaxing'] = time_spent_data['relaxing'].map(percentage_spent_mapping)
time_spent_data['together_working'] = time_spent_data['other_working'].map(percentage_spent_mapping)
time_spent_data['together_relaxing'] = time_spent_data['other_relaxing'].map(percentage_spent_mapping)
time_spent_data['total_time_spent'] = time_spent_data['together_relaxing'] + time_spent_data['together_working'] + time_spent_data['alone_relaxing'] + time_spent_data['alone_working']

# Percentages
time_spent_data['alone_percentage'] = (time_spent_data['alone_working'] + time_spent_data['alone_relaxing'])/time_spent_data['total_time_spent']  * 100
time_spent_data['together_percentage'] = (time_spent_data['together_working'] + time_spent_data['together_relaxing'])/time_spent_data['total_time_spent']  * 100
time_spent_data['working_percentage'] = (time_spent_data['alone_working'] + time_spent_data['together_working'])/time_spent_data['total_time_spent']  * 100
time_spent_data['relaxing_percentage'] = (time_spent_data['alone_relaxing'] + time_spent_data['together_relaxing'])/time_spent_data['total_time_spent']  * 100

# adding averages
combined_csv['avg_alone_percentage'] = time_spent_data.groupby('User')['alone_percentage'].mean()
combined_csv['avg_together_percentage'] = time_spent_data.groupby('User')['together_percentage'].mean()
combined_csv['avg_working_percentage'] = time_spent_data.groupby('User')['working_percentage'].mean()
combined_csv['avg_relaxing_percentage'] = time_spent_data.groupby('User')['relaxing_percentage'].mean()

#%%
def create_grades_dictionary():
    file_path = "data/StudentLife\dataset\education\grades.csv"
    grades_data = pd.read_csv(file_path)

    final_grades_data = {}

    # רשימת כל ה- uid האפשריים
    all_uids = [f"u{str(i).zfill(2)}" for i in range(0, 60)]

    # יצירת מילון עם ערכי ברירת מחדל
    for uid in all_uids:
        final_grades_data[uid] = {
            'gpaAll': None,
            'gpa 13s': None
        }

    # מילוי נתונים מהקובץ
    for student in range(len(grades_data['uid'])):
        name = grades_data['uid'][student]
        if name in final_grades_data:  # רק אם ה- uid ברשימה הרצויה
            final_grades_data[name] = {
                'gpaAll': grades_data[' gpa all'][student],
                'gpa 13s': grades_data[' gpa 13s'][student]
            }

    return final_grades_data

grades_info = create_grades_dictionary()

file_read = pd.read_excel(file_name)
for index, row in file_read.iterrows():
    student_id = row['User']
    file_read.at[index, 'gpa all'] = grades_info[student_id]['gpaAll']
    file_read.at[index, 'gpa 13s'] = grades_info[student_id]['gpa 13s']
# שמירת הקובץ
file_read.to_excel(file_name, index=False)
#%%
# קריאת קובץ האקסל
output_file = "output.xlsx"
df_output = pd.read_excel(output_file)

# המרת combined_csv ל-DataFrame אם הוא עדיין מילון
if isinstance(combined_csv, dict):
    combined_csv = pd.DataFrame(combined_csv)

# מחיקת העמודות הקיימות כדי למנוע כפילויות
columns_to_remove = ['amount_of_workouts', 'avg_workout_per_day', 'avg_workout_time', 'avg_walk_time']
df_output.drop(columns=columns_to_remove, errors='ignore', inplace=True)

# ביצוע המיזוג על פי עמודת "User"
df_output = df_output.merge(combined_csv, on="User", how="left")

# שמירת הנתונים המעודכנים בחזרה לקובץ (ללא מילוי של NaN)
df_output.to_excel(output_file, index=False)
