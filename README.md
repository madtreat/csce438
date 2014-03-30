csce438
=======

Homework 3 (and 4) of CSCE 438 at Texas A&amp;M University


DETAILED DESCRIPTION:
=====================
Use only the following two scripts to start a job and manage it.
Note: your AMT credentials should be entered into a BOTO configuration file
   UNIX: ~/.boto
   see https://code.google.com/p/boto/wiki/BotoConfig

To launch the initial AMT job, use the following script (Note: Python 3.3 is required)
   $ python src/mturk-create-init-seed.py <num_iter> <num_branches> "<seed_phrase>"

The number of iterations and branches provided will change the appearance
of the results graph, and will affect the quality and "far-reaching" 
effect of the brainstorming task.
The "seed_phrase" is the phrase you would like to have crowd-stormed.

Once the above script has been run to create the initial job, results can be checked
using the mturk-manage.py script.
   $ python mturk-manage.py <job_id>

The Job ID returned from the "create-init-seed.py" script should be used as an 
argument to the "manage" script.  

Note that the "manage" script calls all other necessary scripts, thus DO NOT CALL ANY OTHER SCRIPTS except the "init-seed" script to start a crowd storming job, and the "manage" script to collect the 
results, add them to the database, and start the next iteration of AMT HITS.

