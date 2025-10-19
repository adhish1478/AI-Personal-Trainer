import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import LoginModal from "./LoginModal";
import RegisterModal from "./RegisterModal";
import {AuthContext} from "../context/AuthContext";

export default function Navbar() {
  const [loginOpen, setLoginOpen] = useState(false);
  const [registerOpen, setRegisterOpen] = useState(false);

  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };



  return (
    <>
      <nav className="w-full bg-white shadow-sm fixed top-0 left-0 z-50 p-4 flex justify-center">
      <div className="w-full max-w-5xl flex justify-between items-center">
        <section className="flex items-center">
            <img src="./src/assets/logo.png" alt="Logo" className="w-8 h-8 inline-block mr-2"/>
            <h1 className="text-xl font-bold text-green-600">Evolve</h1>
        </section>

        <section className="flex items-center gap-4">
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition"
              >
                Logout
              </button>
            ) : (
              <>
                <button
                  onClick={() => setLoginOpen(true)}
                  className="border border-green-600 text-green-600 px-4 py-2 rounded-md hover:bg-green-50 transition"
                >
                  Login
                </button>

                <button
                  onClick={() => setRegisterOpen(true)}
                  className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md transition"
                >
                  Get Started
                </button>
              </>
            )}
          </section>
        </div>
      </nav>

      <LoginModal
        isOpen={loginOpen}
        onClose={() => setLoginOpen(false)}
        switchToRegister={() => {
          setLoginOpen(false);
          setRegisterOpen(true);
        }}
      />
      <RegisterModal
        isOpen={registerOpen}
        onClose={() => setRegisterOpen(false)}
        switchToLogin={() => {
          setRegisterOpen(false);
          setLoginOpen(true);
        }}
      />
    </>
  );
}