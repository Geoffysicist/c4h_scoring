"""c4h_score_gui.py - GUI for C4HScore, a scoreboard for judging showjumping.
"""

import tkinter as tk
import tkcalendar as cal
import ctypes
# import c4h_score

# from c4h_score import C4HEvent
from .score import C4HEvent
from tkinter import ttk, filedialog, messagebox
from datetime import date

# makes dpi aware so tkinter text isnt blurry
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class C4HScoreGUI(ttk.Notebook):
    #TODO change this to a ttk.Notebook object
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
        self.title = 'Courses4Horses Score'
        self.master = master
        self.master.title(self.title)
        self.favicon = tk.PhotoImage(file='assets/courses4horses_logo_bare.png')
        self.master.iconphoto(False, self.favicon)
        self.master.geometry('1600x1200')
        # self.mainframe = ttk.Notebook(self.master)
        # self.mainframe.grid(row=0, column=0, sticky="NSEW")
        self.grid(row=0, column=0, sticky="NSEW")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # set the main menu
        self.menubar = tk.Menu(self.master)

        # the event menu
        self.eventmenu = tk.Menu(self.menubar, tearoff=0)
        self.eventmenu.add_command(label="New", command=self.event_new)
        self.eventmenu.add_command(label="Open", command=self.event_open)
        self.eventmenu.add_command(label="Edit", command=self.event_edit)
        self.eventmenu.add_command(label="Save", command=self.event_save)
        self.eventmenu.add_command(label="Save As", command=self.event_save_as)
        self.eventmenu.add_separator()
        self.eventmenu.add_command(label="Print", command=self.event_print)
        self.eventmenu.add_separator()
        self.eventmenu.add_command(label="Exit", command=self.event_exit)   
        self.menubar.add_cascade(label="Event", menu=self.eventmenu)

        # the class menu
        self.jumpclassmenu = tk.Menu(self.menubar, tearoff=0)
        self.jumpclassmenu.add_command(label="New", command=self.jumpclass_new)
        # self.jumpclassmenu.add_command(label="Open", command=self.jumpclass_open)
        self.jumpclassmenu.add_command(label="Edit", command=self.jumpclass_edit)
        self.menubar.add_cascade(label="Class", menu=self.jumpclassmenu)

        self.master.config(menu=self.menubar)

        self.update()

    def update(self):

        # enable/disable menu items depending on event state
        if not self.event:
            self.eventmenu.entryconfig("Save", state="disabled")
            self.eventmenu.entryconfig("Save As", state="disabled")
            self.eventmenu.entryconfig("Edit", state="disabled")
            self.menubar.entryconfig("Class", state="disabled")
        else:    
            self.eventmenu.entryconfig("Save As", state="normal")
            self.eventmenu.entryconfig("Edit", state="normal")
            self.menubar.entryconfig("Class", state="normal")
        
            if (self.event.last_change > self.event.last_save) and self.event.filename:
                self.eventmenu.entryconfig("Save", state="normal")
            else:
                self.eventmenu.entryconfig("Save", state="disabled")

            if len(self.event.get_jumpclasses()) == 0:
                self.jumpclassmenu.entryconfig("Edit", state="disabled")
            else:
                self.jumpclassmenu.entryconfig("Edit", state="normal")

    def event_new(self):
        """Opens a new event dialog."""
        if self.event_check_saved() == 'cancelled': return

        self.event = C4HEvent('New Event')
        self.event_edit()

    def event_open(self):
        '''Opens an existing event from a c4hs file.

        Uses a filedialog to get filename and passes this to C4HEvent.open()
        Warns user if unsaved data
        '''
        if self.event_check_saved() == 'cancelled': return

        fn = filedialog.askopenfilename(
            title="Select file to open",
            filetypes=[('C4HScore files','*.c4hs')])

        #if cancel button wasn't clicked
        if fn:
            # if no event yet need to create one
            # TODO better to do this with a class level method
            if not self.event:
                self.event = C4HEvent('_')
            
            self.event = self.event.event_open(fn)

            self.update()

    def event_edit(self):
        '''Opens a C4HEventDialog for editing event details.'''
        
        C4HEventDialog(self)

    def event_save(self):
        self.event.event_save()

    def event_save_as(self):
        '''Saves the event as a c4hs yaml file.

        Opens a filedialog and then passes fn to C4HEvent.save_as()
        '''
        fn = filedialog.asksaveasfilename(
            title="Save file as",
            filetypes=[('C4HScore files','*.c4hs')],
            defaultextension='.c4hs'
            )

        #if cancel button wasn't clicked
        if fn:
            self.event.event_save_as(fn)

    def event_print(self):
        if self.event:
            print(self.event.name)
        else:
            print(type(self.event))

    def event_exit(self):
        if self.event_check_saved() == 'cancelled': return

        self.master.quit()

    def event_check_saved(self):
        '''Checks whether data have been saved since last change.

        Warns is not saved and prompts to save.
        '''
        if self.event:
            if self.event.last_change > self.event.last_save:
                save_changes = messagebox.askyesnocancel(
                    title="Are you sure you aren't making a big mistake?", 
                    message=
                        'WARNING: You have unsaved changes! Do you want to save them?'
                    )

                if save_changes == True:
                    if self.event.filename:
                        self.event_save()
                    else:
                        self.event_save_as()
                elif save_changes == None:
                    # cancelled so do nothing
                    return 'cancelled'

    def jumpclass_new(self):
        """Create a new jumpclass and open the jumpclass editor."""
        #TODO need to ensure a unique ID
        jumpclass = self.event.arenas[0].new_jumpclass()
        self.jumpclass_edit(jumpclass)

    def jumpclass_edit(self, jumpclass=None):
        """Open the jumpclass editor and set selection to jumpclass.
        
        If no lumpclass is passed the selection is set to jumpclass1 in arena1

        Args:
            jumpclass (C4HJumpclass): Default is None.
        """
        if not jumpclass:
            jumpclass = self.event.get_jumpclasses()[0]
        # jumpclass_tab = C4HJumpClassTab(self, jumpclass)
        # self.add(jumpclass_tab, text=jumpclass.name)
        C4HJumpClassTab(self, jumpclass)

