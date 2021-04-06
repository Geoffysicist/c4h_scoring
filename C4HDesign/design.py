"""design.py - backend for C4HDesign showjumping course designcsoftware.

    Defines the main classes called by design_gui.py.
    Not intended for standalone use.

"""
import tkinter as tk
import cmath as c
# from tkinter import Canvas
from .design_helpers import *
from math import radians, cos, sin, sqrt
i = c.sqrt(-1)

class C4HCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.select)
        self.bind("<Button-3>", self.build_vertical)
        self.bind("<B1-Motion>", self.translate)
        self.bind("<Shift-B1-Motion>", self.rotate)
        self.scale = 40 #x such that scale is 1:x in pixels
        self.sprites = []
        self.motion_ref = complex(0, 0) #keeps track of motion when draging item
        self.focus_item = None #item which has focus in the canvas
        # self.items = 1 #a counter to keep track of the items created, used for tag ids
        

    def set_object(self, obj: object, **kwargs) -> bool:
        """Updates the value of the attributes in obj given by kwargs.

        Args:
            obj: A C4HScore object.
            kwargs: Can be any attribute of the obj.

        Returns:
            bool: success or otherwise.

        Example:
            this_event.set_object(arena1, name='Main Arena')
        """

        for key, val in kwargs.items():
            setattr(obj, key, val)

        self.update()
        return True

    def select(self, event):
        """Sets the foucus_tag ie all those items considered to have focus for moving etc.
        """
        d = self.scale * 1
        #find the closes then determine if it is colse enough
        if self.find_overlapping (event.x+d, event.y+d, event.x-d, event.y-d):
            #clicked close enough to item so find closest
            id = self.find_closest(event.x, event.y)[0]
            self.focus_item = self.find_by_id(id)
            self.motion_ref = complex(event.x, -event.y)
        else:
            self.set_focus(None)
            print("no item selected")

    def set_focus(self, sprite):
        """Clears existing focus and set focus to sprite.
        
        if sprite is None then clears all focus
        """
        #clear focus
        if self.focus_item:
            #TODO change the colors - I hate american spelling     
            self.focus_item = None
        
        if sprite:
            #TODO set colors
            self.focus_item = sprite
                
    def find_by_id(self, id: int) -> C4HObstacle:
        """Finds an element by its canvas id.
        """
        for s in self.sprites:
            for c in s.components:
                if id == c.id:                    
                    return s

        return None

    #TODO start here    
    def build_vertical(self, event, width=360):
        v = C4HObstacle()
        half_width = int(width/100 * self.scale /2)
        quarter_width = int(width/100 * self.scale /4)
        # pivot_coords = [event.x, event.y]
        # pivot_id = self.create_polygon(pivot_coords, state=tk.HIDDEN)
        # pivot = C4HComponent(pivot_id, 'pivot', ref_coords=pivot_coords)
        # handle_coords = [event.x+quarter_width, event.y-half_width,event.x-quarter_width, event.y-2*half_width]
        # handle_id = self.create_oval(handle_coords, fill= 'light gray', state=tk.HIDDEN)
        # handle = C4HComponent(handle_id, 'handle', ref_coords=handle_coords)
        pole_coords = [event.x-half_width, event.y, event.x+half_width, event.y]
        pole_id = self.create_line(*pole_coords, width=half_width/10, fill='black')
        pole = C4HComponent(pole_id, 'pole', ref_coords=pole_coords)
        arrow_coords = [event.x, event.y+quarter_width,event.x, event.y-half_width]
        arrow_id = self.create_line(arrow_coords, width=half_width/10, fill= 'red', arrow='last')
        arrow = C4HComponent(arrow_id, 'arrow', ref_coords=arrow_coords)
        # v.components.append(pivot)
        # v.components.append(handle)
        v.components.append(pole)
        v.components.append(arrow)
        # v.pivot = [event.x, event.y]
        v.pivot = complex(event.x, -event.y)
        self.sprites.append(v)

    def rotate(self, event):
        if self.focus_item:
            event_z = complex(event.x, -event.y)
            pivot = self.focus_item.pivot
            delta_phi = c.phase(event_z-pivot)-c.phase(self.motion_ref-pivot)
            self.motion_ref = event_z
            for comp in self.focus_item.components:
                new_zs = [
                    pivot+(z-pivot)*c.exp(i*delta_phi) 
                    # for z in self.focus_item.get_coord_complex()
                    for z in coords_to_complex(self.coords(comp.id))
                    ]
                self.coords(comp.id, complex_to_coords(new_zs))
        

    def translate(self, event):
        if self.focus_item:
            delta_z = complex(event.x, -event.y) -self.motion_ref
            self.motion_ref = complex(event.x, -event.y)
            self.focus_item.pivot += delta_z
            for comp in self.focus_item.components:
                new_zs = [
                    c + delta_z 
                    for c in coords_to_complex(self.coords(comp.id))
                    ]
                self.coords(comp.id, complex_to_coords(new_zs))
        

        

if __name__ == '__main__':
    print('design done!')