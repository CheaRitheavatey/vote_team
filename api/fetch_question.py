import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://vote2.telekom.net/api/v1"
API_KEY = os.getenv("API_KEY")

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}
# get questiion and answer
def fetch_question(enter_code, block_id, question_id):
    response = requests.get(
        f"{BASE_URL}/vote/{enter_code}/blocks/{block_id}/questions/{question_id}",
        headers=headers
    )
    if response.status_code != 200:
        print("Failed to fetch question:", response.status_code, response.text)
        return None
    return response.json()["data"]


# fetch survye
def fetch_surveys():
    response = requests.get(f"{BASE_URL}/vote/", headers=headers)
    if response.status_code == 200:
        surveys = response.json()
        for key, survey in surveys.items():
            title = (survey.get("title") or {}).get("DE", "No title")
            description = (survey.get("description") or {}).get("DE", "No description")
            enter_code = survey.get("enter_code", "N/A")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"Enter Code: {enter_code}")
            print("---")
    else:
        print("Failed to fetch surveys:", response.status_code, response.text)
