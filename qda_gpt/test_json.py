import json
from jinja2 import Template


def generate_tables_from_response(response_text):
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise json.JSONDecodeError("Invalid JSON format", response_text, 0)
        response_text = response_text[start:end]
        response_json = json.loads(response_text)

        tables = []
        if isinstance(response_json, dict):
            for table_name, records in response_json.items():
                if isinstance(records, list):
                    flattened_data = []
                    for record in records:
                        flattened_record = flatten_dict(record)
                        flattened_data.append(flattened_record)

                    if flattened_data:
                        columns = set(flattened_data[0].keys())
                        data = [[record.get(col, None) for col in columns] for record in flattened_data]
                        tables.append({
                            'table_name': table_name,
                            'columns': list(columns),
                            'data': data
                        })
        return tables

    except json.JSONDecodeError as e:
        return []


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if v and isinstance(v[0], dict):
                for i, sub_v in enumerate(v):
                    items.extend(flatten_dict(sub_v, f"{new_key}{sep}{i}", sep=sep).items())
            else:
                items.append((new_key, v))
        else:
            items.append((new_key, v))
    return dict(items)


if __name__ == "__main__":
    response_text = '''
    {
      "Simple Table": [
        {
          "index": 1,
          "name": "Item A",
          "value": "Value A"
        },
        {
          "index": 2,
          "name": "Item B",
          "value": "Value B"
        }
      ],
      "Mediocre Table": [
        {
          "index": 1,
          "category": "Category 1",
          "details": {
            "subindex": 1,
            "subvalue": "Subvalue A"
          }
        },
        {
          "index": 2,
          "category": "Category 2",
          "details": {
            "subindex": 2,
            "subvalue": "Subvalue B"
          }
        }
      ],
      "Complex Table": [
        {
          "index": 1,
          "type": "Type A",
          "attributes": [
            {
              "attr_index": 1,
              "attr_value": "Attribute A1"
            },
            {
              "attr_index": 2,
              "attr_value": "Attribute A2"
            }
          ]
        },
        {
          "index": 2,
          "type": "Type B",
          "attributes": [
            {
              "attr_index": 3,
              "attr_value": "Attribute B1"
            }
          ]
        }
      ],
      "Nested Table": [
        {
          "index": 1,
          "theme": "Theme A",
          "details": {
            "subindex": 1,
            "subdetails": [
              {
                "subsubindex": 1,
                "subsubvalue": "SubSubValue A1"
              },
              {
                "subsubindex": 2,
                "subsubvalue": "SubSubValue A2"
              }
            ]
          }
        },
        {
          "index": 2,
          "theme": "Theme B",
          "details": {
            "subindex": 2,
            "subdetails": [
              {
                "subsubindex": 3,
                "subsubvalue": "SubSubValue B1"
              },
              {
                "subsubindex": 4,
                "subsubvalue": "SubSubValue B2"
              }
            ]
          }
        }
      ],
      "Mixed Types Table": [
        {
          "index": 1,
          "name": "Mixed A",
          "value": "Value A",
          "extra": {
            "extra_index": 1,
            "extra_value": "Extra Value A",
            "more_extra": {
              "nested_extra_index": 1,
              "nested_extra_value": "Nested Extra Value A"
            }
          }
        },
        {
          "index": 2,
          "name": "Mixed B",
          "value": "Value B",
          "extra": {
            "extra_index": 2,
            "extra_value": "Extra Value B",
            "more_extra": {
              "nested_extra_index": 2,
              "nested_extra_value": "Nested Extra Value B"
            }
          }
        }
      ],
      "Large Data Table": [
        {
          "index": 1,
          "name": "Item A",
          "details": {
            "subindex": 1,
            "subdetails": [
              {
                "subsubindex": 1,
                "subsubvalue": "SubSubValue A1"
              },
              {
                "subsubindex": 2,
                "subsubvalue": "SubSubValue A2"
              }
            ]
          }
        },
        {
          "index": 2,
          "name": "Item B",
          "details": {
            "subindex": 2,
            "subdetails": [
              {
                "subsubindex": 3,
                "subsubvalue": "SubSubValue B1"
              },
              {
                "subsubindex": 4,
                "subsubvalue": "SubSubValue B2"
              }
            ]
          }
        },
        {
          "index": 3,
          "name": "Item C",
          "details": {
            "subindex": 3,
            "subdetails": [
              {
                "subsubindex": 5,
                "subsubvalue": "SubSubValue C1"
              },
              {
                "subsubindex": 6,
                "subsubvalue": "SubSubValue C2"
              }
            ]
          }
        },
        {
          "index": 4,
          "name": "Item D",
          "details": {
            "subindex": 4,
            "subdetails": [
              {
                "subsubindex": 7,
                "subsubvalue": "SubSubValue D1"
              },
              {
                "subsubindex": 8,
                "subsubvalue": "SubSubValue D2"
              }
            ]
          }
        }
      ],
      "Super Complex Table": [
        {
          "index": 1,
          "type": "Type A",
          "attributes": [
            {
              "attr_index": 1,
              "attr_value": "Attribute A1",
              "nested_attributes": [
                {
                  "nested_attr_index": 1,
                  "nested_attr_value": "Nested Attribute A1-1"
                },
                {
                  "nested_attr_index": 2,
                  "nested_attr_value": "Nested Attribute A1-2"
                }
              ]
            },
            {
              "attr_index": 2,
              "attr_value": "Attribute A2",
              "nested_attributes": [
                {
                  "nested_attr_index": 3,
                  "nested_attr_value": "Nested Attribute A2-1"
                },
                {
                  "nested_attr_index": 4,
                  "nested_attr_value": "Nested Attribute A2-2"
                }
              ]
            }
          ]
        },
        {
          "index": 2,
          "type": "Type B",
          "attributes": [
            {
              "attr_index": 3,
              "attr_value": "Attribute B1",
              "nested_attributes": [
                {
                  "nested_attr_index": 5,
                  "nested_attr_value": "Nested Attribute B1-1"
                }
              ]
            }
          ]
        }
      ]
    }
    '''

    tables = generate_tables_from_response(response_text)
    for table in tables:
        print(f"Table Name: {table['table_name']}")
        print(f"Columns: {table['columns']}")
        for row in table['data']:
            print(f"Data: {row}")
        print("\n" + "-" * 50 + "\n")

    prompt_table_pairs = [{
        "prompt": "Example User Prompt",
        "tables": tables
    }]

    # Adjust this path to where your response_table.html is located
    template_path = 'C:\\Users\\MM\\PycharmProjects\\QDA-GPT_project\\qda_gpt\\templates\\qda_gpt\\response_table.html'

    # Load the HTML template
    with open(template_path, 'r') as file:
        template_content = file.read()

    # Render the template with the tables data
    template = Template(template_content)
    rendered_html = template.render(prompt_table_pairs=prompt_table_pairs)

    # Save the rendered HTML to a file
    output_path = 'C:\\Users\\MM\\PycharmProjects\\QDA-GPT_project\\qda_gpt\\rendered_response.html'
    with open(output_path, 'w') as file:
        file.write(rendered_html)

    print(f"HTML rendered and saved to {output_path}")
