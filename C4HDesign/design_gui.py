"""c4h_score_gui.py - GUI for C4HScore, a scoreboard for judging showjumping.
"""

import tkinter as tk
# import tkcalendar as cal
import ctypes

# from .score import C4HEvent
from tkinter import ttk, filedialog, messagebox, Canvas, Frame
# from datetime import date

# makes dpi aware so tkinter text isnt blurry
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class C4HDesignGUI(ttk.Notebook):
    ''' Big container for the rest of the stuff.

    Attributes:
        event (C4HEvent): The big kahuna, or None before initialisation
    '''
    def __init__(self, master):
        ''' creates the master window and sets the main menubar.
        '''
        super().__init__(master)
        self.event = None

        # set up the gui
        self.title = 'Courses4Horses Design'
        self.master = master
        self.master.title(self.title)
        self.favicon = tk.PhotoImage(file='assets/courses4horses_logo_bare.png')
        self.master.iconphoto(False, self.favicon)
        self.master.geometry('1600x1200')
        self.grid(row=0, column=0, sticky="NSEW")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # set the main menu
        self.menubar = tk.Menu(self.master)

        # the event menu
        self.eventmenu = tk.Menu(self.menubar, tearoff=0)
        self.eventmenu.add_command(label="New", command=self.canvas_new)
        self.menubar.add_cascade(label="Canvas", menu=self.eventmenu)
        self.master.config(menu=self.menubar)

    def canvas_new(self):
        # new_frame = ttk.Frame(self)
        this_canvas = C4HCanvas(self)

        this_canvas.grid(column=0, row=0, sticky="NSEW")
        self.add(this_canvas, text="Canvas 1")
        return this_canvas


class C4HCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.save_posn)
        self.bind("<B1-Motion>", self.add_line)
        
    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y

    def add_line(self, event):
        self.create_line((self.lastx, self.lasty, event.x, event.y))
        self.save_posn(event)

