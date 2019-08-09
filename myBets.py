from google.appengine.ext import ndb

from myuser import MyUser
from userModel import UserModel

class MyBets(ndb.Model):
    username = ndb.StringProperty()
    squad_name = ndb.StringProperty()
    bet_id = ndb.IntegerProperty()
    bet_market = ndb.StringProperty()
    bet_action = ndb.StringProperty()
    bet_sell_price = ndb.FloatProperty()
    bet_buy_price = ndb.FloatProperty()
