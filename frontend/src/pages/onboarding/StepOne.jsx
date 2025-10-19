export default function StepOne({ formData, setFormData }) {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-semibold">Basic Info</h2>
      <input
        type="number"
        placeholder="Age"
        value={formData.age}
        onChange={(e) => setFormData({ ...formData, age: e.target.value })}
        className="border px-3 py-2 rounded"
      />
      <select
        value={formData.gender}
        onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
        className="border px-3 py-2 rounded"
      >
        <option value="">Select Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>
    </div>
  );
}