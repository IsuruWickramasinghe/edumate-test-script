import requests
import time
from datetime import datetime
from urllib.parse import urlencode

def fetch_report_periods(token, academic_year_ids, base_url, start_year, end_year):
    # Start time
    start_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n----------------------------------------------------------------")
    print("Analytics | Get report periods - fetching started")
    print("----------------------------------------------------------------\n")
    
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json'
    }

    total_duration = 0
    total_report_periods_count = 0
    academic_years = range(start_year, end_year + 1)

    for academic_year in academic_years:
        year_id = academic_year_ids.get(academic_year)
        if not year_id:
            print(f"No valid ID found for year {academic_year}. Skipping...")
            continue

        params = {
            'startAcYearId': year_id,
            'endAcYearId': year_id,
            'limit': 100,
            'offset': 0
        }

        all_report_periods = []  # List to hold all fetched report periods for the current year

        while True:
            # Construct the full endpoint URL with query parameters
            URL = f"{base_url}/api/analytics/report-periods?{urlencode(params)}"
            
            # Print full request URL
            print(f"\nMaking request to: {URL}")

            # Start time for duration measurement
            start_time = time.time()

            response = requests.get(url=URL, headers=headers)

            if response.status_code == 200:
                json_response = response.json()

                # Report periods
                report_periods = json_response.get('data', [])
                all_report_periods.extend(report_periods)
                report_periods_count = sum(len(year_data.get('report_periods', [])) for year_data in report_periods)

                total_report_periods_count += report_periods_count

                # Duration
                duration = time.time() - start_time
                total_duration += duration

                print(f'✔ Year "{academic_year}" fetched successfully \n| Report Periods Count: {report_periods_count} | Duration: {duration:.2f} seconds')

                # Pagination handling
                pagination = json_response.get('pagination', [])
                next_page_url = None
                for page in pagination:
                    if page.get('rel') == 'next':
                        next_page_url = page.get('href')
                        break

                if next_page_url:
                    print("Fetching next page...")
                    params['offset'] += params['limit']
                else:
                    print(f'No more pages for {academic_year}...')
                    break

            else:
                print(f"Error fetching report periods for year {academic_year}: {response.status_code}, {response.text}")
                break

    # Finish time
    end_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Summary output
    print("\n============")
    print(f"Total academic years fetched: {len(academic_years)}")
    print(f"Total report periods fetched: {total_report_periods_count}")
    print(f"Start Time: {start_time_formatted}")
    print(f"Finish Time: {end_time_formatted}")
    print(f"Total duration: {total_duration:.2f} seconds")
    print("============\n")
