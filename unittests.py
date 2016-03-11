import unittest
import sys
import os
import time
import datetime

# adding additional google app engine libraries to path
AE_PATH = "C:\Program Files (x86)\Google\google_appengine"

APP_PATH = os.path.abspath(".")

EXTRA_PATHS = [
    APP_PATH,
    AE_PATH,
    os.path.join(AE_PATH, 'lib', 'antlr3'),
    os.path.join(AE_PATH, 'lib', 'django'),
    os.path.join(AE_PATH, 'lib', 'ipaddr'),
    os.path.join(AE_PATH, 'lib', 'webob-1.2.3'),
    os.path.join(AE_PATH, 'lib', 'webapp2-2.5.2'),
    os.path.join(AE_PATH, 'lib', 'jinja2-2.6'),
    os.path.join(AE_PATH, 'lib', 'yaml', 'lib')
]
sys.path = EXTRA_PATHS + sys.path

from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire
from handlers import getCurrentWeek, missedLectureCheck, challengecheck, point_in_poly


class TestCase(unittest.TestCase):

	currentTime = time.time()

	userEntity = User(
				userid='1234',
				score=0,
				streak=0,
				count=0,
				lectures=[Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=11, duration=1),
						Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=12, duration=1),
						Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=13, duration=1)],
				challenges=[Challenge(challengeid=1, title='First Step', description='Check in to 1 lecture', complete=False, expiresat=currentTime+864000, badge=Badge(iconName='/img/firststeps.png'), points=10),
							Challenge(challengeid=2, title='Not Bad', description='Check in to 5 lectures', complete=False, expiresat=currentTime+1382400, badge=Badge(iconName='/img/notbad.png'), points=30),
							Challenge(challengeid=3, title='Golden Student', description='Check in to 10 lectures', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/goldenstudent.png'), points=50),
							Challenge(challengeid=5, title='Hat-trick', description='Check in to 3 consecutive lectures', complete=False, expiresat=currentTime+1382400, badge=Badge(iconName='/img/hattrick.png'), points=30),
							Challenge(challengeid=6, title='Unstoppable', description='Check in to 5 consecutive lectures', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/unstoppable.png'), points=50),
							Challenge(challengeid=7, title='Perfect Week', description='Attend every lecture in a week', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/perfectweek.png'), points=20),
							Challenge(challengeid=8, title='Selective Attendance', description='Attend the same lecture 3 weeks in a row', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/selectiveattendance.png'), points=30),
							Challenge(challengeid=9, title='Early Bird', description='Make it to a 9am lecture', complete=False, expiresat=currentTime+1382400, badge=Badge(iconName='/img/earlybird.png'), points=10),
							Challenge(challengeid=10, title='Long day', description='Check in to 4 lectures in the same day', complete=False, expiresat=currentTime+1987200, badge=Badge(iconName='/img/longday.png'), points=30)],
				history=[])

	lecture = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=11, duration=1, week=getCurrentWeek(), attended=True)

	checkin = CheckIn(student=userEntity, lecture=lecture, date=datetime.date.today(), time=datetime.datetime.now().time())
		
	# challenge 1 is complete after checking in to one lecture
	# so should be complete after the first check in 
	def test_chall1(self):
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete[0].challengeid, 1)

	# challenge 2 is complete after checking in to 5 lectures
	# so i should not complete when the initial count is 3, but should
	# complete when the initial count is 4
	def test_chall2(self):
		self.userEntity.count = 3
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete, [])
		self.userEntity.count = 4
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete[0].challengeid, 2)

	# same logic for challenge 3, but it needs 10 check-ins to complete
	def test_chall3(self):
		self.userEntity.count = 8
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete, [])
		self.userEntity.count = 9
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete[0].challengeid, 3)

	# similar logic for challenge 5, should only be complete when the streak is 
	# incremented to 3
	def test_chall5(self):
		self.userEntity.streak = 1
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete, [])
		self.userEntity.streak = 2
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete[0].challengeid, 5)

	# same logic for challenge 6 but with a streak of 5
	def test_chall6(self):
		self.userEntity.streak = 3
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete, [])
		self.userEntity.streak = 4
		complete = challengecheck(self.userEntity, self.lecture, self.checkin)
		self.assertEqual(complete[0].challengeid, 6)

	# challenge 7 should only complete once the user has
	# checked in to all of their lectures in the same week
	def test_chall7(self):
		self.userEntity.history = []

		lecture1 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=11, duration=1, week=getCurrentWeek(), attended=True)
		lecture2 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=12, duration=1, week=getCurrentWeek(), attended=True)
		lecture3 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=13, duration=1, week=getCurrentWeek(), attended=True)
		
		checkin1 = CheckIn(student=self.userEntity, lecture=lecture1, date=datetime.date.today(), time=datetime.datetime.now().time())
		checkin2 = CheckIn(student=self.userEntity, lecture=lecture2, date=datetime.date.today(), time=datetime.datetime.now().time())
		checkin3 = CheckIn(student=self.userEntity, lecture=lecture3, date=datetime.date.today(), time=datetime.datetime.now().time())
		
		self.userEntity.history.append(lecture1)
		complete = challengecheck(self.userEntity, lecture1, checkin1)
		self.assertEqual(complete, [])

		self.userEntity.history.append(lecture2)
		complete = challengecheck(self.userEntity, lecture2, checkin2)
		self.assertEqual(complete, [])

		self.userEntity.history.append(lecture3)
		complete = challengecheck(self.userEntity, lecture3, checkin3)
		self.assertEqual(complete[0].challengeid, 7)


	# completes if the user has checked in to the same lecture 3 weeks in a row
	# so should only complete after the 3rd lecture is checked in
	def test_chall8(self):
		self.userEntity.history = []

		pastLecture1 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=11, duration=1, week=getCurrentWeek(), attended=True)
		
		self.userEntity.history.append(pastLecture1)
		checkin1 = CheckIn(student=self.userEntity, lecture=pastLecture1, date=datetime.date.today(), time=datetime.datetime.now().time())
		complete = challengecheck(self.userEntity, pastLecture1, checkin1)
		self.assertEqual(complete, [])

		pastLecture2 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=11, duration=1, week=getCurrentWeek()-1, attended=True)
		self.userEntity.history.append(pastLecture2)
		checkin2 = CheckIn(student=self.userEntity, lecture=pastLecture2, date=datetime.date.today(), time=datetime.datetime.now().time())
		complete = challengecheck(self.userEntity, pastLecture2, checkin2)
		self.assertEqual(complete, [])

		pastLecture3 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=11, duration=1, week=getCurrentWeek()-2, attended=True)
		self.userEntity.history.append(pastLecture3)
		checkin3 = CheckIn(student=self.userEntity, lecture=pastLecture3, date=datetime.date.today(), time=datetime.datetime.now().time())
		complete = challengecheck(self.userEntity, pastLecture3, checkin3)
		self.assertEqual(complete[0].challengeid, 8)

	# completes if user checks in to a 9am lecture, so should only
	# complete for lectures with time=9
	def test_chall9(self):
		lecture1 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=10, duration=1, week=getCurrentWeek(), attended=True)
		checkin1 = CheckIn(student=self.userEntity, lecture=lecture1, date=datetime.date.today(), time=datetime.datetime.now().time())
		complete = challengecheck(self.userEntity, lecture1, checkin1)
		self.assertEqual(complete, [])

		lecture2 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=9, duration=1, week=getCurrentWeek(), attended=True)
		checkin2 = CheckIn(student=self.userEntity, lecture=lecture2, date=datetime.date.today(), time=datetime.datetime.now().time())
		complete = challengecheck(self.userEntity, lecture2, checkin2)
		self.assertEqual(complete[0].challengeid, 9)


	# checks in to 4 lectures on the same day, ensuring the challenge
	# is only complete upon checking in to the 4th lecture
	def test_chall10(self):
		self.userEntity.history = []

		lecture1 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=14, duration=1, week=getCurrentWeek(), attended=True)
		lecture2 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=15, duration=1, week=getCurrentWeek(), attended=True)
		lecture3 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=16, duration=1, week=getCurrentWeek(), attended=True)
		lecture4 = Lecture(module='GENG0013', title='TT Math Support', location='2', day=0, time=17, duration=1, week=getCurrentWeek(), attended=True)

		checkin1 = CheckIn(student=self.userEntity, lecture=lecture1, date=datetime.date.today(), time=datetime.datetime.now().time())
		checkin2 = CheckIn(student=self.userEntity, lecture=lecture2, date=datetime.date.today(), time=datetime.datetime.now().time())
		checkin3 = CheckIn(student=self.userEntity, lecture=lecture3, date=datetime.date.today(), time=datetime.datetime.now().time())
		checkin4 = CheckIn(student=self.userEntity, lecture=lecture4, date=datetime.date.today(), time=datetime.datetime.now().time())

		self.userEntity.history.append(lecture1)
		complete = challengecheck(self.userEntity, lecture1, checkin1)
		self.assertEqual(complete, [])

		self.userEntity.history.append(lecture2)
		complete = challengecheck(self.userEntity, lecture2, checkin2)
		self.assertEqual(complete, [])

		self.userEntity.history.append(lecture3)
		complete = challengecheck(self.userEntity, lecture3, checkin3)
		self.assertEqual(complete, [])

		self.userEntity.history.append(lecture4)
		complete = challengecheck(self.userEntity, lecture4, checkin4)
		self.assertEqual(complete[0].challengeid, 10)

	# this function checks for any missed lectures, so I test that it
	# only counts lectures which haven't occured yet and ignores lectures
	# which are currently occuring - for both single and double lectures
	def test_missedLectureCheck(self):
		day = datetime.date.today().weekday()
		hour = datetime.datetime.now().hour
		minute = datetime.datetime.now().minute
		if minute > 45:
			hour = hour + 1

		self.userEntity.history = []
		self.userEntity.lectures = []
		# adds a single lecture which has already occured, and therefore should be counted as 'missed'
		self.userEntity.lectures.append(Lecture(module='GENG0013', title='0', location='2', day=day, time=hour-1 , duration=1))
		# adds a double lecture which has already occured, and therefore should be counted as 'missed'
		self.userEntity.lectures.append(Lecture(module='GENG0013', title='1', location='2', day=day, time=hour-2 , duration=2))
		# adds a single lecture which is currently occuring, so shouldn't be missed
		self.userEntity.lectures.append(Lecture(module='GENG0013', title='2', location='2', day=day, time=hour , duration=1))
		# adds a double lecture which is currently occuring, so shouldn't be missed
		self.userEntity.lectures.append(Lecture(module='GENG0013', title='3', location='2', day=day, time=hour-1 , duration=2))

		missedLectureCheck(self.userEntity)

		# checks that, in all of the previous weeks, there is a match for each timetabled lecture in the history
		for i in range(1, getCurrentWeek()):
			for lecture in self.userEntity.lectures:
				matched = False
				for pastLecture in self.userEntity.history:
					if pastLecture.week == i and pastLecture.day == lecture.day and pastLecture.time == lecture.time:
						matched = True
				self.assertTrue(matched)

		# an array representing the 4 lectures defined above
		# if they have been added to history, they invert their corresponding value
		# so the first two lectures should invert the first two values to True
		# while the second two should leave their values as True
		checked = [False, False, True, True]

		for pastLecture in self.userEntity.history:
			if pastLecture.week == getCurrentWeek():
				checked[int(pastLecture.title)] = not checked[int(pastLecture.title)]

		for checkedLecture in checked:
			self.assertTrue(checkedLecture)

	# this function checks if a given point is inside a given polygon
	# I defined the building shapes as squares, so I am testing the
	# function using a square as the polygon, with various points inside and outside the square
	def test_pointInPoly(self):
		# defining the coordinates of a square, using simple values to make things easier
		poly = [(0, 0), (0, 1), (1, 1), (1, 0)]
		# a point in the middle
		self.assertTrue(point_in_poly(0.5, 0.5, poly))
		# points just within the polygon
		self.assertTrue(point_in_poly(0.001, 0.001, poly))
		self.assertTrue(point_in_poly(0.999, 0.001, poly))
		self.assertTrue(point_in_poly(0.999, 0.999, poly))
		self.assertTrue(point_in_poly(0.001, 0.999, poly))
		# points just outside the polygon
		self.assertFalse(point_in_poly(0, 0, poly))
		self.assertFalse(point_in_poly(1, 0, poly))
		self.assertFalse(point_in_poly(1.001, 1, poly))
		self.assertFalse(point_in_poly(0, 1, poly))


if __name__ == '__main__':
	unittest.main()