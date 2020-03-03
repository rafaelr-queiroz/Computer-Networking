import socket
import sys

server_port = ""
buffer_size = 2048

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("O script receiver.py deve receber 1 argumento da linha de comando:\r\n" + 
        "argumento 1 - porta do servidor (inteiro entre 10001 e 11000)\r\n")
        quit()
    server_port = sys.argv[1]       # recebe porta do receivr especificada em linha de comando

# valida se o nº da porta é um inteiro entre 10001 e 11000. Caso não seja, informa o usuário
# e termina o script
if not server_port.isdigit():
    print("O nº da porta deve ser um inteiro entre 10001 e 11000")
    quit()
elif int(server_port) < 10001 or int(server_port) > 11000:
    print("O nº da porta deve ser um inteiro entre 10001 e 11000")
    quit()

# cria um socket para envio/recebimento de pacotes UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# especifica o ip do host local e a porta de escuta para o socket
server_socket.bind( ('', int(server_port)) )
 
num_of_sent_ack = 0     
num_of_ack_to_be_sent = -1
seq_number = "0"
payload = ""
answer = ""

while True:
    # lê o que o sender enviar
    received_message, ip_address = server_socket.recvfrom(buffer_size)
    # cria uma lista: tokens = [SEQNO, DATA, MSGS]
    tokens = received_message.decode().split(' ')

    # verifica se há um número de sequência
    if not tokens[0].isdigit():
        print("Mensagem sem número de sequência")
        continue
    # verifica se o total de mensagens está especificado na mensagem recebida
    if not tokens[2].isdigit():
        print("Mensagem sem especificação do número total de mensagens")
        continue
    # se a mensagem estiver corretamente formatada, extrai o número total de mensagens
    # para que o receiver saiba quantas mensagens devem ser reconhecidas
    if num_of_ack_to_be_sent < 0:
        num_of_ack_to_be_sent = int(tokens[2])
    
    print("RECV: " + received_message.decode())

    # se o número de sequência estiver correto, extrai o dado e incrementa o
    # número de mensagens reconhecidas
    if tokens[0] == seq_number:
        payload = tokens[1]
        num_of_sent_ack += 1

    # cria string para ack de acordo com o número de sequência que chegou
    answer = "ACK " + tokens[0]

    # envia ack para o sender
    server_socket.sendto(answer.encode(), ip_address)

    print("SENT: " + answer + "\r\n")

    if num_of_sent_ack == num_of_ack_to_be_sent:
        break

# fecha o socket e termina o script
server_socket.close()
     

