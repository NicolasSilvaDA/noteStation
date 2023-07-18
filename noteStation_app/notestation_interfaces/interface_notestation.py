"""
Módulo para a classe TelaInicial e funcionalidades relacionadas

Este módulo contém a classe TelaInicial, responsável por exibir a interface gráfica principal do programa utilizando a biblioteca dearpygui. Também inclui funcionalidades para carregar tarefas a partir de um arquivo JSON, criar, editar, marcar como concluída e excluir tarefas, além de realizar ordenações na lista de tarefas exibida na interface gráfica.

Classes:
    - TelaInicial: Classe que representa a tela inicial do programa e gerencia as tarefas e a interação com o usuário.

Módulos importados:
    - dearpygui.dearpygui: Módulo da biblioteca dearpygui que é utilizada para criar a interface gráfica.
    - sys: Módulo padrão do Python que fornece acesso a algumas variáveis usadas ou mantidas pelo interpretador e a funções que interagem fortemente com o interpretador.
    - os: Módulo padrão do Python que fornece uma maneira de usar funcionalidades dependentes do sistema operacional.
    - json: Módulo padrão do Python que fornece funções para trabalhar com dados JSON.

    - tarefa_classes: Módulo contendo as classes TarefaBase, TarefaComLembrete, TarefaComPrazo, TarefaOrganizador e suas fábricas.
    - gerenciamento_arquivos: Módulo contendo o Encoder personalizado TarefaEncoder para serialização das tarefas em formato JSON.
"""

import dearpygui.dearpygui as dpg

import sys
import os
import json

diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(diretorio_pai)

from tarefa_classes import *
from gerenciamento_arquivos import *


