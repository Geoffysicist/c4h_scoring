import pytest
import c4h_scoreboard.c4h_scoreboard as c4h

@pytest.fixture
def mock_event():
    mock_event = c4h.C4HEvent('Baccabuggry World Cup')
    arena1 = mock_event.new_arena('Arena1')
    arena2 = mock_event.new_arena('Arena2')
    mock_event.new_class('Class1', arena=arena1)
    mock_event.new_class('Class2', arena=arena2)
    mock_event.new_class('Class3', arena=arena1)
    mock_event.new_class('Class4', arena=arena1)
    mock_event.new_class('Class5', arena=arena2)
    # create a class that is not allocated to an arena
    mock_event.new_class('Class6')
    
    return mock_event

def test_C4HEvent_get_name(mock_event):
    assert mock_event.get_name() == 'Baccabuggry World Cup'

def test_C4HEvent_set_name(mock_event):
    with pytest.raises(TypeError) as e:
        mock_event.set_name(42)
    assert str(e.value) == "event_name 42 is not a string"
    
    mock_event.set_name('Reg')
    assert mock_event.get_name() == 'Reg'

def test_C4HEvent_new_arena(mock_event):
    arena3 = mock_event.new_arena('Arena3')
    assert type(arena3) == c4h.C4HArena
    
    with pytest.raises(ValueError) as e:
        mock_event.new_arena('Arena1')
    assert str(e.value) == "Arena with id Arena1 already exists"

def test_C4HEvent_get_arenas(mock_event):
    assert len(mock_event.get_arenas()) == 2

def test_C4HEvent_get_arena(mock_event):
    assert type(mock_event.get_arena('Arena1')) == c4h.C4HArena
    assert mock_event.get_arena('Arena5') == None

def test_C4HEvent_new_class(mock_event):
    class9 = mock_event.new_class('Class9')
    assert type(class9) == c4h.C4HJumpClass
    
    with pytest.raises(ValueError) as e:
        mock_event.new_class('Class1')
    assert str(e.value) == "Class with id Class1 already exists"

def test_C4HEvent_get_classes(mock_event):
    assert len(mock_event.get_classes()) == 6

def test_C4HEvent_get_class(mock_event):
    assert type(mock_event.get_class('Class1')) == c4h.C4HJumpClass
    assert mock_event.get_arena('Class9') == None

def test_C4HArena_get_classes(mock_event):
    assert len(mock_event.get_arena('Arena1').get_classes()) == 3
    assert len(mock_event.get_arena('Arena2').get_classes()) == 2
    assert type(mock_event.get_arena('Arena2').get_classes()[0]) == c4h.C4HJumpClass

def test_C4HJumpClass_get_arena(mock_event):
    these_classes = mock_event.get_classes()
    arena1 = these_classes[0].get_arena()
    arena_none = these_classes[5].get_arena()

    assert type(arena1) == c4h.C4HArena
    assert arena1.get_id() == 'Arena1'
    assert arena_none == None

def test_C4HJumpClass_set_arena(mock_event):
    these_classes = mock_event.get_classes()
    class1 = these_classes[0]
    class1.set_arena(mock_event.get_arenas()[1])

    assert class1.get_arena().get_id() == 'Arena2'
    with pytest.raises(TypeError) as e:
        class1.set_arena('Arena1')
    assert str(e.value) == "Arg Arena1 is an object of type <class 'str'> should be type C4HArena"

def test_C4HEvent_new_rider(mock_event):
    surname = "Zarzhoff"
    given = 'Bluey'
    new_rider = mock_event.new_rider(surname=surname, given_name=given)
    assert type(new_rider) == c4h.C4HRider
    
    with pytest.raises(ValueError) as e:
        mock_event.new_rider(surname=surname, given_name=given)
    assert str(e.value) == "Rider Zarzhoff Bluey already exists"

    given = 'Bernie'
    ea_number = '1234567'
    new_rider = mock_event.new_rider(surname=surname, given_name=given, ea_number=ea_number)
    assert type(new_rider) == c4h.C4HRider

    given = 'Terry'
    ea_number = '12345678'
    with pytest.raises(ValueError) as e:
            new_rider = mock_event.new_rider(surname=surname, given_name=given, ea_number=ea_number)
    assert str(e.value) == "Rider EA number should be a number 7 digits long"

def test_C4HEvent_new_horse(mock_event):
    name = "Heffalump"
    ea_number = '12345678'
    new_horse = mock_event.new_horse(name)
    assert type(new_horse) == c4h.C4HHorse
    
    with pytest.raises(ValueError) as e:
        mock_event.new_horse(name)
    assert str(e.value) == "Horse Heffalump already exists"

    name = 'Suitable Boy'
    ea_number = '1234567'
    with pytest.raises(ValueError) as e:
            new_horse = mock_event.new_horse(name, ea_number=ea_number)
    assert str(e.value) == "Rider EA number should be a number 8 digits long"


    #TODO add test for EA number length - 8 digits

def test_C4HJumpClass_places(mock_event):
    this_class = mock_event.get_classes()[0]
    places = 6
    this_class.set_places(places)
    assert this_class.get_places() == places