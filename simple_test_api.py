import requests
import json
import time

# Wait for server to be ready
time.sleep(3)

url = "http://127.0.0.1:5001/api/generate-notes"
payload = {
    "user_input": "今天下午5点去野餐"
}

try:
    print(f"Testing: {payload['user_input']}")
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")