import os

import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

def user_key(user_name="Test"):
	return ndb.Key('User', user_name)

class Badge(ndb.Model):
	name=ndb.StringProperty()
	#icon=?

class Day(ndb.Model):
	day=ndb.StringProperty()
	#day = Monday or Tuesday or Wednesday --- look for how to do this

class Challenge(ndb.Model):
	challengeid=ndb.IntegerProperty()
	complete=ndb.BooleanProperty()
	badge=ndb.StructuredProperty(Badge)
	#predicate=ndb.functionproperty()??

class Lecture(ndb.Model):
	module=ndb.StringProperty()
	location=ndb.StringProperty()
	day=ndb.StructuredProperty(Day)
	time=ndb.IntegerProperty()
	attended=ndb.StringProperty()	# can add these two attributes after the lecture
	week=ndb.IntegerProperty()

class User(ndb.Model):
	userid=ndb.StringProperty()
	email=ndb.StringProperty()
	challenges=ndb.StructuredProperty(Challenge, repeated=True)
	lectures=ndb.StructuredProperty(Lecture, repeated=True)
	score=ndb.IntegerProperty()
	streak=ndb.IntegerProperty()
	badges=ndb.StructuredProperty(Badge, repeated=True)

class CheckIn(ndb.Model):
	##adding this temprarily
	lat=ndb.FloatProperty();
	lon=ndb.FloatProperty();
	student=ndb.StringProperty()
	lecture=ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)


class ThisUser():
	username = ""

