import logging
import time
import os
from utils.configs import BUFFER_SIZE, SERVER_IP, TCP_PORT, UDP_PORT
from utils.logger import tcp_logger, udp_logger

# Função para criar uma mensagem com base no número do pacote
def criaMensagem(i):
    mensagem = f"[PACOTE #{i} " + "N" * (i * 10)+ " FIM]"
    return mensagem

# Função para criar uma mensagem com tamanho fixo de ≃1024 bytes
def criaMensagemPadrao(i):
    mensagemPadrao = f"[PACOTE #{i} " + "P" * 1008 + " FIM]"
    return mensagemPadrao

# Teste de explosão de pacotes que consiste em enviar uma quantidade abrupta de pacotes para o servidor
def explosaoDePacotes(cliente_socket, quantidade, protocolo):
    inicio = time.time()
    if protocolo == "TCP":
        for i in range(quantidade):
            mensagem = criaMensagemPadrao(i)
            cliente_socket.send(mensagem.encode())
            tcp_logger.info(f"[PACOTE] Mensagem {i} enviada para {SERVER_IP}:{TCP_PORT}. tamanho: {len(mensagem)}")
            resposta = cliente_socket.recv(BUFFER_SIZE)
            tcp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta.decode()}")
        tempo_total = (time.time() - inicio) * 1000
        tcp_logger.info(f"[METRICA] Tempo total de envio de todos os pacotes enviados: {tempo_total}ms")
    else: # UDP
        vetor_confirmacao = [False] * quantidade # Matriz de confirmação de envio
        for i in range(quantidade):
            mensagem = criaMensagemPadrao(i)
            cliente_socket.sendto(mensagem.encode(), (SERVER_IP, UDP_PORT))
            udp_logger.info(f"[PACOTE] Mensagem {i} enviada para {SERVER_IP}:{UDP_PORT}. tamanho: {len(mensagem)}")
            resposta, _ = cliente_socket.recvfrom(BUFFER_SIZE)
            confirmacao = resposta.decode().split(" ")[1]
            confirmacao = int(confirmacao[1:])
            vetor_confirmacao[confirmacao] = True
            udp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta}")
        tempo_total = (time.time() - inicio) * 1000
        udp_logger.info(f"[METRICA] Teste de explosão de pacotes finalizado. Pacotes confirmados: {vetor_confirmacao.count(True)}")
        tcp_logger.info(f"[METRICA] Tempo total de envio de todos os pacotes enviados: {tempo_total}ms")


# Função para calcular a vazão de transferência de dados, porém para o protocolo UDP que necessita do vetor de confirmação
def calculaVazaoUDP(tamanho, vetor_confirmacao, tempo_total):
    # Número de bytes de dados (payload do protocolo da aplicação) transferidos com sucesso
    numero_de_bytes = 0
    for i in range(tamanho):
        if vetor_confirmacao[i] == True:
            numero_de_bytes += 10 * i

    vazao = numero_de_bytes / (tempo_total / 1000)
    udp_logger.info(f"[METRICA] Vazão de transferência de dados: {vazao} bytes/s")

# Função para calcular a vazão de transferência de dados
def calculaVazaoTCP(tamanho, tempo_total):
    # Número de bytes de dados (payload do protocola da aplicação) transferidos com sucesso
    numero_de_bytes = 0
    for i in range(tamanho):
        numero_de_bytes += 10 * i

    vazao = numero_de_bytes / (tempo_total / 1000)
    tcp_logger.info(f"[METRICA] Vazão de transferência de dados: {vazao} bytes/s")
            
# Teste de tempo de envio de pacotes que consiste em enviar pacotes de tamanhos diferentes para o servidor
def testeTempoEnvioTCP(cliente_socket):
    tcp_logger.info(f"[METRICA] Teste de tempo de envio iniciado")
    tamanho = int(input("Digite até que tamanho de pacote será enviado. \n Começamos com 0 e aumentamos de 10 em 10 até o valor digitado: "))
    # Inicia timer
    # Envia a mensagem para o servidor
    tempo_total = time.time()
    for i in range(tamanho):
        mensagem = criaMensagem(i)
        tcp_logger.info(f"[METRICA] Tamanho da mensagem {i}: {len(mensagem)}")
        inicio = time.time()
        cliente_socket.send(mensagem.encode())
        tcp_logger.info(f"[PACOTE] Mensagem {i} enviada para {SERVER_IP}:{TCP_PORT}. tamanho: {len(mensagem)}")

        # Recebe a resposta do servidor
        resposta = cliente_socket.recv(BUFFER_SIZE)
        tcp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta.decode()}")

        # Finaliza timer
        RTT = (time.time() - inicio) * 1000 
        tcp_logger.info(f"[METRICA] Tempo p/ resposta do servidor: {RTT}ms")
    tempo_total = (time.time() - tempo_total) * 1000
    tcp_logger.info(f"[METRICA] Tempo total de envio de todos os pacotes enviados: {tempo_total}ms")
    calculaVazaoTCP(tamanho, tempo_total)

