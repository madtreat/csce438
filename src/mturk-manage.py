# TODO: wipe/clear the table before running this manager each time
# OR:   make a different db file for each particular instance/idea web generated
# TODO: make the SQLite calls secure versions, not just string concatenations

import datetime, sys, sqlite3, time
from subprocess import call
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection

# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " seed_phrase")

if len(sys.argv) != 2:
   print_usage()
   exit()


# Process command line args
SEED = sys.argv[1]


# Connect to the sqlite results database
database = sqlite3.connect('crowdstorming.db')
db       = database.cursor()

# Ensure "jobs" table exists
seedTable = "CREATE TABLE IF NOT EXISTS jobs ("\
   "Job_ID INTEGER PRIMARY KEY AUTOINCREMENT, "\
   "Seed_Phrase TEXT NOT NULL, "\
   "Created DATE DEFAULT CURRENT_DATE"\
   ")"
db.execute(seedTable)

# Ensure "hits" table exists
hitsTable = "CREATE TABLE IF NOT EXISTS hits ("\
   "Job_ID INTEGER NOT NULL, "\
   "Hit_ID TEXT NOT NULL, "\
   "Parent_Hit_ID TEXT, "\
   "Iter INTEGER NOT NULL, "\
   "Num_Complete INTEGER DEFAULT 0, "\
   "Phrase TEXT NOT NULL, "\
   "PRIMARY KEY(Job_ID, Hit_ID)"\
   ")"
db.execute(hitsTable)


# Add this phrase into the "jobs" table in the database
seedRow = 'INSERT INTO jobs(Seed_Phrase) VALUES (?)'
#seedArg = ','.join('?')
db.execute(seedRow, [SEED])

# Get the next (unique) Phrase ID
seedID = db.lastrowid

# Create table of results for this particular inquiry phrase
seedResults = "CREATE TABLE IF NOT EXISTS results ("\
   "Job_ID   INTEGER NOT NULL,"\
   "Hit_ID   TEXT NOT NULL, "\
   "Task_ID  TEXT NOT NULL, "\
   "Response TEXT, "\
   "PRIMARY KEY(Job_ID, Task_ID)"\
   ")"
db.execute(seedResults)#, [seedID])

# Save changes
database.commit()


# Spawn Initial HIT
call (["python", "mturk-create.py", SEED, str(seedID), "0"])

# Retrieve Results
#cmd = "SELECT * FROM hits;"
#hit_id = db.execute(cmd)
#for hit_id, phrase, num_complete in db.execute(cmd):
#   print ("manager hit: ")
#   print (str(hit_id))
#   time.sleep(1*30)

   # Retrieve initial HIT results
# TODO: change hit_id to job_id
#   call (["python", "mturk-retrieve.py", hit_id])

# Clean up and close the database
database.close()
