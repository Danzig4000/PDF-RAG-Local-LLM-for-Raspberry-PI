import { useState } from "react";
import axios from "axios";

function ChatApp() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const uploadPDF = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://192.168.2.16:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("Upload success:", res.data);
      alert("PDF uploaded!");
    } catch (error) {
      console.error("Upload error:", error);
      alert(`Failed to upload PDF: ${error.message}`);
    }
  };

 const sendQuery = async () => {
  try {
    const response = await axios.post("http://192.168.2.16:8000/query/", { question: query }, {
      headers: { "Content-Type": "application/json" },
    });

    // Ensure we extract only the text response
    setResponse(response.data.answer || "No response received.");
  } catch (error) {
    console.error("Query error:", error);
    setResponse("Query failed.");
  }
 };


  // ? Move JSX return statement outside of sendQuery
  return (
    <div>
      <h2>PDF AI Parser</h2>
      
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadPDF}>Upload PDF</button>

      <br />
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={sendQuery}>Ask</button>

      <p>Response: {response}</p>
    </div>
  );
}

export default ChatApp;  // ? Ensure export is at the bottom

