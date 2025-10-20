import React, { useState } from "react";

const allergyOptions = [
  "Eggs", "Dairy", "Gluten", "Soy",
  "Peanuts", "Tree Nuts", "Fish", "Shellfish"
];

export default function Step5Allergies({ formData, setFormData, onNext, onBack }) {
  const [otherAllergy, setOtherAllergy] = useState("");

  const handleAllergyToggle = (item) => {
    const currentAllergies = formData.allergies || [];

    const updatedAllergies = currentAllergies.includes(item)
      ? currentAllergies.filter(a => a !== item)
      : [...currentAllergies, item];

    setFormData({
      ...formData,
      allergies: updatedAllergies
    });
  };

  const handleOtherAllergyBlur = () => {
    if (!otherAllergy.trim()) return;

    const currentAllergies = formData.allergies || [];

    // Split by commas, trim, and filter empty values
    const newAllergies = otherAllergy
      .split(",")
      .map(a => a.trim())
      .filter(Boolean);

    // Avoid duplicates
    const uniqueAllergies = Array.from(
      new Set([...currentAllergies, ...newAllergies])
    );

    setFormData({
      ...formData,
      allergies: uniqueAllergies
    });

    setOtherAllergy("");
  };

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-semibold text-green-700">Do you have any allergies?</h2>
      <div className="grid grid-cols-2 gap-3">
        {allergyOptions.map((item) => (
          <label key={item} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={formData.allergies?.includes(item) || false}
              onChange={() => handleAllergyToggle(item)}
            />
            <span>{item}</span>
          </label>
        ))}
      </div>

      <input
        type="text"
        placeholder="Other allergies (comma-separated)"
        value={otherAllergy}
        onChange={(e) => setOtherAllergy(e.target.value)}
        onBlur={handleOtherAllergyBlur}
        className="border border-gray-300 rounded-md px-3 py-2 focus:ring-green-600"
      />
    </div>
  );
}