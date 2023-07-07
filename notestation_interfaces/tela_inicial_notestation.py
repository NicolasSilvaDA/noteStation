import dearpygui.dearpygui as dpg
import sys
import os

diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(diretorio_pai)

from tarefa_classes import *


class TelaInicial:
    def __init__(self, organizador):
        self.organizador = organizador

    def exibir(self):
        self.titulos = [self.organizador.checkTarefaDecorator(tarefa).titulo for tarefa in self.organizador.tarefas]

        dpg.create_context()
        dpg.create_viewport(title="noteStation", max_width=600, max_height=500, min_width=600, min_height=500)
        dpg.setup_dearpygui()

        with dpg.window(label="noteStation", width=600, height=500, no_title_bar=True):
            # Listbox para exibir as tarefas
            with dpg.group():
                self.listbox = dpg.add_listbox(label="Tarefas", items=self.titulos, callback=self.get_item_lista, num_items=16)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Adicionar tarefa", tag="openPopUp", callback=self.criar_tarefa_popup)

                    dpg.add_button(label="Excluir tarefa", callback=self.excluir_tarefa, drag_callback=self.listbox)

                    dpg.add_button(label="Desfazer", callback=self.desfazer_operacao)

                    # Botão de edição e visualização
                    # Botão para ordenar por título, prazo ou data de criação

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def get_item_lista(self, sender, app_data):
        return app_data
    
    def atualizar_lista(self):
        self.titulos = [self.organizador.checkTarefaDecorator(tarefa).titulo for tarefa in self.organizador.tarefas]
        dpg.configure_item(self.listbox, items=self.titulos)
        
    def exibir_lembrete(self):
        check = dpg.get_value("tarefa_lembrete_check")
        dpg.configure_item("lembrete_input", show=check)
    
    def exibir_prazo(self):
        check = dpg.get_value("tarefa_prazo_check")
        dpg.configure_item("prazo_input", show=check)

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
        try:
            titulo = dpg.get_value("tarefa_titulo")
            descricao = dpg.get_value("tarefa_descricao")
        except:
            with dpg.popup(parent="adicionar_button", modal=True):
                dpg.add_text("Os campos de título e descrição são obrigatórios")
        
        tarefa = TarefaTrabalhoFactory.criar_tarefa(titulo, descricao)

        lembrete_check = dpg.get_value("tarefa_lembrete_check")
        prazo_check = dpg.get_value("tarefa_prazo_check")

        lembrete = dpg.get_value("lembrete_input")
        prazo = dpg.get_value("prazo_input")

        prazo_text = f'{prazo["month_day"]}/{prazo["month"]}/{prazo["year"] + 1900}'

        if lembrete_check:
            tarefa = TarefaComLembrete(tarefa, lembrete)

        if prazo_check:
            tarefa = TarefaComPrazo(tarefa, prazo_text)

        self.organizador.add_tarefa(tarefa)
        self.atualizar_lista()

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
