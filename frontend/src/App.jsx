import React from 'react';
import './App.css';
import Hero from './components/Hero';
import Workflow from './components/Workflow';
import Demo from './components/Demo';
import Footer from './components/Footer';
import SpaceInvader from './components/SpaceInvader';
import TabBar from './components/TabBar';

function App() {
  return (
    <div className="App" style={{ paddingTop: '80px' }}>
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        opacity: 0.1,
        backgroundImage: `
          linear-gradient(0deg, transparent 24%, rgba(0, 255, 0, .3) 25%, rgba(0, 255, 0, .3) 26%, transparent 27%, transparent 74%, rgba(0, 255, 0, .3) 75%, rgba(0, 255, 0, .3) 76%, transparent 77%, transparent),
          linear-gradient(90deg, transparent 24%, rgba(0, 255, 0, .3) 25%, rgba(0, 255, 0, .3) 26%, transparent 27%, transparent 74%, rgba(0, 255, 0, .3) 75%, rgba(0, 255, 0, .3) 76%, transparent 77%, transparent)
        `,
        backgroundSize: '50px 50px'
      }}></div>

      {/* Pixel Stars */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -2,
        backgroundImage: 'radial-gradient(white 1px, transparent 1px), radial-gradient(white 1px, transparent 1px)',
        backgroundSize: '50px 50px',
        backgroundPosition: '0 0, 25px 25px',
        opacity: 0.1
      }}></div>

      <TabBar />
      <Hero />
      <Workflow />
      <Demo />
      <Footer />
      <SpaceInvader />
    </div>
  );
}export default App;
