import os

import webapp2
from google.appengine.api import users

from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire

from challenges import loadChallenges
from modules import loadModules
from buildings import loadBuildings

import jinja2
import datetime
import time
from google.appengine.ext import ndb
import json
import logging
import urllib2
import math
from bs4 import BeautifulSoup as Soup

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def challengecheck(user, lecture, checkin):	
	for challenge in user.challenges:
		if type(challenge) != Challenge:
			challenge = challenge.b_val

		if predicates[challenge.challengeid](user, lecture, checkin):
			challenge.complete = True;
			user.put()

def missedLectureCheck(user):
	day = datetime.date.today().weekday()
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute
	if minute > 45:
		hour = hour + 1

	logging.info(getCurrentWeek())

	userQuery = User.query(User.userid == user.user_id())
	#gets the current user
	for userEntity in userQuery:
		#loops through the weeks that have occurred so far
		for i in range(1, getCurrentWeek()):
			#loops through the users lectures
			for lecture in userEntity.lectures:
				#sets the default value to not attended
				attended = False
				#loops through the lectures in history
				for attlecture in userEntity.history:
					#checks for a match
					if attlecture.week == i and attlecture.day == lecture.day and attlecture.time == lecture.time:
							#if one is found, there is an entry in the history so don't need to worry
							attended = True
				if not attended:
					#else we need to add that the user missed that lecture to the history
					missedLecture = lecture
					missedLecture.attended = False
					missedLecture.week = i
					userEntity.history.append(missedLecture)
					userEntity.streak = 0

		#does the same check for the current week
		for lecture in userEntity.lectures:
			#only applies to lectures that have already occured
			if lecture.day < day or lecture.day == day and lecture.time < hour:
				attended = False
				for attlecture in userEntity.history:
					if attlecture.week == getCurrentWeek() and attlecture.day == lecture.day and attlecture.time == lecture.time:
						attended = True
				if not attended:
					missedLecture = lecture
					missedLecture.attended = False
					missedLecture.week = getCurrentWeek()
					userEntity.history.append(missedLecture)
					userEntity.streak = 0

		userEntity.put()

def formCheck(self, user):
	 userQuery = User.query(User.userid == user.user_id())
	# #gets the current user
	# for user in userQuery:

	# 	#checks that they have gone through the procedue of reading the participant information
	# 	if user.info != True:
	# 		self.redirect('/info')
	# 	#agreeing to the consent form
	# 	elif user.consent != True:
	# 		self.redirect('/consentform')
	# 	#completing the questionnaire
	# 	elif user.questionnaire is None:
	# 		self.redirect('/questionnaire')
	# 	#and creating a username
	# 	elif user.username is None:
	# 		self.redirect('/ftp')



def predicate1(user, lecture, checkin):
	if lecture.time == 9:
		return True
	else:
		return False

def predicate2(user, lecture, checkin):
	checkinQuery = CheckIn.query(CheckIn.date == checkin.date and CheckIn.lecture.time == lecture.time and CheckIn.student.userid != user.userid)
	for otherCheckin in checkinQuery:
		if otherCheckin.time < checkin.time:
			return False

	return True

def predicate3(user, lecture, checkin):
	if user.streak >= 5:
		return True
	else:
		return False

def predicate4(user, lecture, checkin):
	return False

def predicate5(user, lecture, checkin):
	return False

def predicate6(user, lecture, checkin):
	competitors = []
	userQuery = User.query(User.userid != user.userid)
	for otherUser in userQuery:
		for otherLecture in otherUser.lectures:
			if otherLecture.module == lecture.module:
				competitors.append(otherUser)
	
	for competitor in competitors:
		if competitor.count > user.count:
			return False

	return True

def predicate7(user, lecture, checkin):
	if user.count >= 1:
		return True
	else:
		return True

def predicate8(user, lecture, checkin):
	if user.count >= 5:
		return True
	else:
		return False

