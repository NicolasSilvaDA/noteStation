"""
Módulo contendo a classe TarefaEncoder para codificação personalizada de tarefas em formato JSON.

Módulos importados:
- Nenhum módulo é importado.

Classe:
- TarefaEncoder: Classe que herda de json.JSONEncoder e fornece a funcionalidade de codificação personalizada para tarefas em formato JSON.

Métodos:
- TarefaEncoder.default(obj): Método que converte um objeto em uma representação serializável em JSON.
  - obj: O objeto a ser codificado em JSON.

Detalhes dos atributos e métodos:
- TarefaEncoder.default(obj): Método sobrescrito da classe JSONEncoder que é chamado para objetos não serializáveis padrão.
  - O método verifica o tipo da tarefa passada como argumento e cria um dicionário contendo as informações da tarefa para serem codificadas em JSON.
  - A prioridade da tarefa é verificada e definida como True caso seja uma TarefaComPrioridade, caso contrário, é definida como False.
  - As informações de título, descrição, data de criação, data exata, conclusão, tarefa base (_tarefa), lembrete e prazo são armazenadas no dicionário.
  - O dicionário é retornado como a representação serializável da tarefa em formato JSON.
"""

from gerenciamento_arquivos.json_tarefa_encoder import (
    TarefaEncoder
)