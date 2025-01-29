import os

import pandas as pd
from openpyxl import Workbook

import to_csv

# Define the dataset paths
survey_datasets = {
    "Mood": {"Path": "data/StudentLife/dataset/EMA/response/Mood", "Important_Column": "happyornot"},
    "Mood1": {"Path": "data/StudentLife/dataset/EMA/response/Mood 1", "Important_Column": "tomorrow"},
    "Mood2": {"Path": "data/StudentLife/dataset/EMA/response/Mood 2", "Important_Column": "how"},
    "Exercise": {"Path": "data/StudentLife/dataset/EMA/response/Exercise", "Important_Column": "have"},
    "Stress": {"Path": "data/StudentLife/dataset/EMA/response/Stress", "Important_Column": "level"},
    "Social": {"Path": "data/StudentLife/dataset/EMA/response/Social", "Important_Column": "number"},
    "Sleep": {"Path": "data/StudentLife/dataset/EMA/response/Sleep", "Important_Column": "hour"},
    "Activity": {"Path": "data/StudentLife/dataset/EMA/response/Activity", "Important_Column": "working"}
}

grades_file_path = "data/StudentLife/dataset/education/grades.csv"

def initialize_excel_file(output_path):
    """Creates a new Excel file or deletes the existing one."""
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Deleted existing file: {output_path}")
    wb = Workbook()
    wb.save(output_path)
    print(f"Created new empty file: {output_path}")

def load_survey_data():
    """Loads and processes survey data into a dictionary."""
    all_data = {}
    for survey, dictionary in survey_datasets.items():
        combined_data = to_csv.folder_to_csv(dictionary["Path"], dictionary["Important_Column"], 0)
        all_data[survey] = combined_data
    return all_data

def create_user_column(output_path):
    """Ensures the User column exists in the Excel file."""
    df = pd.read_excel(output_path)
    uids = [f"u{i:02d}" for i in range(60)]
    if "User" in df.columns:
        df["User"] = uids
    else:
        df.insert(0, "User", uids)
    df.to_excel(output_path, index=False)

def process_stress_social(all_data, combined_csv):
    """Processes stress and social activity columns."""
    stress_mapping = {1:3, 2:4, 3:5, 4:2, 5:1}
    social_mapping = {1:2, 2:7, 3:15, 4:30, 5:75, 6:150}
    all_data["Stress"]["stress_level"] = all_data["Stress"]["level"].map(stress_mapping)
    all_data["Social"]["number_of_people"] = all_data["Social"]["number"].map(social_mapping)
    combined_csv["number_of_people"] = all_data["Social"].groupby("User")["number_of_people"].mean()
    combined_csv["avg_stress_level"] = all_data["Stress"].groupby("User")["stress_level"].mean()

def process_exercise(all_data, combined_csv):
    """Processes exercise-related columns."""
    exercise_mapping = {1:0, 2:15, 3:45, 4:75, 5:110}
    semester_length_in_days = 65
    exercise_data = all_data["Exercise"]
    exercise_data["exercise_time"] = exercise_data["exercise"].map(exercise_mapping)
    exercise_data["walk_time"] = exercise_data["walk"].map(exercise_mapping)
    combined_csv["amount_of_workouts"] = exercise_data[exercise_data["have"] == 1].groupby("User")["have"].sum()
    combined_csv["avg_workout_per_day"] = combined_csv["amount_of_workouts"] / semester_length_in_days
    combined_csv["avg_workout_time"] = exercise_data.groupby("User")["exercise_time"].mean()
    combined_csv["avg_walk_time"] = exercise_data.groupby("User")["walk_time"].mean()

def process_sleep(all_data, combined_csv):
    """Crating the sleep related columns"""
    sleep_hour_mapping = {
        1:2, 2:3.5, 3:4, 4:4.5, 5:5, 6:5.5, 7:6, 8:6.5, 9:7, 10:7.5, 11:8, 12:8.5, 13:9, 14:9.5, 15:10, 16:10.5, 17:11, 18:11.5, 19:12
    }
    # Making sure that higher rating means better sleep
    sleep_rate_mapping = {1:4, 2:3, 3:2, 4:1}

    sleep_data = all_data["Sleep"]
    sleep_data["sleep_hours"] = sleep_data["hour"].map(sleep_hour_mapping)
    sleep_data["sleep_rate"] = sleep_data["rate"].map(sleep_rate_mapping)
    combined_csv["avg_sleep_hours"] = sleep_data.groupby("User")["sleep_hours"].mean()
    combined_csv["avg_sleep_rating"] = sleep_data.groupby("User")["sleep_rate"].mean()

