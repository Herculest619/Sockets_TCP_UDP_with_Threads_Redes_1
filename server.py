import socket, sys
from threading import Thread
import mysql.connector

HOST = '127.0.0.1'  # endereço IP Localhost
#HOST = '192.168.2.27'  # endereço IP
PORT_TCP = 20000        # Porta utilizada pelo servidor
PORT_UDP = 20001        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

# Connect to database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'dispositivo'
}

db = mysql.connector.connect(**db_config)  # Conecta ao banco de dados
cursor = db.cursor()  # Cria um cursor para executar comandos SQL


def on_new_conection_tcp(clientsocket,addr):
    while (True):
        try:
            data = clientsocket.recv(BUFFER_SIZE) # recebe os dados do cliente
            if not data:  # se não receber dados, encerra a conexão
                break
            texto_recebido = data.decode('utf-8') # converte os bytes em string
            print('\nrecebido do cliente {} na porta {}: {}'.format(addr[0], addr[1],texto_recebido)) # imprime o texto recebido
            clientsocket.send(data) # envia o mesmo texto ao cliente

            '''if (texto_recebido == 'bye'): # se o texto recebido for 'bye', encerra a conexão
                print('\nvai encerrar o socket do cliente {} !'.format(addr[0])) # imprime o endereço do cliente
                clientsocket.close()  # encerra o socket do cliente
                return '''
            
            # texto_recebido = clientsocket.recv(BUFFER_SIZE).decode('utf-8') # recebe os dados do cliente e converte os bytes em string
            if (texto_recebido == 'cadastrar'):
                print("\nCADASTRAR NOVO DISPOSITIVO!")
                
            elif(texto_recebido == "listar"):
                print("\nListando os dispositivos conectados...")
                # clientsocket.send('teste123'.encode('utf-8'))
            elif(texto_recebido == "desconectar"):
                print("\nDesconectando dispositivo...")
                clientsocket.close()
                return
            else:
                print("\nComando não reconhecido!")


        except Exception as error:
            print("\nErro na conexão com o cliente!!\n")
            print(error)
            return

def on_new_conection_udp(clientsocket,addr):
    pass


def socket_tcp():
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket_tcp: #with fecha o socket ao final
            print("\nTCP server up and listening")
            server_socket_tcp.bind((HOST, PORT_TCP)) #'bind' - associa o socket a um endereço IP e porta
            while True:
                server_socket_tcp.listen() # 'listen' - habilita o socket para aceitar conexões
                clientsocket, addr = server_socket_tcp.accept() # 'accept' - aceita uma conexão e retorna um novo socket e o endereço do cliente
                print('\nConectado ao usuario no endereço:', addr) # imprime o endereço do cliente
                t = Thread(target=on_new_conection_tcp, args=(clientsocket,addr)) # cria uma thread para tratar a conexão
                t.start()   # inicia a thread
    except Exception as error:
        print("\nErro na execução do servidor!!")
        print(error)        
        return             

def socket_udp():
    try:
        # Create a datagram socket
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        UDPServerSocket.bind((HOST, PORT_TCP))
        print("UDP server up and listening")
        # Listen for incoming datagrams
        while(True):
            bytesAddressPair = UDPServerSocket.recvfrom(BUFFER_SIZE) #recebe os dados do cliente
            mensagem = bytesAddressPair[0] #converte de bytes para um formato "printável"
            endereco = bytesAddressPair[1] 
            # clientMsg = "Mensagem do cliente:{}".format(mensagem)
            # clientIP  = "Client IP Address:{}".format(endereco)
            # print(clientMsg)
            # print(clientIP)
            # envia o mesmo texto ao cliente     
            # UDPServerSocket.sendto(mensagem, endereco)

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             


def main(argv):
    #Threads para executar os sockets de TCP e UDP, para cliente e dispositivo
    thread_tcp = Thread(target=socket_tcp)
    thread_udp = Thread(target=socket_udp)

    #Inicia as threads
    thread_tcp.start()
    thread_udp.start()

    #Aguarda as threads terminarem
    thread_tcp.join()
    thread_udp.join()

if __name__ == "__main__":   
    main(sys.argv[1:])