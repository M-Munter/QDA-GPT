import json
from graphviz import Digraph

# Sample JSON data
data = """
{
  "table_format_visualization": [
    {
      "CoreCategory": "Employee Well-being",
      "Relationships": [
        {"From": "Leadership Support", "To": "Emotional Support", "Description": "Effective leadership practices foster a supportive team environment, enhancing emotional support among peers."},
        {"From": "Emotional Support", "To": "Professional Development", "Description": "A supportive team environment encourages employees to engage in professional development opportunities."},
        {"From": "Professional Development", "To": "Employee Well-being", "Description": "Access to training and career advancement opportunities directly contributes to higher job satisfaction and overall well-being."},
        {"From": "Work-Life Balance", "To": "Employee Well-being", "Description": "Flexible work arrangements help employees manage stress and improve their overall well-being."}
      ]
    }
  ]
}
"""

# Parse the JSON data
json_data = json.loads(data)


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


# Function to create flowchart
def create_flowchart(data, max_description_length=40):
    dot = Digraph()

    # Set global graph attributes for spacing
    dot.attr(ranksep='1.0', nodesep='0.75')

    relationships = data["table_format_visualization"][0]["Relationships"]
    nodes = set()
    for relation in relationships:
        description = wrap_text(relation["Description"], max_description_length)
        # Create a left-aligned label with HTML-like line breaks
        formatted_description = '<' + description.replace('\n', '<br align="left"/>') + '>'
        dot.edge(relation["From"], relation["To"], label=formatted_description)
        nodes.add(relation["From"])
        nodes.add(relation["To"])

    # Set all nodes to be rectangles
    for node in nodes:
        dot.node(node, shape='rect')

    return dot


# Create the flowchart
dot = create_flowchart(json_data)
# Render the flowchart as a PNG file
dot.render('flowchart', format='png')

# Create an HTML file to display the flowchart
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flowchart</title>
</head>
<body>
    <h1>Flowchart</h1>
    <img src="flowchart.png" alt="Flowchart">
</body>
</html>
"""

# Write the HTML content to a file
with open('flowchart.html', 'w') as f:
    f.write(html_content)

print("Flowchart generated and saved as flowchart.png")
print("HTML file generated and saved as flowchart.html")
print("Open flowchart.html in your browser to view the flowchart.")
