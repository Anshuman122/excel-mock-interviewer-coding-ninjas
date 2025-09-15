import React from "react";

const ChatHistory = ({ messages }) => {
  return (
    <div style={{ marginBottom: "20px" }}>
      {messages.map((msg, index) => (
        <div key={index} style={{ marginBottom: "8px" }}>
          {msg.role === "system" ? (
            <strong>🧑 Interviewer: {msg.content}</strong>
          ) : (
            <span>🙋 You: {msg.content}</span>
          )}
        </div>
      ))}
    </div>
  );
};

export default ChatHistory;
