import C4HScore.c4h_scoreboard as c4h
# import yaml

fn = './test_output.c4hs'
event = c4h.load_yaml(fn)
print(type(event))
print(event.get_name())
for a in event.get_arenas():
    print(a.get_id())

for r in event.get_riders():
    print(f'{r.get_given_name()} {r.get_surname()}')