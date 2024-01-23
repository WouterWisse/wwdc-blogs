import os
import json
from jinja2 import Environment, FileSystemLoader

# Configuration variables
output_directory = os.path.join('..', 'content', 'docs')
json_file_path = os.path.join('data', 'wwdc_events.json')
template_file_path = os.path.join('templates', 'event_index_template.md')

# Create a Jinja2 environment with the template folder
env = Environment(loader=FileSystemLoader('templates'))

with open(json_file_path, 'r') as json_file:
    events_data = json.load(json_file)

# Load the template
template = env.get_template('index_template.md')

# Convert boolean values to lowercase strings in the JSON data
for event in events_data['events']:
    event['draft'] = str(event['draft']).lower()
    event['toc'] = str(event['toc']).lower()

for event in events_data['events']:
    folder_name = event['title'].lower().replace(" ", "-")
    output_path = os.path.join(output_directory, folder_name)
    os.makedirs(output_path, exist_ok=True)

    # Render the template with JSON data
    index_content = template.render(event)

    with open(os.path.join(output_path, '_index.md'), 'w') as index_file:
        index_file.write(index_content)

print(f"Folders and _index.md files created in '{output_directory}' successfully.")
