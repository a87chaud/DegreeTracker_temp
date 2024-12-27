from bs4 import BeautifulSoup

# Assuming the HTML content is already read into `html_content`
file_path = '/Users/ananyatrivedi/Projects/DegreeTracker/DegreeTracker_temp/requirements.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Function to extract and format requirements
def extract_requirements(soup):
    formatted_requirements = []

    # Find the parent requirement header
    parent_header = soup.find('span', string='Required Courses')
    if not parent_header:
        return "No requirements found"

    # Traverse the structure to find list items
    parent_list = parent_header.find_next('ul')
    if not parent_list:
        return "No requirements list found"

    def extract_items(ul):
        items = []
        for li in ul.find_all('li', recursive=False):
            # Safely extract text from the current list item
            span = li.find('span')
            text = span.get_text(strip=True) if span else "No text found"

            # Check if the list item has a nested list
            nested_ul = li.find('ul')
            if nested_ul:
                items.append({
                    'text': text,
                    'children': extract_items(nested_ul)
                })
            else:
                items.append({'text': text})

        return items

    # Process the parent list
    formatted_requirements = extract_items(parent_list)

    return formatted_requirements

# Extract the requirements
requirements = extract_requirements(soup)

# Display the structured requirements
import json
output = json.dumps(requirements, indent=2)
print(output)

# Optionally, save the structured data to a file
with open('requirements.json', 'w') as f:
    f.write(output)
