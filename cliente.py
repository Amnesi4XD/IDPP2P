#!/usr/bin/python

import secrets
import string
import sys
import time
import socket
from _thread import *
import os
from hashlib import md5

porta_tcp = None

informacao_cliente = {}

def gerar_senha():
    tamanho = 8
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha

def listar_arquivos():
    lista = []
    diretorio = informacao_cliente['nome_diretorio']
    for arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, arquivo)
        hash = md5(open(caminho_completo, 'rb').read()).hexdigest()
        elemento_lista = hash + ',' + arquivo
        lista.append(elemento_lista)
    return lista

def configurar_ambiente():
    #Pegando porta disponível
    porta_tcp = descobre_porta_disponivel()
    informacao_cliente['porta'] = porta_tcp
    
    #Gerando senha para conexão udp
    senha = gerar_senha()
    informacao_cliente['senha'] = senha
    
    #Checando path do diretório de arquivos
    if  not os.path.isdir(informacao_cliente['nome_diretorio']):
        print('Diretorio para salvar arquivos não existe, gostaria de criar diretório com esse nome?')    
        resposta = input('S/N: ')
        if resposta == 'S':
            os.mkdir(informacao_cliente['nome_diretorio'])
        else:
            print('Encerrando serviço')
            sys.exit(0)

def descobre_porta_disponivel():
    for porta in range(31337, 65535):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((informacao_cliente["ip"], porta))
            s.close()
            return porta
        except OSError:
            pass
    raise Exception("Nenhuma porta disponível encontrada")

def controle_udp(senha, socket_cliente, endereco_servidor):
    while True:
        #cria interfaçe para o usúario poder selecionar se ele quer listar arquivos disponíveis, baixar um arquivo ou sair do programa
        print('Selecione uma opção:')
        print('1 - Atualizar arquivos disponíveis')
        print('2 - Baixar um arquivo')
        print('3 - Sair')
        opcao = input('Opção: ')
        if opcao == '1':
            try:
                mensagem = f"UPD {informacao_cliente['senha']}, {informacao_cliente['porta']}, {listar_arquivos()}"
                # mensagem = "UPD" 
                socket_cliente.sendto(mensagem.encode(), endereco_servidor)
                data, server = socket_cliente.recvfrom(4096)
                print(data.decode('utf-8'))
            except:
                print('Erro ao tentar conectar no servidor')
                sys.exit(0)
        elif opcao == '2':
            #enviar LST para servidor
            try:
                mensagem = "LST"
                socket_cliente.sendto(mensagem.encode('utf-8'), endereco_servidor)
                data, server = socket_cliente.recvfrom(4096)
                print(data.decode('utf-8'))
            except:
                print('Erro ao tentar conectar no servidor')
                sys.exit(0)
        elif opcao == '3':
            #enviar END para servidor
            mensagem = f"END {informacao_cliente['senha']} {informacao_cliente['porta']}"
            print(mensagem)
            socket_cliente.sendto(mensagem.encode('utf-8'), endereco_servidor)
            data, server = socket_cliente.recvfrom(4096)
            print(data.decode('utf-8'))
            socket_cliente.close()
            sys.exit(0)

def servico_tcp(client):
    # Código do serviço TCP
    print('Nova conexao TCP')
    client.send(b'OI')
    client.close()

def controle_tcp():
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _socket.bind(('', informacao_cliente['porta']))
    _socket.listen(4096)
    while True:
        client, addr = _socket.accept()
        start_new_thread(servico_tcp, (client, ))
        
def inicia_controle_tcp():
    controle_tcp()

def inicia_controle_udp():
    # Inicia a conexão UDP
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Cliente iniciado')
    endereco_servidor = ('localhost', 54494)
    mensagem = f"REG {informacao_cliente['senha']} {informacao_cliente['porta']} {listar_arquivos()}"
    print(mensagem)
    #Retirar após testes
    try:   
        socket_cliente.sendto(mensagem.encode(), endereco_servidor)
    except:
        print('Erro ao tentar conectar no servidor')
        sys.exit(0)
    controle_udp(informacao_cliente['senha'], socket_cliente, endereco_servidor)

def main():    
    configurar_ambiente()
    # start_new_thread(inicia_controle_tcp(), ())
    start_new_thread(inicia_controle_udp(), ())

    while True:
        time.sleep(60)
        print('Cliente em execução')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        informacao_cliente['ip'] = sys.argv[1]
        informacao_cliente['nome_diretorio'] = sys.argv[2]
        main()
    else:
        print('Uso: python cliente.py <ip> <diretorio>')
        sys.exit(0)