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
    requirement_num = 0
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
    def extraction_helper_function(self, tag:str) -> str:
        text = ""
        tag_to_check = tag.replace(" ", "")
        if "Completeall" in tag_to_check:
            text = "ALL"
        elif "Chooseany" in tag_to_check:
            print('Entered here2')
            text = "ANY"
        elif ("Complete" in tag_to_check and "1" in tag_to_check) or (len(tag_to_check) == 1 and tag_to_check == "1"):
            text = "ONE"
        elif ("Complete" in tag_to_check and "2" in tag_to_check) or (len(tag_to_check) == 1 and tag_to_check == "2"):
            text = "TWO"
        else:
            print("tag: " + tag)
            text = tag
        return text
        

    def extract_list_requirements(self):
        # Parent requirement header
        parent_header_arr = [
            self.soup.find('div', string='List 1'),
            self.soup.find('div', string='List 2'),
            self.soup.find('div', string='List 3'),
        ]
        counter = 1
        for parent_header in parent_header_arr:
            print(f'List {counter}')
            counter += 1
            print('#########################')
            if not parent_header:
                print("No requirements found")
                return
            parent_list = parent_header.find_next('ul')
            if not parent_list:
                print("No requirements list found")
                return

            def extract_items(ul, id):
                items = []
                for li in ul.find_all('li', recursive=False):
                    span = li.find('span')
                    div = li.find('div')
                    is_both = False
                    if div and span:
                        # Process both div and span
                        is_both = True

                    if div:
                        text_div = div.get_text(strip=True)
                        text_div_check = text_div.replace(" ", "")
                        ############# BUG FIXING ###############
                        print('Text in div(list req): ' + text_div_check)
                        ########################################
                        text = self.extraction_helper_function(text_div)
                        if not is_both:
                            # Skip the rest of processing
                            continue

                    if span:
                        text_span = span.get_text(strip=True)
                        text_span_check = text_span.replace(" ", "")
                        ############# BUG FIXING ###############
                        # print('Text in span(list req): ' + text_span_check)
                        ########################################
                        text = self.extraction_helper_function(text_span)
                    else:
                        print("No text found")
                    if div and span:
                        print("parent header text: " + parent_header.text)
                        if parent_header.text == "List 1":
                            if text_span:
                                text = self.extraction_helper_function(text_span)
                            else:
                                text = self.extraction_helper_function(text_div)
                        
                        elif parent_header.text == "List 2":
                            if text_span:
                                text = self.extraction_helper_function(text_span)
                            else:
                                text = self.extraction_helper_function(text_div)
                        
                        elif parent_header.text == "List 3":
                            if text_div:
                                text = self.extraction_helper_function(text_div)
                            else:
                                text = self.extraction_helper_function(text_span)
                    # Check if nested list
                    nested_ul = li.find('ul')
                    if nested_ul:
                        self.requirement_num += 1
                        id = self.requirement_num
                        items.append({
                        'requirement_num':f'requirement_{id}',
                        'tag': text,
                        'children': extract_items(nested_ul,id)
                        })   
                    else:
                        items.append({'text': text})

                return items

            self.formatted_requirements += extract_items(parent_list,0)

    def scrape_course_requirements(self) -> list:

        # Parent requirement header
        parent_header = self.soup.find('span', string='Required Courses')
        
        if not parent_header:
            return "No requirements found"
            

        parent_list = parent_header.find_next('ul')
        if not parent_list:
            return "No requirements list found"

        def extract_items(ul,id):
            items = []
            for li in ul.find_all('li', recursive=False):
                span = li.find('span')
                div = li.find('div')
                if span:
                    text = span.get_text(strip=True)
                    ############# BUG FIXING ###############
                    # print('Text in span: ' + text)
                    ########################################
                    if "Complete all" in text:
                        text = "ALL"
                if div:
                    text = div.get_text(strip=True)    
                    ############# BUG FIXING ###############
                    # print('Text in div: ' + text)
                    ########################################                
                    if "Complete all" in text:
                        text = "ALL"
                    elif "Complete1" in text:
                        text = "ONE"
                    elif "Complete2" in text:
                        text = "TWO"
                else:
                    "No text found"

                # Check if nested list
                nested_ul = li.find('ul')
                if nested_ul:
                    self.requirement_num += 1
                    id = self.requirement_num
                    items.append({
                    'requirement_num':f'requirement_{id}',
                    'tag': text,
                    'children': extract_items(nested_ul,id)
                    })    
                else:
                    items.append({'text': text})

            return items

        self.formatted_requirements += extract_items(parent_list,0)

        
        
    