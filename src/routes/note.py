from flask import Blueprint, jsonify, request
from datetime import datetime, time, date
from src.models.note import Note, db

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        # optional fields: tags (list or comma string), event_date (YYYY-MM-DD), event_time (HH:MM[:SS])
        tags = data.get('tags')
        event_date = data.get('event_date')
        event_time = data.get('event_time')

        note = Note(title=data['title'], content=data['content'])
        note.set_tags(tags)
        if event_date:
            try:
                # Accept plain YYYY-MM-DD
                note.event_date = date.fromisoformat(event_date)
            except Exception:
                note.event_date = None
        if event_time:
            try:
                note.event_time = datetime.fromisoformat(event_time).time()
            except Exception:
                try:
                    # fallback parse HH:MM[:SS]
                    parts = event_time.split(':')
                    h, m = int(parts[0]), int(parts[1])
                    s = int(parts[2]) if len(parts) > 2 else 0
                    note.event_time = time(hour=h, minute=m, second=s)
                except Exception:
                    note.event_time = None
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        # optional updates
        if 'tags' in data:
            note.set_tags(data.get('tags'))
        if 'event_date' in data:
            ed = data.get('event_date')
            if ed:
                try:
                    note.event_date = date.fromisoformat(ed)
                except Exception:
                    note.event_date = None
            else:
                note.event_date = None
        if 'event_time' in data:
            et = data.get('event_time')
            if et:
                try:
                    note.event_time = datetime.fromisoformat(et).time()
                except Exception:
                    try:
                        parts = et.split(':')
                        h, m = int(parts[0]), int(parts[1])
                        s = int(parts[2]) if len(parts) > 2 else 0
                        note.event_time = time(hour=h, minute=m, second=s)
                    except Exception:
                        note.event_time = None
            else:
                note.event_time = None
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])

