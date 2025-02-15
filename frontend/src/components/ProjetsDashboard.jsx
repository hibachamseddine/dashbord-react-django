import React, { useEffect, useState } from "react";
import axios from "axios";
import '../styles/Dashbord.css';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import ProjetsKPI from "../KPI/ProjetsKPI"// Import the ProjetsKPI component

const ProjetsDashboard = () => {
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
    
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/projects/");

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
  if (!kpi) return <p>⚠️ Aucune donnée disponible.</p>;

  const projetsData = [
    { name: "Terminé", value: kpi.projets_termines },
    { name: "En cours", value: kpi.projets_en_cours }
  ];

  return (
    <div className="dashboardContainer">
      <h2>📊 Tableau de bord - Projets</h2>
  
      <div className="kpiContainer">
        {/* Using the ProjetsKPI component to display project-related KPIs */}
        <ProjetsKPI kpi={kpi} />
      </div>
  
      <div className="chartsContainer">
        <div className="chartBox">
          <h3>📊 État des Projets</h3>
          <ResponsiveContainer width={350} height="85%">

            <BarChart data={projetsData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ProjetsDashboard;
