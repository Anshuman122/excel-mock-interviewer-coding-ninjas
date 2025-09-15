# 📊 AI-Powered Excel Mock Interviewer

## 📌 Problem Context
Excel proficiency is a **core skill** for Finance, Operations, and Data Analytics roles at Coding Ninjas.  

Currently, Excel skill interviews are:
- ⏳ **Time-consuming** for senior analysts  
- ⚖️ **Inconsistent** in evaluation  
- 🚧 A **bottleneck** in the hiring pipeline  

👉 This project solves these issues by creating an **AI-powered interviewer** that:
- Automates Excel interviews  
- Evaluates candidates intelligently  
- Generates performance summaries  

---

## 🏗️ Architecture Overview
**Flow:**  
`Candidate → React Frontend (Vercel) → FastAPI Backend (Render) → Gemini API (Google Generative AI) → Evaluation Engine (rubric-based scoring + Excel validation) → Transcript Writer + PDF Report Generator`

**Components:**
- **Frontend:** React + Vite (Vercel)  
- **Backend:** FastAPI (Render)  
- **LLM:** Google Gemini (Generative AI)  
- **Data Handling:** Session manager + transcripts  
- **Reports:** JSON + downloadable PDF  

---

## ⚡ Stack Choices & Justification

| Component     | Choice                | Why? |
|---------------|-----------------------|------|
| **Frontend**  | React (Vite) on Vercel | Fast deploy, interactive UI, free hosting |
| **Backend**   | FastAPI on Render     | Lightweight, async, production-ready |
| **AI Model**  | Google Gemini API     | Strong natural language eval, easy integration |
| **Data**      | In-memory + transcripts | Simple PoC; extendable to DB in future |
| **File Handling** | Pandas + openpyxl  | Excel validation at file-level |
| **Hosting**   | Vercel + Render       | Free-tier friendly, quick deploys |

---

## 🛠️ Setup Instructions

### 🔹 Backend (FastAPI)
```bash
git clone https://github.com/Anshuman122/excel-mock-interviewer-coding-ninjas.git
cd backend
pip install -r requirements.txt
python -m uvicorn backend.main: app --reload
```

### 🔹 Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
```bash
👉 Access at http://localhost:5173
```
## 🔹 Deployable links

Frontend (Vercel): Live App

Backend (Render): API Server

## * Sample Transcripts

Found under /docs/samples/:

session1_transcript.json – Candidate answering basic Excel Qs.

session2_transcript.json – Candidate attempting file-upload question.

## * Features

Multi-turn structured interview (text, design, file questions).

Intelligent evaluation:

Text/design → Gemini-based evaluation.

Excel → Formula validation + report.

Transcript storage + downloadable report.

CORS-enabled frontend ↔ backend integration.

## * How to Test Locally

```bash
Run backend → http://127.0.0.1:8000

Run frontend → update backend.js API URL to local server.
```
## * Try:

Start Interview.

Answer text questions.

Upload Excel file.

End → download transcript/report.