import webapp2
import os
import jinja2
import json
from DankMath import *
from Course2 import Course2
import DankMath
from SemesterSched import SemesterSched
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
    """

    def post(self):
        self.fun()
    def get(self):
        self.fun()
    def fun(self):
        self.response.headers['Content-Type'] = 'text/plain'

        courses = {}
        
        with open("course_data.json") as data:
            data = json.loads(data.read())

            for k,v in data.iteritems():
                courses[v['department'] + v['number']] = Course2(v)

        applyAllWeights(courses, ["circuit", "Microprocessor", "signal", "system","ece","com"])

        maxCourse = maxValuedCourse(courses)

        self.response.write(maxCourse.getTitle() + "\n\n\n")

        self.response.write(str(maxCourse.getWeight()) + "\n\n\n")    
        self.response.write(str(maxCourse.getDescription()) + "\n\n\n")

        SemsOnCampus = self.request.get("semesters")

        #Sched = Schedule(SemsOnCampus,DegreeType)
        #Sched.generateSched()
        Sems= []
        for sem in SemsOnCampus:
            Sems.append(sem.season,sem.year,[],[],allCourses)
        #Sched = Schedule(Sems, DegreeType)

        params = self.request.params.mixed()

        DankMath.applyAllWeights(courses, ["programming", "optimization", "ECE", "electricity", "circuit", "C++", "Microprocessor","signal", "system"])
        sem = SemesterSched("Fall",2016,[],[])
        sem.generateSem([],courses)
        for crs in sem.coursesTaking:
            self.response.write(crs.getID() + crs.getTitle() + crs.getDescription() + "\n")
        #params["courses_taken"] = params["courses_taken"].strip().split("\n")

        if "courses_taken" in params:
            params["courses_taken"] = params["courses_taken"].strip().replace(" ", "").split("\n")
        else:
            params["courses_taken"] = ["ECE20100", "ECE20000"]


        
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