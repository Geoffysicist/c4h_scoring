"""Module1 - A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = SampleClass()
  
  bar = foo.public_method(required_variable, optional_variable=42)
"""

class C4HEvent(object):
    '''Equestrian Event.

    Attributes:
        _name (string): the event name
        _arenas (list): list of C4HArena objects
        _details (string): other information about the event
    '''

    def __init__(self, event_name):
        self._name = event_name
        self._arenas = []
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

class C4HClass(object):
    ''' Show jumping class

    Attributes:
        _name (string): the class name
        _arena (C4HArena):
    '''

class SampleClass(object):
    """Summary of class here.

    Longer class information after leaving a line...
    
    Attributes:
        likes_spam (type): indicates if we like SPAM or not.
        eggs (type): count of the eggs we have eaten.
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self._likes_spam = likes_spam
        self._eggs = 0

    def public_method(self):
        """Short description.
        
        Longer description of desired functionality

        Args:
            required_variable (type): A required argument
            optional_variable (type): An optional argument

        Returns:
            type: nothing but if it did you would describe it here

        Raises:
            NoError: but if it did you would describe it here
        """
        return None

def function_name(required_variable, optional_variable=None):
    """Short description.

    Longer description of desired functionality

    Args:
        required_variable (type): A required argument
        optional_variable (type): An optional argument

    Returns:
        type: nothing but if it did you would describe it here

    Raises:
        NoError: but if it did you would describe it here
    """
    return None

    
if __name__ == "__main__":
    this_event = C4HEvent('Baccabuggry World Cup')
    arena1 = this_event.new_arena('arena1')
    arena2 = this_event.new_arena('arena2')
    arena3 = this_event.new_arena('arena1')

    print(this_event.get_name())
    for a in this_event.get_arenas():
        print (a.get_name())