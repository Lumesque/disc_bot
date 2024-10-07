from dataclasses import dataclass
from enum import Enum, unique
from itertools import cycle
from types import FunctionType
from typing import Optional


@unique
class Stage(Enum):
    """
    Represents the current state of the bidding machine
    """

    DEAD = 0
    RUNNING = 1
    LOCKED = 2


@dataclass
class State:
    stage: Stage
    advance_requirement: Optional[FunctionType] = None


class StateMachine:
    stages = cycle([Stage.DEAD, Stage.RUNNING, Stage.LOCKED])

    def __init__(self):
        self.current_stage = next(self.stages)

    def __next__(self):
        next_stage = next(self.stages)
        self.current_stage = next_stage
        return next_stage

    @property
    def dead(self):
        return self.current_stage == Stage.DEAD

    @property
    def running(self):
        return self.current_stage == Stage.RUNNING

    @property
    def locked(self):
        return self.current_stage == Stage.LOCKED
