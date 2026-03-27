# 🌧️ Weather Rain Prediction API

A FastAPI app that predicts **rain tomorrow** using a Logistic Regression model.

---

## 📁 Project Structure

```
weather_api/
├── main.py                  # FastAPI application
├── weather_model.joblib     # Trained Logistic Regression model
├── scaler.joblib            # StandardScaler for feature normalization
├── requirements.txt         # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Place model files
Make sure `weather_model.joblib` and `scaler.joblib` are in the **same folder** as `main.py`.

### 3. Start the server
```bash
uvicorn app:app --reload
```

Server runs at: **http://127.0.0.1:8000**

---

## 📡 API Endpoints

| Method | Endpoint    | Description              |
|--------|-------------|--------------------------|
| GET    | `/`         | Health check             |
| GET    | `/health`   | Model info & feature list|
| POST   | `/predict`  | Get rain prediction      |
| GET    | `/docs`     | Swagger UI (auto-generated) |
| GET    | `/redoc`    | ReDoc UI                 |

---

## 🔮 Prediction Request

**POST** `/predict`

```json
{
  "Location": 1.0,
  "MinTemp": 13.4,
  "MaxTemp": 22.9,
  "Rainfall": 0.6,
  "Evaporation": 5.0,
  "Sunshine": 7.0,
  "WindGustDir": 8.0,
  "WindGustSpeed": 44.0,
  "WindDir9am": 7.0,
  "WindDir3pm": 8.0,
  "WindSpeed9am": 20.0,
  "WindSpeed3pm": 24.0,
  "Humidity9am": 71.0,
  "Humidity3pm": 22.0,
  "Pressure9am": 1007.7,
  "Pressure3pm": 1007.1,
  "Cloud9am": 8.0,
  "Cloud3pm": 5.0,
  "Temp9am": 16.9,
  "Temp3pm": 21.8
}
```

**Response:**
```json
{
  "prediction": 0,
  "rain_tomorrow": "No ☀️",
  "probability_rain": 18.34,
  "probability_no_rain": 81.66
}
```

---

## 🧪 Test with curl

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Location": 1.0, "MinTemp": 13.4, "MaxTemp": 22.9,
    "Rainfall": 0.6, "Evaporation": 5.0, "Sunshine": 7.0,
    "WindGustDir": 8.0, "WindGustSpeed": 44.0,
    "WindDir9am": 7.0, "WindDir3pm": 8.0,
    "WindSpeed9am": 20.0, "WindSpeed3pm": 24.0,
    "Humidity9am": 71.0, "Humidity3pm": 22.0,
    "Pressure9am": 1007.7, "Pressure3pm": 1007.1,
    "Cloud9am": 8.0, "Cloud3pm": 5.0,
    "Temp9am": 16.9, "Temp3pm": 21.8
  }'
```

---

## 📝 Feature Notes

All categorical features (Location, WindGustDir, WindDir9am, WindDir3pm) must be **label-encoded** (numeric) before sending — matching the encoding used during training.
