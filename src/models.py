#!/bin/env python

from google.appengine.ext import ndb

class Person(ndb.Model):
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()

class Review(ndb.Model):
    date = ndb.DateTimeProperty(auto_now=True)
    rating = ndb.IntegerProperty()
    visitFrequency = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.StringProperty()
