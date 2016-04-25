import re

# not gonna lie, this is pretty much magic (recursion)
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


def applyAnd(opr1,opr2):
	pass

def applyOr(opr1,opr2):
	return opr1 + opr2


def pullParen(stack):
	resL = []
	resS = ""
	first = stack.pop()
	if isinstance(first,list):
		first = first[0]
	resS+=(first + " ")
	resL.append(first)
	assert(first != "&" and first != "|")
	group = stack.pop()
	# so this assert fails, i guess we do have to deal with it
	# assert(group == "&" or group == "|")
	if group == "&" or group == "|":	
		while stack[len(stack) - 1] != "(":
			i = stack.pop()
			if i != group:
				if group == "&":
					assert(i != "|")
					resS+=(i+" ")
				elif group == "|":
					assert(i != "&")
					resL.append(i)
				elif group == "(":
					resS+=(i+" ")
	else:
		stack.append(first)
		return(stack)

	stack.pop()
	result = resS if group == "&" else resL
	stack.append(result)
	return(stack)

				
def parse2(text):
	text = text.replace("\n", " ").strip()
	m = re.search("General Requirements:(.*)",text,flags=re.DOTALL)
	text = m.group(1) if m else ""
	text = text.replace("Course or Test:","")
	text = text.replace("Minimum Grade of  D-","")
	text = text.replace("May not be taken concurrently.","")
	text = text.replace("(","")
	text = text.replace(")","")
	text = text.replace(" ", "")
	print text
	Ors = text.split("or")
	return [i.split("and") for i in Ors]


def parseprereq(text):
	if text.find("General Requirements") != -1:	
		return parse2(text)
	# remove unneeded text, make parsing easier
	text = text.replace("Undergraduate level", "")
 

	text = text.replace("Minimum Grade of C-", "")
	text = text.replace("Minimum Grade of C", "")
	text = text.replace("Minimum Grade of D-", "")
	text = text.replace("Minimum Grade of D", "")
	text = text.replace("  [may be taken concurrently]", "-C ")
	text = text.replace("and", "&")
	text = text.replace("or", "|")
	if text.find("ALEKS") != -1:
		text = text.replace(" |  ALEKS Math Assessment 085","")
		text = text.replace(" |  ALEKS Math Assessment 075","")
		text = text.replace("ALEKS Math Assessment 085","")
		#text = text.strip("(")
		#text = text.strip(")")
	list1 = text.strip().split()

	# fun with stacks
	stack = []
	while list1 != []:
		i = list1.pop(0)
		if i == "(":
			stack.append(i)
		elif i == ")":
			stack = pullParen(stack)
		elif i == "|":
			while len(stack) > 3 and stack[len(stack) -2] == "&":
				a = stack.pop()
				stack.pop()
				b = stack.pop()
				stack.append(applyAnd(a,b))
			stack.append(i)
		elif i == "&":
			while len(stack) > 3 and stack[len(stack) -2] == "&":
				a = stack.pop()
				stack.pop()
				b = stack.pop()
				stack.append(applyAnd(a,b))
			stack.append(i)
		else:
			stack.append(i + list1.pop(0))
	# Check for ambigious prereq (and and ors togther) this is a problem, ECE321 is an example
	# not much we can do about that, but we have to do something, so just split on the or, only take half
	# also, some courses reference non-existant or outdated information. (EE255, ECE 46200)...
	OrList= []
	print stack
	if "|" in stack and "&" in stack:
		print "Sigh..."
		stack = stack[:stack.index("|")]

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
					if not isinstance(j,basestring):
						for k in j:
							OrList.append([k])
					else:
						OrList.append([j])
			elif i != "|":
				OrList.append([i])
		print OrList 
		return OrList
