import yaml

# read yaml file
fn = 'C4HScore/ea_articles.yaml'
with open(fn, 'r') as file:
    articles = yaml.full_load(file)

    for key, details in articles.items():
        print(key, ":", details)


fn = 'C4HScore/ea_articles_test.yaml'
with open(fn,'w') as outFile:
    outFile.write('--- # Articles\n')
    yaml.dump(articles, outFile)



