import webapp2
import os
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

#################
## Course Model
#################

class Course(ndb.Model):
	description = db.TextProperty()    # unicode string of unlimited length
	fomat = db.StringProperty()        # unicode string up to 1500 bytes
	number = db.IntegerProperty()      # 64-bit signed integer      
	credits = db.IntegerProperty()
	department = db.StringProperty()
	semesters = db.StringProperty(repeated=True)
    campuses = db.StringProperty(repeated=True)
    prerequisites = db.LocalStructuredProperty(Prerequisite, repeated=True) # lists of complete OR conditions

########################
## Prerequisite Model
########################
    
class Prerequisite(ndb.Model):
    courses = db.StringProperty(repeated=True)   # list of AND conditions

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
        html.parse("catalog.html")

def get_course(dept, num):
    url = "https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_course_detail?cat_term_in=201420&subj_code_in={dept}&crse_numb_in={num}".format(dept=dept, num=num)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        tree = html.fromstring(result.content)
        return tree.text_content()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/', APIHandler)
], debug=True)
