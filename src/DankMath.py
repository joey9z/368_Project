# The Dank Math Module
from operator import attrgetter#for finding object with maximum weight in a list of objects

#determines the fraction of course description words that were in the keyword list
def fractWeight(course, keywords):
	""" determines the fraction of course description words that were in the keyword list """
	for word in keywords:
		count += course.getDescription().count(word)
	return count / len(course.getDescription())		

def applyAllWeights(allCourses, keywords):
	for crse in allCourses:
		crse.setWeight(fractWeight(crse, keywords))

def maxValuedCourse(allCourses):
	""" returns course object with maximum weight parameter """
	return max(allCourses, key=attrgetter('weight'))
	
def listDiff(listA, listB):
	"""listA - listB, return result is a list note that this is not the same as listB - listA"""
	SB = set([i.getTitle() for i in listB])
	return [starfish for starfish in listA if starfish.getTitle() not in SB]
	
def setDiffOfLists(listA, listB):
	"""listA - listB, return result is a set note that this is not the same as listB - listA"""
	return set(listA) - set(listB)

#remaining things: picking next course, and the over schedule is valid method
