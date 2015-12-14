import os

import webapp2
import jinja2

from handlers import HomePage, ChallengesPage, HistoryPage, ModuleSelectPage

app = webapp2.WSGIApplication([
	#('/', LoginPage),
	('/', HomePage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/modules', ModuleSelectPage)
], debug=True)