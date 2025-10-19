export default function StepOne({ formData, setFormData }) {
   
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-semibold">Basic Info</h2>
      <select
        value={formData.activity_level}
        onChange={(e) => setFormData({ ...formData, activity_level: e.target.value })}
        className="border px-3 py-2 rounded"
      >
        <option value="">Select Activity Level</option>
        <option value="sedentary">Sedentary</option>
        <option value="lightly_active">Lightly Active</option>
        <option value="moderately_active">Moderately Active</option>
        <option value="very_active">Very Active</option>
        <option value="extra_active">Extra Active</option>
      </select>
      <select
        value={formData.goal}
        onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
        className="border px-3 py-2 rounded"
      >
        <option value="">Select Your Goal</option>
        <option value="lose_1kg">Lose 1 kg/week</option>
        <option value="lose_0.75kg">Lose 0.75 kg/week</option>
        <option value="lose_0.5kg">Lose 0.5 kg/week</option>
        <option value="lose_0.25kg">Lose 0.25 kg/week</option>
        <option value="maintain">Maintain weight</option>
        <option value="lean_bulk">Lean bulk</option>
        <option value="gain_0.25kg">Gain 0.25 kg/week</option>
        <option value="gain_0.5kg">Gain 0.5 kg/week</option>
        <option value="gain_0.75kg">Gain 0.75 kg/week</option>
        <option value="gain_1kg">Gain 1 kg/week</option>
      </select>

      <select
        value={formData.lifts_weight}
        onChange={(e) => setFormData({ ...formData, lifts_weight: e.target.value })}
        className="border px-3 py-2 rounded"
      >
        <option value="">Do you Do Strength Training?</option>
        <option value="True">Yes</option>
        <option value="False">No</option>
      </select>
    </div>
  );
}