from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire
import time

def loadChallenges():
	currentTime = time.time()

	chall1 = Challenge(challengeid=1, title='First Step', description='Check in to 1 lecture', complete=False, expiresat=currentTime+864000, badge=Badge(iconName='/img/firststeps.png'), points=10)
	chall2 = Challenge(challengeid=2, title='Not Bad', description='Check in to 5 lectures', complete=False, expiresat=currentTime+1382400, badge=Badge(iconName='/img/notbad.png'), points=30)
	chall3 = Challenge(challengeid=3, title='Golden Student', description='Check in to 10 lectures', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/goldenstudent.png'), points=80)
	chall4 = Challenge(challengeid=4, title='Gotta Go Fast', description='Be the first in your class to check in to a lecture', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/gottagofast.png'), points=30)
	chall5 = Challenge(challengeid=5, title='Hat-trick', description='Check in to 3 consecutive lectures', complete=False, expiresat=currentTime+1382400, badge=Badge(iconName='/img/hattrick.png'), points=30) 
	chall6 = Challenge(challengeid=6, title='Unstoppable', description='Check in to 5 consecutive lectures', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/unstoppable.png'), points=50)
	chall7 = Challenge(challengeid=7, title='Perfect Week', description='Attend every lecture in a week', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/perfectweek.png'), points=20)
	chall8 = Challenge(challengeid=8, title='Selective Attendance', description='Attend the same lecture 3 weeks in a row', complete=False, expiresat=currentTime+2592000, badge=Badge(iconName='/img/selectiveattendance.png'), points=30)
	chall9 = Challenge(challengeid=9, title='Early Bird', description='Make it to a 9am lecture', complete=False, expiresat=currentTime+864000, badge=Badge(iconName='/img/earlybird.png'), points=10)
	chall10 = Challenge(challengeid=10, title='Long day', description='Check in to 4 lectures in the same day', complete=False, expiresat=currentTime+1987200, badge=Badge(iconName='/img/longday.png'), points=30)

	chall1.put()
	chall2.put()
	chall3.put()
	chall4.put()
	chall5.put()
	chall6.put()
	chall7.put()
	chall8.put()
	chall9.put()
	chall10.put()