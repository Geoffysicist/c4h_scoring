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

from datetime import date

class EAArticle(object):
    '''EA/FEI article.

    Attributes:
        identifier (string): the paragraph.subparagraph number string
        description (string): word description of the competition
        alt_name: the deprecated silly names that everyone still uses
    '''

    def __init__(self, article_dict):
        '''init the article with a dictionary of the id, description and old name.
        '''
        self.id = article_dict['id']
        self.description = article_dict['description']
        self.alt_name = article_dict['old_name']

class C4HEvent(object):
    '''Equestrian Event.

    Attributes:
        name (string): the event name
        filename (str): the name of the event file. None for unsaved events
        arenas (list): C4HArena objects
        classes (list): C4HJumpClass objects
        riders (list): C4HRider objects
        horses (list): C4HHorse objects
        combos (list): C4HCombos rider, horse, id
        details (string): other information about the event
        dates (list): list of dates for the event
        indent (string): indent to use in yaml like output files. Default is 2 spaces
        changed (bool): indicates whether the event has been changed since last save
    '''

    def __init__(self, event_name):
        self.name = event_name
        self.filename = None
        self.arenas = []
        self.classes = []
        self.riders = []
        self.horses = []
        self.combos = []
        self.details = ''
        self.dates = [date.today(),date.today()]
        self.indent = '  '
        self.changed = True

        # add default arena
        self.new_arena('Arena1')


    def new_arena(self, arena_id):
        '''creates a new arena and appends it to the arena list.

        Args:
            arena_id (string): the name of the arena to check/create

        Returns:
            C4HArena
        '''
        for a in self.arenas:
            if a.id == arena_id:
                raise ValueError(f"Arena with id {arena_id} already exists")

        a = C4HArena(arena_id, self)
        self.arenas.append(a)
        return a

    def get_arena(self, arena_id):
        '''returns the arena with arena_id.

        Args:
            arena_id (string): the name of the arena to find

        Returns:
            C4HArena or None if not found
        '''

        this_arena = None
        
        for a in self.arenas:
            if a.id == arena_id:
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

        for c in self.classes:
            if c.id == class_id:
                raise ValueError('Class with id {} already exists'.format(class_id))

        if not arena: arena = self.arenas[0]        
        c = C4HJumpClass(class_id, arena=arena)
        self.classes.append(c)
        return c

    def get_class(self, class_id):
        '''returns the class with class_id.

        Args:
            class_id (string): the name of the class to find

        Returns:
            C4HJumpclass or False if not found
        '''
        this_class = False
        
        for c in self.classes:
            if c.id == class_id:
                this_class = c
        
        return this_class        

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
        for r in self.riders:
            if ((r.surname == surname) and (r.given_name == given_name)):
                raise ValueError(f"Rider {surname} {given_name} already exists")

        r = C4HRider(surname=surname, given_name=given_name, ea_number=ea_number)
        self.riders.append(r)
        return r
      
    def get_rider(self, surname, given_name):
        '''returns the C4HRider matching surname and given_name else None if rider doesn't exist.
        '''
        for r in self.riders:
            if (r.surname == surname and r.given_name == given_name):
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
        for h in self.horses:
            if h.name == name:
                raise ValueError(f"Horse {name} already exists")

        h = C4HHorse(name, ea_number=ea_number)
        self.horses.append(h)
        return h

    def get_horse(self, name):
        '''returns the C4HHorse matching name else None if horse doesn't exist.
        '''
        for h in self.horses:
            if (h.name == name):
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
        for c in self.combos:
            if c.id == id:
                raise ValueError(f"Combo ID {id} already exists")

        c = C4HCombo(id, rider, horse)
        self.combos.append(c)
        return c

    def get_combo(self, id):
        '''returns the C4HCombo with id == id else None if it doesn't exist.
        '''
        for c in self.combos:
            if c.id == id: return c

        return None

    def event_save(self):
        with open(self.filename, 'w') as out_file:
            out_file.write('--- # C4H Event Details\n')
            yaml.dump(self, out_file)

        self.changed = False

    def event_save_as(self, fn):
        with open(fn, 'w') as out_file:
            out_file.write('--- # C4H Event Details\n')
            yaml.dump(self, out_file)
        
        self.filename = fn
        self.changed = False

    def event_open(self, fn):
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
        id (string):
        event (C4HEvent):
    '''

    def __init__(self, arena_id, event):
        self.id = arena_id
        self.event = event

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
        id (string):
        name (string):
        arena (C4HArena):
        description (string):
        article (EAArticle):
        height (int): the height in cm
        times (list of ints): the times allowed for each phase
        judge (string): judges name
        cd (string): course designer name
        places (int): the number of places awarded prizes
        combinations (list): list of the horse/rider combinations entered
    '''

    def __init__(self, class_id, arena=None, places=6):
        self.id = class_id
        self.name = None
        self.article = None
        self.arena = arena
        self.description = None
        self.height = None
        self.times = []
        self.judge = None
        self.cd = None
        self.places = places
        self.combos = []

    def get_combo(self, id):
        '''returns the C4HCombo with id == id else None if it doesn't exist.
        '''
        for c in self.combos:
            if c.id == id: return c

        return None

class C4HCombo(object):
    '''Rider/horse combinations.

    Attributes:
        id (int): unique id for combination
        rider (C4HRider):
        horse (C4HHorse):
    '''

    def __init__(self, id, rider, horse):
        self.id = id
        self.rider = rider
        self.horse= horse

class C4HRider(object):
    '''Rider details.

    Attributes:
        surname (string)
        given_name (string): This must n digits
        ea_number (int):
    '''
    def __init__(self, surname, given_name, ea_number):
        self.surname = surname
        self.given_name = given_name

        if ea_number:
            if ea_number.isnumeric() and (len(ea_number) == 7):
                self.ea_number = ea_number
            else:
                raise ValueError('Rider EA number should be a number 7 digits long')

class C4HHorse(object):
    '''Horse details.

    Attributes:
        _name (string):
        _ea_number (int): this must be n digits
    '''
    def __init__(self, name, ea_number):
        self.name = name

        if ea_number:
            if ea_number.isnumeric() and (len(ea_number) == 8):
                self.ea_number = ea_number
            else:
                raise ValueError('Rider EA number should be a number 8 digits long')

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
                jumpclass.combos.append(combo)

    return event

if __name__ == "__main__":
    ea_articles = []

    #Read the EA articles json to a dictionary then objects
    with open('C4HScore/ea_articles.json', 'r') as articles_json:
        ea_art_dict = json.load(articles_json)

    ea_art_dict = ea_art_dict['ea_articles']

    for a in ea_art_dict:
        ea_articles.append(EAArticle(a))

    #now the event stuff



