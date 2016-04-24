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
		for sem in self.semesters:
			pushL = sem.generateSem(pushL)#generates sem and updates the pushList.
			
	def patchNotMetReqs(self, crsesLacking):
		
		
	
	def isValid(self):
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
			crsesLacking += listDiff(EECore, allCrsTaking)#sets only have titles of courses, need to translate
			#seminars(200 and 400)
			crsesLacking += listDiff(ECESeminars, allCrsTaking)
			#advanced selectives(>9 hours)
			crsesLacking += minDiff(allCrsTaking, ECEAdvEESel)
			#Senior design(49595 or 477 or both EPCS411 and 412 over consec sems
			crsesLacking += listDiff(ECESenDes, allCrsTaking)
			#ECE Electives(3 300 level or above labs, and other courses)(>7 hrs at least)
			#No.
			#total ECE creds >= 47, note, only 6 credits allowed of "special content courses"
			#Forget it... only reasonable thing to add is research at this point. Too much...thinking...
			#general engineering
			#-7 first yr, -3 breadth req
			#math
			#science
			#ugh, gen eds-dont forget foundational outcome
			#complementary electives
			
			#then check if each semesterSched was valid
			for lack in crsesLacking:
				replace(lack)#replaces last needed courses
			
			
		elif(self.attribute == "CompE"):
			#Core
			#seminars(200 and 400)
			#Advanced cmpE requirement(437 + 468 or 469)
			#Senior Design 49595 or 477 or both EPCS411 and EPCS412 over consec sems
			#CmpE electives >2 credits used to bring total to 49
			#general engineering
			#-7 first year, -3 breadth req
			#math, calc1 calc2 calc3,linear,diffEq, AND ECE369
			#or calc1 calc2 calc3 MA262 ECE369, and one advanced math selective
			#science
			#Gen eds
			#Complementary electives
		else
			print("Invalid degree type attribute\n")
	
	def replace(self, crsToAdd, allCoursesTaking):
		allPrereqs = []
		for sem in self.semesters:
			for crs in sem:
				for prereqL in crs.getPrereqListList():
					for prereq in prereqL:
						allPrereqs.append(prereq)#progressively accumulates the prereqs that were needed as the schedule was built
				if(!(((self.attribute == "EE" and (crs.getTitle() in EECore or crs.getTitle() in simpleEEAdvSel)) or (self.attribute == "CompE" and(crs.getTitle() in CompECore or crs.getTitle in simpleCompESel))) or crs.getTitle() in ECESeminars or crs.getTitle() in ECESenDes)):
					#if not in the required categories of courses
					if(crs not in allPrereqs):
						#course is not necessary, can replace
						sem[sem.index(crs)] = crsToAdd#new course
	