import os

import webapp2

from handlers import HomePage, ChallengesPage, HistoryPage, ModuleSelectPage, SettingsPage

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/modules', ModuleSelectPage),
	('/settings', SettingsPage)
], debug=True)