class C4HEventDialog(tk.Toplevel):
    '''A top level dialog for editing event details.

    Attributes:
        event (C4HEvent):
        arenas (list of C4HArenas):

    '''
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.event = master.event
        self.title(f'{self.master.title}: {self.event.name}')
        self.iconphoto(False, self.master.favicon)

        self.event_name = tk.StringVar(self,f"{self.event.name}")
        self.arenas = []
        for a in self.event.arenas:
            self.arenas.append([a._ID, tk.StringVar(self,f'{a.id}'),
                tk.StringVar(self,f'{a.name}')])

        event_lbl = ttk.Label(self, text='Event Name: ')
        event_name_entry = ttk.Entry(self, textvariable=self.event_name)

        start_lbl = ttk.Label(self, text='Start Date: ')
        self.start_picker = cal.DateEntry(self, locale='en_AU')
        self.start_picker.set_date(self.event.dates[0])
        end_lbl = ttk.Label(self, text='End Date: ')
        self.end_picker = cal.DateEntry(self, locale='en_AU')
        self.end_picker.set_date(self.event.dates[1])
        self.start_picker.bind('<<DateEntrySelected>>', self.check_dates)
        self.end_picker.bind('<<DateEntrySelected>>', self.check_dates)

        done_btn = ttk.Button(self, text='Done', default='active', command=self.set_event)
        cancel_btn = ttk.Button(self, text='Cancel', command=self.destroy)

        # one frame to rule the arenas
        self.arena_frame = ttk.Frame(self)
        arena_lbl = ttk.Label(self, text='Arenas')
        arena_id_lbl = ttk.Label(self.arena_frame, text='ID')
        arena_name_lbl = ttk.Label(self.arena_frame, text='Name')

        add_arena_btn = ttk.Button(self, text='Add arena', default='active', command=self.arena_add)
        del_arena_btn = ttk.Button(self, text='Delete arena', default='disabled')

        # grid it up, Baby!
        event_lbl.grid(column=1, row=1, sticky='E')
        event_name_entry.grid(column=2, row=1, sticky='EW',columnspan=3)
        start_lbl.grid(column=1, row=2, sticky='E')
        self.start_picker.grid(column=2, row=2)
        end_lbl.grid(column=3, row=2, sticky='E')
        self.end_picker.grid(column=4, row=2)

        ttk.Separator(self, orient='horizontal').grid(column=1, row=3, sticky='EW', columnspan=4)

        arena_lbl.grid(column=1, row=4)
        add_arena_btn.grid(column=1, row=5)
        # edit_arena_btn.grid(column=1, row=6)
        del_arena_btn.grid(column=1, row=7)

        self.arena_frame.grid(column=2, row=4, sticky='NSEW', columnspan=3, rowspan=4)
        self.arena_frame_update() # this needs to be dynamic

        ttk.Separator(self, orient='horizontal').grid(column=1, row=8, sticky='EW', columnspan=4)
        
        done_btn.grid(column=2, row=9)
        cancel_btn.grid(column=3, row=9)

        # add some nice padding all round
        for c in self.winfo_children():
            c.grid_configure(padx=10, pady=10)
        start_lbl.grid_configure(padx=(100,10))
        self.end_picker.grid_configure(padx=(10,100))
        
        # grid the arenaframe children
        arena_id_lbl.grid(column=1, row=1)
        arena_name_lbl.grid(column=2, row=1, sticky='W')
        self.arena_frame.grid_columnconfigure(1, weight=1)
        self.arena_frame.grid_columnconfigure(2, weight=3)
 

        # for c in arena_frame.winfo_children():
        #     c.grid_configure(padx=10, pady=10)

        # jumpclass_name_lbl.grid_configure(padx=(50,10))
        event_name_entry.focus()
        event_name_entry.select_range(0,len(self.event_name.get()))

        self.wait_visibility() # cant grab until visible
        self.grab_set() # keeps focus on this dialog


    def check_dates(self, event):
        '''Ensures that the end date >= start date.
        '''
        if self.start_picker.get_date() > self.end_picker.get_date():
            self.end_picker.set_date(self.start_picker.get_date())
            self.end_picker.configure(mindate=self.start_picker.get_date())

    def arena_frame_update(self):
        # clear the frame
        for w in self.arena_frame.winfo_children():
            w.destroy
        
        # now update it
        for i, val in enumerate(self.arenas, 2): #first entry box on the 2nd row
            ttk.Entry(self.arena_frame, textvariable=val[1]).grid(row=i, column=1)
            ttk.Entry(self.arena_frame, textvariable=val[2]).grid(row=i, column=2)
    
    def arena_add(self):
        id = len(self.arenas)+1
        self.arenas.append([None, tk.StringVar(self,id), tk.StringVar(self, f'Arena {id}')])
        self.arena_frame_update()

    def set_event(self):
        self.event.name = self.event_name.get()
        self.event.dates = [self.start_picker.get_date(),self.end_picker.get_date()]
        # self.event.arenas = []
        for a in self.arenas:
            this_arena = self.event.get_arena(a[0])
            if this_arena: #arena already exists
                this_arena.id = a[1].get()
                this_arena.name = a[2].get()
            else:
                self.event.new_arena(a[1].get(), a[2].get())

        self.event.update()
        self.master.update()
        self.destroy()

