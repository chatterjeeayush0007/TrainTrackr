import { useState } from "react";
import "../styles/landing.css";
import { useNavigate } from "react-router-dom";

export default function Landing() {
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">TrainTrackr</h1>
        <p className="subtitle">Smart Train Companion</p>

        <button className="btn" onClick={() => setShowModal(true)}>
          Get Started
        </button>
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <button className="close" onClick={() => setShowModal(false)}>
              ×
            </button>

            <h2>Login / Signup</h2>
            <p className="auth-subtitle">Enter your details to continue</p>
            
            <input type="text" placeholder="Full Name" />
            <input type="email" placeholder="Email" />
            <input type="password" placeholder="Password" />
            
            <p className="auth-note">
              New user? Just continue — your account will be created automatically
            </p>

            <button
              className="login-btn"
              onClick={() => navigate("/details")}
            >
              Continue → 
            </button>
          </div>
        </div>
      )}
    </div>
  );
}