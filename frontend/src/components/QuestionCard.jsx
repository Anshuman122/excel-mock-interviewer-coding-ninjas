import React, { useState } from "react";

const QuestionCard = ({ question, onSubmit }) => {
  const [answer, setAnswer] = useState("");

  const handleSubmit = () => {
    if (answer.trim() === "") return;
    onSubmit(answer);
    setAnswer(""); // clear input
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <h3>🧑 Interviewer: {question}</h3>
      <textarea
        rows={4}
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        placeholder="Type your answer here..."
        style={{ width: "100%", padding: "8px" }}
      />
      <button onClick={handleSubmit} style={{ marginTop: "10px" }}>
        Submit Answer
      </button>
    </div>
  );
};

export default QuestionCard;
