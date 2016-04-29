import DankMath
import operator#used for finding key corresponding to max value in a dictionary in tunnelling methods around line 120

class Course2:
	def __init__(self, obj):
		for key, val in obj.iteritems():
			setattr(self, key, val)
		self.prereqListList = self.requisites
		
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
		
	#determine if a course is offered in a given semester
	def isOfferedSem(self, semester):
		""" determine if a course is offered in a given semester """
		return (semester in self.validSems)	
		
	def getPriority(self):
		return self.priority
		
	def setPriority(self, priority):
		self.priority = priority
	
	def getCredits(self):
		return self.credits
		
	def getTitle(self):
		return self.title

	def getID(self):
		return self.department + self.number
	
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
	
	def prereqsSatisfied(self, compCrseList, concurrentList,schedIndex):#concurrent list is likely to be empty in most cases
		#"""determines if any group of the groups prerequisites is satisfied as well as concurrency"""
		satisfied = 0
		concurrencyFlag = 1
		i = 0
		j = 0

		for prereqL in self.prereqListList:
			prereqSet = set(prereqL)
			
			concurrencyFlag = 0
			concurrentList[schedIndex - 1].append([])#for each list of prereqs, initalize a new list
			TakenCrseNames= [j.getID() for j in compCrseList]
			unFufilledPrereqs = [i for i in prereqL if i.course not in TakenCrseNames] 
			if(unFufilledPrereqs == []): 
				#satisfied = 1#wait, just return True...
				return 1#only need to satisfy one set, so it is okay to return
			else:#add to concurrency list for semester

				for item in unFufilledPrereqs: 
					if(not item.reqType):#if not all items have concurrent flag ASK ABOUT THIS SYNTAX for HASCONCURRENT FLAG
						concurrentList[schedIndex][i].append(item), #possibly useful, not necessary 
						concurrencyFlag = 1
					#add a current semester concurrency list
					#concurrentList is a list of a list of a list... first level tells which course in schedule the sublist levels deal with
					#schedIndex denotes which course (by order added to a semester schedule is being dealt with
					#has concurrent flag corresponds to import end storing of data for whatev way it was stored
			i+=1		
		if(concurrencyFlag):
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
		if(self.isOfferedSem(seasonSem) and self.prereqsSatisfied(crsList,[],0)):
			return True
		else:
			return False
	
	#finds shortest set of prerequistes given a set of prerequisites
	def bestPrereqSetIndex(self, coursesTaken):
		""" finds shortest set of prerequistes given a set of prerequisites """
		crseNumArr = []
		for ls in self.prereqListList:#create array to determine remaining prereqs needed for a course
			pass
			#TODO-> PANIC!!!!
			#crseNumArr.append(len(set(coursesTaken).intersection(set(self.prereqListList))))
			#len(set([i.getID() for i in coursesTaken]).intersection(set([j.getID() for j in self.prereqListList])))
		return crseNumArr.index(min(crseNumArray))
	
	def nextUnsatReq(self, coursesTaken, coursesTaking, allCourses):
		taken = [i.getID() for i in coursesTaken]
		taking = [i.getID() for i in coursesTaking]
		res = []
		lens = []
		for ls in self.prereqListList:
			res[i] = []
			for req in ls:
				if  req.reqType and req.course not in taken:
					res[i].append(req.course)
				elif req.course not in taking + taken:
					res[i].append(req.course)
			lens.append(len(res[i]))
			i += 1
		if min(lens) <= 0:
			return 0
		else:
			choice = res[lens.index(min(lens))][0]
			if allCourses.has_key(choice):
				return allCourses[choice]
			else:
				return None

					

	