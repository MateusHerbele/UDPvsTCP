import logging  # Biblioteca para logging
import socket  # Biblioteca para comunicação via socket
import time
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, TCP_PORT, TIMEOUT, LOG_LEVEL
from utils.metricas import *

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def cliente_tcp():
    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        try:
            # Configura timeout para o socket
            cliente_socket.settimeout(TIMEOUT)
            # Conecta ao servidor
            cliente_socket.connect((SERVER_IP, TCP_PORT))
            logging.info(f"Conexão estabelecida com {SERVER_IP}:{TCP_PORT}")
            interfaceEnvioTCP(cliente_socket)
        except socket.timeout:
            logging.error(f"Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")
            cliente_socket.close()

if __name__ == "__main__":
    cliente_tcp()