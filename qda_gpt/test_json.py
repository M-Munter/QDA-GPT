import json
from collections import OrderedDict
from jinja2 import Template


def generate_tables_from_response(response_text):
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise json.JSONDecodeError("Invalid JSON format", response_text, 0)
        response_text = response_text[start:end]
        response_json = json.loads(response_text, object_pairs_hook=OrderedDict)

        tables = []
        if isinstance(response_json, dict):
            for table_name, records in response_json.items():
                if isinstance(records, list):
                    flattened_data = []
                    for record in records:
                        flattened_record = flatten_dict(record)
                        flattened_data.append(flattened_record)

                    if flattened_data:
                        first_record = flattened_data[0]
                        columns = list(first_record.keys())
                        data = [[record.get(col, None) for col in columns] for record in flattened_data]
                        tables.append({
                            'table_name': table_name,
                            'columns': columns,
                            'data': data
                        })
        return tables

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    if isinstance(d, dict):
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
    else:
        items.append((parent_key, d))
    return dict(items)



if __name__ == "__main__":
    response_text = '''
{
    "Codes": [
        {
            "index": 1,
            "name": "Problem Solving Skills",
            "definition": "This code refers to instances where gaming has helped improve problem-solving skills. It includes scenarios where players need to strategize, plan, and solve complex problems within the game environment. This differs from 'Learning Motivation' which focuses on the motivational aspects of learning through gaming.",
            "quote": "Gaming has significantly improved my problem-solving skills.",
            "category_requirements": "Codes in this category must demonstrate improvements in cognitive skills due to gaming.",
            "categories": [1],
            "category_names": ["Educational Benefits"]
        },
        {
            "index": 2,
            "name": "Online Friendships",
            "definition": "This code captures instances where gaming has led to the formation of new friendships online. It includes examples of players meeting new people, building friendships, and maintaining social connections through gaming. This differs from 'Community Events' which focuses on organized events within the gaming community.",
            "quote": "I have made many friends through online gaming.",
            "category_requirements": "Codes in this category must reflect social interactions and relationships formed through gaming.",
            "categories": [2],
            "category_names": ["Social Interaction"]
        },
        {
            "index": 3,
            "name": "VR Technology",
            "definition": "This code includes mentions of Virtual Reality (VR) technology in gaming. It encompasses the development, use, and impact of VR on the gaming experience. This differs from 'Game Engine Development' which focuses on the software used to create games.",
            "quote": "The new VR technology has transformed my gaming experience.",
            "category_requirements": "Codes in this category must demonstrate the use and impact of VR technology in gaming.",
            "categories": [1, 2],
            "category_names": ["Educational Benefits", "Social Interaction"]
        },
        {
            "index": 4,
            "name": "Job Creation",
            "definition": "This code represents instances where the gaming industry has created job opportunities. It includes examples of employment in game development, marketing, and esports. This differs from 'Revenue Generation' which focuses on the financial income from gaming.",
            "quote": "The gaming industry has created numerous job opportunities.",
            "category_requirements": "Codes in this category must reflect economic benefits and job creation related to gaming.",
            "categories": [1],
            "category_names": ["Educational Benefits"]
        },
        {
            "index": 5,
            "name": "Learning Motivation",
            "definition": "This code refers to instances where gaming has increased motivation for learning. It includes examples where educational games or gamified learning experiences have encouraged students to engage more with educational content. This differs from 'Problem Solving Skills' which focuses on cognitive skill development.",
            "quote": "Educational games have made me more interested in learning.",
            "category_requirements": "Codes in this category must demonstrate increased motivation for learning due to gaming.",
            "categories": [1],
            "category_names": ["Educational Benefits"]
        },
        {
            "index": 6,
            "name": "Community Events",
            "definition": "This code captures instances of organized events within the gaming community, such as tournaments, meetups, and online gatherings. This differs from 'Online Friendships' which focuses on individual social relationships.",
            "quote": "I love participating in online gaming tournaments.",
            "category_requirements": "Codes in this category must reflect organized community events within the gaming context.",
            "categories": [2],
            "category_names": ["Social Interaction"]
        }
    ],
    "CategoryCodeHierarchy": [
        {
            "category_index": 1,
            "category_name": "Educational Benefits",
            "codes": [
                {
                    "code_index": 1,
                    "code_name": "Problem Solving Skills"
                },
                {
                    "code_index": 3,
                    "code_name": "VR Technology"
                },
                {
                    "code_index": 4,
                    "code_name": "Job Creation"
                },
                {
                    "code_index": 5,
                    "code_name": "Learning Motivation"
                }
            ]
        },
        {
            "category_index": 2,
            "category_name": "Social Interaction",
            "codes": [
                {
                    "code_index": 2,
                    "code_name": "Online Friendships"
                },
                {
                    "code_index": 3,
                    "code_name": "VR Technology"
                },
                {
                    "code_index": 6,
                    "code_name": "Community Events"
                }
            ]
        }
    ],
    "Themes": [
        {
            "name": "Educational and Social Impact",
            "quotes": "Gaming has significantly improved my problem-solving skills. ||| I have made many friends through online gaming. ||| Educational games have made me more interested in learning.",
            "analysis": "This theme shows that gaming has both positive and negative impacts on education and social behavior.",
            "conclusions": "Gaming can be a valuable educational tool but requires careful implementation."
        },
        {
            "name": "Technological Advances",
            "quotes": "The new VR technology has transformed my gaming experience. ||| The gaming industry has created numerous job opportunities. ||| Technological innovations are crucial for the future of gaming.",
            "analysis": "Technological innovations in gaming drive industry growth and change user experiences.",
            "conclusions": "Ongoing technological developments are crucial for the future of the gaming industry."
        }
    ],
    "Overall_Findings": {
        "summary_name": "Key Educational, Social, and Technological Findings from Gaming",
        "description": "This study explores the educational, social, and technological impacts of gaming, highlighting both benefits and challenges.",
        "flagged_segments": "The segment 'Gaming has helped me understand historical events better' is unaddressed, which could potentially provide new insights if properly categorized. ||| The segment 'I use VR for exercise routines' appears to be misclassified under 'Technological Advances' when it might fit better under 'Educational and Social Impact'. ||| The segment 'Gaming can sometimes be isolating' is missing critical information on the specific contexts where this occurs.",
        "analysis_and_interpretation": "The themes collectively highlight the multifaceted impact of gaming on education, social behavior, and technological progress.",
        "conclusions_and_implications": "The study concludes that while gaming offers significant educational and social benefits, there are also challenges that need to be addressed. Technological advancements play a key role in the industry's future."
    }
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
