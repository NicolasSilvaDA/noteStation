"""
    Módulo ainda em desenvolvimento, abaixo encontra-se apenas
    um protótipo da interface
"""

import tkinter as tk
from tkinter import messagebox

# from tarefa_classes import *

class TelaInicial(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("noteStation")
        self.geometry("400x300")

        self.lista_tarefas = []
        self.criar_componentes()

    def criar_componentes(self):
        self.lista_frame = tk.Frame(self)
        self.lista_frame.pack(pady=15)

        self.lista_label = tk.Label(self.lista_frame, text="Lista de Tarefas", font=("system-ui", 14, "bold"))
        self.lista_label.pack()

        self.tarefas_listbox = tk.Listbox(self.lista_frame, width=55)

        self.tarefas_listbox.pack(pady=15)

        self.carregar_tarefas()

        # Botões

        self.botoes_frame = tk.Frame(self)
        self.botoes_frame.pack(pady=10)

        self.ordenar_button = tk.Button(self.botoes_frame, text="Ordenar",
        command=self.ordenar_tarefas)
        self.ordenar_button.pack(side=tk.LEFT, padx=5)

        self.criar_button = tk.Button(self.botoes_frame, text="Criar Tarefa", command=self.abrir_tela_criacao)
        self.criar_button.pack(side=tk.LEFT, padx=5)
    
    def carregar_tarefas(self):
        self.lista_tarefas = [
            "Tarefa 1",
            "Tarefa 2"
        ]

        self.tarefas_listbox.delete(0, tk.END)

        for tarefa in self.lista_tarefas:
            self.tarefas_listbox.insert(tk.END, tarefa)

    def ordenar_tarefas(self):
        ...

    def abrir_tela_criacao(self):
        tela_criacao = TelaCriacao(self)
        self.wait_window(tela_criacao)

class TelaCriacao(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Criar Tarefa")
        self.geometry("400x300")

        self.criar_componentes()

    def criar_componentes(self):
        self.titulo_entry = tk.Entry(self)
        self.titulo_entry.pack(pady=10)

        self.descricao_entry = tk.Entry(self)
        self.descricao_entry.pack(pady=10)

        #Botão de criar
        self.criar_button = tk.Button(self, text="Criar", command=self.criar_tarefa)
        self.criar_button.pack(pady=10)

    def criar_tarefa(self):
        titulo = self.titulo_entry.get()
        descricao = self.descricao_entry.get()

        # Exemplo de mensagem
        messagebox.showinfo("Tarefa criada com sucesso", f'Título: {titulo}\nDescrição: {descricao}')
        self.destroy()

if __name__ == "__main__":
    app = TelaInicial()
    app.mainloop()