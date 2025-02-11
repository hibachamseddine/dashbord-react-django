import React, { useEffect, useState } from "react";
import axios from "axios";
import '../styles/Dashbord.css';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer } from "recharts";
import RhKPI from "../KPI/RhKPI"; // Import the RhKPI component

const RhDashboard = () => {
  const [kpi, setKpi] = useState(() => {
    const cachedData = localStorage.getItem("kpiData");
    return cachedData ? JSON.parse(cachedData) : null;
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchKpiData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/kpi/");
        console.log("📡 Données reçues de l'API:", response.data);
        
        setKpi(response.data);
        localStorage.setItem("kpiData", JSON.stringify(response.data));
      } catch (err) {
        setError("❌ Erreur de chargement des KPI");
        console.error("Erreur API:", err);
      }
    };

    fetchKpiData();
    
    const intervalId = setInterval(fetchKpiData, 10000); // Vérification sans rechargement
    return () => clearInterval(intervalId);
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!kpi) return <p>⚠️ Aucune donnée disponible.</p>;

  const rhData = [
    { name: "Employés actifs", valeur: kpi.employes_actifs },
    { name: "Employés en congé", valeur: kpi.employes_en_conge },
    { name: "Employés inactifs", valeur: kpi.employes_inactifs }
  ];

  return (
    <div className="dashboardContainer">
      <h2>📊 Tableau de bord - Ressources Humaines</h2>
  
      <div className="kpiContainer">
        {/* Using the RhKPI component to display RH data */}
        <RhKPI kpi={kpi} />
      </div>
  
      <div className="chartsContainer">
        <div className="chartBox">
          <h3>👥 Répartition RH</h3>
          <ResponsiveContainer  width={350} height="85%">
            <LineChart data={rhData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="valeur" stroke="#FFBB28" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default RhDashboard;
