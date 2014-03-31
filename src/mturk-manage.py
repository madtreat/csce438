# This file is the main script for our "Crowd-Storming" Application
#
# Created by Madison Treat, Kodi Tapie and Blake Robertson
#
#
# The idea is that this script will be used to manage the lifecycle
# of a job.  In particular, the different functions that will be 
# performed by this script (using the other scripts) are:
#  - retrieve and aggregate all results
#  - create new HITs based on the results
#  - Show current updated Graph
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
   print("\nWhere:")
   print("   job_id  = Job ID given to you after calling mturk-create-init-seed.py")

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

# Get max iterations and branches from job table
db.execute("select * from jobs where Job_ID = ?", [JOB_ID])
jobInfo = db.fetchall()
MAX_ITER = jobInfo[0][2]
BRANCHES = jobInfo[0][3]

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
    # only create new HITs if:
    #  - The current iteration is less than the max iteration specified
    #  - The number of completed assignments is equal to the number of branches we want
    #  - The HIT hasn't already create new HITs based on its results
    if (currIter < (MAX_ITER-1) and numCompleted == BRANCHES and hasChildren == 0):
        newlyCompletedHits.append((hitID, currIter))

# Create new HITs from the newly completed HITs
for hitID, currIter in newlyCompletedHits:
    db.execute("select Response from results where Hit_ID = ?", [hitID])
    newPhrases = db.fetchall()
    nextIter = currIter+1
    
    # for each response in the newly completed HIT create new HITs
    for phrase in newPhrases:
        call (["python", "mturk-create.py", str(phrase[0]), str(JOB_ID), str(nextIter), str(hitID), str(BRANCHES)])
    
    # update Has_Children field
    hitsUpdate =   "UPDATE hits SET Has_Children=1 WHERE Hit_ID=?"
    db.execute(hitsUpdate, [hitID])

    # Save changes
    database.commit()

# draw graph
call (["python", "mturk-draw.py", JOB_ID])

# Clean up and close the database
database.close()

