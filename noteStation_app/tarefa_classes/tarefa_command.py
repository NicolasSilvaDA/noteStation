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
"""

from abc import ABC, abstractmethod
from typing import Optional
from datetime import date, datetime
import copy

from tarefa_classes.tarefa import Tarefa, TarefaOrganizador, TarefaComLembrete, TarefaComPrazo

class TarefaCommand(ABC):
    """
    Classe abstrata que representa um comando relacionado a uma tarefa.

    Atributos:
        - Nenhum atributo na classe abstrata.
    """


    @abstractmethod
    def executar(self):
        """
        Método abstrato para executar o comando.
        """
        pass

    @abstractmethod
    def desfazer_operacao(self):
        """
        Método abstrato para desfazer a operação realizada pelo comando.
        """
        pass


class CriarTarefaCommand(TarefaCommand):
    """
    Classe que representa o comando de criar uma tarefa.

    Atributos:
        - tarefa (Tarefa): A tarefa a ser criada.
        - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será adicionada.
    """
    def __init__(self, tarefa: Tarefa, organizador: TarefaOrganizador):
        """
        Construtor da classe CriarTarefaCommand.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser criada.
            - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será adicionada.
        """
        self.tarefa = tarefa
        self.organizador = organizador

    def executar(self) -> None:
        """
        Executa o comando de criar uma tarefa.
        """
        self.organizador.tarefas.append(self.tarefa)
    
    def desfazer_operacao(self) -> None:
        """
        Desfaz a operação de criação da tarefa.
        """
        self.organizador.tarefas.remove(self.tarefa)


class EditarTarefaCommand(TarefaCommand):
    """
    Classe que representa o comando de editar uma tarefa.

    Atributos:
        - tarefa (Tarefa): A tarefa a ser editada.
        - copiaTarefa (Tarefa): Uma cópia da tarefa original antes da edição.
        - nTitulo (str): O novo título da tarefa.
        - nDescricao (str): A nova descrição da tarefa.
        - nLembrete (Optional[str]): O novo lembrete da tarefa (pode ser None).
        - nPrazo (Optional[date]): O novo prazo da tarefa (pode ser None).
        - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será editada.
    """
    def __init__(self, tarefa: Tarefa, nTitulo: str, nDescricao: str, nLembrete: Optional[str], nPrazo: Optional[date], organizador: TarefaOrganizador):
        """
        Construtor da classe EditarTarefaCommand.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser editada.
            - nTitulo (str): O novo título da tarefa.
            - nDescricao (str): A nova descrição da tarefa.
            - nLembrete (Optional[str]): O novo lembrete da tarefa (pode ser None).
            - nPrazo (Optional[date]): O novo prazo da tarefa (pode ser None).
            - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será editada.
        """
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
        """
        Executa o comando de editar a tarefa.
        """
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
        """
        Desfaz a operação de editar a tarefa, restaurando os valores originais da tarefa.
        """
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
    """
    Classe que representa o comando de excluir uma tarefa.

    Atributos:
        - tarefa (Tarefa): A tarefa a ser excluída.
        - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será excluída.
    """
    def __init__(self, tarefa: Tarefa, organizador: TarefaOrganizador):
        """
        Construtor da classe ExcluirTarefaCommand.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser excluída.
            - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será excluída.
        """
        self.tarefa = tarefa
        self.organizador = organizador

    def executar(self) -> None:
        """
        Executa o comando de excluir a tarefa.
        """
        self.organizador.tarefas.remove(self.tarefa)

    def desfazer_operacao(self) -> None:
        """
        Desfaz a operação de exclusão da tarefa, adicionando a tarefa de volta ao organizador.
        """
        self.organizador.tarefas.append(self.tarefa)


class MarcarConcluidaCommand(TarefaCommand):
    """
    Classe que representa o comando de marcar uma tarefa como concluída.

    Atributos:
        - tarefa (Tarefa): A tarefa a ser marcada como concluída.
        - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será marcada como concluída.
    """
    def __init__(self, tarefa: Tarefa, organizador: TarefaOrganizador):
        """
        Construtor da classe MarcarConcluidaCommand.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser marcada como concluída.
            - organizador (TarefaOrganizador): O organizador de tarefas onde a tarefa será marcada como concluída.
        """
        self.tarefa = tarefa
        self.organizador = organizador

    def executar(self) -> None:
        """
        Executa o comando de marcar a tarefa como concluída.
        """
        tarefa = self.organizador.checkTarefaDecorator(self.tarefa)
        tarefa.concluida = True

    def desfazer_operacao(self) -> None:
        """
        Desfaz a operação de marcar a tarefa como concluída, marcando a tarefa como pendente novamente.
        """
        tarefa = self.organizador.checkTarefaDecorator(self.tarefa)
        tarefa.concluida = False

class OrdenarListaTarefasCommand(TarefaCommand):
    """
    Classe que representa o comando de ordenar a lista de tarefas.

    Atributos:
        - listaTarefasCopia (List[Tarefa]): Uma cópia da lista de tarefas original antes da ordenação.
        - organizador (TarefaOrganizador): O organizador de tarefas cuja lista será ordenada.
        - filtro (str): O critério de ordenação (pode ser "Data de criação", "Tipo de tarefa" ou "Título").
    """
    def __init__(self, organizador: TarefaOrganizador, filtro: str):
        """
        Construtor da classe OrdenarListaTarefasCommand.

        Parâmetros:
            - organizador (TarefaOrganizador): O organizador de tarefas cuja lista será ordenada.
            - filtro (str): O critério de ordenação (pode ser "Data de criação", "Tipo de tarefa" ou "Título").
        """
        self.listaTarefasCopia = copy.copy(organizador.tarefas)
        self.organizador = organizador
        self.filtro = filtro

    def executar(self) -> None:
        """
        Executa o comando de ordenar a lista de tarefas.
        """
        if self.filtro == "Data de criação":
            self.organizador.tarefas.sort(key=lambda x: datetime.strptime(self.organizador.checkTarefaDecorator(x).data_exata, ("%d/%m/%Y %H:%M:%S.%f")))

        if self.filtro == "Tipo de tarefa":
            self.organizador.tarefas.sort(key=lambda x:self.organizador.checkTarefaDecorator(x).__class__.__name__)

        if self.filtro == "Título":
            self.organizador.tarefas.sort(key=lambda x: str.lower(self.organizador.checkTarefaDecorator(x).titulo))
    
    def desfazer_operacao(self) -> None:
        """
        Desfaz a operação de ordenar a lista de tarefas, restaurando a lista de tarefas para o estado original.
        """
        self.organizador.tarefas = [tarefa for tarefa in self.listaTarefasCopia]
        
