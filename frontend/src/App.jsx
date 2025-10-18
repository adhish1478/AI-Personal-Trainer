import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import { Toaster } from "react-hot-toast";
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';



export default function App() {
  return (
    <>
      <Navbar />
      <Toaster />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
    </>
  );
}