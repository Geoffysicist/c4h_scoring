"""c4h_score - A scoreboard for judging showjumping.


"""

import json
import yaml
import csv

from datetime import date, datetime, timezone

class C4HEvent(object):
    '''Equestrian Event.

    Attributes:
        name (string): the event name
        filename (str): the name of the event file. None for unsaved events
        arenas (list): C4HArena objects
        jumpclasses (list): C4HJumpClass objects - now arenas
        riders (list): C4HRider objects
        horses (list): C4HHorse objects
        combos (list): C4HCombos rider, horse, id
        details (string): other information about the event
        dates (list): list of dates for the event
        indent (string): indent to use in yaml like output files. Default is 2 spaces
        # changed (bool): indicates whether the event has been changed since last save
        last_save (datetime): UTC date & time the event was last saved
        last_change (datetime): UTC date and time of last change in any data
        # timezone (timeezone): best to leave as UTC if storing on servers etc
    '''

    def __init__(self, event_name):
        self.name = event_name
        self.filename = None
        self.arenas = []
        # self.jumpclasses = []
        self.riders = []
        self.horses = []
        self.combos = []
        self.details = ''
        self.dates = [date.today(),date.today()]
        self.indent = '  '
        # self.timezone = timezone.utc
        self.last_save = datetime(1984,4,4, 13, tzinfo=timezone.utc)
        self.last_change = datetime.now(timezone.utc)
        # self.changed = True

        # add default arena
        self.new_arena('1','Arena 1')

    def update(self):
        self.last_change = datetime.now(timezone.utc)

    def new_arena(self, arena_id, name):
        '''creates a new arena and appends it to the arena list.

        Args:
            arena_id (string): the name of the arena to check/create
            name (string):

        Returns:
            C4HArena
        '''
        for a in self.arenas:
            if a.id == arena_id:
                raise ValueError(f"Arena with id {arena_id} already exists")

        a = C4HArena(arena_id, name, self)

        self.arenas.append(a)
        self.update()

        return a

    def get_arena(self, arena_ID):
        '''returns the arena with unique private arena _ID.

        Args:
            arena_ID (int):

        Returns:
            C4HArena or None if not found
        '''
        for a in self.arenas:
            if a._ID == arena_ID:
                return a
        
        return None        

    def get_arena_by_public_id(self, arena_id):
        '''returns the arena with public arena_id.

        Args:
            arena_id (str):

        Returns:
            C4HArena or None if not found
        '''
        for a in self.arenas:
            if a.id == arena_id:
                return a
        
        return None        

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
        self.update()

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
        self.update()

        return h

    def get_horse(self, name):
        '''returns the C4HHorse matching name else None if horse doesn't exist.
        '''
        for h in self.horses:
            if (h.name == name):
                return h

        return None

    def get_jumpclasses(self):
        '''
        Returns:
            list of C4HJumpClass objects
        '''
        jclasses = []
        for a in self.arenas:
            for j in a.jumpclasses:
                jclasses.append(j)
        
        return jclasses

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
        self.update()
        return c

    def get_combo(self, id):
        '''returns the C4HCombo with id == id else None if it doesn't exist.
        '''
        for c in self.combos:
            if c.id == id: return c

        return None

    def event_save(self):
        """Dumps the event to a yaml like file."""
        # timestamp first so timestamp gets saved
        self.last_save = datetime.now(timezone.utc)

        with open(self.filename, 'w') as out_file:
            out_file.write(f'--- # {self.name} C4HScore\n')
            yaml.dump(self, out_file)

    def event_save_as(self, fn):       
        self.filename = fn
        self.event_save()

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
    '''An arena in the event which holds jumpclasses.

    Attributes:
        _ID (int): private id
        id (str): public id
        name (string):
        event (C4HEvent): parent event
        jumpclasses (list):
    '''

    def __init__(self, arena_id, name, event):
        self.name = name
        self.event = event
        self.jumpclasses = []
        self.id = arena_id
        next_id = 1
        for a in self.event.arenas:
            if a._ID >= next_id:
                next_id = next_id + 1

        self._ID = next_id

    def new_jumpclass(self):
        '''creates a new jumpclass if it doesn't exist.

        checks to see if a class with name class_id exists
        if it exists a valueerror is raised
        if not a new class is created and added to the class list then returned

        Args:
            class_id (string): the id of the class to check/create

        Raises:
            ValueError: if a class with that class_id already exists
        '''

        # TODO make sure unique id

        j = C4HJumpClass(self)
        self.jumpclasses.append(j)
        return j

    def get_jumpclass(self, class_id):
        '''returns the class with class_id.

        Args:
            class_id (string): the name of the class to find

        Returns:
            C4HJumpclass or False if not found
        '''
        this_class = False
        
        for j in self.jumpclasses:
            if j.id == class_id:
                this_class = j
        
        return this_class
    
