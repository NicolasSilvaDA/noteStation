import sys
import os
import json

diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(diretorio_pai)

from tarefa_classes import *


class TarefaEncoder(json.JSONEncoder):
    def default(self, obj):
        organizador = TarefaOrganizador()
        obj_base = organizador.checkTarefaDecorator(obj)
        
        lembrete = ""
        prazo = ""
        prioridade = False

        if obj_base.__class__.__name__ == "TarefaComPrioridade":
            prioridade = True

        if hasattr(obj, "lembrete"):
            lembrete = obj.lembrete
        elif hasattr(obj._tarefa, "lembrete"):
            lembrete = obj._tarefa.lembrete
        
        if hasattr(obj, "prazo"):
            prazo = obj.prazo
        elif hasattr(obj._tarefa, "prazo"):
            prazo = obj._tarefa.prazo

        return {
            "prioridade": prioridade,
            "titulo": obj_base.titulo,
            "descricao": obj_base.descricao,
            "data_criacao": obj_base.data_criacao,
            "data_exata": obj_base.data_exata,
            "concluida": obj_base.concluida,
            "_tarefa": obj_base._tarefa,
            "lembrete": lembrete,
            "prazo": prazo
        }