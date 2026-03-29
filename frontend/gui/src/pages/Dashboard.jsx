import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { auth } from "../firebase";
import "../styles/dashboard.css";

const BASE_URL = "http://127.0.0.1:8000";

export default function Dashboard() {
  const navigate = useNavigate();
  const firebaseUser = auth.currentUser;
  const storedDetails = JSON.parse(localStorage.getItem("userDetails")) || {};

  const [from, setFrom] = useState(storedDetails.from || "");
  const [to, setTo] = useState(storedDetails.to || "");
  const [time, setTime] = useState(storedDetails.time || "");

  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [trainSlots, setTrainSlots] = useState({});

  const userName = firebaseUser?.displayName || storedDetails.name || "";
  const userType = storedDetails.type || "daily";

  const getCrowdColor = (level) => {
    if (level === "Low") return "green";
    if (level === "Medium") return "orange";
    if (level === "High") return "red";
    return "gray";
  };

  const handleSearch = async () => {
    if (!from || !to || !time) return;

    setLoading(true);
    setShowResults(false);

    try {
      // 1️⃣ Fetch all trains
      const trainsResp = await fetch(`${BASE_URL}/trains/`);
      const trainsData = await trainsResp.json();
      const allTrains = trainsData.trains || [];

      const slots = {};

      // 2️⃣ Process each train one by one
      for (const train of allTrains) {
        // Fetch route for this train
        const routeResp = await fetch(`${BASE_URL}/trains/${train.train_no}/route`);
        const routeData = await routeResp.json();
        const stops = routeData.stops || [];

        const startIndex = stops.findIndex(s => s.station.toLowerCase() === from.toLowerCase());
        const destIndex = stops.findIndex(s => s.station.toLowerCase() === to.toLowerCase());
        if (startIndex < 0 || destIndex < 0 || startIndex >= destIndex) continue;

        const startStop = stops[startIndex];
        if (!startStop.departure) continue;

        // Skip trains departing before selected time
        if (startStop.departure < time) continue;

        // Determine 30-minute slot
        const [hourStr, minStr] = startStop.departure.split(":");
        const hour = parseInt(hourStr);
        const minute = parseInt(minStr);
        const slotStart = `${hour.toString().padStart(2,"0")}:${(Math.floor(minute/30)*30).toString().padStart(2,"0")}`;
        const slotEndHour = minute < 30 ? hour : (hour +1)%24;
        const slotEndMin = minute < 30 ? 29 : 59;
        const slotEnd = `${slotEndHour.toString().padStart(2,"0")}:${slotEndMin.toString().padStart(2,"0")}`;
        const slotKey = `${slotStart}-${slotEnd}`;

        if (!slots[slotKey]) slots[slotKey] = [];

        // Fetch crowd level for start station
        let crowd = "Medium";
        try {
          const crowdResp = await fetch(`${BASE_URL}/crowd/${from}`);
          const crowdData = await crowdResp.json();
          crowd = crowdData.crowd_level || "Medium";
        } catch {}

        slots[slotKey].push({
          train_no: train.train_no,
          train_name: train.train_name,
          departure: startStop.departure,
          arrival: stops[destIndex]?.arrival || "--",
          delay: train.delay || 0,
          crowd
        });
      }

      setTrainSlots(slots);
    } catch (err) {
      console.error("Error fetching trains:", err);
    }

    setLoading(false);
    setShowResults(true);
  };

  return (
    <div className="bg-train">
      <div className="dashboard">
        <button className="back-btn" onClick={() => navigate("/details")}>← Back</button>
        <h1>Train Dashboard</h1>

        {userName && (
          <div className="user-info">
            <h2>Welcome, {userName}</h2>
            <p>{from} → {to}</p>
            <p>{userType} Passenger</p>
          </div>
        )}

        <div className="search-box">
          <input placeholder="From Station" value={from} onChange={(e)=>setFrom(e.target.value)}/>
          <input placeholder="To Station" value={to} onChange={(e)=>setTo(e.target.value)}/>
          <input type="time" value={time} onChange={(e)=>setTime(e.target.value)}/>
          <button onClick={handleSearch}>🔹 Search Trains</button>
        </div>

        {loading && <div className="loader"></div>}

        {showResults && (
          <div className="train-list">
            <h2 style={{fontSize:'20px', marginTop:'20px'}}>Available Trains</h2>
            {Object.keys(trainSlots).length===0 && <p>No trains available for the selected time.</p>}
            {Object.entries(trainSlots).map(([slot, trains])=>(
              <div key={slot}>
                <h3 style={{margin:"10px 0"}}>{slot}</h3>
                {trains.map((train, index)=>(
                  <div className="train-card" key={index}>
                    <h3 style={{margin:"0 0 10px 0"}}>{train.train_name}</h3>
                    <p>Departure: {train.departure} • Arrival: {train.arrival} • Delay: {train.delay} min</p>
                    <p style={{color: getCrowdColor(train.crowd)}}>Crowd Level: {train.crowd}</p>
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}