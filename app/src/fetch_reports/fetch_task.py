import requests
import time
from datetime import datetime
from urllib.parse import urlencode

def fetch_tasks(token, academic_year_ids, base_url):
    # Start time
    start_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global_start_time = time.time()  # Track the overall start time

    print("\n----------------------------------------------------------------")
    print("Analytics | Get tasks - fetching started")
    print("----------------------------------------------------------------\n")

    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json'
    }

    total_duration = 0
    total_tasks_count = 0  # Main total count for all academic years

    for academic_year, year_id in academic_year_ids.items():
        params = {
            'academicYearId': year_id,
            'limit': 100,
            'offset': 0
        }

        all_tasks = []  # List to hold all fetched tasks for the current year
        year_tasks_count = 0  # Counter for tasks in the current academic year
        year_start_time = time.time()  # Start time for the current academic year

        while True:
            # Construct the full endpoint URL with query parameters
            URL = f"{base_url}/api/analytics/tasks?{urlencode(params)}"
            
            # Print full request URL
            print(f"\nMaking request to: {URL}")

            # Start time for duration measurement of this request
            start_time = time.time()

            response = requests.get(url=URL, headers=headers)

            if response.status_code == 200:
                json_response = response.json()

                # Duration for the current request
                duration = time.time() - start_time
                total_duration += duration

                # Print academicYearId and offset count
                print(f'✔ Year "{academic_year}" \n | Academic Year ID: {year_id} | Offset: {params["offset"]:03} | Duration: {duration:.2f} seconds')

                # Store tasks from the response
                tasks = json_response.get('data', [])
                all_tasks.extend(tasks)
                year_tasks_count += len(tasks)  # Increment the current year's task count
                total_tasks_count += len(tasks)  # Increment the total task count across all years

                # Pagination handling
                pagination = json_response.get('pagination', {})

                if isinstance(pagination, dict):
                    next_page_url = pagination.get('next')

                    if next_page_url:
                        print("Fetching next page...")
                        params['offset'] += params['limit']
                    else:
                        print("\nNo more pages to fetch for this academic year.\n")
                        break
                else:
                    print("Warning: Pagination format unexpected. No more pages to fetch.")
                    break

            else:
                print(f"Error fetching tasks for year {academic_year}: {response.status_code}, {response.text}")
                break

        # Calculate year duration
        year_duration = time.time() - year_start_time

        # Print the total task count and total time for the current year
        print("\n============")
        print(f"> Total tasks fetched for Year '{academic_year}': {year_tasks_count}")
        print(f"> Total time taken for Year '{academic_year}': {year_duration:.2f} seconds")
        print("============\n")

    # Finish time
    end_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global_duration = time.time() - global_start_time  # Calculate overall duration

    # Summary output for all years
    print("\n============")
    print(f"Total academic years fetched: {len(academic_year_ids)}")
    print(f"Total tasks fetched: {total_tasks_count}")
    print(f"Start Time: {start_time_formatted}")
    print(f"Finish Time: {end_time_formatted}")
    print(f"Total duration: {global_duration:.2f} seconds")
    print("============\n")

