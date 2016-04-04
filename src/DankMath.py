# The Dank Math Module

#determines the fraction of course description words that were in the keyword list
def fractWeight(course, keywords):
	for word in keywords:
		count += course.getDescription().count(word)
	return count / len(course.getDescription())
	
	
def

#remaining things: picking next course, and the over schedule is valid method
