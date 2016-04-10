import dankMath.py

class SemesterSched:
	def __init__(self, season, year, completedCoursesList, crsesTaking):
		self.season = season
		self.year = year
		self.coursesTaken = []
		for crse in completedCoursesList
			self.coursesTaken.append(crse)
		self.coursesTaking = []
		self.semCreditTotal = 0
		for item in crsesTaking:
			self.addCourseTaking(item)
		self.concurrentList = []
		
	#determines if a course is valid based on semester offered and prereqs and then adds it
	def addCourseTaking(self, crse):
		if(crse.isValid(self.season, self.coursesTaken)):
			self.coursesTaking.append(crse)
			self.semCreditTotal += crse.getCredits()
			return True
		else:
			print('could not add course: {0} to semester: {1} {2}'.format(crse.getTitle(),self.season, self.year))
			return False
	
	def unconditionalAddCourse(self, crse):
		self.coursesTaking.append(crse)
		self.semCreditTotal += crse.getCredits()
	
	#do I need to return a copy? (because wouldn't a shallow copy be deallocated after leaving function?
	def getCourses(self):
		return self.courses
	
	def isValid(self):
		#check all courses valid
		for crs in courses:
			if(!crs.isValid(self.season, self.coursesTaken)):
				return False
		if(self.semCreditTotal < 12):
			return False
		return True #returns true if no courses were invalid

		
	def concurrencyMet(self):
		for thing in concurrentList[schedIndex][:][:]:
			if((thing.intersection(set()) != set()) && set(self.coursesTaking).issuperset(set(thing))):
				return True
		return False #default if none of concurrencies met.
	
	#determines next course to take
	def nextCourse(self,allCourses):
		#to be implemented. see word doc
		#steps:
		#find largest fraction weighted course remaining
		#this assumes weights have been applied at the beginning of the program.
		validSubset = listDiff(allCourses, self.coursesTaken)
		crse = maxValuedCourse(validSubset)#this should copy an object... do I need to worry about this?
		crse.getDeepestPre(coursesTaken)#hmm, think about this; the prereqsSatisfied function should be needed somewhere...
		
	
	def fixAndReplace(self):#to be implemented
	
		
		