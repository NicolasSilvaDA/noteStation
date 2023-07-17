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

Atributos:
- TarefaBase.titulo: String representando o título da tarefa.
- TarefaBase.descricao: String representando a descrição da tarefa.
- TarefaBase.data_criacao: String representando a data de criação da tarefa no formato "dia/mês/ano hora:minuto".
- TarefaBase.data_exata: String representando a data exata da tarefa no formato "dia/mês/ano hora:minuto:segundo.microsegundo".
- TarefaBase.concluida: Booleano indicando se a tarefa está concluída (True) ou pendente (False).
- TarefaBase._tarefa: Atributo protegido que permite o acesso à tarefa original em caso de uso de decorators.

Métodos:
- TarefaBase.exibir(): Método concreto que retorna uma string formatada com as informações da tarefa.

- TarefaComLembrete.lembrete: String representando o lembrete da tarefa.
- TarefaComLembrete.alterar_lembrete(nLembrete): Método para atualizar o lembrete da tarefa com um novo valor.

- TarefaComPrazo.prazo: Objeto date representando o prazo da tarefa.
- TarefaComPrazo.atualizar_prazo(nPrazo): Método para atualizar o prazo da tarefa com um novo valor.

- TarefaOrganizador.tarefas: Lista de tarefas gerenciadas pelo organizador.
- TarefaOrganizador.comandos: Lista de comandos executados pelo organizador (para desfazer operações).
- TarefaOrganizador.get_tarefa(titulo): Retorna a tarefa com o título especificado ou None se não encontrada.
- TarefaOrganizador.checkTarefaDecorator(tarefa): Verifica se a tarefa é um decorator e retorna a tarefa base.
- TarefaOrganizador.add_tarefa(tarefa): Adiciona uma nova tarefa ao organizador.
- TarefaOrganizador.del_tarefa(tarefa): Exclui uma tarefa do organizador.
- TarefaOrganizador.edit_tarefa(tarefa, nTitulo, nDescricao, nLembrete, nPrazo): Edita os atributos de uma tarefa existente.
- TarefaOrganizador.mark_tarefa(tarefa): Marca uma tarefa como concluída.
- TarefaOrganizador.sort_tarefas(filtro): Ordena a lista de tarefas exibida na interface gráfica de acordo com o filtro especificado.
- TarefaOrganizador.desfazer(): Desfaz a última operação realizada pelo usuário (adicionar, editar ou excluir tarefa).
"""

from abc import ABC, abstractmethod
from datetime import datetime, date

class Tarefa(ABC):

    @abstractmethod
    def exibir() -> str:
        pass


class TarefaBase(Tarefa):
    def __init__(self, titulo: str, descricao: str):
        self.titulo = titulo
        self.descricao = descricao
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.data_exata = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        self.concluida = False
        self._tarefa = None

    def exibir(self) -> str:
        status = "Concluída" if self.concluida else "Pendente"
        return f'Título: {self.titulo}\n\
Descrição: {self.descricao}\n\
Status: {status}\n\
Data de criação: {self.data_criacao}\n'
    

class TarefaDecorator(Tarefa):
    def __init__(self, tarefa: Tarefa):
        self._tarefa = tarefa

    @abstractmethod
    def exibir(self) -> str:
        return self._tarefa.exibir()


class TarefaComLembrete(TarefaDecorator):
    def __init__(self, tarefa: Tarefa, lembrete: str):
        super().__init__(tarefa)
        self.lembrete = lembrete

    def exibir(self) -> str:
        tarefa_lembrete = f'Lembrete: {self.lembrete}'
        return self._tarefa.exibir() + tarefa_lembrete
    
    def alterar_lembrete(self, nLembrete) -> None:
        self.lembrete = nLembrete
    

class TarefaComPrazo(TarefaDecorator):
    def __init__(self, tarefa: Tarefa, prazo: date):
        super().__init__(tarefa)
        self.prazo = prazo

    def exibir(self) -> str:
        tarefa_prazo = f'Prazo: {self.prazo}'
        return self._tarefa.exibir() + "\n" +  tarefa_prazo
    
    def atualizar_prazo(self, nPrazo: date):
        self.prazo = nPrazo
    

class TarefaOrganizador:
    def __init__(self):
        self.tarefas = []
        self.comandos = []

    def get_tarefa(self, titulo: str):
        for tarefa in self.tarefas:
            tarefa_cpy = self.checkTarefaDecorator(tarefa)
            if tarefa_cpy.titulo == titulo:
                return tarefa
        
        return None

    def checkTarefaDecorator(self, tarefa: Tarefa):
        if not isinstance(tarefa, TarefaDecorator):
            return tarefa
        
        chTarefa = tarefa._tarefa
        return self.checkTarefaDecorator(chTarefa)

    def add_tarefa(self, tarefa: Tarefa):
        comando = CriarTarefaCommand(tarefa, self)
        comando.executar()
        self.comandos.append(comando)

    def del_tarefa(self, tarefa: Tarefa):
        comando = ExcluirTarefaCommand(tarefa, self)
        comando.executar()
        self.comandos.append(comando)

    def edit_tarefa(self, tarefa: Tarefa, nTitulo: str, nDescricao: str, nLembrete: str, nPrazo: str):
        comando = EditarTarefaCommand(tarefa, nTitulo, nDescricao, nLembrete, nPrazo, organizador=self)
        comando.executar()
        self.comandos.append(comando)

    def mark_tarefa(self, tarefa: Tarefa):
        comando = MarcarConcluidaCommand(tarefa, organizador=self)
        comando.executar()
        self.comandos.append(comando)

    def sort_tarefas(self, filtro: str):
        comando = OrdenarListaTarefasCommand(organizador=self, filtro=filtro)
        comando.executar()
        self.comandos.append(comando)

    def desfazer(self):
        ultimo_comando = self.comandos.pop()
        ultimo_comando.desfazer_operacao()

        

from tarefa_classes.tarefa_command import *