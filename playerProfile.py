import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from userModel import UserModel
from playersData import PlayersData


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class PlayerProfile(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        username = self.request.get('username')

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        player_name = self.request.get('name')
        playerData_key = ndb.Key('PlayersData', player_name)
        playerData = playerData_key.get()

        img = "sample_player_pic.png"

        template_values = {'unique_user' : unique_user, 'player' : playerData, 'img' : img}

        template = JINJA_ENVIRONMENT.get_template('playerProfile.html')
        self.response.write(template.render(template_values))
