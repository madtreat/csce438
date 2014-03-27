import datetime, sys, sqlite3
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection

# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " job_id")

if len(sys.argv) != 2:
   print_usage()
   exit()


# Process command line args
JOB_ID   = sys.argv[1]


# Connect to the sqlite results database
database = sqlite3.connect('crowdstorming.db')
db       = database.cursor()

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


# Retrieve results from MTurk for the given job
jobHits = "SELECT (Hit_ID) FROM hits WHERE Job_ID = ?"
db.execute(jobHits, [JOB_ID])

hit_ids = db.fetchall()
print("Fetching results for Job ID " + JOB_ID)
print("HIT IDs:")
print(hit_ids)
print("\n")

for hit in hit_ids:
   hit_id = hit[0]
   print("HIT: " + hit_id)
   tasks = mt.get_assignments(hit_id)

   for task in tasks:
      task_id = task.AssignmentId
      print ("   Task ID = " + task_id)
      print ("      Worker ID = " + task.WorkerId)
      for question_form_answer in task.answers[0]:
         for response in question_form_answer.fields:
            print ("      Phrase    = " + response)
            # Add the results into the database
            db_entry = "INSERT OR REPLACE INTO results VALUES (?, ?, ?, ?)"

            #print (db_entry)
            db.execute(db_entry, (JOB_ID, hit_id, task_id, response))
   print ("-------------")

# Save changes
database.commit()
database.close()

