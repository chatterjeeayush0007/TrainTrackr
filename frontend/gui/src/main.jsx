import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("./sw.js")
      .then(() => console.log("PWA Ready"))
      .catch((err) => console.log("SW Error:", err));
  });
}
// Register Service Worker
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js") // absolute path is important
      .then((registration) => {
        console.log("PWA Ready: Service Worker registered", registration);
      })
      .catch((error) => {
        console.error("Service Worker registration failed:", error);
      });
  });
}