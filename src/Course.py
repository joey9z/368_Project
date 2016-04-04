class Course:
	def __init__(self, title, prereqs, description, priority, credits, validSems):
		self.title = title
		self.prereqList = []
		for pre in prereqs:
			self.prereqListList.append(pre)
		self.description = []
		for word in description:
			self.description.append(word)
		self.priority = priority
		self.credits = credits
		self.validSems = []
		for sem in validSems:
			self.validSems.append(sem)
		
	def addPrereqSet(self, prereqs):
		for item in prereqs:
			self.prereqListList.append(item)
	
	def addDescription(self, stringsList):
		for word in stringsList:
			self.description.append(word)
	
	def addValidSem(self, sem):
		self.validSems.append(sem)
	
	def addValidSems(self, semList):
		for sem in semList:
			self.validSems.append(sem)
		
	#determine if a course is offered in a given semester
	def isOfferedSem(self, semester):
		return (semester in self.validSems)	
		
	def getPriority(self):
		return self.priority
		
	def setPriority(self, priority):
		self.priority = priority
	
	def getCredits(self):
		return self.credits
		
	def getTitle(self):
		return self.title
	
	def setTitle(self, title):
		self.title = title
			
	def getPrereqListList(self):
		return self.prereqListList
		
	def setPrereqListList(self, preList):
		for item in preList:
			prereqListList.append(item)
			
	def getDescription(self):
		return self.description
	
	def getValidSems(self):
		return validSems
	
	def prereqsSatisfied(self, compCrseList):
		satisfied = 0
		for prereqL in prereqListList:
			if(prereqL in compCrseList):
				satisfied += 1
		if(satisfied):
			return True
		else:
			return False
	
		