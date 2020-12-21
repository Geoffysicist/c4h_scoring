"""c4h_score.py - backend for C4HScore, a scoreboard for judging showjumping.
"""

import json
import yaml
import csv
import uuid

from datetime import date, datetime, timezone
from dataclasses import dataclass, field

INDENT = '  ' #indent used for output

class C4HEvent(object):
    '''Equestrian Event.

    Attributes:
        name (str): the event name
        details (str): other information about the event
        dates (list[date]): start and finish dates for the event
        arenas (list[_C4HArena]):
        jumpclasses (list[_C4HJumpClass]):
        riders (list[_C4HRider]):
        horses (list[_C4HHorse]):
        combos (list[_C4HCombo]):
        judges (list[_C4HJudge]):
        cds (list[C4HCD])
        rounds (list[C4HRound]):
        last_save (datetime): UTC date & time the event was last saved
        last_change (datetime): UTC date and time of last change in any data
        filename (str): the name of the event file. None for unsaved events
    '''

    def __init__(self, event_name):
        self.name = event_name
        self.details = ''
        self.dates = [date.today(),date.today()]
        self.arenas = []
        self.riders = []
        self.horses = []
        self.combos = []
        self.judges = []
        self.cds = []
        self.jumpclasses = []
        self.rounds = []
        self.last_save = datetime(1984,4,4, 13, tzinfo=timezone.utc)
        self.last_change = datetime.now(timezone.utc)
        self.filename = None

        # add default arena
        self.new_arena('1')

    def update(self):
        self.last_change = datetime.now(timezone.utc)
        return self.last_change

    def new_arena(self, arena_id, name=''):
        '''creates a new arena and appends it to the arena list.

        Args:
            arena_id (string):
            name (string):

        Returns:
            _C4HArena
        '''
        if self.get_arenas(id=arena_id):
            raise ValueError(f'Arena with id {arena_id} already exists')
        
        a = _C4HArena(arena_id, name)
        self.arenas.append(a)
        self.update()

        return a

    def get_arenas(self, **kwargs):
        '''Find rider matching kwargs.

        keyword args:
            id (str): public id
            name (string): 

        Returns:
            list[_C4HArena] list empty if no matches.
            List contains all arenas if no kwargs
        '''
        arenas = self.arenas
        for key, val in kwargs.items():
            arenas = [a for a in arenas if getattr(a,key) == val]
        
        return arenas
        
    def new_rider(self, surname=None, given_name=None):
        '''creates a new rider and appends it to the rider list.

        It seems odd to initialise these attribures with None but I want
        users to be able to enter some data if they don't know all of it.
        They may know the given name but not the surname or vice versa

        Args:
            surname (string): 
            given_name (string): 
            # ea_number (string): length must be 7 digits

        Returns:
            _C4HRider
        '''

        if self.get_riders(surname=surname, given_name=given_name):
            raise ValueError(f"Rider {surname} {given_name} already exists")

        r = _C4HRider(surname=surname, given_name=given_name)
        self.riders.append(r)
        self.update()

        return r
      
    def get_riders(self, **kwargs):
        '''Find rider matching kwargs.

        keyword args:
            surname (string)
            given_name (string): 
            ea_number (string):

        Returns:
            list[_C4HRider] list empty if no matches.
            List contains all riders if no kwargs
        '''
        riders = self.riders
        for key, val in kwargs.items():
            riders = [r for r in riders if getattr(r,key) == val]
        
        return riders

    def new_horse(self, name):
        '''creates a new horse and appends it to the _horses list.

        Args:
            name (string): 
            ea_number (int): length must be 8 digits

        Returns:
            _C4HHorse
        '''
        if self.get_horses(name=name):
            raise ValueError(f"Horse {name} already exists")

        h = _C4HHorse(name)
        self.horses.append(h)
        self.update()

        return h

    def get_horses(self, **kwargs):
        '''Find horse matching kwargs.

        keyword args:
            name (string):
            ea_number (string):

        Returns:
            list[_C4HHorse] list empty if no matches.
            List contains all horses if no kwargs
        '''
        horses = self.horses
        for key, val in kwargs.items():
            horses = [h for h in horses if getattr(h,key) == val]
        
        return horses

    def new_combo(self, rider, horse, id=''):
        '''creates a new combination and appends it to the combo list.

        Args:
            rider (_C4HRider): 
            horse (_C4HHorse):
            id (str):
        
        Returns:
            _C4HCombo
        '''
        if self.get_combos(rider=rider, horse=horse):
            raise ValueError(
                f"Combination {rider.surname}, {rider.given_name}: "
                f"{horse.name} already exists"
            )

        c = _C4HCombo(rider, horse, id)
        self.combos.append(c)
        self.update()

        return c

    def get_combos(self, **kwargs):
        '''Find horse matching kwargs.

        keyword args:
            name (string):
            ea_number (string):

        Returns:
            list[_C4HHorse] list empty if no matches.
            List contains all horses if no kwargs
        '''
        combos = self.combos
        for key, val in kwargs.items():
            combos = [c for c in combos if getattr(c,key) == val]
        
        return combos
    
    def new_judge(self):
        pass

    def get_judges(self):
        pass

    def new_cd(self):
        pass

    def get_cds(self):
        pass

    def new_jumpclass(self):
        pass

    def get_jumpclasses(self):
        pass
    #     '''Find jumpclass matching kwargs.

    #     keyword args:
    #         arena (_C4HArena):
    #         article (C4HArticle):
    #         cd (C4Hcd):
    #         description (str):
    #         height (str):
    #         id (str):
    #         judge (C4HJudge):
    #         name (str):
    #         places(int):
    #         rounds(int):
    #         jumpoffs (int):

    #     Returns:
    #         list[_C4HJumpClass] list empty if no matches.
    #     '''
    #     # jclasses = self.jumpclasses
    #     # for key, val in kwargs.items():
    #     #     jclasses = [jc for jc in jclasses if getattr(jc, key) == val]
    #     jclasses = []
    #     jclasses.extend([a.get_jumpclasses(**kwargs) for a in self.arenas])
    #     return jclasses

    def new_round(self):
        pass

    def get_rounds(self):
        pass

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

        # user may have changed the filename so...
        new_event.filename = fn
        return new_event

