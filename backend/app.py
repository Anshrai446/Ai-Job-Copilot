from flask import Flask, request, jsonify
from utils.parser import extract_text_from_pdf
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)

#  Upload folder setup
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#  Clean text function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove symbols
    return text.split()
def extract_keywords(words):
    return {
        word for word in words
        if len(word) > 2 and word not in STOPWORDS
    }
#  Skill set (expand later)
SKILLS = {
    "java", "python", "sql", "javascript", "react", "node", "spring",
    "boot", "flask", "django", "mongodb", "mysql", "aws", "docker",
    "kubernetes", "html", "css", "rest", "api"
}

STOPWORDS = {
    "the", "and", "for", "with", "a", "an", "to", "of", "in",
    "on", "at", "by", "is", "are", "looking", "developer",
    "experience", "knowledge", "skills", "work",
    "backend", "frontend", "engineer"
}

#  Home route
@app.route("/")
def home():
    return "AI Job Copilot Backend Is Running 🚀"

#  Upload + Extract
@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": filename,
        "extracted_text": extracted_text[:500]
    })

#  Analyze Resume vs Job Description
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    resume_text = data.get("resume", "")
    jd_text = data.get("jd", "")

    resume_words = set(clean_text(resume_text))
    jd_words = set(clean_text(jd_text))

    #  Extract only skills
    resume_skills = resume_words.intersection(SKILLS)
    jd_skills = jd_words.intersection(SKILLS)

# 🔥 Dynamic keywords (flexible)
    resume_keywords = extract_keywords(resume_words)
    jd_keywords = extract_keywords(jd_words)

# 🔥 Hybrid merge
    resume_final = resume_skills.union(resume_keywords)
    jd_final = jd_skills.union(jd_keywords)

    matched = resume_final.intersection(jd_final)
    missing = jd_final - resume_final

    match_score = (len(matched) / len(jd_final)) * 100 if jd_final else 0

    return jsonify({
    "match_score": round(match_score, 2),
    "matched_keywords": list(matched),
    "missing_keywords": list(missing)
})

#  Run server
if __name__ == "__main__":
    app.run(debug=True)