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
    def criar_tarefa(titulo, descricao) -> Tarefa:
        return TarefaTrabalho(titulo, descricao)
    

class TarefaComPrioridadeFactory(TarefaFactory):
    def criar_tarefa(titulo: str, descricao: str) -> Tarefa:
        return TarefaComPrioridade(titulo, descricao)