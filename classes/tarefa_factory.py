from abc import ABC, abstractmethod

from classes.tarefa import Tarefa, TarefaBase

class TarefaFactory(ABC):

    @abstractmethod
    def criar_tarefa(self) -> Tarefa:
        pass


class TarefaTrabalho(TarefaBase):
    def exibir(self) -> str:
        return f'Tarefa de Trabalho\n{super().exibir()}'
    

class TarefaComPrioridade(TarefaBase):
    def exibir(self) -> str:
        return f'Tarefa com prioridade\n{super().exibir()}'


class TarefaTrabalhoFactory(TarefaFactory):
    def criar_tarefa(self, titulo, descricao) -> Tarefa:
        return TarefaTrabalho(titulo, descricao)
    

class TarefaComPrioridadeFactory(TarefaFactory):
    def criar_tarefa(self, titulo: str, descricao: str) -> Tarefa:
        return TarefaComPrioridade(titulo, descricao)