from google.appengine.ext import ndb

from myuser import MyUser
from userModel import UserModel

class BettingMarkets(ndb.Model):
    username = ndb.StringProperty()
    squad_name = ndb.StringProperty()
    market_id = ndb.IntegerProperty()
    market_name = ndb.StringProperty()
    market_so_far = ndb.IntegerProperty()
    market_sell_price = ndb.FloatProperty()
    market_buy_price = ndb.FloatProperty()
