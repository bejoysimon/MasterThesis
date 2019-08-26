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

class UpdateMarkets(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        logout = users.create_logout_url('/')

        username = self.request.get('username')

        unique_user_key = ndb.Key('UserModel', username)
        unique_user = unique_user_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        market = BettingMarkets.query(BettingMarkets.username == username).order(BettingMarkets.market_name)

        bet = MyBets.query(MyBets.username == username).order(-MyBets.bet_time)

        template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market, 'bet' : bet, 'logout' : logout}

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
        market_settlement = self.request.get('market_settlement')

        unique_user_key = ndb.Key('UserModel', username)
        unique_user = unique_user_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        user_market_key = username + updated_name
        market_key = ndb.Key('BettingMarkets', user_market_key)
        market = market_key.get()

        if action == "Update":
            user_market_key = username + updated_name
            market_key = ndb.Key('BettingMarkets', user_market_key)
            market = market_key.get()

            bet = MyBets.query(MyBets.username == username and MyBets.bet_market == updated_name)

            if len(market_settlement) != 0:
                if bet.count()>0:
                    for i in bet:
                        i.bet_settlement = int(market_settlement)
                        i.put()

                        if i.bet_action == "BUY":
                            excess_margin = (i.bet_price - i.bet_at_so_far) * i.bet_stake
                            amount = (i.bet_settlement - i.bet_price) * i.bet_stake
                            unique_user.balance = (unique_user.balance + amount) + excess_margin
                            unique_user.put()

                        if i.bet_action == "SELL":
                            amount = (i.bet_price - i.bet_settlement) * i.bet_stake
                            unique_user.balance = unique_user.balance + amount
                            unique_user.put()


            if updated_so_far != 0:
                if bet.count()>0:
                    for i in bet:
                        if i.bet_action == "BUY":
                            bet_margin = (updated_so_far - market.market_so_far) * i.bet_stake
                            unique_user.balance = unique_user.balance + bet_margin
                            unique_user.put()

                        if i.bet_action == "SELL":
                            bet_margin = (updated_so_far - market.market_so_far) * i.bet_stake
                            unique_user.balance = unique_user.balance - bet_margin
                            unique_user.put()


            market.market_so_far = updated_so_far
            market.market_sell_price = updated_sell_price
            market.market_buy_price = updated_buy_price
            if len(market_settlement) != 0:
                market.market_settlement = int(market_settlement)
            market.put()


            self.redirect('/updateMarkets?username='+username)
