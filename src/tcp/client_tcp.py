import logging  # Biblioteca para logging
import socket  # Biblioteca para comunicação via socket
import time
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, TCP_PORT, TIMEOUT, LOG_LEVEL
from utils.metricas import interfaceEnvioTCP

# Configuração do logging
log_file = os.path.join(os.path.dirname(__file__), '../../data/logs/cliente_tcp.log')  # Define o arquivo de log

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log no console
        logging.FileHandler(log_file, mode='a', encoding='utf-8')  # Log no arquivo
    ]
)

def cliente_tcp():
    logging.info(f"[INICIALIZACAO] Cliente TCP iniciado com TIMEOUT={TIMEOUT}s")

    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        try:
            logging.info(f"[CONEXAO] Tentando conectar ao servidor {SERVER_IP}:{TCP_PORT}")

            # Configura timeout para o socket
            cliente_socket.settimeout(TIMEOUT)

            # Conecta ao servidor
            cliente_socket.connect((SERVER_IP, TCP_PORT))
            logging.info(f"[CONEXAO] Conexão estabelecida com {SERVER_IP}:{TCP_PORT}")

            # Interface de envio TCP
            interfaceEnvioTCP(cliente_socket)

        except socket.timeout:
            logging.error(f"[ERRO] Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")
        
        except ConnectionRefusedError as e:
            logging.error(f"[ERRO] Conexão recusada pelo servidor {SERVER_IP}:{TCP_PORT}. Detalhes: {e}", exc_info=True)

        except Exception as e:
            logging.error(f"[ERRO] Ocorreu um erro inesperado: {e}", exc_info=True)
    
    for handler in logging.getLogger().handlers:
        handler.flush()


if __name__ == "__main__":
    cliente_tcp()