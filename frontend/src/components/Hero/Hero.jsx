import React from 'react';
import './Hero.css';

const Hero = () => {
  return (
    <section className="container hero-section">
      <h1 className="hero-title">
        CLUES BY SAM SOLVER
      </h1>
      <div className="pixel-card hero-card">
        <h2 className="hero-subtitle">MISSION BRIEFING</h2>
        <p className="hero-text">
          "Clues by Sam" is a high-stakes logic puzzle where your goal is to identify the <span className="text-innocent">INNOCENTS</span> and catch the <span className="text-criminal">CRIMINALS</span>.
          <br/><br/>
          You are given a set of cryptic hints about who is sitting where and what they are doing.
          This project automates the detective work using <strong>First Order Logic</strong> and the <strong>Z3 Theorem Prover</strong> to deduce the status of every person on the grid instantly.
        </p>
        <div className="hero-actions">
          <a href="#demo" className="pixel-btn red hero-btn hero-btn-demo">WATCH DEMO</a>
          <a href="#workflow" className="pixel-btn hero-btn">READ LOGS</a>
        </div>
      </div>
    </section>
  );
};

export default Hero;
