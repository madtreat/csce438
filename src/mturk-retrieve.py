# This script handles retrieving completed MTurk HITs/Tasks
# and adding them to the Crowdstorming SQLite Database
#
# Created by Madison Treat, Kodi Tapie and Blake Robertson
#
#
# DO NOT call this script except for developmental purposes.
# It should ONLY be called from mturk-manage.py
#

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
database = sqlite3.connect('crowdstorming.db', isolation_level='DEFERRED')
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
#print("HIT IDs:")
#print(hit_ids)
print("")

for hit in hit_ids:
   hit_id = hit[0]
   tasks = mt.get_assignments(hit_id)

   print ("-----------------------------------------------------------")
   print ("HIT: " + hit_id)
   print ("   Num_Complete: " + str(len(tasks)))

   # Update the "hits" table with the number of completed tasks for this HIT
   hitsUpdate =   "UPDATE hits SET Num_Complete=? WHERE Hit_ID=?"
   db.execute(hitsUpdate, [len(tasks), hit_id])
   #print("   Total number of rows changed: " + str(database.total_changes))

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

   database.commit()

# Save changes
database.commit()
database.close()

