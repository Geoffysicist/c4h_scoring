import pytest
import C4HScore.c4h_scoreboard as c4h
import yaml

@pytest.fixture
def mock_event():
    mock_event = c4h.C4HEvent('Baccabuggry World Cup')
    arena1 = mock_event.get_arena('Arena1')
    arena2 = mock_event.new_arena('Arena2')
    class1 = mock_event.new_class('Class1', arena=arena1)
    mock_event.new_class('Class2', arena=arena2)
    mock_event.new_class('Class3', arena=arena1)
    mock_event.new_class('Class4', arena=arena1)
    mock_event.new_class('Class5', arena=arena2)
    # create a class that is not allocated to an arena
    mock_event.new_class('Class6')
    #create a test rider horse combination
    id = '1'
    horse = mock_event.new_horse(name='Pal')
    rider = mock_event.new_rider(given_name='Phil', surname='McCraken')
    combo1 = mock_event.new_combo(id, rider, horse)
    class1.add_combo(combo1)
    
    return mock_event

# Event
# -------------------------------------------------------------
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

def test_C4HEvent_get_rider(mock_event):
    rider = mock_event.get_rider('McCraken', 'Phil')
    assert type(rider) == c4h.C4HRider

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

def test_C4HEvent_get_horse(mock_event):
    horse = mock_event.get_horse('Pal')
    assert type(horse) == c4h.C4HHorse

def test_C4HEvent_new_combo(mock_event):
    initial_len_combo_list = len(mock_event.get_combos())
    id = '2'
    horse = mock_event.new_horse('Topless')
    rider = mock_event.new_rider(('Gravity', 'Andy'))
    this_combo = mock_event.new_combo(id, rider, horse)
    assert type(this_combo) == c4h.C4HCombo
    assert len(mock_event.get_combos()) - initial_len_combo_list == 1

def test_C4HEvent_get_combo(mock_event):
    this_combo = mock_event.get_combo('1')
    assert type(this_combo) == c4h.C4HCombo
    assert type(this_combo.get_rider()) == c4h.C4HRider
    assert type(this_combo.get_horse()) == c4h.C4HHorse
    that_combo = mock_event.get_combo('666')
    assert that_combo is None

def test_C4HEvent_write_c4hs(mock_event):
    mock_event.write_c4hs('test_output.c4hs')

def test_C4HEvent_yaml_dump(mock_event):
    mock_event.yaml_dump('test_output.c4hs')

# Arena
# -------------------------------------------------------------

def test_C4HArena_get_classes(mock_event):
    assert len(mock_event.get_arena('Arena1').get_classes()) == 4 #allocated to Arena1 by default
    assert len(mock_event.get_arena('Arena2').get_classes()) == 2
    assert type(mock_event.get_arena('Arena2').get_classes()[0]) == c4h.C4HJumpClass

# JumpClass
# -------------------------------------------------------------
def test_C4HJumpClass_get_arena(mock_event):
    these_classes = mock_event.get_classes()
    arena1 = these_classes[0].get_arena()
    
    assert type(arena1) == c4h.C4HArena
    assert arena1.get_id() == 'Arena1'

def test_C4HJumpClass_set_arena(mock_event):
    these_classes = mock_event.get_classes()
    class1 = these_classes[0]
    class1.set_arena(mock_event.get_arenas()[1])

    assert class1.get_arena().get_id() == 'Arena2'
    with pytest.raises(TypeError) as e:
        class1.set_arena('Arena1')
    assert str(e.value) == "Arg Arena1 is an object of type <class 'str'> should be type C4HArena"

def test_C4HJumpClass_places(mock_event):
    this_class = mock_event.get_classes()[0]
    places = 6
    this_class.set_places(places)
    assert this_class.get_places() == places

def test_C4HJumpClass_get_combo(mock_event):
    this_combo = mock_event.get_combo('1')
    assert type(this_combo) == c4h.C4HCombo
    assert type(this_combo.get_rider()) == c4h.C4HRider
    assert type(this_combo.get_horse()) == c4h.C4HHorse
    that_combo = mock_event.get_combo('666')
    assert that_combo is None

def test_C4HJumpClass_add_combo(mock_event):
    this_class = mock_event.get_classes()[0]
    num_in_class = len(this_class.get_combos())
    this_class.add_combo(mock_event.get_combo('2'))
    assert len(this_class.get_combos()) - num_in_class == 1

    with pytest.raises(ValueError) as e:
            this_class.add_combo(mock_event.get_combo('1'))
    assert str(e.value) == "Combination 1 already in class"


def test_read_csv_nominate():
    fn = 'tests/test_event_nominate.csv'
    event = c4h.read_csv_nominate(fn)
    event.yaml_dump('test_output.c4hs')
    assert len(event.get_classes()) == 2
    for jc in event.get_classes():
        assert type(jc) == c4h.C4HJumpClass
        for c in jc.get_combos():
            assert type(c) == c4h.C4HCombo
            assert type(c.get_rider()) == c4h.C4HRider
            assert type(c.get_horse()) == c4h.C4HHorse

def test_load_yaml():
    fn = 'test_output.c4hs'
    event = c4h.load_yaml(fn)
    assert type(event) == c4h.C4HEvent
    assert event.get_name() == 'Baccabuggry World Cup'