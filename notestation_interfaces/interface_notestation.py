import dearpygui.dearpygui as dpg

from datetime import datetime, date
import sys
import os

diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(diretorio_pai)

from tarefa_classes import *


class TelaInicial:
    def __init__(self, organizador):
        self.organizador = organizador

    def exibir(self):
        self.titulos = [organizador.checkTarefaDecorator(tarefa).titulo for tarefa in self.organizador.tarefas]


        dpg.create_context()
        dpg.create_viewport(title="noteStation", max_width=500, max_height=390, min_width=500, min_height=390)
        dpg.setup_dearpygui()

        with dpg.window(label="noteStation" , width=600, height=500, no_title_bar=True, no_resize=True, no_move=True, tag="PrimWindow"):
            # Listbox para exibir as tarefas
            with dpg.group():
                self.listbox = dpg.add_listbox(label="Tarefas", items=self.titulos, num_items=16)

                with dpg.popup(dpg.last_item(), max_size=(150, 15)):
                    dpg.add_button(label="Editar tarefa", width=135, callback=self.editar_tarefa_window, drag_callback=self.listbox)

                    dpg.add_button(label="Visualizar tarefa", width=135, tag="VisuButton", callback=self.visualizar_tarefa, drag_callback=self.listbox)

                    dpg.add_button(label="Concluir tarefa", width=135, tag="MarkTarefa", callback=self. marcar_concluida, drag_callback=self.listbox)


                with dpg.group(horizontal=True):
                    dpg.add_button(label="Adicionar tarefa", tag="openPopUp", callback=self.criar_tarefa_popup)

                    dpg.add_button(label="Excluir tarefa", callback=self.excluir_tarefa, drag_callback=self.listbox)

                    dpg.add_button(label="Desfazer", callback=self.desfazer_operacao)

                    # Botão de edição
                    # Botão para ordenar por título, prazo ou data de criação

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
        
    def exibir_lembrete(self):
        check = dpg.get_value("tarefa_lembrete_check")
        dpg.configure_item("lembrete_input", show=check)
    
    def exibir_prazo(self):
        check = dpg.get_value("tarefa_prazo_check")
        dpg.configure_item("prazo_input", show=check)

    def checar_tarefa(self, titulo):
        for tar_titulo in self.titulos:
            if tar_titulo == titulo:
                with dpg.popup(parent="adicionar_button", modal=True):
                    dpg.add_text("Atividade já consta na lista de tarefas")
                    return False

        return True

    def criar_tarefa_popup(self):
        pop_up_criar = dpg.popup(parent="openPopUp", modal=True, tag="popUpCriar", mousebutton=dpg.mvMouseButton_Left)

        with pop_up_criar:
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
            tarefa = TarefaTrabalhoFactory.criar_tarefa(titulo, descricao)

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


tarefa = TarefaBase("Comprar frutas", "abubléf")
tarefa2 = TarefaBase("Alimentar cachorro", "abublés")
tarefa3 = TarefaBase("Fazer compras", "abubléw")
tarefa4 = TarefaBase("Beber água", "abubléee")

organizador = TarefaOrganizador()

organizador.add_tarefa(tarefa)
organizador.add_tarefa(tarefa2)
organizador.add_tarefa(tarefa3)
organizador.add_tarefa(tarefa4)


tela_inicial = TelaInicial(organizador)
tela_inicial.exibir()
