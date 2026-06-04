# AI Job Copilot 🚀

A resume analysis and job application tracking system built with Flask and SQLite.

AI Job Copilot helps job seekers analyze resumes against job descriptions, identify missing skills, and manage job applications in one place.

---

## ✨ Features

### 📄 Resume Analyzer

* Upload resumes in PDF format
* Extract text using PyPDF2
* Compare resumes with job descriptions
* Detect matched and missing skills
* Hybrid keyword extraction
* Stopword filtering
* Phrase detection (e.g., Spring Boot, REST API)
* Section-aware resume parsing
* Weighted skill scoring

### 📋 Job Tracker

* Add job applications
* View all applications
* Update application status
* Delete applications
* SQLite database integration

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* SQLite

### Libraries

* PyPDF2
* Werkzeug

### Tools

* Git
* GitHub
* Thunder Client
* Postman

---

## 📂 Project Structure

```text
backend/
├── app.py
├── jobs.db
├── uploads/
└── utils/
    └── parser.py
```

---

## 🔗 API Endpoints

### Resume APIs

| Method | Endpoint   | Description                            |
| ------ | ---------- | -------------------------------------- |
| POST   | `/upload`  | Upload and extract resume text         |
| POST   | `/analyze` | Analyze resume against job description |

### Job Tracker APIs

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| POST   | `/add-job`         | Add a new application     |
| GET    | `/jobs`            | Fetch all applications    |
| PUT    | `/update-job/<id>` | Update application status |
| DELETE | `/delete-job/<id>` | Delete an application     |

---

## 📊 Sample Analysis Output

```json
{
  "match_score": 61.54,
  "matched_keywords": [
    "java",
    "mysql",
    "rest api"
  ],
  "missing_keywords": [
    "aws",
    "spring boot"
  ]
}
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Anshrai446/Ai-Job-Copilot.git
```

### Navigate to Backend

```bash
cd Ai-Job-Copilot/backend
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Server starts at:

```text
http://127.0.0.1:5000
```

---

## 🚀 Current Status

### Completed

* Resume upload and parsing
* Resume-JD matching engine
* Weighted scoring system
* SQLite-based job tracker
* Full CRUD APIs

### Planned Improvements

* Modular project architecture
* Frontend dashboard
* Authentication
* AI-powered resume recommendations
* Deployment

---

## 🎯 Learning Outcomes

This project demonstrates:

* REST API Development
* Backend Engineering
* Database Design
* File Handling
* Software Architecture
* Git & GitHub Workflow
* Problem Solving

---

## 👨‍💻 Author

**Ansh Rai**

Computer Science Engineering Student

Building real-world projects to strengthen backend engineering and software development skills.
