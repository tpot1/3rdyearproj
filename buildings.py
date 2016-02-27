from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire
from google.appengine.ext import ndb

def loadBuildings():
	b2 = Building(number='2', coordinates=[ndb.GeoPt(50.935625 , -1.399638), ndb.GeoPt(50.937450 , -1.398635), ndb.GeoPt(50.936862 , -1.395631), ndb.GeoPt(50.934408 , -1.39561)])
	b2.put()

	b2a = Building(number='2a', coordinates=[ndb.GeoPt(50.936293 , -1.398331), ndb.GeoPt(50.936932 , -1.397786), ndb.GeoPt(50.936626 , -1.396432), ndb.GeoPt(50.935791 , -1.396821)])
	b2a.put()

	b5 = Building(number='5', coordinates=[ndb.GeoPt(50.935158 , -1.396452), ndb.GeoPt(50.936392 , -1.396039), ndb.GeoPt(50.936040 , -1.393147), ndb.GeoPt(50.934556 , -1.393732)])
	b5.put()

	b7 = Building(number='7', coordinates=[ndb.GeoPt(50.935205 , -1.39605), ndb.GeoPt(50.936527 , -1.39554), ndb.GeoPt(50.935888 , -1.391554), ndb.GeoPt(50.934211 , -1.392649)])
	b7.put()

	b13 = Building(number='13', coordinates=[ndb.GeoPt(50.935334 , -1.395867), ndb.GeoPt(50.936727 , -1.394987), ndb.GeoPt(50.935946 , -1.391404), ndb.GeoPt(50.934370 , -1.392198)])
	b13.put()

	b16 = Building(number='16', coordinates=[ndb.GeoPt(50.937261 , -1.39708), ndb.GeoPt(50.938437 , -1.396393), ndb.GeoPt(50.938119 , -1.394167), ndb.GeoPt(50.936612 , -1.394537)])
	b16.put()

	b27 = Building(number='27', coordinates=[ndb.GeoPt(50.933654 , -1.39598), ndb.GeoPt(50.935286 , -1.394408), ndb.GeoPt(50.934756 , -1.391742), ndb.GeoPt(50.933282 , -1.392488)])
	b27.put()

	b32 = Building(number='32', coordinates=[ndb.GeoPt(50.935929 , -1.39642), ndb.GeoPt(50.937004 , -1.396817), ndb.GeoPt(50.937014 , -1.395524), ndb.GeoPt(50.935783 , -1.395218)])
	b32.put()

	b34 = Building(number='34', coordinates=[ndb.GeoPt(50.934127 , -1.397085), ndb.GeoPt(50.935344 , -1.396092), ndb.GeoPt(50.934948 , -1.393475), ndb.GeoPt(50.933427 , -1.39443)])
	b34.put()

	b35 = Building(number='35', coordinates=[ndb.GeoPt(50.934685, -1.395358), ndb.GeoPt(50.934719, -1.395513), ndb.GeoPt(50.934299, -1.394059), ndb.GeoPt(50.933488, -1.394676)])
	b35.put()

	b58 = Building(number='58', coordinates=[ndb.GeoPt(50.936172 , -1.40054), ndb.GeoPt(50.937592 , -1.400003), ndb.GeoPt(50.937220 , -1.396795), ndb.GeoPt(50.935314 , -1.397391)])
	b58.put()

	b59 = Building(number='59', coordinates=[ndb.GeoPt(50.936764 , -1.398464), ndb.GeoPt(50.937825 , -1.398721), ndb.GeoPt(50.937866 , -1.397026), ndb.GeoPt(50.936821 , -1.396591)])
	b59.put()

	b67 = Building(number='67', coordinates=[ndb.GeoPt(50.935966 , -1.397648), ndb.GeoPt(50.937322 , -1.397863), ndb.GeoPt(50.937487 , -1.395679), ndb.GeoPt(50.935956 , -1.395014)])
	b67.put()