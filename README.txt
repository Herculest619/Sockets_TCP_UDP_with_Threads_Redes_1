Aplicação de Interação entre Cliente e Dispositivos com Servidor Intermediário.
Este projeto utiliza conceitos de TCP/IP, UDP/IP, Banco de Dados e Threads para facilitar a interação entre clientes e dispositivos por meio de um servidor intermediário.

## Vídeo no youtube: 
https://youtu.be/wr23oIbEfsM

## Banco de Dados
1. Certifique-se de que o MySQL está instalado na máquina onde o servidor será executado.
2. Execute o script SQL "dispositivo.sql" no MySQL para criar o banco de dados necessário.
3. Altere as configurações de usuário e senha no arquivo "tcp_udp_server.py" nas linhas 12 a 16.

## Servidor e Dispositivos
1. Execute o servidor principal usando "tcp_udp_server.py".
2. Execute os dispositivos específicos, como "udp_lampada.py", "udp_tv.py" e "udp_ar_condicionado.py". A ordem de execução não é crucial.

## Cliente
1. Execute o arquivo "tcp_cliente.py" para interagir com os dispositivos por meio do servidor.



**Observações Importantes:**
- Certifique-se de que todas as dependências necessárias estejam instaladas.
- Adapte as configurações do MySQL e outras dependências conforme necessário.