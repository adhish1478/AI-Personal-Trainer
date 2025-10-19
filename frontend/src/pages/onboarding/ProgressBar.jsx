export default function ProgressBar({ step, total }) {
  const percentage = (step / total) * 100;
  return (
    <div className="w-full bg-gray-200 h-2 rounded-full mb-4">
      <div
        className="bg-green-600 h-2 rounded-full transition-all"
        style={{ width: `${percentage}%` }}
      ></div>
    </div>
  );
}