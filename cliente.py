#!/usr/bin/python

import time
import socket
from _thread import *

porta_tcp = None

def configurar_ambiente():
    pass


def descobre_porta_disponivel():
    # Define a porta inicial
    porta_inicial = 31337

    while True:
        try:
            # Tenta criar um socket na porta especificada
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', porta_inicial))
            # Se bem-sucedido, retorna a porta
            return porta_inicial
        except socket.error:
            # Se a porta estiver em uso, tenta a próxima
            porta_inicial += 1

def controle_udp():
    # Código do serviço UDP
    while True:
        print('Controle UDP funcionando')
        time.sleep(5)


def servico_tcp(client):
    # Código do serviço TCP
    print('Nova conexao TCP')
    client.send(b'OI')
    client.close()


def controle_tcp():
    global porta_tcp
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _socket.bind(('', porta_tcp))
    _socket.listen(4096)
    while True:
        client, addr = _socket.accept()
        start_new_thread(servico_tcp, (client, ))


def inicia_controle_tcp():
    controle_tcp()


def inicia_controle_udp():
    controle_udp()


def main():
    global porta_tcp
    porta_tcp = descobre_porta_disponivel()

    configurar_ambiente()

    start_new_thread(inicia_controle_tcp, ())
    start_new_thread(inicia_controle_udp, ())

    while True:
        time.sleep(60)
        print('Cliente em execução')


if __name__ == '__main__':
    main()