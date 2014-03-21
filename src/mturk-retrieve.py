import datetime, sys, sqlite3
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection

# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " hit_id")

if len(sys.argv) != 2:
   print_usage()
   exit()


# Process command line args
HIT_ID   = sys.argv[1]


# Connect to the sqlite results database
database = sqlite3.connect('results.db')
db       = database.cursor()

db_entry = "CREATE TABLE IF NOT EXISTS \'" + HIT_ID + "\' (task_id, phrase)"
db.execute(db_entry)


# BOTO Configuration
config = Config()
AWS_ID = config.get('Credentials', 'aws_access_key_id', None)
SECRET_ID = config.get('Credentials', 'aws_secret_access_key_id', None)
HOST = 'mechanicalturk.sandbox.amazonaws.com'

mt = MTurkConnection(
   aws_access_key_id=AWS_ID, 
   aws_secret_access_key=SECRET_ID, 
   host=HOST
   )


# Retrieve results from MTurk
tasks = mt.get_assignments(HIT_ID)

print(tasks)
for task in tasks:
   task_id = task.AssignmentId
   print ("Task ID = " + task_id)
   print ("Task Worker ID = " + task.WorkerId)
   for question_form_answer in task.answers[0]:
      for phrase in question_form_answer.fields:
         print ("Phrase = " + phrase)
         # Add the results into the database
         db_entry = "INSERT OR REPLACE INTO \'" + HIT_ID + "\' VALUES (\'" + task_id + "\',\'" + phrase + "\')"
         #print (db_entry)
         db.execute(db_entry)
      print ("-------------")

# Save changes
database.commit()
database.close()

