import logging  # Biblioteca para logging
import socket  # Biblioteca para comunicação via socket
import time
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.config import SERVER_IP, TCP_PORT, BUFFER_SIZE, TIMEOUT, LOG_LEVEL

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def cria_mensagem(tamanho):
    mensagem = b'11' + b"a" * tamanho + b'22'
    return mensagem

def cliente_tcp(tamanho):
    # Mensagem teste

    mensagem = cria_mensagem(tamanho) 

    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        try:
            # Configura timeout para o socket
            cliente_socket.settimeout(TIMEOUT)
            # Conecta ao servidor
            cliente_socket.connect((SERVER_IP, TCP_PORT))
            # Tudo pra baixo deve ser determinado via CLI
            # Inicia timer
            inicio = time.time()
            # Envia a mensagem para o servidor
            for i in range(10):
                mensagem = cria_mensagem(tamanho * i)
                cliente_socket.send(mensagem)
                logging.info(f"Mensagem {i} enviada para {SERVER_IP}:{TCP_PORT}: {mensagem}")

            # Recebe a resposta do servidor
                resposta = cliente_socket.recv(BUFFER_SIZE)
                logging.info(f"Resposta de {SERVER_IP}: {resposta.decode()}")


            # Finaliza timer
            RTT = (time.time() - inicio) * 1000 
            logging.info(f"Tempo p/ resposta do servidor: {RTT}ms")
        except socket.timeout:
            logging.error(f"Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")
            cliente_socket.close()

if __name__ == "__main__":
    tamanho = int(input("Digite o tamanho da mensagem a ser enviada: "))
    cliente_tcp(tamanho)