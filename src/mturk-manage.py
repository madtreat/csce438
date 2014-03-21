# TODO: wipe/clear the table before running this manager each time
# OR:   make a different db file for each particular instance/idea web generated
# TODO: make the SQLite calls secure versions, not just string concatenations

import datetime, sys, sqlite3, time
from subprocess import call
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection

# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " phrase")

if len(sys.argv) != 2:
   print_usage()
   exit()


# Process command line args
PHRASE   = sys.argv[1]


# Connect to the sqlite results database
database = sqlite3.connect('results.db')
db       = database.cursor()


# BOTO Configuration
#config = Config()
#AWS_ID = config.get('Credentials', 'aws_access_key_id', None)
#SECRET_ID = config.get('Credentials', 'aws_secret_access_key_id', None)
#HOST = 'mechanicalturk.sandbox.amazonaws.com'
#
#mt = MTurkConnection(
#   aws_access_key_id=AWS_ID, 
#   aws_secret_access_key=SECRET_ID, 
#   host=HOST
#   )


# Spawn Initial HIT
call (["python", "mturk-create.py", PHRASE, "0"])
cmd = "SELECT * FROM hits;"
#hit_id = db.execute(cmd)
for hit_id, phrase, num_complete in db.execute(cmd):
   print ("manager hit: ")
   print (str(hit_id))
   time.sleep(1*30)

   # Retrieve initial HIT results
   call (["python", "mturk-retrieve.py", hit_id])


