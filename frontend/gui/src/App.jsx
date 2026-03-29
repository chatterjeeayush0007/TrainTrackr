import { HashRouter, Routes, Route } from "react-router-dom"; 
import Landing from "./pages/Landing";
import UserDetails from "./pages/UserDetails";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <HashRouter> {}
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/details" element={<UserDetails />} />
      </Routes>
    </HashRouter>
  );
}

export default App;