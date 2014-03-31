# This script must be called first to begin a job for our "Crowd-Storming" Application
#
# Created by Madison Treat, Kodi Tapie and Blake Robertson
#
#
# The idea is that this script will be used to create the intial seed phrase
# of the job. This script will create a new entry in the jobs table
# and send off the initial HIT and the user will be given their Job ID.
# The user can then call mturk-manage.py with their Job_ID
#

import datetime, sys, sqlite3, time
from subprocess import call
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection

# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " num_iterations num_branches seed_phrase")

if len(sys.argv) < 4:
   print_usage()
   exit()


# Process command line args
NUM_ITER = sys.argv[1]
NUM_BRANCHES = sys.argv[2]
SEED = sys.argv[3]

# Connect to the sqlite results database
database = sqlite3.connect('crowdstorming.db')
db       = database.cursor()

# Ensure "jobs" table exists
seedTable = "CREATE TABLE IF NOT EXISTS jobs ("\
   "Job_ID INTEGER PRIMARY KEY AUTOINCREMENT, "\
   "Seed_Phrase TEXT NOT NULL, "\
   "Num_Iter INTEGER NOT NULL, "\
   "Num_Branches INTEGER NOT NULL, "\
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
   "Has_Children INTEGER NOT NULL, "\
   "PRIMARY KEY(Job_ID, Hit_ID)"\
   ")"
db.execute(hitsTable)


# Add this phrase and restrictions into the "jobs" table in the database
seedRow = 'INSERT INTO jobs(Seed_Phrase, Num_Iter, Num_Branches) VALUES (?, ?, ?)'
db.execute(seedRow, [SEED, NUM_ITER, NUM_BRANCHES])

# Get the next (unique) Phrase ID
seedID = db.lastrowid

# Create table of results
seedResults = "CREATE TABLE IF NOT EXISTS results ("\
   "Job_ID   INTEGER NOT NULL,"\
   "Hit_ID   TEXT NOT NULL, "\
   "Task_ID  TEXT NOT NULL, "\
   "Response TEXT, "\
   "PRIMARY KEY(Job_ID, Task_ID)"\
   ")"
db.execute(seedResults)


# Create table of unique phrases per job
unique = "CREATE TABLE IF NOT EXISTS unique_phrases ("\
   "Job_ID  INTEGER NOT NULL,"\
   "Phrase  TEXT NOT NULL"\
   ")"

db.execute(unique)

# Save changes
database.commit()

# Spawn Initial HIT
call (["python", "mturk-create.py", SEED, str(seedID), "0", "NULL", str(NUM_BRANCHES)])

# Get user's Job ID and display it to them
db.execute("select Job_ID from jobs")
jobIDs = db.fetchall()
thisJobID = jobIDs[len(jobIDs)-1][0]
print 'Your Job ID is {}'.format(thisJobID)
print 'You can now call mturk-manage.py {} to get completed HITs and updated Graph'.format(thisJobID)

# Clean up and close the database
database.close()

