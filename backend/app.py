from flask import Flask, request, jsonify
from utils.parser import extract_text_from_pdf
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "AI Job Copilot Backend Is Running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    resume_text = data.get("resume", "").lower()
    jd_text = data.get("jd", "").lower()

    resume_words = set(resume_text.split())
    jd_words = set(jd_text.split())

    matched = resume_words.intersection(jd_words)
    match_score = len(matched) / len(jd_words) * 100 if jd_words else 0

    missing = jd_words - resume_words

    return jsonify({
        "match_score": round(match_score, 2),
        "missing_keywords": list(missing)[:20]
    })

if __name__ == "__main__":
    app.run(debug=True)