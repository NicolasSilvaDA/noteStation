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

        # Verificar gerenciamento para decoradores
        check_lembrete = hasattr(obj, "lembrete") or hasattr(obj._tarefa, "lembrete")
        check_prazo = hasattr(obj, "prazo") or hasattr(obj._tarefa, "prazo")
        lembrete = ""
        prazo = ""

        if check_lembrete:
            lembrete = obj.lembrete if obj.lembrete else obj._tarefa.lembrete
        
        if check_prazo:
            prazo = obj.prazo if obj.prazo else obj._tarefa.prazo

        return {
            "titulo": obj_base.titulo,
            "descricao": obj_base.descricao,
            "data_criacao": obj_base.data_criacao,
            "data_exata": obj_base.data_exata,
            "concluida": obj_base.concluida,
            "_tarefa": obj_base._tarefa,
            "lembrete": lembrete,
            "prazo": prazo
        }