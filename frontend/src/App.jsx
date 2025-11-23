import React from 'react';
import './App.css';
import Hero from './components/Hero';
import Workflow from './components/Workflow';
import Demo from './components/Demo';
import Footer from './components/Footer';
import SpaceInvader from './components/SpaceInvader';

function App() {
  return (
    <div className="App">
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        opacity: 0.1,
        backgroundImage: 'linear-gradient(0deg, transparent 24%, rgba(0, 255, 0, .3) 25%, rgba(0, 255, 0, .3) 26%, transparent 27%, transparent 74%, rgba(0, 255, 0, .3) 75%, rgba(0, 255, 0, .3) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(0, 255, 0, .3) 25%, rgba(0, 255, 0, .3) 26%, transparent 27%, transparent 74%, rgba(0, 255, 0, .3) 75%, rgba(0, 255, 0, .3) 76%, transparent 77%, transparent)',
        backgroundSize: '50px 50px'
      }}></div>

      <Hero />
      <Workflow />
      <Demo />
      <Footer />
      <SpaceInvader />
    </div>
  );
}

export default App;
