import logging
import socket
from ..utils.configs import SERVER_IP, UDP_PORT, BUFFER_SIZE, TIMEOUT, LOG_LEVEL

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    )

def servidor_udp():
    logging.info(f"Iniciando servidor UDP em {SERVER_IP}:{UDP_PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_socket:
        # Associa o socket a um endereço e porta
        servidor_socket.bind((SERVER_IP, UDP_PORT))

        while True:
            try:
                # Recebe a mensagem e o endereço do cliente
                mensagem, endereco_cliente = servidor_socket.recvfrom(BUFFER_SIZE)
                logging.info(f"Mensagem de {endereco_cliente}: {mensagem.decode()}")

                # Envia a resposta para o cliente
                resposta = "Olá, cliente!"
                servidor_socket.sendto(resposta.encode(), endereco_cliente)
                logging.info(f"Resposta enviada para {endereco_cliente}: {resposta}")
            except KeyboardInterrupt:
                logging.info("Servidor encerrado.")
                break

if __name__ == "__main__":
    servidor_udp();