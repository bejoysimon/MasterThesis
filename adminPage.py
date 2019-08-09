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

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        admin_key = ndb.Key('UserModel', myuser.username)
        admin_user = admin_key.get()

        # squad_key = ndb.Key('MySquad', myuser.username)
        # squad = squad_key.get()
        squad = MySquad.query()

        template_values = {'admin_user' : admin_user, 'squad' : squad}

        template = JINJA_ENVIRONMENT.get_template('adminPage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action=self.request.get('button')

        if action == "Home":
            self.redirect('/')

        if action == "Add":
            market_id = int(self.request.get("market_id"))
            market_name = self.request.get("market_name")

            add_market = BettingMarkets(id = myuser.username + market_id,
                                        market_id = market_id,
                                        market_name = market_name)
            add_market.put()

            self.redirect('/adminPage')
