<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>

# 🌧️ RainCast — Weather Prediction System

### AI-Powered Weather Forecasting 

*Enter today's weather data and predict whether it will rain tomorrow — powered by Logistic Regression trained on the Australian Weather Dataset.*

</div>

---

## 🖼️ Preview

<div align="center">

| 🌧️ Rain Expected Prediction | ☀️ Clear Skies Prediction |
|:-:|:-:|
| ![Clear Skies](https://i.postimg.cc/XqxtYv4Z/E-NSDA200220prediction-system-frontend-index-html22.png) | ![Rain Expected](https://i.postimg.cc/NFYw0VTG/E-NSDA200220prediction-system-frontend-index-html.png) |

</div>

---

## ✨ Features

- 🔮 **Rain Tomorrow Prediction** — Binary classification using Logistic Regression
- 📊 **Probability Breakdown** — Shows % chance of rain vs. clear skies
- 🌐 **REST API** — Clean FastAPI backend with auto-generated Swagger docs
- 🎨 **Atmospheric Dark UI** — Sleek weather-themed frontend with responsive layout
- ⚡ **Live Deployment** — Hosted on Render with zero cold-start workarounds
- 🧪 **20 Weather Features** — Temperature, humidity, wind, pressure, cloud cover & more

---

## 📁 Project Structure

```
weather_prediction_system/
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css            # Atmospheric dark theme
│   └── script.js            # API calls & result rendering
│
├── app.py                   # FastAPI application & prediction logic
├── weather_model.joblib     # Trained Logistic Regression model
├── scaler.joblib            # StandardScaler for feature normalization
├── requirements.txt         # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/pranto025/weather-rain-prediction.git
cd weather-rain-prediction
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Ensure model files are present
Make sure `weather_model.joblib` and `scaler.joblib` are in the **same folder** as `app.py`.

### 4. Start the server
```bash
uvicorn app:app --reload
```

Server runs at: **http://127.0.0.1:8000**

---

## 📡 API Reference

| Method | Endpoint  | Description                        |
|--------|-----------|------------------------------------|
| `GET`  | `/`       | Health check                       |
| `GET`  | `/health` | Model info & feature list          |
| `POST` | `/predict`| Get rain prediction with probability |
| `GET`  | `/docs`   | Interactive Swagger UI             |

---

## 🔮 Prediction Request & Response

**`POST /predict`**

<details>
<summary>📥 Request Body (click to expand)</summary>

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

</details>

<details>
<summary>📤 Response (click to expand)</summary>

```json
{
  "prediction": 0,
  "rain_tomorrow": "No ☀️",
  "probability_rain": 18.34,
  "probability_no_rain": 81.66
}
```

</details>

---

## 🧪 Test with cURL

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

## 🧠 Model Details

| Property        | Details                              |
|-----------------|--------------------------------------|
| Algorithm       | Logistic Regression                  |
| Dataset         | Australian Weather Dataset (BOM)     |
| Features        | 20 weather attributes                |
| Preprocessing   | StandardScaler normalization         |
| Output          | Binary (Rain / No Rain) + Probability|
| Deployment      | Render (Free tier)                   |

---

## 📝 Feature Encoding Notes

All categorical features must be **label-encoded** (numeric) before sending — matching the encoding used during training:

| Feature       | Type        | Notes                              |
|---------------|-------------|------------------------------------|
| `Location`    | Categorical | Label-encoded (e.g., Albury = 1)   |
| `WindGustDir` | Categorical | 16-point compass → numeric         |
| `WindDir9am`  | Categorical | 16-point compass → numeric         |
| `WindDir3pm`  | Categorical | 16-point compass → numeric         |
| All others    | Numeric     | Float values as-is                 |

---

## 🐛 Known Issues & Fixes

> **Pandas Runtime Error on Render** — Replaced DataFrame construction with pure NumPy arrays to fix a `pandas` compatibility crash on the Render deployment environment.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ by **MD.Pranto025** · Logistic Regression Model · Australian Weather Dataset

</div>
