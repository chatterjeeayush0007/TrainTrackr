import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/details.css";
import { auth } from "../firebase";

export default function UserDetails() {
  const navigate = useNavigate();
  const storedDetails = JSON.parse(localStorage.getItem("userDetails")) || {};

  const [form, setForm] = useState({
    name: storedDetails.name || "",
    email: storedDetails.email || "",
    pincode: storedDetails.pincode || "",
    type: storedDetails.type || "daily",
    ticketType: storedDetails.ticketType || "single",
    from: storedDetails.from || "",
    to: storedDetails.to || "",
    time: storedDetails.time || "",
  });

  useEffect(() => {
    const user = auth.currentUser;
    if (user) {
      setForm((prev) => ({
        ...prev,
        name: prev.name || user.displayName || "",
        email: prev.email || user.email || "",
      }));
    }
  }, []);

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
            <input name="name" placeholder="Full Name" value={form.name} onChange={handleChange} />
            <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
            <input name="pincode" placeholder="Pincode" value={form.pincode} onChange={handleChange} />
            <select name="type" value={form.type} onChange={handleChange}>
              <option value="daily">Daily Passenger</option>
              <option value="occasional">Occasional</option>
            </select>
            <input name="from" placeholder="From Station" value={form.from} onChange={handleChange} />
            <input name="to" placeholder="To Station" value={form.to} onChange={handleChange} />
            <input type="time" name="time" value={form.time} onChange={handleChange} />
          </div>
          <button className="continue-btn" onClick={handleSubmit}>Continue →</button>
        </div>
      </div>
    </div>
  );
}