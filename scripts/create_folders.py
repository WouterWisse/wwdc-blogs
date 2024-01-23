# Define the template file path and output file path
template_file = "templates/_index.md"
output_file = "output.md"

# Define the content to replace placeholders
weight = 1000
date = "2022-06-06T10:00:00+01:00"
author = "Wouter Wise"
title = "WWDC 2022"
icon = "event"
description = "Slogan WWDC 2022"
publishdate = "2022-06-06T10:00:00+01:00"
tags = "['WWDC2022']"

# Read the template file
with open(template_file, "r") as file:
    template_content = file.read()

# Replace placeholders with actual content
template_content = template_content.replace("<WEIGHT>", weight)
template_content = template_content.replace("<DATE>", date)
template_content = template_content.replace("<AUTHOR>", author)
template_content = template_content.replace("<TITLE>", title)
template_content = template_content.replace("<ICON>", icon)
template_content = template_content.replace("<DESCRIPTION>", description)
template_content = template_content.replace("<PUBLISH_DATE>", publishdate)
template_content = template_content.replace("<TAGS>", str(tags))

# Write the modified content to the output file
with open(output_file, "w") as file:
    file.write(template_content)