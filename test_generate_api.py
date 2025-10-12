#!/usr/bin/env python3
import requests
import json

def test_generate_notes():
    url = "http://127.0.0.1:5001/api/generate-notes"
    data = {
        "user_input": "Today I attended a team meeting at 2 PM where we discussed the new project roadmap. We need to implement user authentication, database optimization, and mobile app features by next quarter. The deadline is March 31st, 2024."
    }
    
    try:
        print("Testing Generate Notes API...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nParsed JSON:")
            print(f"Title: {result.get('title', 'N/A')}")
            print(f"Content: {result.get('content', 'N/A')}")
            print(f"Tags: {result.get('tags', 'N/A')}")
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_generate_notes()