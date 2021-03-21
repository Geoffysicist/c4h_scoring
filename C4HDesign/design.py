from tkinter import Canvas
from .design_helpers import *

class C4HCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.set_focus)
        self.bind("<Button-3>", self.build_vertical)
        self.bind("<B1-Motion>", self.drag)
        self.scale = 50
        self.jumps = []
        self.drag_data = [] #keeps track of motion when draging item
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

    def set_focus(self, event):
        """Sets the foucs_tag ie all those items considered to have focus for moving etc.
        """
        d = self.scale/2
        if self.find_overlapping (event.x+d, event.y+d, event.x-d, event.y-d):
            #clicked close enough to item so find closest
            id = self.find_closest(event.x, event.y)[0]
            jump = self.find_by_id(id)
            self.drag_data = [event.x, event.y]
            self.focus_item = jump
        else:
            self.focus_item = None
            print("no item selected")
        
    def build_vertical(self, event):
        v = C4HJump()
        pole_coords = [event.x-self.scale, event.y, event.x+self.scale, event.y]
        arrow_cords = [event.x, event.y+self.scale/2,event.x, event.y-self.scale]
        v.component_ids.append(self.create_line(pole_coords, width=self.scale/10))
        v.component_ids.append(self.create_line(arrow_cords, width=self.scale/10, fill= 'red', arrow='last'))
        self.jumps.append(v)
        
        for j in self.jumps:
            print(j.component_ids)

    def find_by_id(self, id: int) -> C4HJump:
        """Finds an element by its canvas id.
        """

        for j in self.jumps:
            print(id, j.component_ids)
            if id in j.component_ids:
                return j

        return None

    def drag(self, event):
        """ Moves an item in the arena by dragging with the mouse.
        """
        if self.focus_item:
            # compute how much the mouse has moved
            delta_x = event.x - self.drag_data[0]
            delta_y = event.y - self.drag_data[1]
            # move the object the appropriate amount
            for i in self.focus_item.component_ids:
                self.move(i, delta_x, delta_y)
            # record the new position
            self.drag_data = [event.x, event.y]

if __name__ == '__main__':
    print('design done!')