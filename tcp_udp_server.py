import socket, sys, struct, os
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

#Prototipo de descoberta de dispositivos
'''
def discover_server():
    # Configuração do socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Use o endereço de broadcast local
    broadcast_address = '127.255.255.255'
    server_address = ('', 20002)

    # Liga o socket ao endereço do servidor
    udp_socket.bind(server_address)

    # Envia uma mensagem de descoberta
    message = 'DESCOBERTA'
    udp_socket.sendto(message.encode(), (broadcast_address, 20002))
'''

def send_data_to_server(data, server_ip, port):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(data.encode(), (server_ip, port))
        udp_socket.close()
    except Exception as error:
        print("\nErro ao enviar dados para o servidor")
        print(error)
        return

def scanIP():
    # Inicialização da lista de IPs fora do loop
    ips = []
    i = 0

    # Testa conexão com todos os IPs da rede para encontrar dispositivos disponíveis
    for ip in range(1, 255):
        addr = '127.0.0.' + str(ip)

        try:
            # with fecha o socket ao final, AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as UDPClientSocket:
                UDPClientSocket.settimeout(1.0)  # Tempo de espera para resposta do servidor
                # Envia texto para o servidor
                UDPClientSocket.sendto("conectar".encode(), (addr, 20002))

                msg = UDPClientSocket.recvfrom(BUFFER_SIZE)[0].decode('utf-8')
                
                if msg == "lampada" or msg == "tv" or msg == "ar_condicionado":
                    valor = UDPClientSocket.recvfrom(BUFFER_SIZE)[0].decode('utf-8')
                    status = UDPClientSocket.recvfrom(BUFFER_SIZE)[0].decode('utf-8')
                    print(msg, "encontrado no IP:", addr)
                    ips.append([addr, msg, valor, status])  # Adiciona o IP à lista
            UDPClientSocket.close()

        except Exception as error:
            if error.errno != 10054:
                print(error, ip)
            # Se houver uma exceção, ela será tratada e o loop continuará

    # Retorna a lista com os IPs encontrados
    print("\nRetornando lista de IPs encontrados...")
    return ips

def on_new_conection_tcp(clientsocket,addr):
    while (True):
        try:
            data = clientsocket.recv(BUFFER_SIZE) # recebe os dados do cliente
            if not data:  # se não receber dados, encerra a conexão
                break
            texto_recebido = data.decode('utf-8') # converte os bytes em string
            print('\nrecebido do cliente {} na porta {}: {}'.format(addr[0], addr[1],texto_recebido)) # imprime o texto recebido

            if (texto_recebido == 'cadastrar'):
                print("\nCADASTRAR NOVO DISPOSITIVO!")
                # ip_dispositivo = input("\nDigite o IP do dispositivo: ")

                ips_dis = scanIP()

                if ips_dis == []:
                    print("\nNenhum dispositivo encontrado!")
                    clientsocket.sendto("\nNenhum dispositivo encontrado!".encode(), addr)
                    return
                else:
                    print("\nDispositivos encontrados: ")
                    print(ips_dis)
                    
                    #testa se algum ip ja esta cadastrado no banco de dados
                    sql = "SELECT IP FROM lampada"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for i in result:
                        for j in ips_dis:
                            if i[0] == j[0]:
                                ips_dis.remove(j)
                                print("\nRemovendo ip: ", j[0])

                    print("\nResultado após comparar com BD: ", ips_dis)
                    if ips_dis == []:
                        print("\nNenhum dispositivo encontrado!")
                        clientsocket.sendto("Nenhum dispositivo encontrado!".encode(), addr)
                        return

                    string = str(ips_dis)
                    clientsocket.sendto(string.encode(), addr)

                    id = int(clientsocket.recv(BUFFER_SIZE).decode('utf-8'))
                    apelido = clientsocket.recv(BUFFER_SIZE).decode('utf-8')

                    try:
                        sql = "INSERT INTO lampada (IP, porta, valor, status, apelido) VALUES (%s, %s, %s, %s, %s)"
                        val = (ips_dis[id][0], 20002, ips_dis[id][2], ips_dis[id][3], apelido)
                        cursor.execute(sql, val)
                        db.commit()
                        print("lampada inserida.")
                    except Exception as error:
                        # se ja existir, cancela a inserção, e avisa o usuário que o dispositivo já está cadastrado
                        if error.errno == 1062:
                            print("Dispositivo já cadastrado!")
                            return
                        else:
                            print(error)

                
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