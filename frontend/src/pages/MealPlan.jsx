import { useEffect, useState } from "react";
import axiosInstance from "../api/axiosInstance";

export default function MealPlan() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [meal, setMeal] = useState(null);

  const createAIMeal = async () => {
    try {
      setLoading(true);
      setError("");
      // Assuming backend generates AI meal plan from profile
      const res = await axiosInstance.post("diet/meals/create/ai/", {});
      setMeal(res.data);
    } catch (e) {
      setError("Failed to generate meal plan.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    createAIMeal();
  }, []);

  return (
    <div className="pt-20 px-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Your AI Meal Plan</h1>
      <div className="mb-4">
        <button onClick={createAIMeal} className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">
          Regenerate Plan
        </button>
      </div>
      {loading && <p>Generating...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {meal && (
        <div className="grid gap-4">
          <div className="p-4 bg-white rounded shadow">
            <h2 className="text-xl font-semibold">Overview</h2>
            <p className="text-sm text-gray-600">Calories: {meal.calories}</p>
            <p className="text-sm text-gray-600">Carbs: {meal.carbs}g • Protein: {meal.protein}g • Fats: {meal.fats}g</p>
          </div>

          {Array.isArray(meal.items) && meal.items.map((item, idx) => (
            <div key={idx} className="p-4 bg-white rounded shadow">
              <h3 className="font-semibold">{item.name}</h3>
              <p className="text-sm text-gray-600">{item.quantity} {item.unit}</p>
              {item.notes && <p className="text-sm">{item.notes}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


