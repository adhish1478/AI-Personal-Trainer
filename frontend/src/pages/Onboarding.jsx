import { useState } from "react";
import StepOne from "./onboarding/StepOne";
import StepTwo from "./onboarding/StepTwo";
import StepThree from "./onboarding/StepThree";
import ProgressBar from "./onboarding/ProgressBar";
import axiosInstance from "../api/axiosInstance";
import { toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";

export default function Onboarding() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    height: "",
    weight: "",
    goal: "",
    lifts_weight: "",
  });

  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
        toast.error("No access token found, please log in again.");
        return;
        }
        console.log(formData)

        axiosInstance.defaults.headers["Authorization"] = `Bearer ${accessToken}`;
        await axiosInstance.patch("accounts/api/profile/", formData); // adjust endpoint
        toast.success("Profile setup complete!");
        navigate("/dashboard");
        } catch (err) {
        toast.error("Something went wrong.");
        console.error(err);
        }
  };

  return (
    <div className="max-w-md mx-auto mt-24 p-4 bg-white rounded-xl shadow-md">
      <ProgressBar step={step} total={3} />
      
      {step === 1 && <StepOne formData={formData} setFormData={setFormData} />}
      {step === 2 && <StepTwo formData={formData} setFormData={setFormData} />}
      {step === 3 && <StepThree formData={formData} setFormData={setFormData} />}

      <div className="flex justify-between mt-4">
        {step > 1 && (
          <button
            className="px-4 py-2 border rounded"
            onClick={() => setStep(step - 1)}
          >
            Previous
          </button>
        )}

        {step < 3 && (
          <button
            className="px-4 py-2 bg-green-600 text-white rounded"
            onClick={() => setStep(step + 1)}
          >
            Next
          </button>
        )}

        {step === 3 && (
          <button
            className="px-4 py-2 bg-green-600 text-white rounded"
            onClick={handleSubmit}
          >
            Finish
          </button>
        )}
      </div>
    </div>
  );
}