# This file is the main script for our "Crowd-Storming" Application
#
# Created by Madison Treat, Kodi Tapie and Blake Robertson
#
#
# The idea is that this script will be used to manage the lifecycle
# of a job.  In particular, the different functions that will be 
# performed by this script (using the other scripts) are:
#  - retrieve and aggregate all results
#  - display results if all HITs and MTurk Tasks are complete
#
# The other scripts should not be called directly except for 
# developmental purposes, as they are all managed by THIS script.
#
#

import datetime, sys, sqlite3, time
from subprocess import call
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection

# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " job_id")

if len(sys.argv) != 2:
   print_usage()
   exit()


# Process command line args
JOB_ID = sys.argv[1]

# fetch results from amazon
call (["python", "mturk-retrieve.py", JOB_ID])

# Connect to the sqlite results database
database = sqlite3.connect('crowdstorming.db')
db       = database.cursor()

# Get all hits with given job id
db.execute("select * from hits where Job_ID = ?", [JOB_ID])
allHits = db.fetchall()

# see if there are hits that are completed but have no childern
newlyCompletedHits = []
for hit in allHits:
    hitID = str(hit[1]);
    currIter = hit[3]
    numCompleted = hit[4]
    hasChildren = hit[6]
    print hitID + " " + str(currIter) + " " + str(numCompleted) + " " + str(hasChildren)
    if (currIter < 4 and numCompleted == 3 and hasChildren == 0):
        newlyCompletedHits.append((hitID, currIter))

# Get Results from newly completed HIT and create new HITs from them
print newlyCompletedHits
for hitID, currIter in newlyCompletedHits:
    db.execute("select Response from results where Hit_ID = ?", [hitID])
    newPhrases = db.fetchall()
    newIter = currIter+1
    for phrase in newPhrases:
        call (["python", "mturk-create.py", str(phrase[0]), str(JOB_ID), str(newIter), str(hitID)])
    
    # update Has_Children field
    #db.execute('BEGIN DEFERRED TRANSACTION')
    hitsUpdate =   "UPDATE hits SET Has_Children=1 WHERE Hit_ID=?"
    db.execute(hitsUpdate, [hitID])
    #db.execute('COMMIT TRANSACTION')
    #db.execute('END TRANSACTION')

    # Save changes
    database.commit()

# draw graph
call (["python", "mturk-draw.py", JOB_ID])

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

