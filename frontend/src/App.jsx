import React from 'react';
import './App.css';
import Hero from './components/Hero/Hero';
import Workflow from './components/Workflow/Workflow';
import Demo from './components/Demo/Demo';
import Footer from './components/Footer/Footer';
import SpaceInvader from './components/SpaceInvader/SpaceInvader';
import TabBar from './components/TabBar/TabBar';
import PixelBlast from './components/PixelBlast/PixelBlast';

function App() {
  return (
    <div className="App app-container">
      <div className="background-container">
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
          className="pixel-blast-bg"
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
