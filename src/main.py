import webapp2
import re
import os
import jinja2
import PrereqParser
import json
from Course2 import Course2
jinja = jinja2.Environment( loader=jinja2.FileSystemLoader( os.path.join( os.path.dirname(__file__), '') ) )

from models import Requisite, RequisiteList, Course
from lxml import html
from google.appengine.api import urlfetch
        
        
class APIHandler(webapp2.RequestHandler):
    """
    API Request Handler

    Example query: http://localhost:{port}/api?dept=ECE&course=30200
    Used for diagnostics; outputs parsed course parameters
    If no department or course is specified, it defaults to ECE 20100
    """
    def get(self):
        #dept = self.request.get("dept") or "ECE"
        #course = self.request.get("course") or "20100"

        ident = self.request.get("id") or "ECE20100"

        with open("course_data.json") as data:
            courses = json.loads(data.read())
        
        # test course add function, and retrieve the course
        #text = get_course(dept, course)
        #insert_course(dept, course, text)
        #c = Course.get_by_id("{d}{c}".format(d=dept, c=course))
        
        # output the description as a test
        self.response.headers['Content-Type'] = 'text/html'

        print courses[ident]

        template = jinja.get_template('course.html')
        html = template.render(course=courses[ident])

        self.response.write(html)
        
        # output collected parameters to verify accuracy
        
        # self.response.write("<h1>{dept} {num} - {title} ({cr} Credits)</h1>".format(dept = c.department, num = c.number, cr=c.credits, title=c.title))
        # self.response.write("<h2>Description</h2>")
        # self.response.write(c.description)
        # self.response.write("<h2>Semesters Offered</h2>")
        # self.response.write(c.semesters)
        # self.response.write("<h2>Campuses</h2>")
        # self.response.write(c.campuses)
        # self.response.write("<h2>Course Format</h2>")
        # self.response.write(c.form)
        # self.response.write("<h2>Requisites</h2>")
        # self.response.write(c.requisites)
    
class RawHandler(webapp2.RequestHandler):
    """
    Raw Handler

    Example query: http://localhost:{port}/raw?dept=ECE&course=30200
    Used for diagnostics; outputs plain text retrieved from Purdue's Catalog
    If no department or course is specified, it defaults to ECE 20100
    """
    def get(self):
        dept = self.request.get("dept") or "ECE"
        course = self.request.get("course") or "20100"
        text = get_course(dept, course)
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(text)
        
class AdminHandler(webapp2.RequestHandler):
    """
    Admin Handler

    Example query: http://localhost:{port}/admin
    Used for diagnostics; outputs the total list of purdue courses
    """
    def get(self):
        courses = export_courses()
        
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write("Welcome to the Admin Handler\n")
        # self.response.write("There are {num} courses\n".format(num=len(courses)))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(courses))

class JSONHandler(webapp2.RequestHandler):
    """
    Make JSON List

    Example query: http://localhost:{port}/json
    Creates a JSON list of courses from purdue course catalog HTML file
    """
    def get(self):
        with open("purdue_catalog.html") as data:
            html = data.read()
            m = re.findall("detail\?cat_term_in=\d{6}&amp;subj_code_in\=\w+&amp;crse_numb_in=[\d\w]{5}\">(\w+ [\d\w]{5}) - [\w ]*", html)
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(m)

###############################
## Utility Functions
###############################

def export_courses():
    """
    export_courses

    get all courses from the database
    return all courses as a dictionary of course dictionaries
    """
    courses = Course.query().fetch()
    dictionary = {}

    for course in courses:
        dictionary[course.department + "" + course.number] = course.to_dict()

    return dictionary
        
def update_db():
    """ 
    update_db

    Updates the database with all the courses for the current semester
    """
    
    with open("courses_2016.json") as data:
        data = data.read()

        courses = json.loads(data)

        for course in courses:
            try:
                [dept, course] = course.split(" ")
                text = get_course(dept, course)
                insert_course(dept, course, text)
            except:
                failures.append(course)

