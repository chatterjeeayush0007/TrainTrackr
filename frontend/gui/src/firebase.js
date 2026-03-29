// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBbO2EaKOJxmyFwBT-DO0sxbEISKI7YeBI",
  authDomain: "traintrackr-ea971.firebaseapp.com",
  projectId: "traintrackr-ea971",
  storageBucket: "traintrackr-ea971.appspot.com",
  messagingSenderId: "114981450104",
  appId: "1:114981450104:web:279d3571077924591a588d"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

// Email/Password signup
export const signupWithEmail = (email, password) => {
  return createUserWithEmailAndPassword(auth, email, password);
};

// Email/Password login
export const loginWithEmail = (email, password) => {
  return signInWithEmailAndPassword(auth, email, password);
};

// Google login
export const loginWithGoogle = () => {
  return signInWithPopup(auth, googleProvider);
};