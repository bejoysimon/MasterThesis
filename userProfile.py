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

class UserProfile(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        username = self.request.get('username')
        error = ''
        result = ''

        unique_key = ndb.Key('UserModel', username)
        unique_user = unique_key.get()

        template_values = {'unique_user' : unique_user,
                            'error' : error,
                            'result' : result}

        template = JINJA_ENVIRONMENT.get_template('userProfile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        unique_key = ndb.Key('UserModel', myuser.username)
        unique_user = unique_key.get()

        error1 = ''
        error2 = ''
        result = ''

        action = self.request.get('button')

        if action == "Logout":
            self.redirect("/")


        template_values = {'unique_user' : unique_user,
                            'searched_tweets' : searched_tweets,
                            'error2' : error2}

        template = JINJA_ENVIRONMENT.get_template('userProfile.html')
        self.response.write(template.render(template_values))
