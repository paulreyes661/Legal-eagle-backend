from fastapi import FastAPI, UploadFile, File
import pdfplumber
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"status": "Legal Eagle backend running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    
    contents = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(contents)

    text = ""

    with pdfplumber.open("temp.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Analyze legal document and explain risks."},
            {"role": "user", "content": text[:4000]}
        ]
    )

    return {"analysis": response.choices[0].message.content}
