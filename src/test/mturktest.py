from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
import sys
 
ACCESS_ID ='xx'
SECRET_KEY = 'yy'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
title = 'Tell us a word or phrase that relates to a given word/phrase'
description = ('Given a word or short phrase, provide another word or short phrase that relates to'
               ' the one given.')

keywords = 'opinions, relations'

phrase = sys.argv[1];

 
#---------------  BUILD OVERVIEW -------------------
 
overview = Overview()
overview.append_field('Title', 'Tell us things or phrases that relate to a given phrase or picture')
overview.append(FormattedContent('<a target="_blank"'
                                 ' href="http://www.toforge.com">'
                                 ' Mauro Rocco Personal Forge</a>'))
 
#---------------  BUILD QUESTION -------------------
 
qc1 = QuestionContent()
qc1.append_field('Title','Enter a word or phrase that relates to: '+phrase)
 
fta1 = FreeTextAnswer()
 
q1 = Question(identifier="comments",
              content=qc1,
              answer_spec=AnswerSpecification(fta1))
 
#--------------- BUILD THE QUESTION FORM -------------------
 
question_form = QuestionForm()
question_form.append(overview)
question_form.append(q1)
 
#--------------- CREATE THE HIT -------------------
 
mtc.create_hit(questions=question_form,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.05)