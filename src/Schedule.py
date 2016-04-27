import DankSetsAndLists

class Schedule:
	def __init__(self, semList, attribute):
		self.semesters = []
		for item in semList:
			self.semesters.append(item)
		self.attribute = attribute #EE or CompE
		self.coreCreds = 0
		self.seminarCreds = 0
		self.ECEAdvECECreds = 0
		
		
	def generateSched(self):
		pushL = []#carry-over list of courses
		accCourses = []#continues generating the updated courses taken
		for sem in self.semesters:
			sem.addCoursesTaken(accCourses)
			pushL = sem.generateSem(pushL)#generates sem and updates the pushList.
			accCourses += sem.getCoursesTaking()
			
	
	def isValid(self):
		"""checks AND (apparently) corrects schedule"""
		crsesLacking = []
		allCrsTaking = []
		for sem in self.semesters:
			temp = sem.getCoursesTaking()#prevent excess calling of getCoursesTaking in for loop
			for crs in temp:
				allCrsTaking.append(crs)
		#check credits
		#check prereqs all prereqs are met
		if(self.attribute == "EE"):
			#core
			"""need to get EECORE and other string lists converted to object lists for subtraction"""
			recObjList = []
			recObjLL = []
			req = EECore+ECESeminars+ECESenDes#combine for efficiency and readibility
			for str in req:
				for C in allCourses:
					if(str == C.getTitle()):
						recObjList.append(C)
			
			cnt = 0
			for L in ECEAdvEESel:
				recObjLL.append([])
				for strng in L:
					for cs in allCourses:
						if(strng == cs.getTitle()):
							recObjLL[cnt].append(cs)#finish later
				cnt+=1
				
			crsesLacking += listDiff(recObjList, allCrsTaking)#sets only have titles of courses, need to translate
			#seminars(200 and 400)
			crsesLacking += minDiff(allCrsTaking, recObjLL)
			
			#then check if each semesterSched was valid
			for lack in crsesLacking:
				replace(lack)#replaces last needed courses
			
			
		elif(self.attribute == "CompE"):
			#Core
			recObjList = []
			recObjLL = []
			req = CompECore+ECESeminars+ECESenDes#combine for efficiency and readibility
			for str in req:
				for C in allCourses:
					if(str == C.getTitle()):
						recObjList.append(C)
			
			cnt = 0
			for L in ECEAdvCompE:
				recObjLL.append([])
				for strng in L:
					for cs in allCourses:
						if(strng == cs.getTitle()):
							recObjLL[cnt].append(cs)#finish later
				cnt+=1
				
			crsesLacking += listDiff(recObjList, allCrsTaking)#sets only have titles of courses, need to translate
			#seminars(200 and 400)
			crsesLacking += minDiff(allCrsTaking, recObjLL)
			
			#then check if each semesterSched was valid
			for lack in crsesLacking:
				replace(lack)#replaces last needed courses
		else:
			print("Invalid degree type attribute\n")
	
	def replace(self, crsToAdd, allCoursesTaking):
		allPrereqs = []
		for sem in self.semesters:
			for crs in sem:
				for prereqL in crs.getPrereqListList():
					for prereq in prereqL:
						allPrereqs.append(prereq)#progressively accumulates the prereqs that were needed as the schedule was built
				if(not(((self.attribute == "EE" and (crs.getTitle() in EECore or crs.getTitle() in simpleEEAdvSel)) or (self.attribute == "CompE" and(crs.getTitle() in CompECore or crs.getTitle in simpleCompESel))) or crs.getTitle() in ECESeminars or crs.getTitle() in ECESenDes)):
					#if not in the required categories of courses
					if(crs not in allPrereqs):
						#course is not necessary, can replace
						sem[sem.index(crs)] = crsToAdd#new course
	