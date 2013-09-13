import praw
import re
import gdata.spreadsheet.service

r = praw.Reddit(user_agent='my_cool_application')
submissions = r.get_subreddit('dailyprogrammer').get_new(limit=None)

config = {}
execfile('settings.conf', config)

email = config['google_account']
password = config['google_password']

spreadsheet_key = config['spreadsheet_key']
worksheet_id = config['worksheet_id']

ss_client = gdata.spreadsheet.service.SpreadsheetsService()
ss_client.email = email
ss_client.password = password
ss_client.source = 'Daily Programmer to Spreadsheet'
ss_client.ProgrammaticLogin()

def get_title_data(full_title):
  title_data = {}

  # Get Date
  date_match = re.match(r"\[\d+/\d+/\d+\]", full_title)
  if not date_match:
    return False

  title_data['date'] = date_match.group(0)[1:-1]
  trunc_title = full_title[len(title_data['date']) + 3:]

  # Get Challenge number
  challenge_match = re.match(r"\bchallenge\b #\d+", trunc_title, re.IGNORECASE)
  if not challenge_match:
    return False

  title_data['challenge'] = challenge_match.group(0)
  trunc_title = trunc_title[len(title_data['challenge']) + 1:]

  print trunc_title

  difficulty_match = re.match(r"\[\w+\]", trunc_title)
  if difficulty_match:
    title_data['difficulty'] = difficulty_match.group(0)[1:-1]
  else:
    title_data['difficulty'] = "N/A"
  trunc_title = trunc_title[len(title_data['difficulty']) + 3:]

  title_data['title'] = trunc_title

  return title_data

def insert_row(data):
  entry = ss_client.InsertRow(data, spreadsheet_key, worksheet_id)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print "Insert row succeeded."
  else:
    print "Insert row failed."

for submission in submissions:
  data = {}
  full_title = submission.title

  title_data = get_title_data(full_title)

  if not title_data:
    continue

  data['challenge'] = title_data['challenge']
  data['date'] = title_data['date']
  data['title'] = title_data['title']
  data['difficulty'] = title_data['difficulty']
  data['content'] = submission.selftext
  insert_row(data)
