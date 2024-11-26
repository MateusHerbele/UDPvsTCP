import logging
import time
import os
from utils.configs import LOG_LEVEL, BUFFER_SIZE, SERVER_IP, TCP_PORT, UDP_PORT
from utils.logger import tcp_logger, udp_logger
# ou udp_logger se for o caso

# # Configuração do logging
# logging.basicConfig(
#     level=LOG_LEVEL,
#     format="%(asctime)s [%(levelname)s] %(message)s",
# )
# Configuração do logging
# log_file = os.path.join(os.path.dirname(__file__), '../../data/logs/cliente.log')  # Define o arquivo de log

# logging.basicConfig(
#     level=LOG_LEVEL,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         logging.StreamHandler(),  # Log no console
#         logging.FileHandler(log_file, mode='a', encoding='utf-8')  # Log no arquivo
#     ]
# )
def criaMensagem(tamanho, i):
    mensagem = f"[PACOTE #{i} " + "N" * (tamanho * 10)+ " FIM]"
    return mensagem

def testeTempoEnvioTCP(cliente_socket):
    tcp_logger.info(f"[METRICA] Teste de tempo de envio iniciado")
    tamanho = int(input("Digite até que tamanho de pacote será enviado. \n Começamos com 0 e aumentamos de 10 em 10 até o valor digitado: "))
    # Inicia timer
    # Envia a mensagem para o servidor
    tempo_total = time.time()
    for i in range(tamanho):
        mensagem = criaMensagem(tamanho, i)
        tcp_logger.info(f"[METRICA] Tamanho da mensagem {i}: {len(mensagem)}")
        inicio = time.time()
        cliente_socket.send(mensagem.encode())
        tcp_logger.info(f"[PACOTE] Mensagem {i} enviada para {SERVER_IP}:{TCP_PORT}: {mensagem}")

        # Recebe a resposta do servidor
        resposta = cliente_socket.recv(BUFFER_SIZE)
        tcp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta.decode()}")

        # Finaliza timer
        RTT = (time.time() - inicio) * 1000 
        tcp_logger.info(f"[METRICA] Tempo p/ resposta do servidor: {RTT}ms")
    tempo_total = (time.time() - tempo_total) * 1000
    tcp_logger.info(f"[METRICA] Tempo total de envio de todos os pacotes enviados: {tempo_total}ms")

def testeTempoEnvioUDP(cliente_socket):
    udp_logger.info(f"[METRICA] Teste de tempo de envio iniciado")
    tamanho = int(input("Digite até que tamanho de pacote será enviado. \nComeçamos com 0 e aumentamos de 10 em 10 até o valor digitado: "))
    # Inicia timer
    # Envia a mensagem para o servidor
    tempo_total = time.time()
    for i in range(tamanho):
        mensagem = criaMensagem(tamanho, i)
        udp_logger.info(f"[METRICA] Tamanho da mensagem {i}: {len(mensagem)}")
        inicio = time.time()
        cliente_socket.sendto(mensagem.encode(), (SERVER_IP, UDP_PORT))
        udp_logger.info(f"[PACOTE] Mensagem {i} enviada para {SERVER_IP}:{UDP_PORT}: {mensagem}")

        # Recebe a resposta do servidor
        resposta = cliente_socket.recvfrom(BUFFER_SIZE)
        udp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta}")

        # Finaliza timer
        RTT = (time.time() - inicio) * 1000 
        udp_logger.info(f"[METRICA] Tempo p/ resposta do servidor: {RTT}ms")
    tempo_total = (time.time() - tempo_total) * 1000
    udp_logger.info(f"[METRICA] Tempo total de envio de todos os pacotes enviados: {tempo_total}ms")

# definir as métricas de avaliação da rede
# Aqui vamos fazer tanto pro udp quanto pro tcp
# e temos que receber o socket que o cliente está usando 
def interfaceEnvioTCP(cliente_socket):
    tcp_logger.info(f"[INICIALIZACAO] Interface de envio de pacotes TCP iniciada")
    while True:
        print("Escolha a opão de envio de pacotes")
        escolha = input(" 0 - Enviar um pacote \n 1 - Teste de tempo de resposta \n 2 - Teste de vazão \n 3 - Encerrar conexão\n")

        if escolha == "0":
            print("Digite a mensagem a ser enviada")
            mensagem = input()
            mensagem = f"[PACOTE #{0} {mensagem} FIM]"
            cliente_socket.send(mensagem.encode())

            #tcp_logger.info(f"Mensagem enviada para {SERVER_IP}: {mensagem}")
            tcp_logger.info(f"[PACOTE] Mensagem enviada para {SERVER_IP}: {mensagem}")

            resposta = cliente_socket.recv(BUFFER_SIZE)
            #tcp_logger.info(f"Resposta de {SERVER_IP}: {resposta.decode()}")
            tcp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta.decode()}")

        elif escolha == "1":
            testeTempoEnvioTCP(cliente_socket)
        elif escolha == "3" or KeyboardInterrupt:
            #tcp_logger.info("Encerrando conexão com o servidor TCP")
            tcp_logger.info(f"[ENCERRAMENTO] Conexão encerrada com o servidor TCP")
            cliente_socket.send(b"FIM")
            cliente_socket.close()    
            break

def interfaceEnvioUDP(cliente_socket):
    udp_logger.info(f"[INICIALIZACAO] Interface de envio de pacotes UDP iniciada")
    while True:
        print("Escolha a opão de envio de pacotes")
        escolha = input(" 0 - Enviar um pacote \n 1 - Teste de tempo de resposta \n 2 - Teste de vazão \n 3 - Encerrar sistema\n")

        if escolha == "0":
            print("Digite a mensagem a ser enviada")
            mensagem = input()
            mensagem = f"[PACOTE #{0} {mensagem} FIM]"
            cliente_socket.sendto(mensagem.encode(), (SERVER_IP, UDP_PORT))

            #udp_logger.info(f"Mensagem enviada para {SERVER_IP}: {mensagem}")
            udp_logger.info(f"[PACOTE] Mensagem enviada para {SERVER_IP}: {mensagem}")

            resposta = cliente_socket.recvfrom(BUFFER_SIZE)
            #udp_logger.info(f"Resposta de {SERVER_IP}: {resposta}")
            udp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta}")

        elif escolha == "1":
            testeTempoEnvioUDP(cliente_socket)
        elif escolha == "3" or KeyboardInterrupt:
            #udp_logger.info("Encerrando o sistema de envio de pacotes UDP")
            udp_logger.info(f"[ENCERRAMENTO] Envio de pacotes UDP")
            cliente_socket.sendto(b"FIM", (SERVER_IP, UDP_PORT))
            cliente_socket.close()    
            break
