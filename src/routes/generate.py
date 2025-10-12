from flask import Blueprint, jsonify, request
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.call_llm_model import process_user_notes

generate_bp = Blueprint('generate', __name__)


@generate_bp.route('/generate-notes', methods=['POST'])
def generate_notes():
    """
    Generate structured notes from natural language input using LLM.
    
    Expected JSON body:
    {
        "user_input": "natural language input",
        "language": "Chinese" or "English" (optional, defaults to "English")
    }
    
    Returns:
    {
        "title": "generated title",
        "content": "structured notes content", 
        "tags": ["tag1", "tag2", "tag3"]
    }
    """
    data = request.json or {}
    user_input = data.get('user_input')
    language = data.get('language', 'Chinese')  # Changed default to Chinese
    
    if not user_input:
        return jsonify({'error': 'No user_input provided'}), 400

    try:
        result = process_user_notes(language, user_input)
        
        # Check if there was an error in processing
        if 'error' in result:
            return jsonify(result), 500
        
        # Convert the result format to match frontend expectations    
        # The process_user_notes returns: {"Title": "...", "Notes": "...", "Tags": [...], "Event_Date": "...", "Event_Time": "..."}
        # Frontend expects: {"title": "...", "content": "...", "tags": [...], "event_date": "...", "event_time": "..."}
        response = {
            "title": result.get("Title", ""),
            "content": result.get("Notes", ""),
            "tags": result.get("Tags", []),
            "event_date": result.get("Event_Date", None),
            "event_time": result.get("Event_Time", None)
        }
            
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': f'Note generation failed: {str(e)}'}), 500