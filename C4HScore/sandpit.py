import c4h_score as c4h
import yaml
from datetime import datetime, timezone

def test_event():
    event = c4h.C4HEvent("Great Event")
    print(type(event))
    fn = "test_out.c4hs"
    event.yaml_dump(fn)

    print('done')

def test_articles():
    fn = 'C4HScore/ea_articles.yaml'
    with open(fn, 'r') as in_file:
        articles = yaml.load(in_file, Loader=yaml.FullLoader)

    for a, b in articles.items():
        print(f'{a} {b}\n')

def make_articles():
    fn = "test.c4ha"
    articles = []
    articles.append(c4h.C4HArticle(100))
    articles.append(c4h.C4HArticle(101))
    sub_art1 = {'id': '.1.2', 'name': 'sub_art1'}
    sub_art2 = {'id': '.1.2', 'name': 'sub_art2', 'table': 'C'}
    articles[1].sub_articles.append(sub_art1)
    articles[1].sub_articles.append(sub_art2)
    
    with open(fn, 'w') as out_file:
        out_file.write('--- # C4H Articles\n')
        yaml.dump(articles, out_file)

if __name__ == "__main__":
    this_list = [1,2,3,4]
    print(type(this_list))

    