from notestation_interfaces import *
from tarefa_classes import *

organizador = TarefaOrganizador()
dir = 'lista_tarefas.json'

main_app = TelaInicial(organizador, dir)

main_app.exibir()