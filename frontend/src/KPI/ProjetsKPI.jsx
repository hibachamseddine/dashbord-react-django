import React from "react";

const ProjetsKPI = ({ kpi }) => {
  return (
    <div className="kpiBox">
      <h3 className="title">📌 Projets</h3>
      <div className="gridContainer">
        <div className="valueCard">
          <div className="square">{kpi.total_projets}</div>
          <p className="label">Total</p>
        </div>
        <div className="valueCard">
          <div className="square">{kpi.projets_termines}</div>
          <p className="label">Terminés</p>
        </div>
        <div className="valueCard">
          <div className="square">{kpi.projets_en_cours}</div>
          <p className="label">En cours</p>
        </div>
      </div>
      <p className="rate">📈 Taux de complétion : {kpi.taux_completion}%</p>
    </div>
  );
};

export default ProjetsKPI;
