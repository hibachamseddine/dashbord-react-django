import React from "react";

const RhKPI = ({ kpi }) => {
  return (
    <div className="kpiBox">
      <h3 className="title">👥 Ressources Humaines</h3>
      <div className="gridContainer">
        <div className="valueCard">
          <div className="square">{kpi.total_employes}</div>
          <p className="label">Total employés</p>
        </div>
        <div className="valueCard">
          <div className="square">{kpi.employes_actifs}</div>
          <p className="label">Actifs</p>
        </div>
        <div className="valueCard">
          <div className="square">{kpi.employes_inactifs}</div>
          <p className="label">Inactifs</p>
        </div>
        <div className="valueCard">
          <div className="square">{kpi.employes_en_conge}</div>
          <p className="label">En congé</p>
        </div>
      </div>
      <p className="rate">📈 Taux de rétention : {kpi.taux_retention}%</p>
    </div>
  );
};

export default RhKPI;
