
import json
import os
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING (llm_rubric): GOOGLE_API_KEY not set. LLM features disabled.")

model = None
if API_KEY:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print("WARNING: Could not initialize Gemini model:", e)

def evaluate_answer(answer: str, rubric: str):
    if model is None:
        return {"score": 0, "feedback": "LLM not configured; cannot evaluate answer."}

    prompt = f"""
You are an Excel interviewer AI.
Rubric: {rubric}
Candidate Answer: {answer}

Task: Give a score 0-10 and feedback.
Respond ONLY in strict JSON format: {{ "score": 0, "feedback": "..." }}
Do not include markdown code fences.
"""
    response = model.generate_content(prompt)

    try:
        text = response.text.strip()
        # Remove ```json ... ``` or ``` ... ```
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("json", "", 1).strip()
        eval_json = json.loads(text)
    except Exception:
        # fallback if AI doesn't respond in JSON
        eval_json = {"score": 0, "feedback": response.text}

    return eval_json
