export default function ProgressBar({ step, total }) {
    const progressStep = step - 1;
    const percentage = (progressStep / total) * 100;
    return (
        <div className="w-full bg-gray-200 h-2 rounded-full mb-4">
        <div
            className="bg-green-600 h-2 rounded-full transition-all"
            style={{ width: `${percentage}%` }}
        ></div>
        {progressStep > 0 && <p className="text-sm text-gray-500">{progressStep} of {total}</p>}
        </div>
    );
}