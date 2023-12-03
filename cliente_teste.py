import socket
import sys
import time
from _thread import start_new_thread
import os
import hashlib
from IDPP2P.cliente import *

def main():
    global porta_tcp
    porta_tcp = descobre_porta_disponivel()

    senha = input("Digite a senha do servidor: ")
    registrar_no_servidor(senha)
    
    start_new_thread(controle_tcp, ())

    while True:
        print("\nMenu:")
        print("1. Atualizar lista de arquivos (UPD)")
        print("2. Listar arquivos disponíveis (LST)")
        print("3. Desconectar do servidor (END)")
        print("4. Baixar um arquivo (GET)")
        print("5. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            atualizar_arquivos_no_servidor(pasta_compartilhada)
        elif escolha == '2':
            listar_arquivos_disponiveis()
        elif escolha == '3':
            desconectar_do_servidor()
            break
        elif escolha == '4':
            listar_arquivos_disponiveis()
            nome_arquivo = input("Digite o nome do arquivo para baixar: ")
            receber_arquivo(nome_arquivo, pasta_compartilhada)
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

    # Finaliza o programa
    print("Cliente encerrado.")
    sys.exit(0)

# Demais definições de funções...

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Uso: python3 cliente.py <IP_SERVIDOR> <DIRETORIO>")
    #     sys.exit(1)
    
    # Configurações do Cliente
    # ENDERECO_SERVIDOR = (sys.argv[1], 54494)
    # pasta_compartilhada = sys.argv[2]

    main()
