import pytest
import C4HScore.c4h_score as c4h
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
    class1.combos.append(combo1)
    
    return mock_event

# Event
# -------------------------------------------------------------

def test_C4HEvent_new_arena(mock_event):
    arena3 = mock_event.new_arena('Arena3')
    assert type(arena3) == c4h.C4HArena
    
    with pytest.raises(ValueError) as e:
        mock_event.new_arena('Arena1')
    assert str(e.value) == "Arena with id Arena1 already exists"

def test_C4HEvent_get_arena(mock_event):
    assert type(mock_event.get_arena('Arena1')) == c4h.C4HArena
    assert mock_event.get_arena('Arena5') == None

def test_C4HEvent_new_class(mock_event):
    class9 = mock_event.new_class('Class9')
    assert type(class9) == c4h.C4HJumpClass
    
    with pytest.raises(ValueError) as e:
        mock_event.new_class('Class1')
    assert str(e.value) == "Class with id Class1 already exists"

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
    initial_len_combo_list = len(mock_event.combos)
    id = '2'
    horse = mock_event.new_horse('Topless')
    rider = mock_event.new_rider(('Gravity', 'Andy'))
    this_combo = mock_event.new_combo(id, rider, horse)
    assert type(this_combo) == c4h.C4HCombo
    assert len(mock_event.combos) - initial_len_combo_list == 1

def test_C4HEvent_get_combo(mock_event):
    this_combo = mock_event.get_combo('1')
    assert type(this_combo) == c4h.C4HCombo
    assert type(this_combo.rider) == c4h.C4HRider
    assert type(this_combo.horse) == c4h.C4HHorse
    that_combo = mock_event.get_combo('666')
    assert that_combo is None

# Arena
# -------------------------------------------------------------


# JumpClass
# -------------------------------------------------------------
def test_C4HJumpClass_get_combo(mock_event):
    this_combo = mock_event.get_combo('1')
    assert type(this_combo) == c4h.C4HCombo
    assert type(this_combo.rider) == c4h.C4HRider
    assert type(this_combo.horse) == c4h.C4HHorse
    that_combo = mock_event.get_combo('666')
    assert that_combo is None


def test_read_csv_nominate():
    fn = 'tests/test_event_nominate.csv'
    event = c4h.read_csv_nominate(fn)
    assert len(event.classes) == 2
    for jc in event.classes:
        assert type(jc) == c4h.C4HJumpClass
        for c in jc.combos:
            assert type(c) == c4h.C4HCombo
            assert type(c.rider) == c4h.C4HRider
            assert type(c.horse) == c4h.C4HHorse

