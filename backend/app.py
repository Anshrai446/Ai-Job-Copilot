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

def extract_skills_section(text):
    lines = text.lower().split("\n")

    skills_section = []
    capture = False

    for line in lines:
        if "skill" in line:
            capture = True
            continue

        # stop when new section starts
        if capture and ("education" in line or "experience" in line):
            break

        if capture:
            skills_section.append(line)

    return " ".join(skills_section)
def extract_phrases(text):
    phrases = set()

    if "rest api" in text:
        phrases.add("rest api")
    if "spring boot" in text:
        phrases.add("spring boot")

    return phrases
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

    resume_text = extract_skills_section(data.get("resume", ""))
    jd_text = data.get("jd", "")

# Step 1: base words
    resume_words = set(clean_text(resume_text))
    jd_words = set(clean_text(jd_text))

# Step 2: known skills
    resume_skills = resume_words.intersection(SKILLS)
    jd_skills = jd_words.intersection(SKILLS)

# Step 3: dynamic keywords
    resume_keywords = extract_keywords(resume_words)
    jd_keywords = extract_keywords(jd_words)

# Step 4: create final sets FIRST
    resume_final = resume_skills.union(resume_keywords)
    jd_final = jd_skills.union(jd_keywords)

# Step 5: phrase detection (AFTER creation)
    resume_phrases = extract_phrases(resume_text)
    jd_phrases = extract_phrases(jd_text)

    resume_final = resume_final.union(resume_phrases)
    jd_final = jd_final.union(jd_phrases)

# Step 6: matching
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