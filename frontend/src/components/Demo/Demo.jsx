import React, { useRef, useEffect } from 'react';
import './Demo.css';

const Demo = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            videoRef.current.play().catch(error => {
              console.log("Autoplay prevented:", error);
            });
          } else {
            videoRef.current.pause();
          }
        });
      },
      { threshold: 0.5 }
    );

    if (videoRef.current) {
      observer.observe(videoRef.current);
    }

    return () => {
      if (videoRef.current) {
        observer.unobserve(videoRef.current);
      }
    };
  }, []);

  return (
    <section id="demo" className="container">
      <h2 className="section-title">MISSION REPLAY</h2>
      <div className="pixel-card demo-card">
        <div className="demo-video-container">
          <video
            ref={videoRef}
            muted
            loop
            playsInline
            width="100%"
            height="100%"
            className="demo-video"
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
