import dearpygui.dearpygui as dpg

import sys
import os
import json

diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(diretorio_pai)

from tarefa_classes import *
from gerenciamento_arquivos import *


class TelaInicial:
    def __init__(self, dir):
        self.organizador = TarefaOrganizador()
        self.tPrioridade = TarefaComPrioridadeFactory()
        self.tTrabalho = TarefaTrabalhoFactory()
        self.dir = dir

        self.carregar_arquivo()

    def carregar_arquivo(self):
        if os.path.exists(self.dir):
            with open(self.dir, "r", encoding='UTF-8') as arquivo:
                lista_tarefas = json.load(arquivo)
                json_to_tarefas = []

                for tarefa_id in lista_tarefas:
                    tarefa_obj = lista_tarefas[tarefa_id]
                    print(tarefa_obj)

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
        tarefa_titulo = dpg.get_value(dpg.get_item_drag_callback(Sender))
        tarefa = self.organizador.get_tarefa(tarefa_titulo)

        self.organizador.mark_tarefa(tarefa)

        mark_popup = dpg.window(tag="Mark", label="Tarefa concluída", autosize=True)
        with mark_popup:
            dpg.add_text(f'Tarefa {tarefa_titulo} concluída!')
    
    def atualizar_lista(self):
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
        check = dpg.get_value("tarefa_lembrete_check")
        dpg.configure_item("lembrete_input", show=check)
    
    def exibir_prazo(self):
        check = dpg.get_value("tarefa_prazo_check")
        dpg.configure_item("prazo_input", show=check)

    def checar_tarefa(self, titulo):
        for tar_titulo in self.titulos:
            if tar_titulo == titulo:
                    return False

        return True

    def criar_tarefa_popup(self):
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
        self.organizador.desfazer()
        self.atualizar_lista()

    def ordenar_lista(self, Sender):
        filtro = dpg.get_item_configuration(Sender)['label']
        
        self.organizador.sort_tarefas(filtro)

        self.atualizar_lista()
