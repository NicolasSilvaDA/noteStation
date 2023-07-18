"""
Módulo contendo as classes relacionadas à criação, edição e organização de tarefas.

Classes:
    - Tarefa: Classe abstrata que define a estrutura de uma tarefa com o método abstrato "exibir()".
    - TarefaBase: Classe concreta que representa uma tarefa básica com título, descrição, data de criação, data exata, status e um atributo protegido _tarefa.
    - TarefaDecorator: Classe abstrata que serve como base para as classes que decoram as tarefas com funcionalidades adicionais.
    - TarefaComLembrete: Classe concreta que adiciona uma funcionalidade de lembrete a uma tarefa existente.
    - TarefaComPrazo: Classe concreta que adiciona uma funcionalidade de prazo a uma tarefa existente.
    - TarefaOrganizador: Classe que gerencia as tarefas, oferecendo métodos para adicionar, excluir, editar, marcar como concluída e ordenar a lista de tarefas.

Módulos importados:
    - ABC: Módulo do pacote "abc" que fornece as classes e funções para trabalhar com metaprogramação orientada a aspectos.
    - abstractmethod: Decorador para um método abstrato, que deve ser implementado nas classes derivadas.
    - datetime: Módulo padrão do Python que fornece classes para manipulação de datas e horas.
    - date: Classe do módulo datetime que representa uma data (ano, mês e dia).
"""

from abc import ABC, abstractmethod
from datetime import datetime, date

class Tarefa(ABC):
    """
    Classe abstrata que representa uma tarefa.

    Métodos:
        - exibir() -> str: Retorna uma string com as informações da tarefa.
    """
    @abstractmethod
    def exibir() -> str:
        """
        Método abstrato para exibir informações da tarefa.

        Retorna:
            - str: Uma string com as informações da tarefa.
        """
        pass


class TarefaBase(Tarefa):
    """
    Classe que representa uma tarefa base.

    Atributos:
        - titulo (str): O título da tarefa.
        - descricao (str): A descrição da tarefa.
        - data_criacao (str): Data e hora de criação da tarefa (formato: "dd/mm/aaaa HH:MM").
        - data_exata (str): Data e hora exata de criação da tarefa (formato: "dd/mm/aaaa HH:MM:SS.ms").
        - concluida (bool): Indica se a tarefa foi concluída (True) ou não (False).
        - _tarefa (Tarefa): Referência à tarefa base.
    """
    def __init__(self, titulo: str, descricao: str):
        """
        Construtor da classe TarefaBase.

        Parâmetros:
            - titulo (str): O título da tarefa.
            - descricao (str): A descrição da tarefa.
        """
        self.titulo = titulo
        self.descricao = descricao
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.data_exata = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        self.concluida = False
        self._tarefa = None

    def exibir(self) -> str:
        """
        Método para exibir informações da tarefa.

        Retorna:
            - str: Uma string com as informações da tarefa.
        """
        status = "Concluída" if self.concluida else "Pendente"
        return f'Título: {self.titulo}\n\
Descrição: {self.descricao}\n\
Status: {status}\n\
Data de criação: {self.data_criacao}\n'
    

class TarefaDecorator(Tarefa):
    """
    Classe abstrata que representa um decorator de tarefa.

    Atributos:
        - _tarefa (Tarefa): Referência à tarefa decorada.
    """
    def __init__(self, tarefa: Tarefa):
        """
        Construtor da classe TarefaDecorator.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser decorada.
        """
        self._tarefa = tarefa

    @abstractmethod
    def exibir(self) -> str:
        """
        Método abstrato para exibir informações da tarefa decorada.

        Retorna:
            - str: Uma string com as informações da tarefa decorada.
        """
        return self._tarefa.exibir()


class TarefaComLembrete(TarefaDecorator):
    """
    Classe que representa uma tarefa com lembrete.

    Atributos:
        - lembrete (str): O lembrete associado à tarefa.
    """
    
    def __init__(self, tarefa: Tarefa, lembrete: str):
        """
        Construtor da classe TarefaComLembrete.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser decorada.
            - lembrete (str): O lembrete associado à tarefa.
        """
        super().__init__(tarefa)
        self.lembrete = lembrete

    def exibir(self) -> str:
        """
        Método para exibir informações da tarefa com lembrete.

        Retorna:
            - str: Uma string com as informações da tarefa decorada com lembrete.
        """
        tarefa_lembrete = f'Lembrete: {self.lembrete}'
        return self._tarefa.exibir() + tarefa_lembrete
    
    def alterar_lembrete(self, nLembrete) -> None:
        """
        Altera o lembrete associado à tarefa.

        Parâmetros:
            - novo_lembrete (str): O novo lembrete a ser associado à tarefa.
        """
        self.lembrete = nLembrete
    

