
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import joblib
import numpy as np
import os

# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="🌧️ Weather Rain Prediction API",
    description="Predict whether it will rain tomorrow based on today's weather data.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # production এ specific domain দিবে
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Load model & scaler ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model  = joblib.load(os.path.join(BASE_DIR, "weather_model.joblib"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.joblib"))

FEATURES = [
    "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation",
    "Sunshine", "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm",
    "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm",
    "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm",
    "Temp9am", "Temp3pm",
]

# ── Request schema ────────────────────────────────────────────────────────────
class WeatherInput(BaseModel):
    Location:      float = Field(..., example=1.0,    description="Encoded location ID")
    MinTemp:       float = Field(..., example=13.4,   description="Minimum temperature (°C)")
    MaxTemp:       float = Field(..., example=22.9,   description="Maximum temperature (°C)")
    Rainfall:      float = Field(..., example=0.6,    description="Rainfall amount (mm)")
    Evaporation:   float = Field(..., example=5.0,    description="Evaporation (mm)")
    Sunshine:      float = Field(..., example=7.0,    description="Hours of sunshine")
    WindGustDir:   float = Field(..., example=8.0,    description="Encoded wind gust direction")
    WindGustSpeed: float = Field(..., example=44.0,   description="Wind gust speed (km/h)")
    WindDir9am:    float = Field(..., example=7.0,    description="Encoded wind direction at 9am")
    WindDir3pm:    float = Field(..., example=8.0,    description="Encoded wind direction at 3pm")
    WindSpeed9am:  float = Field(..., example=20.0,   description="Wind speed at 9am (km/h)")
    WindSpeed3pm:  float = Field(..., example=24.0,   description="Wind speed at 3pm (km/h)")
    Humidity9am:   float = Field(..., example=71.0,   description="Humidity at 9am (%)")
    Humidity3pm:   float = Field(..., example=22.0,   description="Humidity at 3pm (%)")
    Pressure9am:   float = Field(..., example=1007.7, description="Atmospheric pressure at 9am (hPa)")
    Pressure3pm:   float = Field(..., example=1007.1, description="Atmospheric pressure at 3pm (hPa)")
    Cloud9am:      float = Field(..., example=8.0,    description="Cloud coverage at 9am (oktas 0-8)")
    Cloud3pm:      float = Field(..., example=5.0,    description="Cloud coverage at 3pm (oktas 0-8)")
    Temp9am:       float = Field(..., example=16.9,   description="Temperature at 9am (°C)")
    Temp3pm:       float = Field(..., example=21.8,   description="Temperature at 3pm (°C)")

    class Config:
        json_schema_extra = {
            "example": {
                "Location": 1.0, "MinTemp": 13.4, "MaxTemp": 22.9,
                "Rainfall": 0.6, "Evaporation": 5.0, "Sunshine": 7.0,
                "WindGustDir": 8.0, "WindGustSpeed": 44.0, "WindDir9am": 7.0,
                "WindDir3pm": 8.0, "WindSpeed9am": 20.0, "WindSpeed3pm": 24.0,
                "Humidity9am": 71.0, "Humidity3pm": 22.0,
                "Pressure9am": 1007.7, "Pressure3pm": 1007.1,
                "Cloud9am": 8.0, "Cloud3pm": 5.0,
                "Temp9am": 16.9, "Temp3pm": 21.8,
            }
        }

# ── Response schema ───────────────────────────────────────────────────────────
class PredictionResponse(BaseModel):
    prediction:        int   = Field(..., description="0 = No Rain, 1 = Rain")
    rain_tomorrow:     str   = Field(..., description="Human-readable result")
    probability_rain:  float = Field(..., description="Probability of rain (%)")
    probability_no_rain: float = Field(..., description="Probability of no rain (%)")

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Weather Rain Prediction API is running 🌤️"}


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "model": type(model).__name__,
        "scaler": type(scaler).__name__,
        "features": FEATURES,
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(data: WeatherInput):
    try:
        # Build dataframe in exact feature order
        df = pd.DataFrame([data.model_dump()], columns=FEATURES)

        # Scale → predict
        X_scaled = scaler.transform(df)
        pred      = int(model.predict(X_scaled)[0])
        proba     = model.predict_proba(X_scaled)[0]  # [P(0), P(1)]

        return PredictionResponse(
            prediction          = pred,
            rain_tomorrow       = "Yes 🌧️" if pred == 1 else "No ☀️",
            probability_rain    = round(float(proba[1]) * 100, 2),
            probability_no_rain = round(float(proba[0]) * 100, 2),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
