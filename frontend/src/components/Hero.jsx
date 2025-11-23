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
          "Clues by Sam" is a high-stakes logic puzzle where your goal is to identify the <span style={{color: 'var(--color-text)'}}>INNOCENTS</span> and catch the <span style={{color: 'var(--color-criminal)'}}>CRIMINALS</span>.
          <br/><br/>
          You are given a set of cryptic hints about who is sitting where and what they are doing.
          This project automates the detective work using <strong>First Order Logic</strong> and the <strong>Z3 Theorem Prover</strong> to deduce the status of every person on the grid instantly.
        </p>
        <div style={{ marginTop: '30px' }}>
          <a href="#demo" className="pixel-btn red" style={{ fontSize: '1.2rem', marginRight: '20px', textDecoration: 'none' }}>WATCH DEMO</a>
          <a href="#workflow" className="pixel-btn" style={{ fontSize: '1.2rem', textDecoration: 'none' }}>READ LOGS</a>
        </div>
      </div>
    </section>
  );
};

export default Hero;
