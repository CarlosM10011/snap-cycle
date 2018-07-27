#!/bin/env python
import webapp2
import os
import jinja2
from models import Person, Review, ndb, Address, Item, City, Bin

def getAddressObjectList():
    # Do query.
    objects = Address.query().fetch()
    return objects

def renderAllAddresses():
    # query first:
    list = getAddressObjectList()
    returnList = []
    for i in list:
        returnList.append({"name": i.address1 + " " + i.city + ", " + i.state + ", " + str(i.zip), "id": i.key})
    return returnList

# class UserSearch(ndb.Model):
#     term = ndb.StringProperty(required=False)

    # def increment(self):
    #     self.count += 1
    #     return self.count
# user = UserSearch()

def getAddressObject(address_1, address_2, city, state, zip):
    queryObj1 = None
    obj = None
    queryObj1 = Address.query(Address.state == state)
    if queryObj1.get():
        queryObj2 = queryObj1.filter(Address.city == city)
        queryObj3 = queryObj2.filter(Address.city == city)
        queryObj4 = queryObj3.filter(Address.zip == int(zip))
        queryObj5 = queryObj4.filter(Address.zip == int(zip))
        obj = queryObj5.filter(Address.address1 == address_1).get()
    return obj

def getPersonObjectByName(first_name, last_name):
    queryObj = Person.query(Person.lastName == last_name)
    obj = queryObj.filter(Person.firstName == first_name).get()
    obj = Person.query(Person.firstName == first_name, Person.lastName == last_name).get()
    return obj

def getCityObjectByName(name):
    obj = City.query(City.name == name).get()
    return obj

@ndb.transactional
def getBinObjectByName(parent_key, name):
    obj = City.query(City.name == name, ancestor=parent_key).get()
    return obj

@ndb.transactional
def putBinObject(obj):
    return obj.put()

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
    # First: get a list of all reviews:
    reviews = listAllReviews()
    # Okay we have a list; now let's calculate the total number.
    totalReviews = len(reviews)
    # Okay Now let's calculate how many reviews individually:
    oneStar = 0
    twoStar = 0
    threeStar = 0
    fourStar = 0
    fiveStar = 0
    for i in reviews:
        if i["rating"] == 1: oneStar = oneStar + 1
        elif i["rating"] == 2: twoStar = twoStar + 1
        elif i["rating"] == 3: threeStar = threeStar + 1
        elif i["rating"] == 4: fourStar = fourStar + 1
        elif i["rating"]== 5: fiveStar = fiveStar + 1
    # Great! we now should have the individual reviews.
    # Now let's see if we can calculate the mean reviews:
    if totalReviews!=0: # divide by 0
        meanReviews = ((1*oneStar)+(2*twoStar)+(3*threeStar)+(4*fourStar)+(5*fiveStar))/float(totalReviews)
    else:
        meanReviews = 0.0
    # Great! Now let's add these values to a dictionary:
    returnDict = {
        "reviews": reviews,
        "oneStar": oneStar,
        "twoStar": twoStar,
        "threeStar": threeStar,
        "fourStar": fourStar,
        "fiveStar": fiveStar,
        "mean": meanReviews,
        "totalReviews": totalReviews}
    return returnDict

