import json
import os
import sys
from datetime import datetime, date, time
from dateutil import parser
from dateutil.relativedelta import relativedelta
import re

# Add the project root to sys.path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.llm import call_llm_model, DEFAULT_MODEL

# System prompt for extracting structured notes
system_prompt = '''
Extract the user's notes into the following structured fields:
1. Title: A concise title of the notes less than 5 words
2. Notes: The notes based on user input written in full sentences.
3. Tags (A list): At most 3 Keywords or tags that categorize the content of the notes.
4. Event_Date: If there's a specific date mentioned (like "今天", "明天", "后天", "下周一", "12月15日", "tomorrow", "next Friday"), extract and convert it to YYYY-MM-DD format. Use null if no specific date is found.
5. Event_Time: If there's a specific time mentioned (like "下午5点", "晚上8点", "5pm", "20:00", "8:30"), extract and convert it to HH:MM format (24-hour). Use null if no specific time is found.

Current date context: Today is 2025年10月12日 (October 12th, 2025).

Output in JSON format without ```json. Output title and notes in the language: {lang}.

Example:
Input: "今天下午5点去野餐".
Output:
{{
"Title": "今天野餐",
"Notes": "今天下午5点去野餐。",
"Tags": ["野餐", "户外活动"],
"Event_Date": "2025-10-12",
"Event_Time": "17:00"
}}

Input: "明天上午9点开会讨论项目".
Output:
{{
"Title": "项目会议",
"Notes": "明天上午9点开会讨论项目。", 
"Tags": ["会议", "项目"],
"Event_Date": "2025-10-13",
"Event_Time": "09:00"
}}
'''

def parse_date_time_fallback(user_input):
    """
    Fallback function to parse common Chinese date/time expressions when LLM fails.
    
    Args:
        user_input (str): User input text
    
    Returns:
        tuple: (date_str, time_str) in format (YYYY-MM-DD, HH:MM) or (None, None)
    """
    current_date = date.today()  # 2025-10-12
    parsed_date = None
    parsed_time = None
    
    # Chinese date patterns
    date_patterns = [
        (r'今天|today', 0),
        (r'明天|tomorrow', 1),  
        (r'后天', 2),
        (r'大后天', 3),
        (r'下周一|next monday', 7 - current_date.weekday()),
        (r'下周二|next tuesday', 7 - current_date.weekday() + 1),
        (r'下周三|next wednesday', 7 - current_date.weekday() + 2),
        (r'下周四|next thursday', 7 - current_date.weekday() + 3),
        (r'下周五|next friday', 7 - current_date.weekday() + 4),
        (r'下周六|next saturday', 7 - current_date.weekday() + 5),
        (r'下周日|next sunday', 7 - current_date.weekday() + 6),
    ]
    
    # Check for relative date patterns
    for pattern, days_offset in date_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            target_date = current_date + relativedelta(days=days_offset)
            parsed_date = target_date.strftime('%Y-%m-%d')
            break
    
    # Chinese time patterns
    time_patterns = [
        (r'凌晨(\d{1,2})点?', lambda m: f"{int(m.group(1)):02d}:00"),
        (r'早上(\d{1,2})点?', lambda m: f"{int(m.group(1)):02d}:00"),
        (r'上午(\d{1,2})点?', lambda m: f"{int(m.group(1)):02d}:00"),
        (r'中午(\d{1,2})点?', lambda m: f"{int(m.group(1)):02d}:00"),
        (r'下午(\d{1,2})点?', lambda m: f"{int(m.group(1)) + 12:02d}:00"),
        (r'晚上(\d{1,2})点?', lambda m: f"{int(m.group(1)) + 12:02d}:00"),
        (r'(\d{1,2})[:：](\d{1,2})', lambda m: f"{int(m.group(1)):02d}:{int(m.group(2)):02d}"),
        (r'(\d{1,2})pm|(\d{1,2})PM', lambda m: f"{int(m.group(1)) + 12:02d}:00"),
        (r'(\d{1,2})am|(\d{1,2})AM', lambda m: f"{int(m.group(1)):02d}:00"),
    ]
    
    # Check for time patterns
    for pattern, formatter in time_patterns:
        match = re.search(pattern, user_input)
        if match:
            try:
                parsed_time = formatter(match)
                # Validate time format
                time_parts = parsed_time.split(':')
                if len(time_parts) == 2 and 0 <= int(time_parts[0]) <= 23 and 0 <= int(time_parts[1]) <= 59:
                    break
                else:
                    parsed_time = None
            except (ValueError, AttributeError):
                parsed_time = None
    
    return parsed_date, parsed_time


def process_user_notes(language, user_input):
    """
    Process user input and extract structured note fields using LLM.
    
    Args:
        language (str): Target language for title and notes (e.g., "Chinese", "English")
        user_input (str): Raw user input to be processed
    
    Returns:
        dict: Structured note data with Title, Notes, Tags, Event_Date, Event_Time fields
    """
    system_prompt_filled = system_prompt.format(lang=language)
    
    messages = [
        {
            "role": "system",
            "content": system_prompt_filled,
        },
        {
            "role": "user",
            "content": user_input,
        }
    ]
    
    try:
        response_content = call_llm_model(DEFAULT_MODEL, messages)
        # Try to parse JSON response
        parsed_result = json.loads(response_content.strip())
        
        # Validate and potentially fix date/time fields
        if not parsed_result.get('Event_Date') or not parsed_result.get('Event_Time'):
            fallback_date, fallback_time = parse_date_time_fallback(user_input)
            
            if not parsed_result.get('Event_Date') and fallback_date:
                parsed_result['Event_Date'] = fallback_date
                
            if not parsed_result.get('Event_Time') and fallback_time:
                parsed_result['Event_Time'] = fallback_time
        
        return parsed_result
        
    except json.JSONDecodeError:
        # If JSON parsing fails, try fallback parsing for date/time and return basic structure
        fallback_date, fallback_time = parse_date_time_fallback(user_input)
        
        return {
            "Title": "Generated Note",
            "Notes": user_input,
            "Tags": [],
            "Event_Date": fallback_date,
            "Event_Time": fallback_time,
            "error": "Failed to parse LLM response as JSON, used fallback parsing",
            "raw_response": response_content
        }
    except Exception as e:
        # If LLM call fails, try fallback parsing
        fallback_date, fallback_time = parse_date_time_fallback(user_input)
        
        return {
            "Title": "Generated Note", 
            "Notes": user_input,
            "Tags": [],
            "Event_Date": fallback_date,
            "Event_Time": fallback_time,
            "error": f"LLM call failed: {str(e)}, used fallback parsing"
        }
# Run the main function if this script is executed
if __name__ == "__main__":
    result = process_user_notes("Chinese", "Get up tomorrow 7am")
    print("Chinese result:", json.dumps(result, indent=2, ensure_ascii=False))
    
    result = process_user_notes("English", "Learn python programming and docker")
    print("English result:", json.dumps(result, indent=2, ensure_ascii=False))