import React, { useState } from "react";
import { startSession, sendAnswer, submitExcel, fetchTranscript } from "./api/backend.js";
import ChatHistory from "./components/ChatHistory";
import QuestionCard from "./components/QuestionCard";
import ExcelUpload from "./components/ExcelUpload";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [interviewDone, setInterviewDone] = useState(false);
  const [report, setReport] = useState(null);

  const handleStart = async () => {
    try {
      const data = await startSession();
      setSessionId(data.session_id);
      setCurrentQuestion(data.question);
      setMessages([{ role: "system", content: data.question.prompt }]);
    } catch (err) {
      toast.error("Failed to start session");
      console.error(err);
    }
  };

  const handleAnswerSubmit = async (answer) => {
    // append user answer to chat
    setMessages((prev) => [...prev, { role: "user", content: answer }]);

    try {
      const data = await sendAnswer(sessionId, answer);
      // show evaluation
      if (data.evaluation) {
        setMessages((prev) => [
          ...prev,
          { role: "system", content: `Evaluation: ${JSON.stringify(data.evaluation)}` },
        ]);
      }
      if (data.next_question) {
        setCurrentQuestion(data.next_question);
        setMessages((prev) => [...prev, { role: "system", content: data.next_question.prompt }]);
      } else {
        setCurrentQuestion(null);
        setInterviewDone(true);
        toast.success("Interview finished! Upload your files (if any) or view final report.");
      }
    } catch (err) {
      toast.error("Failed to send answer");
      console.error(err);
    }
  };

  const handleFileSubmit = async (file, answerText = "") => {
    try {
      const data = await submitExcel(sessionId, file, answerText);
      // show evaluation
      if (data.evaluation) {
        setMessages((prev) => [
          ...prev,
          { role: "system", content: `Evaluation: ${JSON.stringify(data.evaluation)}` },
        ]);
      }
      if (data.next_question) {
        setCurrentQuestion(data.next_question);
        setMessages((prev) => [...prev, { role: "system", content: data.next_question.prompt }]);
      } else {
        setCurrentQuestion(null);
        setInterviewDone(true);
        toast.success("Interview finished! You can fetch the transcript.");
      }
    } catch (err) {
      toast.error("Failed to submit file");
      console.error(err);
    }
  };

  const handleFetchTranscript = async () => {
    try {
      const data = await fetchTranscript(sessionId);
      setReport(data);
    } catch (err) {
      toast.error("Failed to fetch transcript");
    }
  };

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "20px" }}>
      <h1>📝 FSM Excel Interview</h1>

      {!sessionId && <button onClick={handleStart}>Start Interview</button>}

      <ChatHistory messages={messages} />

      {currentQuestion && currentQuestion.type === "text" && (
        <QuestionCard question={currentQuestion.prompt} onSubmit={handleAnswerSubmit} />
      )}

      {currentQuestion && currentQuestion.type === "design" && (
        <QuestionCard
          question={`${currentQuestion.prompt} (Design question)`}
          onSubmit={handleAnswerSubmit}
        />
      )}

      {currentQuestion && currentQuestion.type === "file" && (
        <ExcelUpload sessionId={sessionId} onUpload={handleFileSubmit} />
      )}

      {interviewDone && (
        <div style={{ marginTop: 20 }}>
          <button onClick={handleFetchTranscript}>Fetch Transcript / Final Report</button>
        </div>
      )}

      {report && (
        <div style={{ marginTop: 20 }}>
          <h3>Transcript / Report</h3>
          <pre style={{padding: 12 }}>
            {JSON.stringify(report, null, 2)}
          </pre>
          {/* ✅ Download Report Button */}
          <button
            onClick={() => {
              const blob = new Blob([JSON.stringify(report, null, 2)], {
                type: "application/json",
              });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = "interview_report.json"; // filename
              a.click();
              URL.revokeObjectURL(url);
            }}
            style={{
              marginTop: "10px",
              padding: "8px 16px",
              borderRadius: "6px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            ⬇️ Download Report
          </button>
        </div>
      )}
      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  );
}

export default App;
