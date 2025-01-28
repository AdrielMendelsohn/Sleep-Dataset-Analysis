import first_dataset_excel
import analize_first_dataset
import second_dataset_analysis
from src import cleaning
from src import plotting


excel_output_path = "data/output.xlsx"

# Run
def main():
    first_dataset_excel.build_excel(excel_output_path)

    analize_first_dataset.main(excel_output_path)

    # Second Dataset
    second_dataset_analysis.run_full_sleep_analysis()


if __name__ == "__main__":
    main()
