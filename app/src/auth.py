import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv('BASE_URL')
auth_endpoint = f"{base_url}/api/authorize"

auth_body = {
    'grant_type': 'client_credentials',
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET')
}

def get_auth_token():
    response = requests.post(url=auth_endpoint, data=auth_body)
    if response.status_code == 200:
        print("\n----------------------------------------------------------------")
        print(f"Auth successful: {response.status_code}")
        print("----------------------------------------------------------------\n")
        return response.json().get('data').get('access_token')
    else:
        print(f"Auth error: {response.status_code}, {response.text}")
        return None