def check_db():
    """ 
    check_db

    Compares the database entries with the entire list of courses
    Returns a list of courses that failed to insert into the database
    """
    
    with open("courses_2016.json") as data:
        data = data.read()

        courses = json.loads(data)
        course_keys_in_db = Course.query().fetch(keys_only=True)

        db_list = []
        failures = []

        for course in course_keys_in_db:
            db_list.append(course.id())
        failures = [i for i in courses if i.replace(" ","") not in db_list]

        return failures

def get_course(dept, num):
    """ Retrieves the raw course text from the Purdue course catalog """
    
    # semester: 10 = Fall, 20 = Spring, 30 = Summer
    host = "https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_course_detail"
    query = "?cat_term_in={term}&subj_code_in={dept}&crse_numb_in={num}".format(term="201620", dept=dept, num=num)
    urlfetch.set_default_fetch_deadline(600)
    result = urlfetch.fetch(host+query)
    
    if result.status_code == 200:
        tree = html.fromstring(result.content)
        text = tree[1][4][2].text_content()   # get just the relevant text of the webpage 

        # remove unicode non-breaking spaces to allow regexing
        text = text.replace(u'\xa0',u' ')
        return text
    
def insert_course(dept, num, text):
    """ Regexes for extracting class properties; results go into capture group 1 """

    # Course Title  
    m = re.search("[\d\w]{5} - ([\w ]*)", text)
    title = m.group(1) if m else "nomatch"

    # Course Description
    m = re.search("\.\s(.*)\sTypically",text)
    des = m.group(1) if m else "nomatch"

    # Credit hours aren't fixed for every course
    # Credit Hours: 2.00
    # Credit Hours: 2.00 or 3.00. 
    # Credit Hours: 1.00 to 18.00. 
    m = re.search("Credit Hours: (\d+\.\d+)",text, flags=re.IGNORECASE)
    m = re.search("(\d+\.\d+)(.*?)Credit hours",text, flags=re.IGNORECASE) if not m else m
    cr = m.group(1) if m else "-1"

    # Semesters Offered
    m = re.search("Typically offered (.*?)\.", text)
    sem = m.group(1).split() if m else ["nomatch"]

    # Course Type: Lecture, Recitation, Lab, Seminar, etc.
    m = re.search("Schedule Types:\s((?:[\w ]+)(?:,[\w ]+)*) \s+", text)
    form = m.group(1).split(", ") if m else ["nomatch"]

    # Learning objectives will not necessarily follow campuses
    m = re.search("campuses:(\s+([\w\s])+\n)", text)
    campus = m.group(1).strip().split("\n\n") if m else ["nomatch"]
    campus = [camp.strip() for camp in campus]

    # prereq regex and decomosition of prereqs into lists of AND conditions (works for most classes, not 477 and similar)
    # re.DOTALL matches all characters, including "\n"
    idx = text.find("campuses:")
    m = re.search("Prerequisites:(.*)",text[idx:],flags=re.DOTALL)
    if m:
        allReqs = []
        prereqText = m.group(1).strip()
        prereqText =  prereqText.encode('ascii', 'ignore') 
        for i in PrereqParser.parseprereq(prereqText):
            reqArr = []
            for j in i.split():
                if j.find("-C") != -1:
                    j = j.replace("-C","")
                    reqArr.append(Requisite(course=j,reqType=False))
                else:
                    reqArr.append(Requisite(course=j,reqType=True))                    
            allReqs.append(RequisiteList(courses=reqArr))

    else:
        allReqs = []

    # create course entity
    course = Course(number=num, title=title, department=dept, form=form,
                     description=des, credits=float(cr), semesters=sem,
                     campuses=campus,requisites=allReqs, id=dept + num)
    # store course 
    course.put()


            
app = webapp2.WSGIApplication([
    ('/admin/?', AdminHandler),
    ('/json/?', JSONHandler),
    ('/api/?', APIHandler),
    ('/raw/?', RawHandler)
], debug=True)
