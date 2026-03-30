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
    if (level === "Low") return "#4ade80"; // Brighter green for dark mode
    if (level === "Medium") return "#fbbf24"; // Brighter yellow/orange
    if (level === "High") return "#f87171"; // Brighter red
    return "#9ca3af";
  };

  const handleSearch = async () => {
    if (!from || !to || !time) return;

    setLoading(true);
    setShowResults(false);

    try {
      const trainsResp = await fetch(`${BASE_URL}/trains/`);
      const trainsData = await trainsResp.json();
      const allTrains = trainsData.trains || [];

      const slots = {};

      for (const train of allTrains) {
        const routeResp = await fetch(`${BASE_URL}/trains/${train.train_no}/route`);
        const routeData = await routeResp.json();
        const stops = routeData.stops || [];

        const startIndex = stops.findIndex(s => s.station.toLowerCase() === from.toLowerCase());
        const destIndex = stops.findIndex(s => s.station.toLowerCase() === to.toLowerCase());
        if (startIndex < 0 || destIndex < 0 || startIndex >= destIndex) continue;

        const startStop = stops[startIndex];
        if (!startStop.departure) continue;

        if (startStop.departure < time) continue;

        const [hourStr, minStr] = startStop.departure.split(":");
        const hour = parseInt(hourStr);
        const minute = parseInt(minStr);
        const slotStart = `${hour.toString().padStart(2,"0")}:${(Math.floor(minute/30)*30).toString().padStart(2,"0")}`;
        const slotEndHour = minute < 30 ? hour : (hour + 1) % 24;
        const slotEndMin = minute < 30 ? 29 : 59;
        const slotEnd = `${slotEndHour.toString().padStart(2,"0")}:${slotEndMin.toString().padStart(2,"0")}`;
        const slotKey = `${slotStart}-${slotEnd}`;

        if (!slots[slotKey]) slots[slotKey] = [];

        let crowd = "Medium";
        try {
          const crowdResp = await fetch(`${BASE_URL}/stations/crowd/${from}`);
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
          <button onClick={handleSearch}>Search Trains</button>
        </div>

        {loading && <div className="loader" style={{marginTop: '20px', color: 'white'}}>Loading...</div>}

        {showResults && (
          <div className="train-list" style={{ maxHeight: '55vh', overflowY: 'auto', paddingRight: '10px', marginTop: '20px' }}>
            <h2 style={{fontFamily: "'Merienda', cursive", fontSize:'24px', color: 'white', textShadow: '0 2px 4px rgba(0,0,0,0.5)'}}>
              Available Trains
            </h2>
            {Object.keys(trainSlots).length === 0 && <p style={{color: 'white'}}>No trains available for the selected time.</p>}
            
            {Object.entries(trainSlots)
              .sort((a, b) => a[0].localeCompare(b[0])) 
              .map(([slot, trains]) => (
              <div key={slot}>
                <h3 style={{
                  fontFamily: "'Poppins', sans-serif",
                  fontWeight: '600',
                  margin:"15px 0 10px 0", 
                  position: 'sticky', 
                  top: 0, 
                  backgroundColor: 'rgba(30, 30, 30, 0.95)', 
                  color: 'white',
                  padding: '8px 12px', 
                  borderRadius: '8px', 
                  zIndex: 1,
                  boxShadow: '0 2px 8px rgba(0,0,0,0.3)'
                }}>
                  {slot}
                </h3>
                
                {trains
                  .sort((a, b) => a.departure.localeCompare(b.departure))
                  .map((train, index) => (
                  <div className="train-card" key={index}>
                    <h3>{train.train_name}</h3>
                    <p><strong>Departure:</strong> {train.departure} &nbsp;•&nbsp; <strong>Arrival:</strong> {train.arrival}</p>
                    <p><strong>Delay:</strong> {train.delay} min</p>
                    <p style={{color: getCrowdColor(train.crowd), fontWeight: '600', marginTop: '8px'}}>
                      Crowd Level: {train.crowd}
                    </p>
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