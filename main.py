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




class LoginPage(webapp2.RequestHandler):
	def get(self):

		template = JINJA_ENVIRONMENT.get_template('/assets/login.html')
		self.response.write(template.render())

	def post(self):
		user = User(parent=user_key('User'))

		user.username=self.request.get('username')
		user.put()
		self.redirect('/home')



class MainPage(webapp2.RequestHandler):
	def get(self):
		
		template_values = {
			
		}

		query = User.query(User.username == 'test1')
		for user in query:
			 template_values['username'] = user.username

		template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
		self.response.write(template.render(template_values))

		

class ChallengesPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
		self.response.write(template.render())

class HistoryPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
		self.response.write(template.render())

app = webapp2.WSGIApplication([
	('/', LoginPage),
	('/home', MainPage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage)
], debug=True)