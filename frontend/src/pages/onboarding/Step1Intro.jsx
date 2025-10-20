import React from "react";

export default function Step1Intro({ onNext }) {
  return (
    <div className="flex flex-col items-center justify-center text-center gap-6 p-6">
      <h2 className="text-2xl font-bold text-green-700">
        Welcome to Evolve! 🌿
      </h2>
      <p className="text-gray-600 max-w-md">
        Let’s get to know you better so we can create a customized meal plan
        that matches your lifestyle and goals.
      </p>
      <button
        onClick={onNext}
        className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-md transition"
      >
        Get Started
      </button>
    </div>
  );
}