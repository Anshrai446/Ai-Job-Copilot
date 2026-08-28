from flask import Flask, request, jsonify
from database.db import (
    init_db,
    add_job,
    get_all_jobs,
    update_job_status,
    delete_job
)
from routes.resume_routes import resume_bp

app = Flask(__name__)
app.register_blueprint(resume_bp)

#  Home route
@app.route("/")
def home():
    return "AI Job Copilot Backend Is Running 🚀"


@app.route("/add-job", methods=["POST"])
def add_job_route():
    data = request.json

    company = data.get("company")
    role = data.get("role")
    status = data.get("status", "Applied")

    add_job(company, role, status)

    return jsonify({
        "message": "Job added successfully"
    })
@app.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = get_all_jobs()

    return jsonify(jobs)
@app.route("/update-job/<int:id>", methods=["PUT"])
def update_job(id):
    data = request.json
    status = data.get("status")

    update_job_status(id, status)

    return jsonify({
        "message": "Job updated successfully"
    })
@app.route("/delete-job/<int:id>", methods=["DELETE"])
def delete_job_route(id):
    delete_job(id)

    return jsonify({
        "message": "Job deleted successfully"
    })
#  Run server
if __name__ == "__main__":
    init_db()
    app.run(debug=True)