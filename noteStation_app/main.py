import os

from notestation_interfaces import *

PATH_FILE = os.path.expanduser('~\\Documents\\noteStation')

if not os.path.exists(PATH_FILE):
    os.mkdir(PATH_FILE)

dir = os.path.expanduser(PATH_FILE + '\\lista_tarefas.json')

main_app = TelaInicial(dir)

main_app.exibir()