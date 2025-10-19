export default function StepOne({ formData, setFormData }) {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-semibold">Basic Info</h2>
      <input
        type="number"
        placeholder="Height (cm)"
        value={formData.height}
        onChange={(e) => setFormData({ ...formData, height: e.target.value })}
        className="border px-3 py-2 rounded"
      />
      <input
        type="number"
        placeholder="Weight (kg)"
        value={formData.weight}
        onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
        className="border px-3 py-2 rounded"
      />
    </div>
  );
}