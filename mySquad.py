from google.appengine.ext import ndb

from myuser import MyUser
from userModel import UserModel

class MySquad(ndb.Model):
    username = ndb.StringProperty()
    squad_name = ndb.StringProperty()
    squad_cost = ndb.IntegerProperty(default = 0)
    gkp1 = ndb.StringProperty()
    gkp2 = ndb.StringProperty()
    def1 = ndb.StringProperty()
    def2 = ndb.StringProperty()
    def3 = ndb.StringProperty()
    def4 = ndb.StringProperty()
    def5 = ndb.StringProperty()
    mid1 = ndb.StringProperty()
    mid2 = ndb.StringProperty()
    mid3 = ndb.StringProperty()
    mid4 = ndb.StringProperty()
    mid5 = ndb.StringProperty()
    fwd1 = ndb.StringProperty()
    fwd2 = ndb.StringProperty()
    fwd3 = ndb.StringProperty()
    captain = ndb.StringProperty()
    vice_captain = ndb.StringProperty()
    # queriedGPUs = ndb.StructuredProperty(GPUInfo, repeated=True)
