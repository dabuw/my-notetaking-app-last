#!/usr/bin/env python3
"""
Test script for the generate-notes API endpoint
"""

import json
import sys
import os

# Add src to path
sys.path.append('src')

from call_llm_model import process_user_notes

def test_generate_notes():
    """Test the note generation function directly"""
    
    test_cases = [
        "今天下午5点去野餐",
        "明天上午9点开会",
        "后天晚上8点看电影",
        "下周一下午3点牙科预约",
        "Learning Python and Docker",
        "Meeting with client at 2pm tomorrow"
    ]
    
    print("Testing generate notes function:")
    print("="*50)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. Input: {test_input}")
        try:
            if any(char in test_input for char in '今天明天后天下周一二三四五六日上午下午晚上凌晨'):
                language = "Chinese"
            else:
                language = "English"
                
            result = process_user_notes(language, test_input)
            print(f"   Language: {language}")
            print(f"   Result: {json.dumps(result, indent=4, ensure_ascii=False)}")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    test_generate_notes()