import logging
import socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, TCP_PORT, BUFFER_SIZE, LOG_LEVEL

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
                i = 0 # Contador de mensagens
                # Recebe a mensagem do cliente
                while(True):
                    dados = b""
                    while True:
                        parte = cliente.recv(BUFFER_SIZE)
                        print("parte: " + parte.decode())
                        dados += parte
                        if len(parte) < BUFFER_SIZE:
                            break
                    numero_do_pacote = dados.decode().split(" ")[1]
                    logging.debug(f"Mensagem {numero_do_pacote} recebida de {endereco_cliente}: {dados.decode()}")
                    logging.info(f"Mensagem {numero_do_pacote} recebida de {endereco_cliente}")
                    i += 1
                    logging.info(f"Quantidade de mensagens recebidas: {i}")
                    # Envia uma resposta para o cliente
                    resposta = f"Pacote {numero_do_pacote} recebido com sucesso!"
                    cliente.send(resposta.encode())
                    logging.info(f"Resposta enviada parsa {endereco_cliente}: {resposta}")

                    # Fecha a conexão com o cliente após a resposta
                    if dados.decode() == b"FIM":
                        logging.info(f"Conexão encerrada com {endereco_cliente}")
                        cliente.close()
                        break

            except KeyboardInterrupt:
                logging.info("Servidor encerrado.")
                break

if __name__ == "__main__":
    servidor_tcp()