


# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("API_KEY")
# BASE_URL = "https://vote2.telekom.net/api/v1"

# headers = {
#     "x-api-key": API_KEY,
#     "Content-Type": "application/json"
# }

# def fetch_surveys():
#     response = requests.get(f"{BASE_URL}/vote/", headers=headers)
#     if response.status_code == 200:
#         surveys = response.json()
#         for key, survey in surveys.items():
#             title = (survey.get("title") or {}).get("DE", "No title")
#             description = (survey.get("description") or {}).get("DE", "No description")
#             enter_code = survey.get("enter_code", "N/A")
#             print(f"Title: {title}")
#             print(f"Description: {description}")
#             print(f"Enter Code: {enter_code}")
#             print("---")
#     else:
#         print("Failed to fetch surveys:", response.status_code, response.text)

# def fetch_questions(enter_code):
#     response = requests.get(f"{BASE_URL}/vote/{enter_code}/blocks", headers=headers)
#     if response.status_code == 200:
#         blocks_data = response.json().get("data", {})
#         return blocks_data
#     else:
#         print("Failed to fetch blocks:", response.status_code, response.text)
#         return {}

# def submit_answer(enter_code, block_id, question_id, answer_list):
#     answer_data = {
#         "blocks": {
#             block_id: {
#                 "questions": {
#                     question_id: {
#                         "answers": [
#                             {"value": {"DE": answer_list}} 
#                         ]
#                     }
#                 }
#             }
#         }
#     }
#     response = requests.post(
#         f"{BASE_URL}/answers/{enter_code}",
#         headers=headers,
#         json=answer_data
#     )
#     print("Submit answer status:", response.status_code)
#     print(response.text)

# def interactive_vote():
#     fetch_surveys()
#     enter_code = input("Enter survey code: ").strip()
#     blocks = fetch_questions(enter_code)
#     if not blocks:
#         print("No blocks found in this survey.")
#         return

#     for block_id, block in blocks.items():
#         print("\nBlock: {block.get('title', {}).get('DE', 'No title')}")
#         questions = block.get("questions", {})
#         for q_id, q in questions.items():
#             question_text = q.get("question", {}).get("DE", "No question text")
#             q_type = q.get("question_type")
#             options_dict = q.get("config", {}).get("options", {})
#             options = [v.get("DE") for k, v in options_dict.items()]
#             print(f"\nQuestion: {question_text}")
#             print("Options:", ", ".join(options))

#             # get user's answer
#             if q_type == "ChoiceSingle":
#                 ans = input("Enter your answer (single choice): ").strip()
#                 submit_answer(enter_code, block_id, q_id, [ans])
#             elif q_type == "ChoiceMultiple":
#                 ans = input("Enter your answers (comma separated): ").strip().split(",")
#                 ans = [a.strip() for a in ans]
#                 submit_answer(enter_code, block_id, q_id, ans)
#             else:
#                 print(f"Question type '{q_type}' not supported yet.")

# if __name__ == "__main__":
#     interactive_vote()


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

    data = response.json()["data"]
    question_text = data["question"]["DE"]
    options = [v["DE"] for k, v in data["config"]["options"].items()]
    return question_text, options

def submit_answer(enter_code, block_id, question_id, answer_text):
    answer_data = {
        "blocks": {
            block_id: {
                "questions": {
                    question_id: {
                        "answers": [
                            {
                                "value": {"DE": answer_text},
                                "lang": "DE"   },
                            
                        ]
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

    q = fetch_question(enter_code, block_id, question_id)
    if not q:
        return

    question_text, options = q
    print(f"Question: {question_text}")
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")

    while True:
        choice = input(f"Enter your choice (1-{len(options)}): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Invalid choice. Try again.")
            continue
        selected_option = options[int(choice) - 1]  # map number to string
        break

    submit_answer(enter_code, block_id, question_id, selected_option)
    print(f"You selected: {selected_option}")

if __name__ == "__main__":
    interactive_vote()
