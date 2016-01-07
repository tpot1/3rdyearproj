import os

import webapp2
from google.appengine.api import users

from models import Challenge, Lecture, User, CheckIn, ThisUser, Badge, Module, Building

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
	startWeek = datetime.date(2016, 1, 25)	#creates a date object, starting from the first day of semester 2
	currDate = datetime.date.today()	#gets the current date
	weekctr = 0 		#stores the current week number
	
	# adds 7 days to the start week until it is larger than the current week, then returns the number of weeks added
	while startWeek <= currDate:
		startWeek += datetime.timedelta(days = 7)
		weekctr += 1

	return weekctr

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
					email=user.email(),
					score=0,
					streak=0,
					count=0,
					history=[])

				moduleQuery = Module.query(Module.code == 'LECT0000')
				for module in moduleQuery:
					for lecture in module.lectures:
						userEntity.lectures.append(lecture)

				challengeQuery = Challenge.query()
				for challenge in challengeQuery:
					userEntity.challenges.append(challenge)

				userEntity.put()

			else:
				template_values = {
					'username' : user.nickname(),
					'logout' : users.create_logout_url(self.request.uri),
				}
				template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
				self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		#logging.info(self.request.body)
		data = json.loads(self.request.body)
		latitude = data["lat"]
		longitude = data["lon"]

		days = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

		intday = datetime.today().weekday()
		day = days[intday]
		hour = datetime.now().hour

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

		if thisLecture is None:
			self.response.out.write(json.dumps({"valid":3}))
		elif thisLecture.attended:
			self.response.out.write(json.dumps({"valid":4}))
		elif True:#point_in_poly(longitude, latitude, poly):
			checkin = CheckIn(student=thisUser, lecture=thisLecture)
			checkin.put()
			thisLecture.attended = True
			thisLecture.put()

			thisUser.score = thisUser.score + 10 + thisUser.streak
			thisUser.streak = thisUser.streak + 1
			thisUser.count = thisUser.count + 1
			thisLecture.attended = True
			thisLecture.week = getCurrentWeek()
			thisUser.history.append(thisLecture)
			thisUser.put()
			self.response.out.write(json.dumps({"valid":1, "score":thisUser.score, "count":thisUser.count, "streak":thisUser.streak}))
			challengecheck(thisUser, thisLecture, checkin)
		else: 
			self.response.out.write(json.dumps({"valid":2}))	

'''class ModuleSelectPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			if(userQuery.count() == 0):
				userEntity = User(
					userid=user.user_id(),
					email=user.email(),
					lectures=[],
					score=0,
					streak=0,
					count=0,
					history=[])

				challengeQuery = Challenge.query()
				for challenge in challengeQuery:
					userEntity.challenges.append(challenge)

				userEntity.put()

				template_values = {
					'logout' : users.create_logout_url(self.request.uri)
				}

				moduleList = []

				moduleQuery = Module.query()
				for module in moduleQuery:
					moduleList.append(module)

				template_values['modules'] = moduleList

				template = JINJA_ENVIRONMENT.get_template('/assets/modules.html')
				self.response.write(template.render(template_values))

			else:
				self.redirect('/')
		else:
			self.redirect('/')

	def post(self):
		user = users.get_current_user()

		module1 = self.request.get('module1');
		module2 = self.request.get('module2');
		module3 = self.request.get('module3');
		module4 = self.request.get('module4');

		userQuery = User.query(User.userid == user.user_id())
		for thisUser in userQuery:
			
			moduleQuery1 = Module.query(Module.code == module1)
			for module in moduleQuery1:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery2 = Module.query(Module.code == module2)
			for module in moduleQuery2:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery3 = Module.query(Module.code == module3)
			for module in moduleQuery3:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery4 = Module.query(Module.code == module4)
			for module in moduleQuery4:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			thisUser.put()

		self.redirect('/')'''


class ChallengesPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):

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

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'history' : 'class=active',
				'week' : getCurrentWeek()
			}

			userQuery = User.query(User.userid == user.user_id())
			for thisUser in userQuery:
				for lecture in thisUser.history:
					if lecture.week == getCurrentWeek():
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

class ProfilePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'profile' : 'class=active',
				'username' : user.nickname()
			}

			userEntity = None

			userQuery = User.query(User.userid == user.user_id())
			for thisUser in userQuery:
				template_values['score'] = thisUser.score
				template_values['count'] = thisUser.count
				template_values['streak'] = thisUser.streak
				userEntity = thisUser

			'''counter = 1

			for lecture in userEntity.lectures:
				if lecture.module not in template_values.values():
					template_values['mod'+str(counter)] = lecture.module
					counter = counter + 1

			for i in range(1, 5):
				if 'mod'+str(i) not in template_values:
					template_values['mod'+str(i)] = '*Module '+str(i)+'*' '''

			completedChalls = []
			for challenge in userEntity.challenges:
				if challenge.complete:
					completedChalls.append(challenge)

			template_values['completedChalls'] = completedChalls

			'''moduleList = []
			moduleQuery = Module.query()
			for module in moduleQuery:
				if module.code not in template_values.values():
					moduleList.append(module)

			template_values['modules'] = moduleList '''

			template = JINJA_ENVIRONMENT.get_template('/assets/profile.html')
			self.response.write(template.render(template_values))


		else:
			self.redirect('/')
	'''def post(self):
		user = users.get_current_user()

		userQuery = User.query(User.userid == user.user_id())
		for thisUser in userQuery:

			thisUser.lectures = []

			module1 = self.request.get('module1');
			module2 = self.request.get('module2');
			module3 = self.request.get('module3');
			module4 = self.request.get('module4');

			moduleQuery1 = Module.query(Module.code == module1)
			for module in moduleQuery1:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery2 = Module.query(Module.code == module2)
			for module in moduleQuery2:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery3 = Module.query(Module.code == module3)
			for module in moduleQuery3:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery4 = Module.query(Module.code == module4)
			for module in moduleQuery4:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			thisUser.put()

		self.redirect('/') '''