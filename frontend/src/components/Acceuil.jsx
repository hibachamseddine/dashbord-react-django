import React, { useState, useEffect } from 'react';

const Acceuil = ({ setFiltres }) => {
  const [projet, setProjet] = useState('');
  const [equipe, setEquipe] = useState('');
  const [periode, setPeriode] = useState('');

  const handleFilterChange = () => {
    setFiltres({ projet, equipe, periode });
  };

  return (
    <div className="filters">
      <select onChange={(e) => setProjet(e.target.value)} value={projet}>
        <option value="">Choisir un projet</option>
        {/* List of projects */}
      </select>
      <select onChange={(e) => setEquipe(e.target.value)} value={equipe}>
        <option value="">Choisir une équipe</option>
        {/* List of teams */}
      </select>
      <input
        type="date"
        onChange={(e) => setPeriode(e.target.value)}
        value={periode}
      />
      <button onClick={handleFilterChange}>Appliquer</button>
    </div>
  );
};

export default Acceuil;
