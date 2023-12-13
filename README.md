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
- `<DIRETORIO>` é o path do diretório contendo os arquivos a serem compartilhados e onde os arquivos baixados serão salvos. 

### Fluxo de Execução do Cliente
Ao ser executado, o cliente realiza as seguintes ações:
1. Decide uma senha para se registrar no servidor. O usuário pode optar por inserir uma senha manualmente ou ter ela gerada automaticamente
2. Checa se o path do diretorio informado existe, caso não exista, pergunta ao usuário caso ele deseje criá-lo
3. Descobre uma porta TCP disponível para aceitar conexões de outros clientes.
4. Envia uma requisição para se registar no servidor
3. Lista os arquivos que deseja compartilhar.
4. Envia uma mensagem de registro para o servidor.

Paralelamente, o cliente:
- Aceita conexões TCP de outros clientes para envio de arquivos na porta informada ao servidor.
- Interage com o usuário, recebendo comandos para:
  * Listar arquivos disponíveis na rede.
  * Baixar um arquivo.
  * Desconectar do cliente.

Devido à necessidade de executar atividades paralelas, o uso de threads é essencial na implementação do cliente.

## Mensagens

### REG
Mensagem de registro de um novo cliente. O formato da mensagem é:
`REG <SENHA> < q> <ARQUIVOS>`
SENHA é uma palavra secreta qualquer, composta por letras e números, escolhida pelo cliente.
PORTA é a porta TCP que o cliente estará disponível para enviar arquivos para outros clientes.
ARQUIVOS é uma lista de arquivos que o cliente deseja compartilhar com outros clientes. 
O formato dessa lista é `MD51,NOME1;MD52,NOME2;MD53,NOME3;...;MD5N,NOMEN`

onde MD5i é o hash MD5 do arquivo NOMEi. O hash do arquivo e seu respectivo nome são
separados por vírgula, e múltiplos arquivos são separados por ponto e vírgula.
O formato da mensagem de resposta é `OK <N>_REGISTERED_FILES`
onde N é o número de arquivos que o cliente compartilha com outros clientes.

### UPD
Mensagem de atualização de arquivos e porta de um cliente. O formato da mensagem é:
`UPD <SENHA> <PORTA> <ARQUIVOS>`
SENHA é a palavra secreta, composta por letras e números, utilizada pelo cliente, quando o mesmo
se registrou.
PORTA é a porta TCP que o cliente estará disponível para enviar arquivos para outros clientes.
ARQUIVOS é uma lista de arquivos que o cliente deseja compartilhar com outros clientes. O formato
dessa lista é:
`MD51,NOME1;MD52,NOME2;MD53,NOME3;...;MD5N,NOMEN`
Há dois tipos de mensagens de resposta, o primeiro quando a senha está correta:
`OK <N>_REGISTERED_FILES`
e o segundo quando a senha está incorreta:
`ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD`

### LST
Mensagem de listagem de arquivos. O formato da mensagem é:
`LST`
O formato da mensagem de resposta é
`MD51,NOME1,IP1:PORTA1,IP2:PORTA2,...,IPN:PORTAN;MD52,NOME2,IP1:PORTA1,...`
que é uma string única, sem espaços, onde cada arquivo é separado por ponto e vírgula. Cada arquivo é composto pelo hash MD5 do arquivo, seu nome, e uma lista de IPs e portas, separados por dois pontos, de clientes que possuem o arquivo.

### END
Mensagem de desconexão de um cliente, informando ao servidor que o cliente não estará mais disponível para compartilhar arquivos. O formato da mensagem é:
`END <SENHA> <PORTA>`
em que SENHA é a palavra secreta, composta por letras e números, utilizada pelo cliente, quando
o mesmo se registrou, e PORTA é a porta TCP que o cliente estava disponível para enviar arquivos para
outros clientes.
Há dois tipos de mensagens de resposta, o primeiro quando a senha está correta:
`OK CLIENT_FINISHED`
e o segundo quando a senha está incorreta:
`ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD`
## Conclusão
Esta documentação fornece um guia conciso e claro sobre a configuração e operação do sistema de compartilhamento de arquivos. A compreensão detalhada desta documentação é crucial para qualquer desenvolvedor ou usuário que pretenda trabalhar com ou expandir o sistema. Encorajamos a revisão e familiarização com o código-fonte para uma compreensão mais profunda das funções específicas e da arquitetura do sistema.
