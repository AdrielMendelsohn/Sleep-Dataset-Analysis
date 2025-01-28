#    Variables
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
import numpy as np


# Function to generate a sample graph
def generate_graph():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    return plt

# Function to display the graph
def show_graph():
    plt = generate_graph()
    plt.show()

# Function to save the graph
def save_graph():
    plt = generate_graph()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
        title="Save Graph As"
    )
    if file_path:
        plt.savefig(file_path)
        messagebox.showinfo("Success", f"Graph saved successfully as {file_path}")

def exit_application():
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()


# Create the main window
root = tk.Tk()
root.title("Graph Viewer & Saver")
root.geometry("500x300")  # Increased window size
root.resizable(True, True)  # Allow resizing

# Apply a ttk theme
style = ttk.Style(root)
style.theme_use("clam")  # Modern theme for ttk widgets

# Add a title label
title_label = ttk.Label(root, text="Graph Options", font=("Helvetica", 18, "bold"))
title_label.pack(pady=20)

# Add a frame for buttons (for better alignment and customization)
button_frame = ttk.Frame(root, padding=20)
button_frame.pack(fill="x", expand=True)

# Add buttons for user actions
show_button = ttk.Button(button_frame, text="Show Graph", command=show_graph, width=30)
show_button.pack(side="left", padx=10, pady=10)

save_button = ttk.Button(button_frame, text="Save Graph", command=save_graph, width=30)
save_button.pack(side="right", padx=10, pady=10)

# Add the Exit button at the bottom
exit_button = ttk.Button(root, text="Exit", command=exit_application)
exit_button.pack(side="bottom", pady=20)

# Run the main loop
root.mainloop()
