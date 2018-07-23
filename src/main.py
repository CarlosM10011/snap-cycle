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
        search_template = jinja_env.get_template("templates/search.html")
        self.response.out.write(search_template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        index_template = jinja_env.get_template("templates/index.html")
        self.response.out.write(index_template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ], debug=False)
