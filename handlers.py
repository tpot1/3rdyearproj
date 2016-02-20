import os

import webapp2
from google.appengine.api import users

from models import Challenge, Lecture, User, CheckIn, Badge, Module, Building, Questionnaire

from challenges import loadChallenges
from modules import loadModules
from buildings import loadBuildings

import jinja2
import datetime
import time
from google.appengine.ext import ndb
import json
import logging
import urllib2
import math

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def challengecheck(user, lecture, checkin):	
	currTime = time.time()
	completedChalls = []

	for challenge in user.challenges:
		if type(challenge) != Challenge:
			challenge = challenge.b_val

		if not challenge.complete and currTime < challenge.expiresat:
			if predicates[challenge.challengeid](user, lecture, checkin):
				challenge.complete = True;
				completedChalls.append(challenge)
				user.put()

	return completedChalls

def missedLectureCheck(user):
	day = datetime.date.today().weekday()
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute
	if minute > 45:
		hour = hour + 1

	userQuery = User.query(User.userid == user.user_id())
	#gets the current user
	for userEntity in userQuery:
		#loops through the weeks that have occurred so far
		for i in range(1, getCurrentWeek()):
			#loops through the users lectures
			for lecture in userEntity.lectures:
				#sets the default value to not attended
				attended = False
				#loops through the lectures in history
				for attlecture in userEntity.history:
					#checks for a match
					if attlecture.week == i and attlecture.day == lecture.day and attlecture.time == lecture.time:
							#if one is found, there is an entry in the history so don't need to worry
							attended = True
				if not attended:
					#else we need to add that the user missed that lecture to the history
					missedLecture = lecture
					missedLecture.attended = False
					missedLecture.week = i
					userEntity.history.append(missedLecture)
					userEntity.streak = 0

		#does the same check for the current week
		for lecture in userEntity.lectures:
			#only applies to lectures that have already occured
			if lecture.day < day or (lecture.day == day and lecture.time+lecture.duration <= hour):
				#sets the default value to False
				attended = False
				for attlecture in userEntity.history:
					if attlecture.week == getCurrentWeek() and attlecture.day == lecture.day and attlecture.time == lecture.time:
						attended = True
				if not attended:
					missedLecture = lecture
					missedLecture.attended = False
					missedLecture.week = getCurrentWeek()
					userEntity.history.append(missedLecture)
					userEntity.streak = 0

		userEntity.put()

def formCheck(self, user):

	return True

	userQuery = User.query(User.userid == user.user_id())
	# #gets the current user
	for userEntity in userQuery:
	 	#checks that they have gone through the procedue of reading the participant information
	 	if userEntity.info != True:
	 		self.redirect('/info')
	 	#agreeing to the consent form
	 	elif userEntity.consent != True:
	 		self.redirect('/consentform')
	 	#completing the questionnaire
	 	elif userEntity.questionnaire is None:
	 		self.redirect('/questionnaire')
	 	#and creating a username
	 	elif userEntity.username is None:
	 		self.redirect('/ftp')


def predicate1(user, lecture, checkin):
	#always returns true since only needs 1 check in
	return True

def predicate2(user, lecture, checkin):
	if user.count >= 4:
		return True
	else:
		return False

def predicate3(user, lecture, checkin):
	if user.count >= 9:
		return True
	else:
		return False

def predicate4(user, lecture, checkin):
	# finds all check ins for the same lecture, by other students
	checkinQuery = CheckIn.query().filter(CheckIn.lecture.day == lecture.day, CheckIn.lecture.time == lecture.time, CheckIn.lecture.week == getCurrentWeek(), CheckIn.lecture.module == lecture.module, CheckIn.student.userid != user.userid)
	for otherCheckin in checkinQuery:
		# checks if any were made earlier than this check in
		if otherCheckin.time < checkin.time:
			return False

	return True

def predicate5(user, lecture, checkin):
	# the streak will increase after this check in, so if its equal to 2 it will become 3
	if user.streak >= 2:
		return True
	else:
		return False

def predicate6(user, lecture, checkin):
	# the streak will increase after this check in, so if its equal to 4 it will become 5
	if user.streak >= 4:
		return True
	else:
		return False

