import socket  # Biblioteca para comunicação via socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.logger import udp_logger as logging  # Usa o logger UDP
from utils.configs import TIMEOUT
from utils.metricas import interfaceEnvioUDP

def cliente_udp():
    logging.info(f"[INICIALIZACAO] Cliente UDP iniciado com TIMEOUT={TIMEOUT}s")
    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente_socket:
        try:
            # Configura timeout para o socket
            cliente_socket.settimeout(TIMEOUT)
            # Entra na interface de envio de mensagens
            interfaceEnvioUDP(cliente_socket)

        except socket.timeout:
            logging.error(f"[ERRO] Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")
            cliente_socket.close()

        except Exception as e:
            logging.error(f"[ERRO] Ocorreu um erro inesperado: {e}", exc_info=True)
            cliente_socket.close()

if __name__ == "__main__":
    cliente_udp()