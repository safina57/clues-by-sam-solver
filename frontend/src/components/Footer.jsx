import React from 'react';
import { Github, Linkedin, ExternalLink } from 'lucide-react';

const Footer = () => {
  return (
    <footer style={{
      borderTop: '4px solid var(--color-primary)',
      padding: '40px 20px',
      marginTop: '60px',
      backgroundColor: '#111'
    }}>
      <div className="container" style={{ textAlign: 'center' }}>
        <h2 style={{ marginBottom: '30px' }}>CONNECT TO SOURCE</h2>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '30px', flexWrap: 'wrap' }}>
          <a href="https://github.com/safina57/clues-by-sam-solver" target="_blank" rel="noopener noreferrer" className="pixel-btn">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Github size={18} />
              <span>GITHUB REPO</span>
            </div>
          </a>
          <a href="https://www.linkedin.com/in/mohamed-amin-haouas" target="_blank" rel="noopener noreferrer" className="pixel-btn">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Linkedin size={18} />
              <span>LINKEDIN</span>
            </div>
          </a>
        </div>
        <p style={{ marginTop: '40px', fontSize: '0.8rem', color: '#666' }}>
          © 2025 CLUES BY SAM SOLVER. ALL RIGHTS RESERVED.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
