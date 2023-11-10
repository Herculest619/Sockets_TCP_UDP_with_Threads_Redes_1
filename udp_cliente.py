import socket, sys


HOST = '127.0.0.1'  # endereço IP
PORT = 20001        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def main(argv): 
    try:
        # Cria o socket UDP
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as UDPClientSocket:
            # Envia texto para o servidor
            texto = input("Digite o texto a ser enviado ao servidor:\n")
            UDPClientSocket.sendto(texto.encode(), (HOST, PORT))
            msgFromServer = UDPClientSocket.recvfrom(BUFFER_SIZE)
            msg = "Message do servidor {}".format(msgFromServer[0])
            print(msg)

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])