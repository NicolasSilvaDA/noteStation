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

Atributos:
- Nenhum atributo relevante é definido nas classes.

Métodos:
- TarefaFactory.criar_tarefa(): Método abstrato que cria e retorna uma instância de Tarefa.

- TarefaTrabalho.exibir(): Método que retorna uma string formatada com as informações de uma tarefa de trabalho.
- TarefaTrabalhoFactory.criar_tarefa(titulo, descricao): Método que cria e retorna uma tarefa de trabalho com o título e descrição especificados.

- TarefaComPrioridade.exibir(): Método que retorna uma string formatada com as informações de uma tarefa com prioridade.
- TarefaComPrioridadeFactory.criar_tarefa(titulo, descricao): Método que cria e retorna uma tarefa com prioridade com o título e descrição especificados.
"""

from abc import ABC, abstractmethod

from tarefa_classes.tarefa import Tarefa, TarefaBase

class TarefaFactory(ABC):

    @abstractmethod
    def criar_tarefa(self) -> Tarefa:
        pass


class TarefaTrabalho(TarefaBase):
    def exibir(self) -> str:
        return f'Tarefa de Trabalho\n{super().exibir()}\n'
    

class TarefaComPrioridade(TarefaBase):
    def exibir(self) -> str:
        return f'Tarefa com prioridade\n{super().exibir()}\n'


class TarefaTrabalhoFactory(TarefaFactory):
    def criar_tarefa(self, titulo: str, descricao: str) -> Tarefa:
        return TarefaTrabalho(titulo, descricao)
    

class TarefaComPrioridadeFactory(TarefaFactory):
    def criar_tarefa(self, titulo: str, descricao: str) -> Tarefa:
        return TarefaComPrioridade(titulo, descricao)