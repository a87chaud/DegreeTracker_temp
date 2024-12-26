from bs4 import BeautifulSoup
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class Scraper:
    soup = ""
    grad_reqs = ""
    course_reqs = ""
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
    
    def scrape_grad_requirement(self) -> None:
        # Find all div tags with the specified class
        div_tags = self.soup.find_all("div", class_=self.grad_req_class)
                
        for nested_tags in div_tags:
            ul_tags = nested_tags.find_all("ul")
            for ul in ul_tags:
                self.grad_reqs += ul.get_text(strip=True) + '\n'
                
    def scrape_course_requirements(self) -> None:
        div_tags = self.soup.find_all("div", class_=self.course_req_class)
        
        for nested_tags in div_tags:
            ul_tags = nested_tags.find_all("ul")
            for ul in ul_tags:
                self.course_reqs += "PARENT CATEGORY" + '\n'
                li_tags = ul.find_all("li")
                for li in li_tags:
                    self.course_reqs += li.get_text(strip=True) + '\n'

    # FOR TESTING ONLY TO BE REMOVED
    def testing(self):
        with open("testing_grad.txt", "w") as f:
            f.write(self.grad_reqs)
        with open("testing_course.txt", "w") as f2:
            f2.write(self.course_reqs)
         
        