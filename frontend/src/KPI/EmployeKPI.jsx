import React from 'react';

const EmployeKPI = ({ kpi }) => {
  return (
    <div className="kpiBox">
      <h3 className="title">👥 Employés</h3>
      <div className="gridContainer">
        <div className="valueCard">
          <div className="square">{kpi.taux_absentéisme}</div>
          <p className="label">Absentéisme</p>
        </div>
        <div className="valueCard">
          <div className="square">{kpi.avgProductivityScore}</div>
          <p className="label">Productivité moyenne</p>
        </div>
      </div>
     
    </div>
  );
}

export default EmployeKPI;
