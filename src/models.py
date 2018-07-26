#!/bin/env python

from google.appengine.ext import ndb

class Person(ndb.Model):
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()

class Review(ndb.Model):
    date = ndb.DateProperty(auto_now=True)
    rating = ndb.IntegerProperty()
    visitFrequency = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.TextProperty()

class Item(ndb.Model):
    name = ndb.StringProperty()
    image = ndb.StringProperty()
    locations = ndb.JsonProperty()
    bins = ndb.JsonProperty()

class Address(ndb.Model):
    address1 = ndb.StringProperty()
    address2 = ndb.StringProperty()
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    zip = ndb.IntegerProperty()

class City(ndb.Model):
    name = ndb.StringProperty()

class Bin(ndb.Model):
    name = ndb.StringProperty()
    color = ndb.StringProperty()
    sortingInstructions = ndb.StringProperty()
    