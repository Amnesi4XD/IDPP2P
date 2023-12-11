import socket

# Configurações do servidor
ENDERECO_SERVIDOR = ('', 54494)
BUFFER_SIZE = 1024

# Dicionário para armazenar informações dos clientes
informacoes_cliente = {}

# Função para processar mensagens REG
def registrar_cliente(mensagem, endereco_cliente):
    if len(mensagem) != 4:
        return "ERR INVALID_MESSAGE_FORMAT"
    
    senha = mensagem[1]
    porta = int(mensagem[2])
    str_arquivos = mensagem[3]

    # Verifica se o cliente já está registrado
    if (senha, porta) in informacoes_cliente:
        return "ERR CLIENT_ALREADY_REGISTERED"

    # Processa a lista de arquivos
    lista_arquivos = str_arquivos.split(';')
    arquivos_compartilhados = 0

    for info_arquivo in lista_arquivos:
        partes_mensagem_arquivo = info_arquivo.split(',')
        if len(partes_mensagem_arquivo) == 2:
            hash_arquivo, nome_arquivo = partes_mensagem_arquivo[0], partes_mensagem_arquivo[1]
            # Adiciona o arquivo ao cliente
            if endereco_cliente not in informacoes_cliente:
                informacoes_cliente[endereco_cliente] = {'senha': senha, 'porta': porta, 'arquivos': {}}
            informacoes_cliente[endereco_cliente]['arquivos'][nome_arquivo] = hash_arquivo
            arquivos_compartilhados += 1

    return f"OK {arquivos_compartilhados}_REGISTERED_FILES"

# Função para processar mensagens UPD
def atualizar_cliente(mensagem, endereco_cliente):
    if len(mensagem) < 4:
        return "ERR INVALID_MESSAGE_FORMAT"

    senha = mensagem[1]
    porta = int(mensagem[2])
    arquivos_str = mensagem[3]

    # Verifica se o cliente está registrado
    if (senha, porta) not in [(info['senha'], info['porta']) for info in informacoes_cliente.values()]:
        return "ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD"

    # Processa a lista de arquivos
    arquivos_lista = arquivos_str.split(';')
    arquivos_atualizados = 0

    # Atualiza a lista de arquivos do cliente
    for info_arquivo in arquivos_lista:
        partes_arquivo = info_arquivo.split(',')
        if len(partes_arquivo) == 2:
            hash_arquivo, nome_arquivo = partes_arquivo[0], partes_arquivo[1]
            # Atualiza o arquivo no cliente
            informacoes_cliente[endereco_cliente]['arquivos'][nome_arquivo] = hash_arquivo
            arquivos_atualizados += 1

    return f"OK {arquivos_atualizados}_REGISTERED_FILES"

# Função para processar mensagens LST
def listar_arquivos():
    lista_arquivos = []

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

    return resposta

# Função para processar mensagens END
def desconectar_cliente(mensagem, endereco_cliente):
    if len(mensagem) != 3:
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
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.bind(ENDERECO_SERVIDOR)

    print("Servidor iniciado. Aguardando conexões.")

    while True:
        data, endereco_cliente = socket_servidor.recvfrom(BUFFER_SIZE)
        mensagem = data.decode('utf-8').split()

        if not mensagem or len(mensagem) < 2:
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
                response = "ERR INVALID_MESSAGE_FORMAT"

        socket_servidor.sendto(response.encode('utf-8'), endereco_cliente)

if __name__ == "__main__":
    main()
