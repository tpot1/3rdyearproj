from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire
import time

def loadChallenges():
	currentTime = time.time()

	chall1 = Challenge(challengeid=1, title='First Steps', description='Check in to 1 lecture', complete=False, expiresat=currentTime+604800, badge=Badge(iconName='/img/firststeps.png'), points=10)
	chall2 = Challenge(challengeid=2, title='Larger Steps', description='Check in to 5 lectures', complete=False, expiresat=currentTime+1209600, badge=Badge(iconName='/img/largersteps.png'), points=50)
	chall3 = Challenge(challengeid=3, title='Golden Student', description='Check in to 10 lectures', complete=False, expiresat=currentTime+2419200, badge=Badge(iconName='/img/goldenstudent.png'), points=100)
	chall4 = Challenge(challengeid=4, title='Gotta Go Fast', description='Be the first in your class to check in to a lecture', complete=False, expiresat=currentTime+604800, badge=Badge(iconName='/img/gottagofast.png'), points=30)
	chall5 = Challenge(challengeid=5, title='Logging Streak', description='Check in to 5 consecutive lectures', complete=False, expiresat=currentTime+2419200, badge=Badge(iconName='/img/loggingstreak.png'), points=50)
	chall6 = Challenge(challengeid=6, title='Perfect Week', description='Attend every lecture in a week', complete=False, expiresat=currentTime+604800, badge=Badge(iconName='/img/perfectweek.png'), points=30)
	
	chall1.put()
	chall2.put()
	chall3.put()
	chall4.put()
	chall5.put()
	chall6.put()