def predicate7(user, lecture, checkin):
	#loops through all lectures in history for the current week, checking for a match
	for lecture in user.lectures:
		matched = False
		for attlecture in user.history:
			if attlecture.week == getCurrentWeek() and attlecture.day == lecture.day and attlecture.time == lecture.time and attlecture.attended == True:
				matched = True
		if not matched:
			return False

	return True

def predicate8(user, lecture, checkin):
	prev1 = False
	prev2 = False
	#loops through all previous lectures, looking for a lecture that matches the current one from the past 2 weeks
	for prevLecture in user.history:
		if prevLecture.day == lecture.day and prevLecture.time == lecture.time and prevLecture.module == lecture.module and prevLecture.attended:
			if prevLecture.week == getCurrentWeek()-1:
				prev1 = True
			elif prevLecture.week == getCurrentWeek()-2:
				prev2 = True
		
	return prev1 and prev2

def predicate9(user, lecture, checkin):
	return lecture.time == 9

def predicate10(user, lecture, checkin):
	count = 0
	for pastLecture in user.history:
		if pastLecture.day == lecture.day and pastLecture.week == getCurrentWeek() and pastLecture.attended:
			count += 1

	return count >= 4

predicates = {
	1 : predicate1,
	2 : predicate2,
	3 : predicate3,
	4 : predicate4,
	5 : predicate5,
	6 : predicate6,
	7 : predicate7,
	8 : predicate8,
	9 : predicate9,
	10 : predicate10	
}

def point_in_poly(x,y,poly):
	n = len(poly)
	inside = False

	#stores the first two values in the poly
	p1x,p1y = poly[0]
	for i in range(n+1):
		#stores the next two values
		p2x,p2y = poly[i % n]
		#checks if y is greater than the smallest y coord out of the two
		if y > min(p1y,p2y):
			#and less than or equal to the biggest y coord
			if y <= max(p1y,p2y):
				#and x is less than or equal to the biggest x coord
				if x <= max(p1x,p2x):
					#if the two y points are different
					if p1y != p2y:
						#draws an imaginary line between the two points
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					#checks the x point is the correct side of it
					if p1x == p2x or x <= xints:
						inside = not inside
		#moves on to next point
		p1x,p1y = p2x,p2y

	return inside

def timeConversion(expireTime):
	remainingTime = int(expireTime) - time.time()
	if(remainingTime < 3600):
		return str(math.ceil(remainingTime/60)).split('.')[0] + " mins"
	elif(remainingTime < 86400):
		return str(math.floor(remainingTime/3600)).split('.')[0] + " hours"
	else:
		return str(math.floor(remainingTime/86400)).split('.')[0] + " days"

def getCurrentWeek():
	#creates a date object, starting from the first day of semester 2
	startWeek = datetime.date(2016, 1, 25) 
	#gets the current date
	currDate = datetime.date.today()	
	#stores the current week number
	weekctr = 0 		
	
	# adds 7 days to the start week until it is larger than the current week, then returns the number of weeks added
	while startWeek <= currDate:
		startWeek += datetime.timedelta(days = 7)
		weekctr += 1

	return weekctr

class ParticipationInfoPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			for userEntity in userQuery:
				if userEntity.info:
					self.redirect('/')

			template_values = {
				'logout' : users.create_logout_url(self.request.uri)
			}

			template = JINJA_ENVIRONMENT.get_template('/assets/participantInfo.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			for userEntity in userQuery:
				userEntity.info = True
				userEntity.put()
				userEntity.put()
				self.redirect('/consentform')
		else:
			self.redirect(users.create_login_url(self.request.uri))


class ConsentFormPage(webapp2.RequestHandler):
	def get(self, error=""):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			for userEntity in userQuery:
				if userEntity.consent:
					self.redirect('/')

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'error' : error
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/consentForm.html')
			self.response.write(template.render(template_values))

		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		if(user):

			input1 = str(self.request.get('input1')).lower()
			input2 = str(self.request.get('input2')).lower()
			input3 = str(self.request.get('input3')).lower()

			if input1 == input2 == input3:
				if input1.isalpha():
					if input1 != "":
						userQuery = User.query(User.userid == user.user_id())
						for userEntity in userQuery:
							userEntity.consent = True
							userEntity.put()
							userEntity.put()
							self.redirect('/questionnaire')
					else:
						self.get("Your initials boxes were empty")
				else:
					self.get("You have invalid numbers or symbols in your initials")
			else:
				self.get("The initials you entered did not match")
		else:
			self.redirect(users.create_login_url(self.request.uri))


class QuestionnairePage(webapp2.RequestHandler):
	def get(self, error=""):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			for userEntity in userQuery:
				if userEntity.questionnaire is not None:
					self.redirect('/')

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'error' : error
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/questionnaire.html')
			self.response.write(template.render(template_values))

		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		if(user):

			valid = True

			for i in range(1, 10):
				answer = str(self.request.get("q"+str(i)))
				if answer == "":
					self.get("You must answer all of the questions")
					valid = False
				elif not answer.isdigit():
					self.get("Something went wrong. Please try again")
					valid = False

			if valid:
				userQuery = User.query(User.userid == user.user_id())
				for userEntity in userQuery:
					userEntity.questionnaire = Questionnaire(
						answer1 = int(self.request.get("q1")),
						answer2 = int(self.request.get("q2")),
						answer3 = int(self.request.get("q3")),
						answer4 = int(self.request.get("q4")),
						answer5 = int(self.request.get("q5")),
						answer6 = int(self.request.get("q6")),
						answer7 = int(self.request.get("q7")),
						answer8 = int(self.request.get("q8")),
						answer9 = int(self.request.get("q9")))
					userEntity.put()
					userEntity.put()
					self.redirect('/ftp')
		else:
			self.redirect(users.create_login_url(self.request.uri))
		
class FirstTimePage(webapp2.RequestHandler):
	def get(self, error=""):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			for userEntity in userQuery:
				if userEntity.username is not None:
					self.redirect('/')

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'error' : error
			}

			template = JINJA_ENVIRONMENT.get_template('/assets/usernameSelect.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		if(user):
			username = str(self.request.get('username'))
			taken = False

			usernameQuery = User.query()
			for allUsers in usernameQuery:
				if allUsers.username == username:
					taken = True

			if taken:
				self.get("Username taken. Please try another.")

			else:
				userQuery = User.query(User.userid == user.user_id())
				for userEntity in userQuery:
					if len(username) == 0:
						self.response.write("Please enter a username.")
					elif len(username) > 15:
						self.response.write("Your username is too long.")
					else:
						userEntity.username = username
						userEntity.put()
						userEntity.put()
						self.redirect('/')
		else:
			self.redirect(users.create_login_url(self.request.uri))

		

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())

			userEntity = None

			for thisUser in userQuery:
				userEntity = thisUser
				formCheck(self, user)
				missedLectureCheck(user)

			if userEntity is None:
				userEntity = User(
					userid=user.user_id(),
					score=0,
					streak=0,
					count=0,
					history=[])

				module1Query = Module.query(Module.code == 'GENG0013')
				for module in module1Query:
					for lecture in module.lectures:
						userEntity.lectures.append(lecture)

				module2Query = Module.query(Module.code == 'GENG0002')
				for module in module2Query:
					for lecture in module.lectures:
						userEntity.lectures.append(lecture)

				challengeQuery = Challenge.query().order(Challenge.challengeid)
				for challenge in challengeQuery:
					userEntity.challenges.append(challenge)

				userEntity.put()
				self.redirect('/info')

			completedChalls = []

			for challenge in userEntity.challenges:
				if challenge.complete:
					completedChalls.append(challenge)

			template_values = {
				'username' : userEntity.username,
				'logout' : users.create_logout_url(self.request.uri),
				'score' : userEntity.score,
				'count' : userEntity.count,
				'streak' : userEntity.streak,
				'completedChalls' : completedChalls
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
			self.response.write(template.render(template_values))

		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		if user:
			missedLectureCheck(user)
			#logging.info(self.request.body)
			data = json.loads(self.request.body)
			latitude = data["lat"]
			longitude = data["lon"]

			day = datetime.date.today().weekday()
			hour = datetime.datetime.now().hour
			minute = datetime.datetime.now().minute
			if minute > 45:
				hour = hour + 1

			thisLecture = None
			thisUser = None
			poly = []


			day = 6
			hour = 10
			

			userQuery = User.query(User.userid == user.user_id())
			for userEntity in userQuery:
				thisUser = userEntity
				#for lecture in userEntity.lectures:
					
				lecture = Lecture(module='GENG0013', title='TT Math Support', location='35', day=6, time=9, duration=2)
				#checks for a lecture that matches the current day and time
				if(lecture.day == day and (lecture.time <= hour and lecture.time + lecture.duration > hour)):
					thisLecture = lecture
					locations = lecture.location.split(";");
					for location in locations:
						#need to make multiple polys for each lecture, for each possible location
						buildingQuery = Building.query(Building.number == location)
						for building in buildingQuery:
							buildingCoords = []
							for coordinate in building.coordinates:
								c = (coordinate.lon, coordinate.lat)
								buildingCoords.append(c)
							poly.append(buildingCoords)

			noLecture = False
			checkedIn = False

			#checks if there is no current lecture
			if thisLecture is None:
				noLecture = True
				self.response.out.write(json.dumps({"valid":3}))
			# else:
			# 	#checks if the user has already checked in to this lecture
			# 	for pastLecture in thisUser.history:
			# 		if pastLecture.week == getCurrentWeek() and pastLecture.time == thisLecture.time and pastLecture.day == thisLecture.day:
			# 			checkedIn = True
			# 			self.response.out.write(json.dumps({"valid":4}))	
			if not checkedIn and not noLecture:
				inBuilding = False
				for coords in poly:
					if True and not inBuilding:#point_in_poly(longitude, latitude, coords):
						inBuilding = True

						thisLecture.attended = True
						thisLecture.week = getCurrentWeek()

						checkin = CheckIn(student=thisUser, lecture=thisLecture)
						checkin.put()

						thisUser.history.append(thisLecture)

						completedChalls = challengecheck(thisUser, thisLecture, checkin)

						pointsEarned = 0
						
						challIcons = []
						challTitles = []
						challDescs = []
						challPoints = []

						for challenge in completedChalls:
							pointsEarned += challenge.points
							challTitles.append(challenge.title)
							challIcons.append(challenge.badge.iconName)
							challDescs.append(challenge.description)
							challPoints.append(challenge.points)

						thisUser.score = thisUser.score + 10 + thisUser.streak + pointsEarned
						thisUser.streak = thisUser.streak + 1
						thisUser.count = thisUser.count + 1

						thisUser.put()
						
						self.response.out.write(json.dumps({"valid":1, "score":thisUser.score, "count":thisUser.count, "streak":thisUser.streak, "icons":challIcons, "titles":challTitles, "points":challPoints, "descriptions":challDescs}))
				if not inBuilding: 
					self.response.out.write(json.dumps({"valid":2}))	
		else:
			self.redirect(users.create_login_url(self.request.uri))


class ChallengesPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			formCheck(self, user)
			missedLectureCheck(user)
			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'challenges' : 'class=active'
			}

			currTime = time.time()
			currentChalls = []
			completeChalls = []
			query = User.query(User.userid == user.user_id())
			for thisUser in query:
				for challenge in thisUser.challenges:
					if type(challenge) != Challenge:
						challenge = challenge.b_val
					if challenge.complete:
						completeChalls.append(challenge)
					elif currTime < challenge.expiresat:
						currentChalls.append(challenge)

			template_values['currentChalls'] = currentChalls
			template_values['completeChalls'] = completeChalls
			template_values['timeConversion'] = timeConversion

			template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
			self.response.write(template.render(template_values))
			
		else:
			self.redirect('/')


