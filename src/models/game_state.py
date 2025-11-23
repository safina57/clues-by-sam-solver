from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class Status(str, Enum):
    UNKNOWN = "unknown"
    INNOCENT = "innocent"
    CRIMINAL = "criminal"


class Person(BaseModel):
    id: str  # "A1"
    name: str
    profession: str
    row: int  # 1-5
    col: str  # A-D
    status: Status = Status.UNKNOWN
    clue: Optional[str] = None  # The clue revealed by this person, if any
    neighbors: List[str] = []  # Names of neighboring people


class GameState(BaseModel):
    people: List[Person]
    active_clues: List[str]
