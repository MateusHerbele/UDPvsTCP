import logging
import socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, UDP_PORT, BUFFER_SIZE, LOG_LEVEL

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
        i = 0  # Contador de mensagens

        while True:
            try:
                # Recebe a mensagem e o endereço do cliente
                dados, endereco_cliente = servidor_socket.recvfrom(BUFFER_SIZE)
                mensagem = dados.decode()
                logging.info(f"Mensagem recebida de {endereco_cliente}: {mensagem}")

                # Verifica se a mensagem é o comando de término
                if mensagem == "FIM":
                    logging.info(f"Comando de término recebido de {endereco_cliente}. Encerrando conexão.")
                    resposta = "Comunicação encerrada. Adeus!"
                    servidor_socket.sendto(resposta.encode(), endereco_cliente)
                    break

                # Incrementa o contador de pacotes e responde
                i += 1
                numero_do_pacote = mensagem.split(" ")[1] if " " in mensagem else str(i)
                resposta = f"Pacote {numero_do_pacote} recebido com sucesso!"
                servidor_socket.sendto(resposta.encode(), endereco_cliente)

                logging.info(f"Resposta enviada para {endereco_cliente}: {resposta}")
                logging.info(f"Quantidade de mensagens recebidas: {i}")

            except KeyboardInterrupt:
                logging.info("Servidor encerrado manualmente.")
                break
            except Exception as e:
                logging.error(f"Erro no servidor UDP: {e}")
                break

if __name__ == "__main__":
    servidor_udp()
