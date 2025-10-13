import os
import sys

# Ensure repository root is importable when running on Vercel
CURRENT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Expose the WSGI app for Vercel Python runtime
from src.main import app  # noqa: E402


