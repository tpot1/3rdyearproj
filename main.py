import os
import urllib

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class LoginPage(webapp2.RequestHandler):
	def get(self):

		template = JINJA_ENVIRONMENT.get_template('/assets/login.html')
		self.response.write(template.render())


class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
		self.response.write(template.render())

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