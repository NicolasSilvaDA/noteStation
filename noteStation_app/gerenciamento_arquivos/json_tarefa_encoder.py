"""
Módulo contendo uma classe de codificação personalizada para tarefas e importações de módulos.

Módulos importados:
    - sys: Módulo do sistema Python.
    - os: Módulo que fornece uma maneira de usar funcionalidades dependentes do sistema operacional.
    - json: Módulo que permite trabalhar com dados JSON (JavaScript Object Notation).

Atributos:
    - Nenhum atributo relevante é definido na classe.

Métodos:
    - TarefaEncoder.default(obj): Método que converte um objeto em uma representação serializável em JSON.
        - obj: O objeto a ser codificado em JSON.

Detalhes dos atributos e métodos:
    - TarefaEncoder.default(obj): Método sobrescrito da classe JSONEncoder que é chamado para objetos não serializáveis padrão.
        - O método verifica o tipo da tarefa passada como argumento e cria um dicionário contendo as informações da tarefa para serem codificadas em JSON.
        - A prioridade da tarefa é verificada e definida como True caso seja uma TarefaComPrioridade, caso contrário, é definida como False.
        - As informações de título, descrição, data de criação, data exata, conclusão, tarefa base (_tarefa), lembrete e prazo são armazenadas no dicionário.
        - O dicionário é retornado como a representação serializável da tarefa em formato JSON.
"""

import sys
import os
import json

diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(diretorio_pai)

from tarefa_classes import *


class TarefaEncoder(json.JSONEncoder):
    """
    Classe de codificação personalizada para objetos de tarefa em formato JSON.

    Métodos:
        default(obj)
    """
    def default(self, obj):
        """
        Método sobrescrito da classe JSONEncoder que converte um objeto em uma representação serializável em JSON.

        Atributos:
            - obj: O objeto a ser codificado em JSON.
        
        Retorna:
            - Um dicionário contendo as informações da tarefa para serem codificadas em JSON.
                - A prioridade da tarefa é verificada e definida como True caso seja uma TarefaComPrioridade, caso contrário, é definida como False.
                - As informações de título, descrição, data de criação, data exata, conclusão, tarefa base (_tarefa), lembrete e prazo são armazenadas no dicionário.
                - O dicionário é retornado como a representação serializável da tarefa em formato JSON.
        """
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