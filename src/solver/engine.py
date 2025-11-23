from typing import List, Tuple
from z3 import *
from src.models.game_state import Person, Status
from src.solver.knowledge_base import KnowledgeBase

class GameSolver:
    def __init__(self, people: List[Person]):
        self.kb = KnowledgeBase(people)
        self.constraints = []

    def add_constraint(self, constraint_code: str):
        """
        Evaluate and add a constraint string to the solver.
        """
        try:
            constraint_code = constraint_code.strip()
            
            # We expose 'kb' to the eval context
            context = {
                'kb': self.kb,
                'If': If,
                'Sum': Sum,
                'And': And,
                'Or': Or,
                'Not': Not,
                'Implies': Implies,
                'Exists': Exists,
                'ForAll': ForAll
            }
            rule = eval(constraint_code, context)
            self.kb.solver.add(rule)
            self.constraints.append(constraint_code)
            print(f"Added constraint: {constraint_code}")
        except Exception as e:
            print(f"Failed to add constraint: {e}")
            raise e

    def solve(self) -> List[Tuple[str, Status]]:
        """
        Run deduction to find proven statuses.
        Returns a list of (Name, NewStatus).
        """
        proven_facts = []
        
        # First, check if the current state is consistent
        if self.kb.solver.check() == unsat:
            print("CRITICAL: Knowledge Base is inconsistent!")
            return []

        for name, var in self.kb.vars.items():
            # The KB initializes with knowns, so we only need to check unknowns.
            person = self.kb.person_map[name]
            if person.status != Status.UNKNOWN:
                continue

            # Assume CRIMINAL (True)
            self.kb.solver.push()
            self.kb.solver.add(var == True)
            if self.kb.solver.check() == unsat:
                proven_facts.append((name, Status.INNOCENT))
            self.kb.solver.pop()

            # Assume INNOCENT (False)
            self.kb.solver.push()
            self.kb.solver.add(var == False)
            if self.kb.solver.check() == unsat:
                proven_facts.append((name, Status.CRIMINAL))
            self.kb.solver.pop()
            
        return proven_facts

    def add_fact(self, name: str, status: Status):
        """Update the solver with a newly discovered fact."""
        var = self.kb.vars[name]
        if status == Status.CRIMINAL:
            self.kb.solver.add(var == True)
        elif status == Status.INNOCENT:
            self.kb.solver.add(var == False)

