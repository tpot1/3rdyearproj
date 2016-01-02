import os

import webapp2

from handlers import HomePage, ChallengesPage, HistoryPage, ModuleSelectPage, ProfilePage

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/modules', ModuleSelectPage),
	('/profile', ProfilePage)
], debug=True)