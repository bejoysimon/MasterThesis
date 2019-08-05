import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from userModel import UserModel
from playersData import PlayersData
from mySquad import MySquad


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class BuildSquad(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        username = self.request.get('username')

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        squad_key = ndb.Key('MySquad', username)
        squad = squad_key.get()

        query_gkp = PlayersData.query(PlayersData.position == 'GKP')
        query_def = PlayersData.query(PlayersData.position == 'DEF')
        query_mid = PlayersData.query(PlayersData.position == 'MID')
        query_fwd = PlayersData.query(PlayersData.position == 'FWD')

        template_values = {'unique_user' : unique_user,
                            'squad' : squad,
                            'gkp' : query_gkp,
                            'def' : query_def,
                            'mid' : query_mid,
                            'fwd' : query_fwd}

        template = JINJA_ENVIRONMENT.get_template('buildSquad.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        unique_key = ndb.Key('UserModel', myuser.username)
        unique_user = unique_key.get()

        action = self.request.get('button')

        if action == "Logout":
            self.redirect('/')

        if action == "Submit":
            squad_name = self.request.get('squad_name')
            gkp1 = self.request.get('gkp1')
            gkp2 = self.request.get('gkp2')
            def1 = self.request.get('def1')
            def2 = self.request.get('def2')
            def3 = self.request.get('def3')
            def4 = self.request.get('def4')
            def5 = self.request.get('def5')
            mid1 = self.request.get('mid1')
            mid2 = self.request.get('mid2')
            mid3 = self.request.get('mid3')
            mid4 = self.request.get('mid4')
            mid5 = self.request.get('mid5')
            fwd1 = self.request.get('fwd1')
            fwd2 = self.request.get('fwd2')
            fwd3 = self.request.get('fwd3')

            squad_update = MySquad(id = myuser.username,
                                    username = myuser.username,
                                    squad_name = squad_name,
                                    squad_cost = 0,
                                    gkp1 = gkp1,
                                    gkp2 = gkp2,
                                    def1 = def1,
                                    def2 = def2,
                                    def3 = def3,
                                    def4 = def4,
                                    def5 = def5,
                                    mid1 = mid1,
                                    mid2 = mid2,
                                    mid3 = mid3,
                                    mid4 = mid4,
                                    mid5 = mid5,
                                    fwd1 = fwd1,
                                    fwd2 = fwd2,
                                    fwd3 = fwd3)
            squad_update.put()

            self.redirect('/userProfile?username='+myuser.username)


        template_values = {'unique_user' : unique_user}

        template = JINJA_ENVIRONMENT.get_template('buildSquad.html')
        self.response.write(template.render(template_values))
