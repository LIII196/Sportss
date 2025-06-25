from waitress import serve
from app import app  # assuming your Flask app is created in app.py

serve(app, host="0.0.0.0", port=8000)
