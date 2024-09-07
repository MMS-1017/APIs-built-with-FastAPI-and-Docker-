from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import PyPDF2
from database import init_db, store_content, get_content

app = FastAPI()

# Initialize the database
init_db()

class URLRequest(BaseModel):
    url: str

class PDFRequest(BaseModel):
    chat_id: str

class ChatRequest(BaseModel):
    chat_id: str
    question: str

def clean_text(text: str) -> str:
    return " ".join(text.split())

@app.post("/process_url")
async def process_url(request: URLRequest):
    try:
        response = requests.get(request.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = clean_text(soup.get_text())
        chat_id = store_content("url", text)
        return JSONResponse(content={"chat_id": chat_id, "message": "URL content processed and stored successfully."})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += clean_text(page.extract_text()) + " "
        chat_id = store_content("pdf", text)
        return JSONResponse(content={"chat_id": chat_id, "message": "PDF content processed and stored successfully."})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        stored_content = get_content(request.chat_id)
        if not stored_content:
            raise HTTPException(status_code=404, detail="Chat ID not found.")
        
        content_type, content = stored_content
        response_text = f"The content type is {content_type}. Content length is {len(content)} characters."
        return JSONResponse(content={"response": response_text})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))