@dataclass
class _C4HJumpClass(object):
    '''A show jumping class.

    Attributes:
        id (str): an integer that may have a character appended eg. 8c 
        name (string):
        arena (_C4HArena):
        _ID (uuid): unique identifier
        description (string):
        article (EAArticle):
        height (int): the height in cm
        judge (string): judges name
        cd (string): course designer name
        places (int): the number of places awarded prizes
        rounds (list[_C4HRound]): rounds entered in this arenas
    '''
    def __init__(self, id, arena):

        self._ID = uuid.UUID()
        self.id = id
        self.arena = arena
        self.arena.jumpclasses.append(self)
        self.name = f'Class {self.id}'
        self.article = None
        self.description = ''
        self.height = 0
        self.judge = ''
        self.cd = ''
        self.places = 6
        self.rounds= []

@dataclass
class _C4HArena(object):
    '''An arena in the event which holds jumpclasses.

    Attributes:
        _ID (int): private id
        id (str): public id
        name (string):
        # event (C4HEvent): parent event
        jumpclasses (list):
    '''

    id: str
    name: str
    _ID: int = uuid.uuid1()

    def __post_init__(self):
        if not self.name: self.name = f'Arena {self.id}'

    
@dataclass
class _C4HRider(object):
    '''Rider details.

    Attributes:
        surname (string)
        given_name (string): 
        ea_number (string): This must 7 numerical digits
    '''
    surname: str
    given_name: str
    _ea_number: str = ''

    @property
    def ea_number(self):
        return self._ea_number

    @ea_number.setter
    def ea_number(self, ea_number):
        if ea_number.isnumeric() and (len(ea_number) == 7):
            self._ea_number = ea_number
        else:
            raise ValueError('Rider EA number should be a number 7 digits long')
        
        return self._ea_number

@dataclass
class _C4HHorse(object):
    '''Horse details.

    Attributes:
        name (string):
        ea_number (string): this must be 8 numerical digits
    '''
    # def __init__(self, name, ea_number):
    #     self.name = name
    name: str
    _ea_number: str = ''

    @property
    def ea_number(self):
        return self._ea_number

    @ea_number.setter
    def ea_number(self, ea_number):
        if ea_number.isnumeric() and (len(ea_number) == 8):
            self._ea_number = ea_number
        else:
            raise ValueError('Horse EA number should be a number 8 digits long')
        
        return self._ea_number

@dataclass
class _C4HCombo(object):
    '''Rider/horse combinations.

    Attributes:
        id (int): unique id for combination
        rider (_C4HRider):
        horse (_C4HHorse):
    '''

    # def __init__(self, rider, horse, id):
    rider: _C4HRider
    horse: _C4HHorse
    id: str
    _ID: uuid.uuid1 = uuid.uuid1()

class _C4HRound(object):
    '''Jump round and results.

    Attributes:
        jumpclass (_C4HJumpClass):
        round_type (str): identifies whether a round or jumpoff - r1, r2, jo1, jo2 etc
        combo (_C4HCombo):
        faults (list): Jump numbers followed by one or more letters indicating the fault type.
            rail: r, disobedience: d, displacement/knockdown: k, fall: f, elimination: e
        jump_pens (int):
        time (float): time 0.01 secs
        time_pens (int):
        notes (str): optional notes from the judge
    '''
    def __init__(self, jumpclass, round_type, combo):
        self.jumpclass = jumpclass
        self.round_type = round_type
        self.combo = combo
        self.faults = []
        self.jump_pens = 0
        self.time = 0
        self.time_pens = 0
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




