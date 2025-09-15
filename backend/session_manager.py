from uuid import uuid4
import os
import json
from typing import Optional

TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "transcripts")
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

# In-memory sessions (ephemeral). Replace with Redis/DB for persistence.
sessions = {}

DEFAULT_QUESTIONS = [
    {"type": "text", "prompt": "Explain VLOOKUP", "rubric": "Clarity, accuracy, example"},
    {"type": "text", "prompt": "What is a Pivot Table and when would you use it?", "rubric": "Definition, use-case"},
    {"type": "file", "prompt": "Upload an Excel file with a SUM formula in B10", "rubric": "SUM formula presence in B10"},
    {"type": "file", "prompt": "Upload an Excel file showing a basic Pivot Table of sales", "rubric": "Pivot table presence and structure"},
    {"type": "design", "prompt": "Design an Excel template for monthly budgeting (describe columns/structure)", "rubric": "Completeness and design choices"}
]

def create_session():
    sid = str(uuid4())
    sessions[sid] = {
        "stage": "intro",
        "q_index": 0,
        "questions": DEFAULT_QUESTIONS.copy(),
        "answers": [],
        "scores": [],
        "transcript": []
    }
    return sid

def get_session(session_id: str) -> Optional[dict]:
    return sessions.get(session_id)

def get_current_question(session_id: str) -> Optional[dict]:
    s = get_session(session_id)
    if not s:
        return None
    q_index = s["q_index"]
    if q_index < len(s["questions"]):
        q = s["questions"][q_index].copy()
        # send only what's needed to client:
        return {"type": q["type"], "prompt": q["prompt"], "index": q_index}
    else:
        return None

def advance_to_next(session_id: str):
    s = get_session(session_id)
    if not s:
        return
    s["q_index"] += 1
    if s["q_index"] >= len(s["questions"]):
        s["stage"] = "done"
        # when done write transcript to file
        write_transcript(session_id)
    else:
        s["stage"] = "question"

def append_transcript_entry(session_id: str, question: str, answer: str, evaluation: dict):
    s = get_session(session_id)
    if not s:
        return
    entry = {
        "question": question,
        "answer": answer,
        "evaluation": evaluation
    }
    s["transcript"].append(entry)

def write_transcript(session_id: str):
    s = get_session(session_id)
    if not s:
        return
    out = {
        "session_id": session_id,
        "transcript": s["transcript"],
        "final_score": sum([e.get("score", 0) for e in ( [t["evaluation"] for t in s["transcript"]] )]) if s["transcript"] else 0
    }
    path = os.path.join(TRANSCRIPTS_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    return path

def get_transcript_file(session_id: str) -> Optional[str]:
    path = os.path.join(TRANSCRIPTS_DIR, f"{session_id}.json")
    return path if os.path.exists(path) else None