import socket

# Configurações do servidor
ENDERECO_SERVIDOR = ('', 54494)
BUFFER_SIZE = 1024

# Dicionário para armazenar informações dos clientes
informacoes_cliente = {}
lista_arquivos = []

# Função para processar mensagens REG
def registrar_cliente(mensagem, endereco_cliente):
    if len(mensagem) != 4:
        return "ERR INVALID_MESSAGE_FORMAT"

    senha = mensagem[1]
    porta = int(mensagem[2])
    str_arquivos = mensagem[3] #Ex: MD51,NOME1;MD52,NOME2;MD53,NOME3;...;MD5N,NOMEN

    # Verifica se o cliente já está registrado
    if (senha, porta) in informacoes_cliente:
        return "ERR CLIENT_ALREADY_REGISTERED"

    # Processa a lista de arquivos
    lista_arquivos = str_arquivos.split(';')
    arquivos_compartilhados = lista_arquivos.count 
    



    return f"OK {arquivos_compartilhados}_REGISTERED_FILES"

# Função para processar mensagens UPD
def atualizar_cliente(mensagem, endereco_cliente):
    # if len(mensagem) != 4:
    #     return "ERR INVALID_MESSAGE_FORMAT"

    senha = mensagem[1]
    # porta = int(mensagem[2])
    porta = 123
    arquivos_str = mensagem[3] #Ex: MD51,NOME1;MD52,NOME2;MD53,NOME3;...;MD5N,NOMEN

    # Processa a lista de arquivos
    arquivos_lista_temp = arquivos_str.split(';')

    for arquivo in arquivos_lista_temp:
        lista_arquivos.append(arquivo)
    arquivos_atualizados = len(arquivos_lista_temp)

    return f"OK {arquivos_atualizados}_REGISTERED_FILES"

# Função para processar mensagens LST
def listar_arquivos():
    # Percorre todos os clientes e seus arquivos
    for endereco_cliente, info_cliente in informacoes_cliente.items():
        for nome_arquivo, hash_arquivo in info_cliente['arquivos'].items():
            # Verifica se o arquivo já está na lista
            arquivo_existente = next((arquivo_item for arquivo_item in lista_arquivos if arquivo_item['nome'] == nome_arquivo), None)

            if arquivo_existente:
                # Adiciona o IP e porta do cliente ao arquivo existente
                arquivo_existente['localizacoes'].append(f"{endereco_cliente[0]}:{info_cliente['porta']}")
            else:
                # Cria um novo arquivo na lista
                arquivo = {
                    'hash': hash_arquivo,
                    'nome': nome_arquivo,
                    'localizacoes': [f"{endereco_cliente[0]}:{info_cliente['porta']}"]
                }
                lista_arquivos.append(arquivo)

    # Constrói a mensagem de resposta
    resposta = ';'.join([f"{arquivo['hash']},{arquivo['nome']},{','.join(arquivo['localizacoes'])}" for arquivo in lista_arquivos])
    print("Lista de arquivos enviada")
    # resposta = "YES SIRRRRRRRRRRRRRRRRRR"
    return resposta

# Função para processar mensagens END
def desconectar_cliente(mensagem, endereco_cliente):
    if len(mensagem) != 3:
        print(mensagem)
        return "ERR INVALID_MESSAGE_FORMAT"

    senha = mensagem[1]
    porta = int(mensagem[2])

    # Verifica se o cliente está registrado
    if (senha, porta) not in [(info['senha'], info['porta']) for info in informacoes_cliente.values()]:
        return "ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD"

    # Remove as informações do cliente
    informacoes_cliente.pop(endereco_cliente, None)

    return "OK CLIENT_FINISHED"


# Função principal do servidor
def main():
    print("Servidor iniciado")
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_servidor.bind(ENDERECO_SERVIDOR)

    print("Aguardando conexões...")
    while True:
        try:
            data, endereco_cliente = socket_servidor.recvfrom(BUFFER_SIZE)
            mensagem = data.decode('utf-8').split()
            print(mensagem)

            if not mensagem or len(mensagem) < 0: # 0 para fins de teste
                response = "ERR INVALID_MESSAGE_FORMAT"
            else:
                msg_type = mensagem[0]

                if msg_type == "REG":
                    response = registrar_cliente(mensagem, endereco_cliente)
                elif msg_type == "UPD":
                    response = atualizar_cliente(mensagem, endereco_cliente)
                elif msg_type == "LST":
                    response = listar_arquivos()
                elif msg_type == "END":
                    response = desconectar_cliente(mensagem, endereco_cliente)
                else:
                    print(mensagem)
                    response = "ERR INVALID_MESSAGE_FORMAT"
        except KeyboardInterrupt:
            socket_servidor.close()
            break

        socket_servidor.sendto(response.encode('utf-8'), endereco_cliente)

if __name__ == "__main__":
    main()
