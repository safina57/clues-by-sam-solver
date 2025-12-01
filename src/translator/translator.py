from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider


class TranslationResult(BaseModel):
    logic_code: str = Field(
        description="Python code snippet evaluating to a Z3 BoolRef. Return 'None' if text is flavor text."
    )
    confidence: float = Field(description="Confidence score 0-1.")
    reasoning: str = Field(description="Explanation of the translation.")
    is_flavor_text: bool = Field(
        description="True if the text is just flavor text/dialogue and not a logic clue."
    )


class ClueTranslator:
    def __init__(self):
        self.model = OpenAIChatModel(
            "gpt-4o", provider=AzureProvider(), settings=ModelSettings(temperature=0)
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
                "- kb.row_connected(row_num: int, status_is_criminal: bool) -> "
                "Enforces that all people of 'status' in row are connected (orthogonally adjacent).\n\n"
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
                "3. EXTRACT ALL INFORMATION: A single clue often contains multiple constraints. "
                "Use And(...) to combine them.\n"
                "4. 'Exactly M of the N X are Y' implies TWO constraints:\n"
                "   a. There are exactly N people who are X "
                "(e.g., '4 innocents neighboring Carol' -> count_innocents(neighbors('Carol')) == 4)\n"
                "   b. Among those N people, exactly M are Y.\n"
                "5. 'X neighboring Y' means Y is in X's neighbors. "
                "Do NOT assume 'common neighbors' unless the clue says 'neighboring BOTH X and Y'.\n"
                "6. 'Above' means anywhere above in the same column. 'Directly above' means immediately above.\n"
                "7. 'Odd number of X' means count(X) % 2 == 1. 'Even number' means count(X) % 2 == 0. "
                "Do NOT use Exists() for this.\n"
                "8. FLAVOR TEXT: If the input is just dialogue (e.g., 'I should have known...') "
                "or does not contain a logic puzzle clue, set is_flavor_text=True and logic_code='True'.\n"
                "9. SELF REFERENCE: 'me', 'my', 'I' refer to the 'Speaker' provided in the prompt. "
                "Replace them with the speaker's name string.\n"
                "10. 'ONLY X with Y' means X has Y, and ALL OTHER X do NOT have Y. "
                "(e.g., 'Row 2 is the only row with 1 criminal' -> Row 2 has 1 criminal, "
                "all other rows have != 1 criminal).\n"
                "11. 'To the left/right/above/below' refers to ALL people in that direction in the same row/column, "
                "not just neighbors. Use kb.get_left_of() etc.\n"
                "12. DO NOT use backslashes '\\' for line continuation in the generated code. "
                "Python's 'eval' handles newlines inside parentheses automatically.\n"
                "13. 'Exactly N X are Y' (without specifying a total count of X) means `count(X and Y) == N`. "
                "Do NOT infer `count(X) == N` unless explicitly stated (e.g. 'Exactly N of the M X...').\n"
                "    Example: 'Exactly 1 innocent neighboring Ruth is a mech' -> "
                "kb.count_innocents([n for n in kb.get_neighbors('Ruth') if n in kb.get_profession('mech')]) == 1\n\n"
                "14. 'Both X are Y' implies `count(X) == 2` AND `count(X and Y) == 2` (or similar logic).\n"
                "    Example: 'Both innocents in row 1 are connected' -> \n"
                "    And(kb.count_innocents(kb.get_row(1)) == 2, kb.row_connected(1, status_is_criminal=False))\n\n"
                "--- Examples ---\n"
                "Clue: 'Exactly 2 of the 4 innocents neighboring Carol are above Zoe'\n"
                "Code: And(\n"
                "    kb.count_innocents(kb.get_neighbors('Carol')) == 4,\n"
                "    kb.count_innocents([n for n in kb.get_neighbors('Carol') if kb.is_above(n, 'Zoe')]) == 2\n"
                ")\n\n"
                "Clue: 'An odd number of innocents on the edges neighbor Salil'\n"
                "Code: kb.count_innocents([n for n in kb.get_neighbors('Salil') if n in kb.get_edges()]) % 2 == 1\n\n"
                "Clue: 'There is an odd number of criminals to the left of me' (Speaker: 'Anna')\n"
                "Code: kb.count_criminals(kb.get_left_of('Anna')) % 2 == 1\n\n"
                "Clue: 'Row 2 is the only row with exactly one criminal'\n"
                "Code: And(\n"
                "    kb.count_criminals(kb.get_row(2)) == 1,\n"
                "    And([kb.count_criminals(kb.get_row(r)) != 1 for r in range(1, 6) if r != 2])\n"
                ")\n\n"
                "Clue: 'Exactly 2 innocents below Annie are neighboring Sam'\n"
                "Code: kb.count_innocents([n for n in kb.get_below('Annie') if n in kb.get_neighbors('Sam')]) == 2\n\n"
                "Clue: 'I should have known I would get caught...'\n"
                "Code: True\n"
                "is_flavor_text: True\n"
            ),
        )

    async def translate(
        self, clue: str, people_names: List[str], speaker: str = None
    ) -> TranslationResult:
        # We pass the names as context so the LLM knows valid entities
        prompt = f"Clue: \"{clue}\"\nValid Names: {', '.join(people_names)}"
        if speaker:
            prompt += f"\nSpeaker: {speaker}"

        result = await self.agent.run(prompt)
        return result.output
