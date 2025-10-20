import React, { useState } from "react";

const cuisineOptions = [
  "Indian", "Mediterranean", "Chinese",
  "Italian", "American", "Japanese", "Mexican"
];

export default function Step6Cuisine({ formData, setFormData, onNext, onBack }) {
  const [otherCuisine, setOtherCuisine] = useState("");

  const handleCuisineToggle = (item) => {
    const currentCuisines = formData.cuisine || [];

    const updatedCuisines = currentCuisines.includes(item)
      ? currentCuisines.filter(c => c !== item)
      : [...currentCuisines, item];

    setFormData({
      ...formData,
      cuisine: updatedCuisines
    });
  };

  const handleOtherCuisineBlur = () => {
    if (!otherCuisine.trim()) return;

    const currentCuisines = formData.cuisine || [];

    const newCuisines = otherCuisine
      .split(",")
      .map(c => c.trim())
      .filter(Boolean);

    const uniqueCuisines = Array.from(
      new Set([...currentCuisines, ...newCuisines])
    );

    setFormData({
      ...formData,
      cuisine: uniqueCuisines
    });

    setOtherCuisine("");
  };

  return (
    <div className="p-6 flex flex-col gap-4">
      <h2 className="text-xl font-semibold text-green-700">What cuisines do you prefer?</h2>
      <p className="text-gray-500">Select all that apply.</p>

      <div className="grid grid-cols-2 gap-3">
        {cuisineOptions.map((item) => (
          <label key={item} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={formData.cuisine?.includes(item) || false}
              onChange={() => handleCuisineToggle(item)}
            />
            <span>{item}</span>
          </label>
        ))}
      </div>

      <input
        type="text"
        placeholder="Other cuisines (comma-separated)"
        value={otherCuisine}
        onChange={(e) => setOtherCuisine(e.target.value)}
        onBlur={handleOtherCuisineBlur}
        className="border border-gray-300 rounded-md px-3 py-2 focus:ring-green-600"
      />
    </div>
  );
}