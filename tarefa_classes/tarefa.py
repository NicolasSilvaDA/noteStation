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
        self.concluida = False

    def exibir(self) -> str:
        status = "Concluída" if self.concluida else "Pendente"
        return f' Título: {self.titulo}\n\
Descrição: {self.descricao}\n\
Status: {status}\n\
Data de criação: {self.data_criacao}'
    

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
        return self._tarefa.exibir() + '\n' + tarefa_lembrete
    
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

    def add_tarefa(self, tarefa: Tarefa):
        comando = CriarTarefaCommand(tarefa, self)
        comando.executar()
        self.comandos.append(comando)

    def del_tarefa(self, tarefa: Tarefa):
        comando = ExcluirTarefaCommand(tarefa, self)
        comando.executar()
        self.comandos.append(comando)

    def edit_tarefa(self, tarefa: Tarefa):
        comando = EditarTarefaCommand(tarefa)
        comando.executar()
        self.comandos.append(comando)

    def mark_tarefa(self, tarefa: Tarefa):
        comando = MarcarConcluidaCommand(tarefa)
        comando.executar()
        self.comandos.append(comando)

    def desfazer(self):
        ultimo_comando = self.comandos.pop()
        ultimo_comando.desfazer_operacao()

    def sort_tarefas(self, por_tipo: bool = False, por_data: bool = False, por_prazo: bool = False):
        if por_tipo:
            self.tarefas.sort(key=lambda x: type(x).__name__)

        elif por_data:
            self.tarefas.sort(key=lambda x: x.data_criacao)

        elif por_prazo:
            self.tarefas.sort(key=lambda x: x.prazo)

from tarefa_classes.tarefa_command import *