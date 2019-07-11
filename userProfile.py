import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from userModel import UserModel
from tweetsModel import TweetsModel


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

        timeline = TweetsModel.query().filter(TweetsModel.username.IN(unique_user.followings)).order(-TweetsModel.posted_time).fetch(limit = 50)

        template_values = {'unique_user' : unique_user,
                            'timeline' : timeline,
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

        timeline = TweetsModel.query().filter(TweetsModel.username.IN(unique_user.followings)).order(-TweetsModel.posted_time).fetch(limit = 50)

        error1 = ''
        error2 = ''
        result = ''

        action = self.request.get('button')

        if action == "Logout":
            self.redirect("/")

        if action == "Post":
            new_tweet = self.request.get('new_tweet')
            tweet_words_list = new_tweet.split(" ")

            # unique_user.tweets_list.append(new_tweet)
            # unique_user.put()

            adding_tweet = TweetsModel(id = new_tweet,
                                        username = myuser.username,
                                        tweet = new_tweet,
                                        tweet_words = tweet_words_list)
            adding_tweet.put()

            self.redirect('/userProfile?username='+myuser.username)

        if action == "Edit Profile":
            self.redirect("/editProfile?username="+myuser.username)

        if action == "Search":
            searched_username = self.request.get('searched_username')

            if searched_username != myuser.username:
                query = MyUser.query(MyUser.username == searched_username)

                if query.count() == 0:
                    error1 = "No such username exists!"
                    result = ""

                else:
                    for i in query:
                        result = i.username

            template_values = {'unique_user' : unique_user,
                                'timeline' : timeline,
                                'error1' : error1,
                                'result' : result}

            template = JINJA_ENVIRONMENT.get_template('userProfile.html')
            self.response.write(template.render(template_values))

        if action == "LookUp":
            searched_content = self.request.get('searched_content')
            terms = searched_content.split(" ")
            query = TweetsModel.query()

            for t in terms:
                query = query.filter(TweetsModel.tweet_words == t)

            searched_tweets = query.fetch()

            if query.count() == 0:
                error2 = "No tweets for the given search content!"


            template_values = {'unique_user' : unique_user,
                                'timeline' : timeline,
                                'searched_tweets' : searched_tweets,
                                'error2' : error2}

            template = JINJA_ENVIRONMENT.get_template('userProfile.html')
            self.response.write(template.render(template_values))
