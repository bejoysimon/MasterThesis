import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from userModel import UserModel
from mySquad import MySquad
from bettingMarkets import BettingMarkets


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AdminPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        logout = users.create_logout_url('/')

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        unique_key = ndb.Key('UserModel', myuser.username)
        unique_user = unique_key.get()

        total_users = UserModel.query(UserModel.username != 'admin')

        squad = MySquad.query()

        template_values = {'total_users' : total_users, 'squad' : squad, 'logout' : logout}

        template = JINJA_ENVIRONMENT.get_template('adminPage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action=self.request.get('button')

        if action == "Add":
            market_id = int(self.request.get("market_id"))
            market_name = self.request.get("market_name")

            add_market = BettingMarkets(id = myuser.username + market_id,
                                        market_id = market_id,
                                        market_name = market_name)
            add_market.put()

            self.redirect('/adminPage')