def predicate9(user, lecture, checkin):
	if user.count >= 15:
		return True
	else:
		return False

predicates = {
	1 : predicate1,
	2 : predicate2,
	3 : predicate3,
	4 : predicate4,
	5 : predicate5,
	6 : predicate6,
	7 : predicate7,
	8 : predicate8,
	9 : predicate9
}

def point_in_poly(x,y,poly):
	n = len(poly)
	inside = False

	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y

	return inside

def timeConversion(expireTime):
	remainingTime = int(expireTime) - time.time()
	if(remainingTime < 3600):
		return str(math.ceil(remainingTime/60)).split('.')[0] + " mins"
	elif(remainingTime < 86400):
		return str(math.floor(remainingTime/3600)).split('.')[0] + " hours"
	else:
		return str(math.floor(remainingTime/86400)).split('.')[0] + " days"

def getCurrentWeek():
	#creates a date object, starting from the first day of semester 2
	startWeek = datetime.date(2016, 1, 25) 
	#gets the current date
	currDate = datetime.date.today()	
	#stores the current week number
	weekctr = 0 		
	
	# adds 7 days to the start week until it is larger than the current week, then returns the number of weeks added
	while startWeek <= currDate:
		startWeek += datetime.timedelta(days = 7)
		weekctr += 1

	return weekctr

class ParticipationInfoPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/participantInfo.html')
		self.response.write(template.render())

class ConsentFormPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/consentForm.html')
		self.response.write(template.render())

class QuestionnairePage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/questionnaire.html')
		self.response.write(template.render())
		
class FirstTimePage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/usernameSelect.html')
		self.response.write(template.render())
		

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())

			userEntity = None

			for thisUser in userQuery:
				userEntity = thisUser

			if userEntity is None:
				userEntity = User(
					userid=user.user_id(),
					score=0,
					streak=0,
					count=0,
					history=[])

				moduleQuery = Module.query(Module.code == 'GENG0014')
				for module in moduleQuery:
					for lecture in module.lectures:
						userEntity.lectures.append(lecture)

				challengeQuery = Challenge.query()
				for challenge in challengeQuery:
					userEntity.challenges.append(challenge)

				userEntity.put()

			formCheck(self, user)
			missedLectureCheck(user)

			completedChalls = []

			for challenge in userEntity.challenges:
				if challenge.complete:
					completedChalls.append(challenge)

			template_values = {
				'username' : user.nickname(),
				'logout' : users.create_logout_url(self.request.uri),
				'score' : userEntity.score,
				'count' : userEntity.count,
				'streak' : userEntity.streak,
				'completedChalls' : completedChalls
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		missedLectureCheck(user)
		#logging.info(self.request.body)
		data = json.loads(self.request.body)
		latitude = data["lat"]
		longitude = data["lon"]

		day = datetime.date.today().weekday()
		hour = datetime.datetime.now().hour
		minute = datetime.datetime.now().minute
		if minute > 45:
			hour = hour + 1

		thisLecture = None
		thisUser = None
		poly = []

		userQuery = User.query(User.userid == user.user_id())
		for userEntity in userQuery:
			thisUser = userEntity
			for lecture in userEntity.lectures:
				if(lecture.day == day and lecture.time == hour):
					thisLecture = lecture
					buildingQuery = Building.query(Building.number == str(lecture.location))
					for building in buildingQuery:
						for coordinate in building.coordinates:
							c = (coordinate.lon, coordinate.lat)
							poly.append(c)

		if False:#thisLecture is None:
			self.response.out.write(json.dumps({"valid":3}))
		elif False:#thisLecture.attended:
			self.response.out.write(json.dumps({"valid":4}))
		elif True:#point_in_poly(longitude, latitude, poly):



			thisLecture = Lecture() 	#TODO remove this




			
			thisLecture.attended = True
			thisLecture.week = getCurrentWeek()

			checkin = CheckIn(student=thisUser, lecture=thisLecture)
			checkin.put()

			thisUser.history.append(thisLecture)
			thisUser.put()

			thisUser.score = thisUser.score + 10 + thisUser.streak
			thisUser.streak = thisUser.streak + 1
			thisUser.count = thisUser.count + 1
			
			self.response.out.write(json.dumps({"valid":1, "score":thisUser.score, "count":thisUser.count, "streak":thisUser.streak}))
			challengecheck(thisUser, thisLecture, checkin)
		else: 
			self.response.out.write(json.dumps({"valid":2}))	


class ChallengesPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			formCheck(self, user)
			missedLectureCheck(user)
			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'challenges' : 'class=active'
			}

			currTime = time.time()
			currentChalls = []
			query = User.query(User.userid == user.user_id())
			for thisUser in query:
				for challenge in thisUser.challenges:
					if type(challenge) != Challenge:
						challenge = challenge.b_val
					if(currTime < challenge.expiresat):
						currentChalls.append(challenge)

			template_values['currentChalls'] = currentChalls
			template_values['timeConversion'] = timeConversion

			template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
			self.response.write(template.render(template_values))
			
		else:
			self.redirect('/')


