from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire
from google.appengine.ext import ndb

def loadBuildings():
	b2 = Building(number='2', coordinates=[ndb.GeoPt(50.935794, -1.399204), ndb.GeoPt(50.935418, -1.398013), ndb.GeoPt(50.936554, -1.397198), ndb.GeoPt(50.936804, -1.398083)])
	b2.put()

	b2a = Building(number='2a', coordinates=[ndb.GeoPt(50.936351, -1.398109), ndb.GeoPt(50.936754, -1.397766), ndb.GeoPt(50.936608, -1.396927), ndb.GeoPt(50.936111, -1.397257)])
	b2a.put()

	b5 = Building(number='5', coordinates=[ndb.GeoPt(50.935510, -1.395476), ndb.GeoPt(50.935881, -1.39517), ndb.GeoPt(50.935648, -1.394177), ndb.GeoPt(50.935266, -1.394462)])
	b5.put()

	b7 = Building(number='7', coordinates=[ndb.GeoPt(50.935324, -1.394848), ndb.GeoPt(50.935807, -1.394483), ndb.GeoPt(50.935395, -1.392831), ndb.GeoPt(50.934793, -1.393346)])
	b7.put()

	b13 = Building(number='13', coordinates=[ndb.GeoPt(50.935638, -1.394526), ndb.GeoPt(50.936159, -1.394151), ndb.GeoPt(50.935682, -1.39252), ndb.GeoPt(50.935172, -1.392826)])
	b13.put()

	b16 = Building(number='16', coordinates=[ndb.GeoPt(50.937511, -1.396151), ndb.GeoPt(50.937950, -1.395738), ndb.GeoPt(50.937788, -1.3951), ndb.GeoPt(50.937284, -1.395341)])
	b16.put()

	b27 = Building(number='27', coordinates=[ndb.GeoPt(50.934009, -1.394569), ndb.GeoPt(50.934877, -1.394156), ndb.GeoPt(50.934529 , -1.392901), ndb.GeoPt(50.933623 , -1.393448)])
	b27.put()

	b32 = Building(number='32', coordinates=[ndb.GeoPt(50.935878 , -1.396205), ndb.GeoPt(50.936926 , -1.396371), ndb.GeoPt(50.937014 , -1.395524), ndb.GeoPt(50.935783 , -1.395218)])
	b32.put()

	b34 = Building(number='34', coordinates=[ndb.GeoPt(50.934306 , -1.396001), ndb.GeoPt(50.934904 , -1.39561), ndb.GeoPt(50.934634 , -1.394483), ndb.GeoPt(50.934042 , -1.394773)])
	b34.put()

	b35 = Building(number='35', coordinates=[ndb.GeoPt(50.934685, -1.395358), ndb.GeoPt(50.934719, -1.395513), ndb.GeoPt(50.934299, -1.394059), ndb.GeoPt(50.933488, -1.394676)])
	b35.put()

	b58 = Building(number='58', coordinates=[ndb.GeoPt(50.936318 , -1.399606), ndb.GeoPt(50.937098 , -1.39908), ndb.GeoPt(50.936825 , -1.39775), ndb.GeoPt(50.936067 , -1.398206)])
	b58.put()

	b59 = Building(number='59', coordinates=[ndb.GeoPt(50.936889 , -1.398056), ndb.GeoPt(50.937663 , -1.398222), ndb.GeoPt(50.937677 , -1.397321), ndb.GeoPt(50.936936 , -1.397165)])
	b59.put()

	b67 = Building(number='67', coordinates=[ndb.GeoPt(50.936125 , -1.396908), ndb.GeoPt(50.937230 , -1.397171), ndb.GeoPt(50.937298 , -1.396248), ndb.GeoPt(50.936216 , -1.395969)])
	b67.put()