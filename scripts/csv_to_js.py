import csv
import json

# Convert CSV to a JS variable
data = {}
with open('../data/processed/population_under_17.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[row['Pcode']] = {
            'State': row['State'],
            'County': row['County'],
            'Population': int(row['Population_Under_17'])
        }

with open('../population_data.js', 'w') as f:
    f.write('const populationData = ' + json.dumps(data, indent=2) + ';')

print("Created population_data.js")
