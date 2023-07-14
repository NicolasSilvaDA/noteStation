from abc import ABC, abstractmethod
from typing import Optional
from datetime import date, datetime
import copy

from tarefa_classes.tarefa import Tarefa, TarefaOrganizador, TarefaComLembrete, TarefaComPrazo

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
    def __init__(self, tarefa: Tarefa, nTitulo: str, nDescricao: str, nLembrete: Optional[str], nPrazo: Optional[date], organizador: TarefaOrganizador):
        # A anotação Optional[date] indica que o tipo de dado pode ser date ou None, a mesma
        # coisa para o Optional[str]
        self.tarefa = tarefa
        self.copiaTarefa = copy.deepcopy(tarefa)
        self.nTitulo = nTitulo
        self.nDescricao = nDescricao
        self.nLembrete = nLembrete
        self.nPrazo = nPrazo
        self.organizador = organizador

    def executar(self) -> None:

        tarefa = self.organizador.checkTarefaDecorator(self.tarefa)

        if self.nTitulo:
            tarefa.titulo = self.nTitulo
        
        if self.nDescricao:
            tarefa.descricao = self.nDescricao

        if self.nLembrete:
            if isinstance(self.tarefa, TarefaComLembrete):
                self.tarefa.alterar_lembrete(self.nLembrete)

            elif isinstance(self.tarefa._tarefa, TarefaComLembrete):
                self.tarefa._tarefa.alterar_lembrete(self.nLembrete)

        if self.nPrazo:
            if isinstance(self.tarefa, TarefaComPrazo):
                self.tarefa.atualizar_prazo(self.nPrazo)

            elif isinstance(self.tarefa._tarefa, TarefaComPrazo):
                self.tarefa._tarefa.atualizar_prazo(self.nPrazo)

    def desfazer_operacao(self) -> None:

        tarefa = self.organizador.checkTarefaDecorator(self.tarefa)
        copiaTarefa = self.organizador.checkTarefaDecorator(self.copiaTarefa)

        tarefa.titulo = copiaTarefa.titulo
        tarefa.descricao = copiaTarefa.descricao
            
        if self.nLembrete:
            try:
                if isinstance(self.tarefa, TarefaComLembrete) and isinstance(self.copiaTarefa, TarefaComLembrete):
                    self.tarefa.alterar_lembrete(self.copiaTarefa.lembrete)

                elif isinstance(self.tarefa, TarefaComLembrete) and not isinstance(self.copiaTarefa, TarefaComLembrete):
                    self.tarefa.alterar_lembrete(self.copiaTarefa._tarefa.lembrete)

                elif not isinstance(self.tarefa, TarefaComLembrete) and isinstance(self.copiaTarefa, TarefaComLembrete):
                    self.tarefa._tarefa.alterar_lembrete(self.copiaTarefa.lembrete)

                elif not isinstance(self.tarefa, TarefaComLembrete) and not isinstance(self.copiaTarefa, TarefaComLembrete):
                    self.tarefa._tarefa.alterar_lembrete(self.copiaTarefa._tarefa.lembrete)
                    
            except:
                raise Exception("Tarefa não possui lembrete.")

        if self.nPrazo:
            try:
                if isinstance(self.tarefa, TarefaComPrazo) and isinstance(self.copiaTarefa, TarefaComPrazo):
                    self.tarefa.atualizar_prazo(self.copiaTarefa.prazo)

                elif isinstance(self.tarefa, TarefaComPrazo) and not isinstance(self.copiaTarefa, TarefaComPrazo):
                    self.tarefa.atualizar_prazo(self.copiaTarefa._tarefa.prazo)

                elif not isinstance(self.tarefa, TarefaComPrazo) and isinstance(self.copiaTarefa, TarefaComPrazo):
                    self.tarefa._tarefa.atualizar_prazo(self.copiaTarefa.prazo)

                elif not isinstance(self.tarefa, TarefaComPrazo) and not isinstance(self.copiaTarefa, TarefaComPrazo):
                    self.tarefa._tarefa.atualizar_prazo(self.copiaTarefa._tarefa._tarefa.prazo)

            except:
                raise Exception("Tarefa não possui prazo")
        

class ExcluirTarefaCommand(TarefaCommand):
    def __init__(self, tarefa: Tarefa, organizador: TarefaOrganizador):
        self.tarefa = tarefa
        self.organizador = organizador

    def executar(self) -> None:
        self.organizador.tarefas.remove(self.tarefa)

    def desfazer_operacao(self) -> None:
        self.organizador.tarefas.append(self.tarefa)


class MarcarConcluidaCommand(TarefaCommand):
    def __init__(self, tarefa: Tarefa, organizador: TarefaOrganizador):
        self.tarefa = tarefa
        self.organizador = organizador

    def executar(self) -> None:
        tarefa = self.organizador.checkTarefaDecorator(self.tarefa)
        tarefa.concluida = True

    def desfazer_operacao(self) -> None:
        tarefa = self.organizador.checkTarefaDecorator(self.tarefa)
        tarefa.concluida = False

class OrdenarListaTarefasCommand(TarefaCommand):
    def __init__(self, organizador: TarefaOrganizador, filtro: str):
        self.listaTarefasCopia = copy.copy(organizador.tarefas)
        self.organizador = organizador
        self.filtro = filtro

    def executar(self) -> None:
        if self.filtro == "Data de criação":
            self.organizador.tarefas.sort(key=lambda x: datetime.strptime(self.organizador.checkTarefaDecorator(x).data_exata, ("%d/%m/%Y %H:%M:%S.%f")))

        if self.filtro == "Título":
            self.organizador.tarefas.sort(key=lambda x: str.lower(self.organizador.checkTarefaDecorator(x).titulo))
    
    def desfazer_operacao(self) -> None:
        self.organizador.tarefas = [tarefa for tarefa in self.listaTarefasCopia]
        
