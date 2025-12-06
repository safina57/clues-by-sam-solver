from typing import List, Dict
from z3 import Solver, Bool, BoolRef, If, Sum, And, Not, Implies, ArithRef
from src.models.game_state import Person, Status


class KnowledgeBase:
    def __init__(self, people: List[Person]):
        self.people = people
        self.solver = Solver()
        self.vars: Dict[str, BoolRef] = {}
        self.person_map: Dict[str, Person] = {p.name: p for p in people}

        # Initialize Z3 variables
        for p in people:
            self.vars[p.name] = Bool(f"{p.name}_is_criminal")

            # Add known status constraints
            if p.status == Status.CRIMINAL:
                self.solver.add(self.vars[p.name])
            elif p.status == Status.INNOCENT:
                self.solver.add(Not(self.vars[p.name]))

    @property
    def people_names(self) -> List[str]:
        return [p.name for p in self.people]

    def get_var(self, name: str) -> BoolRef:
        return self.vars[name]

    # --- Predicates exposed to LLM ---

    def is_criminal(self, name: str) -> BoolRef:
        return self.vars[name]

    def is_innocent(self, name: str) -> BoolRef:
        return Not(self.vars[name])

    def is_neighboring(self, name1: str, name2: str) -> bool:
        """Check if two people are neighbors."""
        return name2 in self.get_neighbors(name1)

    def get_neighbors(self, name: str) -> List[str]:
        """Return names of neighbors."""
        return self.person_map[name].neighbors

    def get_orthogonal_neighbors(self, name: str) -> List[str]:
        """Return names of orthogonal neighbors (up, down, left, right)."""
        p = self.person_map[name]
        neighbors = []
        for other in self.people:
            if other.name == name:
                continue

            row_diff = abs(p.row - other.row)
            col_p = ord(p.col) - ord("A")
            col_o = ord(other.col) - ord("A")
            col_diff = abs(col_p - col_o)

            if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
                neighbors.append(other.name)
        return neighbors

    def get_common_neighbors(self, name1: str, name2: str) -> List[str]:
        """Return neighbors shared by both name1 and name2."""
        n1 = set(self.get_neighbors(name1))
        n2 = set(self.get_neighbors(name2))
        return list(n1.intersection(n2))

    def is_in_col(self, name: str, col_char: str) -> bool:
        """Check if person is in a specific column."""
        return self.person_map[name].col == col_char

    def is_in_row(self, name: str, row_num: int) -> bool:
        """Check if person is in a specific row."""
        return self.person_map[name].row == row_num

    def get_row(self, row_num: int) -> List[str]:
        return [p.name for p in self.people if p.row == row_num]

    def get_col(self, col_char: str) -> List[str]:
        return [p.name for p in self.people if p.col == col_char]

    def get_profession(self, prof: str) -> List[str]:
        return [p.name for p in self.people if p.profession == prof]

    def get_corners(self) -> List[str]:
        return [p.name for p in self.people if p.id in ["A1", "D1", "A5", "D5"]]

    def get_edges(self) -> List[str]:
        return [p.name for p in self.people if p.row in [1, 5] or p.col in ["A", "D"]]

    def get_between(self, name1: str, name2: str) -> List[str]:
        """Return names of people strictly between name1 and name2 (same row or col)."""
        p1 = self.person_map[name1]
        p2 = self.person_map[name2]
        between = []

        if p1.row == p2.row:
            # Same row
            c1 = ord(p1.col)
            c2 = ord(p2.col)
            start, end = min(c1, c2), max(c1, c2)
            for p in self.people:
                if p.row == p1.row and start < ord(p.col) < end:
                    between.append(p.name)
        elif p1.col == p2.col:
            # Same col
            start, end = min(p1.row, p2.row), max(p1.row, p2.row)
            for p in self.people:
                if p.col == p1.col and start < p.row < end:
                    between.append(p.name)

        return between

    def get_left_of(self, name: str) -> List[str]:
        """Return all people to the left of 'name' in the same row."""
        return [p.name for p in self.people if self.is_left_of(p.name, name)]

    def get_right_of(self, name: str) -> List[str]:
        """Return all people to the right of 'name' in the same row."""
        return [p.name for p in self.people if self.is_right_of(p.name, name)]

    def get_above(self, name: str) -> List[str]:
        """Return all people above 'name' in the same column."""
        return [p.name for p in self.people if self.is_above(p.name, name)]

    def get_below(self, name: str) -> List[str]:
        """Return all people below 'name' in the same column."""
        return [p.name for p in self.people if self.is_below(p.name, name)]

    def get_directly_left(self, name: str) -> str | None:
        """Return the person directly to the left, or None if no one."""
        left = [p.name for p in self.people if self.is_directly_left(p.name, name)]
        return left[0] if left else None

    def get_directly_right(self, name: str) -> str | None:
        """Return the person directly to the right, or None if no one."""
        right = [p.name for p in self.people if self.is_directly_right(p.name, name)]
        return right[0] if right else None

    def get_directly_above(self, name: str) -> str | None:
        """Return the person directly above, or None if no one."""
        above = [p.name for p in self.people if self.is_directly_above(p.name, name)]
        return above[0] if above else None

    def get_directly_below(self, name: str) -> str | None:
        """Return the person directly below, or None if no one."""
        below = [p.name for p in self.people if self.is_directly_below(p.name, name)]
        return below[0] if below else None

    # --- Logic Helpers ---

    def count_criminals(self, names: List[str]) -> ArithRef:
        return Sum([If(self.is_criminal(n), 1, 0) for n in names])

    def count_innocents(self, names: List[str]) -> ArithRef:
        return Sum([If(self.is_innocent(n), 1, 0) for n in names])

    def count_profession(self, profession_or_names) -> int:
        """Count people by profession name or count a list of names."""
        if isinstance(profession_or_names, str):
            # Count by profession name
            return len(self.get_profession(profession_or_names))
        elif isinstance(profession_or_names, list):
            # Count list of names
            return len(profession_or_names)
        else:
            raise ValueError(f"Invalid argument type: {type(profession_or_names)}")

    def is_above(self, name1: str, name2: str) -> bool:
        """Is name1 above name2"""
        p1 = self.person_map[name1]
        p2 = self.person_map[name2]
        return p1.col == p2.col and p1.row < p2.row

    def is_below(self, name1: str, name2: str) -> bool:
        return self.is_above(name2, name1)

    def is_left_of(self, name1: str, name2: str) -> bool:
        """Is name1 left of name2"""
        p1 = self.person_map[name1]
        p2 = self.person_map[name2]
        return p1.row == p2.row and p1.col < p2.col

    def is_right_of(self, name1: str, name2: str) -> bool:
        return self.is_left_of(name2, name1)

    def is_directly_above(self, name1: str, name2: str) -> bool:
        p1 = self.person_map[name1]
        p2 = self.person_map[name2]
        return p1.col == p2.col and p1.row == p2.row - 1

    def is_directly_below(self, name1: str, name2: str) -> bool:
        return self.is_directly_above(name2, name1)

    def is_directly_left(self, name1: str, name2: str) -> bool:
        p1 = self.person_map[name1]
        p2 = self.person_map[name2]
        return p1.row == p2.row and ord(p1.col) == ord(p2.col) - 1

    def is_directly_right(self, name1: str, name2: str) -> bool:
        return self.is_directly_left(name2, name1)

    def row_connected(self, row_num: int, status_is_criminal: bool) -> BoolRef:
        """
        Returns a Z3 constraint enforcing that all people with 'status' in 'row_num' are connected.
        If p1 and p2 are BOTH the target status
        THEN all 'between' must also be the target status.
        """
        row_people = sorted(self.get_row(row_num), key=lambda n: self.person_map[n].col)
        constraints = []

        for i in range(len(row_people)):
            for j in range(i + 2, len(row_people)):
                p1 = row_people[i]
                p2 = row_people[j]
                between = row_people[i + 1 : j]

                if status_is_criminal:
                    cond = And(self.is_criminal(p1), self.is_criminal(p2))
                    conseq = And([self.is_criminal(b) for b in between])
                    constraints.append(Implies(cond, conseq))
                else:
                    # Innocent version
                    cond = And(self.is_innocent(p1), self.is_innocent(p2))
                    conseq = And([self.is_innocent(b) for b in between])
                    constraints.append(Implies(cond, conseq))

        return And(constraints)
