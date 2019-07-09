from google.appengine.ext import ndb

class TweetsModel(ndb.Model):
    username = ndb.StringProperty()
    tweet = ndb.StringProperty()
    tweet_words = ndb.StringProperty(repeated = True)
    posted_time = ndb.DateTimeProperty(auto_now = True)
    posted_image = ndb.BlobKeyProperty()
