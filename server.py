from fastapi import FastAPI, UploadFile, File
import pdfplumber
import ollama
import chromadb
import os
import PyPDF2
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This is insecure and needs to be changed before publishing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Make sure correct permissions are set for /uploads

db = chromadb.PersistentClient(path="./vector_db")
collection = db.get_or_create_collection(name="pdf_data", embedding_function=DefaultEmbeddingFunction())

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ? Create the directory if it doesn't exist

# Store uploaded PDFs
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Extract text from the last uploaded PDF
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Use Ollama to answer questions about the PDF
@app.post("/query/")
async def query_pdf(question: dict):
    try:
        pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".pdf")]
        if not pdf_files:
            return {"answer": "No PDF found. Please upload a PDF first."}

        latest_pdf = os.path.join(UPLOAD_FOLDER, pdf_files[-1])  # Get the last uploaded PDF
        pdf_text = extract_text_from_pdf(latest_pdf)

        if not pdf_text:
            return {"answer": "Failed to extract text from the PDF."}

        # ?? Query Ollama's local Llama3 model with extracted PDF text
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers questions based on provided PDF content."},
                {"role": "user", "content": f"PDF Content:\n{pdf_text[:4000]}\n\nQuestion: {question['question']}"},
            ]
        )

        return {"answer": response["message"]["content"]}
    except Exception as e:
        return {"answer": f"Error processing query: {str(e)}"}
