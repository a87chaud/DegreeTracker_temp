from scraper import Scraper

def main():
    url = "https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/programs/rkDkJCAj2?searchTerm=computational%20math&bc=true&bcCurrent=Computational%20Mathematics%20(Bachelor%20of%20Mathematics%20-%20Honours)&bcItemType=programs"
    fp = "comp_math.txt"
    grad_req_class = "style__noFade___3YZlf"
    course_req_class = "style__noFade___3YZlf"
    compMath = Scraper(url,fp, grad_req_class, course_req_class)
    compMath.load_html()
    compMath.get_html()
    compMath.scrape_grad_requirement()
    compMath.scrape_course_requirements()
    compMath.testing()


if __name__ == "__main__":
    main()

    