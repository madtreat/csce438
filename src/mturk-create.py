# This script handles creating a single HIT for a particular job
# for MTurk workers to perform.
#
# Created by Madison Treat, Kodi Tapie and Blake Robertson
#
#
# DO NOT call this script except for developmental purposes.
# It should ONLY be called from mturk-manage.py and mturk-create-init-seed.py
#

import datetime, sys, sqlite3
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
from boto.mturk.qualification import Qualifications,PercentAssignmentsApprovedRequirement

# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " phrase Job_ID iter parent_HIT_ID")
   print("\nWhere:")
   print("   phrase  = the phrase turkers will see for this HIT")
   print("   Job_ID     = the Seed Phrase ID")
   print("   iter    = the iteration/level for this particular HIT")
   print("   parent_HIT_ID    = the parent HIT of the new HIT to be created")
   print("   num_branches    = Number of branches for each node")

if len(sys.argv) != 6:
   print_usage()
   exit()

# Get Command Line Arguments
PHRASE        = sys.argv[1]
JOB_ID        = sys.argv[2]
ITERATION     = sys.argv[3]
PARENT_HIT_ID = sys.argv[4]
BRANCHES      = sys.argv[5]


# Connect to the HIT database
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

# HIT Configuration - global title, description, keywords, qualifications
TITLE    = 'Provide Related Terms'
DESC     = 'Given a word or phrase, provide another (different) word that relates to the given one.'
KEYWORDS = 'opinions, relations, idea, brainstorm, crowdstorm'
QUAL     = Qualifications()
QUAL     = QUAL.add(PercentAssignmentsApprovedRequirement('GreaterThanOrEqualTo', 75))
REWARD   = 0.01
MAX_ASSN = BRANCHES

# HIT Overview
overview = Overview()
overview.append_field('Title', 'Tell us things or phrases that relate to a given phrase or picture')

# Build Question(s)
qc = QuestionContent()
qc.append_field('Title', 'Enter a word or phrase that relates to:')
qc.append_field('Text',  PHRASE)

answer = FreeTextAnswer()

question = Question(
   identifier='comments',
   content=qc,
   answer_spec=AnswerSpecification(answer),
   is_required = True,
   )

# Build Question Form
qform = QuestionForm()
qform.append(overview)
qform.append(question)

# Create the HIT
# Insert this HIT's info into the database
uniqueTable = "SELECT * FROM unique_phrases WHERE (Job_ID = ? AND  Phrase = ?)"
db.execute(uniqueTable, [JOB_ID, PHRASE])
unique = db.fetchall()

if (len(unique) == 0):
    res = mt.create_hit(
       questions      = [question],
       qualifications = QUAL,
                
       title          = TITLE,
       description    = DESC,
       keywords       = KEYWORDS,
                         
       # These things affect the total cost:
       reward         = mt.get_price_as_price(REWARD),
       max_assignments= MAX_ASSN,
                                     
       # These are for scheduling and timing out.
       # auto-approve timeout
       approval_delay = datetime.timedelta(seconds=60),#4*60*60),
       # how fast the task is abandoned if not finished
       duration       = datetime.timedelta(seconds=15*60),
       )
          
    hit = res[0]
    HIT_ID = hit.HITId
    status = 'iteration {}: hit spawned with id = {} and phrase = {}'.format(ITERATION, HIT_ID, PHRASE)
    print(status)

    # insert new HIT into the HIT table
    hitsTable = "INSERT INTO hits VALUES (?, ?, ?, ?, 0, ?, 0)"
    db.execute(hitsTable, (JOB_ID, HIT_ID, PARENT_HIT_ID, ITERATION, PHRASE))
    
    #insert new phrase into the unique phrase table
    uniqueTable = "INSERT OR REPLACE INTO unique_phrases VALUES(?, ?)"
    db.execute(uniqueTable, (JOB_ID, str(PHRASE).lower()))

# Save changes
database.commit()
database.close()

