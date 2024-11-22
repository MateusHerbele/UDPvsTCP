import logging  # Biblioteca para logging
import socket  # Biblioteca para comunicação via socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, TCP_PORT, BUFFER_SIZE, TIMEOUT, LOG_LEVEL

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def create_message():
    mensagem = "a" * 50000
    return mensagem

def cliente_tcp():
    # Mensagem teste
    mensagem = '10' + create_message() + '11'


    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        try:
            # Configura timeout para o socket
            cliente_socket.settimeout(TIMEOUT)
            # Conecta ao servidor
            cliente_socket.connect((SERVER_IP, TCP_PORT))
            # Envia a mensagem para o servidor
            cliente_socket.send(mensagem.encode())
            logging.info(f"Mensagem enviada para {SERVER_IP}:{TCP_PORT}: {mensagem}")

            # Recebe a resposta do servidor
            resposta = cliente_socket.recv(BUFFER_SIZE)
            logging.info(f"Resposta de {SERVER_IP}: {resposta.decode()}")
        except socket.timeout:
            logging.error(f"Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")
            cliente_socket.close()

if __name__ == "__main__":
    cliente_tcp()