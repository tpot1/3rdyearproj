import os

import webapp2

from handlers import HomePage, ChallengesPage, HistoryPage, LeaderboardsPage, ParticipationInfoPage, ConsentFormPage, QuestionnairePage, FirstTimePage

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/challenges', ChallengesPage),
	('/history', HistoryPage),
	('/leaderboards', LeaderboardsPage),
	('/info', ParticipationInfoPage),
	('/consentform', ConsentFormPage),
	('/questionnaire', QuestionnairePage),
	('/ftp', FirstTimePage)
], debug=False)