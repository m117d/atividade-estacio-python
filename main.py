import sqlite3
import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk

# Funções do banco de dados
def criar_tabela():
    with sqlite3.connect("bancodedados.db") as conector:
        cursor = conector.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS pessoa (nome TEXT, idade INTEGER, cpf TEXT)")
        conector.commit()

def criar_pessoa(nome, idade, cpf):
    with sqlite3.connect("bancodedados.db") as conector:
        cursor = conector.cursor()
        cursor.execute("INSERT INTO pessoa(nome, idade, cpf) VALUES (?, ?, ?)", (nome, idade, cpf))
        conector.commit()

def buscar_pessoa(nome):
    with sqlite3.connect("bancodedados.db") as conector:
        cursor = conector.cursor()
        cursor.execute("SELECT * FROM pessoa WHERE nome = ?", (nome,))
        return cursor.fetchall()

def excluir_pessoa(nome):
    with sqlite3.connect("bancodedados.db") as conector:
        cursor = conector.cursor()
        cursor.execute("DELETE FROM pessoa WHERE nome = ?", (nome,))
        conector.commit()

def alterar_dado(nome, campo, novo_valor):
    with sqlite3.connect("bancodedados.db") as conector:
        cursor = conector.cursor()
        query = f"UPDATE pessoa SET {campo} = ? WHERE nome = ?"
        cursor.execute(query, (novo_valor, nome))
        conector.commit()

def listar_pessoas():
    with sqlite3.connect("bancodedados.db") as conector:
        cursor = conector.cursor()
        cursor.execute("SELECT * FROM pessoa")
        return cursor.fetchall()

# Funções da interface gráfica
def abrir_criar_pessoa():
    janela_criar = ctk.CTkToplevel(app)
    janela_criar.geometry("300x200")

    ctk.CTkLabel(janela_criar, text="Digite o nome:").pack()
    nome_entry = ctk.CTkEntry(janela_criar)
    nome_entry.pack()

    ctk.CTkLabel(janela_criar, text="Digite a idade:").pack()
    idade_entry = ctk.CTkEntry(janela_criar)
    idade_entry.pack()

    ctk.CTkLabel(janela_criar, text="Digite o cpf:").pack()
    cpf_entry = ctk.CTkEntry(janela_criar)
    cpf_entry.pack()

    def on_ok():
        criar_pessoa(nome_entry.get(), idade_entry.get(), cpf_entry.get())
        janela_criar.destroy()

    ctk.CTkButton(janela_criar, text="OK", command=on_ok).pack()

def abrir_buscar_pessoa():
    janela_buscar = ctk.CTkToplevel(app)
    janela_buscar.geometry("300x200")

    ctk.CTkLabel(janela_buscar, text="Digite o nome:").pack()
    nome_entry = ctk.CTkEntry(janela_buscar)
    nome_entry.pack()

    def on_ok():
        resultado = buscar_pessoa(nome_entry.get())
        texto_resultado.set("\n".join(f"Nome: {nome}\nIdade: {idade}\nCPF: {cpf}" for nome, idade, cpf in resultado))
        janela_buscar.destroy()

    ctk.CTkButton(janela_buscar, text="OK", command=on_ok).pack()

def atualizar_resultados():
    pessoas = listar_pessoas()
    resultado_formatado = "\n\n".join(f"Nome: {nome}\nIdade: {idade}\nCPF: {cpf}" for nome, idade, cpf in pessoas)
    texto_resultado.set(resultado_formatado)

def abrir_excluir_pessoa():
    janela_excluir = ctk.CTkToplevel(app)
    janela_excluir.geometry("300x200")

    pessoas = listar_pessoas()
    for pessoa in pessoas:
        ctk.CTkButton(janela_excluir, text=str(pessoa), command=lambda p=pessoa: on_delete(p)).pack()

    def on_delete(pessoa):
        if messagebox.askyesno("Excluir", f"Tem certeza que deseja excluir {pessoa[0]}?"):
            excluir_pessoa(pessoa[0])
            janela_excluir.destroy()

def abrir_alterar_dado():
    janela_alterar = ctk.CTkToplevel(app)
    janela_alterar.geometry("300x200")

    pessoas = listar_pessoas()
    for pessoa in pessoas:
        ctk.CTkButton(janela_alterar, text=str(pessoa), command=lambda p=pessoa: on_select(p)).pack()

    def on_select(pessoa):
        campo = simpledialog.askstring("Alterar", "Qual campo deseja alterar? (nome, idade, cpf)")
        if campo and campo in ["nome", "idade", "cpf"]:
            novo_valor = simpledialog.askstring("Alterar", f"Digite o novo valor para {campo}:")
            if novo_valor:
                alterar_dado(pessoa[0], campo, novo_valor)
                janela_alterar.destroy()
                atualizar_resultados()
        else:
            messagebox.showerror("Erro", "Campo inválido. Escolha entre 'nome', 'idade' ou 'cpf'.")


# Interface principal
app = ctk.CTk()
app.geometry("600x400")

frame_esquerda = ctk.CTkFrame(app)
frame_esquerda.pack(side="left", fill="y")

frame_direita = ctk.CTkFrame(app)
frame_direita.pack(side="right", fill="both", expand=True)

texto_resultado = ctk.StringVar()
ctk.CTkButton(frame_esquerda, text="Criar Tabela", command=criar_tabela).pack(fill="x", pady=10)
ctk.CTkButton(frame_esquerda, text="Criar Pessoa", command=abrir_criar_pessoa).pack(fill="x", pady=10)
ctk.CTkButton(frame_esquerda, text="Buscar Pessoa", command=abrir_buscar_pessoa).pack(fill="x", pady=10)
ctk.CTkButton(frame_esquerda, text="Excluir Pessoa", command=abrir_excluir_pessoa).pack(fill="x", pady=10)
ctk.CTkButton(frame_esquerda, text="Alterar Dado", command=abrir_alterar_dado).pack(fill="x", pady=10)

resultado_label = ctk.CTkLabel(frame_direita, textvariable=texto_resultado, anchor="center", justify="center")
resultado_label.pack(fill="both", expand=True)
ctk.CTkButton(frame_direita, text="Atualizar", command=atualizar_resultados).pack()

app.mainloop()
