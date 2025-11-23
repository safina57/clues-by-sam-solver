import React from 'react';
import { Database, Cpu, Code, Terminal, ArrowRight, ArrowDown } from 'lucide-react';
import './Workflow.css';

const WorkflowStep = ({ icon: Icon, title, description }) => (
  <div className="pixel-card workflow-step-card">
    <div className="workflow-step-header">
      <div className="workflow-icon-container">
        <Icon size={24} color="black" />
      </div>
      <h3 className="workflow-step-title">{title}</h3>
    </div>
    <p className="workflow-step-description">{description}</p>
  </div>
);

const FlowNode = ({ label, icon: Icon, color = 'var(--color-primary)' }) => (
  <div className="flow-node" style={{
    border: `2px solid ${color}`,
    boxShadow: `4px 4px 0 ${color}`
  }}>
    {Icon && <div className="flow-node-icon"><Icon size={20} color={color} /></div>}
    <span className="flow-node-label" style={{ color: color }}>{label}</span>
  </div>
);

const Arrow = ({ vertical = false }) => (
  <div className="arrow-container">
    {vertical ? <ArrowDown size={24} color="var(--color-text)" /> : <ArrowRight size={24} color="var(--color-text)" className="arrow-right" />}
  </div>
);

const WorkflowDiagram = () => {
  return (
    <div className="pixel-card workflow-diagram-card">
      <h3 className="workflow-diagram-title">LOGIC PIPELINE</h3>

      <div className="workflow-diagram-content">
        {/* Main Flow */}
        <div className="workflow-main-flow">
          <FlowNode label="GAME SITE" icon={Terminal} />
          <div className="workflow-arrow-wrapper">
            <span className="workflow-arrow-label">EXTRACT HINTS</span>
            <Arrow />
          </div>

          <FlowNode label="TRANSLATOR" icon={Code} />
          <div className="workflow-arrow-wrapper">
            <span className="workflow-arrow-label">CONVERT TO FOL</span>
            <Arrow />
          </div>

          <div className="workflow-solver-group">
            <FlowNode label="Z3 SOLVER" icon={Cpu} />
            {/* KB Connection */}
            <div className="kb-connection"></div>
            <FlowNode label="KNOWLEDGE BASE" icon={Database} />
          </div>

          <div className="workflow-arrow-wrapper">
            <span className="workflow-arrow-label">INFERENCE</span>
            <Arrow />
          </div>

          <FlowNode label="STATES" icon={Database} color="var(--color-criminal)" />
        </div>
      </div>

      <div className="workflow-legend">
        <span className="legend-primary">■</span> DATA FLOW &nbsp;&nbsp;
        <span className="legend-criminal">■</span> FINAL OUTPUT
      </div>
    </div>
  );
};const Workflow = () => {
  return (
    <section id="workflow" className="container">
      <h2 className="section-title">SYSTEM ARCHITECTURE</h2>

      <WorkflowDiagram />

      <div className="workflow-grid">
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
