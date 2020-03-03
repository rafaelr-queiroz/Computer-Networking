# reliable-transfer-UDP

Este projeto contempla um sender e um receiver com transporte confiável de dados sobre sockets UDP.

# Como utilizar os scripts:

    Serão necessários no mínimo dois computadores ou um computador e uma máquina virtual. Em um dos
    computadores, abra um prompt de comando com um ambiente python 3.8+ e rode o script receiver.py
    conforme a seguinte linha de comando:

    python receiver.py <porta do receiver>

    No caso, <porta do receiver> deve ser um número inteiro entre 10001 e 11000 e representa o núme 
    -ro da porta para o socket UDP do receiver. A partir deste momento o receiver irá aguardar o re  
    -metente (sender) enviar algum pacote UDP para seu ip local na porta: <porta do receiver>.

    No outro computador abra um prompt de comando com um ambiente python 3.8+ e rode sender.py com a
    seguinte linha de comando:

    python sender.py <ip do receiver> <porta do receiver> <nº de mensagens a serem enviadas>

    No caso, <ip do receiver> é o endereço IPv4 do host que estiver rodando o script receiver.py, já
    <porta do receiver> deve ser o mesmo número inserido como argumento para o script receiver.py e o
    parâmetro <nº de mensagens a serem enviadas> é um número inteiro positivo (N) que representa quan
    -tos pacotes o sender enviará para o receiver e este deverá reconhecer.

    Após isso, o script sender.py irá verificar a existência do par ip/porta especificados (informan
    -do quaisquer erros ao usuário) e caso esteja tudo ok, irá enviar N mensagens para o receiver com
    o seguinte formato:

    SEQNO DATA MSGS

    onde SEQNO é um número que alterna entre 0 e 1, DATA é um número que inicia em 0 e vai até N-1 e 
    MSGS = <nº de mensagens a serem enviadas> = N. A cada mensagem reconhecida pelo receiver o número
    SEQNO alterna de valor e DATA é incrementado para a próxima mensagem. Por exemplo, se o sender en
    -viar 5 mensagens para o receiver que escuta na porta 10500 com ip: 192.168.1.120, teríamos:

    linha de comando para receiver.py:

    python receiver.py 10500

    linha de comando para sender.py:

    python sender.py 192.168.1.120 10500 5

    Se tudo ocorresse ok, teríamos no terminal do sender:
    -------------------------------------------------------------------------------------------------
    Resposta do ping: pong

    SENT: 0 0 5
    RECV: ACK 0

    SENT: 1 1 5
    RECV: ACK 1

    SENT: 0 2 5
    RECV: ACK 0

    SENT: 1 3 5
    RECV: ACK 1

    SENT: 0 4 5
    RECV: ACK 0
    -------------------------------------------------------------------------------------------------

    No terminal do receiver:
    -------------------------------------------------------------------------------------------------
    RECV: 0 0 5
    SENT: ACK 0

    RECV: 1 1 5
    SENT: ACK 1

    RECV: 0 2 5
    SENT: ACK 0

    RECV: 1 3 5
    SENT: ACK 1

    RECV: 0 4 5
    SENT: ACK 0
    -------------------------------------------------------------------------------------------------
    

    Note que a resposta do receiver é sempre ACK SEQNO, ou seja, o número SEQNO está ligado a qual ACK
    server como reconhecimento de uma mensagem do sender.

    Obs: Quaisquer erros na chamada dos scripts, a execução é terminada com uma mensagem sobre o proble
    -ma para o usuário. Os scripts terminam automaticamente quando todas as mensagens são enviadas e re
    -conhecidas. Exemplo de erro na chamada do script:

    python receiver.py 12000
    O número da porta deve ser um inteiro entre 10001 e 11000 --> mensagem de erro

    
