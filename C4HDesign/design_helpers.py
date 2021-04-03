""" design_helpers.py - dataclasses for C4HDesign.

These are called by the main class C4HDesign.
They should be considered private and only accessed through CH4Design methods
"""
import uuid
import yaml
import dataclasses
from typing import Any, List
from pydantic import validator
from pydantic.dataclasses import dataclass
# from . import score as c4h

class Config:
    """This defines the configuration for all the dataclasses.
    """
    validate_assignment = True
    arbitrary_types_allowed = True

@dataclass(config=Config)
class C4HComponent(object):
    """Components of a jump or obstacle.

    id is the canvas id of the component
    ref_coord are the coords of the component when the rotation angle is 0.
    """
    id: int
    type: str
    ref_coords: List[int] = dataclasses.field(default_factory=lambda: [])

@dataclass(config=Config)
class C4HObstacle(object):
    """A obstacle consisting of C4HComponents.
    
    may be a jump, island or even start finish lines"""

    number: str = ''
    components: List[C4HComponent] = dataclasses.field(default_factory=lambda: [])
    pivot: List[int] = dataclasses.field(default_factory=lambda: [])


if __name__ == '__main__':
    print('design_helpers done!')