class C4HJumpClass(object):
    '''A show jumping class.

    Attributes:
        _ID (int): unique identifier
        id (str): an integer that may have a character appended eg. 8c 
        name (string):
        arena (C4HArena):
        description (string):
        article (EAArticle):
        height (int): the height in cm
        # times (list of ints): the times allowed for each phase
        judge (string): judges name
        cd (string): course designer name
        places (int): the number of places awarded prizes
        # combinations (list): list of the horse/rider combinations entered
        rounds (list of C4HRounds): rounds entered in this arenas
    '''

    def __init__(self, arena):

        self.arena = arena
        self.arena.jumpclasses.append(self)
        #getunique ID
        self._ID = 0 #need a value here to avoid attribute error if first jumpclass
        self._ID = max([jc._ID for jc in self.arena.event.get_jumpclasses()]) + 1
        # self._ID = jc._ID +1 for jc in arena if self._ID < jc._ID
        # for jc in arena.jumpclasses:
        #     if self._ID <= jc._ID:
        #         self._ID = jc._ID + 1
        self.id = str(self._ID)
        self.name = f'Class {self.id}'
        self.article = None
        self.description = ''
        self.height = None
        # self.times = []
        self.judge = ''
        self.cd = ''
        self.places = 6
        # self.combos = []
        self.rounds= []

    def get_combo(self, id):
        '''returns the C4HCombo with id == id else None if it doesn't exist.
        '''
        for c in self.combos:
            if c.id == id: return c

        return None

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
        name (string):
        ea_number (int): this must be n digits
    '''
    def __init__(self, name, ea_number):
        self.name = name

        if ea_number:
            if ea_number.isnumeric() and (len(ea_number) == 8):
                self.ea_number = ea_number
            else:
                raise ValueError('Rider EA number should be a number 8 digits long')

class C4HCombo(object):
    '''Rider/horse combinations.

    Attributes:
        id (int): unique id for combination
        rider (C4HRider):
        horse (C4HHorse):
        rounds (C4HRound)
    '''

    def __init__(self, id, rider, horse):
        self.id = id
        self.rider = rider
        self.horse= horse

class C4HRound(object):
    '''Jump round and results.

    Attributes:
        jumpclass (C4HJumpClass):
        round_type (str): identifies whether a round or jumpoff - r1, r2, jo1, jo2 etc
        combo (C4HCombo):
        faults (list): Jump numbers followed by one or more letters indicating the fault type.
            rail: r, disobedience: d, displacement/knockdown: k, fall: f, elimination: e
        jump_pens (int):
        time (float): time in secs
        time_pens (int):
        notes (str): optional notes from the judge
    '''
    def __init__(self, jumpclass, round_type, combo):
        self.jumpclass = jumpclass
        self.round_type = round_type
        self.combo = combo
        self.faults = []
        self.jump_pens = None
        self.time = None
        self.time_pens = None
        self.notes = ''

class C4HArticle(object):
    '''EA/FEI article.

    Attributes:
        id (string): Article number
        descrption (string): Short description of the class type
        alt_name (string): Alternative name for the class
        round_num (int): Number of rounds.
        round_table (string): Table for the round.

        identifier (string): the paragraph.subparagraph number string
        description (string): word description of the competition
        alt_name: the deprecated silly names that everyone still uses
    '''

    def __init__(self, id):
        '''init the article with a dictionary of the id, description and old name.
        '''
        self.rules = 'EA'
        self._id = id
        self.description = ''
        self.alt_name = None
        self.round_num = 1
        self.round_table = 'A'
        self.round_against_clock = True
        self.round_combinations = 'allowed'
        self.jo_num = 0
        self.jo_table = ''
        self.jo_jumps = ''
        self.jo_combinations = ''
        self.sub_articles = []

    def articles_save(self, fn=None):
        if not fn: fn = f'{self.rules}_articles.c4ha'

        with open(fn, 'w') as out_file:
            out_file.write(f'--- # {self.rules} Articles\n')
            yaml.dump(self, out_file)

    # def articles_save_as(self, fn):       
    #     self.filename = fn
    #     self.event_save()

    def articles_open(self, fn):
        ''' Creates an event from a c4hs yaml file.
        
        Returns:
            C4HEvent
        '''
        with open(fn, 'r') as in_file:
            new_event = yaml.load(in_file, Loader=yaml.FullLoader)
            print(type(new_event))

        return new_event
    

# def read_csv_nominate(fn, event_name='New Event'):
#     '''Loads event data from a nominate like csv file

#     Args:
#         fn (string): path and filename
#         event_name (string): the name of the event

#     Returns:
#         C4HEvent
#     '''

#     # event_data = pandas.read_csv(fn)
#     with open(fn, newline='') as in_file:
#         in_data = csv.DictReader(in_file)
#         event = C4HEvent(event_name)
#         for entry in in_data:
#             rider = entry['Rider'].split(' ')
#             given_name = rider[0]
#             surname = ' '.join(rider[1:])
#             horse = entry['Horse']
#             id = entry['ID']
#             jumpclass = entry['Class']
#             if not event.get_rider(surname, given_name):
#                 rider = event.new_rider(surname=surname, given_name=given_name)
#             else:
#                 rider = event.get_rider(surname, given_name)
#             if not event.get_horse(horse):
#                 horse = event.new_horse(horse)
#             else:
#                 horse = event.get_horse(horse)
            
#             if not event.get_combo(id):
#                 combo = event.new_combo(id, rider=rider, horse=horse)
#             else:
#                 combo = event.get_combo(id)
            
#             if not event.get_class(jumpclass):
#                 jumpclass = event.new_class(jumpclass)
#             else:
#                 jumpclass = event.get_class(jumpclass)

#             if not jumpclass.get_combo(combo):
#                 jumpclass.combos.append(combo)

#     return event

if __name__ == "__main__":
    pass
    #now the event stuff



