"""
Módulo de Inicialização da Aplicação NoteStation
===============================================

Este módulo inicia a aplicação NoteStation.

Módulos importados:
    - os: Módulo que fornece funções para interagir com o sistema operacional,
          permitindo a criação de diretórios e manipulação de caminhos de arquivos.

Constantes:
    - PATH_FILE: Caminho completo para o diretório onde será armazenado o arquivo de lista de tarefas JSON.

Classes:
    - Nenhuma classe é definida neste módulo.

Funções:
    - Nenhuma função é definida neste módulo.

Variáveis:
    - main_app: Instância da classe TelaInicial que inicia a aplicação NoteStation
                com o diretório do arquivo de lista de tarefas JSON fornecido.

Detalhes das constantes e variáveis:
    - PATH_FILE: Caminho completo para o diretório onde será armazenado o arquivo de lista de tarefas JSON.
      - O caminho é construído usando o módulo os e o método os.path.expanduser para expandir o caminho
        inicial usando o diretório do usuário atual.
      - Se o diretório não existir, é criado usando o método os.mkdir.
      - A variável dir recebe o caminho completo para o arquivo de lista de tarefas JSON usando a
        variável PATH_FILE como base.

    - main_app: Instância da classe TelaInicial que inicia a aplicação NoteStation com o diretório do
                arquivo de lista de tarefas JSON fornecido.
      - É criada uma instância da classe TelaInicial passando o caminho completo para o arquivo de lista
        de tarefas JSON como argumento.
      - A função exibir() da instância main_app é chamada para iniciar a aplicação e exibir a tela inicial
        do NoteStation.
"""

import os

from notestation_interfaces import *

PATH_FILE = os.path.expanduser('~\\Documents\\noteStation')

if not os.path.exists(PATH_FILE):
    os.mkdir(PATH_FILE)

dir = os.path.expanduser(PATH_FILE + '\\lista_tarefas.json')

main_app = TelaInicial(dir)

main_app.exibir()