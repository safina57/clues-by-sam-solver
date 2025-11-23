import React from 'react';
import { Github } from 'lucide-react';
import './TabBar.css';

const TabBar = () => {
  return (
    <nav className="tab-bar">
      <div className="container tab-bar-container">
        <div className="tab-links">
          <a href="#" className="tab-link">HOME</a>
          <a href="#workflow" className="tab-link">SYSTEM</a>
          <a href="#demo" className="tab-link">DEMO</a>
        </div>

        <a
          href="https://github.com/safina57/clues-by-sam-solver"
          target="_blank"
          rel="noopener noreferrer"
          className="pixel-btn source-btn"
        >
          <Github size={14} />
          <span>SOURCE</span>
        </a>
      </div>
    </nav>
  );
};

export default TabBar;
