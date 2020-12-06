from c4h_score import C4HEvent
import tkinter as tk
import tkcalendar as cal
import ctypes

from tkinter import ttk, filedialog, messagebox
from datetime import date
# from functools import partial
# from ttkthemes import ThemedTk

# makes dpi aware so tkinter text isnt blurry
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class C4HScoreGUI(object):
    ''' Big container for the rest of the stuff.

    Attributes:
        event (C4HEvent): The big kahuna, or None before initialisation
    '''
    def __init__(self, master):
        ''' creates the master window and sets the main menubar.
        '''
        self.event = None

        # set up the gui
        self.title = 'Courses4Horses Score'
        self.master = master
        self.master.title(self.title)
        self.favicon = tk.PhotoImage(file='assets/courses4horses_logo_bare.png')
        self.master.iconphoto(False, self.favicon)
        self.master.geometry('1600x1200')
        self.mainframe = ttk.Notebook(self.master)
        self.mainframe.grid(row=0, column=0, sticky="nsew")
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
        self.eventmenu.add_command(label="Exit", command=self.master.quit)   
        self.menubar.add_cascade(label="Event", menu=self.eventmenu)

        # the class menu
        self.classmenu = tk.Menu(self.menubar, tearoff=0)
        self.classmenu.add_command(label="New", command=self.class_new)
        self.classmenu.add_command(label="Open", command=self.class_open)
        self.classmenu.add_command(label="Edit", command=self.class_edit)
        self.menubar.add_cascade(label="Class", menu=self.classmenu)

        self.master.config(menu=self.menubar)

        self.update()

    def update(self):
        print(type(self.event))

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
        
            if self.event.changed and self.event.filename:
                self.eventmenu.entryconfig("Save", state="normal")
            else:
                self.eventmenu.entryconfig("Save", state="disabled")

            if len(self.event.classes) == 0:
                self.classmenu.entryconfig("Edit", state="disabled")
            else:
                self.classmenu.entryconfig("Edit", state="normal")

    def event_new(self):
        ''' Opens a new event dialog.
        '''

        # warn if event has changed and not been saved
        if self.event:
            if self.event.changed:
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
                    return

        dlg = tk.Toplevel(self.master)
        event_name = tk.StringVar(dlg,'New Event')

        # dlg.transient(self.master)
        # dlg.geometry('1600x1200')
        dlg.title(f'{self.title} - {event_name.get()}')
        dlg.iconphoto(False, self.favicon)

        event_lbl = ttk.Label(dlg, text='Event Name: ')
        event_name_entry = ttk.Entry(dlg, textvariable=event_name)

        start_lbl = ttk.Label(dlg, text='Start Date: ')
        start_picker = cal.DateEntry(dlg, date=date.today(), locale='en_AU')
        end_lbl = ttk.Label(dlg, text='End Date: ')
        end_picker = cal.DateEntry(dlg, date=start_picker.get_date(), 
            mindate=start_picker.get_date(), locale='en_AU')
        
        # we need a local function to check start_date < end_date
        def check_dates(eventObject):
            if start_picker.get_date() > end_picker.get_date():
                end_picker.set_date(start_picker.get_date())
                end_picker.configure(mindate=start_picker.get_date())
 
        # local function to set event with local variables
        def set_event():
            self.event = C4HEvent(event_name.get())
            self.event.dates = [start_picker.get_date(),end_picker.get_date()]
            print(self.event.dates)
            print(self.event.name)
            dlg.destroy()
            self.update()

        start_picker.bind('<<DateEntrySelected>>', check_dates)
        end_picker.bind('<<DateEntrySelected>>', check_dates)

        done_btn = ttk.Button(dlg, text='Done', default='active', command=set_event)
        cancel_btn = ttk.Button(dlg, text='Cancel', command=dlg.destroy)

        event_lbl.grid(column=1, row=1, sticky='E')
        event_name_entry.grid(column=2, row=1, sticky='EW',columnspan=3)
        start_lbl.grid(column=1, row=2, sticky='E')
        start_picker.grid(column=2, row=2)
        end_lbl.grid(column=3, row=2, sticky='E')
        end_picker.grid(column=4, row=2)
        done_btn.grid(column=2, row=3)
        cancel_btn.grid(column=3, row=3)

        for c in dlg.winfo_children():
            c.grid_configure(padx=10, pady=10)
        start_lbl.grid_configure(padx=(100,10))
        end_picker.grid_configure(padx=(10,100))
        event_name_entry.focus()
        event_name_entry.select_range(0,len(event_name.get()))

        dlg.wait_visibility() # cant grab until visible
        dlg.grab_set() # keeps focus on this dialog

    def event_open(self):
        '''Opens an existing event from a c4hs file.

        Uses a filedialog to get filename and passes this to C4HEvent.open()
        Warns user if unsaved data
        '''
        if self.event and self.event.changed:
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
                return

        fn = filedialog.askopenfilename(
            title="Select file to open",
            filetypes=[('C4HScore files','*.c4hs')])

        #if cancel button wasn't clicked
        if fn:
            print(f'the filename is {fn}')
            # if no event yet need to create one
            if not self.event:
                self.event = C4HEvent('Temp Event')
            
            self.event = self.event.event_open(fn)
            self.event.changed = False

            self.update()

    def event_edit(self):
        print('event edit stubb')
    
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

    def class_new(self):
        print('class_new stub')

    def class_open(self):
        print('class_open stub')

    def class_edit(self):
        print('class_edit stub')

