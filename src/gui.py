import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
import numpy as np
import first_dataset_analysis, first_dataset_excel, second_dataset_analysis


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
    root.geometry("650x450")  # Slightly larger window for better spacing
    root.resizable(True, True)  # Allow resizing

    # Apply a ttk theme and define custom styles
    style = ttk.Style(root)
    style.theme_use("clam")  # Modern ttk theme

    # Style for frames
    style.configure(
        "Custom.TFrame",
        background="#f9f9f9",  # Light neutral background
        borderwidth=1,
        relief="solid",
    )

    # Style for buttons
    style.configure(
        "Custom.TButton",
        background="#0078D4",  # Professional blue
        foreground="white",    # White text
        font=("Helvetica", 12, "bold"),
        padding=6,
    )
    style.map(
        "Custom.TButton",
        background=[
            ("active", "#005A9E"),  # Darker blue on hover
            ("disabled", "#d3d3d3"),
        ],
        foreground=[
            ("disabled", "#a8a8a8"),  # Lighter gray text when disabled
        ],
    )

    # Style for labels
    style.configure(
        "Custom.TLabel",
        background="#f9f9f9",  # Match frame background
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

    # Add a frame for buttons
    create_excel_frame = ttk.Frame(root, style="Custom.TFrame", padding=20)
    create_excel_frame.pack(fill="x", padx=20, pady=10)

    button_frame = ttk.Frame(root, style="Custom.TFrame", padding=20)
    button_frame.pack(fill="x", padx=20, pady=10)

    # Add buttons for user actions
    show_button = ttk.Button(
        button_frame, text="Show Graph", command=lambda: run_shows(excel_output_path), style="Custom.TButton", width=25
    )
    show_button.pack(side="left", padx=10, pady=10)

    save_button = ttk.Button(
        button_frame, text="Save Graph", command=lambda: run_saves(excel_output_path), style="Custom.TButton", width=25
    )
    save_button.pack(side="right", padx=10, pady=10)

    create_excel_button = ttk.Button(
        create_excel_frame,
        text="Create Excel",
        command=lambda: first_dataset_excel.build_excel(excel_output_path),
        style="Custom.TButton",
        width=15,
    )
    create_excel_button.pack(pady=10)

    # Add the Exit button at the bottom
    exit_button = ttk.Button(
        root, text="Exit", command=lambda: exit_application(root), style="Custom.TButton", width=25
    )
    exit_button.pack(side="bottom", pady=20)

    # Run the main loop
    root.mainloop()
