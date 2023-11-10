import socket, sys

HOST = '127.0.0.1'  # endereço IP Localhost
#HOST = '192.168.2.27'  # endereço IP
PORT_TCP = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #with fecha o socket ao final, AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP
            s.connect((HOST, PORT_TCP)) #conecta ao servidor
            print("\nConectado ao server!")
            s.send("cliente".encode()) #texto.encode - converte a string para bytes
            data = s.recv(BUFFER_SIZE) #recebe os dados do servidor
            texto_recebido = repr(data) #converte de bytes para um formato "printável"
            print('\nRecebido do servidor', texto_recebido) #imprime o texto recebido

            '''
            s.send("listar".encode()) #texto.encode - converte a string para bytes
            data = s.recv(BUFFER_SIZE) #recebe os dados do servidor
            texto_recebido = repr(data) #converte de bytes para um formato "printável"
            print('\nRecebido do servidor', texto_recebido) #imprime o texto recebido
'''
            while(True):       
                texto = input("\nDigite o texto a ser enviado ao servidor:\n")
                s.send(texto.encode()) #texto.encode - converte a string para bytes
                '''data = s.recv(BUFFER_SIZE) #recebe os dados do servidor
                texto_recebido = repr(data) #converte de bytes para um formato "printável"
                print('\nRecebido do servidor', texto_recebido) #imprime o texto recebido
                texto_string = data.decode('utf-8') #converte os bytes em string
                if (texto_string == 'bye'):
                    print('\nvai encerrar o socket cliente!')
                    s.close()
                    break'''
    except Exception as error:
        print("\nExceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])