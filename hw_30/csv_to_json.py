import csv
import json

DATA_ADS = 'data/ads.csv'
JSON_ADS = 'ads.json'
DATA_CAT = 'data/categories.csv'
JSON_CAT = 'categories.json'

def convert_file(csv_file, model_name, json_file):
    result = []
    with open(csv_file, encoding='utf-8') as csvf:
        for row in csv.DictReader(csvf):
            to_add = {'model': model_name, 'pk': int(row['Id'] if 'Id' in row else row['id'])}
            if 'Id' in row:
                del row['Id']
            else:
                del row['id']
            if 'is_publishead' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'price' in row:
                row['price'] = int(row['price'])
            to_add['fields'] = row
            result.append(to_add)

    with open(json_file, 'w', encoding='utf-8') as jsf:
        jsf.write(json.dumps(result, ensure_ascii=False, indent=4))

# convert_file(DATA_ADS, 'ads.ad', JSON_ADS)
convert_file(DATA_CAT, 'ads.category', JSON_CAT)