# The Dank Math Module
from operator import attrgetter#for finding object with maximum weight in a list of objects

#determines the fraction of course description words that were in the keyword list
def fractWeight(course, keywords):
	for word in keywords:
		count += course.getDescription().count(word)
	return count / len(course.getDescription())		

def applyAllWeights(allCourses, keywords):
	for crse in allCourses:
		crse.setWeight(fractWeight(crse, keywords))

def maxValuedCourse(allCourses):
	return max(allCourses, key=attrgetter('weight'))#returns course object with maximum weight parameter
	
def listDiff(listA, listB):
	SB = set(listB)
	return [starfish for starfish in listA if starfish not in SB]
	
def setDiffOfLists(listA, listB):
	return set(listA) - set(listB)

#remaining things: picking next course, and the over schedule is valid method
