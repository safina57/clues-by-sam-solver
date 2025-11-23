import React from 'react';

const Demo = () => {
  return (
    <section id="demo" className="container">
      <h2 className="section-title">MISSION REPLAY</h2>
      <div className="pixel-card" style={{ padding: '10px' }}>
        <div style={{
          width: '100%',
          aspectRatio: '16/9',
          backgroundColor: '#000',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: '2px solid #333',
          overflow: 'hidden'
        }}>
          <video
            controls
            width="100%"
            height="100%"
            style={{ display: 'block' }}
          >
            <source src="./demo.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
    </section>
  );
};

export default Demo;
