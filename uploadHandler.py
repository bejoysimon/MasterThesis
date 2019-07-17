import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import os
import csv

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
        # with open(filename, 'rb') as csv_file:
        #     fileReader = csv.reader(csv_file, delimiter=',')
            row_count = 0
            for row in fileReader:
                row = row.rstrip()
                if row_count == 0:
                    row_count += 1
                else:
                    player_name = row[0]
                    playerData_key = ndb.Key('PlayersData', player_name)
                    playerData = playerData_key.get()

                    if playerData == None:
                        playerData = PlayersData(name = row[0],
                                                team = row[1],
                                                position = row[2],
                                                cost = row[3],
                                                creativity = row[4],
                                                influence = row[5],
                                                threat = row[6],
                                                ict = row[7],
                                                goals_conceded = row[8],
                                                goals_scored = row[9],
                                                assists = row[10],
                                                own_goals = row[11],
                                                penalties_missed = row[12],
                                                penalties_saved = row[13],
                                                saves = row[14],
                                                yellow_cards = row[15],
                                                red_cards = row[16],
                                                tsb = row[17],
                                                minutes = row[18],
                                                bonus = row[19],
                                                points = row[20],)
                        playerData.put()
                        row_count += 1

        self.redirect('/addPlayersData')


        # if filename:
        #     fileReader = blobstore.BlobReader(blobinfo.key())
        #     for line in fileReader:
        #
        #         line = line.rstrip()
        #
        #         user_word_key = user.user_id() + ordered_word
        #         word_key = ndb.Key('WordStore', user_word_key)
        #         word = word_key.get()
        #
        #         if word==None:
        #             for i in range(3, len(line)+1):
        #                 for c in combinations(ordered_word, i):
        #                     u_word_key = str(user.user_id()) + ''.join(c)
        #                     w_key = ndb.Key('WordStore', u_word_key)
        #                     w = w_key.get()
        #                     if w == None:
        #                         w = WordStore(id=u_word_key, letter_count=len(line))
        #                         w.put()
        #             word = word_key.get()
        #
        #         if line not in word.words:
        #             if len(word.words) == 0:
        #                 myuser.anagram_count = myuser.anagram_count + 1
        #             word.words.append(line)
        #             myuser.word_count = myuser.word_count + 1
        #             myuser.put()
        #             word.put()
        #
        # self.redirect('/')
