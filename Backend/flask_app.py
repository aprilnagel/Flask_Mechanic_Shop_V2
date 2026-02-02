from app.models import db
from app import create_app
from flask_cors import CORS   # <-- ADD THIS

app = create_app("ProductionConfig")
CORS(app)                     # <-- AND THIS

@app.route("/health")
def health():
    return {"status": "ok"}, 200