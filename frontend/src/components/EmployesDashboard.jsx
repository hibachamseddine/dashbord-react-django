import React, { useEffect, useState } from "react";
import axios from "axios";
import '../styles/Dashbord.css';
import EmployeKPI from "../KPI/EmployeKPI";  // Import the EmployeKPI component

const EmployeDashboard = () => {
  const [kpi, setKpi] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [error, setError] = useState(null);

  const fetchEmployeeData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/employees/");
      setEmployees(response.data);
    } catch (err) {
      setError("Erreur de chargement des employés");
    }
  };
  const removeEmployeeLocally = (employeeId) => {
    setEmployees(prevEmployees => prevEmployees.filter(emp => emp.id !== employeeId));
  };
  
  
  
  useEffect(() => {

    fetchEmployeeData();
    const fetchKpiData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/kpi/");
        setKpi(response.data);
      } catch (err) {
        setError("Erreur de chargement des KPI");
      }
    };

    fetchKpiData();


    const socket = new WebSocket("ws://127.0.0.1:8000/ws/employees/");

    socket.onopen = () => {
      console.log("✅ WebSocket connecté !");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "update") {
        console.log("🔄 Mise à jour reçue :", data.message);
        fetchEmployeeData(); // 🔄 Rafraîchir les employés automatiquement
      } else if (data.type === "delete") {
        console.log(`🗑️ Suppression de l'employé ID: ${data.employee_id}`);
        removeEmployeeLocally(data.employee_id);
        fetchEmployeeData(); 
      }
    };

    socket.onerror = (error) => {
      console.error("❌ WebSocket Erreur :", error);
    };

    socket.onclose = () => {
      console.log("❌ WebSocket fermé !");
    };

    return () => socket.close();
  }, []);



  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/employees/${id}/`);
      console.log(`✅ Employé ${id} supprimé !`);
      // ❌ PAS BESOIN de fetchEmployeeData() car WebSocket mettra à jour React
    } catch (err) {
      console.error("❌ Erreur lors de la suppression :", err);
    }
  };

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!kpi || !employees.length) return <p>⚠️ Aucune donnée disponible.</p>;

  return (
    <div className="dashboardContainer">
      <div className="kpiContainer">
        <EmployeKPI kpi={kpi} />
      </div>

      <div className="employeeTableContainer">
        <h3>📋 Liste des Employés</h3>
        <table className="employeeTable">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Rôle</th>
              <th>Score de productivité</th>
              <th>Absences</th>
              <th>Statut</th>
              <th>Âge</th>
              <th>Email</th>
              <th>Photo</th>
            </tr>
          </thead>
          <tbody>
            {employees.map(emp => (
              <tr key={emp.id}>
                <td>{emp.name}</td>
                <td>{emp.role}</td>
                <td>{emp.productivity_score}</td>
                <td>{emp.absences}</td>
                <td>{emp.status}</td>
                <td>{emp.age}</td>
                <td>{emp.email}</td>
                <td>
                  {emp.photo ? (
                    <img src={emp.photo} alt="photo" width={50} height={50} />
                  ) : (
                    <span>Pas de photo</span>
                  )}
                </td>
                <td>
                <button onClick={() => handleDelete(emp.id)}>❌ Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EmployeDashboard;
