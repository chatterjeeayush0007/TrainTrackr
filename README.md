# 🚂 TrainTrackr

**TrainTrackr** is a smart transit companion designed to make commuting smoother and more predictable. Powered by a lightning-fast Python FastAPI backend, it provides commuters with local train schedules, heuristic delay predictions, platform details, and station crowd estimations to help plan faster, safer routes.

---

## ✨ Key Features

* **🚆 Train & Route Management:** View all available trains, fetch specific train details by number, and map out complete stop-by-stop routes.
* **🚉 Station Intelligence:** Browse the full list of stations or use the search functionality to find specific transit hubs instantly.
* **⏱️ Delay Predictions:** Get heuristic-based estimates for train delays and dynamically updated arrival times.
* **👥 Crowd Estimation:** Check expected crowd densities (Low / Medium / High) at specific stations before you arrive.
* **⚡ Modern API Architecture:** Built on FastAPI for high performance, featuring modular routing, schema validation, and built-in CORS support.

---

## 📂 Project Structure

```text
TRAINTRACKR-1/
├── .venv/
├── .vscode/
├── app/
│   ├── data/
│   │   ├── mock_users.json
│   │   ├── pincode_population.json
│   │   └── trains.json
│   ├── db/
│   │   ├── __init__.py
│   │   └── mongodb.py
│   ├── models/
│   │   ├── travel.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predictions.py
│   │   ├── railradar.py
│   │   ├── recommendations.py
│   │   ├── stations.py
│   │   ├── trains.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── crowd_predict.py
│   │   ├── delay_predict.py
│   │   ├── gps_mapper.py
│   │   ├── locationiq_mapper.py
│   │   ├── populate_stations.py
│   │   ├── population_model.py
│   │   ├── simulate_trains.py
│   │   ├── time_calc.py
│   │   └── train_assistant_logic.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── train_assistant.py
├── frontend/
│   └── gui/
│       ├── dist/
│       │   ├── assets/
│       │   ├── favicon.svg
│       │   ├── icon.png
│       │   ├── icons.svg
│       │   ├── index.html
│       │   ├── manifest.json
│       │   ├── sw.js
│       │   └── train-bg.jpeg
│       ├── public/
│       │   ├── favicon.svg
│       │   ├── icon.png
│       │   ├── icons.svg
│       │   ├── manifest.json
│       │   ├── sw.js
│       │   └── train-bg.jpeg
│       ├── src/
│       │   ├── assets/
│       │   ├── pages/
│       │   ├── styles/
│       │   ├── App.css
│       │   ├── App.jsx
│       │   ├── firebase.js
│       │   ├── index.css
│       │   └── main.jsx
│       ├── .gitignore
│       ├── eslint.config.js
│       ├── index.html
│       ├── package-lock.json
│       ├── package.json
│       ├── README.md
│       └── vite.config.js
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt

⚡ Installation & Setup

1. Clone the repository
Bash

git clone https://github.com/chatterjeeayush0007/TrainTrackr
cd TRAINTRACKR-1

2. Create and activate a virtual environment
Bash

python -m venv .venv

# On Linux/Mac:
source .venv/bin/activate 

# On Windows:
.\.venv\Scripts\activate

3. Install backend dependencies
Bash

pip install -r requirements.txt

🏃 Running the Server

Start the FastAPI backend server using Uvicorn:
Bash

uvicorn app.main:app --reload

    Interactive API Docs (Swagger UI): http://127.0.0.1:8000/docs

    Health Check: GET /

🛠 API Endpoints Overview
Endpoint	Method	Description
/trains	GET	Retrieve a list of all available trains.
/trains/{train_no}	GET	Fetch specific details for a train by its number.
/trains/{train_no}/route	GET	Get the full stop-by-stop route for a specific train.
/stations	GET	Retrieve a list of all stations.
/stations/search?q=	GET	Search for stations by name or code.
/predictions/delay/{train_no}	GET	Get heuristic predictions for train delays.
/crowd/{station}	GET	Estimate the current/expected crowd level at a station.
🧩 Current Status & Roadmap

    Data Source: Currently utilizes static JSON data (trains.json, mock_users.json) for safe testing and development.

    Logic-Based Estimates: Delay predictions and crowd estimations are currently driven by internal heuristic logic and population modeling.

    In Progress (Roadmap): * Full integration of the React/Vite UI (frontend/gui).

        Real-time GPS tracking and live mapping via LocationIQ.