import dearpygui.dearpygui as dpg
from datetime import datetime

from tarefa_classes import *
from notestation_interfaces import *


# tarefa = TarefaBase("Exemplo 1", "aaaaaa")

# print(tarefa.exibir())

# tarefa_com_lembrete = TarefaComLembrete(tarefa, "Importante lembrar")

# print(tarefa_com_lembrete.exibir())

# tarefa_com_lembrete_e_prazo = TarefaComPrazo(tarefa_com_lembrete, "26/06/2023")

# print(tarefa_com_lembrete_e_prazo.exibir())

# # 2

# tarefa_trabalho_fact = TarefaTrabalhoFactory()

# tar_trab = tarefa_trabalho_fact.criar_tarefa("Exemplo 2", "BBBBBB")
# print(tar_trab.exibir())
# print(f'\n({tar_trab.__class__.__name__})')

# tarefa_prio_fact = TarefaComPrioridadeFactory()

# tar_prio = tarefa_prio_fact.criar_tarefa("Exemplo 3", "CCCCCC")
# print(tar_prio.exibir())
# print(f'\n({tar_prio.__class__.__name__})')

# # 3

# org = TarefaOrganizador()

# tarefa2 = TarefaBase("Exemplo 4", "DDDDDD")
# tarefa2 = TarefaComLembrete(tarefa2, "Importante")
# tarefa2 = TarefaComPrazo(tarefa2, "26/06/2023")

# criar_tar_com = CriarTarefaCommand(tarefa2, org)
# excluir_tar_com = ExcluirTarefaCommand(tarefa2, org)
# editar_tar_com = EditarTarefaCommand(tarefa2, "Teste 4", "GGGGGG", "Nada demais", "01/07/2023")
# concluir_tar_com = MarcarConcluidaCommand(tarefa2)

# print(tarefa2.exibir())
# print("____________________")

# criar_tar_com.executar()
# print(org.tarefas)

# editar_tar_com.executar()
# print(tarefa2.exibir())

# print("\n\n")

# concluir_tar_com.executar()
# print(tarefa2.exibir())

# excluir_tar_com.executar()
# print(org.tarefas)

# print("_______________________")

# excluir_tar_com.desfazer_operacao()
# print(org.tarefas)

# concluir_tar_com.desfazer_operacao()
# print(tarefa2.exibir())

# editar_tar_com.desfazer_operacao()
# print(tarefa2.exibir())

# criar_tar_com.desfazer_operacao()
# print(org.tarefas)

tarefa = TarefaBase("Comprar frutas", "abubléf")
tarefa2 = TarefaBase("Alimentar cachorro", "abublés")
tarefa3 = TarefaBase("Fazer compras", "abubléw")
tarefa4 = TarefaBase("Beber água", "abubléee")

organizador = TarefaOrganizador()

organizador.add_tarefa(tarefa)
organizador.add_tarefa(tarefa2)
organizador.add_tarefa(tarefa3)
organizador.add_tarefa(tarefa4)

print(organizador.tarefas)

print(organizador.tarefas.sort(key=lambda x: organizador.checkTarefaDecorator(x).titulo))

print(organizador.tarefas)

print(organizador.tarefas.sort(key=lambda x:  datetime.strptime(organizador.checkTarefaDecorator(x).data_criacao, "%d/%m/%Y %H:%M")))

print(organizador.tarefas)

# tela_inicial = TelaInicial(organizador)
# tela_inicial.exibir()
# dpg.create_context()
# dpg.show_viewport()

# while dpg.is_dearpygui_running():
#     dpg.render_dearpygui_frame()

# dpg.destroy_context()