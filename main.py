import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import csv

from myuser import MyUser
from mySquad import MySquad
from userModel import UserModel
from userSignUp import UserSignUp
from userProfile import UserProfile
from payments import Payments
from scoring import Scoring
from rules import Rules
from playerStats import PlayerStats
from playerProfile import PlayerProfile
from buildSquad import BuildSquad
from betting import Betting
from bettingMarkets import BettingMarkets
from myBets import MyBets
from adminPage import AdminPage
from addPlayersData import AddPlayersData
from blobCollection import BlobCollection
from uploadHandler import UploadHandler


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back'

        user = users.get_current_user()
        admin = False

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if users.is_current_user_admin():
                welcome = 'Welcome'

                myuser = MyUser(id=user.user_id(), email = user.email(), username = 'admin')
                myuser.put()

                admin_key = ndb.Key('UserModel', myuser.username)
                admin_user = admin_key.get()

                admin_user = UserModel(id = myuser.username,
                                        email = user.email(),
                                        username = myuser.username,
                                        name = 'Administrator')
                admin_user.put()
                admin = True

            if myuser == None:
                welcome = 'Welcome'
                myuser = MyUser(id=user.user_id(), email = user.email())
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'admin' : admin,
            'welcome' : welcome,
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/userSignUp', UserSignUp),
                                ('/userProfile', UserProfile),
                                ('/payments', Payments),
                                ('/scoring', Scoring),
                                ('/rules', Rules),
                                ('/playerStats', PlayerStats),
                                ('/playerProfile', PlayerProfile),
                                ('/adminPage', AdminPage),
                                ('/addPlayersData', AddPlayersData),
                                ('/buildSquad', BuildSquad),
                                ('/betting', Betting),
                                ('/upload', UploadHandler)], debug=True)
