import React, { useEffect, useState } from "react";
import axios from "axios";
import '../styles/Dashbord.css';
import EmployeKPI from "../KPI/EmployeKPI";  // Import the EmployeKPI component

const EmployeDashboard = () => {
  const [kpi, setKpi] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [error, setError] = useState(null);
  const updatePhoto = async (employeeId, file) => {
    const formData = new FormData();
    formData.append("photo", file);
  
    try {
      const response = await axios.put(
        `http://127.0.0.1:8000/api/employee/update/${employeeId}/`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      console.log("Photo mise à jour :", response.data);
    } catch (error) {
      console.error("Erreur lors de la mise à jour :", error);
    }
  };
  
  // Fetch KPI data and employee data
  useEffect(() => {
    const fetchKpiData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/kpi/"); // Adjust the API endpoint if needed
        setKpi(response.data);  // Ensure that the response contains KPI data
      } catch (err) {
        setError("Erreur de chargement des KPI");
      }
    };

    const fetchEmployeeData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/employees/"); // Endpoint to fetch employee data
        setEmployees(response.data);
      } catch (err) {
        setError("Erreur de chargement des employés");
      }
    };

    fetchKpiData();
    fetchEmployeeData();

    const intervalId = setInterval(() => {
      fetchKpiData();
      fetchEmployeeData();
    }, 10000); // Fetch data every 10 seconds

    return () => clearInterval(intervalId);
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!kpi || !employees.length) return <p>⚠️ Aucune donnée disponible.</p>;



  return (
    <div className="dashboardContainer">
      {/* Display KPI */}
      <div className="kpiContainer">
        <EmployeKPI kpi={kpi} />  {/* Pass the KPI data to the EmployeKPI component */}
      </div>

      {/* Display Employee Data in a Table */}
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
    <img src={`http://127.0.0.1:8000${emp.photo}`} alt="photo" width={50} height={50} />
  ) : (
    <span>Pas de photo</span>
  )}
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
