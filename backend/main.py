import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse

from .session_manager import (
    create_session, get_current_question, get_session, append_transcript_entry,
    advance_to_next, write_transcript, get_transcript_file
)
from .llm_rubric import evaluate_answer
from .generate_report import generate_report  # for file-based evaluation

# Configure Gemini if key present
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY not set. LLM features disabled.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000","https://anshuman-excel-mock-interviewer-coding-ninja.vercel.app",],  # add your frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    answer: str

@app.get("/")
def home():
    return {"message": "✅ Excel Mock Interviewer Backend is Running on Render!"}

@app.get("/ping")
def ping():
    return {"message": "Server is running!"}

@app.post("/session")
def start_session():
    session_id = create_session()
    # After creating we return a welcome + first question
    q = get_current_question(session_id)
    return {"session_id": session_id, "question": q}

@app.post("/session/{session_id}/message")
async def submit_text_answer(session_id: str, msg: MessageRequest):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="session not found")

    # Get current question
    q = get_current_question(session_id)
    if not q:
        
        return {"next_question": None, "session_done": True, "message": "Interview already finished."}

    # Only accept text for text/design types
    q_meta = session["questions"][session["q_index"]]
    q_type = q_meta["type"]

    if q_type not in ("text", "design"):
        raise HTTPException(status_code=400, detail=f"Current question expects file upload (type={q_type}).")

    # evaluate (design & text use LLM)
    eval_result = evaluate_answer(msg.answer, q_meta.get("rubric", ""))
    # store
    session["answers"].append(msg.answer)
    session["scores"].append(eval_result.get("score", 0))
    append_transcript_entry(session_id, q_meta["prompt"], msg.answer, eval_result)

    # advance
    advance_to_next(session_id)

    # next question (or done)
    next_q = get_current_question(session_id)
    return {"evaluation": eval_result, "next_question": next_q, "session_done": next_q is None}

@app.post("/session/{session_id}/submit")
async def submit_file_answer(session_id: str, answer: str = Form(None), excel_file: UploadFile = File(None)):
    """
    Handle file-based questions. The frontend should POST exam file to this endpoint.
    `answer` may be an optional text describing the file (like filename or comment).
    """
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="session not found")

    q_meta = session["questions"][session["q_index"]]
    q_type = q_meta["type"]

    if q_type != "file":
        raise HTTPException(status_code=400, detail=f"Current question expects text (type={q_type}).")

    if not excel_file:
        raise HTTPException(status_code=400, detail="No excel_file provided.")

    # save the uploaded file temporarily
    tmp_path = f"temp_{session_id}_{excel_file.filename}"
    with open(tmp_path, "wb") as fh:
        fh.write(await excel_file.read())

    # Use generate_report to run both text eval and excel validation
    # For files we use generate_report(answer_text, rubric, excel_file_path)
    report = generate_report(answer or "", q_meta.get("rubric", ""), tmp_path)

    # store: combine text eval and excel eval into a single evaluation dict
    # We'll use text_eval score if present else excel_eval.score (or sum/heuristic)
    text_eval = report.get("text_eval") or {"score": 0, "feedback": ""}
    excel_eval = report.get("excel_eval") or {}
    # For simplicity compute evaluation score: prefer excel_eval['score'] if present else text_eval
    eval_score = 0
    if isinstance(excel_eval, dict) and "score" in excel_eval:
        eval_score = excel_eval.get("score", 0)
    else:
        eval_score = text_eval.get("score", 0)

    evaluation = {
        "score": eval_score,
        "text_eval": text_eval,
        "excel_eval": excel_eval
    }

    session["answers"].append({"file": excel_file.filename, "note": answer})
    session["scores"].append(eval_score)
    append_transcript_entry(session_id, q_meta["prompt"], f"file:{excel_file.filename}", evaluation)

    # advance
    advance_to_next(session_id)

    # optionally remove temp file
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    next_q = get_current_question(session_id)
    return {"evaluation": evaluation, "next_question": next_q, "session_done": next_q is None}

@app.get("/session/{session_id}/transcript")
def download_transcript(session_id: str):
    path = get_transcript_file(session_id)

    if not path:
        # maybe not yet written — write now if session done
        s = get_session(session_id)
        if s and s.get("stage") == "done":
            path = write_transcript(session_id)
        else:
            raise HTTPException(status_code=404, detail="Transcript not found")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Transcript file missing on disk")

    return FileResponse(
        path,
        media_type="application/json",
        filename=f"{session_id}_transcript.json"
    )
