from app.models import db
from app import create_app

app = create_app("ProductionConfig")

@app.route("/health")
def health():
    return {"status": "ok"}, 200