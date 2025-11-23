import React from 'react';

const Hero = () => {
  return (
    <section className="container" style={{ textAlign: 'center', padding: '60px 20px' }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '20px', color: 'var(--color-primary)', textShadow: '4px 4px 0 #004400' }}>
        CLUES BY SAM SOLVER
      </h1>
      <div className="pixel-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '20px' }}>MISSION BRIEFING</h2>
        <p style={{ fontSize: '1.2rem', lineHeight: '1.6' }}>
          "Clues by Sam" is a logic puzzle game where you must deduce the correct arrangement of items based on a set of clues.
          <br/><br/>
          This project is an automated solver that uses <strong>First Order Logic</strong> and the <strong>Z3 Theorem Prover</strong> to crack the code instantly.
        </p>
        <div style={{ marginTop: '30px' }}>
          <a href="#demo" className="pixel-btn" style={{ fontSize: '1.2rem', marginRight: '20px' }}>WATCH DEMO</a>
          <a href="#workflow" className="pixel-btn" style={{ fontSize: '1.2rem', backgroundColor: 'transparent', border: '2px solid var(--color-primary)', color: 'var(--color-primary)' }}>READ LOGS</a>
        </div>
      </div>
    </section>
  );
};

export default Hero;
