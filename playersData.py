from google.appengine.ext import ndb

class PlayersData(ndb.Model):
    name = ndb.StringProperty()
    team = ndb.StringProperty()
    position = ndb.StringProperty()
    cost = ndb.IntegerProperty(default=0)
    creativity = ndb.FloatProperty(default=0.00)
    influence = ndb.FloatProperty(default=0.00)
    threat = ndb.FloatProperty(default=0.00)
    ict = ndb.FloatProperty(default=0.00)
    goals_conceded = ndb.IntegerProperty(default=0)
    goals_scored = ndb.IntegerProperty(default=0)
    assists = ndb.IntegerProperty(default=0)
    own_goals = ndb.IntegerProperty(default=0)
    penalties_missed = ndb.IntegerProperty(default=0)
    penalties_saved = ndb.IntegerProperty(default=0)
    saves = ndb.IntegerProperty(default=0)
    yellow_cards = ndb.IntegerProperty(default=0)
    red_cards = ndb.IntegerProperty(default=0)
    tsb = ndb.FloatProperty(default=0.00)
    minutes = ndb.IntegerProperty(default=0)
    bonus = ndb.IntegerProperty(default=0)
    points = ndb.IntegerProperty(default=0)

    # tweets_list = ndb.StructuredProperty(TweetsModel, repeated=True)