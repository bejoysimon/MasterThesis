import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import os

from myuser import MyUser
from playersData import PlayersData


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if filename:
            fileReader = blobstore.BlobReader(blobinfo.key())
            row_count = 0
            for row in fileReader:
                row = row.rstrip()
                row = row.split(',')
                if row_count == 0:
                    row_count += 1
                else:
                    player_name = row[0]
                    playerData_key = ndb.Key('PlayersData', player_name)
                    playerData = playerData_key.get()

                    if playerData == None:
                        playerData = PlayersData(id = row[0],
                                                name = row[0],
                                                team = row[1],
                                                position = row[2],
                                                cost = int(row[3]),
                                                creativity = float(row[4]),
                                                influence = float(row[5]),
                                                threat = float(row[6]),
                                                ict = float(row[7]),
                                                goals_conceded = int(row[8]),
                                                goals_scored = int(row[9]),
                                                assists = int(row[10]),
                                                own_goals = int(row[11]),
                                                penalties_missed = int(row[12]),
                                                penalties_saved = int(row[13]),
                                                saves = int(row[14]),
                                                yellow_cards = int(row[15]),
                                                red_cards = int(row[16]),
                                                tsb = float(row[17]),
                                                minutes = int(row[18]),
                                                bonus = int(row[19]),
                                                points = int(row[20]),)
                        playerData.put()
                        row_count += 1

        self.redirect('/adminPage')
