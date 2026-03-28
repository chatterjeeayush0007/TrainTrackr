
import { useState } from "react";
import "../styles/dashboard.css";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const user = JSON.parse(localStorage.getItem("userDetails"));

  const [from, setFrom] = useState(user?.from || "");
  const [to, setTo] = useState(user?.to || "");
  const [date, setDate] = useState("");
  const [time, setTime] = useState(user?.time || "");

  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const navigate = useNavigate();

  const getTrains = () => {
    if (!time) return [];
    const hour = parseInt(time.split(":")[0]);
    if (hour < 12) {
      return [{ name: "Morning Express", status: "On Time", platform: 1, insight: "Smooth morning route", color: "green" }];
    } else if (hour < 18) {
      return [{ name: "Afternoon Superfast", status: "+5 min delayed", platform: 2, insight: "Moderate traffic", color: "red" }];
    } else {
      return [{ name: "Night Express", status: "On Time", platform: 4, insight: "Less congestion", color: "green" }];
    }
  };

  const handleSearch = () => {
    setLoading(true);
    setShowResults(false);
    setTimeout(() => {
      setLoading(false);
      setShowResults(true);
    }, 1200);
  };

  return (
    <div className="bg-train">
      <div className="dashboard">
        <button className="back-btn" onClick={() => navigate("/details")}>
          ← Back
        </button>
        
        <h1>Train Dashboard</h1>

        {user && (
          <div className="user-info">
            <h2>Welcome, {user.name}</h2>
            <p>{user.from} → {user.to}</p>
            <p>{user.type} Passenger</p>
          </div>
        )}

        <div className="search-box">
          <input
            placeholder="From Station"
            value={from}
            onChange={(e) => setFrom(e.target.value)}
          />
          <input
            placeholder="To Station"
            value={to}
            onChange={(e) => setTo(e.target.value)}
          />
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
          <input
            type="time"
            value={time}
            onChange={(e) => setTime(e.target.value)}
          />
          <button onClick={handleSearch}>🔹 Search Trains</button>
        </div>

        {loading && <div className="loader"></div>}

        {showResults && (
          <div className="train-list">
            <h2 style={{fontSize: '20px', marginTop: '20px'}}>Available Trains</h2>
            {getTrains().map((train, index) => (
              <div className="train-card" key={index}>
                <h3 style={{margin: '0 0 10px 0'}}>{train.name}</h3>
                <p>Platform: {train.platform} • Status: <span className={train.color}>{train.status}</span></p>
                <p style={{fontSize: '13px', opacity: 0.8}}>{train.insight}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}