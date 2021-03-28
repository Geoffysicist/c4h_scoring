import tkinter as tk
from tkinter import Canvas
from .design_helpers import *
from math import radians, cos, sin

class C4HCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.select)
        self.bind("<Button-3>", self.build_vertical)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Shift-B1-Motion>", self.rotate)
        self.scale = 4
        self.jumps = []
        self.motion_data = [] #keeps track of motion when draging item
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
        """Sets the foucs_tag ie all those items considered to have focus for moving etc.
        """
        d = self.scale * 10
        if self.find_overlapping (event.x+d, event.y+d, event.x-d, event.y-d):
            #clicked close enough to item so find closest
            id = self.find_closest(event.x, event.y)[0]
            jump = self.find_by_id(id)
            self.motion_data = [event.x, event.y]
            self.set_focus(jump)
            print("here")
        else:
            self.set_focus(None)
            print("no item selected")

    def set_focus(self, jump):
        """Clears existing focus andset new focus to jump.
        
        if jump is None then clears all focus
        """
        #clear focus
        if self.focus_item:
            for c in self.focus_item.components:
                if c.type in ['pivot', 'handle']:
                    self.itemconfigure(c.id, state=tk.HIDDEN)
            
            self.focus_item = None
        
        if jump:
            for c in jump.components:
                if c.type in ['pivot', 'handle']:
                    self.itemconfigure(c.id, state=tk.NORMAL)    

            self.focus_item = jump
                

        
    def build_vertical(self, event, width=36):
        v = C4HObstacle()
        half_width = int(width * self.scale /2)
        quarter_width = int(width * self.scale /4)
        # pivot_coords = [event.x+quarter_width, event.y+quarter_width,event.x-quarter_width, event.y-quarter_width]
        pivot_coords = [event.x, event.y,event.x, event.y]
        pivot_id = self.create_oval(pivot_coords, fill= 'light gray', state=tk.HIDDEN)
        pivot = C4HComponent(pivot_id, 'pivot', ref_coords=pivot_coords)
        handle_coords = [event.x+quarter_width, event.y-half_width,event.x-quarter_width, event.y-2*half_width]
        handle_id = self.create_oval(handle_coords, fill= 'light gray', state=tk.HIDDEN)
        handle = C4HComponent(handle_id, 'handle', ref_coords=handle_coords)
        pole_coords = [event.x-half_width, event.y, event.x+half_width, event.y]
        pole_id = self.create_line(*pole_coords, width=half_width/10, fill='black')
        pole = C4HComponent(pole_id, 'pole', ref_coords=pole_coords)
        arrow_coords = [event.x, event.y+quarter_width,event.x, event.y-half_width]
        arrow_id = self.create_line(arrow_coords, width=half_width/10, fill= 'red', arrow='last')
        arrow = C4HComponent(arrow_id, 'arrow', ref_coords=arrow_coords)
        v.components.append(pivot)
        v.components.append(handle)
        v.components.append(pole)
        v.components.append(arrow)
        v.pivot = [event.x, event.y]
        self.jumps.append(v)


    def find_by_id(self, id: int) -> C4HObstacle:
        """Finds an element by its canvas id.
        """
        for j in self.jumps:
            for c in j.components:
                if id == c.id:
                    return j

        return None

    def rotate(self, event):
        if self.focus_item:
            print(event.x, event.y)

    def drag(self, event):
        """ Moves an item in the arena by dragging with the mouse.
        """
        if self.focus_item:
            # compute how much the mouse has moved
            dx = event.x - self.motion_data[0]
            dy = event.y - self.motion_data[1]
            # move the object the appropriate amount
            self.translate(dx, dy)
            self.motion_data = [event.x, event.y]

    def translate(self, dx, dy):       
        for c in self.focus_item.components:
            self.move(c.id, dx, dy)
        # record the new position
        



        



if __name__ == '__main__':
    print('design done!')