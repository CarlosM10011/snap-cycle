#!/bin/env python
import webapp2
import os
import jinja2
from models import Person, Review, ndb, Address

def getAddressObject(address_1, address_2, city, state, zip):
    queryObj1 = None
    obj = None
    queryObj1 = Address.query(Address.state == state)
    if queryObj1.get():
        queryObj2 = queryObj1.filter(Address.city == city)
        queryObj3 = queryObj2.filter(Address.city == city)
        queryObj4 = queryObj3.filter(Address.zip == int(zip))
        queryObj5 = queryObj4.filter(Address.zip == zip)
        obj = queryObj5.filter(Address.address1 == address_1).get()
    return obj

def getPersonObjectByName(first_name, last_name):
    queryObj = Person.query(Person.lastName == last_name)
    obj = queryObj.filter(Person.firstName == first_name).get()
    obj = Person.query(Person.firstName == first_name, Person.lastName == last_name).get()
    return obj

def getPersonObjectByEmail(email_address):
    obj = Person.query(Person.email == email_address).get()
    return obj

def getPersonObjectByEmail(email_address):
    obj = Person.query(Person.email == email_address).get()
    return obj

@ndb.transactional
def getReviewEntryCount(parent_key):
    count = WordEntry.query(ancestor=parent_key).count()
    return count

@ndb.transactional
def getReviewObject(parent_key):
    obj = Review.query(ancestor=parent_key).get()
    return obj

@ndb.transactional
def putReviewObject(obj):
    return obj.put()

@ndb.transactional
def putWordEntryObject(obj):
    return obj.put()

def getPersonObjectList():
    return Person.query().fetch()

def renderAllReviews():
    # this will return a list with all the reviews for jinja to render.
    finalArray = []
    # first thing's first: we need a list of people:
    peopleObjects = getPersonObjectList()
    # Now we need to load the info from each person:
    for i in peopleObjects:
        reviewObject = getReviewObject(i.key)
        # Initialize and append a dictionary for each person:
        finalArray.append({"email": i.email,
                           "first_name": i.firstName.capitalize(),
                           "last_name": i.lastName.capitalize(),
                           "subject": reviewObject.subject,
                           "date": reviewObject.date,
                           "rating": reviewObject.rating,
                           "message": reviewObject.message,
                           })
    return finalArray

jinja_current_directory = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_current_directory), extensions=['jinja2.ext.autoescape'], autoescape=True)

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/html'
        search_template = jinja_env.get_template("templates/index.html")
        self.response.out.write(search_template.render())
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        search_template = jinja_env.get_template("templates/searchresults.html")
        search = self.request.get('search')
        user_input = {
            'search': search.upper(),
        }
        self.response.out.write(search_template.render(user_input))

class LocationHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        location_template = jinja_env.get_template("templates/location.html")
        self.response.out.write(location_template.render())
        
class AddLocationHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        location_add_template = jinja_env.get_template("templates/addlocation.html")
        self.response.out.write(location_add_template.render())
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        address = None
        if not getAddressObject(self.request.get("address1").lower(), self.request.get("address2").lower(), self.request.get("city").lower(), self.request.get("state").lower(), self.request.get("zip")):
            address = Address()
            address.address1 = self.request.get("address1").lower()
            address.address2 = self.request.get("address2").lower()
            address.city = self.request.get("city").lower()
            address.state = self.request.get("state").lower()
            if self.request.get("zip")!="": address.zip = int(self.request.get("zip"))
            address.put()
        else:
            pass
        location_add_template = jinja_env.get_template("templates/addlocation.html")
        self.response.out.write(location_add_template.render())

class ReviewHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        review_template = jinja_env.get_template("templates/reviews.html")
        self.response.out.write(review_template.render(reviews=renderAllReviews()))
    def post(self):
        person = None
        if self.request.get("email").lower()!="":
            if not getPersonObjectByEmail(self.request.get("email").lower()):
                person = Person()
                person.firstName = self.request.get("first_name").lower()
                person.lastName = self.request.get("last_name").lower()
                person.email = self.request.get("email").lower()
                person.put()
            else:
                person = getPersonObjectByEmail(self.request.get("email").lower())
            review = None
            if not getReviewObject(person.key): # person hasn't submitted a review.
                review = Review(parent=person.key)
                review.rating = int(self.request.get("rating").lower())
                review.subject = "no subject"
                review.message = self.request.get("message_body")
                review.visitFrequency = self.request.get("visit_frequency")
                putReviewObject(review)
        else:
            pass
        review_template = jinja_env.get_template("templates/reviews.html")
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(review_template.render(reviews=renderAllReviews()))

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
    ('/searchresult', SearchHandler),
    ('/location', LocationHandler),
    ('/location/add', AddLocationHandler),
    #('/items/add', AddItemHandler),
    #('/bins/add', AddBinHandler),
    ('/reviews', ReviewHandler),
    ('/aboutus', AboutUsHandler),
    ], debug=False)
