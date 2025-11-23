import React from 'react';
import './SpaceInvader.css';

const SpaceInvader = () => {
  return (
    <div className="space-invader-container">
      <div className="space-invader">
        <svg width="40" height="40" viewBox="0 0 11 8" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M2 0H8V1H9V2H11V5H9V8H8V6H7V8H4V6H3V8H2V5H0V2H2V1H3V0H2Z" fill="#00ff00"/>
          <rect x="3" y="2" width="1" height="1" fill="black"/>
          <rect x="7" y="2" width="1" height="1" fill="black"/>
        </svg>
      </div>
    </div>
  );
};

export default SpaceInvader;
