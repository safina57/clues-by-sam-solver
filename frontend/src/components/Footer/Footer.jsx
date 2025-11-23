import React from 'react';
import { Github, Linkedin, ExternalLink } from 'lucide-react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container footer-container">
        <h2 className="footer-title">CONNECT TO SOURCE</h2>
        <div className="footer-links">
          <a href="https://github.com/safina57/clues-by-sam-solver" target="_blank" rel="noopener noreferrer" className="pixel-btn">
            <div className="footer-link-content">
              <Github size={18} />
              <span>GITHUB REPO</span>
            </div>
          </a>
          <a href="https://www.linkedin.com/in/mohamed-amin-haouas" target="_blank" rel="noopener noreferrer" className="pixel-btn">
            <div className="footer-link-content">
              <Linkedin size={18} />
              <span>LINKEDIN</span>
            </div>
          </a>
        </div>
        <p className="footer-copyright">
          © 2025 CLUES BY SAM SOLVER. ALL RIGHTS RESERVED.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
