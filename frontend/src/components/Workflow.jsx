import React from 'react';
import { Database, Cpu, Code, Terminal } from 'lucide-react';

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

const Workflow = () => {
  return (
    <section id="workflow" className="container">
      <h2 className="section-title">SYSTEM ARCHITECTURE</h2>
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
