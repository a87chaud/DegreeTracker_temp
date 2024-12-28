from bs4 import BeautifulSoup
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json

class Major:
    soup = ""
    grad_reqs = ""
    course_reqs = ""
    formatted_requirements = []
    # Passing in the URL to scrape as well as the fp for the html file
    def __init__(self, url: str, html_out_fp: str, grad_req_class: str, course_req_class: str) -> None:
        print('Init done')
        self.url = url
        self.html_out_fp = html_out_fp
        # HTMl class for grad req
        self.grad_req_class = grad_req_class 
        # HTML class for course req
        self.course_req_class = course_req_class
    
            
    def load_html(self) -> None:    
        print('Entered')
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.url)
            page.wait_for_load_state('networkidle') 
            html = page.content()
            with open(self.html_out_fp, "w") as f:
                f.write(html)
            
            print(f"Written to {self.html_out_fp}")
            browser.close()

    def get_html(self) -> None:
        with open(self.html_out_fp, "r", encoding="utf-8") as file:
            html = file.read()

        self.soup = BeautifulSoup(html, "html.parser")
    
    def scrape_grad_requirement(self) -> str:
        # Find all div tags with the specified class
        div_tags = self.soup.find_all("div", class_=self.grad_req_class)
                
        for nested_tags in div_tags:
            ul_tags = nested_tags.find_all("ul")
            for ul in ul_tags:
                self.grad_reqs += ul.get_text(strip=True) + '\n'
    
    def scrape_course_requirements(self) -> list:

        # Parent requirement header
        parent_header = self.soup.find('span', string='Required Courses')
        # Alternative parent for the div tag
        if not parent_header:
            # Check if we are dealing with the div case
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

        self.formatted_requirements = extract_items(parent_list)


    # FOR TESTING ONLY TO BE REMOVED
    def testing(self):
        with open("testing_grad.txt", "w") as f:
            # output = json.dumps(self.scrape_grad_requirement(), indent=2)
            f.write(self.grad_reqs)
        with open("testing_course.txt", "w") as f2:
            f2.write(self.course_reqs)
        with open("testing_categories.txt", "w") as f3:
            f3.write(json.dumps(self.formatted_requirements, indent=2))


class CompMath(Major):
    def extract_list_requirements(self):
        # Parent requirement header
        parent_header = self.soup.find('div', string='List 1')
        
        if not parent_header:
            print("No requirements found")
            return
            

        parent_list = parent_header.find_next('ul')
        if not parent_list:
            print("No requirements list found")
            return
        def extract_items(ul):
            items = []
            for li in ul.find_all('li', recursive=False):
                span = li.find('span')
                div = li.find('div')
                if span:
                    text = span.get_text(strip=True)
                    if "Complete" in text:
                        text = "ALL"
                elif div:
                    text = div.get_text(strip=True)
                else:
                    "No text found"

                # Check if nested list
                nested_ul = li.find('ul')
                if nested_ul:
                    
                    # Special cases
                    if nested_ul.get('data-test') == 'ruleView-G':
                        items.append({
                        'text': text,
                        'children': extract_items(nested_ul)
                        })
                    elif nested_ul.get('data-test') == 'ruleView-F':
                        items.append({
                        'text': text,
                        'children': extract_items(nested_ul)
                        })
                    # General case
                    else:
                        items.append({
                        'text': text,
                        'children': extract_items(nested_ul)
                        })    
                else:
                    items.append({'text': text})

            return items

        self.formatted_requirements += extract_items(parent_list)

    def scrape_course_requirements(self) -> list:

        # Parent requirement header
        parent_header = self.soup.find('span', string='Required Courses')
        
        if not parent_header:
            return "No requirements found"
            

        parent_list = parent_header.find_next('ul')
        if not parent_list:
            return "No requirements list found"

        def extract_items(ul):
            items = []
            for li in ul.find_all('li', recursive=False):
                span = li.find('span')
                div = li.find('div')
                if span:
                    text = span.get_text(strip=True)
                    if "Complete" in text:
                        text = "ALL"
                elif div:
                    text = div.get_text(strip=True)
                else:
                    "No text found"

                # Check if nested list
                nested_ul = li.find('ul')
                if nested_ul:
                    
                    # Special cases
                    if nested_ul.get('data-test') == 'ruleView-G':
                        items.append({
                        'text': text,
                        'children': extract_items(nested_ul)
                        })
                    elif nested_ul.get('data-test') == 'ruleView-F':
                        items.append({
                        'text': text,
                        'children': extract_items(nested_ul)
                        })
                    # General case
                    else:
                        items.append({
                        'text': text,
                        'children': extract_items(nested_ul)
                        })    
                else:
                    items.append({'text': text})

            return items

        self.formatted_requirements += extract_items(parent_list)

        
        
    