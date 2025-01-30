import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
import numpy as np
import first_dataset_analysis, first_dataset_excel, second_dataset_analysis, create_sleep_model
import os
import pandas as pd


def ensure_results_directory():
    """Create 'results' directory if it doesn't exist"""
    if not os.path.exists("results"):
        os.makedirs("results")

def run_saves(excel_output_path, sleep_dataset_path):
    try:
        ensure_results_directory()
        first_dataset_analysis.run_full_data_analysis(excel_output_path, False, True)
        second_dataset_analysis.run_full_sleep_analysis(sleep_dataset_path, False, True)
    except(FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}")

def run_shows(excel_output_path, sleep_dataset_path):
    try:
        first_dataset_analysis.run_full_data_analysis(excel_output_path, True, False)
        second_dataset_analysis.run_full_sleep_analysis(sleep_dataset_path, True, False)
    except(FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}")


def create_and_run_model(entries, sleep_dataset_path):
    """Collect inputs from GUI, clean data, train the model, and make a prediction."""
    try:
        # Collect user input from entry widgets
        user_inputs = [float(entry.get()) for entry in entries]

        # Load and prepare the dataset
        data, scaler = create_sleep_model.clean_model_data(sleep_dataset_path)
        model = create_sleep_model.train_model(data)

        # Create a DataFrame and scale the inputs using the trained scaler
        user_data = pd.DataFrame([user_inputs], columns=create_sleep_model.features)
        scaled_user_data = pd.DataFrame(scaler.transform(user_data), columns=create_sleep_model.features)

        # Predict using the trained model
        prediction = model.predict(scaled_user_data)[0]

        # Display the prediction result
        messagebox.showinfo("Prediction Result", f"Predicted Score: {prediction:.2f}")

    except ValueError as e:
        messagebox.showerror("Input Error", f"Please enter valid numeric inputs.\n{str(e)}")

# def create_and_run_model(sleep_dataset_path):
#     data, scaler = create_sleep_model.clean_model_data(sleep_dataset_path)
#     model = create_sleep_model.train_model(data)
#     create_sleep_model.predict_user_input(model, scaler)

def exit_application(root):
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()

def open_gui(excel_output_path, sleep_dataset_path):
    # Create the main window
    root = tk.Tk()
    root.title("Graph Viewer & Saver")
    root.geometry("650x650")  
    root.resizable(True, True)

    # Apply a ttk theme and define custom styles
    style = ttk.Style(root)
    style.theme_use("clam") 

    # Style for frames
    style.configure(
        "Custom.TFrame",
        background="#f9f9f9", 
        borderwidth=1,
        relief="solid",
    )

    # Style for buttons
    style.configure(
        "Custom.TButton",
        background="#0078D4",  # Professional blue
        foreground="white",   
        font=("Helvetica", 12, "bold"),
        padding=6,
    )
    style.map(
        "Custom.TButton",
        background=[
            ("active", "#289BFF"), 
            ("disabled", "#d3d3d3"),
        ],
        foreground=[
            ("disabled", "#a8a8a8"),  # Lighter gray text when disabled
        ],
    )

    # Style for labels
    style.configure(
        "Custom.TLabel",
        background="#f9f9f9",  # To match frame background
        font=("Helvetica", 16, "bold"),
        padding=10,
    )

    # Add a frame for the title
    title_frame = ttk.Frame(root, style="Custom.TFrame", padding=10)
    title_frame.pack(fill="x", pady=10)

    title_label = ttk.Label(
        title_frame, text="Project Interface", style="Custom.TLabel"
    )
    title_label.pack(pady=5)

    # User input section frame
    input_frame = ttk.Frame(root, padding=20)
    input_frame.pack(padx=20, pady=10)

    # Button for predicting score
    predict_button = ttk.Button(
        root, text="Predict Score", command=lambda: create_and_run_model(entries, sleep_dataset_path)
    )
    predict_button.pack(pady=10)

    # Add a frame for buttons
    create_excel_frame = ttk.Frame(root, style="Custom.TFrame", padding=20)
    create_excel_frame.pack(fill="x", padx=20, pady=10)

    button_frame = ttk.Frame(root, style="Custom.TFrame", padding=20)
    button_frame.pack(fill="x", padx=20, pady=10)


    # Dynamic creation of labels and entry fields for features
    entries = []  # To store entry widgets
    for feature in create_sleep_model.features:
        row_frame = ttk.Frame(input_frame)
        row_frame.pack(fill="x", pady=5)

        label = ttk.Label(row_frame, text=f"{feature}:", width=20, anchor="w")
        label.pack(side="left")

        entry = ttk.Entry(row_frame, width=30)
        entry.pack(side="right", padx=5)
        entries.append(entry)


    # Add buttons for user actions
    show_button = ttk.Button(
        button_frame, text="Show Graph", command=lambda: run_shows(excel_output_path, sleep_dataset_path), style="Custom.TButton", width=25
    )
    show_button.pack(side="left", padx=10, pady=10)

    save_button = ttk.Button(
        button_frame, text="Save Graph", command=lambda: run_saves(excel_output_path, sleep_dataset_path), style="Custom.TButton", width=25
    )
    save_button.pack(side="right", padx=10, pady=10)

    create_excel_button = ttk.Button(
        create_excel_frame,
        text="Create Excel",
        command=lambda: first_dataset_excel.build_excel(excel_output_path),
        style="Custom.TButton",
        width=15,
    )
    create_excel_button.pack(side="left", padx=25, pady=10)

    # run_model_button = ttk.Button(
    #     create_excel_frame,
    #     text="Predict Score",
    #     command=lambda: create_and_run_model(sleep_dataset_path),
    #     style="Custom.TButton",
    #     width=15,
    # )
    # run_model_button.pack(side="right", padx=25, pady=10)

    # Add the Exit button at the bottom
    exit_button = ttk.Button(
        root, text="Exit", command=lambda: exit_application(root), style="Custom.TButton", width=10
    )
    exit_button.pack(side="right", padx=25, pady=15)

    root.mainloop()
