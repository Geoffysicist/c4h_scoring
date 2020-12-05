"""c4h_scoreboard - A scoreboard for judging showjumping.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = SampleClass()
  
  bar = foo.public_method(required_variable, optional_variable=42)
"""

import json
import yaml
import csv
import tkinter as tk
import tkcalendar as cal
import datetime as dt
import ctypes

# import pandas
from tkinter import ttk, filedialog, messagebox
from datetime import date
from functools import partial
# from ttkthemes import ThemedTk

# makes dpi aware so tkinter text isnt blurry
ctypes.windll.shcore.SetProcessDpiAwareness(1)



class EAArticle(object):
    '''EA/FEI article.

    Attributes:
        _identifier (string): the paragraph.subparagraph number string
        _description (string): word description of the competition
        _old_name: the deprecated silly names that everyone still uses
    '''

    def __init__(self, article_dict):
        '''init the article with a dictionary of the id, description and old name.
        '''
        self._id = article_dict['id']
        self._description = article_dict['description']
        self._old_name = article_dict['old_name']

    def get_id(self):
        return self._id

    def get_description(self):
        return self._description

    def get_old_name(self):
        return self._old_name

class C4HEvent(object):
    '''Equestrian Event.

    Attributes:
        _name (string): the event name
        filename (str): the name of the event file. None for unsaved events
        _arenas (list): C4HArena objects
        _classes (list): C4HJumpClass objects
        _riders (list): C4HRider objects
        _horses (list): C4HHorse objects
        _combos (list): C4HCombos rider, horse, id
        _details (string): other information about the event
        dates (list): list of dates for the event
        _indent (string): indent to use in yaml like output files. Default is 2 spaces
        changed (bool): indicates whether the event has been changed since last save
    '''

    def __init__(self, event_name):
        self._name = event_name
        self.filename = None
        self._arenas = []
        self._classes = []
        self._riders = []
        self._horses = []
        self._combos = []
        self._details = ''
        self.dates = [date.today(),date.today()]
        self._indent = '  '
        self.changed = True

        # add default arena
        self.new_arena('Arena1')

    def get_name(self):
        ''' returns the name of the event.'''
        return self._name

    def set_name(self, event_name):
        '''Sets the name of the event

        Args:
            event_name (string)
        '''
        if type(event_name) == str:
            self._name = event_name
        else:
            raise TypeError(f"event_name {event_name} is not a string")

    def set_dates(self, dates):
        ''' Sets the start and end dates of the event

        Args:
            dates (list): list of datetimes [start, end]

        '''
        self.dates=dates

    def get_dates(self):
        return self.dates

    def new_arena(self, arena_id):
        '''creates a new arena and appends it to the arena list.

        Args:
            arena_id (string): the name of the arena to check/create

        Returns:
            C4HArena
        '''
        for a in self._arenas:
            if a.get_id() == arena_id:
                raise ValueError(f"Arena with id {arena_id} already exists")

        a = C4HArena(arena_id, self)
        self._arenas.append(a)
        return a

    def get_arenas(self):
        '''returns the list of arenas in the event'''
        return self._arenas
    
    def get_arena(self, arena_id):
        '''returns the arena with arena_id.

        Args:
            arena_id (string): the name of the arena to find

        Returns:
            C4HArena or None if not found
        '''

        this_arena = None
        
        for a in self._arenas:
            if a.get_id() == arena_id:
                this_arena = a
        
        return this_arena        

    def new_class(self, class_id, arena=None):
        '''creates a new class if it doesn't exist.

        checks to see if a class with name class_id exists
        if it exists a valueerror is raised
        if not a new class is created and added to the class list then returned

        Args:
            class_id (string): the id of the class to check/create

        Raises:
            ValueError: if a class with that class_id already exists
        '''

        for c in self._classes:
            if c.get_id() == class_id:
                raise ValueError('Class with id {} already exists'.format(class_id))

        if not arena: arena = self._arenas[0]        
        c = C4HJumpClass(class_id, arena=arena)
        self._classes.append(c)
        return c

    def get_class(self, class_id):
        '''returns the class with class_id.

        Args:
            class_id (string): the name of the class to find

        Returns:
            C4HJumpclass or False if not found
        '''
        this_class = False
        
        for c in self._classes:
            if c.get_id() == class_id:
                this_class = c
        
        return this_class        

    def get_classes(self):
        '''returns the list of classes in the event'''
        return self._classes

    def new_rider(self, surname=None, given_name=None, ea_number=None):
        '''creates a new rider and appends it to the rider list.

        It seems odd to initialise these attribures with None but I want
        users to be able to enter some dataif they don't know all of it.
        They may know the given name but not the surname or vice versa

        Args:
            surname (string): 
            given_name (string): 
            ea_number (string): length must be 7 digits

        Returns:
            C4HRider
        '''
        for r in self._riders:
            if ((r.get_surname() == surname) and (r.get_given_name() == given_name)):
                raise ValueError(f"Rider {surname} {given_name} already exists")

        r = C4HRider(surname=surname, given_name=given_name, ea_number=ea_number)
        self._riders.append(r)
        return r

    def get_riders(self):
        return self._riders
        
    def get_rider(self, surname, given_name):
        '''returns the C4HRider matching surname and given_name else None if rider doesn't exist.
        '''
        for r in self._riders:
            if (r.get_surname() == surname and r.get_given_name() == given_name):
                return r

        return None

    def new_horse(self, name, ea_number=None):
        '''creates a new horse and appends it to the _horses list.

        Args:
            name (string): 
            ea_number (int): length must be 8 digits

        Returns:
            C4HHorse
        '''
        for h in self._horses:
            if h.get_name() == name:
                raise ValueError(f"Horse {name} already exists")

        h = C4HHorse(name, ea_number=ea_number)
        self._horses.append(h)
        return h

    def get_horse(self, name):
        '''returns the C4HHorse matching name else None if horse doesn't exist.
        '''
        for h in self._horses:
            if (h.get_name() == name):
                return h

        return None

    def new_combo(self, id, rider=None, horse=None):
        '''creates a new rider and appends it to the _combos list.

        Args:
            id (str): unique id
            rider (C4HRider):
            horse(C4HHorse)

        Returns:
            C4HCombo
        '''
        for c in self._combos:
            if c.get_id() == id:
                raise ValueError(f"Combo ID {id} already exists")

        c = C4HCombo(id, rider, horse)
        self._combos.append(c)
        return c

    def get_combo(self, id):
        '''returns the C4HCombo with id == id else None if it doesn't exist.
        '''
        for c in self._combos:
            if c.get_id() == id: return c

        return None

    def get_combos(self):
        '''Returns a list of C4HCombo
        '''
        return self._combos

    def write_c4hs(self, fn):
        '''Write event info to a yaml like file.

        File has *.c4hs suffix
        Hierachy is:
            Event
                Date
                    Arena
                        Class
                            Combos
                                id
                                round
            Combo
                id
                rider
                    surname
                    given_name
                horse
        '''

        i = self._indent
        with open(fn, 'w') as out_file:
            out_file.write(f'--- # {self.get_name()}\n')
            out_file.write(f'Event details:\n')
            
            for d in self.dates:
                out_file.write(f'{i}date: {d}\n')
                for a in self._arenas:
                    out_file.write(f'{i}{i}arena: {a.get_id()}\n')
                    for j in a.get_classes():
                        out_file.write(f'{i}{i}{i}class: {j.get_id()}\n')
                        for c in j.get_combos():
                            out_file.write(f'{i}{i}{i}{i}entry: {c.get_id()}\n')
            out_file.write(f'\nCombinations:\n')
            for c in self._combos:
                out_file.write(f'{i}entry: {c.get_id()}\n')
                out_file.write(f'{i}{i}rider:\n')
                r = c.get_rider()
                out_file.write(f'{i}{i}{i}surname: {r.get_surname()}\n')
                out_file.write(f'{i}{i}{i}given name: {r.get_given_name()}\n')
                out_file.write(f'{i}{i}horse: {c.get_horse().get_name()}\n')

    def yaml_dump(self, fn):
        '''Write event info to a yaml like file.

        File has *.c4hs suffix
        Hierachy is:
            Event
                Date
                    Arena
                        Class
                            Combos
                                id
                                round
            Combo
                id
                rider
                    surname
                    given_name
                horse
        '''

        with open(fn, 'w') as out_file:
            out_file.write('--- # Event Details\n')
            yaml.dump(self, out_file)

            # for c in self.get_combos():
            #     out_file.write(f'\n--- # Combo {c.get_id()} Details\n')
            #     yaml.dump(c, out_file)

    def file_save(self):
        with open(self.filename, 'w') as out_file:
            out_file.write('--- # C4H Event Details\n')
            yaml.dump(self, out_file)

        self.changed = False

    def file_save_as(self, fn):
        with open(fn, 'w') as out_file:
            out_file.write('--- # C4H Event Details\n')
            yaml.dump(self, out_file)
        
        self.filename = fn
        self.changed = False

    def file_open(self, fn):
        ''' Creates an event from a c4hs yaml file.
        
        Returns:
            C4HEvent
        '''
        with open(fn, 'r') as in_file:
            new_event = yaml.load(in_file, Loader=yaml.FullLoader)
            print(type(new_event))

        return new_event



