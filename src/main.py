#!/bin/env python
import webapp2
import os
import jinja2
from google.appengine.ext import ndb

jinja_current_directory = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_current_directory), extensions=['jinja2.ext.autoescape'], autoescape=True)

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        search_template = jinja_env.get_template("templates/searchresults.html")
        self.response.out.write(search_template.render())

class LocationHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        location_template = jinja_env.get_template("templates/location.html")
        self.response.out.write(location_template.render())

class ReviewHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        feedback_template = jinja_env.get_template("templates/feedback.html")
        self.response.out.write(feedback_template.render())

class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        about_template = jinja_env.get_template("templates/aboutus.html")
        self.response.out.write(about_template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        index_template = jinja_env.get_template("templates/index.html")
        self.response.out.write(index_template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/location', LocationHandler),
    ('/reviews', ReviewHandler),
    ('/aboutus', AboutUsHandler),
    ], debug=False)
