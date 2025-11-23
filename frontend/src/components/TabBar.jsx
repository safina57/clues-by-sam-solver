import React from 'react';
import { Github } from 'lucide-react';

const TabBar = () => {
  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      backgroundColor: 'var(--color-bg)',
      borderBottom: '4px solid var(--color-primary)',
      zIndex: 1000,
      padding: '10px 0',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <div className="container" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%',
        margin: 0
      }}>
        <div style={{ display: 'flex', gap: '20px' }}>
          <a href="#" style={{ color: 'var(--color-text)', fontSize: '1.2rem', textDecoration: 'none' }}>HOME</a>
          <a href="#workflow" style={{ color: 'var(--color-text)', fontSize: '1.2rem', textDecoration: 'none' }}>SYSTEM</a>
          <a href="#demo" style={{ color: 'var(--color-text)', fontSize: '1.2rem', textDecoration: 'none' }}>DEMO</a>
        </div>

        <a
          href="https://github.com/safina57/clues-by-sam-solver"
          target="_blank"
          rel="noopener noreferrer"
          className="pixel-btn"
          style={{
            padding: '5px 10px',
            fontSize: '10px',
            display: 'flex',
            alignItems: 'center',
            gap: '5px'
          }}
        >
          <Github size={14} />
          <span>SOURCE</span>
        </a>
      </div>
    </nav>
  );
};

export default TabBar;