# class C4HJumpClassTab(ttk.Frame):
class C4HJumpClassTab(tk.Toplevel):
    '''Frame for holding jump class details.
    '''

    def __init__(self, master, jumpclass):
        ''' Inits the jump class.

        master (C4HEventDialog)
        jumpclass (C4HJumpClass)
        '''
        super().__init__(master)
        self.jumpclass = jumpclass
        self.master = master

        # set up all the tk string variables
        self.jumpclass_id = tk.StringVar(self, f'{self.jumpclass.id}')
        self.jumpclass_name = tk.StringVar(self, f'{self.jumpclass.name}')
        self.article = tk.StringVar(self, f'{self.jumpclass.article}')
        self.arena_id = tk.StringVar(self, f'{self.jumpclass.arena.id}')
        self.jumpclass_description = tk.StringVar(self, f'{self.jumpclass.description}')
        self.jumpclass_height = tk.IntVar(self, f'{self.jumpclass.height}')
        self.jumpclass_judge = tk.StringVar(self, f'{self.jumpclass.judge}')
        self.jumpclass_cd = tk.StringVar(self, f'{self.jumpclass.cd}')
        self.jumpclass_places = tk.IntVar(self, self.jumpclass.places)

        # set up the corresponding widgets
        jumpclass_id_lbl = ttk.Label(self, text='Class ID: ')
        self.jumpclass_id_entry = ttk.Combobox(self, textvariable=self.jumpclass_id)
        jumpclass_name_lbl = ttk.Label(self, text='Class Name: ')
        jumpclass_name_entry = ttk.Entry(self, textvariable=self.jumpclass_name)
        arena_id_lbl = ttk.Label(self, text='Arena ID: ')
        self.arena_id_entry = ttk.Combobox(self, textvariable=self.arena_id)
        jumpclass_description_lbl = ttk.Label(self, text='Description: ')
        jumpclass_description_entry = ttk.Entry(self, textvariable=self.jumpclass_description)
        jumpclass_height_lbl = ttk.Label(self, text='Height (cm)')
        jumpclass_height_entry = ttk.Entry(self, textvariable=self.jumpclass_height)
        jumpclass_judge_lbl = ttk.Label(self, text='Judge: ')
        jumpclass_judge_entry = ttk.Entry(self, textvariable=self.jumpclass_judge)
        jumpclass_cd_lbl = ttk.Label(self, text='Course Designer: ')
        jumpclass_cd_entry = ttk.Entry(self, textvariable=self.jumpclass_cd)
        jumpclass_places_lbl = ttk.Label(self, text='Places')
        jumpclass_places_entry = ttk.Entry(self, textvariable=self.jumpclass_places)
        done_btn = ttk.Button(self, text='Done', default='active', command=self.set_jumpclass)
        cancel_btn = ttk.Button(self, text='Cancel', command=self.destroy)

        #set the combo boxes
        arena_ids = [a.id for a in self.master.event.arenas]
        self.arena_id_entry.configure(values=arena_ids)
        jumpclass_ids = [j.id for j in self.master.event.get_jumpclasses()]
        self.jumpclass_id_entry.configure(values=jumpclass_ids)
        self.jumpclass_id_entry.bind("<<ComboboxSelected>>", self.jumpclass_selected)

        # grid it up
        jumpclass_id_lbl.grid(row=1, column=1)
        self.jumpclass_id_entry.grid(row=1, column=2)
        arena_id_lbl.grid(row=1, column=3)
        self.arena_id_entry.grid(row=1, column=4)
        jumpclass_name_lbl.grid(row=2, column=1)
        jumpclass_name_entry.grid(row=2, column=2, columnspan=3, sticky='EW')
        jumpclass_description_lbl.grid(row=3, column=1)
        jumpclass_description_entry.grid(row=3, column=2, columnspan=3, sticky='EW')
        jumpclass_height_lbl.grid(row=4, column=1)
        jumpclass_height_entry.grid(row=4, column=2)
        jumpclass_places_lbl.grid(row=4, column=3)
        jumpclass_places_entry.grid(row=4, column=4)
        jumpclass_judge_lbl.grid(row=5, column=1)
        jumpclass_judge_entry.grid(row=5, column=2)
        jumpclass_cd_lbl.grid(row=5, column=3)
        jumpclass_cd_entry.grid(row=5, column=4)
        done_btn.grid(row=6, column=2)
        cancel_btn.grid(row=6, column=3)

        # self.bind('<FocusIn>', self.update)
        # self.update()

    def update(self):
        self.jumpclass_id.set(self.jumpclass.id)
        self.jumpclass_name.set(self.jumpclass.name)
        self.article.set(self.jumpclass.article)
        self.arena_id.set(self.jumpclass.arena.id)
        self.jumpclass_description.set(self.jumpclass.description)
        self.jumpclass_height.set(self.jumpclass.height)
        self.jumpclass_judge.set(self.jumpclass.judge)
        self.jumpclass_cd.set(self.jumpclass.cd)
        self.jumpclass_places.set(self.jumpclass.places)

    def jumpclass_selected(self, eventObject):
        '''Upates dialog field after selection made in jumpclass combo box.
        '''
        for j in self.master.event.get_jumpclasses():
            if j.id == self.jumpclass_id.get():
                self.jumpclass = j
                

        self.update()


        # arena_ids = [a.id for a in self.master.event.arenas]
        # self.arena_id_entry.configure(values=arena_ids)
        # jumpclass_ids = [j.id for j in self.master.event.get_jumpclasses()]
        # self.jumpclass_id_entry.configure(values=jumpclass_ids)

    def set_jumpclass(self):
        self.jumpclass.arena = self.master.event.get_arena_by_public_id(
            self.arena_id.get()
        )

        for key, attribute in vars(self.jumpclass).items():
            for dlg_key, dlg_val in vars(self).items():
                
                if f'jumpclass_{key}' == dlg_key:
                    self.jumpclass.__setattr__(key, dlg_val.get())
                    
                    
        
        self.update()
        self.master.update()
        self.master.event.update()
        self.destroy()


            




        
