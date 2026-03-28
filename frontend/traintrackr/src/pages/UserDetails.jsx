import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/details.css";

export default function UserDetails() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    pincode: "",
    type: "daily",
    ticketType: "single", 
    from: "",
    to: "",
    time: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    localStorage.setItem("userDetails", JSON.stringify(form));
    navigate("/dashboard");
  };

  return (
    <div className="bg-train">
      <div className="bg-content">
        <div className="details-container">
          <h2>Journey Details</h2>

          <div className="form-grid">
            <input name="name" placeholder="Full Name" onChange={handleChange} />
            <input name="pincode" placeholder="Pincode" onChange={handleChange} />

            <select name="type" onChange={handleChange}>
              <option value="daily">Daily Passenger</option>
              <option value="occasional">Occasional</option>
            </select>

            <select name="ticketType" onChange={handleChange}>
              <option value="single">Single Journey</option>
              <option value="return">Return Journey</option>
              <option value="seasonal">Seasonal Pass</option>
            </select>

            <input name="from" placeholder="From Station" onChange={handleChange} />
            <input name="to" placeholder="To Station" onChange={handleChange} />

            <input type="time" name="time" onChange={handleChange} />
          </div>

          <p className="info-note">
            The data collected is essential for better crowd prediction and commute optimization.
          </p>

          <button className="continue-btn" onClick={handleSubmit}>
            Continue →
          </button>
        </div>
      </div>
    </div>
  );
}