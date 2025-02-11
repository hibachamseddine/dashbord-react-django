import React from "react";
import { Link } from "react-router-dom";
import '../styles/Navbar.css';  // For styling the navbar (optional)

const Navbar = () => {
  return (
    <nav className="navbar">
    <ul>
      <li>
        <Link to="/projets">📌 Projets</Link>
      </li>
      <li>
        <Link to="/rh">👥 Ressources Humaines</Link>
      </li>
      <li>
        <Link to="/employes">👥 Employés</Link>
      </li>
    </ul>
  </nav>
  );
};

export default Navbar;
