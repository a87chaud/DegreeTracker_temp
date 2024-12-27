from bs4 import BeautifulSoup

file_path = '/Users/ananyatrivedi/Projects/DegreeTracker/DegreeTracker_temp/requirements.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

def extract_requirements(soup):
    formatted_requirements = []

    # Parent requirement header
    parent_header = soup.find('span', string='Required Courses')
    if not parent_header:
        return "No requirements found"

    parent_list = parent_header.find_next('ul')
    if not parent_list:
        return "No requirements list found"

    def extract_items(ul):
        items = []
        for li in ul.find_all('li', recursive=False):
            span = li.find('span')
            text = span.get_text(strip=True) if span else "No text found"

            # Check if nested list
            nested_ul = li.find('ul')
            if nested_ul:
                items.append({
                    'text': text,
                    'children': extract_items(nested_ul)
                })
            else:
                items.append({'text': text})

        return items

    formatted_requirements = extract_items(parent_list)

    return formatted_requirements

# Extract the requirements
requirements = extract_requirements(soup)

import json
output = json.dumps(requirements, indent=2)
print(output)