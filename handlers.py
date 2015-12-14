import os

import jinja2
import webapp2
from google.appengine.api import users

from models import Challenge, Lecture, User, CheckIn, ThisUser, Badge, Day 

from datetime import datetime
from google.appengine.ext import ndb
import json
import logging
import urllib2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

#def challengecheck(user):	call this whenever a user attends a lecture?
#	for challenge in user.challenges:
#		if(challenge.predicate):
#			challenge.complete=True
#			challenge.put

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


#class LoginPage(webapp2.RequestHandler):
	#def get(self):
		#template = JINJA_ENVIRONMENT.get_template('/assets/login.html')
		#self.response.write(template.render())
#	def get(self):
#		user = users.get_current_user()
#
#		if user:
#			self.redirect('/home')
#		else:
#			self.redirect(users.create_login_url(self.request.uri))
#
#	def post(self):
#		exists=False;
#		ThisUser.username=self.request.get('username')
#		userQuery = User.query(User.username == self.request.get('username'))
#		for user in userQuery:
#			exists=True;
#			self.redirect('/home')
#
#		if(exists==False):
#			user = User(username=self.request.get('username'),
#				challenges=[Challenge(challengeid=1, complete=False),
#							Challenge(challengeid=2, complete=False),
#							Challenge(challengeid=3, complete=False),
#							Challenge(challengeid=4, complete=False),
#							Challenge(challengeid=5, complete=False),
#							Challenge(challengeid=6, complete=False),
#							Challenge(challengeid=7, complete=False),
#							Challenge(challengeid=8, complete=False),
#							Challenge(challengeid=9, complete=False)],
#				lectures=[],
#				score=0,
#				streak=0)
#			user.put()
#			self.redirect('/modules')


class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			exists=False
			for existingUser in userQuery:
				exists=True

			if(exists==False):
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
		#logging.info(self.request.body)
		data = json.loads(self.request.body)
		latitude = data["lat"]
		longitude = data["lon"]

		#logging.info(latitude)
		#logging.info(longitude)
		
		#poly = [(-1.39313923280514, 50.9354851665757),(-1.39297834453775, 50.9357212920631),(-1.39255721433256, 50.9356073903953),(-1.39271810259994, 50.9353712643295),(-1.39313923280514, 50.9354851665757)]

		poly = [(52.187149, 0.207588), (52.187349, 208165), (52.186322, 0.209375), (52.186111, 0.208449)];

		point_in_poly(latitude, longitude, poly);

		if(point_in_poly(latitude, longitude, poly)):
			location = CheckIn(lat=latitude, lon=longitude)
			location.put()
			self.response.out.write(json.dumps({"valid":1}))
			userQuery = User.query(User.username == ThisUser.username)
			#for user in userQuery:
				#user.score = user.score + 10 + user.streak;
				#user.streak = user.streak + 1;
				#user.put()
		else: 
			self.response.out.write(json.dumps({"valid":2}))

		#time = datetime.now()

		#self.response.write(" Day:" + str(time.day))
		#self.response.write(" Hour:" + str(time.hour))
		#self.response.write(" Min:" + str(time.minute))			

		#meQuery = User.query(User.username == ThisUser.username)
		#for me in meQuery:
		#	for lecture in me.lectures:
		#		if(lecture.date == time.day and lecture.time == time.hour):
		#			self.response.write(" working")

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
		self.response.write(self.request.get('module1'));
		self.response.write(self.request.get('module2'));
		self.response.write(self.request.get('module3'));
		self.response.write(self.request.get('module4'));
		

class ChallengesPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			template_values = {
				'logout' : users.create_logout_url(self.request.uri)
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
				'logout' : users.create_logout_url(self.request.uri)
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')