class TelaInicial:
    """
    Classe responsável por representar a tela inicial do programa e gerenciar as tarefas e a interação com o usuário.

    Atributos:
        - organizador (TarefaOrganizador): Instância da classe TarefaOrganizador que gerencia as tarefas do programa.
        - tPrioridade (TarefaComPrioridadeFactory): Instância da classe TarefaComPrioridadeFactory utilizada para criar tarefas com prioridade.
        - tTrabalho (TarefaTrabalhoFactory): Instância da classe TarefaTrabalhoFactory utilizada para criar tarefas de trabalho.
        - dir (str): Diretório do arquivo JSON usado para armazenar as tarefas.

    Métodos:
        - carregar_arquivo()
        - exibir()
        - visualizar_tarefa(Sender)
        - editar_tarefa_window(Sender)
        - editar_tarefa(Sender)
        - marcar_concluida(Sender)
        - atualizar_lista()
        - exibir_lembrete()
        - exibir_prazo()
        - checar_tarefa(titulo)
        - criar_tarefa_popup()
        - criar_tarefa()
        - excluir_tarefa(Sender)
        - desfazer_operacao()
        - ordenar_lista(Sender)
    """
    def __init__(self, dir):
        """
        Inicializa a classe TelaInicial.

        Atributos:
            - dir (str): O diretório do arquivo JSON usado para armazenar as tarefas.
        """
        self.organizador = TarefaOrganizador()
        self.tPrioridade = TarefaComPrioridadeFactory()
        self.tTrabalho = TarefaTrabalhoFactory()
        self.dir = dir

        self.carregar_arquivo()

    def carregar_arquivo(self):
        """
        Carrega as tarefas a partir do arquivo JSON especificado no atributo "dir" e as adiciona ao organizador.
        """
        if os.path.exists(self.dir):
            with open(self.dir, "r", encoding='UTF-8') as arquivo:
                lista_tarefas = json.load(arquivo)
                json_to_tarefas = []

                for tarefa_id in lista_tarefas:
                    tarefa_obj = lista_tarefas[tarefa_id]

                    tarefa = None
                    if tarefa_obj['prioridade'] == True:
                        tarefa = self.tPrioridade.criar_tarefa(tarefa_obj['titulo'], tarefa_obj['descricao'])
                    else:
                        tarefa = self.tTrabalho.criar_tarefa(tarefa_obj['titulo'], tarefa_obj['descricao'])
                    
                    tarefa.data_criacao = tarefa_obj['data_criacao']
                    tarefa.data_exata = tarefa_obj['data_exata']
                    tarefa.concluida = tarefa_obj['concluida']
                    tarefa._tarefa = tarefa_obj['_tarefa']

                    if tarefa_obj['lembrete']:
                        tarefa = TarefaComLembrete(tarefa, tarefa_obj['lembrete'])
                    
                    if tarefa_obj['prazo']:
                        tarefa = TarefaComPrazo(tarefa, tarefa_obj['prazo'])
                    
                    json_to_tarefas.append(tarefa)
                
                self.organizador.tarefas = json_to_tarefas
        else:
            with open(self.dir, "w", encoding='UTF-8') as arquivo:
                arquivo.write("")

    def exibir(self):
        """
        Exibe a interface gráfica principal do programa, mostrando a lista de tarefas e opções para interagir com elas.
        """
        self.titulos = [self.organizador.checkTarefaDecorator(tarefa).titulo for tarefa in self.organizador.tarefas]


        dpg.create_context()
        dpg.create_viewport(title="noteStation", max_width=700, max_height=400, min_width=700, min_height=400)
        dpg.setup_dearpygui()

        with dpg.window(label="noteStation" , width=700, height=400, no_title_bar=True, no_resize=True, no_move=True, tag="PrimWindow"):
            # Listbox para exibir as tarefas
            with dpg.group():
                self.listbox = dpg.add_listbox(label="Tarefas", items=self.titulos, num_items=16, width=500)

                with dpg.popup(dpg.last_item(), max_size=(150, 15)):
                    dpg.add_button(label="Editar tarefa", width=135, callback=self.editar_tarefa_window, drag_callback=self.listbox)

                    dpg.add_button(label="Visualizar tarefa", width=135, tag="VisuButton", callback=self.visualizar_tarefa, drag_callback=self.listbox)

                    dpg.add_button(label="Concluir tarefa", width=135, tag="MarkTarefa", callback=self. marcar_concluida, drag_callback=self.listbox)


                with dpg.group(horizontal=True):
                    dpg.add_button(label="Adicionar tarefa", tag="openPopUp", callback=self.criar_tarefa_popup)

                    dpg.add_button(label="Excluir tarefa", callback=self.excluir_tarefa, drag_callback=self.listbox)

                    dpg.add_button(label="Desfazer", callback=self.desfazer_operacao)

                    dpg.add_button(label="Ordenar", tag="OrdenarButton")

                    with dpg.popup(parent="OrdenarButton", mousebutton=dpg.mvMouseButton_Left, tag="OrdenarPopUp", min_size=(130, 60)):
                        dpg.add_button(label="Título", callback=self.ordenar_lista, width=120)

                        dpg.add_button(label="Data de criação", callback=self.ordenar_lista, width=120)

                        dpg.add_button(label="Tipo de tarefa", callback=self.ordenar_lista, width=120)

        dpg.show_viewport()
        dpg.set_primary_window("PrimWindow", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def visualizar_tarefa(self, Sender):
        """
        Exibe os detalhes de uma tarefa em uma janela popup quando o usuário clica em "Visualizar tarefa".

        Atributos:
            - Sender: O objeto que enviou o sinal de clique.
        """
        tarefa_titulo = dpg.get_value(dpg.get_item_drag_callback(Sender))
        tarefa = self.organizador.get_tarefa(tarefa_titulo)

        if dpg.does_item_exist("Visu"):
            dpg.set_value("VisuText", tarefa.exibir())
            dpg.show_item("Visu")
        else:
            visu_popup = dpg.window(tag="Visu", label="Detalhes da tarefa", autosize=True)
            with visu_popup:
                dpg.add_text(tarefa.exibir(), tag="VisuText")

    def editar_tarefa_window(self, Sender):
        """
        Abre uma janela popup para editar os atributos de uma tarefa quando o usuário clica em "Editar tarefa".

        Atributos:
            - Sender: O objeto que enviou o sinal de clique.
        """
        tarefa_titulo = dpg.get_value(dpg.get_item_drag_callback(Sender))
        tarefa = self.organizador.get_tarefa(tarefa_titulo)
        tarefa = self.organizador.checkTarefaDecorator(tarefa)

        if dpg.does_item_exist("Edit"):
            dpg.configure_item("att_titulo", default_value=tarefa.titulo)
            dpg.configure_item("att_descricao", default_value=tarefa.descricao)
            dpg.configure_item("att_lembrete", default_value="")
            dpg.show_item("Edit")
        else:
            edit_window = dpg.window(tag="Edit", label="Atualização de tarefa", autosize=True)

            with edit_window:
                dpg.add_input_text(label="Título", default_value=tarefa.titulo, tag="att_titulo")

                dpg.add_input_text(label="Descrição", default_value=tarefa.descricao, tag="att_descricao")

                dpg.add_input_text(label="Lembrete", tag="att_lembrete")

                dpg.add_date_picker(label="Prazo", tag="att_prazo")

                dpg.add_button(label="Atualizar tarefa", callback=self.editar_tarefa, tag="AtualizarButton", drag_callback=self.listbox)

    def editar_tarefa(self, Sender):
        """
        Atualiza os atributos de uma tarefa após o usuário realizar as alterações na janela de edição.

        Atributos:
            - Sender: O objeto que enviou o sinal de clique.
        """
        tarefa_titulo = dpg.get_value(dpg.get_item_drag_callback(Sender))
        tarefa = self.organizador.get_tarefa(tarefa_titulo)

        titulo = dpg.get_value("att_titulo")
        descricao = dpg.get_value("att_descricao")
        lembrete = dpg.get_value("att_lembrete")

        prazo = dpg.get_value("att_prazo")
        prazo_text = f'{prazo["month_day"]}/{prazo["month"] + 1}/{prazo["year"] + 1900}'

        self.organizador.edit_tarefa(tarefa, titulo, descricao, lembrete, prazo_text)

        self.atualizar_lista()

    def marcar_concluida(self, Sender):
        """
        Marca uma tarefa como concluída e exibe uma mensagem em uma janela popup.

        Atributos:
            - Sender: O objeto que enviou o sinal de clique.
        """
        tarefa_titulo = dpg.get_value(dpg.get_item_drag_callback(Sender))
        tarefa = self.organizador.get_tarefa(tarefa_titulo)

        self.organizador.mark_tarefa(tarefa)

        mark_popup = dpg.window(tag="Mark", label="Tarefa concluída", autosize=True)
        with mark_popup:
            dpg.add_text(f'Tarefa {tarefa_titulo} concluída!')
    
    def atualizar_lista(self):
        """
        Atualiza a lista de tarefas exibida na interface gráfica após modificações (adicionar, editar, excluir tarefas).
        """
        self.titulos = [self.organizador.checkTarefaDecorator(tarefa).titulo for tarefa in self.organizador.tarefas]
        dpg.configure_item(self.listbox, items=self.titulos)

        tarefas_to_json = {}
        count = 0

        with open(self.dir, "w", encoding='UTF-8') as arquivo:
            for tarefa in self.organizador.tarefas:
                tarefa_json = json.dumps(
                    tarefa,
                    cls=TarefaEncoder
                )
                
                tarefa_json = json.loads(tarefa_json)

                tarefas_to_json[count] = tarefa_json
                count += 1

            json.dump(
                tarefas_to_json,
                arquivo,
                ensure_ascii=False
            )
        
    def exibir_lembrete(self):
        """
        Exibe ou oculta o campo de lembrete dependendo do valor do checkbox "Lembrete".
        """
        check = dpg.get_value("tarefa_lembrete_check")
        dpg.configure_item("lembrete_input", show=check)
    
    def exibir_prazo(self):
        """
        Exibe ou oculta o campo de prazo dependendo do valor do checkbox "Prazo".
        """
        check = dpg.get_value("tarefa_prazo_check")
        dpg.configure_item("prazo_input", show=check)

    def checar_tarefa(self, titulo):
        """
        Verifica se o título da tarefa já existe na lista de títulos de tarefas exibida na interface gráfica.

        Atributos:
            - titulo (str): O título da tarefa a ser verificado.

        Retorna:
            - bool: True se o título não existir, False caso contrário.
        """
        for tar_titulo in self.titulos:
            if tar_titulo == titulo:
                    return False

        return True

    def criar_tarefa_popup(self):
        """
        Abre uma janela popup para criar uma nova tarefa quando o usuário clica em "Adicionar tarefa".
        """
        pop_up_criar = dpg.popup(parent="openPopUp", modal=True, tag="popUpCriar", mousebutton=dpg.mvMouseButton_Left)

        with pop_up_criar:
            dpg.add_checkbox(label="Prioridade?", tag="tarefa_prioridade_check")

            dpg.add_input_text(label="Título", tag="tarefa_titulo")
            dpg.add_input_text(label="Descrição", tag="tarefa_descricao")

            dpg.add_checkbox(label="Lembrete", tag="tarefa_lembrete_check", callback=self.exibir_lembrete)
            dpg.add_input_text(tag="lembrete_input", show=False)

            dpg.add_checkbox(label="Prazo", tag="tarefa_prazo_check", callback=self.exibir_prazo)

            dpg.add_date_picker(tag="prazo_input", show=False)

            dpg.add_button(label="Adicionar", tag="adicionar_button", callback=self.criar_tarefa)

    def criar_tarefa(self):
        """
        Cria uma nova tarefa com os atributos especificados pelo usuário na janela de criação e a adiciona ao organizador.
        """
        titulo = dpg.get_value("tarefa_titulo")
        descricao = dpg.get_value("tarefa_descricao")
        
        check_titulo = self.checar_tarefa(titulo)

        if check_titulo:
            tarefa = None

            if dpg.get_value("tarefa_prioridade_check") == True:
                tarefa = self.tPrioridade.criar_tarefa(titulo, descricao)
            else:
                tarefa = self.tTrabalho.criar_tarefa(titulo, descricao)

            print(tarefa.__class__.__name__)

            lembrete_check = dpg.get_value("tarefa_lembrete_check")
            prazo_check = dpg.get_value("tarefa_prazo_check")

            if lembrete_check:
                lembrete = dpg.get_value("lembrete_input")
                tarefa = TarefaComLembrete(tarefa, lembrete)

            if prazo_check:

                prazo = dpg.get_value("prazo_input")
                prazo_text = f'{prazo["month_day"]}/{prazo["month"] + 1}/{prazo["year"] + 1900}'
                
                tarefa = TarefaComPrazo(tarefa, prazo_text)

            self.organizador.add_tarefa(tarefa)
            self.atualizar_lista()
            return

    def excluir_tarefa(self, Sender):
        """
        Exclui uma tarefa selecionada na lista quando o usuário clica em "Excluir tarefa".

        Atributos:
            - Sender: O objeto que enviou o sinal de clique.
        """
        item_titulo = dpg.get_value(dpg.get_item_drag_callback(Sender))

        for tarefa in self.organizador.tarefas:
            tarefa_ch = self.organizador.checkTarefaDecorator(tarefa)

            if tarefa_ch.titulo == item_titulo:
                self.organizador.del_tarefa(tarefa)
                print(f'Tarefa removida')
                self.atualizar_lista()
                break
        else:
            print(f'Tarefa não encontrada')

    def desfazer_operacao(self):
        """
        Desfaz a última operação realizada pelo usuário (adicionar, editar, excluir, concluir e ordenar).
        """
        self.organizador.desfazer()
        self.atualizar_lista()

    def ordenar_lista(self, Sender):
        """
        Ordena a lista de tarefas exibida na interface gráfica de acordo com o filtro especificado (título, data de criação ou tipo de tarefa).

        Atributos:
            - Sender: O objeto que enviou o sinal de clique.
        """
        filtro = dpg.get_item_configuration(Sender)['label']
        
        self.organizador.sort_tarefas(filtro)

        self.atualizar_lista()
