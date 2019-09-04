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

class Betting(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        logout = users.create_logout_url('/')

        username = self.request.get('username')

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        market = BettingMarkets.query(BettingMarkets.username == username).order(BettingMarkets.market_name)

        bet = MyBets.query(MyBets.username == username).order(-MyBets.bet_time)

        template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market, 'bet' : bet, 'logout' : logout}

        template = JINJA_ENVIRONMENT.get_template('betting.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        logout = users.create_logout_url('/')

        username = self.request.get('username')

        # user = users.get_current_user()
        # myuser_key = ndb.Key('MyUser', user.user_id())
        # myuser = myuser_key.get()

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        action = self.request.get('button')

        if action == "BUY":
            market_name = self.request.get('market_name')
            market_so_far = int(self.request.get('market_so_far'))
            bet_stake = float(self.request.get('bet_stake'))
            market_buy_price = float(self.request.get('market_buy_price'))
            balance = unique_user.balance
            margin_balance = unique_user.margin

            bet_margin = (market_buy_price - market_so_far) * bet_stake

            if bet_margin < margin_balance:
                margin_balance = unique_user.margin - bet_margin
                unique_user.margin = margin_balance
                unique_user.put()

                add_bet = MyBets(username = username,
                                squad_name = squad.squad_name,
                                bet_market = market_name,
                                bet_at_so_far = market_so_far,
                                bet_action = action,
                                bet_price = market_buy_price,
                                bet_stake = bet_stake,
                                bet_margin = bet_margin)
                add_bet.put()

                self.redirect('/betting?username='+username)
            else:
                self.response.write("***Insufficient Margin Balance!***")

                market = BettingMarkets.query(BettingMarkets.username == username).order(BettingMarkets.market_name)

                bet = MyBets.query(MyBets.username == username).order(-MyBets.bet_time)

                template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market, 'bet' : bet, 'logout' : logout}

                template = JINJA_ENVIRONMENT.get_template('betting.html')
                self.response.write(template.render(template_values))

        if action == "SELL":
            market_name = self.request.get('market_name')
            market_so_far = int(self.request.get('market_so_far'))
            bet_stake = float(self.request.get('bet_stake'))
            market_sell_price = float(self.request.get('market_sell_price'))
            balance = unique_user.balance
            margin_balance = unique_user.margin

            bet_margin = ((2 * market_sell_price) - market_so_far) * bet_stake

            if bet_margin < margin_balance:
                margin_balance = unique_user.margin - bet_margin
                unique_user.margin = margin_balance
                unique_user.put()

                add_bet = MyBets(username = username,
                                squad_name = squad.squad_name,
                                bet_market = market_name,
                                bet_at_so_far = market_so_far,
                                bet_action = action,
                                bet_price = market_sell_price,
                                bet_stake = bet_stake,
                                bet_margin = bet_margin)
                add_bet.put()

                self.redirect('/betting?username='+username)
            else:
                self.response.write("***Insufficient Margin Balance!***")

                market = BettingMarkets.query(BettingMarkets.username == username).order(BettingMarkets.market_name)

                bet = MyBets.query(MyBets.username == username).order(-MyBets.bet_time)

                template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market, 'bet' : bet, 'logout' : logout}

                template = JINJA_ENVIRONMENT.get_template('betting.html')
                self.response.write(template.render(template_values))
