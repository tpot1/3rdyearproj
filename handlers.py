import os

import webapp2
from google.appengine.api import users

from models import Challenge, Lecture, User, CheckIn, ThisUser, Badge, Module, Building

import jinja2
from datetime import datetime
from google.appengine.ext import ndb
import json
import logging
import urllib2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

#def challengecheck(user):	call this whenever a user checks in successfully
#	loop through all challenges, and call a specific check on each challenge

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

	LECT1111.put()
	LECT1112.put()
	LECT1113.put()
	LECT1114.put()

def loadBuildings():
	house = Building(number='0', coordinates=[ndb.GeoPt(52.187149, 0.207588), ndb.GeoPt(52.187349, 0.208165), ndb.GeoPt(52.186322, 0.209375), ndb.GeoPt(52.186111, 0.208449)])
	house.put()

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			if userQuery.count() == 0:
				newUser = User(
					userid=user.user_id(),
					email=user.email(),
					challenges=[Challenge(challengeid=1, complete=False),
								Challenge(challengeid=2, complete=False),
								Challenge(challengeid=3, complete=False),
								Challenge(challengeid=4, complete=False),
								Challenge(challengeid=5, complete=False),
								Challenge(challengeid=6, complete=False),
								Challenge(challengeid=7, complete=False),
								Challenge(challengeid=8, complete=False),
								Challenge(challengeid=9, complete=False)],
					lectures=[],
					score=0,
					streak=0)
				newUser.put()
				self.redirect('/modules')

			template_values = {
				'username' : user.nickname(),
				'logout' : users.create_logout_url(self.request.uri)
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		logging.info(self.request.body)
		data = json.loads(self.request.body)
		latitude = data["lat"]
		longitude = data["lon"]

		#logging.info(latitude)
		#logging.info(longitude)

		#time = datetime.now()

		#self.response.write(" Day:" + str(time.day))
		#self.response.write(" Hour:" + str(time.hour))
		#self.response.write(" Min:" + str(time.minute))			

		#meQuery = User.query(User.username == ThisUser.username)
		#for me in meQuery:
		#	for lecture in me.lectures:
		#		if(lecture.date == time.day and lecture.time == time.hour):
		#			self.response.write(" working")
		days = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

		intday = datetime.today().weekday()
		day = days[intday]
		hour = datetime.now().hour

		userQuery = User.query(User.userid == user.user_id())
		for userEntity in userQuery:
			for lecture in userEntity.lectures:
				if(lecture.day == day and lecture.time == hour):
					logging.info(lecture)

		
		#poly = [(-1.39313923280514, 50.9354851665757),(-1.39297834453775, 50.9357212920631),(-1.39255721433256, 50.9356073903953),(-1.39271810259994, 50.9353712643295),(-1.39313923280514, 50.9354851665757)]

		poly = [(52.187149, 0.207588), (52.187349, 0.208165), (52.186322, 0.209375), (52.186111, 0.208449)];

		point_in_poly(latitude, longitude, poly);

		if(point_in_poly(latitude, longitude, poly)):
			location = CheckIn(lat=latitude, lon=longitude)
			location.put()
			self.response.out.write(json.dumps({"valid":1}))
			#for user in userQuery:
				#user.score = user.score + 10 + user.streak;
				#user.streak = user.streak + 1;
				#user.put()
		else: 
			self.response.out.write(json.dumps({"valid":2}))


class ModuleSelectPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			template_values = {
				'logout' : users.create_logout_url(self.request.uri)
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/modules.html')
			self.response.write(template.render(template_values))
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
		loadBuildings()
		user = users.get_current_user()
		if(user):
			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'challenges' : 'class=active'
			}
			query = User.query(User.userid == user.user_id())
			for thisUser in query:
				for challenge in thisUser.challenges:
					if(challenge.complete):
						template_values['status'+str(challenge.challengeid)] = "success"
					else:
						template_values['status'+str(challenge.challengeid)] = "null"

			template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')


class HistoryPage(webapp2.RequestHandler):
	def get(self):
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