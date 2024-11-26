import csv
import json

def csv_to_json(csv_file, json_file):

    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]

    with open(json_file, 'w') as json_file:
        json_file.dump(data, json_file, indent=4)

    print(f'CSV2JSON converted {len(data)} records to {json_file}')

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as json_file:
        json_reader = json.load(json_file)

    data = json_reader['data']

    with open(csv_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        count = 0
        for row in json_reader:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(row.values())