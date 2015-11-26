import os
import urllib2

import webapp2
import jinja2

import json
import logging

from datetime import datetime

from google.appengine.ext import ndb
from bs4 import BeautifulSoup as BS

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)



def user_key(user_name="Test"):

	return ndb.Key('User', user_name)

class Challenge(ndb.Model):
	challengeid=ndb.IntegerProperty()
	complete=ndb.BooleanProperty()

class Lecture(ndb.Model):
	module=ndb.StringProperty()
	location=ndb.StringProperty()
	date=ndb.IntegerProperty()
	time=ndb.IntegerProperty()
	attended=ndb.StringProperty()

class User(ndb.Model):
	username=ndb.StringProperty()
	challenges=ndb.StructuredProperty(Challenge, repeated=True)
	lectures=ndb.StructuredProperty(Lecture, repeated=True)

class CheckIn(ndb.Model):
	student=ndb.StringProperty()
	lecture=ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)



class LectureCode(ndb.Model):
	lecture=ndb.StringProperty()
	code=ndb.StringProperty()
	creator=ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

class ThisUser():
	username=""

class LoginPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/login.html')
		self.response.write(template.render())

	def post(self):
		exists=False;
		ThisUser.username=self.request.get('username')
		userQuery = User.query(User.username == self.request.get('username'))
		for user in userQuery:
			exists=True;
			if(user.username == 'lecturer'):
				self.redirect('/lhome')
			
			else:
				self.redirect('/home')

		if(exists==False):
			user = User(username=self.request.get('username'),
				challenges=[Challenge(challengeid=1, complete=True),
							Challenge(challengeid=2, complete=False),
							Challenge(challengeid=3, complete=False),
							Challenge(challengeid=4, complete=False),
							Challenge(challengeid=5, complete=False),
							Challenge(challengeid=6, complete=False),
							Challenge(challengeid=7, complete=False),
							Challenge(challengeid=8, complete=False),
							Challenge(challengeid=9, complete=False)],
				lectures=[Lecture(module="LECT1111", location="34", date=25, time=22)])
			user.put()
			self.redirect('/home')


class StudentHome(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'username' : ThisUser.username
		}
		template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
		self.response.write(template.render(template_values))

	def post(self):
		logging.info(self.request.body)
		data = json.loads(self.request.body)
		latitude = data["lat"]
		longitude = data["lon"]

		logging.info(latitude)
		logging.info(longitude)
		
		self.response.out.write(json.dumps({"valid":1}))
		
		#time = datetime.now()

		#self.response.write(" Day:" + str(time.day))
		#self.response.write(" Hour:" + str(time.hour))
		#self.response.write(" Min:" + str(time.minute))			

		#meQuery = User.query(User.username == ThisUser.username)
		#for me in meQuery:
		#	for lecture in me.lectures:
		#		if(lecture.date == time.day and lecture.time == time.hour):
		#			self.response.write(" working")




class CheckInPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/checkin.html')
		self.response.write(template.render())

	def post(self):
		code = " " + self.request.get('checkincode')
		lecture = self.request.get('checkinlecture')
		invalidcode=True;

		lectureCodeQuery = LectureCode.query(LectureCode.lecture == lecture)
		for lectureCode in lectureCodeQuery:
			if(lectureCode.code == code):
				checkin = CheckIn()
				checkin.student=template_values['username']
				checkin.lecture=lecture
				checkin.put()
				invalidcode=False;
				self.redirect('/home')
		
		if(invalidcode):
			self.response.write("Invalid Code")
		

class ChallengesPage(webapp2.RequestHandler):
	def get(self):

		template_values = {

		}

		query = User.query(User.username == ThisUser.username)
		for user in query:
			for challenge in user.challenges:
				if(challenge.complete):
					template_values['status'+str(challenge.challengeid)] = "success"
				else:
					template_values['status'+str(challenge.challengeid)] = "null"

		template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
		self.response.write(template.render(template_values))


class HistoryPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
		self.response.write(template.render())

class CodePage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/codegenerator.html')
		self.response.write(template.render())

	def post(self):
		lecturecode = LectureCode()
		lecturecode.lecture = self.request.get('lecture')
		lecturecode.code = self.request.get('code')
		lecturecode.creator = template_values['username']

		codeQuery = LectureCode.query(LectureCode.lecture == self.request.get('lecture'))
		for code in codeQuery:
			code.key.delete()

		lecturecode.put()
		self.redirect('/lhome')
		
class LecturerHome(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'username' : ThisUser.username
		}
		template = JINJA_ENVIRONMENT.get_template('/assets/lecturerhome.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
	('/', LoginPage),
	('/home', StudentHome),
	('/checkin', CheckInPage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/code', CodePage),
	('/lhome', LecturerHome)
], debug=True)