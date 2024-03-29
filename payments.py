import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from userModel import UserModel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Payments(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        logout = users.create_logout_url('/')

        username = self.request.get('username')

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        template_values = {'unique_user' : unique_user, 'logout' : logout}

        template = JINJA_ENVIRONMENT.get_template('payments.html')
        self.response.write(template.render(template_values))

    # def post(self):
    #     self.response.headers['Content-Type'] = 'text/html'
    #
    #     user = users.get_current_user()
    #     myuser_key = ndb.Key('MyUser', user.user_id())
    #     myuser = myuser_key.get()
    #
    #     unique_key = ndb.Key('UserModel', myuser.username)
    #     unique_user = unique_key.get()
    #
    #     action = self.request.get('button')
