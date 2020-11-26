"""Module1 - A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = SampleClass()
  
  bar = foo.public_method(required_variable, optional_variable=42)
"""

import json

class C4HEvent(object):
    '''Equestrian Event.

    Attributes:
        _name (string): the event name
        _arenas (list): list of C4HArena objects
        _classes (list): list of C4HJumpClass objects
        _details (string): other information about the event
    '''

    def __init__(self, event_name):
        self._name = event_name
        self._arenas = []
        self._classes = []
        self._details = ''

    def get_name(self):
        ''' returns the name of the event.'''
        return self._name

    def get_arenas(self):
        '''returns the list of arenas in the event'''
        return self._arenas
    
    def new_arena(self, arena_name):
        '''creates a new arena if it doesn't exist.

        checks to see if an arena with name arena_name exists
        if it exists the arena is returned
        if not a new arena is created and added to the arena list then returned

        Args:
            arena_name (string): the name of the arena to check/create
        '''

        for a in self._arenas:
            if a.get_name() == arena_name:
                return a
                
        a = C4HArena(arena_name, self)
        self._arenas.append(a)
        return a

    def new_class(self, class_id):
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
                
        c = C4HJumpClass(class_id, self)
        self._classes.append(c)
        return c

class C4HArena(object):
    '''An arena in the event which holds classes.

    Attributes:
        _name (string):
        _event (C4HEvent):
        _classes (list): list of C4HClasses
    '''

    def __init__(self, arena_name, event):
        self._name = arena_name
        self._event = event
        self._classes = []

    def get_name(self):
        return self._name

    def add_class(self, jump_class):
        if type(jump_class) == C4HJumpClass:
            self._classes.append(jump_class)
            jump_class.set_arena(self)
        else:
            raise TypeError('{} is type {} not type C4HJumpClass'.format(jump_class, type(jump_class)))
            # raise TypeError(f'{jump_class} is type {type(jump_class)} not type C4HJumpClass')

    def get_classes(self):
        return self._classes

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
        _places (int): the number ofplaces awarded prizes
        _combinations (list): list of the horse/rider combinations entered
    '''

    def __init__(self, class_id, places=6):
        self._id = class_id
        self._name = None
        self._article = None
        self._arena = None
        self._description = None
        self._height = None
        self._times = []
        self._judge = None
        self._cd = None
        self._places = places
        self._combinations = []

    def get_id(self):
        return self._id
    
    def set_arena(self, arena):
        if type(arena) == C4HArena:
            self._arena = arena
        else:
            raise TypeError('{} is type {} not type C4HArena'.format(arena, type(arena)))
            

    def get_arena(self):
        return self._arena

if __name__ == "__main__":
    ea_articles = []

    #Read the EA articles json to a dictionary then objects
    with open('c4h_scoreboard/ea_articles.json', 'r') as articles_json:
        ea_art_dict = json.load(articles_json)

    ea_art_dict = ea_art_dict['ea_articles']

    for a in ea_art_dict:
        ea_articles.append(EAArticle(a))

    this_event = C4HEvent('Baccabuggry World Cup')
    arena1 = this_event.new_arena('arena1')
    class1 = this_event.new_class('class1')
    class2 = this_event.new_class('class2')
    class3 = this_event.new_class('class3')
    class4 = this_event.new_class('class3')
    arena1.add_class(class1)
    arena1.add_class(class2)
    arena2 = this_event.new_arena('arena2')
    arena2.add_class(class3)
    
    print(this_event.get_name())

    for a in this_event.get_arenas():
        print (a.get_name())
        for c in a.get_classes():
            print(c.get_id())