class TarefaComPrazo(TarefaDecorator):
    """
    Classe que representa uma tarefa com prazo.

    Atributos:
        - prazo (date): O prazo associado à tarefa.
    """
    def __init__(self, tarefa: Tarefa, prazo: date):
        """
        Construtor da classe TarefaComPrazo.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser decorada.
            - prazo (date): O prazo associado à tarefa.
        """
        super().__init__(tarefa)
        self.prazo = prazo

    def exibir(self) -> str:
        """
        Método para exibir informações da tarefa com prazo.

        Retorna:
            - str: Uma string com as informações da tarefa decorada com prazo.
        """
        tarefa_prazo = f'Prazo: {self.prazo}'
        return self._tarefa.exibir() + "\n" +  tarefa_prazo
    
    def atualizar_prazo(self, nPrazo: date):
        """
        Atualiza o prazo associado à tarefa.

        Parâmetros:
            - novo_prazo (date): O novo prazo a ser associado à tarefa.
        """
        self.prazo = nPrazo
    

class TarefaOrganizador:
    """
    Classe que representa um organizador de tarefas.

    Atributos:
        - tarefas (List[Tarefa]): Lista de tarefas no organizador.
        - comandos (List[TarefaCommand]): Lista de comandos realizados no organizador.
    """
    def __init__(self):
        """
        Construtor da classe TarefaOrganizador.
        """
        self.tarefas = []
        self.comandos = []

    def get_tarefa(self, titulo: str):
        """
        Obtém uma tarefa pelo título.

        Parâmetros:
            - titulo (str): O título da tarefa a ser buscada.

        Retorna:
            - Tarefa or None: A tarefa encontrada ou None se não encontrada.
        """
        for tarefa in self.tarefas:
            tarefa_cpy = self.checkTarefaDecorator(tarefa)
            if tarefa_cpy.titulo == titulo:
                return tarefa
        
        return None

    def checkTarefaDecorator(self, tarefa: Tarefa):
        """
        Verifica se a tarefa é um decorator e obtém a tarefa base.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser verificada.

        Retorna:
            - Tarefa: A tarefa base, caso a tarefa seja um decorator.
        """
        if not isinstance(tarefa, TarefaDecorator):
            return tarefa
        
        chTarefa = tarefa._tarefa
        return self.checkTarefaDecorator(chTarefa)

    def add_tarefa(self, tarefa: Tarefa):
        """
        Adiciona uma tarefa ao organizador.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser adicionada.
        """
        comando = CriarTarefaCommand(tarefa, self)
        comando.executar()
        self.comandos.append(comando)

    def del_tarefa(self, tarefa: Tarefa):
        """
        Remove uma tarefa do organizador.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser removida.
        """
        comando = ExcluirTarefaCommand(tarefa, self)
        comando.executar()
        self.comandos.append(comando)

    def edit_tarefa(self, tarefa: Tarefa, nTitulo: str, nDescricao: str, nLembrete: str, nPrazo: str):
        """
        Edita uma tarefa existente no organizador.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser editada.
            - nTitulo (str): O novo título da tarefa.
            - nDescricao (str): A nova descrição da tarefa.
            - nLembrete (str): O novo lembrete da tarefa.
            - nPrazo (str): O novo prazo da tarefa.
        """
        comando = EditarTarefaCommand(tarefa, nTitulo, nDescricao, nLembrete, nPrazo, organizador=self)
        comando.executar()
        self.comandos.append(comando)

    def mark_tarefa(self, tarefa: Tarefa):
        """
        Marca uma tarefa como concluída.

        Parâmetros:
            - tarefa (Tarefa): A tarefa a ser marcada como concluída.
        """
        comando = MarcarConcluidaCommand(tarefa, organizador=self)
        comando.executar()
        self.comandos.append(comando)

    def sort_tarefas(self, filtro: str):
        """
        Ordena a lista de tarefas no organizador.

        Parâmetros:
            - filtro (str): O critério de ordenação das tarefas (por título ou por prazo).
        """
        comando = OrdenarListaTarefasCommand(organizador=self, filtro=filtro)
        comando.executar()
        self.comandos.append(comando)

    def desfazer(self):
        """
        Desfaz a última operação realizada no organizador.
        """
        ultimo_comando = self.comandos.pop()
        ultimo_comando.desfazer_operacao()

        

from tarefa_classes.tarefa_command import *