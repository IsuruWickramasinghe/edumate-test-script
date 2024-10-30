import requests
import time
from datetime import datetime
from urllib.parse import urlencode

def fetch_task_results(token, academic_year_ids, base_url):
    # Start time
    start_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global_start_time = time.time()

    print("\n----------------------------------------------------------------")
    print("Analytics | Get task results - fetching started")
    print("----------------------------------------------------------------\n")

    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json'
    }

    # Fetch course list with parameters
    course_params = {
        'limit': 100,
        'offset': 0
    }
    course_codes = []

    while True:
        course_url = f"{base_url}/api/analytics/course-list?{urlencode(course_params)}"
        course_response = requests.get(course_url, headers=headers)

        if course_response.status_code != 200:
            print("Error fetching course list:", course_response.text)
            return

        course_data = course_response.json().get("data", [])
        if not course_data:
            print("No active courses found.")
            return

        # Collect course codes from the response
        course_codes.extend([course["course_code"] for course in course_data])

        # Pagination handling
        pagination = course_response.json().get("pagination", {})
        if pagination and pagination.get("next"):
            print("Fetching next page of courses...")
            course_params['offset'] += course_params['limit']
        else:
            break

    total_duration = 0
    total_results_count = 0

    for academic_year, year_id in academic_year_ids.items():
        for course_code in course_codes:
            params = {
                'academicYearId': year_id,
                'courseCode': course_code,
                'limit': 100,
                'offset': 0
            }

            all_results = []
            results_count = 0
            start_time = time.time()

            while True:
                URL = f"{base_url}/api/analytics/task-results?{urlencode(params)}"
                print(f"\nMaking request to: {URL}")

                response = requests.get(URL, headers=headers)
                request_duration = time.time() - start_time
                total_duration += request_duration

                if response.status_code == 200:
                    json_response = response.json()
                    task_results = json_response.get("data", [])
                    all_results.extend(task_results)
                    results_count += len(task_results)
                    total_results_count += len(task_results)

                    pagination = json_response.get("pagination", {})
                    if pagination and pagination.get("next"):
                        print("Fetching next page...")
                        params['offset'] += params['limit']
                    else:
                        break
                else:
                    print(f"Error fetching task results for Year '{academic_year}', Course '{course_code}': {response.status_code}, {response.text}")
                    break

            year_duration = time.time() - start_time
            print(f"> Total results fetched for Year '{academic_year}', Course '{course_code}': {results_count}")
            print(f"> Total time taken: {year_duration:.2f} seconds\n")

    end_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global_duration = time.time() - global_start_time

    print("\n============")
    print(f"Total academic years fetched: {len(academic_year_ids)}")
    print(f"Total results fetched: {total_results_count}")
    print(f"Start Time: {start_time_formatted}")
    print(f"Finish Time: {end_time_formatted}")
    print(f"Total duration: {global_duration:.2f} seconds")
    print("============\n")
