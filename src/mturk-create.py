import datetime
from boto.pyami.config import Config, BotoConfigLocations
import boto.mturk.connection
import boto.mturk.question as mtq
import boto.mturk.qualification as mtqu

config = Config()
AWS_ID = config.get('Credentials', 'aws_access_key_id', None)
SECRET_ID = config.get('Credentials', 'aws_secret_access_key_id', None)
HOST = 'mechanicalturk.sandbox.amazonaws.com'

mt = boto.mturk.connection.MTurkConnection(
   aws_access_key_id=AWS_ID, 
   aws_secret_access_key=SECRET_ID, 
   host=HOST)
 
text_en = '''Hello!
I am test text message to be translated from English to Russian.
If you ask me, I was born in a mind of a crazy web developer,
who tests the MTurk API to start a very promising service later.
'''

question_id = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
print('id=%s' % question_id)

content1 = mtq.QuestionContent()
content1.append_field('Title', 'Translate a text between the markers below from English to Russian.')
content1.append_field('Title', 'Human translation only! Machine tranlations will be rejected.')
content1.append_field('Text', '================= FROM HERE =================')
content1.append_field('Text', text_en)
content1.append_field('Text', '================= TILL HERE =================')
   
content2 = mtq.QuestionContent()
content2.append_field('Title', 'Any notes? Advices? Emotions? (Optional)')
   
question1 = mtq.Question(
   question_id,
   content = content1,
   answer_spec = mtq.AnswerSpecification(mtq.FreeTextAnswer()),
   is_required = True,
   )
question2 = mtq.Question(
   question_id+'-b',
   content = content2,
   answer_spec = mtq.AnswerSpecification(mtq.FreeTextAnswer()),
   is_required = False,
   )
   
qualifications = mtqu.Qualifications()
qualifications.add(mtqu.PercentAssignmentsApprovedRequirement('GreaterThanOrEqualTo', 75))
      
res = mt.create_hit(
   questions=[question1, question2],
   qualifications=qualifications,
            
   title = 'Translate 3 lines from English to Russian (human translation needed).',
   description = 'Translate 3 lines of English to Russian. No machine translations will be accepted. Only human translation.',
   keywords='translate, translation, english, russian',
                     
   # These things affect the total cost:
   reward=mt.get_price_as_price(0.05),
   max_assignments=2,
                                 
   # These are for scheduling and timing out.
   approval_delay=datetime.timedelta(seconds=24*60*60),# auto-approve timeout
   duration=datetime.timedelta(seconds=15*60),# how fast the task is abandoned if not finished
   )
      
hit = res[0]
hit_id = hit.HITId
print('hit id = %s' % hit_id)
filename = 'hit-%s.txt' % question_id
file(filename, 'wt').write(hit_id)
print('saved to %s' % filename)



