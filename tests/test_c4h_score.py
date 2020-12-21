import pytest
from ..C4HScore import score as c4h
import time
# import yaml


@pytest.fixture
def mock_event():
    mock_event = c4h.C4HEvent('Baccabuggry World Cup')
    # arena1 = mock_event.arenas[0]
    arena2 = mock_event.new_arena('2','Arena2')
    # class1 = arena1.new_jumpclass()
    # arena2.new_jumpclass()
    # arena1.new_jumpclass()
    # arena1.new_jumpclass()
    # arena2.new_jumpclass()
    # # create a class that is not allocated to an arena
    # arena2.new_jumpclass()
    # #create a test rider horse combination
    id = '1'
    horse = mock_event.new_horse('Topless')
    horse.ea_number = '12345678'
    rider = mock_event.new_rider(given_name='Phil', surname='McCraken')
    rider = mock_event.new_rider(given_name='Bob', surname='Down')
    combo1 = mock_event.new_combo(rider, horse, id=id)
    # # class1.combos.append(combo1)
    
    return mock_event

# Event
# -------------------------------------------------------------
def test_C4HEvent_update(mock_event):
    previous_update = mock_event.last_change
    time.sleep(1e-6)
    assert mock_event.update() > previous_update

# def test_C4HEvent_check_unique_id(mock_event):
#     assert mock_event.check_unique_id('1', mock_event.arenas) == False
#     assert mock_event.check_unique_id('42', mock_event.arenas) == True

def test_C4HEvent_new_arena(mock_event):
    arena3 = mock_event.new_arena('3','Arena3')
    assert type(arena3) == c4h.C4HArena
    
    with pytest.raises(ValueError) as e:
        mock_event.new_arena('1','Arena1')
    assert str(e.value) == "Arena with id 1 already exists"

def test_C4HEvent_get_arenas(mock_event):
    assert type(mock_event.get_arenas(id='1')[0]) == c4h.C4HArena
    assert type(mock_event.get_arenas(name='Arena2')[0]) == c4h.C4HArena
    assert not mock_event.get_arenas(id='42')

def test_C4HEvent_new_rider(mock_event):
    surname = "Zarzhoff"
    given = 'Bluey'
    new_rider = mock_event.new_rider(surname=surname, given_name=given)
    assert type(new_rider) == c4h.C4HRider
    
    with pytest.raises(ValueError) as e:
        mock_event.new_rider(surname=surname, given_name=given)
    assert str(e.value) == "Rider Zarzhoff Bluey already exists"

    # test with a correct number of digits for ea_number
    given = 'Bernie'
    ea_number = '1234567'
    new_rider = mock_event.new_rider(surname=surname, given_name=given)
    new_rider.ea_number = ea_number
    assert type(new_rider) == c4h.C4HRider

    # test with an incorrect number of digits for ea_number
    given = 'Terry'
    ea_number = '12345678'
    with pytest.raises(ValueError) as e:
            # new_rider = mock_event.new_rider(surname=surname, given_name=given, ea_number=ea_number)
            new_rider = mock_event.new_rider(surname=surname, given_name=given)
            new_rider.ea_number = ea_number
    assert str(e.value) == "Rider EA number should be a number 7 digits long"

def test_C4HEvent_get_riders(mock_event):
    riders = mock_event.get_riders(surname='McCraken', given_name='Phil')
    assert type(riders[0]) == c4h.C4HRider
    riders = mock_event.get_riders(surname='Down', given_name='Bob')
    assert type(riders[0]) == c4h.C4HRider
    assert len(riders) == 1
    assert not mock_event.get_riders(surname='McCraken', given_name='Bob')
    assert not mock_event.get_riders(surname='Down', given_name='Phil')

def test_C4HEvent_get_horses(mock_event):
    horses = mock_event.get_horses(name='Topless')
    assert len(horses) == 1
    assert type(horses[0]) == c4h.C4HHorse
    horses = mock_event.get_horses(ea_number='12345678')
    assert len(horses) == 1
    assert type(horses[0]) == c4h.C4HHorse
    assert not mock_event.get_horses(ea_number='12345679')


def test_C4HEvent_new_horse(mock_event):
    name = "Heffalump"
    new_horse = mock_event.new_horse(name)
    assert type(new_horse) == c4h.C4HHorse
    
    with pytest.raises(ValueError) as e:
        mock_event.new_horse(name)
    assert str(e.value) == "Horse Heffalump already exists"

def test_C4HEvent_get_combo(mock_event):
    combo = mock_event.get_combos(id='1')
    assert type(combo[0]) == c4h.C4HCombo
    assert type(combo[0].rider) == c4h.C4HRider
    assert type(combo[0].horse) == c4h.C4HHorse
    assert not mock_event.get_combos(id='666')

def test_C4HEvent_new_combo(mock_event):
    horse = mock_event.new_horse('Pal')
    rider = mock_event.new_rider('Gravity', 'Andy')
    combo = mock_event.new_combo(rider, horse)
    assert type(combo) == c4h.C4HCombo

    with pytest.raises(ValueError) as e:
        mock_event.new_combo(rider, horse)
    assert str(e.value) == "Combination Gravity, Andy: Pal already exists"


# def test_C4HEvent_get_jumpclasses(mock_event):
#     assert type(mock_event.get_jumpclasses()) == list
#     assert type(mock_event.get_jumpclasses()[0]) == c4h.C4HJumpClass

# JumpClass
# -------------------------------------------------------------


# Arena
# -------------------------------------------------------------
# def test_C4HArena_new_jumpclass(mock_event):
#     assert type(mock_event.arenas[0].new_jumpclass()) == c4h.C4HJumpClass

# def test_C4HArena_get_jumpclass(mock_event):
#     assert type(mock_event.arenas[0].get_jumpclass('1')) == c4h.C4HJumpClass
#     assert mock_event.arenas[0].get_jumpclass('99') == False



# # # Article
# # # -------------------------------------------------------------
# def test_C4HArticle_init():
#     this_article=c4h.C4HArticle('238.2.2')
#     this_article.sub_articles.append({
#         'id': f'{this_article._id}/245.3',
#         'description': 'Immediate Jumpoff',
#         'alt_name': 'AM7'
#     })
#     assert type(this_article) == c4h.C4HArticle

# # # def test_read_csv_nominate():
# # #     fn = 'tests/test_event_nominate.csv'
# # #     event = c4h.read_csv_nominate(fn)
# # #     assert len(event.classes) == 2
# # #     for jc in event.classes:
# # #         assert type(jc) == c4h.C4HJumpClass
# # #         for c in jc.combos:
# # #             assert type(c) == c4h.C4HCombo
# # #             assert type(c.rider) == c4h.C4HRider
# # #             assert type(c.horse) == c4h.C4HHorse

