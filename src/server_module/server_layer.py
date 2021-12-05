import socket
import os, sys
from _thread import *
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from db.database import *
from models.cliente import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
porta = 1233
cont_thread = 0

criar_db()

try:
    server_socket.bind((host, porta))
except socket.error as error:
    print(str(error))

print('Aguardando conexão...')
server_socket.listen(5)

def gerenciar_cliente_thread(conexao, endereco):
    conexao.send(str.encode('Bem vindo ao servidor'))
    while True:
        data = conexao.recv(2048)
        req = data.decode('utf-8')
        req_header = str(req).split('.')
        handle_request(req_header, conexao, endereco)

        if not data:
            print('data is null')
            break
    print('Servidor vai fechar a conexao')
    
    conexao.close()

def handle_request(req, conn, endereco):
    if req[0] == 'cadastro':
        cliente = Cliente(req[1], req[2], req[3])
        criar_cliente(cliente)
        conn.sendall(str.encode('ok'))
    elif req[0] == 'login':
        if not autenticar_cliente(req[1], req[2]):
            print('Login com sucesso')
            print(conn.getsockname())
            print(conn.getpeername())
            print('Mandando para', conn.getsockname())
            conn.sendall(str.encode('sucesso'))
        else:
            print('Login falhou')
            conn.send(str.encode('falha'))

while True:
    client_socket, endereco = server_socket.accept()
    print('Conectado a: ' + endereco[0] + ': ' + str(endereco[1]))
    start_new_thread(gerenciar_cliente_thread, (client_socket, endereco))
    cont_thread += 1
    print('Numero de threads: ' + str(cont_thread))

server_socket.close()