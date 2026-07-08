import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "@/pages/Home";
import Choice from "@/pages/Choice";
import Judge from "@/pages/Judge";
import Short from "@/pages/Short";
import Calc from "@/pages/Calc";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/choice" element={<Choice />} />
        <Route path="/judge" element={<Judge />} />
        <Route path="/short" element={<Short />} />
        <Route path="/calc" element={<Calc />} />
      </Routes>
    </Router>
  );
}
