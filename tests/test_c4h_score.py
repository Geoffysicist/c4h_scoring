import pytest
from ..C4HScore import score as c4h
from ..C4HScore import score_helpers as sh
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
    arena = mock_event.arenas[0]
    assert mock_event.set_object(arena, name='Main Arena')
    assert arena.name == 'Main Arena'


def test_C4HEvent_exists_object(mock_event):
    arena = mock_event.arenas[0]
    assert mock_event.exists_object(arena)
    assert mock_event.exists_object(arena, id='1')
    assert not mock_event.exists_object(arena, id='42')


def test_C4HEvent_get_objects(mock_event):
    mock_event.new_arena(id='99')
    assert len(mock_event.get_objects(mock_event.arenas)) == len(mock_event.arenas)
    assert mock_event.get_objects(mock_event.arenas, id='99')
    assert not mock_event.get_objects(mock_event.arenas, id='42')

def test_C4HEvent_new_arena(mock_event):
    arena = mock_event.new_arena(id='2')
    assert type(arena) == score_helpers.C4HArena
    assert arena.id == '2'

def test_C4HEvent_new_rider(mock_event):
    assert type(mock_event.new_rider()) == c4h.C4HRider
    assert mock_event.new_rider(forename='fred').forename == 'fred'
    assert mock_event.new_rider(ea_number='1234567')
    num = '12345678'
    with pytest.raises(ValueError) as e:
        mock_event.new_rider(ea_number=num)
    assert str(e.value) == f'Rider EA number should be 7 not {len(num)} digits long'
    
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
