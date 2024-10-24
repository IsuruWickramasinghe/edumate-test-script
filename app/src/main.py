from datetime import datetime
import os
from dotenv import load_dotenv
from auth import get_auth_token

load_dotenv()

# import fetchers
from fetch_reports.fetch_report_periods import fetch_report_periods
from fetch_reports.fetch_task import fetch_tasks

YEARS_COUNT = 2 # with current year this counted as a 3 years

current_year = datetime.now().year
start_year = current_year - YEARS_COUNT
end_year = current_year
academic_year_ids = {year: 4500 + (year - 2022) for year in range(start_year, end_year + 1)}


def main():
    base_url = os.getenv('BASE_URL')
    token = get_auth_token()

    if token:
        fetch_report_periods(token, academic_year_ids, base_url, start_year, end_year)
        fetch_tasks(token, academic_year_ids, base_url)

if __name__ == "__main__":
    main()
