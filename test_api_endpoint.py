#!/usr/bin/env python3
"""
Test HTTP API endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5001"

def test_generate_notes_api():
    """Test the /api/generate-notes endpoint"""
    
    url = f"{BASE_URL}/api/generate-notes"
    
    test_cases = [
        {
            "user_input": "今天下午5点去野餐",
            "expected_fields": ["title", "content", "tags", "event_date", "event_time"]
        },
        {
            "user_input": "明天上午9点开会讨论项目",
            "expected_fields": ["title", "content", "tags", "event_date", "event_time"]
        }
    ]
    
    print("Testing /api/generate-notes endpoint:")
    print("="*50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing input: {test_case['user_input']}")
        
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={"user_input": test_case["user_input"]},
                timeout=30
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=4, ensure_ascii=False)}")
                
                # Check if expected fields are present
                missing_fields = []
                for field in test_case["expected_fields"]:
                    if field not in data:
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"   ⚠️  Missing fields: {missing_fields}")
                else:
                    print("   ✅ All expected fields present")
                    
                    # Validate date and time format
                    if data.get("event_date"):
                        print(f"   📅 Event Date: {data['event_date']}")
                    if data.get("event_time"):
                        print(f"   ⏰ Event Time: {data['event_time']}")
                        
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def check_server_status():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

if __name__ == "__main__":
    print("Checking server status...")
    if check_server_status():
        print("\nWaiting for server to be ready...")
        time.sleep(2)
        test_generate_notes_api()
    else:
        print("Please start the server first with: .venv\\Scripts\\python.exe src\\main.py")