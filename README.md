# Documentação do Protocolo e Implementação

## Sumário
- [Introdução](#introdução)
- [Arquivo Cliente (`cliente.py`)](#arquivo-cliente-clientepy)
- [Arquivo Servidor (`servidor.py`)](#arquivo-servidor-servidorpy)
- [Fluxo de Execução](#fluxo-de-execução)
- [Conclusão](#conclusão)

## Introdução
Este documento descreve a implementação e o funcionamento do protocolo utilizado na comunicação entre cliente e servidor. O objetivo é fornecer informações suficientes para que outros desenvolvedores possam compreender e trabalhar com o código.

## Arquivo Cliente (`cliente.py`)
O arquivo `cliente.py` implementa a lógica do cliente em uma rede de compartilhamento de arquivos. Principais funções:

- `gerar_senha()`: Gera uma senha aleatória.
- `string_arquivos()`: Lista os arquivos disponíveis no diretório do cliente.
- `porta_disponivel()`, `descobre_porta_disponivel()`: Verifica e encontra uma porta de rede disponível.
- `configurar_ambiente()`: Configura o ambiente inicial do cliente.
- `envia_recebe_udp()`: Envia e recebe mensagens via UDP.
- `menu_selecionar_arquivo()`, `menu_selecionar_host()`: Interfaces de usuário para selecionar arquivos e hosts.
- `requisita_arquivo()`: Requisita um arquivo de outro cliente.
- `controle_tcp()`, `controle_udp()`: Gerencia as conexões TCP e UDP.

## Arquivo Servidor (`servidor.py`)
O arquivo `servidor.py` implementa a lógica do servidor. Principais funções:

- `registrar_cliente()`: Registra um novo cliente no servidor.
- `atualizar_cliente()`: Atualiza informações de um cliente registrado.
- `listar_arquivos()`: Lista todos os arquivos disponíveis na rede.
- `desconectar_cliente()`: Desconecta um cliente do servidor.
- `main()`: Função principal que inicia o servidor e aguarda mensagens dos clientes.

## Fluxo de Execução
1. **Início do Cliente**: O cliente inicia, configura seu ambiente e inicia os serviços TCP e UDP.
2. **Registro no Servidor**: O cliente se registra no servidor via UDP, enviando suas informações.
3. **Listagem e Seleção de Arquivos**: O cliente pode solicitar a lista de arquivos disponíveis e selecionar um para download.
4. **Transferência de Arquivos**: A transferência de arquivos ocorre através de uma conexão TCP entre os clientes.
5. **Atualização e Encerramento**: O cliente pode atualizar suas informações no servidor ou se desconectar.

## Conclusão
Esta documentação apresenta uma visão geral da implementação do cliente e do servidor. É importante que futuros desenvolvedores revisem o código-fonte para uma compreensão mais detalhada das funcionalidades específicas.
