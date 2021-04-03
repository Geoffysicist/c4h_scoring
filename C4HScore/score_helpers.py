""" score_helpers.py - dataclasses for C4HScore.

These are called by the main class C4HEvent.
They should be considered private and only accessed through CH4Event methods
All unit tests are performed through C4HEvent
"""

import uuid
import yaml
import dataclasses
from typing import Any
from pydantic import validator
from pydantic.dataclasses import dataclass
from . import score as c4h

def is_C4HEvent(event) -> bool:
    if not isinstance(event, c4h.C4HEvent):
        raise TypeError('Event must be a C4HEvent')
    return isinstance(event, c4h.C4HEvent)

class Config:
    """This defines the configuration for all the dataclasses.
    """
    validate_assignment = True
    arbitrary_types_allowed = True

@dataclass(config=Config)
class C4HArena(object):
    '''An arena in the event.'''

    event: Any #c4h.C4HEvent # Must be a C4HEvent
    id: str = ''
    name: str = ''
    ID: uuid.UUID = dataclasses.field(default=uuid.uuid1(), compare=False)

    # validators
    _valid_event = validator('event', allow_reuse=True)(is_C4HEvent)


@dataclass(config=Config)
class C4HRider:
    '''Rider details.

    Attributes:
        event (C4HEvent):
        surname (str):
        forename (str):
        _ID (uuid.UUID): unique ID
        ea_number (str): This must 7 numerical digits
    '''
    event: Any
    surname: str = ''
    forename: str = ''
    ID: uuid.UUID = uuid.uuid1()
    ea_number: str = ''

    # validators
    _valid_event = validator('event', allow_reuse=True)(is_C4HEvent)

    @validator('ea_number')
    def seven_digit_numerical(cls, val):
        # pass
        if val:
            if not val.isdigit():
                raise ValueError('EA Number may only constist of digits')
            if len(val) != 7:
                raise ValueError(f'Rider EA number should be 7 not {len(val)} digits long')
        return val


@dataclass(config=Config)
class C4HHorse:
    '''Rider details.

    Attributes:
        event (C4HEvent):
        name (str):
        ID (uuid.UUID): unique ID
        ea_number (str): This must 8 numerical digits
    '''
    # def __init__(self, name, ea_number):
    #     self.name = name
    event: Any
    name: str = ''
    ea_number: str = ''
    ID: uuid.UUID = uuid.uuid1()

    # validators
    _valid_event = validator('event', allow_reuse=True)(is_C4HEvent)

    @validator('ea_number')
    def seven_digit_numerical(cls, val):
        # pass
        if val:
            if not val.isdigit():
                raise ValueError('EA Number may only constist of digits')
            if len(val) != 8:
                raise ValueError(f'Rider EA number should be 7 not {len(val)} digits long')
        return val


@dataclass(config=Config)
class C4HCombo:
    '''Rider/horse combinations.

    Attributes:
        id (int):
        ID (uuid.UUID):
        rider (C4HRider):
        horse (C4HHorse):
    '''

    event: Any
    rider: C4HRider = None
    horse: C4HHorse = None
    id: str = ''
    ID: uuid.UUID = uuid.uuid1()

    # validators
    _valid_event = validator('event', allow_reuse=True)(is_C4HEvent)

    @validator('event')   
    def is_C4HEvent(cls, val):
        if not isinstance(val, c4h.C4HEvent):
            raise TypeError('Event must be a C4HEvent')
        
        return val


@dataclass(config=Config)
class C4HOfficial:
    '''Official details.

    Attributes:
        surname (str):
        forename (str): 
        judge (bool): default True
        cd (bool): default False
    '''
    surname: str = ''
    forename: str = ''
    judge: bool = True
    cd: bool = False

@dataclass(config=Config)
class C4HJumpClass:
    '''A show jumping class.

    Attributes:
        id (str): an integer that may have a character appended eg. 8c 
        name (str):
        arena (_C4HArena):
        _ID (uuid): unique identifier
        description (str):
        article (EAArticle):
        height (int): the height in cm
        judge (str): judges name
        cd (str): course designer name
        places (int): the number of places awarded prizes
        rounds (list[_C4HRound]): rounds entered in this arenas
    '''
    def __init__(self, id, arena):

        self._ID = uuid.UUID()
        self.id = id
        self.arena = arena
        self.name = f'Class {self.id}'
        self.article = None
        self.description = ''
        self.height = 0
        self.judge = ''
        self.cd = ''
        self.places = 6
        self.rounds= []

class C4HRound(object):
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
        id (str): Article number
        descrption (str): Short description of the class type
        alt_name (str): Alternative name for the class
        round_num (int): Number of rounds.
        round_table (str): Table for the round.

        identifier (str): the paragraph.subparagraph number string
        description (str): word description of the competition
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
#         fn (str): path and filename
#         event_name (str): the name of the event

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
