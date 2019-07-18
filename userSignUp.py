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

class UserSignUp(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        actual_username = myuser.username

        template_values = {'actual_username' : actual_username}

        template = JINJA_ENVIRONMENT.get_template('userSignUp.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action=self.request.get('button')

        if action == "Home":
            self.redirect('/')

        if action == 'Submit':
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            username = self.request.get('username')
            actual_username = myuser.username

            if username != actual_username:
                self.response.write('Incorrect Username!')

            else:
                self.redirect('/userProfile?username='+username)

        if action == 'Create':
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            username = self.request.get('username')
            name = self.request.get('name')
            actual_username = myuser.username

            query_username = MyUser.query(MyUser.username == username)

            unique_key = ndb.Key('UserModel', username)
            unique_user = unique_key.get()

            if query_username.count() == 0:
                if myuser.username == None:
                    myuser.username = username
                    myuser.put()

                    unique_user = UserModel(id = username,
                                            email = user.email(),
                                            username = username,
                                            name = name,)
                    unique_user.put()

                    self.redirect('/userProfile?username='+username)
            else:
                self.response.write('Username Exists. Please choose another!')


        template_values = {
            'username' : username,
            'actual_username' : actual_username
        }

        template = JINJA_ENVIRONMENT.get_template('userSignUp.html')
        self.response.write(template.render(template_values))
