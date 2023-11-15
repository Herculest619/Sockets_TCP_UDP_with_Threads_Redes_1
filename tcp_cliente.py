import socket, sys, os, ast

HOST = '127.0.0.1'  # endereço IP Localhost
#HOST = '192.168.2.27'  # endereço IP
PORT_TCP = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def main(argv): 
    #limpa a tela do cmd no windows
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #with fecha o socket ao final, AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP
            s.connect((HOST, PORT_TCP)) #conecta ao servidor
            print("\nConectado ao server!")
            # s.send("cliente".encode()) #texto.encode - converte a string para bytes
            # data = s.recv(BUFFER_SIZE) #recebe os dados do servidor
            # texto_recebido = repr(data) #converte de bytes para um formato "printável"
            # print('\nRecebido do servidor', texto_recebido) #imprime o texto recebido

            '''
            s.send("listar".encode()) #texto.encode - converte a string para bytes
            data = s.recv(BUFFER_SIZE) #recebe os dados do servidor
            texto_recebido = repr(data) #converte de bytes para um formato "printável"
            print('\nRecebido do servidor', texto_recebido) #imprime o texto recebido
'''
            while(True):       
                #limpa a tela do cmd no windows
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nBem vindo ao sistema de gerenciamento de dispositivos!")
                print("\nSeleciona uma das opções abaixo:")

                print("\n1 - Cadastrar novo dispositivo")
                print("2 - Listar dispositivos")
                print("3 - Sair")

                opcao = input("\nDigite a opção desejada: ")

                if(opcao == "1"):
                    print("\nCADASTRAR NOVO DISPOSITIVO!")
                    s.send("cadastrar".encode())
                    data = s.recv(BUFFER_SIZE).decode('utf-8')

                    #conferir se a string esta vazia
                    if data == "Nenhum dispositivo encontrado!":
                        print(data)
                        input("\nPressione qualquer tecla para continuar...")
                        main(sys.argv[1:])
                        return

                    else:
                        # Convertendo a string para lista
                        data_tupla = ast.literal_eval(data)
                        print(type(data_tupla))

                        j = 0
                        for i in data_tupla:
                            if len(i) == 4:
                                print("\nID: ", j,"----> IP: ", i[0], " Tipo: ", i[1], " Valor: ", i[2], " Status: ", i[3])
                            else:
                                print("Tupla inválida: ", i)
                            j += 1

                        id = input("\nDigite o ID dispositivo que deseja cadastrar: ")
                        s.send(id.encode())

                        apelido = input("\nDigite o apelido do dispositivo: ")
                        s.send(apelido.encode())

                        msg = s.recv(BUFFER_SIZE).decode('utf-8')
                        print(msg)
                        input("\nPressione qualquer tecla para continuar...")

                elif(opcao == "2"):
                    print("\nListando os dispositivos conectados...")
                    s.send("listar".encode())

                    lampadas = s.recv(BUFFER_SIZE).decode('utf-8')
                    #testa se a string esta vazia
                    if lampadas == "Nenhuma lampada encontrada!":
                        qnt_lampadas = 0
                    else:
                        # Convertendo a string para lista
                        lampadas_tupla = ast.literal_eval(lampadas)
                        qnt_lampadas = len(lampadas_tupla)

                    tvs = s.recv(BUFFER_SIZE).decode('utf-8')
                    if tvs == "Nenhuma TV encontrada!":
                        qnt_tvs = 0
                    else:
                        # Convertendo a string para lista
                        tvs_tupla = ast.literal_eval(tvs)
                        qnt_tvs = len(tvs_tupla)

                    ars = s.recv(BUFFER_SIZE).decode('utf-8')
                    if ars == "Nenhum ar condicionado encontrado!":
                        qnt_ars = 0
                    else:
                        # Convertendo a string para lista
                        ars_tupla = ast.literal_eval(ars)
                        qnt_ars = len(ars_tupla)

                    if qnt_ars == 0 and qnt_lampadas == 0 and qnt_tvs == 0:
                        print("\nNENHUM DISPOSITIVO CADASTRADO!")
                        s.send("sem disp para alterar".encode())
                        s.send("sem disp para alterar".encode())
                        s.send("sem disp para alterar".encode())
                        input("\nPressione qualquer tecla para continuar...")
                        main(sys.argv[1:])
                        return
                    else:
                        print("\n")
                        print("*"*50)
                        print("TOTAL DE DISPOSITIVOS CADASTRADOS: ", qnt_ars + qnt_lampadas + qnt_tvs)
                        print("*"*50)

                        var = 1
                        print("\nLAMPADAS CADASTRADAS:")
                        if qnt_lampadas > 0:
                            for i in lampadas_tupla:
                                if len(i) == 5:
                                    status = "Ligado" if i[3] == 1 else "Desligado"
                                    print("ID:", var,"----> IP:", i[0], " Porta:", i[1], " Valor:", i[2], " Status:", status, " Apelido:", i[4])
                                else:
                                    print("Tupla inválida: ", i)
                                var += 1
                        else:
                            print("\nNenhuma lampada cadastrada!")
                        
                        print("\nTVs CADASTRADAS:")
                        if qnt_tvs > 0:
                            #impime as tvs cadastradas em listas
                            for i in tvs_tupla:
                                if len(i) == 5:
                                    status = "Ligado" if i[3] == 1 else "Desligado"
                                    print("ID:", var,"----> IP:", i[0], " Porta:", i[1], " Valor:", i[2], " Status:", status, " Apelido:", i[4])
                                else:
                                    print("Tupla inválida: ", i)
                                var += 1
                        else:
                            print("Nenhuma TV cadastrada!")

                        print("\nARs CADASTRADOS:")
                        if qnt_ars > 0:
                            for i in ars_tupla:
                                status = "Ligado" if i[3] == 1 else "Desligado"
                                if len(i) == 5:
                                    print("ID:", var,"----> IP:", i[0], " Porta:", i[1], " Valor:", i[2], " Status:", status, " Apelido:", i[4])
                                else:
                                    print("Tupla inválida: ", i)
                                var += 1
                        else:
                            print("Nenhum ar condicionado cadastrado!")

                        print("\n" + "*"*50)

                        try:
                            id_alteracao = int(input("\nDigite o ID do dispositivo que deseja alterar: "))
                        except:
                            print("\nID inválido!")
                            input("\nPressione qualquer tecla para continuar...")
                            main(sys.argv[1:])
                            return
                        
                        if id_alteracao > var or id_alteracao < 0:
                            print("\nID inválido!")
                            input("\nPressione qualquer tecla para continuar...")
                            main(sys.argv[1:])
                            return
                        else:
                            aux = 1
                            if qnt_lampadas > 0:
                                for i in lampadas_tupla:
                                    if aux == id_alteracao:
                                        print("aux: ", aux)
                                        ipaux = i[0]
                                        tipo = "Lampada"
                                        status_aux = i[3]
                                    aux += 1
                                
                            if qnt_tvs > 0:
                                for i in tvs_tupla:
                                    if aux == id_alteracao:
                                        print("aux: ", aux)
                                        ipaux = i[0]
                                        tipo = "Televisao"
                                        status_aux = i[3]
                                    aux += 1

                            if qnt_ars > 0:
                                for i in ars_tupla:
                                    if aux == id_alteracao:
                                        print("aux: ", aux)
                                        ipaux = i[0]
                                        tipo = "Ar-condicionado"
                                        status_aux = i[3]
                                    aux += 1

                            print("\n" + tipo + " selecionado com o IP: " + ipaux)
                            s.send(ipaux.encode())
                            s.send(tipo.encode())

                            print("\nO QUE DESEJA ALTERAR?")
                            print("\n1 - Ligar/Desligar")
                            if tipo == "Lampada":
                                print("2 - Alterar cor")
                            elif tipo == "Televisao":
                                print("2 - Alterar volume")
                            elif tipo == "Ar-condicionado":
                                print("2 - Alterar temperatura")
                            print("3 - Alterar apelido")
                            print("4 - Excluir dispositivo")

                            opcao_alteracao = input("\nDigite a opção desejada: ")
                            s.send(opcao_alteracao.encode())

                            if opcao_alteracao == "1":
                                #verifica o status atual do dispositivo
                                if status_aux == 1:
                                    print("\nDesligando o dispositivo...")
                                    s.send("desligar".encode())
                                else:
                                    print("\nLigando o dispositivo...")
                                    s.send("ligar".encode())

                            elif opcao_alteracao == "2":
                                if tipo == "Lampada":
                                    print("\nALTERAR COR!")
                                    cor = input("\nAzul, Vermelho ou Verde: ")
                                    s.send(cor.encode())
                                elif tipo == "Televisao":
                                    print("\nALTERAR VOLUME!")
                                    volume = input("\nDigite o volume desejado: ")
                                    #testa se o volume é um numero inteiro entre 0 e 100    
                                    try:
                                        volume = int(volume)
                                        if volume < 0 or volume > 100:
                                            volume = -1
                                            print("\nVolume inválido!")
                                            input("\nPressione qualquer tecla para continuar...")
                                            main(sys.argv[1:])
                                            return
                                    except:
                                        print("\nVolume inválido!")
                                        input("\nPressione qualquer tecla para continuar...")
                                        main(sys.argv[1:])
                                        return
                                    volume = str(volume)
                                    s.send(volume.encode())
                                elif tipo == "Ar-condicionado":
                                    print("\nALTERAR TEMPERATURA!")
                                    s.send("alterar temperatura".encode())
                                    temperatura = input("\nDigite a temperatura desejada: (16~30)")
                                    #testa se a temperatura é um numero inteiro entre 16 e 30
                                    try:
                                        temperatura = int(temperatura)
                                        if temperatura < 16 or temperatura > 30:
                                            temperatura = -1
                                            print("\nTemperatura inválida!")
                                            input("\nPressione qualquer tecla para continuar...")
                                            main(sys.argv[1:])
                                            return
                                    except:
                                        print("\nTemperatura inválida!")
                                        input("\nPressione qualquer tecla para continuar...")
                                        main(sys.argv[1:])
                                        return
                                    temperatura = str(temperatura)
                                    s.send(temperatura.encode())

                            elif opcao_alteracao == "3":
                                print("\nALTERAR APELIDO!")
                                apelido = input("\nDigite o novo apelido: ")
                                s.send(apelido.encode())

                            elif opcao_alteracao == "4":
                                print("\nEXCLUIR DISPOSITIVO!")

                            else:
                                print("\nOpção inválida!")
                                input("\nPressione qualquer tecla para continuar...")
                                main(sys.argv[1:])
                                return
                    mensagem = s.recv(BUFFER_SIZE).decode('utf-8')
                    print(mensagem)
                    input("\nPressione qualquer tecla para continuar...")
                    main(sys.argv[1:])
                    return
                
                elif(opcao == "3"):
                    print("\nSaindo do sistema...")
                    s.send("sair".encode())
                    s.close()
                    break

                else:
                    print("\nOpção inválida!")
                    input("\nPressione qualquer tecla para continuar...")
                    main(sys.argv[1:])
                    return

    except Exception as error:
        print("\nExceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])