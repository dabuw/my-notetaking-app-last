import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Ensure repository root is importable when running on Vercel
CURRENT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    # Import and configure the Flask app
    from flask import Flask
    from flask_cors import CORS
    from src.models.user import db
    from src.routes.user import user_bp
    from src.routes.note import note_bp
    from src.routes.translate import translate_bp
    from src.routes.generate import generate_bp
    from src.routes.tags import tags_bp
    from src.models.note import Note
    
    # Create Flask app instance
    app = Flask(__name__, static_folder=os.path.join(REPO_ROOT, 'src', 'static'))
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-for-vercel')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS for all routes
    CORS(app)
    
    # Configure database
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Ensure sslmode=require if not explicitly set (Neon requires SSL)
        if database_url.startswith('postgres') and 'sslmode=' not in database_url:
            sep = '&' if '?' in database_url else '?'
            database_url = f"{database_url}{sep}sslmode=require"
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback to in-memory SQLite for Vercel if no DATABASE_URL
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(note_bp, url_prefix='/api')
    app.register_blueprint(translate_bp, url_prefix='/api')
    app.register_blueprint(generate_bp, url_prefix='/api')
    app.register_blueprint(tags_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Add health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Vercel deployment is working'}
    
    # Debug endpoint to check routes
    @app.route('/api/debug/routes')
    def debug_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': rule.rule
            })
        return {'routes': routes, 'blueprints': list(app.blueprints.keys())}
    
    # Serve static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            from flask import send_from_directory
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                from flask import send_from_directory
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

except Exception as e:
    # Create a minimal error-reporting app if main app fails
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/api/error')
    def error_info():
        return jsonify({
            'error': 'Application initialization failed',
            'details': str(e),
            'type': type(e).__name__
        }), 500
    
    @app.route('/')
    def root_error():
        return f"Application startup error: {str(e)}", 500


