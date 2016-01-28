from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire
from google.appengine.ext import ndb

def loadBuildings():
	#house = Building(number='0', coordinates=[ndb.GeoPt(52.187149, 0.207588), ndb.GeoPt(52.187349, 0.208165), ndb.GeoPt(52.186322, 0.209375), ndb.GeoPt(52.186111, 0.208449)])
	#house.put()

	b35 = Building(number='35', coordinates=[ndb.GeoPt(50.934685, -1.395358), ndb.GeoPt(50.934719, -1.395513), ndb.GeoPt(50.934299, -1.394059), ndb.GeoPt(50.933488, -1.394676)])
	b35.put()