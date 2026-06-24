
# AI Job Agent🤖💼

An AI-powered job search agent that leverages large language models to analyze job descriptions, match candidate skills, optimize resumes, and automate application submissions.
An autonomous, AI-powered assistant designed to automate and optimize the job search process. The system parses resumes, calculates ATS scores, analyzes skill gaps using Generative AI, and fetches real-time job recommendations.

---

## 🚀 Features

* **📄 Resume Upload & Parsing**
  * Upload resumes in PDF format.
  * Extracts text automatically from the uploaded resume.
* **🧠 AI Resume Analysis**
  * Uses Generative AI to analyze the resume.
  * Generates detailed insights about the candidate's profile.
* **🛠 Skill Extraction**
  * Detects technical and professional skills from the resume.
  * Displays extracted skills in an interactive dashboard.
* **📊 ATS Score Calculation**
  * Calculates an Applicant Tracking System (ATS) score.
  * Helps users understand how ATS-friendly their resume is.
* **🎯 Skill Gap Analysis**
  * Identifies missing skills required for recommended jobs.
  * Helps users improve their employability.
* **💼 Job Recommendation System**
  * Matches resume skills against job requirements.
  * Provides ranked job recommendations with match percentages.
* **🌐 Live Job Search Integration**
  * Fetches real-time job opportunities using Job Search APIs.
  * Displays company name, location, and application links.
* **🎨 Interactive Dashboard**
  * Modern and responsive user interface.
  * **Displays:** Resume details, ATS score, Skill analysis, Missing skills, AI insights, and Recommended jobs.

---

## 🔄 System Workflow

```text
Resume Upload 
     ↓ 
Resume Parsing 
     ↓ 
Skill Extraction 
     ↓ 
ATS Score Analysis 
     ↓ 
Skill Gap Detection 
     ↓ 
AI Resume Analysis 
     ↓ 
Job Recommendation Engine 
     ↓ 
Live Job Search API 
     ↓ 
Interactive Dashboard
```

---

## 🛠️ Technology Stack

### Frontend
* HTML5
* CSS3
* Jinja2 Templates

### Backend
* Python
* Flask

### Libraries
* `pdfplumber` (PDF text extraction)
* `pandas` (Data manipulation)
* `requests` (API HTTP requests)
* `google-generativeai` (Gemini API integration)
* `reportlab` (PDF generation)

### APIs Used
RAPIDAPI_KEY=c9d7d5dee6msh20246da560c866p1d30c8jsn9f1aff6c6933
NGROK_AUTHTOKEN=3FRMxgVGB0CguFPPVbCXKMIQeTx_3WcndHgbZ13vchUjnGjGx

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd ai-job-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   RAPIDAPI_KEY=your_rapidapi_key_here
   FLASK_SECRET_KEY=your_secret_key
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

   ##Sample Output📄
   # Sample Output

## AI Career Assistant Report

### Resume Analysis Dashboard

| Metric          | Result    |
| --------------- | --------- |
| ATS Score       | 92/100    |
| Skills Detected | 8         |
| Job Matches     | 15        |
| Resume Strength | Excellent |

---

## Resume Summary

The uploaded resume belongs to a candidate pursuing a Bachelor's degree in Artificial Intelligence and Machine Learning with internship experience in AI and Web Development. The profile demonstrates strong programming fundamentals, practical project exposure, and career readiness for software and AI-related roles.

---

## Skills Detected

### Programming Languages

* Python
* Java
* C

### Web Technologies

* HTML
* CSS

### AI & Data Skills

* Artificial Intelligence
* Machine Learning

### Tools

* Git

---

## ATS Analysis

### ATS Score: 92/100

### Strengths

✅ Well-structured resume format

✅ Relevant technical skills included

✅ Internship experience present

✅ Education details clearly mentioned

✅ Industry-relevant keywords detected

### Areas for Improvement

⚠ Add LinkedIn profile URL

⚠ Add GitHub portfolio links

⚠ Include certifications section

⚠ Add measurable project achievements

⚠ Include professional summary section

---

## AI Insights

### Candidate Strengths

* Strong Python programming skills
* Exposure to Artificial Intelligence concepts
* Practical internship experience
* Good technical foundation
* Suitable for entry-level software roles

### Suggested Improvements

* Learn SQL and Database Management
* Build Machine Learning projects
* Learn FastAPI and Flask
* Practice Data Structures & Algorithms
* Gain Cloud Computing experience

---

## Missing High-Demand Skills

To improve employability and ATS performance:

* SQL
* FastAPI
* Flask
* Pandas
* NumPy
* Scikit-Learn
* TensorFlow
* Docker
* AWS
* REST APIs

---

## Recommended Jobs

| Job Title                 | Match Score |
| ------------------------- | ----------- |
| AI/ML Intern              | 96%         |
| Python Developer          | 94%         |
| Backend Developer         | 90%         |
| Software Engineer Intern  | 88%         |
| Data Analyst              | 86%         |
| Machine Learning Engineer | 84%         |
| Full Stack Developer      | 82%         |
| Data Science Intern       | 80%         |

---

## Career Roadmap

### Beginner Level

* Python Advanced Concepts
* SQL Fundamentals
* Git & GitHub

### Intermediate Level

* FastAPI
* Flask
* REST API Development
* Database Integration

### Advanced Level

* Machine Learning Projects
* Deep Learning
* Cloud Deployment
* Docker & Kubernetes

---

## Recommended Companies

### Product-Based Companies

* Google
* Microsoft
* Amazon
* Adobe
* Salesforce

### Service-Based Companies

* Infosys
* TCS
* Cognizant
* Wipro
* Accenture

---

## Future Enhancements

* AI Resume Ranking System
* Resume Builder
* Interview Question Generator
* LinkedIn Profile Analysis
* Skill Gap Detection
* Multi-Resume Comparison
* Job Alert Notifications
* Salary Prediction System
* AI Career Chatbot
* Cloud Deployment

---

##Author

Susmija Punnam — Designed and developed an AI-driven Resume Career Assistant that analyzes resumes, identifies key skills, evaluates ATS compatibility, and recommends relevant career opportunities using Python, AI/NLP techniques, and job-matching algorithms.

⭐ If this project helps you explore AI-powered career guidance and resume analysis, consider giving the repository a star on GitHub.


