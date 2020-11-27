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

    def set_name(self, event_name):
        '''Sets the name of the event

        Args:
            event_name (string)
        '''
        if type(event_name) == str:
            self._name = event_name
        else:
            raise TypeError(f"event_name {event_name} is not a string")

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

class C4HArena(object):
    '''An arena in the event which holds classes.

    Attributes:
        _id (string):
        _event (C4HEvent):
    '''

    def __init__(self, arena_id, event):
        self._id = arena_id
        self._event = event

    def get_id(self):
        return self._id

    def get_classes(self):
        '''returns the classes in this arena.
        '''
        classes = []
        for c in self._event.get_classes():
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
        _places (int): the number ofplaces awarded prizes
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
        self._combinations = []

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



if __name__ == "__main__":
    ea_articles = []

    #Read the EA articles json to a dictionary then objects
    with open('c4h_scoreboard/ea_articles.json', 'r') as articles_json:
        ea_art_dict = json.load(articles_json)

    ea_art_dict = ea_art_dict['ea_articles']

    for a in ea_art_dict:
        ea_articles.append(EAArticle(a))

    #now the event stuff
    this_event = C4HEvent('Baccabuggry World Cup')
    arena1 = this_event.new_arena('arena1')
    arena2 = this_event.new_arena('arena2')
    class1 = this_event.new_class('class1')
    class2 = this_event.new_class('class2')
    class3 = this_event.new_class('class3', arena=arena2)
    class4 = this_event.new_class('class4', arena=arena1)
    class1.set_arena(arena1)
    class2.set_arena(arena2)
    
    print(this_event.get_name())

    for a in this_event.get_arenas():
        print (a.get_id())
        for c in a.get_classes():
            print(c.get_id())