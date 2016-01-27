from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Survey
import time

def loadChallenges():
	currentTime = time.time()

	chall1 = Challenge(challengeid=1, title='Early Bird', description='Make it to a 9am lecture', complete=False, expiresat=currentTime+172800, badge=Badge(iconName='/img/icon1.png'))
	chall2 = Challenge(challengeid=2, title='First Blood', description='Be the first in your class to check in to a lecture', complete=False, expiresat=currentTime+72800, badge=Badge(iconName='/img/icon2.png'))
	chall3 = Challenge(challengeid=3, title='Logging Streak', description='Check in to 5 consecutive lectures', complete=False, expiresat=currentTime+1800, badge=Badge(iconName='/img/icon3.png'))
	chall4 = Challenge(challengeid=4, title='I can go all day', description='Attend every lecture in a day', complete=False, expiresat=currentTime+8000, badge=Badge(iconName='/img/icon4.png'))
	chall5 = Challenge(challengeid=5, title='Perfect Week', description='Attend every lecture in a week', complete=False, expiresat=currentTime+10000, badge=Badge(iconName='/img/icon5.png'))
	chall6 = Challenge(challengeid=6, title="Teacher's Pet", description='Have the highest (or joint highest) attendance out of all the students in your class', complete=False, expiresat=currentTime+1500, badge=Badge(iconName='/img/icon6.png'))
	chall7 = Challenge(challengeid=7, title='First Steps', description='Check in to 1 lecture', complete=False, expiresat=currentTime+12000, badge=Badge(iconName='/img/icon7.png'))
	chall8 = Challenge(challengeid=8, title='Larger Steps', description='Check in to 5 lectures', complete=False, expiresat=currentTime+500, badge=Badge(iconName='/img/icon8.png'))
	chall9 = Challenge(challengeid=9, title='Golden Student', description='Check in to 15 lectures', complete=False, expiresat=currentTime+600, badge=Badge(iconName='/img/icon9.png'))

	chall1.put()
	chall2.put()
	chall3.put()
	chall4.put()
	chall5.put()
	chall6.put()
	chall7.put()
	chall8.put()
	chall9.put()