import webapp2
import re
import PrereqParser

from lxml import html
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

###############################
## Database Models
##
## Reference: https://cloud.google.com/appengine/docs/python/ndb/properties
###############################

########################
## Requisite
########################
    
class Requisite(ndb.Model):
    course = ndb.StringProperty()   # course code, eg. "ECE20100"
    # changed name to reqType, type is a keyword
    reqType = ndb.BooleanProperty() # represents prerequisite (1) or co-requisite (0)

########################
## RequisiteList
## See: https://cloud.google.com/appengine/docs/python/ndb/properties#structured
########################
    
class RequisiteList(ndb.Model):
    courses = ndb.LocalStructuredProperty(Requisite, repeated=True)   # list of AND conditions

#################
## Course Model
#################

class Course(ndb.Model):
    title = ndb.StringProperty()        # unicode string up to 1500 bytes
    description = ndb.TextProperty()    # unicode string of unlimited length
    form = ndb.StringProperty(repeated=True)        # unicode string up to 1500 bytes
    number = ndb.IntegerProperty()      # 64-bit signed integer      
    credits = ndb.FloatProperty()		# float because some classes have half credits (source: I got 3.5 credits for ENGR 141/2)
    department = ndb.StringProperty()
    semesters = ndb.StringProperty(repeated=True)
    campuses = ndb.StringProperty(repeated=True)
    requisites = ndb.LocalStructuredProperty(RequisiteList, repeated=True) # lists of complete OR conditions
        
#######################
## API Request Handler
##
## Example query: http://localhost:{port}/api?dept=ECE&course=30200
## Outputs parsed course parameters
## If no department or course is specified, it defaults to ECE 20100
######################   
        
class APIHandler(webapp2.RequestHandler):
    def get(self):
        dept = self.request.get("dept") or "ECE"
        course = self.request.get("course") or "20100"
        #html.parse("catalog.html")
        
        # test course add function, and retrieve the course
        text = get_course(dept, course)
        insert_course(dept, course, text)
        c = Course.get_by_id("{d}{c}".format(d=dept, c=course))
        
        # output the description as a test
        self.response.headers['Content-Type'] = 'text/html'
        
        # output collected parameters to verify accuracy
        
        self.response.write("<h1>{dept} {num} - {title} ({cr} Credits)</h1>".format(dept = c.department, num = c.number, cr=c.credits, title=c.title))
        self.response.write("<h2>Description</h2>")
        self.response.write(c.description)
        self.response.write("<h2>Semesters Offered</h2>")
        self.response.write(c.semesters)
        self.response.write("<h2>Campuses</h2>")
        self.response.write(c.campuses)
        self.response.write("<h2>Course Format</h2>")
        self.response.write(c.form)
        self.response.write("<h2>Requisites</h2>")
        self.response.write(c.requisites)
        
#######################
## Raw Handler
##
## Example query: http://localhost:{port}/raw?dept=ECE&course=30200
## Outputs plain text retrieved from Purdue's Catalog
######################
    
class RawHandler(webapp2.RequestHandler):
    def get(self):
        dept = self.request.get("dept") or "ECE"
        course = self.request.get("course") or "20100"
        text = get_course(dept, course)
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(text)
        
class AdminHandler(webapp2.RequestHandler):
    def get(self):
        courses = update_db()
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("Welcome to the Admin Handler\n")
        self.response.write("There are {num} courses".format(num=len(courses)))
        
###############################
## Utility Functions
###############################
        
def update_db():
    with open("purdue_catalog.html") as data:
        data = data.read()

        m = re.findall("detail\?cat_term_in=\d{6}\&subj_code_in\=\w+&crse_numb_in=[\d\w]{5}\">(\w+ [\d\w]{5}) - [\w ]*", data)
        courses = m if m else "nomatch"

        return courses

def get_course(dept, num):
    host = "https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_course_detail"
    query = "?cat_term_in={term}&subj_code_in={dept}&crse_numb_in={num}".format(term="201420", dept=dept, num=num)
    result = urlfetch.fetch(host+query)
    
    if result.status_code == 200:
        tree = html.fromstring(result.content)
        text = tree[1][4][2].text_content()   # get just the relevant text of the webpage 

        # remove unicode non-breaking spaces to allow regexing
        text = text.replace(u'\xa0',u' ')
        return text
    
def insert_course(dept, num, text):
    # Regexes for extracting class properties
    # results go into capture group 1
    
    # TODO: regex to capture course title
    
    m = re.search("[\d\w]{5} - ([\w ]*)", text)
    title = m.group(1) if m else "nomatch"

    m = re.search("\.\s(.*)\sTypically",text)
    des = m.group(1) if m else "nomatch"

    # TODO: Credit hours aren't fixed for every course
    # Credit Hours: 2.00 or 3.00. 
    # Credit Hours: 1.00 to 18.00. 

    m = re.search("Credit Hours: (\d\.\d\d)",text)
    cr = m.group(1) if m else "-1"

    m = re.search("Typically offered (.*?)\.", text)
    sem = m.group(1).split() if m else ["nomatch"]

    m = re.search("Schedule Types:\s((?:[\w ]+)(?:,[\w ]+)*) \s+", text)
    form = m.group(1).split(", ") if m else ["nomatch"]

    # TODO: campus parsing fails on ECE 302

    m = re.search("campuses:\s*(.*)Learn", text,flags=re.DOTALL)
    campus = m.group(1).strip().split("\n\n") if m else ["nomatch"]

    # prereq regex and decomosition of prereqs into lists of AND conditions (works for most classes, not 477 and similar)
    # How do we handle co-requisite courses?
    m = re.search("Prerequisites:(.*)",text,flags=re.DOTALL)
    if m:
        allReqs = []
        prereqText = m.group(1).strip()
        prereqText =  prereqText.encode('ascii', 'ignore') 
        for i in PrereqParser.parseprereq(prereqText):
            reqArr = []
            for j in i:
                if j.find(" ") != -1:
                    i.remove(j)
                    for k in j.strip().split():
                        i.append(k)
            for j in i:
                if j.find("-C") != -1:
                    j = j.replace("-C","")
                    reqArr.append(Requisite(course=j,reqType=False))
                else:
                    reqArr.append(Requisite(course=j,reqType=True))
            allReqs.append(RequisiteList(courses=reqArr))
    else:
        allReqs = []
    # course numbers are a total of 5 characters: [(optional starting letter) (4 digits)] or [(5 digits)]
    # See Zool Z1030

    # create course entity
    course = Course(number=int(num), title=title, department=dept, form=form,
                     description=des, credits=float(cr), semesters=sem,
                     campuses=campus,requisites=allReqs, id=dept + num)
    # store course 
    course.put()
    # unnecessary with ndb
            
app = webapp2.WSGIApplication([
    ('/admin/?', AdminHandler),
    ('/api/?', APIHandler),
    ('/raw/?', RawHandler)
], debug=True)
