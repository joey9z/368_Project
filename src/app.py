import webapp2
import os
import jinja2
import json
from models import Course

jinja = jinja2.Environment( loader=jinja2.FileSystemLoader( os.path.join( os.path.dirname(__file__), '') ) )

###############################
## Setup Web Request Handlers
##
## Reference: https://cloud.google.com/appengine/docs/python/tools/webapp2
###############################
    
class MainHandler(webapp2.RequestHandler):
    """ serves the main application page """
    def get(self):
        template = jinja.get_template('index.html')
        html = template.render()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)
        
class SubmitHandler(webapp2.RequestHandler):
    """ 
    Submit Handler
    
    serves the /submit page
    will initiate schedule generation
    """

    def post(self):
        self.fun()
    def get(self):
        self.fun()
    def fun(self):
        self.response.headers['Content-Type'] = 'application/json'
        
        c = Course.get_by_id("ECE20100")
        
        params = self.request.params.mixed()
        params["courses_taken"] = params["courses_taken"].strip().split("\n")
        
        schedule = {
            "semesters": [
                { 
                  "semester": "Fall",
                  "year": 2016,
                  "courses": ["ECE 202", "ECE 208", "SPAN 201", "ME 270"]
                },
                { 
                  "semester": "Spring",
                  "year": 2017,
                  "courses": ["ECE 301", "ECE 302", "ECE 270", "ECE 264"]
                }
            ],
            "received": params
        }
        
        self.response.write(json.dumps(schedule))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler)
], debug=True)