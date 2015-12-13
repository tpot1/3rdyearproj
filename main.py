import os

import webapp2
import jinja2

from handlers import LoginPage, HomePage, ChallengesPage, HistoryPage, ModuleSelectPage

app = webapp2.WSGIApplication([
	('/', LoginPage),
	('/home', HomePage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/modules', ModuleSelectPage)
], debug=True)