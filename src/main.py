try:
    from ..src import gui
except ImportError:
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from src import gui


excel_output_path = "data/output.xlsx"
sleep_dataset_path = r"data\cmu-sleep.csv"

# Run
def main():
    
    gui.open_gui(excel_output_path, sleep_dataset_path)


if __name__ == "__main__":
    main()
