"""
Módulo contendo a interface principal do aplicativo "NoteStation".

Classes:
    - TelaInicial: Classe responsável por representar a tela inicial do aplicativo "NoteStation" e interagir com o usuário.

Módulos importados:
    - TelaInicial: Classe da interface principal do aplicativo "NoteStation" importada do módulo "notestation_interfaces.interface_notestation".

Atributos:
    - Nenhum atributo relevante é definido na classe.

Métodos:
    - TelaInicial.__init__(dir): Método construtor da classe TelaInicial, que recebe o diretório do arquivo de armazenamento de tarefas.
    - TelaInicial.carregar_arquivo(): Método que carrega as tarefas do arquivo de armazenamento.
    - TelaInicial.exibir(): Método que exibe a interface principal do aplicativo.
    - TelaInicial.visualizar_tarefa(Sender): Método que exibe detalhes de uma tarefa específica.
    - TelaInicial.editar_tarefa_window(Sender): Método que exibe a janela de edição de uma tarefa.
    - TelaInicial.editar_tarefa(Sender): Método que edita uma tarefa com base nos dados fornecidos pelo usuário.
    - TelaInicial.marcar_concluida(Sender): Método que marca uma tarefa como concluída.
    - TelaInicial.atualizar_lista(): Método que atualiza a lista de tarefas exibida na interface e salva as alterações no arquivo de armazenamento.
    - TelaInicial.exibir_lembrete(): Método que exibe o campo de lembrete ao criar ou editar uma tarefa.
    - TelaInicial.exibir_prazo(): Método que exibe o campo de prazo ao criar ou editar uma tarefa.
    - TelaInicial.checar_tarefa(titulo): Método que verifica se uma tarefa com um determinado título já existe.
    - TelaInicial.criar_tarefa_popup(): Método que exibe a janela para criar uma nova tarefa.
    - TelaInicial.criar_tarefa(): Método que cria uma nova tarefa com base nos dados fornecidos pelo usuário.
    - TelaInicial.excluir_tarefa(Sender): Método que exclui uma tarefa da lista.
    - TelaInicial.desfazer_operacao(): Método que desfaz a última operação realizada.
    - TelaInicial.ordenar_lista(Sender): Método que ordena a lista de tarefas com base no filtro selecionado pelo usuário.
"""

from notestation_interfaces.interface_notestation import (
    TelaInicial
)