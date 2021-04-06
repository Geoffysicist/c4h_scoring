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


def complex_to_coords(complex_nums):
    return [
        item for tup in [
            (c.real, -c.imag) for c in complex_nums
            ] for item in tup
        ]

def coords_to_complex(coords):
    return [
        complex(x,-y) for x,y in zip(coords[0::2], coords[1::2])
        ]

def get_pivot(coords: list) -> complex:
    """returns a pivot point as a complex number

    the pivot point is the mean of the points.
    """
    zs = coords_to_complex(coords)
    return sum(zs)/len(zs)

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

@dataclass(config=Config)
class C4HObstacle(object):
    """A obstacle consisting of C4HComponents.
    
    may be a jump, island or even start finish lines"""

    number: str = ''
    components: List[C4HComponent] = dataclasses.field(default_factory=lambda: [])
    has_focus: bool = False

if __name__ == '__main__':
    print('design_helpers done!')

