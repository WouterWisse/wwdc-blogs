import os
import json
import re
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Prompt the user for the event year
event_year = input("Please enter the WWDC Event year (e.g., 2014): ")

# Determine the JSON file path based on the entered year
json_file_path = os.path.join('data', 'sessions', event_year, 'sessions.json')

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file for WWDC {event_year} sessions not found.")
    exit(1)

# Configuration variables
output_directory = os.path.join('..', 'content', 'docs', f'wwdc-{event_year}')
current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')

# Create a Jinja2 environment with the template folder
env = Environment(loader=FileSystemLoader('templates'))

# Load the template for sessions and category index
session_template = env.get_template('session_index_template.md')
category_index_template = env.get_template('category_index_template.md')

with open(json_file_path, 'r') as json_file:
    events_data = json.load(json_file)

def clean_filename(filename):
    # Remove characters like '&' from the filename
    return re.sub(r'[^a-zA-Z0-9]+', '-', filename)

event_category_index = 1
for event_category in events_data.get('event', []):
    category_folder_name = clean_filename(event_category['category']['title'].lower())
    category_output_path = os.path.join(output_directory, category_folder_name)
    os.makedirs(category_output_path, exist_ok=True)

    # Render the category index template with the provided data
    category_index_content = category_index_template.render(
        category=event_category['category'],
        categories=events_data.get('event', []),
        weight=event_category_index,
        title=event_category['category']['title'],
        icon=event_category['category']['icon'],
        description=f"WWDC {event_year} - {event_category['category']['title']}",
        date=current_date,
        publishdate=current_date,
        tags=event_category['category']['tags']
    )

    # Write the category index to the category folder
    category_index_file_path = os.path.join(category_output_path, '_index.md')
    with open(category_index_file_path, 'w') as category_index_file:
        category_index_file.write(category_index_content)

    session_index = 1
    for session in event_category.get('sessions', []):
        session_file_name = clean_filename(session['title'].lower()) + '.md'
        session_file_path = os.path.join(category_output_path, session_file_name)

        # Set date and publishdate to current date
        session['date'] = current_date
        session['publishdate'] = current_date
        session['weight'] = session_index
        session['tags'] = session.get('tags', []) + event_category['category']['tags'] # also add the category tags.
        session_index += 1

        # Render the template with session data
        index_content = session_template.render(session)

        with open(session_file_path, 'w') as session_file:
            session_file.write(index_content)

    event_category_index += 1
print(f"WWDC Sessions and Category Index successfully set up in '{output_directory}'.")
