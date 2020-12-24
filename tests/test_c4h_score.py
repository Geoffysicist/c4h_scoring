import pytest
from ..C4HScore import score as c4h
import time
# import yaml


@pytest.fixture
def mock_event():
    mock_event = c4h.C4HEvent('Baccabuggry World Cup')
    arena = mock_event.new_arena(id='1')
    # rider = mock_event.new_rider(given_name='Bob', surname='Down')
    # horse = mock_event.new_horse(name='Topless')
    # combo = mock_event.new_combo(rider, horse)
    
    return mock_event

# Event
# -------------------------------------------------------------
def test_C4HEvent_update(mock_event):
    previous_update = mock_event.last_change
    time.sleep(1e-6)
    assert mock_event.update() > previous_update


def test_C4HEvent_set_object(mock_event):
    """ Test the set object method for each C4HScore dataclass.

    add a new test whenever you add a dataclass.
    """
    #C4HArena
    arena = mock_event.arenas[0]
    assert mock_event.set_object(arena, name='Main Arena')
    assert arena.name == 'Main Arena'

#     #C4HRider
#     rider = mock_event.new_rider()
#     sname = 'McCracken'
#     gname = 'Phil'
#     assert mock_event.set_object(rider, surname=sname, given_name=gname)
#     assert mock_event.riders[-1].surname == sname
#     with pytest.raises(ValueError) as e:
#         mock_event.set_object(rider, surname='Down', given_name='Bob')
#     assert str(e.value) == f"Rider named Down, Bob already exists"
#     assert mock_event.set_object(rider, ea_number = '1234567')
#     with pytest.raises(ValueError) as e:
#         mock_event.set_object(rider, ea_number = '12345678')
#     assert str(e.value) == "Rider EA number should be 7 not 8 digits long"
   
#     #C4HHorse
#     with pytest.raises(ValueError) as e:
#         number = '1234567'
#         mock_event.set_object(mock_event.horses[0],ea_number=number)
#     assert str(e.value) == f"Horse EA number should be 8 not {len(number)} digits long"
#     assert mock_event.set_object(mock_event.horses[0],ea_number='12345678')
#     with pytest.raises(ValueError) as e:
#         name = mock_event.horses[0].name
#         mock_event.set_object(mock_event.horses[0],name=name)
#     assert str(e.value) == f"Horse {name} already exists"

#     #C4HCombo
#     # test id
#     # rider defined above
#     horse = mock_event.horses[-1]
#     combo = mock_event.new_combo(rider, horse)
#     id = '42'
#     assert mock_event.set_object(combo, id=id)
#     with pytest.raises(ValueError) as e:
#         mock_event.set_object(combo, id=id)
#     assert str(e.value) == f"Combo with id {id} already exists"
#     with pytest.raises(ValueError) as e:
#         mock_event.set_object(mock_event.combos[0], rider=rider, horse=horse)
#     assert str(e.value) == f'Combo: {rider.surname} {rider.given_name} riding {horse.name} already exists'

def test_C4HEvent_exists_object(mock_event):

    arena = mock_event.arenas[0]
    assert mock_event.exists_object(arena)
    # assert mock_event.exists_object(arena, id='1')
    


# def test_C4HEvent_get_objects(mock_event):
#     """Test the get objects method for each C4HScore dataclass.

#     add a new test whenever you add a dataclass
#     """
#     #C4HArena
#     assert type(mock_event.get_objects(mock_event.arenas, id='1')[0]) == c4h._C4HArena
#     assert type(mock_event.get_objects(mock_event.arenas, name='Arena 1')[0]) == c4h._C4HArena
#     assert not mock_event.get_objects(mock_event.arenas, id='42')

#     #C4HRider
#     assert type(mock_event.get_objects(
#         mock_event.riders, surname='Down', given_name='Bob'
#         )[0]) == c4h._C4HRider
#     assert not mock_event.get_objects(
#         mock_event.riders, surname='Down', given_name='Ben'
#         )

# def test_C4HEvent_merge_objects(mock_event):
#     pass # TODO

def test_C4HEvent_new_arena(mock_event):
    arena = mock_event.new_arena(id='2')
    assert type(arena) == c4h._C4HArena
    assert arena.name == 'Arena 2'

#     with pytest.raises(ValueError) as e:
#         mock_event.new_arena('1')
#     assert str(e.value) == "Arena with id 1 already exists"

# def test_C4HEvent_new_rider(mock_event):
#     assert type(mock_event.new_rider()) == c4h._C4HRider
    
# # TODO start here
# def test_C4HEvent_new_horse(mock_event):
#     name = "Heffalump"
#     assert type(mock_event.new_horse(name=name)) == c4h._C4HHorse

# def test_C4HEvent_new_combo(mock_event):
#     rider = mock_event.new_rider(given_name='Andy', surname='Gravity')
#     horse = mock_event.new_horse(name='Heffalump')
#     assert type(mock_event.new_combo(rider, horse)) == c4h._C4HCombo

#     with pytest.raises(ValueError) as e:
#         mock_event.new_combo(rider, horse)
#     assert str(e.value) == f"Combination {rider.surname}, {rider.given_name}: {horse.name} already exists"

# def test_C4HEvent_new_official(mock_event):
#     surname = "Hunt"
#     given = "Mike"
#     new_official = mock_event.new_official(surname, given)
#     assert type(new_official) == c4h._C4HOfficial

#     with pytest.raises(ValueError) as e:
#         mock_event.new_official(surname, given)
#     assert str(e.value) == "Official Hunt Mike already exists"
