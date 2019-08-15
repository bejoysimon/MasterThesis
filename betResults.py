import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from userModel import UserModel
from mySquad import MySquad
from bettingMarkets import BettingMarkets
from myBets import MyBets


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class BetResults(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        username = self.request.get('username')

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        market = BettingMarkets.query(BettingMarkets.username == username).order(BettingMarkets.market_name)

        bet = MyBets.query(MyBets.username == username).order(-MyBets.bet_time)

        template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market,  'bet' : bet}

        template = JINJA_ENVIRONMENT.get_template('betResults.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        unique_key = ndb.Key('UserModel', myuser.username)
        unique_user = unique_key.get()

        squad_key = ndb.Key('MySquad', myuser.username)
        squad = squad_key.get()

        action = self.request.get('button')

        if action == "Logout":
            self.redirect('/')