def listAllReviews():
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
        print("Welcome")
        # self.response.headers['Content-Type'] = 'text/html'
        search_template = jinja_env.get_template("templates/index.html")
        # a = jinja_env.get_template("templates/reviews.html")
        self.response.out.write(search_template.render())

    def post(self):
        print("HEY")
        self.response.headers['Content-Type'] = 'text/html'
        search_template = jinja_env.get_template("templates/searchresults.html")
        search_term = self.request.get('search')

        search_term = search_term.lower()
        search = search_term.split(" ")
        word = ''

        for i in search:
            word += i

        print(word)

        ret = {
            "search": search_term.upper(),
        }

        def get_compost_words():
            with open('compost.txt') as f:
                content = ' '.join(f.readlines()).replace('\n','').replace('\r','').lower()
                return content.split(' ')

        def get_recycling_words():
            with open('recycling.txt') as f:
                content = ' '.join(f.readlines()).replace('\n','').replace('\r','').lower()
                return content.split(' ')

        def get_ewaste_words():
            with open('e_waste.txt') as f:
                content = ' '.join(f.readlines()).replace('\n','').replace('\r','').lower()
                return content.split(' ')

        compost = get_compost_words()
        recycling = get_recycling_words()
        ewaste = get_ewaste_words()

        # for i in compost:
        #     i.lower()
        # for i in recycling:
        #     i.lower()
        # for i in ewaste:
        #     i.lower()

        print(word)
        if word in recycling:
            ret['pic'] = "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=f7e0a66cba220611e4b926593b3b795f&auto=format&fit=crop&w=800&q=60"
            ret['word'] = "Recycling: "
            ret['word2'] = "The item you have entered is Recyclable. By correctly disposing of the product, you are making a difference in our ecosystem. Recycling is the first step towards a better world. To locate local Recycling sites, please enter your zip code below."
        elif word in compost:
            ret['pic'] = "https://images.unsplash.com/photo-1503596476-1c12a8ba09a9?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=2d74cf1088e47e1007c800942ec97a31&auto=format&fit=crop&w=800&q=60"
            ret['word'] = "Compost: "
            ret['word2'] = "The item you have entered is Compostable. This means that if you are growing your own garden you can dispose of it by leaving it slightly buried with your plants. Even if you lack a garden you could leave it on your yard and the grass will be able to absorb nutrients from it. If your would like to locate local Compost sites, please go to our 'Location' page and enter your zip code."
        elif word in ewaste:
            ret['pic'] = "https://images.unsplash.com/photo-1526406915894-7bcd65f60845?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=9028dd6de93ea441c4fa84efb852bcf9&auto=format&fit=crop&w=800&q=60"
            ret['word'] = "E-Waste: "
            ret['word2'] = "The item you have entered is a Recyclable Electronic. Dispose of this head to your local electronic recycling facility and they will be able to reuse your item. Do not throw this item in the trash since this could be bad for waste disposal system. To locate local E Waste sites, please go to our 'Location' page and enter your zip code."
        else:
            ret['pic'] = "https://images.unsplash.com/photo-1493852303730-955ff798ba12?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=d0a3aa0e3ad08c0fb0691593c7c74b71&auto=format&fit=crop&w=800&q=60"
            ret['word'] = "Error:"
            ret['word2'] = "The item you have entered could not be found in our database. Please ensure that you have not misspelled the item. Contact us at safecycle1@gmail.com and we will include this item in our database. "

        self.response.out.write(search_template.render(ret))

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

class AddBinHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        bin_add_template = jinja_env.get_template("templates/addbin.html")
        self.response.out.write(bin_add_template.render())
    def post(self):
        city = None
        if self.request.get("city").lower()!="":
            if not getCityObjectByName(self.request.get("city").lower()):
                city = City()
                city.name = self.request.get("city").lower()
                city.put()
            else:
                city = getCityObjectByName(self.request.get("city").lower())
            bin = None
            if not getBinObjectByName(city.key, self.request.get("bin_name").lower()):
                bin = Bin(parent=city.key)
                bin.name = self.request.get("bin_name").lower()
                bin.image = self.request.get("image").lower()
                bin.sortingInstructions = self.request.get("sorting_instructions")
                putBinObject(bin)
        else:
            pass
        bin_add_template = jinja_env.get_template("templates/addbin.html")
        self.response.out.write(bin_add_template.render())

class ReviewHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        review_template = jinja_env.get_template("templates/reviews.html")
        self.response.out.write(review_template.render(renderAllReviews()))
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
        self.response.out.write(review_template.render(renderAllReviews()))

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
    ('/bins/add', AddBinHandler),
    ('/reviews', ReviewHandler),
    ('/aboutus', AboutUsHandler),
    ], debug=False)