class C4HArena(object):
    '''An arena in the event which holds classes.

    Attributes:
        _id (string):
        event (C4HEvent):
    '''

    def __init__(self, arena_id, event):
        self._id = arena_id
        self.event = event

    def get_id(self):
        return self._id

    def get_classes(self):
        '''returns the classes in this arena.
        '''
        classes = []
        for c in self.event.get_classes():
            if c.get_arena() == self:
                classes.append(c)

        return classes
    
class C4HJumpClass(object):
    '''A show jumping class.

    Attributes:
        _id (string):
        _name (string):
        _arena (C4HArena):
        _description (string):
        _article (EAArticle):
        _height (int): the height in cm
        _times (list of ints): the times allowed for each phase
        _judge (string): judges name
        _cd (string): course designer name
        _places (int): the number of places awarded prizes
        _combinations (list): list of the horse/rider combinations entered
    '''

    def __init__(self, class_id, arena=None, places=6):
        self._id = class_id
        self._name = None
        self._article = None
        self._arena = arena
        self._description = None
        self._height = None
        self._times = []
        self._judge = None
        self._cd = None
        self._places = places
        self._combos = []

    def get_id(self):
        return self._id

    def get_arena(self):
        return self._arena
    
    def set_arena(self, arena):
        '''sets the arena of the class.

        Args:
            arena_id (C4HArena):

        Raises:
            TypeError: if arena is not type C4HArena
        '''
        if type(arena) == C4HArena:
            self._arena = arena
        else:
            raise TypeError(f"Arg {arena} is an object of type {type(arena)} should be type C4HArena")

    def set_places(self, places):
        self._places = places
    
    def get_places(self):
        return self._places

    def get_combos(self):
        '''Returns a list of C4HCombo
        '''
        return self._combos

    def get_combo(self, id):
        '''returns the C4HCombo with id == id else None if it doesn't exist.
        '''
        for c in self._combos:
            if c.get_id() == id: return c

        return None

    def add_combo(self, combo):
        '''Adds a C4HCombo to the class.
        '''
        for c in self._combos:
            if c == combo:
                raise ValueError(f"Combination {c.get_id()} already in class")
        
        self._combos.append(combo)

