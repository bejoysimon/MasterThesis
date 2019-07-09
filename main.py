import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from userModel import UserModel
from tweetsModel import TweetsModel
from userSignUp import UserSignUp
from userProfile import UserProfile
from editProfile import EditProfile
from searchedProfile import SearchedProfile
from editTweet import EditTweet 


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back'

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id(), email = user.email())
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/userSignUp', UserSignUp),
                                ('/userProfile', UserProfile),
                                ('/editProfile', EditProfile),
                                ('/searchedProfile', SearchedProfile),
                                ('/editTweet', EditTweet),], debug=True)
