import socket, sys, os

HOST = '127.0.0.19'  # endereço IP Localhost
#HOST = '192.168.2.27'  # endereço IP
PORT = 20002        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

def main(argv):
    valor = "branco"
    status = 1

    try:
        # Create a datagram socket
        # SOCK_DGRAM - UDP, AF_INET - IPv4
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        UDPServerSocket.bind((HOST, PORT))
        print("Lampada UDP server up and listening")
        # Listen for incoming datagrams
        while(True):
            bytesAddressPair = UDPServerSocket.recvfrom(BUFFER_SIZE) #recebe os dados do cliente
            mensagem = bytesAddressPair[0].decode() #converte de bytes para um formato "printável"
            endereco = bytesAddressPair[1] 
            # clientMsg = "Mensagem do cliente:{}".format(mensagem)
            # clientIP  = "Client IP Address:{}".format(endereco)
        
            # print(clientMsg)
            # print(clientIP)
            # # envia o mesmo texto ao cliente     
            # UDPServerSocket.sendto(mensagem, endereco)

            if(mensagem == "conectar"):
                print("Conectando a lampada...")
                UDPServerSocket.sendto("lampada".encode(), endereco)
                UDPServerSocket.sendto(valor.encode(), endereco)
                UDPServerSocket.sendto(str(status).encode(), endereco)

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])