# Teste de tempo de envio de pacotes que consiste em enviar pacotes de tamanhos diferentes para o servidor
def testeTempoEnvioUDP(cliente_socket):
    udp_logger.info(f"[METRICA] Teste de tempo de envio iniciado")
    tamanho = int(input("Digite o número de pacotes que serão enviados. \nComeçamos com 0 e aumentamos de 10 em 10 até enviar o número de pacotes especificado: "))
    tempo_total = time.time()
    vetor_confirmacao = [False] * tamanho # Matriz de confirmação de envio
    for i in range(tamanho):
        mensagem = criaMensagem(i)
        udp_logger.info(f"[METRICA] Tamanho da mensagem {i}: {len(mensagem)}")
        inicio = time.time()
        cliente_socket.sendto(mensagem.encode(), (SERVER_IP, UDP_PORT))
        udp_logger.info(f"[PACOTE] Mensagem {i} enviada para {SERVER_IP}:{UDP_PORT}. tamanho: {len(mensagem)}")

        # Recebe a resposta do servidor
        resposta, _ = cliente_socket.recvfrom(BUFFER_SIZE)

        confirmacao = resposta.decode().split(" ")[1]
        confirmacao = int(confirmacao[1:]) 
        vetor_confirmacao[confirmacao] = True

        udp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta}")

        # Finaliza timer
        RTT = (time.time() - inicio) * 1000 
        udp_logger.info(f"[METRICA] Tempo p/ resposta do servidor: {RTT}ms")
    tempo_total = (time.time() - tempo_total) * 1000
    udp_logger.info(f"[METRICA] Pacotes confirmados: {vetor_confirmacao.count(True)}")
    udp_logger.info(f"[METRICA] Tempo total de envio de todos os pacotes enviados: {tempo_total}ms")
    calculaVazaoUDP(tamanho, vetor_confirmacao, tempo_total)

# --------------------------------------------------------------------------------------------------------------------------------------------------------

# Interfaces de envio de pacotes para o servidor
# Utilizam das funções acima, tendo quando necessário suas contrapartes para o protocolo UDP e TCP

def interfaceEnvioTCP(cliente_socket):
    tcp_logger.info(f"[INICIALIZACAO] Interface de envio de pacotes TCP iniciada")
    while True:
        print("Escolha a opão de envio de pacotes")
        escolha = input(" 0 - Enviar um pacote \n 1 - Teste de tempo de resposta e vazão \n 2 - Mandar um número arbitrário de pacotes com carga padrão (1024 Bytes) \n 3 - Encerrar sistema\n")

        if escolha == "0":
            print("Digite a mensagem a ser enviada")
            mensagem = input()
            mensagem = f"[PACOTE #{0} {mensagem} FIM]"
            cliente_socket.send(mensagem.encode())

            tcp_logger.info(f"[PACOTE] Mensagem enviada para {SERVER_IP}. tamanho: {len(mensagem)}")

            resposta = cliente_socket.recv(BUFFER_SIZE)
            tcp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta.decode()}")

        elif escolha == "1":
            testeTempoEnvioTCP(cliente_socket)
        elif escolha == "2":
            tamanho = int(input("Digite o número de pacotes a serem enviados: "))
            explosaoDePacotes(cliente_socket, tamanho, "TCP")
        elif escolha == "3" or KeyboardInterrupt:
            tcp_logger.info(f"[ENCERRAMENTO] Conexão encerrada com o servidor TCP")
            cliente_socket.send(b"FIM")
            cliente_socket.close()    
            exit()
            break

def interfaceEnvioUDP(cliente_socket):
    udp_logger.info(f"[INICIALIZACAO] Interface de envio de pacotes UDP iniciada")
    while True:
        print("Escolha a opão de envio de pacotes")
        escolha = input(" 0 - Enviar um pacote \n 1 - Teste de tempo de resposta e vazão \n 2 - Mandar um número arbitrário de pacotes com carga padrão (~1024 Bytes) \n 3 - Encerrar sistema\n")

        if escolha == "0":
            print("Digite a mensagem a ser enviada")
            mensagem = input()
            mensagem = f"[PACOTE #{0} {mensagem} FIM]"
            cliente_socket.sendto(mensagem.encode(), (SERVER_IP, UDP_PORT))

            udp_logger.info(f"[PACOTE] Mensagem enviada para {SERVER_IP}. tamanho: {len(mensagem)}")

            resposta, _ = cliente_socket.recvfrom(BUFFER_SIZE)
            udp_logger.info(f"[PACOTE] Resposta de {SERVER_IP}: {resposta}")

        elif escolha == "1":
            testeTempoEnvioUDP(cliente_socket)

        elif escolha == "2":
            tamanho = int(input("Digite o número de pacotes a serem enviados: "))
            explosaoDePacotes(cliente_socket, tamanho, "UDP")
        elif escolha == "3" or KeyboardInterrupt:
            udp_logger.info(f"[ENCERRAMENTO] Envio de pacotes UDP")
            cliente_socket.sendto(b"FIM", (SERVER_IP, UDP_PORT))
            cliente_socket.close()    
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue
