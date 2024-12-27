from bs4 import BeautifulSoup
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class Major:
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
        # div_tags = self.soup.find_all("div", class_=self.course_req_class)
        
        # for nested_tags in div_tags:
        #     ul_tags = nested_tags.find_all("ul")
        #     for ul in ul_tags:
        #         self.course_reqs += "PARENT CATEGORY" + '\n'
        #         li_tags = ul.find_all("li")
        #         for li in li_tags:
        #             self.course_reqs += li.get_text(strip=True) + '\n'
        course_requirements_section = self.soup.find('h3', string='Course Requirements')
        course_requirements_list = course_requirements_section.find_next('ul')
        # print(type(course_requirements_list))
        ##################### FOR TESTING ONLY #######################
        # testing = [ul.get_text(strip=True)  + '\n' for ul in course_requirements_list.find_all('ul')]
        # print(testing[0])
        # for t in testing:
            # print(t)
        
        for children in course_requirements_list.descendants:
            print(children)
            


        counter = 0
        # li_list = course_requirements_list.find_all('li',recursive=True)
        # for li in li_list:
        #     text = li.get_text(separator=' ', strip=True)
        #     nested_ul = li.find('ul')
        #     if nested_ul:
        #         print('NESTED UL')
        #         print(nested_ul.get_text(separator=' ', strip=True))
        #     if "Complete" in text:
        #         # print(text)
        #         counter += 1
        print(counter)
                
        
        #############################################################
        # course_req_ul_arr = [ul.get_text(strip=True) for ul in course_requirements_section.find_all('ul')]
        # for a in course_req_ul_arr:
        #     print(a)
        
        # li_list = course_requirements_list.find_all('li')
        # course_requirements_arr = [li.get_text(strip=True) for li in li_list]
        
        # for c in course_requirements_arr:
            # self.course_reqs += c + '\n'


    # FOR TESTING ONLY TO BE REMOVED
    def testing(self):
        with open("testing_grad.txt", "w") as f:
            f.write(self.grad_reqs)
        with open("testing_course.txt", "w") as f2:
            f2.write(self.course_reqs)


class CompMath(Major):
    def extract_list_requirements():
        pass
    