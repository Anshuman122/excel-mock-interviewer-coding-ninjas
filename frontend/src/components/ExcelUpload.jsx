// frontend/src/components/ExcelUpload.jsx
import React, { useState } from "react";

export default function ExcelUpload({ sessionId, onUpload }) {
  const [file, setFile] = useState(null);
  const [note, setNote] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) {
      alert("Choose a file first.");
      return;
    }
    onUpload(file, note);
    setFile(null);
    setNote("");
  };

  return (
    <div>
      <h3>Upload Excel File</h3>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".xlsx" onChange={(e) => setFile(e.target.files[0])} />
        <input type="text" placeholder="Optional note" value={note} onChange={(e) => setNote(e.target.value)} />
        <button type="submit">Submit File</button>
      </form>
    </div>
  );
}
