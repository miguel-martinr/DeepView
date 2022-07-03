from subprocess import Popen
from time import sleep, time


log_file = open("run_log.txt", "w")
p = Popen(["pipenv", "run", "python", "manage.py", "runserver"], stderr=log_file)







