import os
from subprocess import Popen
from time import sleep, time


# get this dir path
workdir = os.path.dirname(os.path.abspath(__file__))

# set this path as working path
os.chdir(workdir)

log_file = open("run_log.txt", "w")
p = Popen(["pipenv", "run", "python", "manage.py", "runserver"], stderr=log_file)







