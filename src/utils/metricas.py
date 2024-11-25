import logging
import time
from utils.configs import LOG_LEVEL, BUFFER_SIZE, SERVER_IP, TCP_PORT, UDP_PORT

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def criaMensagem(tamanho, i):
    mensagem = f"[PACOTE #{i} " + "N" * (tamanho * 10)+ " FIM]"
    return mensagem

def testeTempoEnvio(cliente_socket, protocolo):
    porta = TCP_PORT if protocolo == "TCP" else UDP_PORT
    logging.info(f"Teste de tempo de envio iniciado")
    tamanho = int(input("Digite até que tamanho de pacote será enviado. \n Começamos com 0 e aumentamos de 10 em 10 até o valor digitado: "))
    # Inicia timer
    # Envia a mensagem para o servidor
    tempo_total = time.time()
    for i in range(tamanho):
        mensagem = criaMensagem(tamanho, i)
        logging.info(f"Tamanho da mensagem {i}: {len(mensagem)}")
        inicio = time.time()
        cliente_socket.send(mensagem.encode())
        logging.info(f"Mensagem {i} enviada para {SERVER_IP}:{porta}: {mensagem}")

        # Recebe a resposta do servidor
        resposta = cliente_socket.recv(BUFFER_SIZE)
        logging.info(f"Resposta de {SERVER_IP}: {resposta.decode()}")

        # Finaliza timer
        RTT = (time.time() - inicio) * 1000 
        logging.info(f"Tempo p/ resposta do servidor: {RTT}ms")
    tempo_total = (time.time() - tempo_total) * 1000
    logging.info(f"Tempo total de envio de todos os pacotes enviados: {tempo_total}ms")

# definir as métricas de avaliação da rede
# Aqui vamos fazer tanto pro udp quanto pro tcp
# e temos que receber o socket que o cliente está usando 
def interfaceEnvioTCP(cliente_socket):
    logging.info(f"Interface de envio de pacotes iniciada")
    while True:
        print("Escolha a opão de envio de pacotes")
        escolha = input("0 - Enviar um pacote \n 1 - Teste de tempo de resposta \n 2 - Teste de vazão \n 3 - Encerrar conexão\n")

        if escolha == "0":
            print("Digite a mensagem a ser enviada")
            mensagem = input()
            cliente_socket.send(mensagem.encode())
            logging.info(f"Mensagem enviada para {SERVER_IP}: {mensagem}")
            resposta = cliente_socket.recv(BUFFER_SIZE)
            logging.info(f"Resposta de {SERVER_IP}: {resposta.decode()}")
        elif escolha == "1":
            testeTempoEnvio(cliente_socket, "TCP")
        elif escolha == "3" or KeyboardInterrupt:
            logging.info("Encerrando conexão com o servidor TCP")
            cliente_socket.send(b"FIM")
            cliente_socket.close()    
            break
