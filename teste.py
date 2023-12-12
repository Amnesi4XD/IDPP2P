def menu_selecionar_arquivo(lista_arquivos):
    arquivos = lista_arquivos.split(';')
    print('Selecione um arquivo que deseja baixar:')
    for i, arquivo_info in enumerate(arquivos):
        md5, nome, *hosts = arquivo_info.split(',')
        print(f'{i+1} - Nome: {nome}, Hash: {md5}')

    opcao = int(input('\nOpção: '))
    arquivo_selecionado = arquivos[opcao - 1]
    return arquivo_selecionado

def menu_selecionar_host(arquivo_selecionado):
    _ , nome, *hosts = arquivo_selecionado.split(',')
    
    print(f'\nSelecione um host para baixar o arquivo "{nome}":')
    for i, host_info in enumerate(hosts):
        ip, porta = host_info.split(':')
        print(f'{i+1} - IP: {ip}, Porta: {porta}')

    opcao = int(input('\nOpção: '))
    host_selecionado = hosts[opcao - 1]
    return host_selecionado

# Exemplo de uso
lista_arquivos = '698dc19d489c4e4db73e28a713eab07b,teste1.txt,127.0.0.1:31337;938e48f757d17fbf400e2cbf066eb6b3,teste2.bin,127.0.0.1:31337'
arquivo_selecionado = menu_selecionar_arquivo(lista_arquivos)
host_selecionado = menu_selecionar_host(arquivo_selecionado)

print(f'\nVocê selecionou o arquivo "{arquivo_selecionado}" do host "{host_selecionado}" para download.')
