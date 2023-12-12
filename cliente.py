#!/usr/bin/python

import secrets
import string
import sys
import socket
from _thread import *
import os
from hashlib import md5
import time

informacao_cliente = {}

encerra_tcp = False

#Função para gerar senha da conexão com o servidor udp
def gerar_senha():
    print("Deseja informar uma senha para conexão ou cria-la automaticamente?")
    opcao = input("S/N: ")
    if(opcao.upper() == "S"):
        senha = input("Digite a senha: ")
        return senha
    else:
        tamanho = 8
        caracteres = string.ascii_letters + string.digits + string.punctuation
        senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        print("Senha gerada automaticamente: " + senha)
        return senha

#Função para gerar string com arquivos do diretório
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

#Função para verificar se a porta está disponível
def porta_disponivel(porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', porta))
        return True  # Vinculação bem-sucedida, a porta está disponível
    except OSError as e:
        return False # Vinculação falhou, a porta não está disponível
    finally:
        sock.close()
        
#Função para descobrir porta disponível
def descobre_porta_disponivel():
    for porta in range(31337, 65535):
        if porta_disponivel(porta):
            return porta

    raise Exception("Nenhuma porta disponível encontrada")

#Função para configurar ambiente do cliente
def configurar_ambiente():    
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

#Função para enviar e receber mensagens udp
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
    while True:
        if not str_arquivos:
            print('Não há arquivos disponíveis para download.\n')
            return None

        # Transforma a string em uma lista de arquivos
        arquivos_lista = str_arquivos.split(';')

        # Verifica se há arquivos disponíveis para download
        arquivos_disponiveis = [arquivo for arquivo in arquivos_lista if (str(informacao_cliente['ip']) + ':' + str((informacao_cliente['porta']))) not in arquivo.split(',')[2:]]

        if not arquivos_disponiveis:
            print('Não há arquivos disponíveis para download.\n')
            return None

        print('Selecione um arquivo que deseja baixar:')
        for i, arquivo_info in enumerate(arquivos_disponiveis, start=1):
            md5, nome, *hosts = arquivo_info.split(',')
            print(f'{i} - Nome: {nome}, Hash: {md5}')

        print('0 - Sair')
        opcao = int(input('\nOpção: '))

        # Verifica se a opção selecionada está dentro do índice dos arquivos disponíveis
        if 0 <= opcao <= len(arquivos_disponiveis):
            if opcao == 0:
                print('Saindo do menu de seleção de arquivo.')
                return None
            else:
                arquivo_selecionado = arquivos_disponiveis[opcao - 1]
                return arquivo_selecionado
        else:
            print('Opção inválida. Tente novamente.')

# Cria menu interativo para cliente selecionar host que deseja baixar o arquivo
def menu_selecionar_host(arquivo_selecionado):
    nome , md5, *hosts = arquivo_selecionado.split(',')
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

#Função para requisitar arquivo
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
                if not data:
                    break
                arquivo.write(data)
    except Exception as e:
        print(f"\nErro ao requisitar o arquivo: {nome}")
    finally:
        print('Selecione uma opção:')
        print('1 - Atualizar arquivos disponíveis')
        print('2 - Baixar um arquivo')
        print('3 - Sair')
        print('Opção:')
        socket_cliente.close()

#Função para enviar e receber mensagens udp
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

#Função para controle udp
def controle_udp():
    global encerra_tcp
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
            str_arquivos = string_arquivos()
            mensagem = f"UPD {informacao_cliente['senha']} {informacao_cliente['porta']} {str_arquivos}"
            envia_recebe_udp(mensagem, endereco_servidor, socket_cliente)
        elif opcao == '3':
            #enviar END para servidor
            mensagem = f"END {informacao_cliente['senha']} {informacao_cliente['porta']}"
            envia_recebe_udp(mensagem, endereco_servidor, socket_cliente)
            encerra_tcp = True
            socket_cliente.close()
            sys.exit(0)


#Função para controle tcp
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
        print('Selecione uma opção:')
        print('1 - Atualizar arquivos disponíveis')
        print('2 - Baixar um arquivo')
        print('3 - Sair')
        print('Opção:')
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
    
    #Descobre porta disponível para abrir escuta TCP
    porta_tcp = descobre_porta_disponivel()
    informacao_cliente['porta'] = porta_tcp
    start_new_thread(inicia_controle_tcp, ())
    start_new_thread(inicia_controle_udp, ())

    while True:
        if encerra_tcp:
            sys.exit(0)
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        informacao_cliente['ip'] = sys.argv[1]
        informacao_cliente['nome_diretorio'] = sys.argv[2]
        main()
    else:
        print('Uso: python cliente.py <ip> <diretorio>')
        sys.exit(0)