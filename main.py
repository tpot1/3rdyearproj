import os
import urllib

import webapp2
import jinja2

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def user_key(user_name="Test"):

	return ndb.Key('User', user_name)

class User(ndb.Model):
	username=ndb.StringProperty()

class LectureCode(ndb.Model):
	lecture=ndb.StringProperty()
	code=ndb.StringProperty()

class CheckIn(ndb.Model):
	student=ndb.StringProperty()
	lecture=ndb.StringProperty()


template_values = {
			
}

class LoginPage(webapp2.RequestHandler):
	def get(self):

		template = JINJA_ENVIRONMENT.get_template('/assets/login.html')
		self.response.write(template.render())

	def post(self):
		user = User(parent=user_key('User'))

		user.username=self.request.get('username')

		template_values['username'] = user.username

		user.put()
		self.redirect('/home')


class MainPage(webapp2.RequestHandler):
	def get(self):

		userQuery = User.query(User.username == "example1")
		for user in userQuery:
			template_values['example'] = user.username

		template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
		self.response.write(template.render(template_values))


class CheckInPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/checkin.html')
		self.response.write(template.render())

	def post(self):
		code = self.request.get('checkincode')		
		if(code == "test"):
			checkin = CheckIn()
			checkin.student=template_values['username']
			checkin.lecture=self.request.get('checkinlecture')
			checkin.put()
			self.redirect('/home')
		else:
			self.response.write("invalid code")


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
		

app = webapp2.WSGIApplication([
	('/', LoginPage),
	('/home', MainPage),
	('/checkin', CheckInPage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage)
], debug=True)