class HistoryPage(webapp2.RequestHandler):
	def get(self):
		#loadChallenges()
		#loadBuildings()
		#loadModules()
		user = users.get_current_user()
		if(user):
			formCheck(self, user)
			missedLectureCheck(user)
			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'history' : 'class=active',
				'week' : getCurrentWeek()
			}

			days = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

			userQuery = User.query(User.userid == user.user_id())
			for thisUser in userQuery:
				for lecture in thisUser.history:
					if lecture.week == getCurrentWeek():
						template_values[days[lecture.day]+str(lecture.time)] = lecture.module
						if lecture.attended:
							template_values[days[lecture.day]+str(lecture.time)+'att'] = 'bgcolor=#77FF77'
						else:
							template_values[days[lecture.day]+str(lecture.time)+'att'] = 'bgcolor=#FF7777'
				for lecture in thisUser.lectures:
					if days[lecture.day]+str(lecture.time) not in template_values.keys():
						template_values[days[lecture.day]+str(lecture.time)] = lecture.module
						template_values[days[lecture.day]+str(lecture.time)+'att'] = 'bgcolor=#CCDDFF'

			template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')

	def post(self):

		user = users.get_current_user()
		if(user):

			missedLectureCheck(user)

			logging.info(self.request.body)

			data = json.loads(self.request.body)

			logging.info(data)
			#views the next week
			weeknum = getCurrentWeek()+1

			template_values = {
					'logout' : users.create_logout_url(self.request.uri),
					'history' : 'class=active',
					'week' : weeknum
				}

			userQuery = User.query(User.userid == user.user_id())
			for thisUser in userQuery:
				for lecture in thisUser.history:
					if lecture.week == weeknum:
						template_values[lecture.day+str(lecture.time)] = lecture.module
						if lecture.attended:
							template_values[lecture.day+str(lecture.time)+'att'] = 'bgcolor=#77FF77'
						else:
							template_values[lecture.day+str(lecture.time)+'att'] = 'bgcolor=#FF7777'
				for lecture in thisUser.lectures:
					if lecture.day+str(lecture.time) not in template_values.keys():
						template_values[lecture.day+str(lecture.time)] = lecture.module
						template_values[lecture.day+str(lecture.time)+'att'] = 'bgcolor=#DDEEFF'

			template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')

class LeaderboardsPage(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()
		if(user):

			missedLectureCheck(user)

			allUsers = []
			me = None

			allUserQuery = User.query()
			for userEntity in allUserQuery:
				allUsers.append(userEntity)
				if userEntity.userid == user.user_id():
					me = userEntity

			allUsers = sorted(allUsers, key=lambda user: user.score, reverse=True)

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'leaderboards' : 'class=active',
				'users' : allUsers,
				'me' : me
			}

			template = JINJA_ENVIRONMENT.get_template('/assets/leaderboards.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')