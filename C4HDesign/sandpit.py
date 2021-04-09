import tkinter as tk
from tkinter import Canvas

import cmath as c
# from cmath import polar, phase, rect, sqrt
from math import radians
from random import randrange
from tkinter import Canvas, mainloop

i = c.sqrt(-1)

class Kanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # self.bind("<Button-1>", self.translate)
        self.bind('<Enter>', lambda event: self.focus_set()) #sets focus to canvas
        self.bind('<Leave>', lambda event: self.master.focus_set()) #remove focus
        self.bind("<KeyPress>", self.print_key)
        self.bind("<Button-1>", self.set_focus) #sets focus to sprite
        self.bind("<Button-3>", self.make_rand_poly)
        self.bind("<B1-Motion>", self.translate)
        self.bind("<Shift-B1-Motion>", self.rotate)
        self.focus_item = None
        self.polygons = []
        self.motion_ref = complex(0, 0)

    def print_key(self, event):
        if event.keysym == 'a':
            print('a')
        else:
            print(event)

    def set_focus(self, event):
        closest = self.find_closest(event.x, event.y)[0]
        for p in self.polygons:
            if p.id == closest:
                self.focus_item = p

        self.motion_ref = complex(event.x, -event.y)

    def make_rand_poly(self, event):
        self.polygons.append(Random_Polygon(self, event))
          
    def complex_to_coords(self, complex_nums):
        return [
            item for tup in [
                (c.real, -c.imag) for c in complex_nums
                ] for item in tup
            ]

    def coords_to_complex(self, coords):
        # coords = self.canvas.coords(self.id)
        return [
            complex(x,-y) for x,y in zip(coords[0::2], coords[1::2])
            ]

    def translate(self, event):
        delta_z = complex(event.x, -event.y) -self.motion_ref
        self.focus_item.pivot += delta_z
        # new_zs = [c + delta_xy for c in self.focus_item.get_coord_complex()]
        new_zs = [
            c + delta_z 
            for c in self.coords_to_complex(self.coords(self.focus_item.id))
            ]
        self.coords(self.focus_item.id, self.complex_to_coords(new_zs))
        self.motion_ref = complex(event.x, -event.y)
        
    def rotate(self, event):
        event_z = complex(event.x, -event.y)
        pivot = self.focus_item.pivot
        delta_phi = c.phase(event_z-pivot)-c.phase(self.motion_ref-pivot)
        new_coords = [
            pivot+(z-pivot)*c.exp(i*delta_phi) 
            # for z in self.focus_item.get_coord_complex()
            for z in self.coords_to_complex(self.coords(self.focus_item.id))
            ]
        self.coords(self.focus_item.id, self.complex_to_coords(new_coords))
        self.motion_ref = event_z
        
        
class Random_Polygon(object):
    def __init__(self, canvas, event, max_points=8) -> None:
        super().__init__()
        self.canvas = canvas
        self.pivot = complex(event.x, -event.y)
        points = randrange(3, max_points)
        coords = []
        self.id = None
        
        for p in range(points):
            dx = randrange(canvas.winfo_width()/-10,canvas.winfo_width()/10)
            dy = randrange(canvas.winfo_height()/-10,canvas.winfo_height()/10)
            c_p = complex(dx, -dy) + self.pivot
            coords.append((c_p.real, -c_p.imag))
        
        self.id = self.canvas.create_polygon(coords)


    def coord_to_complex(self):
        coords = self.canvas.coords(self.id)
        return [complex(x,-y) for x,y in zip(coords[0::2], coords[1::2])]



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x600')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.update()
    canvas = Kanvas(root)
    canvas.grid(column=0, row=0, sticky="NWES")
    root.update()
    print(canvas.winfo_height(),canvas.winfo_width())
    root.mainloop()

