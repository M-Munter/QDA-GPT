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
        summary = {}

        if isinstance(response_json, dict):
            for key, value in response_json.items():
                if isinstance(value, dict):
                    # Handle summary as a dictionary
                    summary[key] = value
                elif isinstance(value, list):
                    flattened_data = []
                    for record in value:
                        print(f"Processing record in table '{key}': {record}")
                        flattened_record = flatten_dict(record)
                        flattened_data.append(flattened_record)

                    if flattened_data:
                        first_record = flattened_data[0]
                        columns = list(first_record.keys())
                        data = [[record.get(col, None) for col in columns] for record in flattened_data]
                        tables.append({
                            'table_name': key,
                            'columns': columns,
                            'data': data
                        })
        return summary, tables

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return {}, []
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}, []

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
        print(f"Found a string where dict was expected: {d}")
        items.append((parent_key, d))
    return dict(items)



if __name__ == "__main__":
    response_text = '''
    {
    "Summary": {
        "name": "Gaming Impact Overview",
        "description": "Video games have profound effects on child development, interactive learning, social behavior, and education."
    },
    "Themes": [
        {
          "index": 1,
          "name": "Educational Games Scepticism",
          "description": "Mixed views on the effectiveness of educational games for learning, with skepticism towards serious games.",
          "quote": "A lot of them just... they're not fun, and what's the point, it's missing the whole point of what a game can do."
        },
        {
          "index": 2,
          "name": "Toxicity in Online Gaming",
          "description": "Discussions on the prevalence of toxic interactions in online gaming communities.",
          "quote": "Some games have more toxic communities than others... it's not as toxic."
        },
        {
          "index": 3,
          "name": "Dual Educational-Entertainment Value",
          "description": "Recognition of games' ability to simultaneously educate and entertain.",
          "quote": "Games generally, interactive entertainment, they can do both at the same time."
        },
        {
          "index": 4,
          "name": "Parental Engagement & Respect",
          "description": "Acknowledgment of the benefits of parents engaging with and respecting their children's gaming interests.",
          "quote": "I think it's a good aspect, it's not necessarily something that all parents would have to do as a rule, but it absolutely could be beneficial."
        }
    ],
    "Groups": [
        {
          "index": 1,
          "name": "Educational Impact",
          "description": "Themes related to the educational aspects of gaming, including skepticism, educational-entertainment value, and parental engagement.",
          "topics": [1, 3, 4]
        },
        {
          "index": 2,
          "name": "Online Gaming Community Dynamics",
          "description": "Themes discussing toxic interactions and community dynamics in online gaming.",
          "topics": [2]
        }
    ],
    "Initial Expressions": [
        "Put forward the next version based on player feedback",
        "Bring fantasy elements into the picture",
        "Reduce game prices to combat piracy",
        "Include new devices to enhance player experience",
        "Create curiosity in players for monetization",
        "Stop disruptive in-game ads for monetization",
        "Combat piracy through internet access control",
        "Address the challenge of inclusiveness in games",
        "Encourage developers to try new things and be realistic about game promises",
        "Recognize the benefits that games can bring"
    ],
    "Clusters": [
        {
          "subcategory": "Player Engagement and Feedback",
          "expressions": [
            "Put forward the next version based on player feedback",
            "Bring fantasy elements into the picture",
            "Include new devices to enhance player experience",
            "Create curiosity in players for monetization"
          ]
        },
        {
          "subcategory": "Monetization Strategy",
          "expressions": [
            "Create curiosity in players for monetization",
            "Stop disruptive in-game ads for monetization"
          ]
        },
        {
          "subcategory": "Combatting Piracy",
          "expressions": [
            "Reduce game prices to combat piracy",
            "Combat piracy through internet access control"
          ]
        },
        {
          "subcategory": "Game Development and Industry Challenges",
          "expressions": [
            "Address the challenge of inclusiveness in games",
            "Encourage developers to try new things and be realistic about game promises",
            "Recognize the benefits that games can bring"
          ]
        }
    ],
    "Theoretical Concepts": [
        {
          "concept": "Player-Centric Game Development",
          "linked_clusters": [
            "Player Engagement and Feedback"
          ]
        },
        {
          "concept": "Monetization Optimization",
          "linked_clusters": [
            "Monetization Strategy"
          ]
        },
        {
          "concept": "Anti-Piracy Measures",
          "linked_clusters": [
            "Combatting Piracy"
          ]
        },
        {
          "concept": "Innovation and Sustainability in Game Industry",
          "linked_clusters": [
            "Game Development and Industry Challenges"
          ]
        }
    ],
    "Categories": [
        {
          "name": "Player Feedback Integration",
          "description": "This category involves aspects related to incorporating player feedback into the development process to enhance player experience and engagement.",
          "related_concepts": [
            "Player-Centric Game Development"
          ],
          "real_examples": [
            "Developing the next game version based on direct player feedback received from surveys."
          ],
          "hypothetical_examples": [
            "Creating a new character in the game inspired by player suggestions."
          ],
          "non_examples": [
            "A developer deciding game features solely based on personal preferences."
          ],
          "rules": "Includes any action or decision that directly integrates feedback from players to improve the game."
        },
        {
          "name": "Monetization Strategy Enhancement",
          "description": "This category focuses on strategies implemented to optimize game monetization while maintaining player engagement and satisfaction.",
          "related_concepts": [
            "Monetization Optimization"
          ],
          "real_examples": [
            "Adjusting in-game purchase systems to align with player preferences for better financial performance."
          ],
          "hypothetical_examples": [
            "Introducing limited-time offers to incentivize player spending."
          ],
          "non_examples": [
            "Ignoring player experience to force frequent in-game purchases."
          ],
          "rules": "Includes methods aimed at improving the financial aspects of the game without compromising player enjoyment."
        },
        {
          "name": "Piracy Prevention Measures",
          "description": "This category involves strategies and actions taken to prevent unauthorized copying and distribution of games to protect intellectual property and revenue.",
          "related_concepts": [
            "Anti-Piracy Measures"
          ],
          "real_examples": [
            "Implementing secure online verification processes to restrict access to the game to legitimate buyers."
          ],
          "hypothetical_examples": [
            "Using unique game keys for each purchased copy to deter piracy."
          ],
          "non_examples": [
            "Offering free copies of the game on unofficial websites."
          ],
          "rules": "Includes any efforts to deter and reduce piracy of the game through technological or legal means."
        },
        {
          "name": "Industry Innovation Encouragement",
          "description": "This category pertains to promoting creativity and exploration among game developers to drive industry growth and sustainability.",
          "related_concepts": [
            "Innovation and Sustainability in Game Industry"
          ],
          "real_examples": [
            "Organizing industry events to showcase innovative game designs and concepts."
          ],
          "hypothetical_examples": [
            "Establishing grants for indie developers to pursue experimental game projects."
          ],
          "non_examples": [
            "Continuing with traditional game development practices without seeking innovation."
          ],
          "rules": "Encompasses activities that support new ideas and practices in game development for long-term success and advancement."
        }
    ],
    "Pilot Testing Results": [
        {
          "text": "The developers integrated suggestions from player surveys to create an expansion pack with new characters and features.",
          "initial_category": "Player Feedback Integration",
          "revised_category": "Player Feedback Integration"
        },
        {
          "text": "In an effort to boost revenue, the company introduced a time-limited exclusive offer for in-game purchases.",
          "initial_category": "Monetization Strategy Enhancement",
          "revised_category": "Monetization Strategy Enhancement"
        },
        {
          "text": "The game includes a unique online authentication system to prevent unauthorized distribution.",
          "initial_category": "Piracy Prevention Measures",
          "revised_category": "Piracy Prevention Measures"
        },
        {
          "text": "A new initiative was launched to encourage developers to experiment with unconventional game mechanics.",
          "initial_category": "Industry Innovation Encouragement",
          "revised_category": "Industry Innovation Encouragement"
        }
    ],
    "Complex Data": [
        {
          "index": 1,
          "name": "Complex Structure 1",
          "details": {
            "level_1": {
              "level_2": {
                "value": "Deeply nested value 1"
              }
            }
          }
        },
        {
          "index": 2,
          "name": "Complex Structure 2",
          "details": {
            "level_1": {
              "level_2": {
                "value": "Deeply nested value 2"
              }
            }
          }
        }
    ],
    "Super Simple": [
        {
          "only_field": "Simple Value"
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
