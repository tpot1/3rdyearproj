from models import Challenge, Lecture, User, CheckIn, ThisUser, Badge, Module, Building

def loadModules():
	LECT1111 = Module(
			code='LECT1111',
			lectures=[
				Lecture(module='LECT1111', location=1, day='MONDAY', time=13),
				Lecture(module='LECT1111', location=2, day='TUESDAY', time=14),
				Lecture(module='LECT1111', location=3, day='WEDNESDAY', time=15),
				Lecture(module='LECT1111', location=4, day='THURSDAY', time=16)])

	LECT1112 = Module(
			code='LECT1112',
			lectures=[
				Lecture(module='LECT1112', location=1, day='MONDAY', time=9),
				Lecture(module='LECT1112', location=2, day='TUESDAY', time=9),
				Lecture(module='LECT1112', location=3, day='WEDNESDAY', time=18),
				Lecture(module='LECT1112', location=4, day='FRIDAY', time=20)])

	LECT1113 = Module(
			code='LECT1113',
			lectures=[
				Lecture(module='LECT1113', location=1, day='MONDAY', time=10),
				Lecture(module='LECT1113', location=3, day='WEDNESDAY', time=12),
				Lecture(module='LECT1113', location=4, day='THURSDAY', time=9),
				Lecture(module='LECT1113', location=2, day='FRIDAY', time=18)])

	LECT1114 = Module(
			code='LECT1114',
			lectures=[
				Lecture(module='LECT1114', location=1, day='MONDAY', time=12),
				Lecture(module='LECT1114', location=2, day='TUESDAY', time=15),
				Lecture(module='LECT1114', location=3, day='WEDNESDAY', time=10),
				Lecture(module='LECT1114', location=4, day='THURSDAY', time=14)])

	LECT0000 = Module(
		code='LECT0000',
			lectures=[
				Lecture(module='LECT0000', location=0, day='MONDAY', time=10),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=10),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=10),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=10),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=10),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=10),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=10),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=11),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=11),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=11),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=11),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=11),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=11),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=11),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=12),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=12),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=12),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=12),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=12),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=12),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=12),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=13),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=13),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=13),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=13),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=13),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=13),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=13),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=14),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=14),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=14),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=14),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=14),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=14),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=14),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=15),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=15),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=15),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=15),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=15),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=15),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=15),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=16),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=16),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=16),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=16),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=16),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=16),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=16),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=17),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=17),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=17),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=17),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=17),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=17),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=17),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=18),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=18),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=18),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=18),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=18),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=18),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=18),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=19),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=19),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=19),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=19),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=19),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=19),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=19),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=20),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=20),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=20),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=20),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=20),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=20),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=20),

				Lecture(module='LECT0000', location=0, day='MONDAY', time=21),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=21),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=21),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=21),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=21),
				Lecture(module='LECT0000', location=0, day='SATURDAY', time=21),
				Lecture(module='LECT0000', location=0, day='SUNDAY', time=21)])

	LECT0000.put()
	LECT1111.put()
	LECT1112.put()
	LECT1113.put()
	LECT1114.put()