#    Variables
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
import numpy as np
from . import first_dataset_analysis, first_dataset_excel, second_dataset_analysis


def run_saves(excel_output_path):
    first_dataset_analysis.run_full_data_analysis(excel_output_path, False, True)
    second_dataset_analysis.run_full_sleep_analysis(False, True)

def run_shows(excel_output_path):
    first_dataset_analysis.run_full_data_analysis(excel_output_path, True, False)
    second_dataset_analysis.run_full_sleep_analysis(True, False)


def exit_application(root):
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()

def open_gui(excel_output_path):
    # Create the main window
    root = tk.Tk()
    root.title("Graph Viewer & Saver")
    root.geometry("600x400")  # Increased window size
    root.resizable(True, True)  # Allow resizing

    # Apply a ttk theme
    style = ttk.Style(root)
    style.theme_use("clam")  # Modern theme for ttk widgets

    # Add a title label
    title_label = ttk.Label(root, text="Graph Options", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=20)

    # Add a frame for buttons (for better alignment and customization)
    create_excel_frame = ttk.Frame(root, padding=20)
    create_excel_frame.pack(fill="x", expand=True)
    button_frame = ttk.Frame(root, padding=20)
    button_frame.pack(fill="x", expand=True)

    # Add buttons for user actions
    show_button = ttk.Button(button_frame, text="Show Graph", command=lambda: run_shows(excel_output_path), width=30)
    show_button.pack(side="left", padx=10, pady=10)

    save_button = ttk.Button(button_frame, text="Save Graph", command=lambda: run_saves(excel_output_path), width=30)
    save_button.pack(side="right", padx=10, pady=10)

    create_excel_button = ttk.Button(create_excel_frame, text="Create Excel", command=lambda: first_dataset_excel.build_excel(excel_output_path), width=15)
    create_excel_button.pack(side="left", padx=10, pady=10)

    # Add the Exit button at the bottom
    exit_button = ttk.Button(root, text="Exit", command=lambda: exit_application(root))
    exit_button.pack(side="bottom", pady=20)

    # Run the main loop
    root.mainloop()


