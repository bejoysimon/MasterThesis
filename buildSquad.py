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

        img = '/static/blank_player_pic.png'

        query_all = PlayersData.query()
        query_gkp = PlayersData.query(PlayersData.position == 'GKP')
        query_def = PlayersData.query(PlayersData.position == 'DEF')
        query_mid = PlayersData.query(PlayersData.position == 'MID')
        query_fwd = PlayersData.query(PlayersData.position == 'FWD')

        template_values = {'unique_user' : unique_user,
                            'img' : img,
                            'squad' : squad,
                            'all' : query_all,
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

        squad_key = ndb.Key('MySquad', myuser.username)
        squad = squad_key.get()

        error1 = '***Invalid Squad! Squad cost over available budget!***'
        error2 = '***Invalid Squad! Same player chosen for different positions!***'

        action = self.request.get('button')

        if action == "Logout":
            self.redirect('/')

        if action == "Submit":
            squad_name = self.request.get('squad_name')

            gkp1 = self.request.get('gkp1')
            player_key = ndb.Key('PlayersData', gkp1)
            player = player_key.get()
            cost_gkp1 = player.cost

            gkp2 = self.request.get('gkp2')
            player_key = ndb.Key('PlayersData', gkp2)
            player = player_key.get()
            cost_gkp2 = player.cost

            def1 = self.request.get('def1')
            player_key = ndb.Key('PlayersData', def1)
            player = player_key.get()
            cost_def1 = player.cost

            def2 = self.request.get('def2')
            player_key = ndb.Key('PlayersData', def2)
            player = player_key.get()
            cost_def2 = player.cost

            def3 = self.request.get('def3')
            player_key = ndb.Key('PlayersData', def3)
            player = player_key.get()
            cost_def3 = player.cost

            def4 = self.request.get('def4')
            player_key = ndb.Key('PlayersData', def4)
            player = player_key.get()
            cost_def4 = player.cost

            def5 = self.request.get('def5')
            player_key = ndb.Key('PlayersData', def5)
            player = player_key.get()
            cost_def5 = player.cost

            mid1 = self.request.get('mid1')
            player_key = ndb.Key('PlayersData', mid1)
            player = player_key.get()
            cost_mid1 = player.cost

            mid2 = self.request.get('mid2')
            player_key = ndb.Key('PlayersData', mid2)
            player = player_key.get()
            cost_mid2 = player.cost

            mid3 = self.request.get('mid3')
            player_key = ndb.Key('PlayersData', mid3)
            player = player_key.get()
            cost_mid3 = player.cost

            mid4 = self.request.get('mid4')
            player_key = ndb.Key('PlayersData', mid4)
            player = player_key.get()
            cost_mid4 = player.cost

            mid5 = self.request.get('mid5')
            player_key = ndb.Key('PlayersData', mid5)
            player = player_key.get()
            cost_mid5 = player.cost

            fwd1 = self.request.get('fwd1')
            player_key = ndb.Key('PlayersData', fwd1)
            player = player_key.get()
            cost_fwd1 = player.cost

            fwd2 = self.request.get('fwd2')
            player_key = ndb.Key('PlayersData', fwd2)
            player = player_key.get()
            cost_fwd2 = player.cost

            fwd3 = self.request.get('fwd3')
            player_key = ndb.Key('PlayersData', fwd3)
            player = player_key.get()
            cost_fwd3 = player.cost

            captain = self.request.get('captain')
            vice_captain = self.request.get('vice_captain')

            total_cost = cost_gkp1 + cost_gkp2 + cost_def1 + cost_def2 + cost_def3 + cost_def4 + cost_def5 + cost_mid1 + cost_mid2 + cost_mid3 + cost_mid4 + cost_mid5 + cost_fwd1 + cost_fwd2 + cost_fwd3

            if (gkp1 != gkp2 and
                def1 != def2 and def1 != def3 and def1 != def4 and def1 != def5 and def2 != def3 and def2 != def4 and def2 != def5 and def3 != def4 and def3 != def5 and def4 != def5 and
                mid1 != mid2 and mid1 != mid3 and mid1 != mid4 and mid1 != mid5 and mid2 != mid3 and mid2 != mid4 and mid2 != mid5 and mid3 != mid4 and mid3 != mid5 and mid4 != mid5 and
                fwd1 != fwd2 and fwd2 != fwd3 and fwd1 != fwd3):
                if total_cost <= 1000:
                    squad_update = MySquad(id = myuser.username,
                                            username = myuser.username,
                                            squad_name = squad_name,
                                            squad_cost = total_cost,
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
                                            fwd3 = fwd3,
                                            captain = captain,
                                            vice_captain = vice_captain)
                    squad_update.put()

                    self.redirect('/userProfile?username='+myuser.username)
                else:
                    self.response.write(error1)

                    img = '/static/blank_player_pic.png'

                    query_gkp = PlayersData.query(PlayersData.position == 'GKP')
                    query_def = PlayersData.query(PlayersData.position == 'DEF')
                    query_mid = PlayersData.query(PlayersData.position == 'MID')
                    query_fwd = PlayersData.query(PlayersData.position == 'FWD')

                    template_values = {'unique_user' : unique_user,
                                        'img' : img,
                                        'squad' : squad,
                                        'gkp' : query_gkp,
                                        'def' : query_def,
                                        'mid' : query_mid,
                                        'fwd' : query_fwd}

                    template = JINJA_ENVIRONMENT.get_template('buildSquad.html')
                    self.response.write(template.render(template_values))
            else:
                self.response.write(error2)

                img = '/static/blank_player_pic.png'

                query_gkp = PlayersData.query(PlayersData.position == 'GKP')
                query_def = PlayersData.query(PlayersData.position == 'DEF')
                query_mid = PlayersData.query(PlayersData.position == 'MID')
                query_fwd = PlayersData.query(PlayersData.position == 'FWD')

                template_values = {'unique_user' : unique_user,
                                    'img' : img,
                                    'squad' : squad,
                                    'gkp' : query_gkp,
                                    'def' : query_def,
                                    'mid' : query_mid,
                                    'fwd' : query_fwd}

                template = JINJA_ENVIRONMENT.get_template('buildSquad.html')
                self.response.write(template.render(template_values))
