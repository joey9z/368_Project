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
	res = [x for x in makeAndLists([opr1] + [opr2],0,[])]
	res2 = []
	for x in res:
		a = ""
		for y in x:
			a = a + " " + y
		res2.append(a.strip())
	return res2

def applyOr(opr1,opr2):
	return opr1 + opr2


def pullParen(stack):
	while stack[len(stack) - 2] != "(":
		a = stack.pop()
		op = stack.pop()
		b = stack.pop()
		if op == "|":
			stack.append(applyOr(a,b))
		elif op == "&":
			stack.append(applyAnd(a,b))
		else:
			print "uh-oh\n"
			print(op)	
			print("\n")

	res = stack.pop()
	stack.pop()
	stack.append(res)
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
	text = text.replace("and", " ")
	Ors = text.split("or")
	return Ors


def parseprereq(text):
	if text.find("General Requirements") != -1:	
		return parse2(text)
	# remove unneeded text, make parsing easier
	text = text.replace("Undergraduate level", "")
 

	text = text.replace("Minimum Grade of C-", "")
	text = text.replace("Minimum Grade of C", "")
	text = text.replace("Minimum Grade of D-", "")
	text = text.replace("Minimum Grade of D", "")
	text = text.replace("Minimum Grade of S", "")
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
	#print list1
	# fun with stacks
	stack = []
	while list1 != []:
		i = list1.pop(0)
		if i == "(":
			stack.append(i)
		elif i == ")":
			stack = pullParen(stack)
		elif i == "|":
			while len(stack) >= 3 and stack[len(stack) -2] == "&":
				a = stack.pop()
				stack.pop()
				b = stack.pop()
				stack.append(applyAnd(a,b))
			stack.append(i)
		elif i == "&":
			while len(stack) >= 3 and stack[len(stack) -2] == "&":
				a = stack.pop()
				stack.pop()
				b = stack.pop()
				stack.append(applyAnd(a,b))
			stack.append(i)
		else:
			stack.append([i + list1.pop(0)])
	# some courses reference non-existant or outdated information. (EE255, ECE 46200)...
	#print stack
	while len(stack) > 2:
		a = stack.pop()
		op = stack.pop()
		b = stack.pop()
		if op == "|":
			stack.append(applyOr(a,b))
		elif op == "&":
			stack.append(applyAnd(a,b))
		else:
			print "uh-oh\n"
			print(op)	
			print("\n")	
	#print stack
	if len(stack) < 1:
		return []
	else:
		return stack[0]