class HistoryPage(webapp2.RequestHandler):
	def get(self):
		#loadChallenges()
		#loadBuildings()
		#loadModules()
		user = users.get_current_user()
		if(user):
			formCheck(self, user)
			missedLectureCheck(user)

			dates = ['25th Jan - 29th Jan', '1st Feb - 5th Feb', '8th Feb - 12th Feb', '15th Feb - 19th Feb', '22nd Feb - 26th Feb', '29th Feb - 4th March', '8th March - 12th March', '15th March - 19th March']
			days = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'history' : 'class=active',
				'week' : getCurrentWeek(),
				'dates' : dates[getCurrentWeek()-1]
			}

			userQuery = User.query(User.userid == user.user_id())
			for thisUser in userQuery:
				for lecture in thisUser.history:
					if lecture.week == getCurrentWeek():
						for i in range(0, lecture.duration):
							if(i == 0):
								template_values[days[lecture.day]+str(lecture.time+i)] = lecture.title
							if lecture.attended:
								template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#77FF77'
							else:
								template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#FF7777'
				for lecture in thisUser.lectures:
					if days[lecture.day]+str(lecture.time) not in template_values.keys():
						for i in range(0, lecture.duration):
							if(i == 0):
								template_values[days[lecture.day]+str(lecture.time+i)] = lecture.title
							template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#DDEEFF'

			template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')

	def post(self):
		user = users.get_current_user()
		if(user):
			missedLectureCheck(user)

			weeknum = int(self.request.get('week'))

			fwd = self.request.get('fwd')
			if fwd == "Forward":
				weeknum += 1
				if weeknum > 8:
					weeknum = 8

				dates = ['25th Jan - 29th Jan', '1st Feb - 5th Feb', '8th Feb - 12th Feb', '15th Feb - 19th Feb', '22nd Feb - 26th Feb', '29th Feb - 4th March', '8th March - 12th March', '15th March - 19th March']

				template_values = {
					'logout' : users.create_logout_url(self.request.uri),
					'history' : 'class=active',
					'week' : weeknum,
					'dates' : dates[weeknum-1]
				}

				days = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

				userQuery = User.query(User.userid == user.user_id())
				for thisUser in userQuery:
					for lecture in thisUser.history:
						if lecture.week == weeknum:
							for i in range(0, lecture.duration):
								if(i == 0):
									template_values[days[lecture.day]+str(lecture.time+i)] = lecture.title
								if lecture.attended:
									template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#77FF77'
								else:
									template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#FF7777'
					for lecture in thisUser.lectures:
						if days[lecture.day]+str(lecture.time) not in template_values.keys():
							for i in range(0, lecture.duration):
								if(i == 0):
									template_values[days[lecture.day]+str(lecture.time+i)] = lecture.title
								template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#DDEEFF'

				template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
				self.response.write(template.render(template_values))
			else:
				weeknum -= 1
				if(weeknum < 1):
					weeknum = 1

				dates = ['25th Jan - 29th Jan', '1st Feb - 5th Feb', '8th Feb - 12th Feb', '15th Feb - 19th Feb', '22nd Feb - 26th Feb', '29th Feb - 4th March', '8th March - 12th March', '15th March - 19th March']

				template_values = {
					'logout' : users.create_logout_url(self.request.uri),
					'history' : 'class=active',
					'week' : weeknum,
					'dates' : dates[weeknum-1]
				}
				days = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

				userQuery = User.query(User.userid == user.user_id())
				for thisUser in userQuery:
					for lecture in thisUser.history:
						if lecture.week == weeknum:
							for i in range(0, lecture.duration):
								if(i == 0):
									template_values[days[lecture.day]+str(lecture.time+i)] = lecture.title
								if lecture.attended:
									template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#77FF77'
								else:
									template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#FF7777'
					for lecture in thisUser.lectures:
						if days[lecture.day]+str(lecture.time) not in template_values.keys():
							for i in range(0, lecture.duration):
								if(i == 0):
									template_values[days[lecture.day]+str(lecture.time+i)] = lecture.title
								template_values[days[lecture.day]+str(lecture.time+i)+'att'] = 'bgcolor=#DDEEFF'

				template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
				self.response.write(template.render(template_values))
		else:
			self.redirect('/')


class LeaderboardsPage(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()
		if(user):

			missedLectureCheck(user)

			allUsers = []
			me = None

			allUserQuery = User.query()
			for userEntity in allUserQuery:
				allUsers.append(userEntity)
				if userEntity.userid == user.user_id():
					me = userEntity

			allUsers = sorted(allUsers, key=lambda user: user.score, reverse=True)

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'leaderboards' : 'class=active',
				'users' : allUsers,
				'me' : me
			}

			template = JINJA_ENVIRONMENT.get_template('/assets/leaderboards.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')