import { useState } from "react";
import StepOne from "./onboarding/Step1Intro";
import StepTwo from "./onboarding/Step2Basic";
import StepThree from "./onboarding/Step3BodyStats";
import StepFour from "./onboarding/Step4Activity";
import StepFive from "./onboarding/Step5Allergies"
import StepSix from "./onboarding/Step6Cuisine"
import StepSeven from "./onboarding/Step7Additional"
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
    allergies:"",
    cuisine:"",
    remarks: ""
  });

  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
        console.log(formData)
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
      <ProgressBar step={step} total={6} />

      {step === 1 && <StepOne onNext={() => setStep(2)}/>}
      {step === 2 && <StepTwo formData={formData} setFormData={setFormData} />}
      {step === 3 && <StepThree formData={formData} setFormData={setFormData} />}
      {step === 4 && <StepFour formData={formData} setFormData={setFormData} />}
      {step === 5 && <StepFive formData={formData} setFormData={setFormData} />}
      {step === 6 && <StepSix formData={formData} setFormData={setFormData} />}
      {step === 7 && <StepSeven formData={formData} setFormData={setFormData} />}

      <div className="flex justify-between mt-4">
        {step > 1 && (
          <button
            className="px-4 py-2 border rounded"
            onClick={() => setStep(step - 1)}
          >
            Previous
          </button>
        )}

        {step < 7 && step > 1 && (
          <button
            className="px-4 py-2 bg-green-600 text-white rounded"
            onClick={() => setStep(step + 1)}
          >
            Next
          </button>
        )}

        {step === 7 && (
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