import { Fragment, useState, useContext } from "react";
import { Dialog, Transition } from "@headlessui/react";
import GoogleAuth from "/src/components/GoogleAuth";
import axiosInstance from "/src/api/axiosInstance";
import { LOGIN } from "/src/api/endpoints";
import { toast } from "react-hot-toast"; // install if not done: npm i react-hot-toast
import { AuthContext } from "/src/context/AuthContext"; // we'll create this
import { useNavigate } from 'react-router-dom';


export default function LoginModal({ isOpen, onClose, switchToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();


  const handleLogin = async () => {
    const payload = { email, password };

    try {
      const response = await axiosInstance.post(LOGIN, payload);
      const { user, access, refresh } = response.data;

      // Save tokens to localStorage
      login(user, access, refresh);

      // Update default Axios headers
      axiosInstance.defaults.headers["Authorization"] = `Bearer ${access}`;

      toast.success("Login successful!");
    

      // ✅ Decide where to go next
      if (!user.is_profile_completed) {
        toast.success("Let's complete your profile!");
        navigate('/onboarding');
      } else {
        toast.success("Welcome back!");
        navigate('/dashboard');
      }
      onClose(); // close modal


    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      toast.error("Invalid credentials, please try again.");
      setPassword(""); // clear password field
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

        {/* Modal */}
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
                  Login
                </Dialog.Title>

                <div className="mt-4 flex flex-col gap-4">
                  <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600"
                  />
                  <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-600"
                  />

                  <button
                    onClick={handleLogin}
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md"
                  >
                    Login
                  </button>

                  <p className="text-sm text-center text-gray-600">
                    Not registered?{" "}
                    <span
                      onClick={switchToRegister}
                      className="text-green-600 cursor-pointer hover:underline"
                    >
                      Register here
                    </span>
                  </p>

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