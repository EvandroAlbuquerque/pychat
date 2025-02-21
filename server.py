import socket
import threading

HOST = '127.0.0.1'
PORT = 6969

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

salas= {}

def broadcast(sala, mensagem):
    for s in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        s.send(mensagem)

def enviar_mensagem(nome, sala, client):
    while True:
        mensagem = client.recv(1024)
        mensagem = f'{nome}: {mensagem.decode()}\n'
        broadcast(sala, mensagem)

while True:
    client, addr = server.accept()
    client.send(b'SALA')
    sala = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    
    if sala not in salas.keys():
        salas[sala] = []
    
    salas[sala].append(client)
    print(f'{nome} se conectou na sala {sala}: {addr}.')
    broadcast(sala, f'{nome} entrou na sala.\n')
    t = threading.Thread(target=enviar_mensagem, args=(nome, sala, client))
    t.start()