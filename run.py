import os
from subprocess import Popen
from time import sleep, time


# get this dir path
workdir = os.path.dirname(os.path.abspath(__file__))

# set this path as working path
os.chdir(workdir)

p = Popen(["poetry", "run", "python", "manage.py", "runserver"])








