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
	fomat = ndb.StringProperty()        # unicode string up to 1500 bytes
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
        
class APIHandler(webapp2.RequestHandler):
    def get(self):
        #html.parse("catalog.html")
        # test course add function, and retrieve the course
        get_course("ECE","20100")
        c = Course.get_by_id("ECE20100")
        # output the description as a test
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(c.description)



def get_course(dept, num):
    url = "https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_course_detail?cat_term_in=201420&subj_code_in={dept}&crse_numb_in={num}".format(dept=dept, num=num)
    result = urlfetch.fetch(url)
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

        m = re.search("campuses:\s*(.*)Learn", text,flags=re.DOTALL)
        campus = m.group(1).strip().split("\n\n") if m else ["nomatch"]

        # TODO prereq regex and decomosition of prereqs into lists of AND conditions
        #  prereqList = parsePrereqs(text);
        # prereq = Prerequisite(parent=ndb.Key('Course'), courses=prereqList)
        # create course entity
        course = Course(number=int(num), department=dept, description=des, credits=float(cr), semesters=sem, campuses=campus, id=dept + num)
        # store course 
        course.put()
        # unnecessary with ndb 
        # return tree.text_content()
        return campus
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/', APIHandler)
], debug=True)
