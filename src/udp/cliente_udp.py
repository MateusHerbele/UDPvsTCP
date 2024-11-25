import logging  # Biblioteca para logging
import socket  # Biblioteca para comunicação via socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, UDP_PORT, BUFFER_SIZE, TIMEOUT, LOG_LEVEL
from utils.metricas import interfaceEnvioUDP

# Configuração do logging
log_file = os.path.join(os.path.dirname(__file__), '../../data/logs/cliente_udp.log')  # Define o arquivo de log

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log no console
        logging.FileHandler(log_file, mode='a', encoding='utf-8')  # Log no arquivo
    ]
)

def cliente_udp():
    logging.info(f"[INICIALIZACAO] Cliente UDP iniciado com TIMEOUT={TIMEOUT}s")
    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente_socket:
        try:
            # Configura timeout para o socket
            cliente_socket.settimeout(TIMEOUT)
            # Envia a mensagem para o servidor
            interfaceEnvioUDP(cliente_socket)

        except socket.timeout:
            logging.error(f"[ERRO] Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")

        except Exception as e:
            logging.error(f"[ERRO] Ocorreu um erro inesperado: {e}", exc_info=True)

if __name__ == "__main__":
    cliente_udp()