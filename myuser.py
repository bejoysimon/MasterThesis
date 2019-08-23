from google.appengine.ext import ndb

class MyUser(ndb.Model):
    email = ndb.StringProperty()
    username = ndb.StringProperty()
