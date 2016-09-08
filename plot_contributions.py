import math
import getopt
import sys
from datetime import datetime, timedelta
from collections import Counter

from imgurpython import ImgurClient
from bokeh.plotting import figure, show


# the local config file needs to set two variables, CLIENT_ID, and
# CLIENT_SECRET, both of which can be obtained by registering your application
# at https://api.imgur.com/oauth2/addclient
import config
CLIENT = ImgurClient(config.CLIENT_ID, config.CLIENT_SECRET)


def mean(numbers, precision=2):
  """return mean of a list, a basic function that is bafflingly absent"""
  return round(float(sum(numbers)) / max(len(numbers), 1), precision)


def beginning_of_week(date):
  """round a datetime down to the begining of the week (a monday)"""
  return date + timedelta(days = date.weekday())


def beginning_of_month(date):
  """round a datetime down to the begining of the month"""
  return date + timedelta(days = 1 - int(date.strftime('%d')))


def truncate_time(date):
  """remove the time part of a datetime stamp"""
  return date - timedelta(hours = int(date.strftime("%H")), minutes = int(date.strftime("%M")), seconds = int(date.strftime("%S")), microseconds = int(date.strftime("%f")))


def get_comment_info(comment_id):
  """print voting info on a single comment"""
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


def weekly_plot_of_user(username):
  """get weekly data about a user's commenting history"""
  # get all comments
  # sort them into monthly buckets
  # produce two plots:
  # 1) # of comments by month
  # 2) total score by month
  comments_per_page = 50
  comment_count = CLIENT.get_account_comment_count(username)
  pages = int(math.floor(comment_count / comments_per_page))

  comments_by_month = Counter()
  points_by_month = Counter()

  for page in range(0,pages):
    comments = CLIENT.get_account_comments(username, 'newest', page)
    for comment in comments:
      comment_date = datetime.fromtimestamp(int(comment.datetime))
      month = truncate_time(beginning_of_month(comment_date))
      comments_by_month[month] += 1
      points_by_month[month] += comment.points

  # plot the data
  month = points_by_month.keys()
  month.sort()
  x = month
  y = [points_by_month[month] for month in month]

  p = figure(title='test plot', x_axis_type='datetime', x_axis_label='Month', y_axis_label='Score')
  p.line(x, y, legend='Points per Month', line_width=4)

  return p


def usage():
  """print usage information and exit"""
  print "%s [-u | -user <username>] [-c | -comment <comment_id>]" % sys.argv[0]
  sys.exit(2)


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
      #get_user_commenting_info(arg)
      p = weekly_plot_of_user(arg)
      show(p)
    elif opt in ['-c', '--comment']:
      get_comment_info(int(arg))

if __name__ == '__main__':
  main()
