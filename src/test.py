from SemesterSched import SemesterSched
from Schedule import Schedule
from Course2 import Course2


c = Course2("ECE200",[],"Some lame Course",0,1.0,["Fall","Spring"])
a = SemesterSched("Fall",2016,[],[],[c])
a.generateSem([])



class SubmitHandler(webapp2.RequestHandler):
    """
    Submit Handler
    """
    def get(self):
        allCourses =[]
        for c in Course:    
            allCourses.append(Course2(c.title,c.requisites,c.description,0,c.credits,c.semesters))
        #Sched = Schedule(SemsOnCampus,DegreeType)
        #Sched.generateSched()
        Sems= []
        for sem in SemsOnCampus:
            Sems.append(sem.season,sem.year,[],[],allCourses)
        Sched = Schedule(Sems,"EE")
