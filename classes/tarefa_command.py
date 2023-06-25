from abc import ABC, abstractmethod
from typing import Optional
from datetime import date
from copy import deepcopy

from classes.tarefa import Tarefa, TarefaOrganizador, TarefaComLembrete, TarefaComPrazo

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
    def __init__(self, tarefa: Tarefa, nTitulo: str, nDescricao: str, nLembrete: Optional[str], nPrazo: Optional[date]):
        # A anotação Optional[date] indica que o tipo de dado pode ser date ou None
        self.tarefa = tarefa
        self.copiaTarefa = deepcopy(tarefa)
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
            if isinstance(self.tarefa, TarefaComLembrete):
                self.tarefa.atualizar_lembrete(self.nLembrete)

        if self.nPrazo:
            if isinstance(self.tarefa, TarefaComPrazo):
                self.tarefa.atualizar_prazo(self.nPrazo)

    def desfazer_operacao(self) -> None:
        self.tarefa.titulo = self.copiaTarefa.titulo
        self.tarefa.descricao = self.copiaTarefa.descricao
        if isinstance(self.tarefa, TarefaComLembrete):
            self.tarefa.atualizar_lembrete(self.copiaTarefa.lembrete)
        
        if isinstance(self.tarefa, TarefaComPrazo):
            self.tarefa.atualizar_prazo(self.copiaTarefa.prazo)
        

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
