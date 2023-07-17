"""
Módulo contendo classes relacionadas a comandos para manipulação de tarefas e seus estados.

Classes:
- TarefaCommand: Classe abstrata que define a estrutura de um comando para manipular tarefas, com os métodos abstratos "executar()" e "desfazer_operacao()".
- CriarTarefaCommand: Classe concreta que implementa um comando para criar uma nova tarefa.
- EditarTarefaCommand: Classe concreta que implementa um comando para editar uma tarefa existente.
- ExcluirTarefaCommand: Classe concreta que implementa um comando para excluir uma tarefa.
- MarcarConcluidaCommand: Classe concreta que implementa um comando para marcar uma tarefa como concluída.
- OrdenarListaTarefasCommand: Classe concreta que implementa um comando para ordenar a lista de tarefas.

Módulos importados:
- ABC: Módulo do pacote "abc" que fornece as classes e funções para trabalhar com metaprogramação orientada a aspectos.
- abstractmethod: Decorador para um método abstrato, que deve ser implementado nas classes derivadas.
- Optional: Tipo de dado para indicar que um parâmetro pode ser do tipo especificado ou None.
- date: Tipo de dado que representa uma data.
- datetime: Tipo de dado que representa uma data e hora.
- copy: Módulo que fornece funções para criar cópias de objetos.

Atributos:
- Nenhum atributo relevante é definido nas classes.

Métodos:
- TarefaCommand.executar(): Método abstrato que executa o comando em uma tarefa.
- TarefaCommand.desfazer_operacao(): Método abstrato que desfaz a operação realizada pelo comando.

- CriarTarefaCommand.__init__(tarefa, organizador): Método construtor da classe CriarTarefaCommand, que recebe uma tarefa a ser criada e o organizador de tarefas.
- CriarTarefaCommand.executar(): Método que executa o comando de criação de tarefa.
- CriarTarefaCommand.desfazer_operacao(): Método que desfaz a operação de criação de tarefa.

- EditarTarefaCommand.__init__(tarefa, nTitulo, nDescricao, nLembrete, nPrazo, organizador): Método construtor da classe EditarTarefaCommand, que recebe os dados para editar uma tarefa, a tarefa original e o organizador de tarefas.
- EditarTarefaCommand.executar(): Método que executa o comando de edição de tarefa.
- EditarTarefaCommand.desfazer_operacao(): Método que desfaz a operação de edição de tarefa.

- ExcluirTarefaCommand.__init__(tarefa, organizador): Método construtor da classe ExcluirTarefaCommand, que recebe a tarefa a ser excluída e o organizador de tarefas.
- ExcluirTarefaCommand.executar(): Método que executa o comando de exclusão de tarefa.
- ExcluirTarefaCommand.desfazer_operacao(): Método que desfaz a operação de exclusão de tarefa.

- MarcarConcluidaCommand.__init__(tarefa, organizador): Método construtor da classe MarcarConcluidaCommand, que recebe a tarefa a ser marcada como concluída e o organizador de tarefas.
- MarcarConcluidaCommand.executar(): Método que executa o comando de marcação de tarefa como concluída.
- MarcarConcluidaCommand.desfazer_operacao(): Método que desfaz a operação de marcação de tarefa como concluída.

- OrdenarListaTarefasCommand.__init__(organizador, filtro): Método construtor da classe OrdenarListaTarefasCommand, que recebe o organizador de tarefas e o filtro de ordenação.
- OrdenarListaTarefasCommand.executar(): Método que executa o comando de ordenação da lista de tarefas.
- OrdenarListaTarefasCommand.desfazer_operacao(): Método que desfaz a operação de ordenação da lista de tarefas.
"""

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

        if self.filtro == "Tipo de tarefa":
            self.organizador.tarefas.sort(key=lambda x:self.organizador.checkTarefaDecorator(x).__class__.__name__)

        if self.filtro == "Título":
            self.organizador.tarefas.sort(key=lambda x: str.lower(self.organizador.checkTarefaDecorator(x).titulo))
    
    def desfazer_operacao(self) -> None:
        self.organizador.tarefas = [tarefa for tarefa in self.listaTarefasCopia]
        
