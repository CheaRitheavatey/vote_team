import requests
from dotenv import load_dotenv
import os

load_dotenv()  # load .env file

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://vote2.telekom.net/api/v1"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}



# fetch survey
response = requests.get(f"{BASE_URL}/vote/", headers=headers)

if response.status_code == 200:
    surveys = response.json()
    for key, survey in surveys.items():
        print("Title:", survey["title"]["DE"])
        print("Description:", survey["description"]["DE"])
        print("Enter Code:", survey["enter_code"])
        print("---")
else:
    print("Fail to fetch survey:", response.status_code, response.text)


# after able to fetch just the main thing , try fetching detail
# enter_code = "487612" 

# response = requests.get(f"{BASE_URL}/vote/{enter_code}/blocks", headers=headers)

# if response.status_code == 200:
#     blocks_data = response.json().get("data")  
#     if not blocks_data:
#         print("No blocks found in this survey.")
#     else:
#         for block_id, block in blocks_data.items():
#             title = block.get("title", {}).get("DE", "No title")
#             print("Block ID:", block_id)
#             print("Block Title:", title)
#             questions = block.get("questions", {})
#             print("Questions:")
#             for q_id, q in questions.items():
#                 q_text = q.get("question", {}).get("DE", "No question text")
#                 print(" -", q_text)
#             print("---")
# else:
#     print("Failed to fetch blocks:", response.status_code, response.text)