import os

import webapp2

from handlers import HomePage, ChallengesPage, HistoryPage, ProfilePage

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/profile', ProfilePage)
], debug=True)