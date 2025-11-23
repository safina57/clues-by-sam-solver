from typing import List, Tuple
from z3 import If, Sum, And, Or, Not, Implies, Exists, ForAll, unsat
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
            constraint_code = constraint_code.replace("\\n", "\n").replace("\\t", "\t")
            constraint_code = constraint_code.replace("\\", " ")

            # We expose 'kb' to the eval context
            context = {
                "kb": self.kb,
                "If": If,
                "Sum": Sum,
                "And": And,
                "Or": Or,
                "Not": Not,
                "Implies": Implies,
                "Exists": Exists,
                "ForAll": ForAll,
            }
            rule = eval(constraint_code, context)
            self.kb.solver.add(rule)
            self.constraints.append(constraint_code)
        except Exception as e:
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
            self.kb.solver.add(var)
            if self.kb.solver.check() == unsat:
                proven_facts.append((name, Status.INNOCENT))
            self.kb.solver.pop()

            # Assume INNOCENT (False)
            self.kb.solver.push()
            self.kb.solver.add(Not(var))
            if self.kb.solver.check() == unsat:
                proven_facts.append((name, Status.CRIMINAL))
            self.kb.solver.pop()

        return proven_facts

    def add_fact(self, name: str, status: Status):
        """Update the solver with a newly discovered fact."""
        var = self.kb.vars[name]
        if status == Status.CRIMINAL:
            self.kb.solver.add(var)
        elif status == Status.INNOCENT:
            self.kb.solver.add(Not(var))

    def log_state(self, iteration: int, filepath: str = "solver_log.txt"):
        """Log the current state of the KB to a file."""
        with open(filepath, "a") as f:
            f.write(f"\n{'=' * 20} Iteration {iteration} {'=' * 20}\n")

            f.write("\n--- Known Facts ---\n")
            for p in self.kb.people:
                if p.status != Status.UNKNOWN:
                    f.write(f"{p.name}: {p.status.value}\n")

            f.write("\n--- Added Constraints (Code) ---\n")
            for i, c in enumerate(self.constraints):
                f.write(f"{i + 1}. {c}\n")

            f.write("\n--- Z3 Solver State ---\n")
            f.write(str(self.kb.solver))
            f.write(f"\n{'=' * 50}\n")
