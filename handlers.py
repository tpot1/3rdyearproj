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

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())

			userEntity = None

			for thisUser in userQuery:
				userEntity = thisUser

			if userEntity is None:
				self.redirect('/modules')

			else:
				template_values = {
					'username' : user.nickname(),
					'logout' : users.create_logout_url(self.request.uri),
					'score' : userEntity.score,
					'streak' : userEntity.streak
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

		thisLecture = None
		poly = []

		userQuery = User.query(User.userid == user.user_id())
		for userEntity in userQuery:
			for lecture in userEntity.lectures:
				if(lecture.day == day and lecture.time == hour):
					thisLecture = lecture
					buildingQuery = Building.query(Building.number == str(lecture.location))
					for building in buildingQuery:
						for coordinate in building.coordinates:
							c = (coordinate.lon, coordinate.lat)
							poly.append(c)

		if thisLecture is None:
			self.response.out.write(json.dumps({"valid":3}))
		elif thisLecture.attended:
			self.response.out.write(json.dumps({"valid":4}))
		elif point_in_poly(longitude, latitude, poly):
			checkin = CheckIn(student=user.user_id(), lecture=thisLecture.module)
			checkin.put()
			thisLecture.attended = True
			thisLecture.put()
			for userEntity in userQuery:
				userEntity.score = userEntity.score + 10 + userEntity.streak;
				userEntity.streak = userEntity.streak + 1;
				for lecture in userEntity.lectures:
					if(lecture.key == thisLecture.key):
						lecture.attended = True
				userEntity.put()
				self.response.out.write(json.dumps({"valid":1, "score":userEntity.score, "streak":userEntity.streak}))
				challengecheck(userEntity, thisLecture)
		else: 
			self.response.out.write(json.dumps({"valid":2}))	

class ModuleSelectPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			userQuery = User.query(User.userid == user.user_id())
			if(userQuery.count() == 0):
				currentTime = time.time()
				userEntity = User(
					userid=user.user_id(),
					email=user.email(),
					#instead of this I should probably make a list of challenges, and then update the users challenges from the list
						#this would also solve the problem of users receiving their challenges at different times and therefore they exire at different times
					challenges=[Challenge(challengeid=9, title='Golden Student', description='Check in to 15 lectures', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=1, title='Early Bird', description='Make it to a 9am lecture', complete=False, expiresat=currentTime+172800),
								Challenge(challengeid=2, title='First Blood', description='Be the first in your class to check in to a lecture', complete=False, expiresat=currentTime+72800),
								Challenge(challengeid=3, title='Logging Streak', description='Check in to 5 consecutive lectures', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=4, title='I can go all day', description='Attend every lecture in a day', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=5, title='Perfect Week', description='Attend every lecture in a week', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=6, title="Teacher's Pet", description='Have the highest (or joint highest) attendance out of all the students in your class', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=7, title='First Steps', description='Check in to 1 lecture', complete=False, expiresat=currentTime+120),
								Challenge(challengeid=8, title='Larger Steps', description='Check in to 5 lectures', complete=False, expiresat=currentTime+120)],
					lectures=[],
					score=0,
					streak=0)

				userEntity.put()

				template_values = {
					'logout' : users.create_logout_url(self.request.uri)
				}

				template = JINJA_ENVIRONMENT.get_template('/assets/modules.html')
				self.response.write(template.render(template_values))

				self.response.out.write("<script> var moduleList = document.getElementById('moduleList');")

				moduleQuery = Module.query()
				for module in moduleQuery:
					self.response.out.write("var option = document.createElement('option'); option.text = option.value = option.name = '" + module.code + "'; moduleList.add(option,moduleList.length);")

				self.response.out.write("</script>")

			else:
				self.redirect('/')
		else:
			self.redirect(users.create_login_url(self.request.uri))

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

		#can be used to add appropriate code to the challenges.html file, but I can't write this to the file to update it - this is a restriction on GAE
		'''soup = Soup(open('challenges.html'))

		thead = soup.find('thead')

		tbody = soup.new_tag('tbody')

		tr = soup.new_tag('tr')
		tr['class'] = "{{status1}}"

		tdTitle = soup.new_tag('td')
		tdTitle.insert(1, "{{title1}} TEST1")

		tdDesc = soup.new_tag('td')
		tdDesc.insert(1, "{{desc1}} TEST2")

		tdTime = soup.new_tag('td')
		tdTime.insert(1, "{{time1}} TEST3")
		
		thead.insert_after(tbody)
		tbody.insert(1, tr)
		tr.insert(1, tdTitle)
		tr.insert(1, tdDesc)
		tr.insert(1, tdTime)

		logging.info(soup.prettify())

		html = soup.prettify("utf-8")
		with open("challenges.html", "w") as file:
			logging.info(file)
			#file.write(html)'''

		user = users.get_current_user()
		if(user):
			template_values = {
				'logout' : users.create_logout_url(self.request.uri),
				'challenges' : 'class=active'
			}

			activechalls=[]

			query = User.query(User.userid == user.user_id())
			for thisUser in query:
				for challenge in thisUser.challenges:
					if type(challenge) != Challenge:
						challenge = challenge.b_val
					if(time.time() > challenge.expiresat):
						thisUser.challenges.remove(challenge)
						thisUser.put()
					else:
						activechalls.append(challenge)

			for i in range(0, len(activechalls)):
				template_values['title'+str(i)] = activechalls[i].title
				template_values['desc'+str(i)] = activechalls[i].description
				template_values['time'+str(i)] = timeConversion(activechalls[i].expiresat - time.time())
				if(activechalls[i].complete):
					template_values['status'+str(i)] = "success"
				else:
					template_values['status'+str(i)] = "null"

			template = JINJA_ENVIRONMENT.get_template('/assets/challenges.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))


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
			self.redirect(users.create_login_url(self.request.uri))
