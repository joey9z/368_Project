#this contains nifty global sets...
#names may need to be adjusted based on how formatted in classes

#also, if needed, could consider whether set, list, or dict are best for these data

EECore = {"ECE201","ECE207","ECE202","ECE255","ECE208","ECE270","ECE301","ECE302","ECE311"}

CompECore = {"ECE201","ECE207","ECE264","ECE202","ECE270","ECE301","ECE362","ECE337","ECE368","ECE364","ECE302"}

ECESeminars = {"ECE200","ECE400"}

ECEAdvCompE = [["ECE437","ECE468"],["ECE437","ECE469"]]

#how do I manage this epics thing where they have to be consecutive semesters... have a condition in the final schedule check
ECESenDes = [["ECE495"],["ECE477"],["ECE411","ECE412"]]

ECEElectiveCompE = [#Uhhh, not sure how to do these...]

FirstYrEng = [["ENGR131", "ENGR132"],["EPCS111", "EPCS121", "ENGR133", "CS159"], ["ENGR141","ENGR142"]]

EEmath = [["MA161","MA162","MA261"]]#gotta figure this and sciences out as well
#gen eds will be decided kinda like ECEElectives

BreadthReq = 3#implementation is the question, this one is fairly easy though

def EERequired(crse):
	temp = crse.getTitle()
	if(temp.issubset(EECore) or temp.issubset(CompECore) or temp.issubset(ECESeminars) or ()):
        pass

def CompERequired(crse):
	temp = crse.getTitle()
	if True:
        pass