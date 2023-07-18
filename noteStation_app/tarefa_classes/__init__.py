"""
Módulo tarefa_classes

Este módulo contém classes relacionadas a tarefas, organização de tarefas e comandos para manipular as tarefas.

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