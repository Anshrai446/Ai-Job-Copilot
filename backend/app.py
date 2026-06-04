from flask import Flask, request, jsonify
from utils.parser import extract_text_from_pdf
from werkzeug.utils import secure_filename
import os
import re
import sqlite3

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
        if any(keyword in line for keyword in ["skill", "technology", "tools"]):
            capture = True
            continue

        # stop when new section starts
        if capture and ("education" in line or "experience" in line):
            break

        if capture:
            skills_section.append(line)

    return " ".join(skills_section)
def extract_phrases(text):
    text = text.lower()
    phrases = set()

    if "rest api" in text:
        phrases.add("rest api")
    if "spring boot" in text:
        phrases.add("spring boot")

    return phrases
def normalize_keywords(keywords):
    normalized = set(keywords)

    if "rest api" in normalized:
        normalized.discard("rest")
        normalized.discard("apis")

    if "spring boot" in normalized:
        normalized.discard("spring")
        normalized.discard("boot")

    return normalized

def calculate_weighted_score(matched, jd_final):
  matched_score = sum(WEIGHTS.get(skill, 1) for skill in matched)
  total_score = sum(WEIGHTS.get(skill, 1) for skill in jd_final)

  return (matched_score / total_score) * 100 if total_score else 0
def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
WEIGHTS = {
    "java": 3,
    "spring boot": 4,
    "sql": 3,
    "mysql": 3,

    "aws": 2,
    "docker": 2,
    "kubernetes": 2,
    "rest api": 2,   

    "html": 1,
    "css": 1,
    "javascript": 1
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

    raw_resume = data.get("resume", "")
    skills_section = extract_skills_section(raw_resume)
    jd_text = data.get("jd", "")

# fallback if section not found
    resume_text = skills_section if skills_section.strip() else raw_resume

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
    
    resume_final = normalize_keywords(resume_final)
    jd_final = normalize_keywords(jd_final)

# Step 6: matching
    matched = resume_final.intersection(jd_final)
    missing = jd_final - resume_final


    match_score = calculate_weighted_score(matched, jd_final)

    return jsonify({
    "match_score": round(match_score, 2),
    "matched_keywords": sorted(list(matched)),
    "missing_keywords": sorted(list(missing))
})
@app.route("/add-job", methods=["POST"])
def add_job():
    data = request.json

    company = data.get("company")
    role = data.get("role")
    status = data.get("status", "Applied")

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO jobs (company, role, status) VALUES (?, ?, ?)",
        (company, role, status)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Job added successfully"
    })
@app.route("/jobs", methods=["GET"])
def get_jobs():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()

    conn.close()

    jobs = []

    for row in rows:
        jobs.append({
            "id": row[0],
            "company": row[1],
            "role": row[2],
            "status": row[3]
        })

    return jsonify(jobs)
@app.route("/update-job/<int:id>", methods=["PUT"])
def update_job(id):
    data = request.json

    status = data.get("status")

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE jobs SET status = ? WHERE id = ?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Job updated successfully"
    })
@app.route("/delete-job/<int:id>", methods=["DELETE"])
def delete_job(id):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM jobs WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Job deleted successfully"
    })
#  Run server
if __name__ == "__main__":
    init_db()
    app.run(debug=True)