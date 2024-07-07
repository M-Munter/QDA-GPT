
import json

response_text = '''
{
  "Expressions": [
    "simplified expression 1",
    "simplified expression 2",
    "another expression"
  ],
  "Clusters": [
    {
      "subcategory": "subcategory name 1",
      "expressions": [
        "simplified expression 1",
        "simplified expression 2"
      ]
    },
    {
      "subcategory": "subcategory name 2",
      "expressions": [
        "another expression",
        "yet another expression"
      ]
    }
  ],
  "groups": [
    {
      "index": 1,
      "name": "Gaming Community Dynamics",
      "description": "Themes focusing on the dynamics, behavior, and interactions within the gaming community.",
      "topics": [2, 3]
    },
    {
      "index": 2,
      "name": "Educational and Social Impact",
      "description": "Themes discussing the educational benefits and social implications of gaming.",
      "topics": [1, 3, 4]
    },
    {
      "index": 3,
      "name": "eSports and Ethics",
      "description": "Themes related to the ethical considerations and involvement in eSports.",
      "topics": [4]
    },
    {
      "index": 4,
      "name": "Economic Impact",
      "description": "Themes discussing the economic aspects and impacts of gaming.",
      "topics": [1, 2]
    }
  ]
}
'''


def generate_tables_from_response(response_text):
    try:
        # Parse the JSON response
        response_json = json.loads(response_text)

        # Prepare the table data
        tables = []
        if isinstance(response_json, dict):
            for table_name, records in response_json.items():
                if isinstance(records, list):
                    if records and all(isinstance(record, dict) for record in records):
                        columns = list(records[0].keys())
                        data = [list(record.values()) for record in records]
                        tables.append({
                            'table_name': table_name,
                            'columns': columns,
                            'data': data
                        })
                    else:
                        tables.append({
                            'table_name': table_name,
                            'columns': ["Expressions"],
                            'data': [[expression] for expression in records]
                        })
        return tables

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return []


if __name__ == "__main__":
    tables = generate_tables_from_response(response_text)
    for table in tables:
        print(f"Table Name: {table['table_name']}")
        print(f"Columns: {table['columns']}")
        for row in table['data']:
            print(f"Data: {row}")
        print("\n" + "-" * 50 + "\n")