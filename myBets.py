from google.appengine.ext import ndb

from myuser import MyUser
from userModel import UserModel

class MyBets(ndb.Model):
    username = ndb.StringProperty()
    squad_name = ndb.StringProperty()
    bet_market = ndb.StringProperty()
    bet_at_so_far = ndb.IntegerProperty()
    bet_action = ndb.StringProperty()
    bet_price = ndb.FloatProperty()
    bet_stake = ndb.FloatProperty()
    bet_margin = ndb.FloatProperty()
    bet_time = ndb.DateTimeProperty(auto_now = True)
    bet_settlement = ndb.IntegerProperty()
