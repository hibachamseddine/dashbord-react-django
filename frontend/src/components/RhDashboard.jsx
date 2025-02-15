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
      setKpi(response.data);
      localStorage.setItem("kpiData", JSON.stringify(response.data));
    } catch (err) {
      setError("❌ Erreur de chargement des KPI");
      
    }
  };
  fetchKpiData();
  
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/employees/");
  
    socket.onopen = () => {
      console.log("✅ WebSocket connecté !");
    };
  
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      console.log("🔄 Mise à jour reçue :", data.message);
      
      fetchKpiData();
      
    };
  
    socket.onerror = (error) => {
      console.error("❌ WebSocket Erreur :", error);
    };
  
    socket.onclose = () => {
      console.log("❌ WebSocket fermé !");
    };
  
    return () => socket.close();
  }, []);
  


  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!kpi ) return <p>⚠️ Aucune donnée disponible.</p>;

  const rhData = [
    { name: "Employés actifs", valeur: kpi.employes_actifs },
    { name: "Employés en congé", valeur: kpi.employes_en_conge },
    { name: "Employés Sortie", valeur: kpi.employes_Sortis }
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
