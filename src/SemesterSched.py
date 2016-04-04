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