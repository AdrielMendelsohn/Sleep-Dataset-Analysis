from src import first_dataset_analysis, first_dataset_excel, second_dataset_analysis

excel_output_path = "data/output.xlsx"
save_choice = False
show_choice = True

# Run
def main():


    first_dataset_excel.build_excel(excel_output_path)

    first_dataset_analysis.main(excel_output_path, show_choice, save_choice)

    # Second Dataset
    second_dataset_analysis.run_full_sleep_analysis(show_choice, save_choice)


if __name__ == "__main__":
    main()
