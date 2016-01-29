from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire
import time

def loadChallenges():
	currentTime = time.time()

	chall2 = Challenge(challengeid=2, title='First Blood', description='Be the first in your class to check in to the lecture', complete=False, expiresat=currentTime+72800, badge=Badge(iconName='/img/icon2.png'), points=30)
	chall3 = Challenge(challengeid=3, title='Logging Streak', description='Check in to 5 consecutive lectures', complete=False, expiresat=currentTime+1800, badge=Badge(iconName='/img/icon3.png'), points=50)
	chall5 = Challenge(challengeid=5, title='Perfect Week', description='Attend every lecture in a week', complete=False, expiresat=currentTime+10000, badge=Badge(iconName='/img/icon5.png'), points=30)
	chall7 = Challenge(challengeid=7, title='First Steps', description='Check in to 1 lecture', complete=False, expiresat=currentTime+12000, badge=Badge(iconName='/img/icon7.png'), points=10)
	chall8 = Challenge(challengeid=8, title='Larger Steps', description='Check in to 5 lectures', complete=False, expiresat=currentTime+500, badge=Badge(iconName='/img/icon8.png'), points=50)
	chall9 = Challenge(challengeid=9, title='Golden Student', description='Check in to 10 lectures', complete=False, expiresat=currentTime+600, badge=Badge(iconName='/img/icon9.png'), points=100)

	chall2.put()
	chall3.put()
	chall5.put()
	chall7.put()
	chall8.put()
	chall9.put()