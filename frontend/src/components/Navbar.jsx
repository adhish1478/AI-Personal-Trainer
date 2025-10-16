import { useState } from "react";
import LoginModal from "./LoginModal";
import RegisterModal from "./RegisterModal";

export default function Navbar() {
  const [loginOpen, setLoginOpen] = useState(false);
  const [registerOpen, setRegisterOpen] = useState(false);

  return (
    <>
      <nav className="fixed top-0 left-0 w-full bg-white shadow-md z-50 flex justify-between items-center px-6 py-4">
        <h1 className="text-2xl font-bold text-green-600">NutriAI</h1>

        <div className="flex gap-3">
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