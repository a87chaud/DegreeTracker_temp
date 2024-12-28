from scraper import *

def main():
    # url = "https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/rkDkJCAj2?searchTerm=computational%20math&bc=true&bcCurrent=Computational%20Mathematics%20(Bachelor%20of%20Mathematics%20-%20Honours)&bcItemType=programs"
    url = "https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/H1z0kJR0in?searchTerm=math&bc=true&bcCurrent=Mathematical%20Studies%20(Bachelor%20of%20Mathematics%20-%20Honours)&bcItemType=programs"
    
    fp = "reg_math.txt"
    grad_req_class = "style__noFade___3YZlf"
    course_req_class = "style__noFade___3YZlf"
    compMath = CompMath(url,fp, grad_req_class, course_req_class)
    compMath.load_html()
    compMath.get_html()
    compMath.scrape_grad_requirement()
    compMath.scrape_course_requirements()
    # compMath.extract_list_requirements()
    compMath.testing()


if __name__ == "__main__":
    main()

    