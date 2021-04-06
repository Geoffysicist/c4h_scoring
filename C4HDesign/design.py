"""design.py - backend for C4HDesign showjumping course designcsoftware.

    Defines the main classes called by design_gui.py.
    Not intended for standalone use.

"""
import tkinter as tk
import cmath as c
from random import randint
# from tkinter import Canvas
from .design_helpers import *
from math import radians, cos, sin
i = c.sqrt(-1)

class C4HCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.select)
        self.bind("<Button-3>", self.new_sprite)
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

    def new_sprite(self, event):
        z = complex(event.x, -event.y)
        self.build_vertical(z)
        self.build_shrub(z+2*self.scale)

    def build_vertical(self, pivot: complex, width=360, angle=0) -> None:
        """Buid a new vertical jump and appends it to the sprite list
        Args:
            r_width (int): the width of the rails in cm
            w_width (int): the width of the wings in cm
            angle (float): the rotation angle clockwise in degrees

        """
        v = C4HObstacle()
        width = self.scale*width/100
        phi = radians(angle)
        rail_l = pivot - (width/2)*c.exp(i*phi)
        rail_r = pivot + (width/2)*c.exp(i*phi)
        rail_id = self.create_line(complex_to_coords([rail_l,rail_r]), width=self.scale*0.1, fill='black')
        rail = C4HComponent(rail_id, 'rail')
        arrow_tip = pivot - (width/3)*c.exp(i*(phi-c.pi/2))
        arrow_tail = pivot + (width/6)*c.exp(i*(phi-c.pi/2))
        arrow_id = self.create_line(complex_to_coords([arrow_tip,arrow_tail]), width=self.scale*0.1, fill= 'red', arrow='first')
        arrow = C4HComponent(arrow_id, 'arrow')
        v.components.append(rail)
        v.components.append(arrow)
        self.sprites.append(v)

    def build_shrub(self, pivot: complex, radius=100, angle=0) -> None:
        """Buid a new vertical jump and appends it to the sprite list
        Args:
            radius (int): the radius of the shrub in cm
            angle (float): the rotation angle clockwise in degrees

        """
        shrub = C4HObstacle()
        radius = int(self.scale*radius/100)
        phi = radians(angle)
        zs = []
        for n in range(16):
            zs.append(pivot + randint(int(radius/2),radius)*c.exp(i*n*c.tau/16))
        shrub_id = self.create_polygon(complex_to_coords(zs), fill='dark green')
        shrub.components.append(C4HComponent(shrub_id, 'shrub'))
        self.sprites.append(shrub)


        
    def rotate(self, event):
        if self.focus_item:
            event_z = complex(event.x, -event.y)
            pivot = get_pivot(self.coords(self.focus_item.components[0].id))

            delta_phi = c.phase(event_z-pivot)-c.phase(self.motion_ref-pivot)
            self.motion_ref = event_z
            for comp in self.focus_item.components:
                new_zs = [
                    pivot+(z-pivot)*c.exp(i*delta_phi) 
                    for z in coords_to_complex(self.coords(comp.id))
                    ]
                self.coords(comp.id, complex_to_coords(new_zs))
        

    def translate(self, event):
        if self.focus_item:
            delta_z = complex(event.x, -event.y) -self.motion_ref
            self.motion_ref = complex(event.x, -event.y)
            for comp in self.focus_item.components:
                new_zs = [
                    c + delta_z 
                    for c in coords_to_complex(self.coords(comp.id))
                    ]
                self.coords(comp.id, complex_to_coords(new_zs))
        

        

if __name__ == '__main__':
    print('design done!')