import socket, sys
from threading import Thread

HOST = '127.0.0.1'  # endereço IP Localhost
#HOST = '192.168.2.22'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

def on_new_client(clientsocket,addr):
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE) # recebe os dados do cliente
            if not data:  # se não receber dados, encerra a conexão
                break
            texto_recebido = data.decode('utf-8') # converte os bytes em string
            print('\nrecebido do cliente {} na porta {}: {}'.format(addr[0], addr[1],texto_recebido)) # imprime o texto recebido
            clientsocket.send(data) # envia o mesmo texto ao cliente
            if (texto_recebido == 'bye'): # se o texto recebido for 'bye', encerra a conexão
                print('\nvai encerrar o socket do cliente {} !'.format(addr[0])) # imprime o endereço do cliente
                clientsocket.close()  # encerra o socket do cliente
                return 
        except Exception as error:
            print("\nErro na conexão com o cliente!!")
            return


def main(argv):
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #with fecha o socket ao final
            server_socket.bind((HOST, PORT)) #'bind' - associa o socket a um endereço IP e porta
            while True:
                server_socket.listen() # 'listen' - habilita o socket para aceitar conexões
                clientsocket, addr = server_socket.accept() # 'accept' - aceita uma conexão
                print('\nConectado ao cliente no endereço:', addr) # imprime o endereço do cliente
                t = Thread(target=on_new_client, args=(clientsocket,addr)) # cria uma thread para tratar a conexão
                t.start()   # inicia a thread
    except Exception as error:
        print("\nErro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])