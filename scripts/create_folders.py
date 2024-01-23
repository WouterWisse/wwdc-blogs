import os
import json

output_directory = os.path.join('..', 'content', 'docs')
json_file_path = os.path.join('templates', 'wwdc_events.json')
template_file_path = os.path.join('templates', 'template.md')

with open(json_file_path, 'r') as json_file:
    events_data = json.load(json_file)

with open(template_file_path, 'r') as template_file:
    template_str = template_file.read()

for event in events_data['events']:
    folder_name = event['title'].lower().replace(" ", "-")
    output_path = os.path.join(output_directory, folder_name)
    os.makedirs(output_path, exist_ok=True)

    index_content = template_str.format(
        weight=event['weight'],
        date=event['date'],
        draft=event['draft'],
        author=event['author'],
        title=event['title'],
        icon=event['icon'],
        toc=event['toc'],
        description=event['description'],
        publishdate=event['publishdate'],
        tags=event['tags']
    )

    with open(os.path.join(output_path, '_index.md'), 'w') as index_file:
        index_file.write(index_content)

print(f"Folders and _index.md files created in '{output_directory}' successfully.")