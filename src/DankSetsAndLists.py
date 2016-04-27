#this contains nifty global sets...
#names may need to be adjusted based on how formatted in classes

#also, if needed, could consider whether set, list, or dict are best for these data

EECore = ["ECE201","ECE207","ECE202","ECE255","ECE208","ECE270","ECE301","ECE302","ECE311"]

CompECore = ["ECE201","ECE207","ECE264","ECE202","ECE270","ECE301","ECE362","ECE337","ECE368","ECE369","ECE364","ECE302"]

ECESeminars = ["ECE200","ECE400"]

ECEAdvCompE = [["ECE437","ECE468"],["ECE437","ECE469"]]

simpleEEAdvSel = ["ECE305", "ECE321", "ECE362", "ECE382", "ECE438", "ECE440"]
simpleCompESel = ["ECE437", "ECE469", "ECE469"]

ECEAdvEESel = [["ECE305", "ECE321", "ECE362"],["ECE305", "ECE321", "ECE382"],["ECE305", "ECE321", "ECE438"],
["ECE305", "ECE321", "ECE440"],["ECE305","ECE362","ECE382"],["ECE305","ECE362","ECE438"],["ECE305","ECE362","ECE440"],
["ECE305","ECE382","ECE438"],["ECE305","ECE382","ECE440"],["ECE321","ECE362","ECE382"],["ECE321","ECE362","ECE438"],
["ECE321","ECE362","ECE440"],["ECE321","ECE382","ECE438"],["ECE321","ECE382","ECE440"],["ECE362","ECE382","ECE438"],
["ECE362","ECE382","ECE440"]]

#how do I manage this epics thing where they have to be consecutive semesters... have a condition in the final schedule check
ECESenDes = ["ECE495","ECE477"]

FirstYrEng = [["ENGR131", "ENGR132"],["EPCS111", "EPCS121", "ENGR133", "CS159"], ["ENGR141","ENGR142"]]

EEmath = ["MA161","MA162","MA261"]#gotta figure this and sciences out as well
#gen eds will be decided kinda like ECEElectives

def minDiff(inList,listOfLists):#args are a list(of taken courses most likely) and a list of lists
	"""returns the difference list with the minimum elements in it (each sublist of listOfLists - inList)"""
	diffList = []#list of differences
	sizesLs = []#list of sizes
	for ls in listOfLists:
		#find minimum sized difference set
		diffList.append(listDiff(ls, inList))
		sizesLs.append(len(diffList))
	return diffList[diffList.index(min(sizesLs))]#sure, that works...