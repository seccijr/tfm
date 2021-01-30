import sys
import os
import json
import re
import urllib.request, json

base_url = 'http://www.wikidata.org/entity/'
news = open('news-json.tsv', 'r',encoding='utf-8')
lines = news.readlines()
kg = open('kg.tsv', 'a', encoding='utf-8')
item_entity = open('item_entity.tsv', 'a', encoding='utf-8')

for line in lines:
    try:
        print("New line...")
        line_tokens = re.split(r'\t+', line.rstrip('\t'))
        new_id = line_tokens[0]
        title_entities = json.loads(line_tokens[1])
        body_entities = json.loads(line_tokens[2]) if len(line_tokens) == 3 else []
        for entity in title_entities + body_entities:
            print(f'{new_id}\t{entity["WikidataId"]}\n')
            item_entity.write(f'{new_id}\t{entity["WikidataId"]}\n')
            url = f'{base_url}{entity["WikidataId"]}'
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            for property_key in data['entities'][entity['WikidataId']]['claims']:
                claims = data['entities'][entity['WikidataId']]['claims'][property_key]
                for claim in claims:
                    if 'type' in claim and claim['type'] == 'statement' \
                        and 'mainsnak' in claim and 'datatype' in claim['mainsnak'] \
                        and claim['mainsnak']['datatype'] == 'wikibase-item' \
                        and 'datavalue' in claim['mainsnak'] and 'type' in claim['mainsnak']['datavalue'] \
                        and claim['mainsnak']['datavalue']['type'] == 'wikibase-entityid':
                        print(f'{entity["WikidataId"]}\t{claim["mainsnak"]["property"]}\t{claim["mainsnak"]["datavalue"]["value"]["id"]}\n')
                        kg.write(f'{entity["WikidataId"]}\t{claim["mainsnak"]["property"]}\t{claim["mainsnak"]["datavalue"]["value"]["id"]}\n')
    except Exception as e:
        continue

kg.close()
item_entity.close()