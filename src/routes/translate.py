from flask import Blueprint, jsonify, request
from src.llm import translate

translate_bp = Blueprint('translate', __name__)


@translate_bp.route('/translate', methods=['POST'])
def translate_text():
    data = request.json or {}
    text = data.get('text')
    lang = data.get('lang', 'zh-CN')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        translated = translate(text, lang)
        return jsonify({'translation': translated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
