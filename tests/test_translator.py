import pytest
from unittest.mock import AsyncMock, MagicMock
from z3 import *
from src.models.game_state import Person, Status
from src.solver.knowledge_base import KnowledgeBase
from src.translator.translator import ClueTranslator, TranslationResult

# Setup dummy people for testing
@pytest.fixture
def people():
    return [
        Person(id="A1", name="Anna", profession="painter", row=1, col="A"),
        Person(id="B1", name="Betty", profession="teacher", row=1, col="B"),
        Person(id="C1", name="Carol", profession="teacher", row=1, col="C"),
        Person(id="A2", name="Dave", profession="guard", row=2, col="A"),
        Person(id="B2", name="Eli", profession="guard", row=2, col="B"),
        Person(id="C2", name="Fay", profession="cook", row=2, col="C"),
    ]

@pytest.fixture
def kb(people):
    return KnowledgeBase(people)

def test_generated_code_execution(kb):
    """
    Verify that the code snippets we expect the LLM to generate 
    are actually executable and produce valid Z3 constraints.
    """
    
    # Case 1: "Exactly 2 neighbors of Anna are innocent"
    # Anna (A1) neighbors: Betty (B1), Dave (A2), Eli (B2)
    code_1 = "kb.count_innocents(kb.get_neighbors('Anna')) == 2"
    
    # Execute
    context = {'kb': kb, 'If': If, 'Sum': Sum, 'And': And, 'Or': Or, 'Not': Not}
    constraint = eval(code_1, context)
    
    # Verify it's a Z3 BoolRef
    assert isinstance(constraint, BoolRef)
    
    # Add to solver and check consistency
    kb.solver.add(constraint)
    assert kb.solver.check() == sat

def test_complex_logic_execution(kb):
    """Test more complex generated logic."""
    
    # Case 2: "All criminals in row 1 are connected"
    code_2 = "kb.row_connected(1, True)"
    context = {'kb': kb, 'If': If, 'Sum': Sum, 'And': And, 'Or': Or, 'Not': Not}
    constraint = eval(code_2, context)
    
    assert isinstance(constraint, BoolRef)
    kb.solver.add(constraint)
    
    # Case 3: "Betty is directly left of a criminal"
    # Betty is B1. Left of C1 (Carol). So Carol must be criminal.
    # Note: "Left of" in game rules means "To the left", so A is left of B.
    # "Betty is directly left of X" -> Betty is at Col B. X must be at Col C.
    # Wait, "To the left/right always means somewhere in the same row (from your point of view)".
    # So A is left of B.
    # If Betty (B1) is directly left of X, X must be C1 (Carol).
    
    # Let's see how we'd write this in code if we didn't know who X was.
    # "Or([And(kb.is_directly_left('Betty', x), kb.is_criminal(x)) for x in kb.people_names])"
    # But we need 'kb.people_names' or similar exposed. 
    # The KB doesn't have a simple list of names property exposed in the prompt yet, 
    # but we can use kb.get_row(1) since we know Betty is in row 1.
    
    # Let's assume the LLM generates:
    code_3 = "Or([And(kb.is_directly_left('Betty', x), kb.is_criminal(x)) for x in kb.get_row(1)])"
    
    constraint_3 = eval(code_3, context)
    kb.solver.add(constraint_3)
    
    # With "Betty is directly left of a criminal", and Betty is B1, 
    # the only person to her right (who she is left of) is Carol (C1).
    # So Carol MUST be criminal.
    
    kb.solver.push()
    kb.solver.add(kb.is_innocent("Carol"))
    assert kb.solver.check() == unsat
    kb.solver.pop()

@pytest.mark.asyncio
async def test_translator_mock(monkeypatch):
    """Test the translator class with a mocked agent."""
    # Set dummy API key to bypass pydantic-ai validation during init
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")
    
    translator = ClueTranslator()
    
    # Mock the agent response
    mock_result = TranslationResult(
        logic_code="kb.is_innocent('Anna')",
        confidence=0.95,
        reasoning="Simple statement"
    )
    
    # We need to mock the agent.run method
    # Since pydantic-ai Agent.run is async
    translator.agent.run = AsyncMock(return_value=MagicMock(data=mock_result))
    
    result = await translator.translate("Anna is innocent", ["Anna", "Betty"])
    
    assert result.logic_code == "kb.is_innocent('Anna')"
    assert result.confidence == 0.95
