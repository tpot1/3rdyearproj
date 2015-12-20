import os

import webapp2
from google.appengine.api import users

from models import Challenge, Lecture, User, CheckIn, ThisUser, Badge, Module, Building

import jinja2
from datetime import datetime
import time
from google.appengine.ext import ndb
import json
import logging
import urllib2
import math
from bs4 import BeautifulSoup as Soup

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def challengecheck(user, lecture):	
	for challenge in user.challenges:
		if type(challenge) != Challenge:
			challenge = challenge.b_val

		if predicates[challenge.challengeid](user, lecture):
			challenge.complete = True;
			user.put()

def predicate1(user, lecture):
	if lecture.time == 9:
		return True
	else:
	 return False

def predicate2(user, lecture):
	return False

def predicate3(user, lecture):
	return False

def predicate4(user, lecture):
	return False

def predicate5(user, lecture):
	return False

def predicate6(user, lecture):
	return False

def predicate7(user, lecture):
	return False

def predicate8(user, lecture):
	return False

def predicate9(user, lecture):
	return True

predicates = {
	1 : predicate1,
	2 : predicate2,
	3 : predicate3,
	4 : predicate4,
	5 : predicate5,
	6 : predicate6,
	7 : predicate7,
	8 : predicate8,
	9 : predicate9
}

def point_in_poly(x,y,poly):
	n = len(poly)
	inside = False

	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y

	return inside

def timeConversion(remainingTime):
	logging.info(remainingTime)
	if(remainingTime < 3600):
		return str(math.ceil(remainingTime/60)).split('.')[0] + " mins"
	elif(remainingTime < 86400):
		return str(math.floor(remainingTime/3600)).split('.')[0] + " hours"
	else:
		return str(math.floor(remainingTime/86400)).split('.')[0] + " days"

def loadModules():
	LECT1111 = Module(
			code='LECT1111',
			lectures=[
				Lecture(module='LECT1111', location=1, day='MONDAY', time=13),
				Lecture(module='LECT1111', location=2, day='TUESDAY', time=14),
				Lecture(module='LECT1111', location=3, day='WEDNESDAY', time=15),
				Lecture(module='LECT1111', location=4, day='THURSDAY', time=16)])

	LECT1112 = Module(
			code='LECT1112',
			lectures=[
				Lecture(module='LECT1112', location=1, day='MONDAY', time=9),
				Lecture(module='LECT1112', location=2, day='TUESDAY', time=9),
				Lecture(module='LECT1112', location=3, day='WEDNESDAY', time=18),
				Lecture(module='LECT1112', location=4, day='FRIDAY', time=20)])

	LECT1113 = Module(
			code='LECT1113',
			lectures=[
				Lecture(module='LECT1113', location=1, day='MONDAY', time=10),
				Lecture(module='LECT1113', location=3, day='WEDNESDAY', time=12),
				Lecture(module='LECT1113', location=4, day='THURSDAY', time=9),
				Lecture(module='LECT1113', location=2, day='FRIDAY', time=18)])

	LECT1114 = Module(
			code='LECT1114',
			lectures=[
				Lecture(module='LECT1114', location=1, day='MONDAY', time=12),
				Lecture(module='LECT1114', location=2, day='TUESDAY', time=15),
				Lecture(module='LECT1114', location=3, day='WEDNESDAY', time=10),
				Lecture(module='LECT1114', location=4, day='THURSDAY', time=14)])

	LECT0000 = Module(
		code='LECT0000',
			lectures=[
				Lecture(module='LECT0000', location=0, day='MONDAY', time=12),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=12),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=12),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=12),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=12),
				Lecture(module='LECT0000', location=0, day='MONDAY', time=20),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=20),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=20),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=20),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=20),
				Lecture(module='LECT0000', location=0, day='MONDAY', time=21),
				Lecture(module='LECT0000', location=0, day='TUESDAY', time=21),
				Lecture(module='LECT0000', location=0, day='WEDNESDAY', time=21),
				Lecture(module='LECT0000', location=0, day='THURSDAY', time=21),
				Lecture(module='LECT0000', location=0, day='FRIDAY', time=21)])

	LECT0000.put()
	#LECT1111.put()
	#LECT1112.put()
	#LECT1113.put()
	#LECT1114.put()

