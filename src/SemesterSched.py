import DankMath

class SemesterSched:
	def __init__(self, season, year, completedCoursesList, crsesTaking):
		self.season = season
		self.year = year
		self.coursesTaken = []
		for crse in completedCoursesList:
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
	
	def addCoursesTaken(self, crsList):
		self.coursesTaken += crsList
		
	def unconditionalAddCourse(self, crse):
		self.coursesTaking.append(crse)
		self.semCreditTotal += crse.getCredits()
	
	#do I need to return a copy? (because wouldn't a shallow copy be deallocated after leaving function?
	def getCoursesTaking(self):
		return self.coursesTaking
	
	def isValid(self):
		"""only used in case of conditional course add, which wasn't used"""
		#check all courses valid
		for crs in courses:
			if(not crs.isValid(self.season, self.coursesTaken)):
				return False
		if(self.semCreditTotal < 12):
			return False
		return True #returns true if no courses were invalid

		
	def concurrencyMet(self):
		for thing in concurrentList[schedIndex][:][:]:
			if((thing.intersection(set()) != set()) and set(self.coursesTaking).issuperset(set(thing))):
				return True
		return False #default if none of concurrencies met.
	
	#determines next course to take
	def nextCourse(self,allCourses,schedInd):#schedInd is position in schedule. Needed for concurrency issues
		#to be implemented. see word doc
		#steps:
		#find largest fraction weighted course remaining
		#this assumes weights have been applied at the beginning of the program.
		validSubset = listDiff(listDiff(allCourses, self.coursesTaken), coursesTaking)
		crse = maxValuedCourse(validSubset)#this should copy an object... do I need to worry about this?
		if(crse.preReqsSatisfied(coursesTaken,concurrentList,schedInd)):
			return self
		else:
			return crse.getDeepestPre(coursesTaken)#hmm, think about this; the prereqsSatisfied function should be needed somewhere...
		#after the schedule is created, iterate over it again to determine if concurrency met
	
	def generateSem(self,priorPushList):
		conNotMet = []#0's if conc not met
		pushList = []
		schedInd = 0
		
		for prior in priorPushList:#load prior push list
			self.unconditonalAddCourse(nextCourse(allCourses,schedInd))
			schedInd+=1
			
		while(self.semCreditTotal < 14):
			self.unconditonalAddCourse(nextCourse(allCourses,schedInd))
		for crs in self.coursesTaking:
			if(crs.prereqsSatisfied(self.coursesTaken+self.coursesTaking, self.concurrentList,schedIndex) != 1):
				conNotMet.append(1)
			else:
				conMet.append(0)#use pop
				#self.unconditionalAddCourse(nextCourse(allCourses,schedInd))#should cause necessary concurrent to be added
			schedInd+=1
		if(sum(conNotMet) == 1):
			self.unconditionalAddCourse(nextCourse(allCourses,schedInd))#first patch for concurrency
			schedInd+=1
			if(not self.concurrencyMet()):#change the function concMet to rereqs sat somehow
				conNotMet.append(1)
			else:
				conMet.append(0)#use pop
		elif(sum(conNotMet) == 0):
			pass
			#peachy keen!
			#quit now while the going's good!
		else:
			n=0
			conNotMet = []
			removeList
			for ob in self.coursesTaking:
				if(ob.prereqsSatisfied(self.coursesTaken+self.coursesTaking, self.concurrentList,schedIndex) != 1):
					pass
					#conNotMet.append(0)
				else:
					#conNotMet.append(1)
					pushList.append(ob)
					removeList.append(n)
				n+=1#increment to determine which courses are not satisfied still
				#ok, so there is a flaw in the logic here. if I take out a course, it may through
				#off other courses that I satisfy the prerequisites for that depend on it.
				nextSubset = allCourses#the code will separate this from coursesTaking.
			for replacedCrs in pushList:
				#replace each course
				tempCrse = nextCourse(allCourses,schedInd)
				while(tempCrse.prereqsSatisfied(self.coursesTaken+self.coursesTaking, self.concurrentList,schedIndex) != 1):
					nextSubset = listDiff(nextSubset, [tempCrse])
					tempCrse = nextCourse(nextSubset,schedInd)
				self.unconditonalAddCourse(nextCourse(allCourses,schedInd))
				
		for rem in removeList:
			removeList.pop(rem)#clears out the pushed courses from the current semester
		return pushList #will be empty if not needed
			
	
	def fixAndReplace(self):#to be implemented
		pass
		#will need to have the minimum intersections
	
		
		