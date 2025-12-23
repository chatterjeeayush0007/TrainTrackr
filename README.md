# 📘 TrainTrackr

TrainTrackr is a **smart transit companion** that provides **local train schedules, delay predictions, platform info, and crowd estimations**. Powered by a Python FastAPI backend, it helps commuters **plan faster routes and travel with confidence**.

---

## 🚀 Features

* **Train Listing & Details**
  List all trains, fetch details by train number, get full route (stops).

* **Station Listing & Search**
  Return all stations or search by query.

* **Delay Prediction**
  Heuristic-based train delay predictions and expected arrival times.

* **Crowd Estimation**
  Estimate crowd levels (Low / Medium / High) at stations.

* **Clean API Structure**
  FastAPI backend with modular routes and CORS-enabled.

---

## 📂 Project Structure

```
TrainTrackr/
├── app/
│   ├── main.py
│   ├── data/trains.json
│   ├── routes/
│   │   ├── trains.py
│   │   ├── stations.py
│   │   ├── predictions.py
│   │   └── crowd.py
│   ├── utils/
│   │   ├── delay_predict.py
│   │   └── time_calc.py
│   ├── models.py
│   └── schemas.py
├── README.md
└── requirements.txt
```

---

## ⚡ Installation

1. **Clone the repo**

```bash
git clone <repo-url>
cd TrainTrackr
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Server

```bash
uvicorn app.main:app --reload
```

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Health check: `GET /`

---

## 🛠 API Endpoints Overview

| Endpoint                        | Method | Description             |
| ------------------------------- | ------ | ----------------------- |
| `/trains`                       | GET    | List all trains         |
| `/trains/{train_no}`            | GET    | Train details by number |
| `/trains/{train_no}/route`      | GET    | Full train route        |
| `/stations`                     | GET    | List all stations       |
| `/stations/search?q=`           | GET    | Search stations         |
| `/predictions/delay/{train_no}` | GET    | Predict train delay     |
| `/crowd/{station}`              | GET    | Estimate station crowd  |

---

## 🧩 Notes

* Currently **static data** from `trains.json`
* Delay predictions and crowd estimations are **heuristic-based**
* Frontend/UI and real-time GPS integration are **future enhancements**
