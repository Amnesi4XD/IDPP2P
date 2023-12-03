import socket
import sys
import time
from _thread import start_new_thread
import os
import hashlib
import socket


# Verifica se o número correto de argumentos foi passado
# if len(sys.argv) != 3:
#     print("Uso: python3 cliente.py <IP_SERVIDOR> <DIRETORIO>")
#     sys.exit(1)

# Configurações do Cliente
ENDERECO_SERVIDOR = ("127.0.0.1", 54494)
BUFFER_SIZE = 1024

# Informações do Cliente
senha = "123456"
porta_tcp = None
pasta_compartilhada = "/home/rafanog/desktop/redes/armazena"
# Socket UDP para comunicação com o servidor
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def descobre_porta_disponivel():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))  # O sistema operacional irá atribuir uma porta disponível
    porta = s.getsockname()[1]  # Obtemos a porta atribuída
    s.close()  # Fechamos o socket, a porta pode ser reutilizada
    return porta


def registrar_no_servidor(senha):
    porta_tcp = descobre_porta_disponivel()
    mensagem = f"REG {senha} {porta_tcp} {listar_arquivos_disponiveis()}"
    socket_udp.sendto(mensagem.encode(), ENDERECO_SERVIDOR)
    resposta, _ = socket_udp.recvfrom(BUFFER_SIZE)
    print("Resposta do servidor:", resposta.decode())

def atualizar_arquivos_no_servidor(pasta):
    arquivos = listar_arquivos_pasta(pasta)
    arquivos_compartilhados = ';'.join([f"{hash_arquivo},{nome_arquivo}" for hash_arquivo, nome_arquivo in arquivos])

    mensagem = f"UPD {senha} {porta_tcp} {arquivos_compartilhados}"
    socket_udp.sendto(mensagem.encode(), ENDERECO_SERVIDOR)

    resposta, _ = socket_udp.recvfrom(BUFFER_SIZE)
    print("Resposta do servidor à atualização:", resposta.decode())

def listar_arquivos_disponiveis():
    mensagem = "LST"
    socket_udp.sendto(mensagem.encode(), ENDERECO_SERVIDOR)
    resposta, _ = socket_udp.recvfrom(BUFFER_SIZE)
    print("Arquivos disponíveis:", resposta.decode())

def desconectar_do_servidor():
    mensagem = f"END {senha} {porta_tcp}"
    socket_udp.sendto(mensagem.encode(), ENDERECO_SERVIDOR)
    resposta, _ = socket_udp.recvfrom(BUFFER_SIZE)
    print("Resposta do servidor:", resposta.decode())

def servico_tcp(cliente, pasta):
    mensagem = cliente.recv(BUFFER_SIZE).decode()
    comando, nome_arquivo = mensagem.split()

    if comando == 'GET':
        enviar_arquivo(cliente, nome_arquivo, pasta)
    elif comando == 'SEND':
        receber_arquivo(cliente, nome_arquivo, pasta)
    else:
        cliente.send(b"ERRO: COMANDO INVALIDO")

    cliente.close()

def controle_tcp():
    global porta_tcp
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_tcp.bind(('', porta_tcp))
    socket_tcp.listen(5)
    while True:
        cliente, endereco = socket_tcp.accept()
        start_new_thread(servico_tcp, (cliente,))

def enviar_arquivo(cliente, nome_arquivo, pasta):
    caminho_arquivo = os.path.join(pasta, nome_arquivo)
    if not os.path.exists(caminho_arquivo):
        cliente.send(b"ERRO: ARQUIVO NAO ENCONTRADO")
        return

    cliente.send(b"OK")

    with open(caminho_arquivo, 'rb') as arquivo:
        while True:
            dados = arquivo.read(BUFFER_SIZE)
            if not dados:
                break
            cliente.send(dados)

def receber_arquivo(cliente, nome_arquivo, pasta):
    caminho_arquivo = os.path.join(pasta, nome_arquivo)
    with open(caminho_arquivo, 'wb') as arquivo:
        while True:
            dados = cliente.recv(BUFFER_SIZE)
            if not dados:
                break
            arquivo.write(dados)

    
def gerar_hash_arquivo(nome_arquivo):
    hasher = hashlib.sha256()
    with open(nome_arquivo, 'rb') as arquivo:
        buf = arquivo.read()
        hasher.update(buf)
    return hasher.hexdigest()

def listar_arquivos_pasta(pasta):
    arquivos = []
    for nome_arquivo in os.listdir(pasta):
        if os.path.isfile(os.path.join(pasta, nome_arquivo)):
            hash_arquivo = gerar_hash_arquivo(os.path.join(pasta, nome_arquivo))
            arquivos.append((hash_arquivo, nome_arquivo))
    return arquivos

def main():
    global porta_tcp
    porta_tcp = descobre_porta_disponivel()

    registrar_no_servidor()
    # Iniciar outras funcionalidades conforme necessário

    start_new_thread(controle_tcp, ())
    while True:
        # Loop principal do cliente
        time.sleep(60)

if __name__ == "__main__":
    main()
