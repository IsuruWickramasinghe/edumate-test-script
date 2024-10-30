import requests
import time
from datetime import datetime
from urllib.parse import urlencode

def fetch_student_course_results(token, base_url, report_period_ids):
    # Start time
    start_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global_start_time = time.time()  # Track the overall start time

    print("\n----------------------------------------------------------------")
    print("Analytics | Get student course results - fetching started")
    print("----------------------------------------------------------------\n")

    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json'
    }

    total_duration = 0
    total_results_count = 0  # Main total count for all report periods

    for report_period_id in report_period_ids:
        params = {
            'limit': 100,
            'offset': 0
        }
        scope = "all"
        all_results = []  # List to hold all fetched results for the current report period
        report_period_results_count = 0  # Counter for results in the current report period
        report_period_start_time = time.time()  # Start time for the current report period

        while True:
            # Construct the full endpoint URL with path parameters
            URL = f"{base_url}/api/analytics/student/course-results/{scope}/{report_period_id}"
            # Append params as query string
            full_url = f"{URL}?{urlencode(params)}"
            
            # Print full request URL
            print(f"\nMaking request to: {full_url}")

            # Start time for duration measurement of this request
            start_time = time.time()

            response = requests.get(url=full_url, headers=headers)

            if response.status_code == 200:
                json_response = response.json()

                # Duration for the current request
                duration = time.time() - start_time
                total_duration += duration

                # Print reportPeriodId and offset count
                print(f'✔ Report Period ID "{report_period_id}" | Offset: {params["offset"]:03} | Duration: {duration:.2f} seconds')

                # Store results from the response
                results = json_response.get('data', [])
                all_results.extend(results)
                report_period_results_count += len(results)  # Increment the current report period's result count
                total_results_count += len(results)  # Increment the total result count across all report periods

                # Pagination handling
                pagination = json_response.get('pagination', {})

                if isinstance(pagination, dict):
                    next_page_url = pagination.get('next')

                    if next_page_url:
                        print("Fetching next page...")
                        params['offset'] += params['limit']
                    else:
                        print("\nNo more pages to fetch for this report period.\n")
                        break
                else:
                    print("Warning: Pagination format unexpected. No more pages to fetch.")
                    break

            else:
                print(f"Error fetching course results for report period {report_period_id}: {response.status_code}, {response.text}")
                break

        # Calculate report period duration
        report_period_duration = time.time() - report_period_start_time

        # Print the total result count and total time for the current report period
        print("\n============")
        print(f"> Total results fetched for Report Period '{report_period_id}': {report_period_results_count}")
        print(f"> Total time taken for Report Period '{report_period_id}': {report_period_duration:.2f} seconds")
        print("============\n")

    # Finish time
    end_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global_duration = time.time() - global_start_time  # Calculate overall duration

    # Summary output for all report periods
    print("\n============")
    print(f"Total report periods fetched: {len(report_period_ids)}")
    print(f"Total results fetched: {total_results_count}")
    print(f"Start Time: {start_time_formatted}")
    print(f"Finish Time: {end_time_formatted}")
    print(f"Total duration: {global_duration:.2f} seconds")
    print("============\n")
