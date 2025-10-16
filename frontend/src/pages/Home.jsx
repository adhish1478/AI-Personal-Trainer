import { useState } from "react"
import {ArrowRightIcon} from '@heroicons/react/24/solid'
import heroImage from "../assets/logo2.png";

export default function Home() {
    const [showAuth, setShowAuth] = useState(false);
    console.log(showAuth);

    return (
    <div className="flex flex-col items-center justify-between min-h-screen bg-gradient-to-b from-white to-green-100 text-gray-800 p-6 pt-[130px]">

      {/* Hero Section */}
      <div className="flex flex-col md:flex-row items-center justify-between w-full max-w-5xl mt-16 space-y-8 md:space-y-0">
        {/* Left Text */}
        <div className="flex flex-col space-y-6 text-center md:text-left md:w-1/2">
          <h2 className="text-4xl md:text-6xl font-bold leading-tight text-gray-900">
            Eat Smart. <br />
            <span className="text-green-600">Stay Healthy.</span>
          </h2>
          <p className="text-gray-600 text-lg">
            Personalized AI-powered meal plans for your goals — built by smart nutrition algorithms.
          </p>

          <button
            onClick={() => setShowAuth(true)}
            className="flex items-center justify-center bg-green-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-green-700 transition md:self-start cursor-pointer"
          >
            Get Started
            <ArrowRightIcon className="w-5 h-5 ml-2" />
          </button>
        </div>

        {/* Right Image */}
        <div className="md:w-1/2 flex justify-center">
          <img
            src={heroImage}
            alt="Healthy food"
            className="w-64 md:w-96 drop-shadow-lg rounded-2xl"
          />
        </div>
      </div>

      {/* Footer */}
      <footer className="text-sm text-gray-500 mt-16 mb-6">
        © 2025 AI Nutrition Coach. All rights reserved.
      </footer>
    </div>
  );
}