import praw
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

def insert_row(data):
  entry = ss_client.InsertRow(data, spreadsheet_key, worksheet_id)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print "Insert row succeeded."
  else:
    print "Insert row failed."

for submission in submissions:
  data = {}
  data['title'] = submission.title
  data['content'] = submission.selftext
  insert_row(data)
