from google.appengine.ext import ndb

class UserModel(ndb.Model):
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    balance = ndb.FloatProperty(default=100.00)
