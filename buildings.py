from models import Challenge, Lecture, User, CheckIn, ThisUser, Badge, Module, Building

def loadBuildings():
	house = Building(number='0', coordinates=[ndb.GeoPt(52.187149, 0.207588), ndb.GeoPt(52.187349, 0.208165), ndb.GeoPt(52.186322, 0.209375), ndb.GeoPt(52.186111, 0.208449)])
	house.put()