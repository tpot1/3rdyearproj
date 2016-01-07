import os

import webapp2

from google.appengine.ext import ndb

def user_key(user_name="Test"):
	return ndb.Key('User', user_name)

class Badge(ndb.Model):
	iconName=ndb.StringProperty()

class Challenge(ndb.Model):
	challengeid=ndb.IntegerProperty()
	title=ndb.StringProperty()
	description=ndb.StringProperty()
	complete=ndb.BooleanProperty()
	badge=ndb.StructuredProperty(Badge)
	expiresat = ndb.FloatProperty()

class Lecture(ndb.Model):
	module=ndb.StringProperty()
	location=ndb.IntegerProperty()
	day=ndb.StringProperty()
	time=ndb.IntegerProperty()
	attended=ndb.BooleanProperty()	# can add these two attributes after the lecture
	week=ndb.IntegerProperty()

class Module(ndb.Model):
	code=ndb.StringProperty()
	lectures=ndb.StructuredProperty(Lecture, repeated=True)

class Building(ndb.Model):
	number=ndb.StringProperty()
	coordinates=ndb.GeoPtProperty(repeated=True)

class User(ndb.Model):
	userid=ndb.StringProperty()
	email=ndb.StringProperty()
	challenges=ndb.StructuredProperty(Challenge, repeated=True)
	lectures=ndb.StructuredProperty(Lecture, repeated=True)
	score=ndb.IntegerProperty()
	streak=ndb.IntegerProperty()
	count=ndb.IntegerProperty()
	badges=ndb.StructuredProperty(Badge, repeated=True)
	history=ndb.StructuredProperty(Lecture, repeated=True)

class CheckIn(ndb.Model):
	student=ndb.StructuredProperty(User)
	lecture=ndb.StructuredProperty(Lecture)
	date = ndb.DateProperty(auto_now_add=True)
	time = ndb.TimeProperty(auto_now_add=True)


class ThisUser():
	username = ""

