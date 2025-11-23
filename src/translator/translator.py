import os
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai import Agent


class TranslationResult(BaseModel):
    logic_code: str = Field(description="Python code snippet evaluating to a Z3 BoolRef. Return 'None' if text is flavor text.")
    confidence: float = Field(description="Confidence score 0-1.")
    reasoning: str = Field(description="Explanation of the translation.")

class ClueTranslator:
    def __init__(self):
        self.model = OpenAIChatModel(
        'gpt-4o',
        provider=AzureProvider(),
        settings=ModelSettings(temperature=0)
        )
        self.agent = Agent(
            model=self.model,
            output_type=TranslationResult,
            system_prompt=(
                "You are an expert logic translator for the 'Clues by Sam' puzzle. "
                "Your goal is to translate natural language clues into Python code that uses the Z3 solver. "
                "You have access to a 'kb' object with the following API:\n"
                "--- Predicates (return Z3 BoolRef) ---\n"
                "- kb.is_criminal(name: str)\n"
                "- kb.is_innocent(name: str)\n"
                "- kb.row_connected(row_num: int, status_is_criminal: bool) -> Enforces that all people of 'status' in row are connected (orthogonally adjacent).\n\n"
                "--- List Getters (return List[str] of names) ---\n"
                "- kb.get_neighbors(name) -> All 8 neighbors (including diagonals)\n"
                "- kb.get_orthogonal_neighbors(name) -> Up/Down/Left/Right only\n"
                "- kb.get_common_neighbors(n1, n2) -> Neighbors shared by both\n"
                "- kb.get_row(row_num) -> All in row (1-5)\n"
                "- kb.get_col(col_char) -> All in col ('A'-'D')\n"
                "- kb.get_profession(prof_str) -> All with profession\n"
                "- kb.get_corners() -> The 4 corner people\n"
                "- kb.get_edges() -> The 14 edge people\n"
                "- kb.get_between(n1, n2) -> People strictly between n1 and n2 (same row/col)\n"
                "- kb.get_left_of(name) -> All people to the left in same row\n"
                "- kb.get_right_of(name) -> All people to the right in same row\n"
                "- kb.get_above(name) -> All people above in same col\n"
                "- kb.get_below(name) -> All people below in same col\n\n"
                "--- Counters (return Z3 ArithRef) ---\n"
                "- kb.count_criminals(names: List[str])\n"
                "- kb.count_innocents(names: List[str])\n\n"
                "--- Static Checks (return bool) ---\n"
                "- kb.is_above(n1, n2) -> n1 is in same col, lower row index than n2\n"
                "- kb.is_below(n1, n2)\n"
                "- kb.is_left_of(n1, n2) -> n1 is in same row, lower col index than n2\n"
                "- kb.is_right_of(n1, n2)\n"
                "- kb.is_directly_above(n1, n2)\n"
                "- kb.is_directly_below(n1, n2)\n"
                "- kb.is_directly_left(n1, n2)\n"
                "- kb.is_directly_right(n1, n2)\n\n"
                "--- Instructions ---\n"
                "1. Return ONLY the expression that evaluates to a Z3 constraint (BoolRef).\n"
                "2. Use Python list comprehensions and Z3 functions (If, Sum, And, Or, Not, Implies) if needed.\n"
                
            )
        )
    async def translate(self, clue: str, people_names: List[str]) -> TranslationResult:
        # We pass the names as context so the LLM knows valid entities
        prompt = f"Clue: \"{clue}\"\nValid Names: {', '.join(people_names)}"
        result = await self.agent.run(prompt)
        return result.output
