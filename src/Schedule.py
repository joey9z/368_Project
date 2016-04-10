class Schedule:
	def __init__(self, semList, attribute):
		self.semesters = []
		for item in semList:
			self.semesters.append(item)
		self.attribute = attribute #EE or CompE
		self.coreCreds = 0
		self.seminarCreds = 0
		self.ECEAdvECECreds = 0
		
		self.ECEElCreds = 0
		self.senDesCreds = 0
		self.firstYrEngCreds = 0
		self.mathCreds = 0
		self.scienceCreds = 0
		self.genEdTotCreds = 0
		self.totECECreds = 0
		self.engBreadthCreds = 0
		#okay, so it is nearly impossible to determine which gen eds, as well as apply attributes to all courses...
		
		
		
		
	
	def isValid(self):
		#check credits
		#check prereqs all prereqs are met
		if(self.attribute == "EE"):
			#core
			#seminars(200 and 400)
			#advanced selectives(>9 hours)
			#Senior design(49595 or 477 or both EPCS411 and 412 over consec sems
			#ECE Electives(3 300 level or above labs, and other courses)(>7 hrs at least)
			#total ECE creds >= 47, note, only 6 credits allowed of "special content courses"
			#general engineering
			#-7 first yr, -3 breadth req
			#math
			#science
			#ugh, gen eds-dont forget foundational outcome
			#complementary electives
			
			#then check if each semesterSched was valid
			
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
		
		