class C4HCombo(object):
    '''Rider/horse combinations.

    Attributes:
        _id (int): unique id for combination
        _rider (C4HRider):
        _horse (C4HHorse):
    '''

    def __init__(self, id, rider, horse):
        self._id = id
        self._rider = rider
        self._horse= horse

    def get_id(self):
        return self._id

    def get_rider(self):
        return self._rider

    def get_horse(self):
        return self._horse

class C4HRider(object):
    '''Rider details.

    Attributes:
        _surname (string)
        _given_name (string): This must n digits
        _ea_number (int):
    '''
    def __init__(self, surname, given_name, ea_number):
        self._surname = surname
        self._given_name = given_name

        if ea_number:
            if ea_number.isnumeric() and (len(ea_number) == 7):
                self._ea_number = ea_number
            else:
                raise ValueError('Rider EA number should be a number 7 digits long')

    def get_surname(self):
        return self._surname

    def get_given_name(self):
        return self._given_name

    def get_ea_number(self):
        return self._ea_number

class C4HHorse(object):
    '''Horse details.

    Attributes:
        _name (string):
        _ea_number (int): this must be n digits
    '''
    def __init__(self, name, ea_number):
        self._name = name

        if ea_number:
            if ea_number.isnumeric() and (len(ea_number) == 8):
                self._ea_number = ea_number
            else:
                raise ValueError('Rider EA number should be a number 8 digits long')


    def get_name(self):
        return self._name

    def get_ea_number(self):
        return self._ea_number

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
        self._title = 'Courses4Horses Score'
        self._master = master
        self._master.title(self._title)
        self._favicon = tk.PhotoImage(file='assets/courses4horses_logo_bare.png')
        self._master.iconphoto(False, self._favicon)
        self._master.geometry('1600x1200')
        self._mainframe = ttk.Notebook(self._master)
        self._mainframe.grid(row=0, column=0, sticky="nsew")
        self._master.grid_rowconfigure(0, weight=1)
        self._master.grid_columnconfigure(0, weight=1)
        
        # set the main menu
        self.menubar = tk.Menu(self._master)

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
        self.eventmenu.add_command(label="Exit", command=self._master.quit)   
        self.menubar.add_cascade(label="Event", menu=self.eventmenu)

        # the class menu
        self.classmenu = tk.Menu(self.menubar, tearoff=0)
        self.classmenu.add_command(label="New", command=self.new_class)
        self.classmenu.add_command(label="Open", command=self.open_class)
        self.classmenu.add_command(label="Edit", command=self.edit_class)


        self._master.config(menu=self.menubar)

        self.update()
    
    
    # eventmenu.add_command(label="Open", command=donothing)
    # eventmenu.add_command(label="Save", command=donothing)


    # helpmenu = Menu(menubar, tearoff=0)
    # helpmenu.add_command(label="Help Index", command=donothing)
    # helpmenu.add_command(label="About...", command=donothing)

    def update(self):
        print(type(self.event))

        # enable/disable menu items depending on event state
        if not self.event:
            self.eventmenu.entryconfig("Save", state="disabled")
            self.eventmenu.entryconfig("Save As", state="disabled")
        else:    
            self.eventmenu.entryconfig("Save As", state="normal")
        
            if self.event.changed and self.event.filename:
                self.eventmenu.entryconfig("Save", state="normal")
            else:
                self.eventmenu.entryconfig("Save", state="disabled")


    def get_event(self):
        return self.event

    def event_new(self):
        ''' Opens a new event dialog.
        '''

        # TODO add warning if event has changed and not been saved
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

        dlg = tk.Toplevel(self._master)
        event_name = tk.StringVar(dlg,'New Event')

        # dlg.transient(self._master)
        # dlg.geometry('1600x1200')
        dlg.title(f'{self._title} - {event_name.get()}')
        dlg.iconphoto(False, self._favicon)

        event_lbl = ttk.Label(dlg, text='Event Name: ')
        event_name_entry = ttk.Entry(dlg, textvariable=event_name)

        # date_ = date.today()
        start_lbl = ttk.Label(dlg, text='Start Date: ')
        start_picker = cal.DateEntry(dlg, date=date.today(), locale='en_AU')
        # start_picker.selection_set(date.today())
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
            self.event.set_dates([start_picker.get_date(),end_picker.get_date()])
            print(self.event.get_dates())
            print(self.event.get_name())
            dlg.destroy()
            self.update()

        start_picker.bind('<<DateEntrySelected>>', check_dates)
        end_picker.bind('<<DateEntrySelected>>', check_dates)

        done_btn = ttk.Button(dlg, text='Done', default='active', command=set_event)
        cancel_btn = ttk.Button(dlg, text='Cancel', command=dlg.destroy)
        # done_btn = ttk.Button(dlg, text='Done', default='active', command=partial(print, event_name.get()))

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
        if self.event.changed:
            save_changes = messagebox.askyesnocancel(
                title="Are you sure you aren't making a big mistake?", 
                message=
                    'WARNING: You have unsaved changes! Do you want to save them?'
                )

            if save_changes == True:
                if self.event.filename:
                    self.file_save()
                else:
                    self.file_save_as()
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
            
            self.event = self.event.file_open(fn)
            self.event.changed = False

            self.update()
    
    def event_save(self):
        self.event.file_save()

    def event_save_as(self):
        '''Saves the event as a c4hs yaml file.

        Opens a filedialog and then passes fn to C4HEvent.save_as()
        '''
        fn = filedialog.asksaveasfilename(
            title="Save file as",
            filetypes=[('C4HScore files','*.c4hs')])

        #if cancel button wasn't clicked
        if fn:
            self.event.file_save_as(fn)

    def file_print(self):
        if self.event:
            print(self.event.get_name())
        else:
            print(type(self.event))

