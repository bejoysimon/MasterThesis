from google.appengine.ext import ndb

class UserModel(ndb.Model):
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    balance = ndb.FloatProperty(default=0.00)

    # tweets_list = ndb.StructuredProperty(TweetsModel, repeated=True)
