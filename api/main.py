import os
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import APIError, AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

from ai.report_generator import generate_report
from ai.reasoning import assess_risk, get_followup_questions
from knowledge.diseases import DISEASE_INFO

# Resolve base directory relative to api/main.py
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATASET_DIR = BASE_DIR / "dataset"
load_dotenv(BASE_DIR / ".env")


def _resolve_model_path(name: str) -> Path:
    candidate = MODELS_DIR / name
    if candidate.exists():
        return candidate

    fallback = BASE_DIR / name
    if fallback.exists():
        return fallback

    raise FileNotFoundError(f"Missing required model file: {name}")


app = FastAPI(title="HealthGuide AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and encoders
model_path = _resolve_model_path("disease_model.pkl")
encoder_path = _resolve_model_path("label_encoder.pkl")
dataset_path = DATASET_DIR / "disease_dataset.csv"

if not dataset_path.exists():
    raise FileNotFoundError("Missing dataset file: disease_dataset.csv")

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

# Load feature names
dataset = pd.read_csv(dataset_path)
FEATURES = list(dataset.drop("disease", axis=1).columns)


class PredictionRequest(BaseModel):
    symptoms: list[str]


class AssistantMessage(BaseModel):
    role: str
    content: str


class AssistantRequest(BaseModel):
    message: str
    history: list[AssistantMessage] = []


def display_name(value: str) -> str:
    return value.replace("_", " ").title()


@app.get("/")
def home():
    return {"message": "HealthGuide AI API Running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/assistant")
async def assistant_chat(data: AssistantRequest):
    """Provide general health information through OpenAI without exposing its key to clients."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI assistant is not configured. Set OPENAI_API_KEY on the server.",
        )

    history = [
        {"role": item.role, "content": item.content}
        for item in data.history[-8:]
        if item.role in {"user", "assistant"}
    ]
    instructions = (
        "You are HealthGuide AI, a supportive health-information assistant. "
        "Give concise, plain-language general information, not a diagnosis. "
        "Encourage professional medical care for concerning symptoms. "
        "For severe chest pain, trouble breathing, signs of stroke, severe bleeding, "
        "loss of consciousness, or immediate danger, tell the user to seek emergency "
        "help now. Do not prescribe medicines or give dosing instructions."
    )

    try:
        async with AsyncOpenAI(api_key=api_key) as client:
            response = await client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": instructions},
                    *history,
                    {"role": "user", "content": data.message},
                ],
            )
    except APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI assistant is temporarily unavailable. Please try again.",
        ) from None

    answer = response.choices[0].message.content.strip() if response.choices else ""
    if not answer:
        raise HTTPException(status_code=502, detail="The AI assistant returned no response.")
    return {"message": answer}


@app.get("/symptoms")
def symptoms():
    return [
        {
            "id": symptom,
            "name": display_name(symptom)
        }
        for symptom in FEATURES
    ]


@app.get("/diseases")
def diseases():
    return [
        {
            "name": disease,
            "severity": info.get("severity", "Unknown"),
            "description": info.get("description", ""),
            "recommendation": info.get("recommendation", ""),
            "medications": info.get("medications", []),
        }
        for disease, info in DISEASE_INFO.items()
    ]


@app.get("/diseases/{disease_name}")
def disease_details(disease_name: str):
    normalized = disease_name.lower()

    for disease, info in DISEASE_INFO.items():
        if disease.lower() == normalized:
            return {
                "name": disease,
                "severity": info.get("severity", "Unknown"),
                "description": info.get("description", ""),
                "recommendation": info.get("recommendation", ""),
                "medications": info.get("medications", []),
            }

    raise HTTPException(status_code=404, detail="Disease not found")


@app.post("/predict")
def predict(data: PredictionRequest):
    sample = {feature: 0 for feature in FEATURES}

    for symptom in data.symptoms:
        if symptom in sample:
            sample[symptom] = 1

    df = pd.DataFrame([sample])

    probabilities = model.predict_proba(df)[0]
    classes = encoder.inverse_transform(model.classes_)

    disease_scores = []
    for disease, probability in zip(classes, probabilities):
        info = DISEASE_INFO.get(disease, {"severity": "Unknown"})
        disease_scores.append({
            "disease": disease,
            "confidence": round(probability * 100, 2),
            "severity": info.get("severity", "Unknown")
        })

    disease_scores.sort(key=lambda x: x["confidence"], reverse=True)
    best = disease_scores[0]

    default_info = {
        "severity": "Unknown",
        "description": "No description available.",
        "recommendation": "Consult a healthcare professional.",
        "medications": []
    }
    info = DISEASE_INFO.get(best["disease"], default_info)

    report = generate_report(
        data.symptoms,
        best["disease"],
        best["confidence"],
        info
    )

    risk = assess_risk(data.symptoms)
    questions = get_followup_questions(best["disease"])

    return {
        "prediction": best["disease"],
        "confidence": best["confidence"],
        "severity": info.get("severity", "Unknown"),
        "risk": risk,
        "description": info.get("description", ""),
        "recommendation": info.get("recommendation", ""),
        "medications": info.get("medications", []),
        "follow_up_questions": questions,
        "top_predictions": disease_scores[:3],
        "report": report,
    }

    "top_predictions": disease_scores[:3],

    "report": report

}}
