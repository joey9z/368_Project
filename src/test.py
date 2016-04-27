from SemesterSched import SemesterSched
from Schedule import Schedule
from Course2 import Course2
import DankMath

c = Course2("ECE20000",[],"Some lame Course",0,1.0,["Fall","Spring"])
a = SemesterSched("Fall",2016,[],[],[c])
#a.generateSem([])

d = Course2("ECE20000",[],"Some lame Course",0,1.0,["Fall","Spring"])
e = Course2("ECE20001",[],"Some lame Course",0,1.0,["Fall","Spring"])
y = [i.title for i in [c]]
print y
z = [i.title for i in [d,e]]
print z
x = DankMath.listDiff([c],[d,e])
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
