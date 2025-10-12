import requests
import json

# Test the Generate Notes API
url = "http://127.0.0.1:5001/api/generate-notes"
payload = {
    "user_input": "Meeting tomorrow 3pm with John about project updates",
    "language": "English"  
}

print("Testing Generate Notes API...")
try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nGenerated Notes:")
        print(f"Title: {data.get('title')}")
        print(f"Content: {data.get('content')}")  
        print(f"Tags: {data.get('tags')}")
    
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")