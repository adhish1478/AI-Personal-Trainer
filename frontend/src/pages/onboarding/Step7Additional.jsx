import React from "react";

export default function Step7Additional({ formData, setFormData, onBack, onFinish }) {
  return (
    <div className="p-6 flex flex-col gap-4">
      <h2 className="text-xl font-semibold text-green-700">
        Anything else you'd like us to know?
      </h2>
      <p className="text-gray-500">
        This helps us further personalize your plan. Feel free to mention likes, dislikes, religious
        restrictions, or cooking habits.
      </p>

      <textarea
        rows="5"
        placeholder="Type here..."
        value={formData.remarks || ""}
        onChange={(e) => setFormData({ ...formData, remarks: e.target.value })}
        className="border border-gray-300 rounded-md px-3 py-2 focus:ring-green-600"
      ></textarea>

    </div>
  );
}