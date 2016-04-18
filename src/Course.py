import DankMath.py
import operator.py  #used for finding key corresponding to max value in a dictionary in tunnelling methods around line 120

class Course:
	def __init__(self, title, prereqs, description, priority, credits, validSems):
		self.title = title
		self.prereqListList = []
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
		self.weight = 0
		
	def addPrereqSet(self, prereqs):
		for item in prereqs:
			self.prereqListList.append(item)
	
	def setWeight(self, wght):
		self.weight = wght
	
	def getWeight(self):
		return self.weight
	
	def addDescription(self, stringsList):
		for word in stringsList:
			self.description.append(word)
	
	def addValidSem(self, sem):
		self.validSems.append(sem)
	
	def addValidSems(self, semList):
		for sem in semList:
			self.validSems.append(sem)
		
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
    
    def fromDict(self, obj):
        """ copies the attributes of a dict into the class instance"""
        for key, val in obj.iteritems()
            setattr(self, key, val)

    def isOfferedSem(self, semester):
        """ determine if a course is offered in a given semester """
		return (semester in self.validSems)	

	def prereqsSatisfied(self, compCrseList, concurrentList, schedIndex):#concurrent list is likely to be empty in most cases
        """ determines if a prerequisite is satisfied """
		satisfied = 0
		concurrentFlag = 1
		i = 0
		j = 0 
		for prereqL in prereqListList:
			prereqSet = set(prereqL)
			
			concurrencyFlag = 0
			concurrentList[schedIndex].append([])    #for each list of prereqs, initalize a new list
			if (prereqL in compCrseList):
				#satisfied = 1#wait, just return True...
				return 1#only need to satisfy one set, so it is okay to return
			else:    #add to concurrency list for semester
				for (item in listDiff(prereqL, compCrseList)):
					if (item.hasConcurrentFlag):    #if not all items have concurrent flag ASK ABOUT THIS SYNTAX for HASCONCURRENT FLAG
						concurrentList[schedIndex][i].append(item)
						concurrencyFlag = 1
					#add a current semester concurrency list
					#concurrentList is a list of a list of a list... first level tells which course in schedule the sublist levels deal with
					#schedIndex denotes which course (by order added to a semester schedule is being dealt with
			i+=1		
		if (concurrencyFlag):
			return 2
		else:
			return 0
		#note, 0 = prereqs dissatisfied, 1 = prereqs satisfied, 2 = only concurrency needed
		#the use of returning two is so that if only concurrency is an issue, then 
		#courses can be decided to be added regardless, and once adding is finished,
		#a call to concurrencyMet() in the SemesterSched class
		#will determine whether to keep concurrency dependent
		#courses.
	
	def isValid(self, seasonSem, crsList):
        """ determines if the course is valid """
		if(crse.isOfferedSem(seasonSem) && crse.prereqsSatisfied(crsList))
			return True
		else
			return False

	def bestPrereqSetIndex(self, coursesTaken):
        """ finds shortest set of prerequistes given a set of prerequisites """
		crseNumArr = []
		for ls in self.prereqListList:#create array to determine remaining prereqs needed for a course
			crseNumArr.append(len(set(coursesTaken).intersection(set(self.prereqListList))))
		return crseNumArr.index(min(crseNumArray))

	def getDeepestPre(self, coursesTaken):
        """ returns string title of the course that is farthest down the prereq chain """
		endPoints = {self.getTitle():depth}   #initializes with top course and depth 0 
		depth = 0
		for pre in self.prereqListList[self.bestPrereqSetIndex(coursesTaken)]:
			pre.tunnelAndRecord(endPoints,coursesTaken, depth)
		#dict should be formed now, so determine farthest down
		return max(endPoints.iteritems(), key=operator.itemgetter(1))[0]  #this recursion stuff hurt, but should work

	def tunnelAndRecord(self, preDict, coursesTaken, depth):
        """ burrows down the prerequisite chain, recording depths, helper function to getDeepestPre """
		depth += 1#recursive incrementing will occur
		if(self.prereqListList[self.bestPrereqSetIndex(coursesTaken)] == []): #no prereqs, end of a chain
			if(preDict.has_key(self.getTitle()) and preDict[self.getTitle()] > depth):   #entry already in dictionary and at lower depth
				preDict[self.getTitle()] = depth    #change entry depth, basically, doesn't record if key already in at lower depth
			else:
				preDict[self.getTitle()] = depth
		else:
			for item in self.prereqListList[self.bestPrereqSetIndex(coursesTaken)]:
				item.tunnelAndRecord(preDict, coursesTaken, depth)  #REEEECUUURRRRSSIOOOONNNN!!!!!
		