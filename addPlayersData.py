import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from blobCollection import BlobCollection
from uploadHandler import UploadHandler
from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class AddPlayersData(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        collection_key = ndb.Key('BlobCollection', 1)
        collection = collection_key.get()

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if collection == None:
            collection = BlobCollection(id=1)
            collection.put()

        template_values = {'collection' : collection,
                            'upload_url' : blobstore.create_upload_url('/upload')}

        template = JINJA_ENVIRONMENT.get_template('addPlayersData.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action=self.request.get('button')

        if action == "Go HOME":
            self.redirect('/')


# app = webapp2.WSGIApplication([('/upload', UploadHandler)])
