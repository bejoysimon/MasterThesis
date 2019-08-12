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

class AddMarkets(webapp2.RequestHandler):
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

        template = JINJA_ENVIRONMENT.get_template('addMarkets.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action=self.request.get('button')

        username = self.request.get('username')
        squad_name = self.request.get('squad_name')
        market_name = self.request.get('market_name')
        market_so_far = int(self.request.get('market_so_far'))
        market_sell_price = float(self.request.get('market_sell_price'))
        market_buy_price = float(self.request.get('market_buy_price'))

        unique_user_key = ndb.Key('UserModel', username)
        unique_user = unique_user_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        user_market_key = username + market_name
        market_key = ndb.Key('BettingMarkets', user_market_key)
        market = market_key.get()

        if action == "Home":
            self.redirect('/')

        if action == "Add":
            if market == None:
                add_market = BettingMarkets(id = user_market_key,
                                            username = username,
                                            squad_name = squad_name,
                                            market_name = market_name,
                                            market_so_far = market_so_far,
                                            market_sell_price = market_sell_price,
                                            market_buy_price = market_buy_price)
                add_market.put()

                self.redirect('/addMarkets?username='+username)
            else:
                self.response.write("***Market already exists!***")

                market = BettingMarkets.query(BettingMarkets.username == username).order(BettingMarkets.market_name)

                template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market}

                template = JINJA_ENVIRONMENT.get_template('addMarkets.html')
                self.response.write(template.render(template_values))
