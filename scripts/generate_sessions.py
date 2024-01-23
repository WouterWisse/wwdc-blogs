import os
import json
from jinja2 import Environment, FileSystemLoader

# Configuration variables
event_year = "2014"  # Set the year of the event here
output_directory = os.path.join('..', 'content', 'docs', f'wwdc-{event_year}')
json_file_path = os.path.join('data', f'wwdc_{event_year}_sessions.json')
template_file_path = os.path.join('templates', 'session_index_template.md')

# Create a Jinja2 environment with the template folder
env = Environment(loader=FileSystemLoader('templates'))

with open(json_file_path, 'r') as json_file:
    events_data = json.load(json_file)

# Load the template
template = env.get_template('index_template.md')

# Convert boolean values to lowercase strings in the JSON data
for event in events_data['event']:
    event['draft'] = str(event['draft']).lower()
    event['toc'] = str(event['toc']).lower()

for event_category in events_data['event']:
    category_folder_name = event_category['category']['title'].lower().replace(" ", "-")
    category_output_path = os.path.join(output_directory, category_folder_name)
    os.makedirs(category_output_path, exist_ok=True)

    for session in event_category['sessions']:
        session_folder_name = session['title'].lower().replace(" ", "-")
        session_output_path = os.path.join(category_output_path, session_folder_name)
        os.makedirs(session_output_path, exist_ok=True)

        # Render the template with session data
        index_content = template.render(session)

        with open(os.path.join(session_output_path, '_index.md'), 'w') as index_file:
            index_file.write(index_content)

print(f"Folders and _index.md files created in '{output_directory}' successfully.")
