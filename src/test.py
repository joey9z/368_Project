from SemesterSched import SemesterSched
from Schedule import Schedule
from Course2 import Course2
import DankMath

c = Course2("ECE20000",[],"Some lame Course",0,1.0,["Fall","Spring"])
e = Course2("ECE20100",[],"Some lame Course",0,1.0,["Fall","Spring"])
print "woo" if c.isValid("Fall",[]) else "Boo"
a = SemesterSched("Fall",2016,[],[],[c,e])
a.generateSem([])

d = Course2("ECE20000",[],"Some lame Course",0,1.0,["Fall","Spring"])

x = DankMath.listDiff([c,e],[d])
print x[0].title


"""class SubmitHandler(webapp2.RequestHandler):
   
    Submit Handler
    
    def get(self):
    	SemsOnCampus = self.request.get("semesters")

        allCourses =[]
        for c in Course:    
            allCourses.append(Course2(c.title,c.requisites,c.description,0,c.credits,c.semesters))
        #Sched = Schedule(SemsOnCampus,DegreeType)
        #Sched.generateSched()
        Sems= []
        for sem in SemsOnCampus:
            Sems.append(sem.season,sem.year,[],[],allCourses)
        Sched = Schedule(Sems, DegreeType)"""
