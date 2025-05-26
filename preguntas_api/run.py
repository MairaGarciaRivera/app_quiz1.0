from waitress import serve
from app import app

print("Starting server on http://localhost:5000")
serve(app, host='0.0.0.0', port=5000)