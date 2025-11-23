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
    {vertical ? <ArrowDown size={24} color="var(--color-text)" /> : <ArrowRight size={24} color="var(--color-text)" />}
  </div>
);

const WorkflowDiagram = () => {
  return (
    <div className="pixel-card" style={{ padding: '40px', marginBottom: '60px', overflowX: 'auto' }}>
      <h3 style={{ textAlign: 'center', marginBottom: '30px', color: 'var(--color-primary)' }}>LOGIC PIPELINE</h3>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
        {/* Main Flow */}
        <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', justifyContent: 'center' }}>
          <FlowNode label="GAME SITE" icon={Terminal} />
          <div style={{ textAlign: 'center', margin: '0 10px' }}>
            <span style={{ fontSize: '0.6rem', color: '#666' }}>EXTRACT HINTS</span>
            <Arrow />
          </div>

          <FlowNode label="TRANSLATOR" icon={Code} />
          <div style={{ textAlign: 'center', margin: '0 10px' }}>
            <span style={{ fontSize: '0.6rem', color: '#666' }}>FIRST ORDER LOGIC</span>
            <Arrow />
          </div>

          <FlowNode label="Z3 SOLVER" icon={Cpu} />
          <div style={{ textAlign: 'center', margin: '0 10px' }}>
            <span style={{ fontSize: '0.6rem', color: '#666' }}>INFERENCE</span>
            <Arrow />
          </div>

          <FlowNode label="STATES" icon={Database} color="var(--color-criminal)" />
        </div>

        {/* KB Connection */}
        <div style={{ display: 'flex', alignItems: 'center', marginTop: '-10px' }}>
           <div style={{ width: '2px', height: '30px', background: 'var(--color-primary)', marginRight: '160px' }}></div>
        </div>
        <div style={{ marginRight: '160px' }}>
           <FlowNode label="KNOWLEDGE BASE" icon={Database} />
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
          icon={Database}
          title="KNOWLEDGE BASE"
          description="The game state is modeled as a collection of facts and constraints. We define the entities (colors, items, positions) and their relationships."
        />
        <WorkflowStep
          icon={Code}
          title="FIRST ORDER LOGIC"
          description="Clues are translated into First Order Logic formulas. For example, 'The red item is left of the blue item' becomes a mathematical constraint on positions."
        />
        <WorkflowStep
          icon={Cpu}
          title="Z3 SOLVER"
          description="Microsoft's Z3 Theorem Prover is the core engine. It takes the logical constraints and efficiently searches for a satisfying model that fits all clues."
        />
        <WorkflowStep
          icon={Terminal}
          title="TRANSLATOR"
          description="A custom translator parses the natural language clues from the game and converts them into the Z3-compatible constraints automatically."
        />
      </div>
    </section>
  );
};

export default Workflow;
