"""
Módulo tarefa_classes

Este módulo contém classes relacionadas a tarefas, organização de tarefas e comandos para manipular as tarefas.

Classes:
    - TarefaBase: Classe abstrata que representa uma tarefa básica.
    - TarefaComLembrete: Classe que representa uma tarefa com lembrete.
    - TarefaComPrazo: Classe que representa uma tarefa com prazo.
    - TarefaOrganizador: Classe que representa um organizador de tarefas.

    - TarefaComPrioridadeFactory: Classe que representa uma fábrica de tarefas de trabalho.
    - TarefaTrabalhoFactory: Classe que representa uma fábrica de tarefas com prioridade.

    - CriarTarefaCommand: Classe que representa o comando de criar uma tarefa.
    - ExcluirTarefaCommand: Classe que representa o comando de excluir uma tarefa.
    - EditarTarefaCommand: Classe que representa o comando de editar uma tarefa.
    - MarcarConcluidaCommand: Classe que representa o comando de marcar uma tarefa como concluída.

Módulos importados:
    - tarefa_classes.tarefa: Módulo que contém as classes TarefaBase, TarefaComLembrete, TarefaComPrazo e TarefaOrganizador.
    - tarefa_classes.tarefa_factory: Módulo que contém as classes TarefaComPrioridadeFactory e TarefaTrabalhoFactory.
    - tarefa_classes.tarefa_command: Módulo que contém as classes CriarTarefaCommand, ExcluirTarefaCommand, EditarTarefaCommand e MarcarConcluidaCommand.
"""

from tarefa_classes.tarefa import (
    TarefaBase,
    TarefaComLembrete,
    TarefaComPrazo,
    TarefaOrganizador
)

from tarefa_classes.tarefa_factory import (
    TarefaComPrioridadeFactory,
    TarefaTrabalhoFactory
)

from tarefa_classes.tarefa_command import (
    CriarTarefaCommand,
    ExcluirTarefaCommand,
    EditarTarefaCommand,
    MarcarConcluidaCommand
)