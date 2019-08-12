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

class UpdateMarkets(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        username = self.request.get('username')

        unique_user_key = ndb.Key('UserModel', username)
        unique_user = unique_user_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        market = BettingMarkets.query(BettingMarkets.username == username).order(BettingMarkets.market_name)

        template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market}

        template = JINJA_ENVIRONMENT.get_template('updateMarkets.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action=self.request.get('button')

        username = self.request.get('username')
        squad_name = self.request.get('squad_name')
        updated_name = self.request.get('updated_name')
        updated_so_far = int(self.request.get('updated_so_far'))
        updated_sell_price = float(self.request.get('updated_sell_price'))
        updated_buy_price = float(self.request.get('updated_buy_price'))

        unique_user_key = ndb.Key('UserModel', username)
        unique_user = unique_user_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        user_market_key = username + updated_name
        market_key = ndb.Key('BettingMarkets', user_market_key)
        market = market_key.get()

        if action == "Home":
            self.redirect('/')

        if action == "Update":
            user_market_key = username + updated_name
            market_key = ndb.Key('BettingMarkets', user_market_key)
            market = market_key.get()

            market.market_so_far = updated_so_far
            market.market_sell_price = updated_sell_price
            market.market_buy_price = updated_buy_price
            market.put()

            self.redirect('/updateMarkets?username='+username)
