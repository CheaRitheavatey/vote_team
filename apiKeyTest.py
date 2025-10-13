import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = "https://vote2.telekom.net/api/v1"
URL = "https://vote2.telekom.net"
headers = {
   "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

res = requests.get(f"{API_URL}/vote/", headers=headers)
print(res.status_code)
print(res.text)

# yes work api 

# Replace with one enter_code from your response
enter_code = "478708"
url = f"{URL}/surveys/{enter_code}"

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)