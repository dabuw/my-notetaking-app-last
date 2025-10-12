import requests
import json

# 简单测试
url = "http://127.0.0.1:5001/api/generate-notes"
data = {"user_input": "今天开了个会，讨论项目进度"}

print("Testing API...")
response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")