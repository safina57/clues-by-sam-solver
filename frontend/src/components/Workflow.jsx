import React from 'react';
import { Database, Cpu, Code, Terminal, ArrowRight, ArrowDown } from 'lucide-react';

const WorkflowStep = ({ icon: Icon, title, description }) => (
  <div className="pixel-card" style={{ height: '100%' }}>
    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
      <div style={{
        background: 'var(--color-primary)',
        padding: '10px',
        marginRight: '15px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <Icon size={24} color="black" />
      </div>
      <h3 style={{ margin: 0, fontSize: '1.2rem' }}>{title}</h3>
    </div>
    <p style={{ lineHeight: '1.5' }}>{description}</p>
  </div>
);

const FlowNode = ({ label, icon: Icon, color = 'var(--color-primary)' }) => (
  <div style={{
    border: `2px solid ${color}`,
    padding: '10px',
    textAlign: 'center',
    width: '140px',
    background: '#000',
    position: 'relative',
    boxShadow: `4px 4px 0 ${color}`
  }}>
    {Icon && <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5px' }}><Icon size={20} color={color} /></div>}
    <span style={{ color: color, fontSize: '0.8rem' }}>{label}</span>
  </div>
);

const Arrow = ({ vertical = false }) => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '10px'
  }}>
    {vertical ? <ArrowDown size={24} color="var(--color-text)" /> : <ArrowRight size={24} color="var(--color-text)" style={{ transform: 'scaleX(2)' }} />}
  </div>
);

const WorkflowDiagram = () => {
  return (
    <div className="pixel-card" style={{
      padding: '40px',
      marginBottom: '60px',
      overflowX: 'auto',
      scrollbarWidth: 'none', /* Firefox */
      msOverflowStyle: 'none' /* IE/Edge */
    }}>
      <style>
        {`
          .pixel-card::-webkit-scrollbar {
            display: none;
          }
        `}
      </style>
      <h3 style={{ textAlign: 'center', marginBottom: '30px', color: 'var(--color-primary)' }}>LOGIC PIPELINE</h3>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px', minWidth: '800px' }}>
        {/* Main Flow */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <FlowNode label="GAME SITE" icon={Terminal} />
          <div style={{ textAlign: 'center', margin: '0 10px' }}>
            <span style={{ fontSize: '0.6rem', color: '#666' }}>EXTRACT HINTS</span>
            <Arrow />
          </div>

          <FlowNode label="TRANSLATOR" icon={Code} />
          <div style={{ textAlign: 'center', margin: '0 10px' }}>
            <span style={{ fontSize: '0.6rem', color: '#666' }}>CONVERT TO FOL</span>
            <Arrow />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative' }}>
            <FlowNode label="Z3 SOLVER" icon={Cpu} />
            {/* KB Connection */}
            <div style={{ width: '2px', height: '20px', background: 'var(--color-primary)' }}></div>
            <FlowNode label="KNOWLEDGE BASE" icon={Database} />
          </div>

          <div style={{ textAlign: 'center', margin: '0 10px' }}>
            <span style={{ fontSize: '0.6rem', color: '#666' }}>INFERENCE</span>
            <Arrow />
          </div>

          <FlowNode label="STATES" icon={Database} color="var(--color-criminal)" />
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '40px', fontSize: '0.8rem', color: '#666' }}>
        <span style={{ color: 'var(--color-primary)' }}>■</span> DATA FLOW &nbsp;&nbsp;
        <span style={{ color: 'var(--color-criminal)' }}>■</span> FINAL OUTPUT
      </div>
    </div>
  );
};const Workflow = () => {
  return (
    <section id="workflow" className="container">
      <h2 className="section-title">SYSTEM ARCHITECTURE</h2>

      <WorkflowDiagram />

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '20px'
      }}>
        <WorkflowStep
          icon={Terminal}
          title="GAME REPRESENTATION"
          description="The game is represented as a grid of people with different professions. Relationships are defined by spatial constraints like neighbors, edges, or relative positions."
        />
        <WorkflowStep
          icon={Code}
          title="AI TRANSLATOR"
          description="An AI-powered translator converts natural language hints into First Order Logic (FOL) formulas that serve as input for the inference engine."
        />
        <WorkflowStep
          icon={Cpu}
          title="Z3 SOLVER ENGINE"
          description="The core engine uses the Z3 Theorem Prover with a knowledge base that augments with each iteration to prove satisfiability and deduce the final state."
        />
      </div>
    </section>
  );
};

export default Workflow;
