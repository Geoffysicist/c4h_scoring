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
class C4HJump(object):
    '''A jump.'''

    id: int = 0
    number: str = ''
    shape: str = ''
    component_ids: List[int] = dataclasses.field(default_factory=lambda: [])
    
    

if __name__ == '__main__':
    print('design_helpers done!')

