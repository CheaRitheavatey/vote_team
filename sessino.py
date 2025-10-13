import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://vote2.telekom.net/api/v1"
API_KEY = os.getenv("API_KEY")

# A small pool of random user agents to mimic unique sessions
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    "Mozilla/5.0 (Android 13; Mobile; rv:120.0)"
]


def create_session():
    """Create a new session with random headers each time."""
    session = requests.Session()
    session.headers.update({
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": random.choice(USER_AGENTS)
    })
    return session


def fetch_question(session, enter_code, block_id, question_id):
    response = session.get(
        f"{BASE_URL}/vote/{enter_code}/blocks/{block_id}/questions/{question_id}"
    )
    if response.status_code != 200:
        print("❌ Failed to fetch question:", response.status_code, response.text)
        return None
    return response.json()["data"]


def submit_answer(session, enter_code, block_id, question_id, option_index):
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

    response = session.post(
        f"{BASE_URL}/answers/{enter_code}",
        json=answer_data
    )
    print("✅ Submit answer status:", response.status_code)
    print(response.text)


def interactive_vote():
    enter_code = input("Enter survey code: ").strip()
    block_id = "0"
    question_id = "0"

    while True:
        session = create_session()  # ← new session per attempt
        data = fetch_question(session, enter_code, block_id, question_id)
        if not data:
            print("No data found or invalid code.")
            break

        # Display question and options
        question_text = data["question"]["DE"]
        options = [v["DE"] for k, v in data["config"]["options"].items()]
        print(f"\nQuestion: {question_text}")
        for i, opt in enumerate(options):
            print(f"{i}. {opt}")

        try:
            choice = int(input("Enter your choice number (option ID): "))
            if 0 <= choice < len(options):
                submit_answer(session, enter_code, block_id, question_id, choice)
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

        again = input("Submit another vote? (y/n): ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    interactive_vote()
