# The Dank Math Module
from operator import attrgetter#for finding object with maximum weight in a list of objects

#determines the fraction of course description words that were in the keyword list
def fractWeight(course, keywords):
	""" determines the fraction of course description words that were in the keyword list """
	count = 0.0
	for word in keywords:
		#print course.getDescription().encode('ascii','ignore')
		count += course.getDescription().count(word)
	if len(course.getDescription()) > 0:
		return count #/ len(course.getDescription())
	else:
		return 0 

def applyAllWeights(allCourses, keywords):
	for k,crse in allCourses.iteritems():
		crse.setWeight(fractWeight(crse, keywords))

def maxValuedCourse(allCourses):
	""" returns course object with maximum weight parameter """
	maxWeight = -1
	maxCourse = None

	for k,course in allCourses.iteritems():
		if course.getWeight() > maxWeight:
			maxWeight = course.getWeight()
			maxCourse = course

	return maxCourse

	
def listDiff(listA, listB):
	"""listA - listB, return result is a list note that this is not the same as listB - listA"""
	SB = set([i.getTitle() for i in listB])
	res = []
	if(len(listA) > 0):
		if isinstance(listA[0],basestring):
			res = [starfish for starfish in listA if starfish not in SB]
		else:
			res = [starfish for starfish in listA if starfish.getID() not in SB]
	return res 

def setDiffOfLists(listA, listB):
	"""listA - listB, return result is a set note that this is not the same as listB - listA"""
	return set(listA) - set(listB)

#remaining things: picking next course, and the over schedule is valid method
