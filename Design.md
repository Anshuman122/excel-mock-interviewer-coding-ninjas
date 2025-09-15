📐 Design Document – Excel Mock Interviewer
🎯 Strategy

Structured Interview Flow

Start session → greet candidate → explain flow.

Ask 4–5 Excel questions (text + file upload).

Track progress via session state.

Evaluation Engine

Text/design → Gemini API with rubric.

Excel/file → validate formulas, sheets, correctness.

Score aggregation → average + feedback.

Agentic Behavior

Maintains session state (question index, answers, scores).

Moves sequentially through Qs.

Ends gracefully with summary + transcript.

Feedback Report

Transcript saved per session.

Includes Q, candidate answer, AI evaluation.

Export as JSON and PDF.

❄️ Cold Start Solution

No pre-existing dataset of transcripts.

Bootstrapped by:

Using synthetic Q&A pairs (curated Excel questions + ideal answers).

Leveraging expert seeding: manually written rubrics for evaluation.

Over time → transcripts collected → fine-tuning possible.

🔮 Future Improvements

Add speech mode (voice-to-text + conversational).

Use vector DB for storing candidate history + advanced analytics.

Integrate adaptive difficulty → harder/easier based on performance.

Expand beyond Excel → Google Sheets, SQL, Python.

Multiple Student Interview handling

Richer PDF reports with charts + candidate benchmarking.

3. excel-mock-interviewer-main\backend\transcripts

sample_transcript_1.json → interview 1

sample_transcript_2.json → interview 2



4. Final Testing Checklist

✅ One candidate can complete end-to-end interview.

✅ Evaluations returned correctly.

✅ Transcript downloadable.

✅ Frontend ↔ backend integration works.

✅ Deployed links accessible.