# utils.py

import csv

def parse_response_to_table(json_response):
    table_data = []
    for item in json_response:
        row = {
            'Number or Index': item.get('index', ''),
            'Theme': item.get('theme', ''),
            'Description': item.get('description', '')
        }
        table_data.append(row)
    return table_data


def generate_csv(table_data, file_path):
    keys = table_data[0].keys() if table_data else []
    with open(file_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(table_data)