from abc import ABC, abstractmethod

from tarefa import Tarefa, TarefaBase, TarefaTrabalho, TarefaComPrioridade

class TarefaFactory(ABC):

    @abstractmethod
    def criar_tarefa(self) -> Tarefa:
        pass


class TarefaTrabalhoFactory(TarefaFactory):
    def criar_tarefa(self) -> Tarefa:
        return TarefaTrabalho(TarefaBase())
    

class TarefaComPrioridadeFactory(TarefaFactory):
    def criar_tarefa(self) -> Tarefa:
        return TarefaComPrioridade(TarefaBase())