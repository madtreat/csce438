import datetime, sys, sqlite3
from boto.pyami.config import Config, BotoConfigLocations
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
from boto.mturk.qualification import Qualifications,PercentAssignmentsApprovedRequirement


# Ensure this script was correctly called
def print_usage():
   print("Usage: " + sys.argv[0] + " word iteration")

if len(sys.argv) != 3:
   print_usage()
   exit()


# Connect to the HIT database
database = sqlite3.connect('hits.db')
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
REWARD   = 0.05
MAX_ASSN = 1# 10? 20?

# The given phrase to be brainstormed - read from the first argument
PHRASE   = sys.argv[1]
ITERATION= sys.argv[2]


# HIT Overview
overview = Overview()
overview.append_field('Title', 'Tell us things or phrases that relate to a given phrase or picture')
#overview.append(FormattedContent('<a target="_blank"'
#                                 ' href="http://www.toforge.com">'
#                                 ' Mauro Rocco Personal Forge</a>'))


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
res = mt.create_hit(
   questions      = [question],#, question2],
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
hit_id = hit.HITId
status = 'iteration {}: hit spawned with id = {}'.format(ITERATION, hit_id)
print(status)

db.execute('''CREATE TABLE IF NOT EXISTS hits (id, iter)''')
db_entry = "INSERT INTO hits VALUES (\'" + hit_id + "\',\'" + ITERATION + "\')"
db.execute(db_entry)

