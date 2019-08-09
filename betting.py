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

        username = self.request.get('username')

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        market_key = ndb.Key('BettingMarkets', username)
        market = market_key.get()

        bet_key = ndb.Key('MyBets', username)
        bet = bet_key.get()

        template_values = {'unique_user' : unique_user, 'squad' : squad, 'market' : market, 'bet' : bet}

        template = JINJA_ENVIRONMENT.get_template('betting.html')
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

        bet_key = ndb.Key('MyBets', myuser.username)
        bet = bet_key.get()

        # total_goals_sell = self.request.get('total_goals_sell')
        # total_goals_buy = self.request.get('total_goals_buy')
        # total_bookings_sell = self.request.get('total_bookings_sell')
        # total_bookings_buy = self.request.get('total_bookings_buy')
        # captain_points_sell = self.request.get('captain_points_sell')
        # captain_points_buy = self.request.get('captain_points_buy')
        # goal_minutes_sell = self.request.get('goal_minutes_sell')
        # goal_minutes_buy = self.request.get('goal_minutes_buy')
        # squad_points_sell = self.request.get('squad_points_sell')
        # squad_points_buy = self.request.get('squad_points_buy')


        action = self.request.get('button')

        if action == "Logout":
            self.redirect('/')

        # if action == "SELL":
        #     add_bet = MyBets(username = myuser.username,
        #                     squad_name = squad.sqaud_name,
        #                     bet_id =
        #                     bet_market =
        #                     bet_action = action,
        #                     bet_sell_price =
        #                     bet_buy_price = )
        #     add_bet.put()
        #
        #     self.redirect('/betting?username='+myuser.username)


        template_values = {'unique_user' : unique_user}

        template = JINJA_ENVIRONMENT.get_template('betting.html')
        self.response.write(template.render(template_values))
