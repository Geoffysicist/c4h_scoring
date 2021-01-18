import yaml
import pprint

pp = pprint.PrettyPrinter(indent=2)

# read yaml file
fn = 'C4HScore/ea_articles.yaml'
with open(fn, 'r') as file:
    articles = yaml.full_load(file)
    pp.pprint(articles)

    print(f'{articles.keys()}')

    # for key, details in articles.items():
    #     pp.pprint(key, ":", details)


fn = 'C4HScore/ea_articles_test.yaml'
with open(fn,'w') as outFile:
    outFile.write('--- # Articles\n')
    yaml.dump(articles, outFile)



