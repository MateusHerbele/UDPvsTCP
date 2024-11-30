import socket  # Biblioteca para comunicação via socket
import sys
import os
import time

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.logger import tcp_logger as logging  # Usa o logger TCP
from utils.configs import SERVER_IP, TCP_PORT, TIMEOUT
from utils.metricas import interfaceEnvioTCP

def cliente_tcp():
    logging.info(f"[INICIALIZACAO] Cliente TCP iniciado com TIMEOUT={TIMEOUT}s")

    # Criação do socket UDP
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
            try:
                logging.info(f"[CONEXAO] Tentando conectar ao servidor {SERVER_IP}:{TCP_PORT}.")

                # Configura timeout para o socket
                cliente_socket.settimeout(TIMEOUT)

                # Conecta ao servidor
                cliente_socket.connect((SERVER_IP, TCP_PORT))
                logging.info(f"[CONEXAO] Conexão estabelecida com {SERVER_IP}:{TCP_PORT}.")

                # Entra na interface de envio de mensagens
                interfaceEnvioTCP(cliente_socket)

            except socket.timeout:
                logging.error(f"[ERRO] Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")
                cliente_socket.close()

            except ConnectionRefusedError as e:
                logging.error(f"[ERRO] Conexão recusada pelo servidor {SERVER_IP}:{TCP_PORT}. Detalhes: {e}", exc_info=True)
                time.sleep(5)

            except Exception as e:
                logging.error(f"[ERRO] Ocorreu um erro inesperado: {e}", exc_info=True)
                cliente_socket.close()


if __name__ == "__main__":
    cliente_tcp()
