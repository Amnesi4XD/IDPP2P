#!/usr/bin/python

import secrets
import string
import sys
import time
import socket
from _thread import *
import os
from hashlib import md5

informacao_cliente = {}

def gerar_senha():
    tamanho = 8
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha

def string_arquivos():
    lista = []
    diretorio = informacao_cliente['nome_diretorio']

    for arquivo_nome in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, arquivo_nome)

        if os.path.isfile(caminho_arquivo):  # Certifica-se de que é um arquivo, não um diretório
            with open(caminho_arquivo, 'rb') as arquivo:
                md5_arquivo = md5(arquivo.read()).hexdigest()
                elemento_lista = f"{md5_arquivo},{arquivo_nome}"
                lista.append(elemento_lista)

    # Junte os elementos da lista em uma única string
    str_lista = ';'.join(lista)
    return str_lista


def porta_disponivel(porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', porta))
        return False  # Conexão bem-sucedida, a porta está em uso
    except ConnectionRefusedError:
        return True   # Conexão recusada, a porta está disponível
    finally:
        sock.close()

def descobre_porta_disponivel():
    for porta in range(31337, 65535):
        if porta_disponivel(porta):
            return porta

    raise Exception("Nenhuma porta disponível encontrada")

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
        if resposta.upper() == 'S':
            os.mkdir(informacao_cliente['nome_diretorio'])
        else:
            print('Encerrando serviço')
            sys.exit(0)

def envia_recebe_udp(mensagem, endereco_servidor, socket_cliente):
    try:
        socket_cliente.sendto(mensagem.encode('utf-8'), endereco_servidor)
        print(f'\nMensagem enviada: {mensagem}\n')
        data, _ = socket_cliente.recvfrom(4096)
        resposta = data.decode('utf-8')
        print(f'\nMensagem recebida: {resposta}\n')
        return resposta
    except:
        print(f'Erro ao tentar se comunicar com o servidor\n')

# Cria menu interativo para cliente selecionar arquivo que deseja baixar
def menu_selecionar_arquivo(str_arquivos):
    if not str_arquivos:
        print('Não há arquivos disponíveis para download.')
        return None

    # Transforma a string em uma lista de arquivos
    arquivos_lista = str_arquivos.split(';')

    print('Selecione um arquivo que deseja baixar:')
    for i, arquivo_info in enumerate(arquivos_lista):
        md5, nome, *hosts = arquivo_info.split(',')
        
        # Verifica se o IP e a porta do cliente estão na lista de hosts do arquivo
        if (str(informacao_cliente['ip']) + ':' + str((informacao_cliente['porta']))) not in hosts:
            print(f'{i + 1} - Nome: {nome}, Hash: {md5}')

    opcao = int(input('\nOpção: '))

    # Verifica se a opção selecionada está dentro do índice da arquivos_lista
    if 1 <= opcao <= len(arquivos_lista):
        arquivo_selecionado = arquivos_lista[opcao - 1]
        return arquivo_selecionado
    else:
        print('Opção inválida.')
        return None


def menu_selecionar_host(arquivo_selecionado):
    md5 , nome, *hosts = arquivo_selecionado.split(',')
    print(f'\nSelecione um host para baixar o arquivo "{nome}":')
    for i, host_info in enumerate(hosts):
        ip, porta = host_info.split(':')
        print(f'{i+1} - IP: {ip}, Porta: {porta}')

    opcao = int(input('\nOpção: '))

#Verifica se a opção selecionada esta dentro do índice de hosts
    if 1<= opcao <= len(hosts):
        host_selecionado = hosts[opcao - 1]
        print(f'\nVocê selecionou o arquivo "{nome}" do host "{host_selecionado}" para download.')
        ip, porta = host_selecionado.split(':')
        return ip, porta, md5, nome
    else:
        print('Opção inválida.')

def requisita_arquivo(ip, porta, hash, nome):
    try:
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_cliente.connect((ip, int(porta)))
        mensagem = f"GET {hash}"
        socket_cliente.send(mensagem.encode('utf-8'))
        print(f'\nMensagem enviada: {mensagem}\n')

        with open(os.path.join(informacao_cliente['nome_diretorio'], nome), 'wb') as arquivo:
            while True:
                data = socket_cliente.recv(4096)
                print(f'\nMensagem recebida: {data}\n')
                if not data:
                    break
                arquivo.write(data)
    except Exception as e:
        print(f"\nErro ao requisitar o arquivo: {nome}")
    finally:
        socket_cliente.close()
def envia_recebe_udp(mensagem, endereco_servidor, socket_cliente):
    try:
        socket_cliente.sendto(mensagem.encode('utf-8'), endereco_servidor)
        print(f'\nMensagem enviada: {mensagem}\n')
        data, _ = socket_cliente.recvfrom(4096)
        resposta = data.decode('utf-8')
        print(f'\nMensagem recebida: {resposta}\n')
        return resposta
    except:
        print(f'Erro ao tentar se comunicar com o servidor\n')

def controle_udp():
    # Inicia a conexão UDP
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    endereco_servidor = ('localhost', 54494)
    str_arquivos = string_arquivos()
    if str_arquivos == '':
        mensagem = f"REG {informacao_cliente['senha']} {informacao_cliente['porta']}"
    else:
        mensagem = f"REG {informacao_cliente['senha']} {informacao_cliente['porta']} {str_arquivos}"
    envia_recebe_udp(mensagem, endereco_servidor, socket_cliente)
    
    while True:
        #cria interfaçe para o usúario poder selecionar se ele quer listar arquivos disponíveis, baixar um arquivo ou sair do programa
        print('Selecione uma opção:')
        print('1 - Atualizar arquivos disponíveis')
        print('2 - Baixar um arquivo')
        print('3 - Sair')
        opcao = input('Opção: ')
        if opcao == '1':
            str_arquivos = string_arquivos()
            if str_arquivos == '':
                mensagem = f"UPD {informacao_cliente['senha']} {informacao_cliente['porta']}"
            else:
                mensagem = f"UPD {informacao_cliente['senha']} {informacao_cliente['porta']} {str_arquivos}"
            envia_recebe_udp(mensagem, endereco_servidor, socket_cliente)
            print('Erro ao tentar conectar no servidor')
        elif opcao == '2':
            #enviar LST para servidor
            mensagem = "LST"
            resposta = envia_recebe_udp(mensagem, endereco_servidor, socket_cliente)
            info_arquivo = menu_selecionar_arquivo(resposta)
            if info_arquivo is None:
                continue
            ip, porta, hash, nome = menu_selecionar_host(info_arquivo)
            requisita_arquivo(ip, porta, hash, nome)
            str_arquivos = string_arquivos
            mensagem = f"UPD {informacao_cliente['senha']} {informacao_cliente['porta']} {str_arquivos}"
            envia_recebe_udp(mensagem, endereco_servidor, socket_cliente)
        elif opcao == '3':
            #enviar END para servidor
            mensagem = f"END {informacao_cliente['senha']} {informacao_cliente['porta']}"
            envia_recebe_udp(mensagem, endereco_servidor, socket_cliente)
            socket_cliente.close()
            sys.exit(0)

def servico_tcp(client):
    try:
        mensagem = client.recv(4096).decode('utf-8')
        print(f'\nMensagem recebida: {mensagem}\n')
        
        if mensagem.startswith("GET "):
            _, hash_arquivo = mensagem.split(" ")
            diretorio = informacao_cliente['nome_diretorio']

            for arquivo_nome in os.listdir(diretorio):
                caminho_arquivo = os.path.join(diretorio, arquivo_nome)

                if os.path.isfile(caminho_arquivo):
                    with open(caminho_arquivo, 'rb') as arquivo:
                        md5_arquivo = md5(arquivo.read()).hexdigest()

                        if md5_arquivo == hash_arquivo:
                            # Envia o arquivo para o cliente
                            with open(caminho_arquivo, 'rb') as arquivo_enviar:
                                dados = arquivo_enviar.read()
                                client.sendall(dados)
                            break
            else:
                client.sendall('Arquivo não encontrado')
        else:
            client.sendall('Mensagem inválida')

    except Exception as e:
        return

    finally:
        client.close()

def controle_tcp():
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _socket.bind((informacao_cliente['ip'], informacao_cliente['porta']))
    _socket.listen(4096)
    while True:
        client, addr = _socket.accept()
        start_new_thread(servico_tcp, (client, ))
        
def inicia_controle_tcp():
    controle_tcp()

def inicia_controle_udp():
    controle_udp()

def main():    
    configurar_ambiente()
    
    start_new_thread(inicia_controle_tcp, ())
    start_new_thread(inicia_controle_udp, ())

    while True:
        time.sleep(60)
        print('\nCliente em execução')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        informacao_cliente['ip'] = sys.argv[1]
        informacao_cliente['nome_diretorio'] = sys.argv[2]
        main()
    else:
        print('Uso: python cliente.py <ip> <diretorio>')
        sys.exit(0)