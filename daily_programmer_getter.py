import praw
import re
import os
import string
import markdown

r = praw.Reddit(user_agent='my_cool_application')
submissions = r.get_subreddit('dailyprogrammer').get_new(limit=None)

def get_title_data(title):
  title_data = {}

  # Get Date
  date_match = re.match(r"\[\d+/\d+/\d+\]", title)
  if date_match:
    title_data['date'] = date_match.group(0)[1:-1]
    title = title[len(title_data['date']) + 3:]

  # Get Challenge number
  challenge_match = re.match(r"\bchallenge\b #\d+", title, re.IGNORECASE)
  if not challenge_match:
    return False

  title_data['challenge'] = challenge_match.group(0)
  title = title[len(title_data['challenge']) + 1:]

  # Get Difficulty
  difficulty_match = re.match(r"\[(easy|intermediate|hard|difficult)\]", title, re.IGNORECASE)
  if difficulty_match:
    title_data['difficulty'] = difficulty_match.group(0)[1:-1]
  else:
    title_data['difficulty'] = "N/A"
  title = title[len(title_data['difficulty']) + 2:]

  # Get Challenge Title
  title_data['title'] = title.strip()

  return title_data


main_dir = "C:\Users\Luke\Desktop\DailyProgrammer"
fdirs = [main_dir,
        os.path.join(main_dir, 'Easy'),
        os.path.join(main_dir, 'Intermediate'),
        os.path.join(main_dir, 'Difficult'),
        os.path.join(main_dir, 'Other')]
for fdir in fdirs:
  if not os.path.exists(fdir):
    os.makedirs(fdir)

for submission in submissions:
  data = {}
  title = submission.title
  
  title_data = get_title_data(title)
  if not title_data:
    continue

  for key, value in title_data.iteritems():
    data[key] = value

  if data['title'] == '':
    data['title'] = data['challenge']
  fname = re.sub('[\\/:*?"<>|]', '-', data['title']) + '.html'
  fdir = main_dir
  if data['difficulty'] == 'Easy':
    fdir = os.path.join(main_dir, 'Easy')
  elif data['difficulty'] == 'Intermediate':
    fdir = os.path.join(main_dir, 'Intermediate')
  elif data['difficulty'] == 'Difficult' or data['difficulty'] == 'Hard':
    fdir = os.path.join(main_dir, 'Difficult')
  else:
    fdir = os.path.join(main_dir, 'Other')

  f = open(os.path.join(fdir, fname), 'w')
  f.write(markdown.markdown(submission.selftext).encode("UTF-8"))
  f.close()

# \/:*?"<>|