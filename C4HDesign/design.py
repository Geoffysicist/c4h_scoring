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

STRIDE = 370 #stride length in cm

class C4HPlan(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.scale = 40 #x such that scale is 1:x in pixels
        self.sprites = []
        self.motion_ref = complex(0, 0) #keeps track of motion when draging item
        self.focus_sprites = [] #items which have focus in the canvas
        self.class_height = 100 #class height in cm
        self.open = False # 3.5 stride approach, False -> 2.5 stride approach

        # all the event bindings
        self.bind('<Enter>', lambda event: self.focus_set()) #sets focus to canvas
        self.bind('<Leave>', lambda event: self.master.focus_set()) #remove focus
        self.bind("<KeyPress>", self.key_press)
        self.bind("<Button-1>", self.select)
        self.bind("<Shift-Button-1>", self.shift_select)
        self.bind("<Button-3>", self.new_sprite)
        self.bind("<B1-Motion>", self.translate)
        self.bind("<Control-B1-Motion>", self.rotate)
        

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
            self.set_focus(sprite)
            
    def clear_focus(self):
        self.focus_sprites.clear()
        self.plan_update()

    def set_focus(self, sprite):
        """Set focus to sprite.
        """
        if not sprite in self.focus_sprites:
            self.focus_sprites.append(sprite)
        self.plan_update()

    def plan_update(self):
        """Updates the colors based on focus status."""
        for sprite in self.sprites:
            for c in sprite.components:
                self.itemconfigure(
                    c.id, 
                    fill=COLORS.get(c.type)[sprite in self.focus_sprites]
                )
                
    def find_by_id(self, id: int) -> C4HSprite:
        """Finds an element by its canvas id.
        """
        for s in self.sprites:
            for c in s.components:
                if id == c.id:                    
                    return s

        return None

    def new_sprite(self, event):
        z = complex(event.x, -event.y)
        sprite = self.build_jump(z)
        self.sprites.append(sprite)
        self.plan_update()

    def delete_sprite(self, sprite):
        for component in sprite.components:
            self.delete(component.id)
        self.sprites.remove(sprite)
        
    def delete_focus_sprites(self):
        for sprite in self.focus_sprites:
            self.delete_sprite(sprite)
        self.focus_sprites.clear()
        
    def key_press(self, event):
        """Responds to a keypress by performing action on all focus sprites.
        """
        if self.focus_sprites:
            cases = {
                'd': self.replace_w_double,
                'p': self.add_path,
                's': self.replace_w_shrub,
                't': self.replace_w_triple,
                'v': self.replace_w_vertical,
                'Delete': self.delete_focus_sprites,
                }
            try:
                cases[event.keysym]()
            except KeyError:
                #not an option so
                pass


    def build_jump(self, pivot: complex, toprails: int = 1) -> C4HSprite:
        """Buid a new jump and appends it to the sprite list
        Args:
            r_width (int): the width of the rails in cm
            w_width (int): the width of the wings in cm
            angle (float): the rotation angle clockwise in degrees
        """
        j = C4HSprite()
        distance = 3.5*STRIDE
        if not self.open:
            distance = 2.5*STRIDE
        
        j.path_controls['approach_control'][0] = j.path_controls['landing_control'][0] = 2 * distance
        j.path_controls['approach'][0] = j.path_controls['landing'][0] = distance

        line_width = self.scale*0.2
        width = j.rail_width*self.scale/100 #convert width to pixels
        phi = radians(j.angle) #convert angle to radians
        j.spread = rail_spread = 0
        if toprails > 1:
            j.spread = (self.class_height+10*(toprails-1))*self.scale/100 #spread in pixels
            rail_spread = j.spread/(toprails-1)-line_width

        # make rails
        _pivot = pivot
        for toprail in range(toprails):
            rail_l = _pivot - (width/2)*c.exp(i*phi)
            rail_r = _pivot + (width/2)*c.exp(i*phi)
            rail_id = self.create_line(
                complex_to_coords([rail_l,rail_r]),
                width=line_width,
                )
            rail = C4HComponent(rail_id, 'rail')
            j.components.append(rail)
            _pivot = _pivot + rail_spread*c.exp(i*(phi-c.pi/2))

        #make arrow
        # reset the pivot
        arrow_tip = pivot - (width/3)*c.exp(i*(phi-c.pi/2))
        arrow_tail = pivot + (j.spread+width/6)*c.exp(i*(phi-c.pi/2))
        arrow_id = self.create_line(
            complex_to_coords([arrow_tip,arrow_tail]),
            width=line_width/2,
            arrow='first'
            )
        arrow = C4HComponent(arrow_id, 'arrow')
        j.components.append(arrow)

        return j

    def build_shrub(self, pivot: complex, radius=100, angle=0) -> None:
        """Buid a new vertical jump and appends it to the sprite list
        Args:
            radius (int): the radius of the shrub in cm
            angle (float): the rotation angle clockwise in degrees

        """
        shrub = C4HSprite()
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
        return shrub

    def replace_w_vertical(self):
        for i, sprite in enumerate(self.focus_sprites):
            pivot = get_pivot(self.coords(sprite.components[0].id))
            self.focus_sprites[i] = self.build_jump(pivot, toprails=1)
            self.sprites.append(self.focus_sprites[i])
            self.delete_sprite(sprite)
        self.plan_update()

    def replace_w_double(self):
        for i, sprite in enumerate(self.focus_sprites):
            pivot = get_pivot(self.coords(sprite.components[0].id))
            self.focus_sprites[i] = self.build_jump(pivot, toprails=2)
            self.sprites.append(self.focus_sprites[i])
            self.delete_sprite(sprite)
        self.plan_update()

    def replace_w_triple(self):
        for i, sprite in enumerate(self.focus_sprites):
            pivot = get_pivot(self.coords(sprite.components[0].id))
            self.focus_sprites[i] = self.build_jump(pivot, toprails=3)
            self.sprites.append(self.focus_sprites[i])
            self.delete_sprite(sprite)
        self.plan_update()

    def replace_w_shrub(self):
        for i, sprite in enumerate(self.focus_sprites):
            pivot = get_pivot(self.coords(sprite.components[0].id))
            self.focus_sprites[i] = self.build_shrub(pivot)
            self.sprites.append(self.focus_sprites[i])
            self.delete_sprite(sprite)
        self.plan_update()
        
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
            # self.set_motion_ref(event)
            self.motion_ref = event_z
            for components in [sprite.components for sprite in self.focus_sprites]:
                for component in components:
                    new_zs = [
                        z + delta_z 
                        for z in coords_to_complex(self.coords(component.id))
                        ]
                    self.coords(component.id, complex_to_coords(new_zs))
        

    def add_path(self):
        path_zs = []
        last_pivot = complex(0,0)
        last_phi = 0

        if self.open:
            approach = STRIDE*2.5*self.scale/100
        else:
            approach = STRIDE*1.5*self.scale/100

        for id, sprite in enumerate(self.focus_sprites):
            arrow_zs = coords_to_complex(self.coords(sprite.get_arrow()))
            this_pivot = get_pivot(self.coords(sprite.get_rails()[0]))
            this_phi = c.phase(arrow_zs[0]-arrow_zs[1])
            if id: #skip for the first point
                #add points of curve between last point and next point
                ac, a, l, lc = sprite.path_controls.values()
                p1 = last_pivot + l[0]*c.exp(i*last_phi)
                p2 = last_pivot + lc[0]*c.exp(i*(last_phi+lc[1]))
                p3 = this_pivot - ac[0]*c.exp(i*(this_phi+ac[1]))
                p4 = this_pivot - a[0]*c.exp(i*this_phi)
                path_zs += bezier([p1, p2, p3, p4])
            path_zs.append(this_pivot)
            last_pivot, last_phi = this_pivot, this_phi
            
        self.create_line(complex_to_coords(path_zs), smooth=True, dash=(5,5))
        self.create_line(complex_to_coords(path_zs), fill='red', dash=(5,5))
        path_len = 0
        for id, z in enumerate(path_zs):
            if id: path_len += abs(z-path_zs[id-1]) #ignore id 0
        print(f'path length: {path_len/self.scale} m')


if __name__ == '__main__':
    print('design done!')