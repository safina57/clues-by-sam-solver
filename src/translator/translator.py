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
        )
        self.agent = Agent(
            model=self.model,
            output_type=TranslationResult,
            system_prompt=(
                "You are an expert logic translator for the 'Clues by Sam' puzzle. "
                "Your goal is to translate natural language clues into Python code that uses the Z3 solver. "
            )
        )
    async def translate(self, clue: str, people_names: List[str]) -> TranslationResult:
        # We pass the names as context so the LLM knows valid entities
        prompt = f"Clue: \"{clue}\"\nValid Names: {', '.join(people_names)}"
        result = await self.agent.run(prompt)
        return result.output
