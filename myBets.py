from google.appengine.ext import ndb

from myuser import MyUser
from userModel import UserModel

class MyBets(ndb.Model):
    username = ndb.StringProperty()
    squad_name = ndb.StringProperty()
    balance = ndb.FloatProperty()
    bet_market = ndb.StringProperty()
    bet_action = ndb.StringProperty()
    bet_price = ndb.FloatProperty()
