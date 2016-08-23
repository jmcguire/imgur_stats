import sys
import math
from datetime import datetime
from imgurpython import ImgurClient

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

client_id = '9d9878ff940099e'
client_secret = '0f9969a855e56960a988aee44a1ffe6d513e02db'

client = ImgurClient(client_id, client_secret)
username = 'lifefeed'

comments_per_page = 50
comment_count = client.get_account_comment_count(username)
pages = int(math.floor(comment_count / comments_per_page))

scores = []
days = []

#comment = client.get_comment(XXX)
#print "up: %d\ndown: %d" % (comment.ups, comment.downs)
#sys.exit()

for page in range(0,pages):
    comments = client.get_account_comments(username, 'newest', page)
    for comment in comments:
        date_string = datetime.fromtimestamp(int(comment.datetime)).strftime('%Y-%m-%d')
        #print "%s score: %d" % (date_string, comment.points)
        scores.append(comment.points)
        days.append(date_string)
    page += 1

print min(scores)
print max(scores)
print mean(scores)
#print mode(scores)

