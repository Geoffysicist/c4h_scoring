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

def bezier(control_points: list, num_points: int = 8) -> list:
    """Created a cubic bezier curve from four complex points.

    returns a list of complex point.
    """
    curve_zs = []
    p1, p2, p3, p4 = control_points
    for p in range(num_points):
        t = p/(num_points-1)
        curve_zs.append(
            p1*(1-t)**3 + 3*p2*(1-t)**2*(t)+3*p3*(1-t)*t**2+p4*t**3
            )
    return curve_zs

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
class C4HSprite(object):
    """A obstacle consisting of C4HComponents.
    
    may be a jump, island or even start finish lines"""

    number: str = ''
    rail_width: int = 360 #rail width or radius in cm
    wing_width: int = 70 #wing width in cm
    spread: int = 0 # spread in cm
    angle: int = 0 # angle from N in degrees
    components: List[C4HComponent] = dataclasses.field(default_factory=lambda: [])
    path_controls = { #modify bezier paths
        'approach_control': [0,0],
        'approach': [0],
        'landing': [0],
        'landing_control': [0,0]
    }

    def get_arrow(self) -> C4HComponent:
        """Returns the id of the arrow components.
        """
        for c in self.components:
            if c.type == 'arrow': return c.id
        return None

    def get_rails(self) -> list:
        """Returns the id of the arrow components.
        """
        return [c.id for c in self.components if c.type == 'rail']

if __name__ == '__main__':
    print('design_helpers done!')

