from abc import ABC, abstractmethod
from typing import Optional
from datetime import date

from tarefa import Tarefa, TarefaOrganizador


class TarefaCommand(ABC):

    @abstractmethod
    def executar(self):
        pass

    @abstractmethod
    def desfazer_operacao(self):
        pass


class CriarTarefaCommand(TarefaCommand):
    def __init__(self, tarefa: Tarefa, organizador: TarefaOrganizador):
        self.tarefa = tarefa
        self.organizador = organizador

    def executar(self) -> None:
        self.organizador.tarefas.append(self.tarefa)
    
    def desfazer_operacao(self) -> None:
        self.organizador.tarefas.remove(self.tarefa)


class EditarTarefaCommand(TarefaCommand):
    def __init__(self, tarefa: Tarefa, nTitulo: str, nDescricao: str, nLembrete: str, nPrazo: Optional[date]):
        # A anotação Optional[date] indica que o tipo de dado pode ser date ou None
        self.tarefa = tarefa
        self.copiaTarefa = tarefa
        self.nTitulo = nTitulo
        self.nDescricao = nDescricao
        self.nLembrete = nLembrete
        self.nPrazo = nPrazo

    def executar(self) -> None:
        if self.nTitulo:
            self.tarefa.titulo = self.nTitulo
        
        if self.nDescricao:
            self.tarefa.descricao = self.nDescricao

        if self.nLembrete:
            self.tarefa.lembrete = self.nLembrete

        if self.nPrazo:
            self.tarefa.prazo = self.nPrazo

    def desfazer_operacao(self) -> None:
        self.tarefa.titulo = self.copiaTarefa.titulo
        self.tarefa.descricao = self.copiaTarefa.descricao
        self.tarefa.lembrete = self.copiaTarefa.lembrete
        self.tarefa.prazo = self.copiaTarefa.prazo
        

class ExcluirTarefaCommand(TarefaCommand):
    def __init__(self, tarefa: Tarefa, organizador: TarefaOrganizador):
        self.tarefa = tarefa
        self.organizador = organizador

    def executar(self) -> None:
        self.organizador.tarefas.remove(self.tarefa)

    def desfazer_operacao(self) -> None:
        self.organizador.tarefas.append(self.tarefa)


class MarcarConcluidaCommand(TarefaCommand):
    def __init__(self, tarefa: Tarefa):
        self.tarefa = tarefa

    def executar(self) -> None:
        self.tarefa.concluida = True

    def desfazer_operacao(self) -> None:
        self.tarefa.concluida = False