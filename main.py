import os

import webapp2

from handlers import HomePage, ChallengesPage, HistoryPage

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage)
], debug=True)