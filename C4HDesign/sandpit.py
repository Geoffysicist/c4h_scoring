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
        self.bind("<Button-1>", self.set_focus)
        self.bind("<Button-3>", self.make_rand_poly)
        self.bind("<B1-Motion>", self.translate)
        self.bind("<Shift-B1-Motion>", self.rotate)
        self.focus_item = None
        self.polygons = []
        self.motion_ref = complex(0, 0)

    def set_focus(self, event):
        closest = self.find_closest(event.x, event.y)[0]
        for p in self.polygons:
            if p.id == closest:
                self.focus_item = p

        self.motion_ref = complex(event.x, -event.y)

    def make_rand_poly(self, event):
        self.polygons.append(Random_Polygon(self, event))

          
    def translate(self, event):
        delta_xy = complex(event.x, -event.y) -self.motion_ref
        self.focus_item.pivot += delta_xy
        new_coords = [c + delta_xy for c in self.focus_item.get_coord_complex()]
        self.coords(self.focus_item.id, self.complex_coords_to_list(new_coords))
        self.motion_ref = complex(event.x, -event.y)

    def complex_coords_to_list(self, complex_coords):
        return [
            item for tup in [
                (c.real, -c.imag) for c in complex_coords
                ] for item in tup
            ]

    def _rotate(self, event):
        xy = complex(event.x, event.y)
        pivot = self.focus_item.pivot
        # delta_phi = phase(pivot-xy)-phase(self.motion_ref-pivot)
        delta_phi = phase(self.motion_ref-pivot)-phase(pivot-xy)
        new_coords = [
            rect(abs(c-pivot), delta_phi+phase(pivot-c))+pivot 
            for c in self.focus_item.get_coord_complex()
            ]
        self.coords(self.focus_item.id, self.complex_coords_to_list(new_coords))
        self.motion_ref = xy
        
    def rotate(self, event):
        xy = complex(event.x, -event.y)
        pivot = self.focus_item.pivot
        delta_phi = c.phase(xy-pivot)-c.phase(self.motion_ref-pivot)
        new_coords = [
            pivot+(z-pivot)*c.exp(i*delta_phi) 
            for z in self.focus_item.get_coord_complex()
            ]
        self.coords(self.focus_item.id, self.complex_coords_to_list(new_coords))
        self.motion_ref = xy
        
        

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


    def get_coord_complex(self):
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

