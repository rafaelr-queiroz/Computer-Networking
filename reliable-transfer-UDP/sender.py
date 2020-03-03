#MIT License
#
#Copyright (c) 2020 Rafael Rodrigues Queiroz
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
#
#################################################################################
#
#
#   This script provides a sender to a reliable data transfer over a UDP socket
#
import socket
import sys


server_ip = ""
server_port = ""
num_of_messages = ""
buffer_size = 2048
# coleta argumentos passados para o script em linha de comando
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("O script sender.py deve receber 3 argumentos da linha de comando:\r\n" + 
        "argumento 1 - ip do servidor\r\n" + 
        "argumento 2 - porta do servidor (inteiro entre 10001 e 11000)\r\n" + 
        "argumento 3 - número de mensagens a serem enviadas (inteiro positivo)\r\n")
        quit()

    server_ip = sys.argv[1]         # ip do servidor
    server_port = sys.argv[2]       # porta do servidor
    num_of_messages = sys.argv[3]   # nº de mensagens a serem enviadas

# verifica se o nº da porta é um inteiro positivo. Caso seja, verifica se 
# está em um intervalo válido (10001 <= server_port <= 11000)
if not server_port.isdigit():
    print("O número da porta deve ser um inteiro entre 10001 e 11000")
    quit()
elif int(server_port) < 10001 or int(server_port) > 11000:
    print("O número da porta deve ser um inteiro entre 10001 e 11000")
    quit()

# verifica se o número de mensagens é um argumento válido, ou seja, se é um 
# inteiro positivo
if not num_of_messages.isdigit():
    print("O número de mensagens a serem enviadas deve ser um inteiro positivo")
    quit()
elif int(num_of_messages) == 0:
    print("O número de mensagens a serem enviadas deve ser um inteiro positivo")
    quit()

# cria um socket para envio/recebimento de pacotes UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# especifica um timeout de 1 segundo
client_socket.settimeout(1)

# faz um ping no servidor para verificar a existência do mesmo
client_socket.sendto("teste".encode(), ( server_ip, int(server_port)) )

try:
    test_message, ip_from_test = client_socket.recvfrom(buffer_size)
    # escreve no terminal a resposta do ping
    print("Resposta do ping: " + test_message.decode())
except socket.timeout:
    # caso o servidor não exista, informa o usuário do problema
    # fecha o socket e termina o script
    print("Endereço IP do servidor inválido")
    client_socket.close()
    quit()

seq_number = "0"                    # SEQNO
payload = 0                         # mensagem a ser enviada para o receiver
packet = ""                         # pacote no formato: SEQNO DATA MSGS

msg_counter = int(num_of_messages)

while msg_counter > 0:
    # cria string representando o pacote
    packet = seq_number + " " + str(payload) + " " + num_of_messages
    # envia pacote para o receiver e informa usuário pelo terminal
    client_socket.sendto( packet.encode(), (server_ip, int(server_port)) )
    print("SENT: " + packet)
    
    try:
        # le resposta do receiver e imprime a mesma no terminal
        received_message, ip_addr = client_socket.recvfrom(buffer_size)
        print("RECV:" + received_message.decode() + "\r\n")
    except socket.timeout:
        # caso ocorra timeout, informa o usuário do problema e reenvia
        # o pacote
        print("RECV: timeout\r\n")
        continue
    
    if len(received_message) != 5:          # valida comprimento do pacote enviado pelo receiver
        continue
    elif received_message[0:3] != "ACK ":   # valida se pacote possui a substring "ACK "
        continue
    elif received_message[4] != seq_number: # valida o nº da sequência do pacote
        continue

    # caso todas as validações estejam ok, alterna o sequence number, incrementa o payload
    # e decrementa msg_counter para enviar o próximo pacote
    if seq_number == "0":
        seq_number = "1"
    else:
        seq_number = "0"

    payload += 1
    msg_counter -= 1

# fecha o socket e termina o script
client_socket.close()