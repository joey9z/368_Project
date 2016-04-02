import re
# not gonna lie, this is pretty much magic
# returns a list (ish-its a generator) that contains all the different combinations of classes that are valid pre-reqs for the class
def makeAndLists(prereqs, depth, current):
	if(depth == len(prereqs)):
		x = []
		for j in current:
			temp = j.split("&")
			for k in temp:
				x.append(k)
		yield x
	else:
		for j in prereqs[depth]:
			for val in makeAndLists(prereqs, depth + 1, current + [j]):
				yield val


def pullParen(stack):
	resL = []
	resS = ""
	first = stack.pop()
	resS+=(first + " ")
	resL.append(first)
	assert(first != "&" and first != "|")
	group = stack.pop()
	assert(group == "&" or group == "|")

	while stack[len(stack) - 1] != "(":
		i = stack.pop()
		if i != group:
			if group == "&":
				assert(i != "|")
				resS+=(i+" ")
			else:
				assert(i != "&")
				resL.append(i)

	stack.pop()
	result = resS if group == "&" else resL
	stack.append(result)
	return(stack)
				


def parseprereq(text):
	# remove unneeded text, make parsing easier
	text = text.replace("Undergraduate level", "")
	text = text.replace("Minimum Grade of C-", "")
	text = text.replace("Minimum Grade of C", "")
	text = text.replace("Minimum Grade of D-", "")
	text = text.replace("  [may be taken concurrently]", "-C ")
	text = text.replace("and", "&")
	text = text.replace("or", "|")
	list1 = text.strip().split()
	#list1 = re.split("\(|\)|\||&",text.strip())
	#print list1
	#print "\n\n"

	# fun with stacks
	stack = []
	while list1 != []:

		i = list1.pop(0)
		#print i
		# print "\n\n"
		if i == "(":
			stack.append(i)
		elif i == ")":
			stack = pullParen(stack)
		elif i == "|":
			stack.append(i)
		elif i == "&":
			stack.append(i)
		else:
			stack.append(i + list1.pop(0))
	#print stack
	#print "\n\n"
	# Check for ambigious prereq (and and ors togther) this is a problem, ECE321 is an example
	# not much we can do about that.
	# also, some courses reference non-existant or outdated information. (EE255, ECE 46200)
	OrList= []
	if "|" in stack and "&" in stack:
		print "Sigh..."
		return []

	
	if "&" in stack:
		for i in stack:
			if not isinstance(i,basestring):
					OrList.append(i)
			elif i != "&":
				OrList.append([i])
		return makeAndLists(OrList, 0, [])
	else:
		for i in stack:
			if not isinstance(i,basestring):
				for j in i:
					OrList.append([j])
			elif i != "|":
				OrList.append([i]) 
		return OrList																																																																																																																											
#test = "(Undergraduate level MA 16600 Minimum Grade of C- or Undergraduate level MA 16200 Minimum Grade of C-) and (Undergraduate level ENGR 13100 Minimum Grade of D- or Undergraduate level ENGR 14100 Minimum Grade of D- or Undergraduate level ENGR 13300 Minimum Grade of D-) and (Undergraduate level PHYS 17200 Minimum Grade of D- or Undergraduate level PHYS 15200 Minimum Grade of D-) and (Undergraduate level MA 26100 Minimum Grade of D- [may be taken concurrently] or Undergraduate level MA 17400 Minimum Grade of D- [may be taken concurrently] or Undergraduate level MA 18200 Minimum Grade of D- [may be taken concurrently] or Undergraduate level MA 27100 Minimum Grade of D- [may be taken concurrently])"
#test2 = "(Undergraduate level  PHYS 17200 Minimum Grade of D- or Undergraduate level  PHYS 15200 Minimum Grade of D- or (Undergraduate level  PHYS 16200 Minimum Grade of D- and Undergraduate level  PHYS 16300 Minimum Grade of D-)   ) and (Undergraduate level  MA 16200 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MA 17100 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MA 17300 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MA 16900 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MA 16600 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MATH 16400 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MATH M2160 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MA 18100 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MA 16400 Minimum Grade of D- [may be taken concurrently] or Undergraduate level  MATH 16600 Minimum Grade of D- [may be taken concurrently])"
#lists = parseprereq(test)
#lists = []
#for i in lists:
#	print i
#	print "\n"