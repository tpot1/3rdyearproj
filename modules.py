from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire

def loadModules():

	# GENG0014 = Module(
	# 		code='GENG0014',
	# 		lectures=[
	# 			Lecture(module='GENG0014', location=35, day=3, time=15),
	# 			Lecture(module='GENG0014', location=35, day=4, time=11)])

	# GENG0014.put()

	GENG0013 = Module(
			code='GENG0013',
			lectures=[
				Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=11, duration=1),
				Lecture(module='GENG0013', title='TT Math Support', location='35', day=0, time=15, duration=1),
				Lecture(module='GENG0013', title='TT Math Support', location='16', day=3, time=9, duration=2),
				Lecture(module='GENG0013', title='TT Math Support', location='59', day=3, time=12, duration=2)])
	GENG0013.put()

	GENG0002 = Module(
			code='GENG0002',
			lectures=[
				Lecture(module='GENG0002', title='Mathematics B', location='59;67;34;32;16;13', day=0, time=17, duration=1),
				Lecture(module='GENG0002', title='Mathematics B', location='2a', day=1, time=11, duration=1),
				Lecture(module='GENG0002', title='Mathematics B', location='58', day=2, time=11, duration=1),
				Lecture(module='GENG0002', title='Mathematics B', location='2a', day=3, time=11, duration=1),
				Lecture(module='GENG0002', title='Mathematics B', location='7;5;27;16', day=3, time=16, duration=2)])

	GENG0002.put()