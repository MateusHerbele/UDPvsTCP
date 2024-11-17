import logging  # Biblioteca para logging
import socket  # Biblioteca para comunicação via socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, UDP_PORT, BUFFER_SIZE, TIMEOUT, LOG_LEVEL

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def cliente_udp():
    # Mensagem teste
    mensagem = "Olá, servidor!"

    # Criação do socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente_socket:
        try:
            # Configura timeout para o socket
            cliente_socket.settimeout(TIMEOUT)
            # Envia a mensagem para o servidor
            cliente_socket.sendto(mensagem.encode(), (SERVER_IP, UDP_PORT))
            logging.info(f"Mensagem enviada para {SERVER_IP}:{UDP_PORT}: {mensagem}")

            # Recebe a resposta do servidor
            resposta, endereco_servidor = cliente_socket.recvfrom(BUFFER_SIZE)
            logging.info(f"Resposta de {endereco_servidor}: {resposta.decode()}")
        except socket.timeout:
            logging.error(f"Timeout de {TIMEOUT} segundos excedido. O servidor não respondeu.")
            cliente_socket.close()

if __name__ == "__main__":
    cliente_udp()