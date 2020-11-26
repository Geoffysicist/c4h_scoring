import json

articles = [
    ('238.2.2','Jump-off Competition','AM5'),
    ('245.3','Immediate Jump-off Competition','AM7')
    ]

articles_json = {}
articles_json['ea_articles'] = []

for a in articles:
    articles_json['ea_articles'].append({
    'id': a[0],
    'description': a[1],
    'old_name': a[2]
    })

#Write the object to file.
with open('docs/ea_articles.json','w') as jsonFile:
    json.dump(articles_json, jsonFile)