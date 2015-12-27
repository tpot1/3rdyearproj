import os

import webapp2
from google.appengine.api import users

from models import Challenge, Lecture, User, CheckIn, ThisUser, Badge, Module, Building

from challenges import loadChallenges
from modules import loadModules
from buildings import loadBuildings

import jinja2
from datetime import datetime
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

def timeConversion(remainingTime):
	if(remainingTime < 3600):
		return str(math.ceil(remainingTime/60)).split('.')[0] + " mins"
	elif(remainingTime < 86400):
		return str(math.floor(remainingTime/3600)).split('.')[0] + " hours"
	else:
		return str(math.floor(remainingTime/86400)).split('.')[0] + " days"

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())

			userEntity = None

			for thisUser in userQuery:
				userEntity = thisUser

			if userEntity is None:
				self.redirect('/modules')

			else:
				template_values = {
					'username' : user.nickname(),
					'logout' : users.create_logout_url(self.request.uri),
					'score' : userEntity.score,
					'streak' : userEntity.streak,
					'count' : userEntity.count
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
		elif point_in_poly(longitude, latitude, poly):
			checkin = CheckIn(student=thisUser, lecture=thisLecture)
			checkin.put()
			thisLecture.attended = True
			thisLecture.put()

			thisUser.score = thisUser.score + 10 + thisUser.streak
			thisUser.streak = thisUser.streak + 1
			thisUser.count = thisUser.count + 1
			for lecture in thisUser.lectures:
				if(lecture.key == thisLecture.key):
					lecture.attended = True
			thisUser.put()
			self.response.out.write(json.dumps({"valid":1, "score":thisUser.score, "count":thisUser.count, "streak":thisUser.streak}))
			challengecheck(thisUser, thisLecture, checkin)
		else: 
			self.response.out.write(json.dumps({"valid":2}))	

class ModuleSelectPage(webapp2.RequestHandler):
	def get(self):
		#loadChallenges()
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
					count=0)

				challengeQuery = Challenge.query()
				for challenge in challengeQuery:
					userEntity.challenges.append(challenge)

				userEntity.put()

				template_values = {
					'logout' : users.create_logout_url(self.request.uri)
				}

				template = JINJA_ENVIRONMENT.get_template('/assets/modules.html')
				self.response.write(template.render(template_values))

				self.response.out.write("<script> var moduleList = document.getElementById('moduleList');")

				moduleQuery = Module.query()
				for module in moduleQuery:
					self.response.out.write("var option = document.createElement('option'); option.text = option.value = option.name = '" + module.code + "'; moduleList.add(option,moduleList.length);")

				self.response.out.write("</script>")

			else:
				self.redirect('/')
		else:
			self.redirect('/')

	def post(self):
		user = users.get_current_user()

		userQuery = User.query(User.userid == user.user_id())
		for thisUser in userQuery:

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

		self.redirect('/')


class ChallengesPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'challenges' : 'class=active'
			}

			template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
			self.response.write(template.render(template_values))

			self.response.out.write('<script> var table = document.getElementById("challengeTable"); ')

			currTime = time.time()
			query = User.query(User.userid == user.user_id())
			for thisUser in query:
				for challenge in thisUser.challenges:
					if type(challenge) != Challenge:
						challenge = challenge.b_val
					if(currTime > challenge.expiresat):
						thisUser.challenges.remove(challenge)
						thisUser.put()
					else:
						self.response.out.write('var row = table.insertRow(table.rows.length); var cell1 = row.insertCell(0); var cell2 = row.insertCell(1); var cell3 = row.insertCell(2); cell1.innerHTML = "'+challenge.title+'"; cell2.innerHTML = "'+challenge.description+'"; cell3.innerHTML = "'+timeConversion(challenge.expiresat - currTime)+'"; ')
						if challenge.complete:
							self.response.out.write('row.className = "success"; ')

			self.response.out.write('</script>')
			
		else:
			self.redirect('/')


class HistoryPage(webapp2.RequestHandler):
	def get(self):
		#loadChallenges()
		user = users.get_current_user()
		if(user):

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'history' : 'class=active',
			}

			userQuery = User.query(User.userid == user.user_id())
			for thisUser in userQuery:
				for lecture in thisUser.lectures:
					template_values[lecture.day+str(lecture.time)] = lecture.module

			template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')