def process_mood(all_data, combined_csv):
    """Crating the mood related columns"""
    sad_happy_data = all_data["Mood"]
    feeling_data = all_data["Mood2"]
    # Cleaning the data
    sad_happy_data = sad_happy_data.dropna(subset=["happy"])
    sad_happy_data.loc[sad_happy_data["happyornot"] == 2, "happy"] = 0
    sad_happy_data = sad_happy_data.dropna(subset=["sad"])
    sad_happy_data.loc[sad_happy_data["sadornot"] == 2, "sad"] = 0
    # Analysing
    average_happy_rating = sad_happy_data.groupby("User")["happy"].mean()
    average_sad_rating = sad_happy_data.groupby("User")["sad"].mean()

    total_mood_entries = feeling_data.groupby("User")["how"].sum()
    happy_entry_sum = feeling_data[feeling_data["how"] == 1].groupby("User")["how"].sum()
    sad_entry_sum = feeling_data[feeling_data["how"] == 3].groupby("User")["how"].sum()
    stressed_entry_sum = feeling_data[feeling_data["how"] == 2].groupby("User")["how"].sum()
    # Adding to combined df
    combined_csv["avg_happy_rating"] = average_happy_rating
    combined_csv["avg_sad_rating"] = average_sad_rating
    combined_csv["happy_percentage"] = (happy_entry_sum/total_mood_entries)*100
    combined_csv["sad_percentage"] = (sad_entry_sum/total_mood_entries)*100
    combined_csv["stressed_percentage"] = (stressed_entry_sum/total_mood_entries)*100

def process_time_managment(all_data, combined_csv):
    """Crating the columns related to how the students manage their time"""
    percentage_spent_mapping = {
        1:5, 2:18, 3:38, 4:63, 5:88
    }
    time_spent_data = all_data["Activity"]

    time_spent_data["alone_working"] = time_spent_data["working"].map(percentage_spent_mapping)
    time_spent_data["alone_relaxing"] = time_spent_data["relaxing"].map(percentage_spent_mapping)
    time_spent_data["together_working"] = time_spent_data["other_working"].map(percentage_spent_mapping)
    time_spent_data["together_relaxing"] = time_spent_data["other_relaxing"].map(percentage_spent_mapping)
    time_spent_data["total_time_spent"] = time_spent_data["together_relaxing"] + time_spent_data["together_working"] + time_spent_data["alone_relaxing"] + time_spent_data["alone_working"]

    # Percentages
    time_spent_data["alone_percentage"] = (time_spent_data["alone_working"] + time_spent_data["alone_relaxing"])/time_spent_data["total_time_spent"]  * 100
    time_spent_data["together_percentage"] = (time_spent_data["together_working"] + time_spent_data["together_relaxing"])/time_spent_data["total_time_spent"]  * 100
    time_spent_data["working_percentage"] = (time_spent_data["alone_working"] + time_spent_data["together_working"])/time_spent_data["total_time_spent"]  * 100
    time_spent_data["relaxing_percentage"] = (time_spent_data["alone_relaxing"] + time_spent_data["together_relaxing"])/time_spent_data["total_time_spent"]  * 100

    # adding averages
    combined_csv["avg_alone_percentage"] = time_spent_data.groupby("User")["alone_percentage"].mean()
    combined_csv["avg_together_percentage"] = time_spent_data.groupby("User")["together_percentage"].mean()
    combined_csv["avg_working_percentage"] = time_spent_data.groupby("User")["working_percentage"].mean()
    combined_csv["avg_relaxing_percentage"] = time_spent_data.groupby("User")["relaxing_percentage"].mean()



def create_grades_dictionary():
    """Processes the GPA-related columns."""
    grades_data = pd.read_csv(grades_file_path)
    final_grades_data = {f"u{i:02d}": {"gpaAll": None, "gpa_13s": None} for i in range(60)}
    for student in range(len(grades_data["uid"])):
        name = grades_data["uid"][student]
        if name in final_grades_data:
            final_grades_data[name] = {
                "gpaAll": grades_data[" gpa all"][student] * 25,
                "gpa_13s": grades_data[" gpa 13s"][student] * 25
            }
    return final_grades_data

def merge_data_with_output(combined_csv, output_path):
    """Merges the processed data into the Excel output file."""
    df_output = pd.read_excel(output_path)
    combined_csv = pd.DataFrame(combined_csv)
    df_output = df_output.merge(combined_csv, on="User", how="left")
    df_output.to_excel(output_path, index=False)
    print("The file has been successfully updated!")

def build_excel(output_path = "output.xlsx"):
    """Runs the full data processing pipeline."""
    initialize_excel_file(output_path)
    all_data = load_survey_data()
    create_user_column(output_path)
    combined_csv = {}
    process_stress_social(all_data, combined_csv)
    process_exercise(all_data, combined_csv)
    process_sleep(all_data, combined_csv)
    process_mood(all_data, combined_csv)
    process_time_managment(all_data, combined_csv)
    grades_info = create_grades_dictionary()
    df = pd.read_excel(output_path)
    for index, row in df.iterrows():
        student_id = row["User"]
        df.at[index, "gpa_all"] = grades_info[student_id]["gpaAll"]
        df.at[index, "gpa_13s"] = grades_info[student_id]["gpa_13s"]
    df.to_excel(output_path, index=False)
    merge_data_with_output(combined_csv, output_path)


