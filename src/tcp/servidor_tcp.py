import logging
import socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(_file_), '../'))

from utils.configs import SERVER_IP, TCP_PORT, BUFFER_SIZE, TIMEOUT, LOG_LEVEL

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def servidor_tcp():
    logging.info(f"Iniciando servidor TCP em {SERVER_IP}:{TCP_PORT}")

    # Criação do socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        # Associa o socket a um endereço e porta
        servidor_socket.bind((SERVER_IP, TCP_PORT))
        servidor_socket.listen()

        while True:
            try:
                # Aceita a conexão do cliente
                cliente, endereco_cliente = servidor_socket.accept()
                logging.info(f"Conexão recebida de {endereco_cliente}")

                # Recebe a mensagem do cliente
                dados = b""
                while True:
                    parte = cliente.recv(BUFFER_SIZE)
                    print("parte: " + parte.decode())
                    dados += parte
                    if len(parte) < BUFFER_SIZE:
                        break

                logging.info(f"Mensagem recebida de {endereco_cliente}: {dados.decode()}")

                # Envia uma resposta para o cliente
                resposta = "Olá, cliente!"
                cliente.send(resposta.encode())
                logging.info(f"Resposta enviada para {endereco_cliente}: {resposta}")

                # Fecha a conexão com o cliente após a resposta
                cliente.close()

            except KeyboardInterrupt:
                logging.info("Servidor encerrado.")
                break

if _name_ == "_main_":
    servidor_tcp()