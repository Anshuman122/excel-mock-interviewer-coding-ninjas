// frontend/src/api/backend.js
import axios from "axios";
const API_URL = "https://excel-mock-interviewer-coding-ninjas.onrender.com";

export const startSession = async () => {
  const resp = await axios.post(`${API_URL}/session`);
  // resp.data: { session_id, question: { type, prompt, index } }
  return resp.data;
};

export const sendAnswer = async (sessionId, answer) => {
  const resp = await axios.post(`${API_URL}/session/${sessionId}/message`, { answer });
  // resp.data: { evaluation, next_question, session_done }
  return resp.data;
};

export const submitExcel = async (sessionId, file, answerText = "") => {
  const formData = new FormData();
  formData.append("excel_file", file);
  formData.append("answer", answerText);

  const resp = await axios.post(`${API_URL}/session/${sessionId}/submit`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return resp.data;
};

export const fetchTranscript = async (sessionId) => {
  const resp = await axios.get(`${API_URL}/session/${sessionId}/transcript`);
  return resp.data;
}
