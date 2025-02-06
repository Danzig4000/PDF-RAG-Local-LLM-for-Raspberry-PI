# PDF-RAG-Local-LLM-for-Raspberry-PI

This application allows users to upload a PDF document and ask questions about its contents through a web-based chat interface. It utilizes FastAPI as the backend, React.js for the frontend, and Ollama running Llama3.2 as the local AI model to process queries.

🔧 How It Works
1️⃣ User Uploads a PDF
The React frontend allows users to select and upload a PDF.
The file is sent to the FastAPI backend, where it is saved in the uploads/ directory.
2️⃣ Extracting Text from the PDF
FastAPI uses PyPDF2 to extract text from the uploaded PDF.
The extracted text is stored temporarily to be used in processing user queries.
3️⃣ User Asks a Question
The user inputs a question into the chatbox.
The question is sent via Axios (HTTP request) to the FastAPI backend.
4️⃣ Query Processing with Ollama (Llama3.2)
The backend sends the question along with the extracted PDF text to Ollama.
Ollama processes the question based on the PDF content and generates a response.
5️⃣ Displaying the AI’s Answer
The response is sent back to the React frontend.
The frontend displays the AI's answer to the user.

🛠️ Technologies Used
Frontend: React.js, Axios
Backend: FastAPI, PyPDF2
AI Model: Llama3.2 via Ollama
Communication: REST API with JSON
Hosting: Runs locally on Linux with uvicorn

🚀 How to Use
Start the backend (server.py) with FastAPI:
uuvicorn server:app --host 0.0.0.0 --port 8000 --reload

Start the frontend (React app):
npm start

Upload a PDF and ask questions through the web portal.
This setup ensures fast, private, and local AI-powered document search and summarization. 🚀
