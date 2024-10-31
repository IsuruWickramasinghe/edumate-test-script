from datetime import datetime
import os
from dotenv import load_dotenv
from auth import get_auth_token

load_dotenv()

# Import fetchers
from fetch_reports.fetch_report_periods import fetch_report_periods
from fetch_reports.fetch_task import fetch_tasks
from fetch_reports.fetch_task_results import fetch_task_results
from fetch_reports.fetch_student_course_results import fetch_student_course_results

YEARS_COUNT = 2  # With current year this counted as a 3 years

current_year = datetime.now().year
start_year = current_year - YEARS_COUNT
end_year = current_year
academic_year_ids = {year: 4500 + (year - 2022) for year in range(start_year, end_year + 1)}

# Separate dictionary for fetch_report_periods from 2000 to 2024
report_period_academic_year_ids = {year: 4500 + (year - 2022) for year in range(2000, 2025)}

def main():
    base_url = os.getenv('BASE_URL')
    token = get_auth_token()

    if not token:
        return None
    
    while True:
        print("\nSelect the function to run:")
        print("1. fetch_report_periods")
        print("2. fetch_tasks")
        print("3. fetch_task_results")
        print("4. fetch_student_course_results")
        print("0. Exit")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            fetch_report_periods(token, report_period_academic_year_ids, base_url, 2000, 2024)

        elif choice == "2":
            fetch_tasks(token, academic_year_ids, base_url)

        elif choice == "3":
            fetch_task_results(token, academic_year_ids, base_url)

        elif choice == "4":
            report_period_ids = fetch_report_periods(token, academic_year_ids, base_url, start_year, end_year, return_ids=True)
            fetch_student_course_results(token, base_url, report_period_ids)

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
