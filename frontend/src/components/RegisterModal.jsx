import { Fragment, useState, useContext } from "react";
import { Dialog, Transition } from "@headlessui/react";
import GoogleAuth from '/src/components/GoogleAuth';
import axiosInstance from "/src/api/axiosInstance";
import { REGISTER } from "/src/api/endpoints";
import toast from "react-hot-toast";
import LoginModal from "./LoginModal";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";


export default function RegisterModal({ isOpen, onClose, switchToLogin }) {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const processName= (fullName) => {
    const [first_name, ...rest] = fullName.trim().split(" ");
    const last_name= rest.join(" ");
    return {first_name, last_name};
  }

  const handleRegister= async () => {
    const {first_name, last_name}= processName(form.name);

    const payload_name= {
      first_name,
      last_name}
    const registerPayload= {
      email: form.email,
      password: form.password
    };
    
      try {
    // 1️⃣ Register user
    const registerResponse = await axiosInstance.post(REGISTER, registerPayload);

    toast.success("Registration successful! Logging you in...");

    // 2️⃣ Immediately log them in to get tokens
    const loginResponse = await axiosInstance.post("accounts/token/", {
      email: form.email,
      password: form.password
    });

    const { access, refresh, user } = loginResponse.data;

    login(user, access, refresh);
    axiosInstance.defaults.headers["Authorization"] = `Bearer ${access}`;


    // 3️⃣ Now update the UserProfile
    await axiosInstance.patch("accounts/api/profile/", {
      first_name,
      last_name
    });

    console.log("Profile details saved!");

    if (!user.is_profile_completed) {
        navigate('/onboarding');
        toast.success("Let's complete your profile!");
      } else {
        navigate('/dashboard');
        toast.success("Welcome back!");
      }

    onClose();

    } catch (error) {
      console.error("Registration failed:", error);

      // Failure toast
      toast.error("Registration failed. Try again.");
    }
  };

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        {/* Overlay */}
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 backdrop-blur-sm" />
        </Transition.Child>

        {/* Modal panel */}
        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <Dialog.Title
                  as="h3"
                  className="text-lg font-medium leading-6 text-gray-900 text-center"
                >
                  Register
                </Dialog.Title>

                <div className="mt-4 flex flex-col gap-4">
                  <input
                    type="text"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    placeholder="Full Name"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600"
                  />
                  <input
                    type="email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    placeholder="Email"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600"
                  />
                  <input
                    type="password"
                    name="password"
                    value={form.password}
                    onChange={handleChange}
                    placeholder="Password"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600"
                  />

                  <p className="text-sm text-center text-gray-600">
                    Already have an account?{" "}
                    <span
                      onClick={switchToLogin}
                      className="text-green-600 cursor-pointer hover:underline font-medium"
                    >
                      Login here
                    </span>
                  </p>

                  <button onClick={handleRegister} className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md transition cursor-pointer">
                    Register
                  </button>

                  <GoogleAuth />
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}