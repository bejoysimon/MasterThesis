from google.appengine.ext import ndb

class UserModel(ndb.Model):
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    bio = ndb.StringProperty()

    # tweets_list = ndb.StringProperty(repeated=True) 
    followers = ndb.StringProperty(repeated=True)
    followings = ndb.StringProperty(repeated=True)

    follower_count = ndb.IntegerProperty(default=0)
    following_count = ndb.IntegerProperty(default=0)

    # tweets_list = ndb.StructuredProperty(TweetsModel, repeated=True)
