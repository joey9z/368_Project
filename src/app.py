import webapp2
import os
import jinja2
import json
from DankMath import *
from Course2 import Course2
from Schedule import Schedule

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

    Spring = 10, Summer = 20, Fall = 30
    """

    def post(self):
        self.fun()
    def get(self):
        self.fun()
    def fun(self):
        self.response.headers['Content-Type'] = 'application/json'

        courses = {}
        semesters = []
        
        with open("course_data.json") as data:
            data = json.loads(data.read())

            for k,v in data.iteritems():
                courses[v['department'] + v['number']] = Course2(v)

        applyAllWeights(courses, ["circuit", "Microprocessor", "signal", "system","ece","com"])

        maxCourse = maxValuedCourse(courses)

        # self.response.write(maxCourse.getTitle() + "\n\n\n")

        # self.response.write(str(maxCourse.getWeight()) + "\n\n\n")    
        # self.response.write(str(maxCourse.getDescription()) + "\n\n\n")

        #Sched = Schedule(SemsOnCampus,DegreeType)
        #Sched.generateSched()
        #Sched = Schedule(Sems, DegreeType)

        params = self.request.params.mixed()

        if "courses_taken" in params:
            params["courses_taken"] = params["courses_taken"].strip().replace(" ", "").split("\n")
        else:
            params["courses_taken"] = ["ECE20100", "ECE20000"]

        for sem in params["semesters"]:
            semesters.append(Semester(sem))
        
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