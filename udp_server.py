#https://pythontic.com/modules/socket/udp-client-server-example

import socket, sys
from threading import Thread

HOST = '127.0.0.1'  # endereço IP
PORT = 20001        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

def main(argv):
    try:
        # Create a datagram socket
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        UDPServerSocket.bind((HOST, PORT))
        print("UDP server up and listening")
        # Listen for incoming datagrams
        while(True):
            bytesAddressPair = UDPServerSocket.recvfrom(BUFFER_SIZE) #recebe os dados do cliente
            mensagem = bytesAddressPair[0] #converte de bytes para um formato "printável"
            endereco = bytesAddressPair[1] 
            clientMsg = "Mensagem do cliente:{}".format(mensagem)
            clientIP  = "Client IP Address:{}".format(endereco)
        
            print(clientMsg)
            print(clientIP)
            # envia o mesmo texto ao cliente     
            UDPServerSocket.sendto(mensagem, endereco)

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])