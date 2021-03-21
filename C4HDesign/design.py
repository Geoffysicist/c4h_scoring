"""design.py - backend for C4HDesign, a graphics program for showjumping course design.

    Defines the main class C4HArena.

"""
# from typing import List, Any
# import yaml
# import copy

# from pathlib import Path
# from datetime import date, datetime, timezone
from tkinter import Canvas
from .design_helpers import *
# from pydantic import BaseModel

class C4HArena(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.draw_vertical)

    def draw_vertical(self, event):
        size = 20
        pole_coords = (event.x-size, event.y, event.x+size, event.y)
        self.create_line(pole_coords, width=size/10)
        


if __name__ == "__main__":
    pass