import React from 'react';
import './App.css';
import Hero from './components/Hero';
import Workflow from './components/Workflow';
import Demo from './components/Demo';
import Footer from './components/Footer';
import SpaceInvader from './components/SpaceInvader';
import TabBar from './components/TabBar';
import PixelBlast from './components/PixelBlast';

function App() {
  return (
    <div className="App" style={{ paddingTop: '80px', position: 'relative', minHeight: '100vh' }}>
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        backgroundColor: '#000000'
      }}>
        <PixelBlast
          color="#00ff00"
          pixelSize={4}
          variant="square"
          patternScale={4}
          patternDensity={1.5}
          speed={0.2}
          transparent={true}
          enableRipples={true}
          rippleSpeed={0.5}
          style={{ opacity: 0.3 }}
        />
      </div>

      <TabBar />
      <Hero />
      <Workflow />
      <Demo />
      <Footer />
      <SpaceInvader />
    </div>
  );
}

export default App;
