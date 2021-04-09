"""c4h_score_gui.py - GUI for C4HScore, a scoreboard for judging showjumping.

    assumed screen ratio of 16:9
    prototype window is 3200:1800
    set scale in design.py to 20 -> 1 m is 20 pixels
"""

import tkinter as tk
# import tkcalendar as cal
from PIL import ImageTk, Image
import ctypes #make tkinter dpi aware

from .design import C4HPlan
from tkinter import ttk#, filedialog, messagebox, Canvas, Frame
# from datetime import date

# makes dpi aware so tkinter text isnt blurry
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class C4HDesignGUI(ttk.Notebook):
    ''' Big container for the rest of the stuff.

    '''
    def __init__(self, master):
        ''' creates the master window and sets the main menubar.
        '''
        super().__init__(master)
        # self.event = None

        # set up the gui
        self.title = 'Courses4Horses Design'
        self.master = master
        self.master.title(self.title)
        self.favicon = tk.PhotoImage(file='assets/courses4horses_logo_bare.png')
        self.master.iconphoto(False, self.favicon)
        self.master.geometry('3200x1800')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.update()
        self.grid(row=0, column=0, sticky="NSEW")
        # self.master.grid_rowconfigure(0, weight=1)
        # self.master.grid_columnconfigure(0, weight=1)

        # set the main menu
        self.menubar = tk.Menu(self.master)

        # the event menu
        self.eventmenu = tk.Menu(self.menubar, tearoff=0)
        self.eventmenu.add_command(label="New", command=self.plan_new)
        self.menubar.add_cascade(label="Plan", menu=self.eventmenu)
        self.master.config(menu=self.menubar)

    def plan_new(self):
        # this_canvas = C4HPlan(self,width=2200, height=1600)
        this_canvas = C4HPlan(self)

        this_canvas.grid(column=0, row=0, sticky="NSEW")
        # this_canvas.grid(column=0, row=0, sticky="NW")
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.add(this_canvas, text="Plan 1")
        
        return this_canvas




