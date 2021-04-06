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

COLORS = {
    'rail': ('black', 'light gray'),
    'wing': ('dark green', 'light green'),
    'arrow': ('red', 'pink'),
    'shrub': ('dark green', 'light green')
}

class C4HCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.select)
        self.bind("<Shift-Button-1>", self.shift_select)
        # self.bind("<Control-Button-1>", self.set_motion_ref)
        self.bind("<Button-3>", self.new_sprite)
        self.bind("<B1-Motion>", self.translate)
        self.bind("<Control-B1-Motion>", self.rotate)
        self.scale = 40 #x such that scale is 1:x in pixels
        self.sprites = []
        self.motion_ref = complex(0, 0) #keeps track of motion when draging item
        self.focus_sprites = [] #items which have focus in the canvas
        

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

    def set_motion_ref(self, event):
        self.motion_ref = complex(event.x, -event.y)

    def select(self, event):
        """Set focus to a single item.
        """
        self.clear_focus()
        # self.set_motion_ref(event)
        self.shift_select(event)

    def shift_select(self, event):
        """Adds an item to the focus items if close to mouse press event.
        """
        self.set_motion_ref(event)
        d = self.scale * 1
        #find the closes then determine if it is close enough
        if self.find_overlapping (event.x+d, event.y+d, event.x-d, event.y-d):
            #clicked close enough to item so find closest
            id = self.find_closest(event.x, event.y)[0]
            sprite = self.find_by_id(id)
            if not sprite.has_focus:
                self.set_focus(sprite)
            
    def clear_focus(self):
        for sprite in self.focus_sprites:
            for c in sprite.components:
                self.itemconfigure(c.id, fill=COLORS.get(c.type)[0])
        self.focus_sprites.clear()

    def set_focus(self, sprite):
        """Clears existing focus and set focus to sprite.
        
        if sprite is None then clears all focus
        """
        for c in sprite.components:
            self.itemconfigure(c.id, fill=COLORS.get(c.type)[1])
        self.focus_sprites.append(sprite)
                
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
        rail_id = self.create_line(
            complex_to_coords([rail_l,rail_r]),
            width=self.scale*0.1,
            fill=COLORS.get('rail')[0]
            )
        rail = C4HComponent(rail_id, 'rail')
        arrow_tip = pivot - (width/3)*c.exp(i*(phi-c.pi/2))
        arrow_tail = pivot + (width/6)*c.exp(i*(phi-c.pi/2))
        arrow_id = self.create_line(
            complex_to_coords([arrow_tip,arrow_tail]),
            width=self.scale*0.1,
            fill= COLORS.get('arrow')[0],
            arrow='first'
            )
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
        shrub_id = self.create_polygon(
            complex_to_coords(zs),
            fill=COLORS.get('shrub')[0]
            )
        shrub.components.append(C4HComponent(shrub_id, 'shrub'))
        self.sprites.append(shrub)


        
    def rotate(self, event):
        event_z = complex(event.x, -event.y)
        if self.focus_sprites:
            pivot = get_pivot(
                self.coords(self.focus_sprites[0].components[0].id)
                )

            delta_phi = c.phase(event_z-pivot)-c.phase(self.motion_ref-pivot)
            self.motion_ref = event_z
            for components in [sprite.components for sprite in self.focus_sprites]:
                for component in components:
                    new_zs = [
                        pivot+(z-pivot)*c.exp(i*delta_phi) 
                        for z in coords_to_complex(self.coords(component.id))
                        ]
                    self.coords(component.id, complex_to_coords(new_zs))
        

    def translate(self, event):
        event_z = complex(event.x, -event.y)
        if self.focus_sprites:
            delta_z = event_z -self.motion_ref
            self.set_motion_ref(event)
            for components in [sprite.components for sprite in self.focus_sprites]:
                for component in components:
                    new_zs = [
                        z + delta_z 
                        for z in coords_to_complex(self.coords(component.id))
                        ]
                    self.coords(component.id, complex_to_coords(new_zs))
        

        

if __name__ == '__main__':
    print('design done!')