import json
from graphviz import Digraph

# Sample JSON data (including a table that should not be printed)
data = """
```json
{
  "Theoretical Coding_relationships": [
    {
      "core_category_name": "Gaming Experience and Development",
      "relationship": "Family Influence on Gaming Preferences → Evolution of Gaming Preferences: Family dynamics shape individual preferences leading to evolution in gaming choices."      
    },
    {
      "core_category_name": "Gaming Experience and Development",
      "relationship": "Evolution of Gaming Preferences ↔ Game Development Challenges: Changes in gaming preferences influence the game development process and encountered challenges."     
    },
    {
      "core_category_name": "Gaming Experience and Development",
      "relationship": "Game Development Challenges → Gaming Community Interactions: Challenges in development impact community interactions within the gaming industry."
    }
  ],
  "Theoretical Coding_theoretical_codes": [
    {
      "core_category_name": "Gaming Experience and Development",
      "theoretical_code": "If family influences shape gaming preferences, then there is an evolution in individual gaming choices."
    },
    {
      "core_category_name": "Gaming Experience and Development",
      "theoretical_code": "The evolution of gaming preferences leads to encountered challenges in game development."
    },
    {
      "core_category_name": "Gaming Experience and Development",
      "theoretical_code": "Challenges in game development influence interactions within gaming communities."
    }
  ],
  "Theoretical Coding_theoretical_framework": [
    {
      "core_category_name": "Gaming Experience and Development",
      "framework_component": "Family Influence and Gaming Preferences",
      "description": "Shapes individual preferences and leads to an evolution in gaming choices."
    },
    {
      "core_category_name": "Gaming Experience and Development",
      "framework_component": "Evolution of Gaming Preferences",
      "description": "Influences encountered challenges in game development."
    },
    {
      "core_category_name": "Gaming Experience and Development",
      "framework_component": "Game Development Challenges",
      "description": "Impacts community interactions within the gaming industry."
    }
  ],
  "table_format_visualization": [
    {
      "CoreCategory": "Gaming Experience and Development",
      "Relationships": [
        {"From": "Family Influence on Gaming Preferences", "To": "Evolution of Gaming Preferences", "Description": "Family dynamics shape individual preferences leading to evolution in gaming choices."},
        {"From": "Evolution of Gaming Preferences", "To": "Game Development Challenges", "Description": "Changes in gaming preferences influence the game development process and encountered challenges."},
        {"From": "Game Development Challenges", "To": "Gaming Community Interactions", "Description": "Challenges in development impact community interactions within the gaming industry."}
      ]
    }
  ]
}
```

"""


# Function to wrap text
def wrap_text(text, max_length):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


# Function to create the combined flowchart
def create_combined_flowchart(data):
    # Function to clean and parse JSON data
    def clean_and_parse_json(response_text):
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise json.JSONDecodeError("Invalid JSON format", response_text, 0)
        response_text = response_text[start:end]
        return json.loads(response_text)

    # Parse JSON data
    json_data = clean_and_parse_json(data)

    # Filter the data to only include tables with "visualization" in their name
    filtered_data = {k: v for k, v in json_data.items() if "visualization" in k}

    # Create a single Digraph instance
    dot = Digraph()

    # Set global graph attributes for spacing
    dot.attr(rankdir='TB')  # Ensure top-to-bottom direction for entire graph

    # Process each CoreCategory in the filtered tables
    for i, table_data in enumerate(filtered_data["table_format_visualization"]):
        core_category = table_data["CoreCategory"]
        relationships = table_data["Relationships"]

        # Add a subgraph for each CoreCategory to maintain separation
        with dot.subgraph(name=f'cluster_{i}') as sub:
            sub.attr(label=core_category, rank='same', style='invis')
            nodes = set()
            for relation in relationships:
                description = wrap_text(relation["Description"], 40)
                # Create a left-aligned label with HTML-like line breaks
                formatted_description = '<' + description.replace('\n', '<br align="left"/>') + '>'
                sub.edge(relation["From"], relation["To"], label=formatted_description)
                nodes.add(relation["From"])
                nodes.add(relation["To"])

            # Set all nodes to be rectangles
            for node in nodes:
                sub.node(node, shape='rect')

    return dot


# Function to save the flowchart as a PNG file
def save_flowchart_as_png(dot, filename):
    # Render the combined flowchart as a PNG file
    dot.render(filename, format='png', cleanup=True)
    print(f"Combined flowchart image generated and saved as {filename}.png")








# Create the combined flowchart
dot = create_combined_flowchart(data)

# Save the flowchart as a PNG file
save_flowchart_as_png(dot, 'combined_flowchart')

# Create an HTML file to display the combined flowchart
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Flowcharts</title>
</head>
<body>
    <h1>Combined Flowcharts</h1>
    <img src="combined_flowchart.png" alt="Combined Flowcharts">
</body>
</html>
"""

# Write the HTML content to a file
html_file_name = 'combined_flowcharts.html'
with open(html_file_name, 'w') as f:
    f.write(html_content)

print(f"HTML file generated and saved as {html_file_name}")
print(f"Open {html_file_name} in your browser to view the combined flowcharts.")
