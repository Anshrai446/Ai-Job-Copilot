from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from utils.parser import extract_text_from_pdf
from services.resume_service import analyze_resume
import os


resume_bp = Blueprint("resume", __name__)

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@resume_bp.route("/upload", methods=["POST"])
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


@resume_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    raw_resume = data.get("resume", "")
    jd_text = data.get("jd", "")

    result = analyze_resume(raw_resume, jd_text)

    return jsonify(result)