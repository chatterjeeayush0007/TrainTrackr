import { useState } from "react";
import "../styles/landing.css";
import { useNavigate } from "react-router-dom";
import { auth, googleProvider } from "../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
} from "firebase/auth";

export default function Landing() {
  const [showModal, setShowModal] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleEmailSignIn = async () => {
    setError("");
    try {
      await signInWithEmailAndPassword(auth, email, password);
      navigate("/details");
    } catch (err) {
      if (err.code === "auth/user-not-found") {
        try {
          await createUserWithEmailAndPassword(auth, email, password);
          navigate("/details");
        } catch (createErr) {
          setError(createErr.message);
        }
      } else {
        setError(err.message);
      }
    }
  };

  const handleGoogleSignIn = async () => {
    setError("");
    try {
      const result = await signInWithPopup(auth, googleProvider);
      if (!name) setName(result.user.displayName || "");
      navigate("/details");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="title-gradient">TrainTrackr</h1>
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

            {error && <p className="auth-error">{error}</p>}

            {/* Google Sign-In button */}
            <button className="login-btn google-btn" onClick={handleGoogleSignIn}>
              <span className="google-icon">G</span> Sign in with Google
            </button>

            {/* Small OR separator */}
            <div className="or-separator">or</div>

            {/* Input fields */}
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <p className="auth-note">
              New user? Just continue — your account will be created automatically
            </p>

            {/* Continue button */}
            <button className="login-btn" onClick={handleEmailSignIn}>
              Continue →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}