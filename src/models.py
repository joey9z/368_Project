from google.appengine.ext import ndb

###############################
## Database Models
##
## Reference: https://cloud.google.com/appengine/docs/python/ndb/properties
###############################

########################
## Requisite
########################
    
class Requisite(ndb.Model):
    course = ndb.StringProperty()   # course code, eg. "ECE20100"
    # changed name to reqType, type is a keyword
    reqType = ndb.BooleanProperty() # represents prerequisite (1) or co-requisite (0)

########################
## RequisiteList
## See: https://cloud.google.com/appengine/docs/python/ndb/properties#structured
########################
    
class RequisiteList(ndb.Model):
    courses = ndb.LocalStructuredProperty(Requisite, repeated=True)   # list of AND conditions

#################
## Course Model
#################

class Course(ndb.Model):
    title = ndb.StringProperty()        # unicode string up to 1500 bytes
    description = ndb.TextProperty()    # unicode string of unlimited length
    form = ndb.StringProperty(repeated=True)        # unicode string up to 1500 bytes
    number = ndb.StringProperty()      # 64-bit signed integer      
    credits = ndb.FloatProperty()		# float because some classes have half credits (source: I got 3.5 credits for ENGR 141/2)
    department = ndb.StringProperty()
    semesters = ndb.StringProperty(repeated=True)
    campuses = ndb.StringProperty(repeated=True)
    requisites = ndb.LocalStructuredProperty(RequisiteList, repeated=True) # lists of complete OR conditions
