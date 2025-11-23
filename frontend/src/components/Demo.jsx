import React from 'react';

const Demo = () => {
  return (
    <section id="demo" className="container">
      <h2 className="section-title">MISSION REPLAY</h2>
      <div className="pixel-card" style={{ padding: '10px' }}>
        <div style={{
          width: '100%',
          aspectRatio: '16/9',
          backgroundColor: '#111',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: '2px solid #333'
        }}>
          {/* Replace this with your actual video tag later */}
          <div style={{ textAlign: 'center' }}>
            <p style={{ color: '#666', marginBottom: '10px' }}>[ VIDEO SIGNAL LOST ]</p>
            <p style={{ color: 'var(--color-primary)' }}>INSERT TAPE TO PLAY DEMO</p>
            {/* Example video tag:
            <video controls width="100%" height="100%">
              <source src="/assets/demo.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            */}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Demo;
