import socket
import threading
from tkinter import *
from tkinter import simpledialog
from time import sleep



class Cliente:
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 6969
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        
        login = Tk()
        login.withdraw()
        
        self.janela_carregada= False
        self.ativo = True
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome: ', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite o nome da sala que seseja entrar: ', parent=login)
        
        t = threading.Thread(target=self.conectar)
        t.start()
        self.abrir_janela()

    def abrir_janela(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title('Chat')
        
        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)
        
        self.campo_mensagem = Entry(self.root)
        self.campo_mensagem.place(relx=0.05, rely=0.8, width=500, height=20)
        
        self.botao_enviar = Button(self.root, text='Enviar', command=self.enviar_mensagem)
        self.botao_enviar.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol('WM_DELETE_WINDOW', self.fechar_janela)
        
        self.root.mainloop()
        
    def fechar_janela(self):
        self.root.destroy()
        self.client.close()
        
    def enviar_mensagem(self):
        mensagem = self.campo_mensagem.get()
        self.client.send(mensagem.encode())
    
    def conectar(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
                sleep(1)  
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass
    
        
cliente = Cliente()