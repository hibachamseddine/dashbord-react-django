import { useState, useEffect } from "react";

const Dashboard = () => {
    const [employees, setEmployees] = useState([]); // 🔹 Initialiser avec un tableau vide

    useEffect(() => {
        fetch("http://localhost:8000/api/employees/") // 🔹 Vérifiez bien l'URL !
            .then((response) => response.json())
            .then((data) => {
                console.log("Data received:", data); // 🔹 Vérifiez ce qui est reçu
                setEmployees(data || []);
            })
            .catch((error) => console.error("Error fetching employees:", error));
    }, []);

    return (
        <div>
            
                <ul>
                    {employees.map((employee) => ( // 🔹 Utiliser le bon nom de variable
                       <li key={`${employee.employee_id}-${employee.name}`}>{employee.name} - {employee.role}</li>

                    ))}
                </ul>
            
        </div>
    );
};

export default Dashboard;
