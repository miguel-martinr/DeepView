from subprocess import Popen
from time import sleep, time


log_file = open("log.txt", "w")
p = Popen(["pipenv", "install"], stderr=log_file)

p.wait()

input("Dependencias instaladas. Puedes cerrar esta ventana.")



