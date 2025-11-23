import pytest
from z3 import *
from src.models.game_state import Person, Status
from src.solver.knowledge_base import KnowledgeBase

def calculate_neighbors(people):
    for p in people:
        p.neighbors = []
        for other in people:
            if p.name == other.name:
                continue
            
            row_diff = abs(p.row - other.row)
            col_p = ord(p.col) - ord('A')
            col_o = ord(other.col) - ord('A')
            col_diff = abs(col_p - col_o)
            
            if row_diff <= 1 and col_diff <= 1:
                p.neighbors.append(other.name)

def test_knowledge_base_logic():
    # Setup a mini grid
    people = [
        Person(id="A1", name="Anna", profession="painter", row=1, col="A"),
        Person(id="B1", name="Betty", profession="teacher", row=1, col="B"),
        Person(id="A2", name="Carol", profession="guard", row=2, col="A"),
    ]
    calculate_neighbors(people)
    
    kb = KnowledgeBase(people)
    
    # Test 1: Neighbors
    # Anna (A1) should be neighbor to Betty (B1) and Carol (A2) (and B2 if it existed)
    neighbors = kb.get_neighbors("Anna")
    assert "Betty" in neighbors
    assert "Carol" in neighbors
    assert "Anna" not in neighbors
    
    # Test 2: Z3 Constraint
    # "Anna is innocent"
    kb.solver.add(kb.is_innocent("Anna"))
    assert kb.solver.check() == sat
    
    # "Betty is criminal"
    kb.solver.add(kb.is_criminal("Betty"))
    assert kb.solver.check() == sat
    
    # "Carol is same as Anna" (Innocent)
    kb.solver.add(kb.is_criminal("Carol") == kb.is_criminal("Anna"))
    
    # Check model
    if kb.solver.check() == sat:
        m = kb.solver.model()
        # Use is_true/is_false for robust checking
        assert is_false(m.evaluate(kb.vars["Anna"]))
        assert is_true(m.evaluate(kb.vars["Betty"]))
        assert is_false(m.evaluate(kb.vars["Carol"]))

def test_complex_constraint():
    # "Exactly 1 neighbor of Anna is criminal"
    people = [
        Person(id="A1", name="Anna", profession="painter", row=1, col="A"),
        Person(id="B1", name="Betty", profession="teacher", row=1, col="B"),
        Person(id="A2", name="Carol", profession="guard", row=2, col="A"),
    ]
    calculate_neighbors(people)
    kb = KnowledgeBase(people)
    
    # Constraint: Sum(Criminals in Neighbors(Anna)) == 1
    # Neighbors are Betty and Carol
    constraint = kb.count_criminals(kb.get_neighbors("Anna")) == 1
    kb.solver.add(constraint)
    
    # Case A: Betty=Crim, Carol=Inn -> Valid
    kb.solver.push()
    kb.solver.add(kb.is_criminal("Betty"))
    kb.solver.add(kb.is_innocent("Carol"))
    assert kb.solver.check() == sat
    kb.solver.pop()
    
    # Case B: Betty=Crim, Carol=Crim -> Invalid (Sum=2)
    kb.solver.push()
    kb.solver.add(kb.is_criminal("Betty"))
    kb.solver.add(kb.is_criminal("Carol"))
    assert kb.solver.check() == unsat
    kb.solver.pop()