# functions
def new_event(name="New Event"):
    return C4HEvent(name)

def read_csv_nominate(fn, event_name='New Event'):
    '''Loads event data from a nominate like csv file

    Args:
        fn (string): path and filename
        event_name (string): the name of the event

    Returns:
        C4HEvent
    '''

    # event_data = pandas.read_csv(fn)
    with open(fn, newline='') as in_file:
        in_data = csv.DictReader(in_file)
        event = C4HEvent(event_name)
        for entry in in_data:
            rider = entry['Rider'].split(' ')
            given_name = rider[0]
            surname = ' '.join(rider[1:])
            horse = entry['Horse']
            id = entry['ID']
            jumpclass = entry['Class']
            if not event.get_rider(surname, given_name):
                rider = event.new_rider(surname=surname, given_name=given_name)
            else:
                rider = event.get_rider(surname, given_name)
            if not event.get_horse(horse):
                horse = event.new_horse(horse)
            else:
                horse = event.get_horse(horse)
            
            if not event.get_combo(id):
                combo = event.new_combo(id, rider=rider, horse=horse)
            else:
                combo = event.get_combo(id)
            
            if not event.get_class(jumpclass):
                jumpclass = event.new_class(jumpclass)
            else:
                jumpclass = event.get_class(jumpclass)

            if not jumpclass.get_combo(combo):
                jumpclass.add_combo(combo)

    return event

def load_yaml(fn):
    with open(fn, 'r') as in_file:
        this_event = yaml.load(in_file, Loader=yaml.FullLoader)
    
    return this_event



if __name__ == "__main__":
    ea_articles = []

    #Read the EA articles json to a dictionary then objects
    with open('C4HScore/ea_articles.json', 'r') as articles_json:
        ea_art_dict = json.load(articles_json)

    ea_art_dict = ea_art_dict['ea_articles']

    for a in ea_art_dict:
        ea_articles.append(EAArticle(a))

    #now the event stuff