def loadBuildings():
	house = Building(number='0', coordinates=[ndb.GeoPt(52.187149, 0.207588), ndb.GeoPt(52.187349, 0.208165), ndb.GeoPt(52.186322, 0.209375), ndb.GeoPt(52.186111, 0.208449)])
	house.put()

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			if userQuery.count() == 0:
				currentTime = time.time()
				newUser = User(
					userid=user.user_id(),
					email=user.email(),
					#instead of this I should probably make a list of challenges, and then update the users challenges from the list
					challenges=[Challenge(challengeid=1, title='Early Bird', description='Make it to a 9am lecture', complete=False, expiresat=currentTime+172800),
								Challenge(challengeid=2, title='First Blood', description='Be the first in your class to check in to a lecture', complete=False, expiresat=currentTime+72800),
								Challenge(challengeid=3, title='Logging Streak', description='Check in to 5 consecutive lectures', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=4, title='I can go all day', description='Attend every lecture in a day', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=5, title='Perfect Week', description='Attend every lecture in a week', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=6, title="Teacher's Pet", description='Have the highest (or joint highest) attendance out of all the students in your class', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=7, title='First Steps', description='Check in to 1 lecture', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=8, title='Larger Steps', description='Check in to 5 lectures', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=9, title='Golden Student', description='Check in to 15 lectures', complete=False, expiresat=currentTime+120)],
					lectures=[],
					score=0,
					streak=0)
				newUser.put()
				self.redirect('/modules')

			template_values = {
				'username' : user.nickname(),
				'logout' : users.create_logout_url(self.request.uri)
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/home.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user = users.get_current_user()
		#logging.info(self.request.body)
		data = json.loads(self.request.body)
		latitude = data["lat"]
		longitude = data["lon"]

		days = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

		intday = datetime.today().weekday()
		day = days[intday]
		hour = datetime.now().hour

		thisLecture=Lecture()
		poly = []

		userQuery = User.query(User.userid == user.user_id())
		for userEntity in userQuery:
			for lecture in userEntity.lectures:
				if(lecture.day == day and lecture.time == hour):
					thisLecture = lecture
					buildingQuery = Building.query(Building.number == str(lecture.location))
					for building in buildingQuery:
						for i in range(0, len(building.coordinates)):
							poly.append((building.coordinates[i].lat, building.coordinates[i].lon))
		
		#poly = [(-1.39313923280514, 50.9354851665757),(-1.39297834453775, 50.9357212920631),(-1.39255721433256, 50.9356073903953),(-1.39271810259994, 50.9353712643295),(-1.39313923280514, 50.9354851665757)]
		#poly = [(52.187149, 0.207588), (52.187349, 0.208165), (52.186322, 0.209375), (52.186111, 0.208449)];
		

		#if not poly:
		#	self.response.out.write(json.dumps({"valid":3}))

		#elif point_in_poly(latitude, longitude, poly):
		if True:
			checkin = CheckIn(student=user.user_id(), lecture=thisLecture.module)
			checkin.put()
			self.response.out.write(json.dumps({"valid":1}))
			for userEntity in userQuery:
				userEntity.score = userEntity.score + 10 + userEntity.streak;
				userEntity.streak = userEntity.streak + 1;
				userEntity.put()
				challengecheck(userEntity, thisLecture)
		else: 
			self.response.out.write(json.dumps({"valid":2}))


class ModuleSelectPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			template_values = {
				'logout' : users.create_logout_url(self.request.uri)
			}
			template = JINJA_ENVIRONMENT.get_template('/assets/modules.html')
			self.response.write(template.render(template_values))
		else:

			self.redirect('/')

	def post(self):
		user = users.get_current_user()

		userQuery = User.query(User.userid == user.user_id())
		for thisUser in userQuery:

			module1 = self.request.get('module1');
			module2 = self.request.get('module2');
			module3 = self.request.get('module3');
			module4 = self.request.get('module4');

			moduleQuery1 = Module.query(Module.code == module1)
			for module in moduleQuery1:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery2 = Module.query(Module.code == module2)
			for module in moduleQuery2:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery3 = Module.query(Module.code == module3)
			for module in moduleQuery3:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			moduleQuery4 = Module.query(Module.code == module4)
			for module in moduleQuery4:
				for lecture in module.lectures:
					thisUser.lectures.append(lecture)

			thisUser.put()

		self.redirect('/')


class ChallengesPage(webapp2.RequestHandler):
	def get(self):
		#loadModules()
		#loadBuildings()

		soup = Soup(open('challenges.html'))

		tbody = soup.find('thead')
		meta = soup.new_tag('tbody')
		meta['content'] = "<tr class=success> <td>TEST</td> <td>test/td> <td>testtt</td> </tr>"
		meta['http-equiv'] = "Content-Type"
		tbody.insert_after(meta)

		print soup

		user = users.get_current_user()
		if(user):
			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'challenges' : 'class=active'
			}
			query = User.query(User.userid == user.user_id())
			for thisUser in query:
				for challenge in thisUser.challenges:
					if type(challenge) != Challenge:
						challenge = challenge.b_val
					if(time.time() > challenge.expiresat):
						thisUser.challenges.remove(challenge)
						thisUser.put()
					else:
						template_values['title'+str(challenge.challengeid)] = challenge.title
						template_values['desc'+str(challenge.challengeid)] = challenge.description
						template_values['time'+str(challenge.challengeid)] = timeConversion(challenge.expiresat - time.time())
						if(challenge.complete):
							template_values['status'+str(challenge.challengeid)] = "success"
						else:
							template_values['status'+str(challenge.challengeid)] = "null"

			template = JINJA_ENVIRONMENT.get_template('challenges.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')


class HistoryPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):

			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'history' : 'class=active',

			}

			userQuery = User.query(User.userid == user.user_id())
			for thisUser in userQuery:
				for lecture in thisUser.lectures:
					template_values[lecture.day+str(lecture.time)] = lecture.module

			template = JINJA_ENVIRONMENT.get_template('/assets/history.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')
