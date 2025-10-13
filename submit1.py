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

def fetch_question(enter_code, block_id, question_id):
    response = requests.get(
        f"{BASE_URL}/vote/{enter_code}/blocks/{block_id}/questions/{question_id}",
        headers=headers
    )
    if response.status_code != 200:
        print("Failed to fetch question:", response.status_code, response.text)
        return None
    return response.json()["data"]

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

    # Show question and options
    question_text = data["question"]["DE"]
    options = [v["DE"] for k, v in data["config"]["options"].items()]
    print(f"Question: {question_text}")
    for i, opt in enumerate(options):
        print(f"{i}. {opt}")

    # Ask user to choose option index
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

if __name__ == "__main__":
    interactive_vote()
