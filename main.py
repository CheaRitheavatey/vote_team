import requests
import json
import os
from dotenv import load_dotenv

BASE_URL = "https://vote2.telekom.net/api/v1"
API_KEY = os.getenv("API_KEY")

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

print("Testing API key...")
test = requests.get(f"{BASE_URL}/vote/", headers=headers)
print("Status:", test.status_code)

if test.status_code != 200:
    print("❌ Invalid API key or permission issue.")
    exit()


print("\nCreating a new survey...")

vote_data = {
    "data": {
        "title": "Test Survey from API",
        "description": "This is a test survey created using the Vote REST API",
        "visibility": "public",
        "module": "Survey",
        "config": {
            "title": "Test Survey Config",
            "creator": "Andreas.Steffl@telekom.de",
            "public": True,
            "settings": {},
            "analysis_mode": "none",
            "structure": {},
            "admin_pw": "W5L:p7dl4(NKpQ_B7TTh"
        },
        "question_blocks": {
            "block_1": {
                "title": "Block 1",
                "questions": []
            }
        }
    }
}

response = requests.post(f"{BASE_URL}/vote", headers=headers, json=vote_data)
print("Create survey:", response.status_code, response.text)

if response.status_code == 200:
    result = response.json()
    print("✅ Survey created successfully!")
    print(json.dumps(result, indent=2))
else:
    print("⚠️ Survey creation failed.")
