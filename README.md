# Documentação do Protocolo e Implementação

## Sumário
- [Introdução](#introdução)
- [Arquivo Servidor (`servidor.py`)](#arquivo-servidor-servidorpy)
- [Arquivo Cliente (`cliente.py`)](#arquivo-cliente-clientepy)
- [Execução](#execução)
- [Fluxo de Execução do Cliente](#fluxo-de-execução-do-cliente)
- [Conclusão](#conclusão)

## Introdução
Esta documentação detalha a implementação e o funcionamento do protocolo de comunicação entre um servidor e múltiplos clientes em uma rede de compartilhamento de arquivos. Ela oferece uma visão geral sobre como executar e interagir com os componentes do sistema.

## Arquivo Servidor (`servidor.py`)
O `servidor.py` é o arquivo principal do servidor. Ele gerencia as conexões e as requisições dos clientes, mantendo o registro dos arquivos disponíveis na rede e gerenciando as atualizações dos clientes.

### Execução
Para iniciar o servidor, execute o seguinte comando no terminal:

`python3 servidor.py`


## Arquivo Cliente (`cliente.py`)
O `cliente.py` é o arquivo principal do cliente, que interage com a rede para compartilhar e baixar arquivos. Além do arquivo principal, podem existir outros arquivos auxiliares para ajudar na execução do cliente.

### Execução
Para iniciar o cliente, utilize o comando:

`python3 cliente.py <IP> <DIRETORIO>`

Onde:
- `<IP>` é o endereço IP do servidor.
- `<DIRETORIO>` é o diretório contendo os arquivos a serem compartilhados e onde os arquivos baixados serão salvos.

### Fluxo de Execução do Cliente
Ao ser executado, o cliente realiza as seguintes ações:
1. Descobre uma porta TCP disponível para aceitar conexões de outros clientes.
2. Decide uma senha para se registrar no servidor.
3. Lista os arquivos que deseja compartilhar.
4. Envia uma mensagem de registro para o servidor.

Paralelamente, o cliente:
- Aceita conexões TCP de outros clientes para envio de arquivos na porta informada ao servidor.
- Interage com o usuário, recebendo comandos para:
  * Listar arquivos disponíveis na rede.
  * Baixar um arquivo.
  * Desconectar do cliente.

Devido à necessidade de executar atividades paralelas, o uso de threads é essencial na implementação do cliente.

## Conclusão
Esta documentação fornece um guia conciso e claro sobre a configuração e operação do sistema de compartilhamento de arquivos. A compreensão detalhada desta documentação é crucial para qualquer desenvolvedor ou usuário que pretenda trabalhar com ou expandir o sistema. Encorajamos a revisão e familiarização com o código-fonte para uma compreensão mais profunda das funções específicas e da arquitetura do sistema.
