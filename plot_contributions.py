import math
import getopt
import sys
from datetime import datetime
from imgurpython import ImgurClient

CLIENT_ID = '9d9878ff940099e'
CLIENT_SECRET = '0f9969a855e56960a988aee44a1ffe6d513e02db'
CLIENT = ImgurClient(CLIENT_ID, CLIENT_SECRET)

def mean(numbers, precision=2):
  """return mean of a list, a basic function that is bafflingly absent"""
  return round(float(sum(numbers)) / max(len(numbers), 1), precision)

def get_comment_info(comment_id):
  """print voting info ona single comment"""
  comment = CLIENT.get_comment(comment_id)
  print "comment: %d\nup: %d\ndown: %d" % (comment_id, comment.ups, comment.downs)

def get_user_commenting_info(username):
  """print info about a user's commenting history"""
  comments_per_page = 50
  comment_count = CLIENT.get_account_comment_count(username)
  pages = int(math.floor(comment_count / comments_per_page))

  scores = []
  days = []

  for page in range(0,pages):
    comments = CLIENT.get_account_comments(username, 'newest', page)
    scores.extend(map(lambda x: x.points, comments))
    days.extend(map(lambda x: datetime.fromtimestamp(int(x.datetime)), comments))

  date_format = '%Y-%m-%d'

  print "count: ", len(scores)
  print "min: ", min(scores)
  print "max: ", max(scores)
  print "mean: ", mean(scores)
  print "earliest: ", days[-1].strftime(date_format)
  print "last: ", days[0].strftime(date_format)

def usage():
  """print usage information and exit"""
  print "%s [-u | -user <username>] [-c | -comment <comment_id>]" % sys.argv[0]

def main():
  # we have two main arguments: username, or comment_id
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'su:c:', ['user=', 'username=', 'comment='])
  except getopt.GetoptError:
    usage()

  if not opts:
    usage()

  for opt, arg, in opts:
    if opt in ['-u', '--user', '--username']:
      get_user_commenting_info(arg)
    elif opt in ['-c', '--comment']:
      get_comment_info(int(arg))

if __name__ == '__main__':
  main()
