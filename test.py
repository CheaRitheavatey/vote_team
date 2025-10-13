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

# create new survey
def create_survey():
    survey_data = {
        "data": {
            "module": "Survey",
            "config": {
                "title": {"DE": "Test Survey"},
                "creator": "Andreas.Steffl@telekom.de",
                "public": True,
                "settings": {
                    "editable_answer": True,
                    "full_participation": True,
                    "participation_mode": "UNGUIDED",
                    "participation_val_mode": "COOKIE"
                },
                "analysis_mode": "FREE",
                "structure": {"start": 0, "components": {"0": {"default": -1}}},
                "admin_pw": "W5L:p7dl4(NKpQ_B7TTh"
            },
            "question_blocks": {
                "0": {
                    "title": {"DE": "Block 1"},
                    "description": {"DE": "First block"},
                    "questions": {
                        "0": {
                            "question": {"DE": "How old are you?"},
                            "question_type": "ChoiceSingle",
                            "settings": {"mandatory": True, "grid": False},
                            "config": {
                                "option_type": "TEXT",
                                "options": {"0": {"DE": "18 and below"}, "1": {"DE": "18-25"}, "2": {"DE": "25+"}}
                            },
                            "analysis_mode": "FREE"
                        }
                    },
                    "analysis_mode": "FREE",
                    "structure": {"start": 0, "components": {"0": {"default": -1}}}
                }
            }
        }
    }

    response = requests.post(f"{BASE_URL}/vote", headers=headers, json=survey_data)
    print("Create survey status:", response.status_code)
    print(response.text)

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

# submit answer
def submit_answer(enter_code, block_id, question_id, option_index):
    answer_data = {
        "blocks": {
            block_id: {
                "questions": {
                    question_id: {
                        "answers": [
                            {
                                "0": {
                                    "0": [
                                        {"answer": str(option_index), "cond_answer": "string"}
                                    ]
                                }
                            }
                        ],
                        "lang": "DE",
                        "skip": False
                    }
                }
            }
        }
    }

    response = requests.post(
        f"{BASE_URL}/answers/{enter_code}",
        headers=headers,
        json=answer_data
    )
    print("Submit answer status:", response.status_code)
    print(response.text)

def interactive_vote():
    enter_code = input("Enter survey code: ").strip()
    block_id = "0"
    question_id = "0"

    data = fetch_question(enter_code, block_id, question_id)
    if not data:
        return

    # show question and option
    question_text = data["question"]["DE"]
    options = [v["DE"] for k, v in data["config"]["options"].items()]
    print(f"Question: {question_text}")
    for i, opt in enumerate(options):
        print(f"{i}. {opt}")

    # user choose option index
    while True:
        try:
            choice = int(input("Enter your choice number (option ID): "))
            if 0 <= choice < len(options):
                break
            else:
                print("Invalid option number. Try again.")
        except ValueError:
            print("Please enter a valid integer.")

    submit_answer(enter_code, block_id, question_id, choice)

# get result
def get_survey_results(enter_code):
    response = requests.get(f"{BASE_URL}/analysis/{enter_code}/blocks", headers=headers)
    print("Results status:", response.status_code)
    print(response.text)


if __name__ == "__main__":
    while True:
        print("\n1. Fetch Surveys")
        print("2. Create Survey")
        print("3. Submit Answer")
        print("4. Get Results")
        print("5. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            fetch_surveys()
        elif choice == "2":
            create_survey()
        elif choice == "3":
            interactive_vote()
        elif choice == "4":
            code = input("Enter survey code: ")
            get_survey_results(code)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")
