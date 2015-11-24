import os
import urllib2

import webapp2
import jinja2

from google.appengine.ext import ndb
from bs4 import BeautifulSoup as BS

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def user_key(user_name="Test"):

	return ndb.Key('User', user_name)

class User(ndb.Model):
	username=ndb.StringProperty()
	challenges=ndb.IntegerProperty()
	history=ndb.IntegerProperty()

class LectureCode(ndb.Model):
	lecture=ndb.StringProperty()
	code=ndb.StringProperty()
	creator=ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

class CheckIn(ndb.Model):
	student=ndb.StringProperty()
	lecture=ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)



class LoginPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/login.html')
		self.response.write(template.render())

	def post(self):
		exists=False;

		userQuery = User.query(User.username == self.request.get('username'))
		for user in userQuery:
			exists=True;
			if(user.username == 'lecturer'):
				self.redirect('/lhome?user='+user.username)
			
			else:
				self.redirect('/home?user='+user.username)

		if(exists==False):
			user = User(parent=user_key('User'))
			user.username=self.request.get('username')
			user.put()
			self.redirect('/home?user='+user.username)

		
		


class StudentHome(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'username' : self.request.get('user')
		}
		template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
		self.response.write(template.render())


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
		template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
		self.response.write(template.render())

	def post(self):
		challenge1 = self.response.get("chall1")
		self.response.write(challenge1)


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
		template = JINJA_ENVIRONMENT.get_template('/assets/lecturerhome.html')
		self.response.write(template.render())

app = webapp2.WSGIApplication([
	('/', LoginPage),
	('/home', StudentHome),
	('/checkin', CheckInPage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/code', CodePage),
	('/lhome', LecturerHome)
], debug=True)