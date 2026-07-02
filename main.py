from database import create_database
from database import save_analysis
from database import get_all_logs
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import base64


# ---------------- Setup ----------------

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
create_database()

# ---------------- Models ----------------

class ChatRequest(BaseModel):
    prompt: str

class AnalyzeRequest(BaseModel):
    type: str   # sms | url | audio | image | text
    content: str


# ---------------- Core AI Engine ----------------

def fraud_analysis_engine(content: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert AI banking fraud detection system.

Return ONLY valid JSON:

{
  "risk_score": 0,
  "confidence_score": 0,
  "risk_level": "Low",
  "scam_detected": false,
  "indicators": [],
  "summary": ""
}

Rules:
- risk_score: 0-100
- confidence_score: 0-100
- risk_level must be Low, Medium, High
"""
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )

    text = response.choices[0].message.content

    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        return {
            "risk_score": 0,
            "confidence_score": 0,
            "risk_level": "Unknown",
            "scam_detected": False,
            "indicators": [],
            "summary": text
        }


# ---------------- Routes ----------------

@app.get("/")
def home():
    return {"message": "Aman AI API is running"}

# Chat (اختياري)
@app.post("/chat")
def chat(req: ChatRequest):

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": req.prompt}]
    )

    return {"response": res.choices[0].message.content}


# ---------------- Unified Analyze API ----------------

@app.post("/analyze")
def analyze(req: AnalyzeRequest):

    result = fraud_analysis_engine(req.content)
    save_analysis(
    input_type=req.type,
    content=req.content,
    risk_score=result.get("risk_score", 0),
    confidence_score=result.get("confidence_score", 0),
    risk_level=result.get("risk_level", "Unknown"),
    scam_detected=result.get("scam_detected", False),
    summary=result.get("summary", "")
)

    return {
        "status": "success",
        "type": req.type,
        "content": req.content,
        "fraud_analysis": result
    }


# ---------------- Audio ----------------

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    temp = f"temp_{file.filename}"

    try:
        with open(temp, "wb") as f:
            f.write(await file.read())

        with open(temp, "rb") as audio:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio
            )

        text = transcript.text
        analysis = fraud_analysis_engine(text)
        save_analysis(
        input_type="audio",
        content=text,
        risk_score=analysis.get("risk_score", 0),
        confidence_score=analysis.get("confidence_score", 0),
        risk_level=analysis.get("risk_level", "Unknown"),
        scam_detected=analysis.get("scam_detected", False),
        summary=analysis.get("summary", "")
)

        return {
            "status": "success",
            "transcript": text,
            "fraud_analysis": fraud_analysis_engine(text)
        }

    finally:
        if os.path.exists(temp):
            os.remove(temp)


# ---------------- Image (Vision) ----------------

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):

    temp = f"temp_{file.filename}"

    try:
        with open(temp, "wb") as f:
            f.write(await file.read())

        with open(temp, "rb") as img:
            b64 = base64.b64encode(img.read()).decode("utf-8")

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract text and detect fraud in this screenshot"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64}"
                            }
                        }
                    ]
                }
            ]
        )

        extracted = res.choices[0].message.content
        analysis = fraud_analysis_engine(extracted)

        save_analysis(
            input_type="image",
            content=file.filename,
            risk_score=analysis.get("risk_score", 0),
            confidence_score=analysis.get("confidence_score", 0),
            risk_level=analysis.get("risk_level", "Unknown"),
    scam_detected=analysis.get("scam_detected", False),
    summary=analysis.get("summary", "")
)

        return {
            "status": "success",
            "fraud_analysis": fraud_analysis_engine(extracted)
        }

    finally:
        if os.path.exists(temp):
            os.remove(temp)
@app.get("/logs")
def logs():

    data = get_all_logs()

    return {
        "status": "success",
        "count": len(data),
        "logs": [
            {
                "id": r[0],
                "timestamp": r[1],
                "type": r[2],
                "content": r[3],
                "risk_score": r[4],
                "confidence_score": r[5],
                "risk_level": r[6],
                "scam_detected": r[7],
                "summary": r[8],
            }
            for r in data
        ]
    }