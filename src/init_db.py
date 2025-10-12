"""Small helper to (re)create the database tables for the Flask app.
WARNING: Running this will drop existing data if using a file-based sqlite DB.

Usage: python src/init_db.py
"""
import os
import sys

# make sure repo root is on path so `src` imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
from src.models.user import db


with app.app_context():
    # Drop all and recreate (simple approach for this lab). Be careful in production.
    db.drop_all()
    db.create_all()
    print('Database tables created/recreated.')
