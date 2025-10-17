import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import { Toaster } from "react-hot-toast";


export default function App() {
  return (
    <>
      <Navbar />
      <Toaster />
      <Home />
    </>
  );
}