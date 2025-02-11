import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProjetsDashboard from "./components/ProjetsDashboard";
import RhDashboard from "./components/RhDashboard"; 
import EmployesDashboard from "./components/EmployesDashboard"; 
import Acceuil from "./components/Acceuil";

const App = () => {
  return (
    <Router>
    <Navbar />
    <Routes>
    <Route path="/" element={<Acceuil />} />
      <Route path="/projets" element={<ProjetsDashboard />} />
      <Route path="/rh" element={<RhDashboard />} />
      <Route path="/employes" element={<EmployesDashboard />} />
    </Routes>
  </Router>
  );
};

export default App;
