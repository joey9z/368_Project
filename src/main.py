import webapp2
import os
import re
import jinja2
from lxml import html
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

jinja = jinja2.Environment( loader=jinja2.FileSystemLoader( os.path.join( os.path.dirname(__file__), '') ) )

###############################
## Database Models
##
## Reference: https://cloud.google.com/appengine/docs/python/ndb/properties
###############################

########################
## Prerequisite Model
########################
    
class Prerequisite(ndb.Model):
    courses = ndb.StringProperty(repeated=True)   # list of AND conditions


#################
## Course Model
#################

class Course(ndb.Model):
	description = ndb.TextProperty()    # unicode string of unlimited length
	form = ndb.StringProperty(repeated=True)        # unicode string up to 1500 bytes
	number = ndb.IntegerProperty()      # 64-bit signed integer      
	credits = ndb.FloatProperty()		# float because some classes have half credits (source: I got 3.5 credits for ENGR 141/2)
	department = ndb.StringProperty()
	semesters = ndb.StringProperty(repeated=True)
	campuses = ndb.StringProperty(repeated=True)
	prerequisites = ndb.LocalStructuredProperty(Prerequisite, repeated=True) # lists of complete OR conditions


###############################
## Setup Web Request Handlers
##
## Reference: https://cloud.google.com/appengine/docs/python/tools/webapp2
###############################
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('index.html')
        html = template.render()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)
        
#######################
## API Request Handler
##
## Example query: http://localhost:{port}/api?dept=ECE&course=30200
## If no department or course is specified, it defaults to ECE 20100
######################   
        
class APIHandler(webapp2.RequestHandler):
    def get(self):
        dept = self.request.get("dept") or "ECE"
        course = self.request.get("course") or "20100"
        #html.parse("catalog.html")
        
        # test course add function, and retrieve the course
        text = get_course(dept, course)
        c = Course.get_by_id("{d}{c}".format(d=dept, c=course))
        
        # output the description as a test
        self.response.headers['Content-Type'] = 'text/html'
        
        # output collected parameters to verify accuracy
        
        self.response.write("<h1>{dept} {num} ({cr} Credits)</h1>".format(dept = c.department, num = c.number, cr=c.credits))
        self.response.write("<h2>Raw Text</h2>");
        self.response.write(text)
        self.response.write("<h2>Description</h2>")
        self.response.write(c.description)
        self.response.write("<h2>Semesters Offered</h2>")
        self.response.write(c.semesters)
        self.response.write("<h2>Campuses</h2>")
        self.response.write(c.campuses)
        self.response.write("<h2>Course Format</h2>")
        self.response.write(c.form)
        

def get_course(dept, num):
    host = "https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_course_detail"
    query = "?cat_term_in={term}&subj_code_in={dept}&crse_numb_in={num}".format(term="201420", dept=dept, num=num)
    result = urlfetch.fetch(host+query)
    
    if result.status_code == 200:
        tree = html.fromstring(result.content)
        
        # get just the relevant text of the webpage 
        text = tree[1][4][2][1][0].text_content()

        # remove unicode non-breaking spaces to allow regexing
        text = text.replace(u'\xa0',u' ')

        # Regexes for extracting class properties
        # results go into capture group 1
        
        m = re.search("\.\s(.*)\sTypically",text)
        des = m.group(1) if m else "nomatch"

        m = re.search("Credit Hours: (\d\.\d\d)",text)
        cr = m.group(1) if m else "-1"

        m = re.search("Typically offered (.*?)\.", text)
        sem = m.group(1).split() if m else ["nomatch"]
        
        m = re.search("Schedule Types:\s((?:[\w ]+)(?:,[\w ]+)*) \s+", text)
        form = m.group(1).split(", ") if m else ["nomatch"]
        
        # TODO: campus parsing fails on ECE 302
        
        m = re.search("campuses:\s*(.*)Learn", text,flags=re.DOTALL)
        campus = m.group(1).strip().split("\n\n") if m else ["nomatch"]

        # TODO prereq regex and decomosition of prereqs into lists of AND conditions
        
        # prereqList = parsePrereqs(text);
        # prereq = Prerequisite(parent=ndb.Key('Course'), courses=prereqList)
        
        # create course entity
        course = Course(number=int(num), department=dept, form=form, description=des, credits=float(cr), semesters=sem, campuses=campus, id=dept + num)
        # store course 
        course.put()
        # unnecessary with ndb 
        # return tree.text_content()
        return text

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/?', APIHandler)
], debug=True)
