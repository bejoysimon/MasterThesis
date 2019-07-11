from google.appengine.ext import ndb

class UserModel(ndb.Model):
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    bio = ndb.StringProperty()

    # tweets_list = ndb.StructuredProperty(TweetsModel, repeated=True)
