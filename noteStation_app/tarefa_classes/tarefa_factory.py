"""
Módulo contendo as classes e fábricas relacionadas à criação de tarefas e suas implementações.

Classes:
    - TarefaFactory: Classe abstrata que define a estrutura de uma fábrica de tarefas com o método abstrato "criar_tarefa()".
    - TarefaTrabalhoFactory: Classe concreta que implementa uma fábrica de tarefas de trabalho.
    - TarefaComPrioridadeFactory: Classe concreta que implementa uma fábrica de tarefas com prioridade.
    - TarefaTrabalho: Classe concreta que representa uma tarefa de trabalho, herdando de TarefaBase.
    - TarefaComPrioridade: Classe concreta que representa uma tarefa com prioridade, herdando de TarefaBase.

Módulos importados:
    - ABC: Módulo do pacote "abc" que fornece as classes e funções para trabalhar com metaprogramação orientada a aspectos.
    - abstractmethod: Decorador para um método abstrato, que deve ser implementado nas classes derivadas.
"""

from abc import ABC, abstractmethod

from tarefa_classes.tarefa import Tarefa, TarefaBase

class TarefaFactory(ABC):
    """
    Classe abstrata que define uma fábrica de tarefas.

    Métodos abstratos:
        - criar_tarefa(self, titulo: str, descricao: str) -> Tarefa: Cria e retorna uma nova instância de Tarefa.

    Atributos:
        - Nenhum atributo na classe abstrata.
    """
    @abstractmethod
    def criar_tarefa(self) -> Tarefa:
        """
        Método abstrato para criar uma nova tarefa.

        Parâmetros:
            - titulo (str): O título da tarefa.
            - descricao (str): A descrição da tarefa.

        Retorna:
            - Tarefa: Uma nova instância de Tarefa.
        """
        pass


class TarefaTrabalho(TarefaBase):
    """
    Classe que representa uma tarefa de trabalho.

    Métodos:
        - exibir(self) -> str: Retorna uma string formatada com os detalhes da tarefa de trabalho.

    Atributos:
        - Nenhum atributo específico nesta classe. Os atributos são herdados da classe TarefaBase.
    """
    def exibir(self) -> str:
        """
        Retorna uma string formatada com os detalhes da tarefa de trabalho.

        Retorna:
            - str: Uma string com os detalhes da tarefa de trabalho.
        """
        return f'Tarefa de Trabalho\n{super().exibir()}\n'
    

class TarefaComPrioridade(TarefaBase):
    """
    Classe que representa uma tarefa com prioridade.

    Métodos:
        - exibir(self) -> str: Retorna uma string formatada com os detalhes da tarefa com prioridade.

    Atributos:
        - Nenhum atributo específico nesta classe. Os atributos são herdados da classe TarefaBase.
    """
    def exibir(self) -> str:
        """
        Retorna uma string formatada com os detalhes da tarefa com prioridade.

        Retorna:
            - str: Uma string com os detalhes da tarefa com prioridade.
        """
        return f'Tarefa com prioridade\n{super().exibir()}\n'


class TarefaTrabalhoFactory(TarefaFactory):
    """
    Classe que implementa a fábrica de tarefas de trabalho.

    Métodos:
        - criar_tarefa(self, titulo: str, descricao: str) -> Tarefa: Cria e retorna uma nova instância de TarefaTrabalho.

    Atributos:
        - Nenhum atributo específico nesta classe. Os atributos são herdados da classe TarefaFactory.
    """
    def criar_tarefa(self, titulo: str, descricao: str) -> Tarefa:
        """
        Cria e retorna uma nova instância de TarefaTrabalho.

        Parâmetros:
            - titulo (str): O título da tarefa.
            - descricao (str): A descrição da tarefa.

        Retorna:
            - TarefaTrabalho: Uma nova instância de TarefaTrabalho.
        """
        return TarefaTrabalho(titulo, descricao)
    

class TarefaComPrioridadeFactory(TarefaFactory):
    """
    Classe que implementa a fábrica de tarefas com prioridade.

    Métodos:
        - criar_tarefa(self, titulo: str, descricao: str) -> Tarefa: Cria e retorna uma nova instância de TarefaComPrioridade.

    Atributos:
        - Nenhum atributo específico nesta classe. Os atributos são herdados da classe TarefaFactory.
    """
    def criar_tarefa(self, titulo: str, descricao: str) -> Tarefa:
        """
        Cria e retorna uma nova instância de TarefaComPrioridade.

        Parâmetros:
            - titulo (str): O título da tarefa.
            - descricao (str): A descrição da tarefa.

        Retorna:
            - TarefaComPrioridade: Uma nova instância de TarefaComPrioridade.
        """
        return TarefaComPrioridade(titulo, descricao)