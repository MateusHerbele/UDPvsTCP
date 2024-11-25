import logging
import socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, UDP_PORT, BUFFER_SIZE, LOG_LEVEL

# Configuração do logging
log_file = os.path.join(os.path.dirname(__file__), '../../data/logs/servidor_udp.log')  # Define o arquivo de log

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log no console
        logging.FileHandler(log_file, mode='a', encoding='utf-8')  # Log no arquivo
    ]
)

def servidor_udp():
    logging.info(f"[INICIALIZACAO] Servidor UDP em {SERVER_IP}:{UDP_PORT}")
    logging.info(f"[INICIALIZACAO] BUFFER_SIZE={BUFFER_SIZE}, LOG_LEVEL={LOG_LEVEL}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_socket:
        # Associa o socket a um endereço e porta
        servidor_socket.bind((SERVER_IP, UDP_PORT))
        i = 0  # Contador de mensagens
        while True:
            try:
                # Recebe a mensagem e o endereço do cliente
                dados, endereco_cliente = servidor_socket.recvfrom(BUFFER_SIZE)
                mensagem = dados.decode()
                logging.info(f"[PACOTE] Mensagem recebida de {endereco_cliente}")

                # Verifica se a mensagem é o comando de término
                if mensagem == "FIM":
                    logging.info(f"[ENCERRAMENTO] Conexão encerrada com {endereco_cliente}")
                    logging.info(f"[STATUS] Total de pacotes recebidos: {i}")
                    #servidor_socket.sendto(f"Conexão encerrada.\nNúmero de pacotes recebidos: {i}".encode(), endereco_cliente)                    
                    servidor_socket.close()
                    break

                # Incrementa o contador de pacotes e responde
                numero_do_pacote = mensagem.split(" ")[1] if " " in mensagem else str(i)
                #logging.debug(f"Mensagem {numero_do_pacote} recebida de {endereco_cliente}: {dados.decode()}")
                logging.info(f"[PACOTE] Mensagem #{numero_do_pacote} recebida de {endereco_cliente}")
                i += 1
                logging.info(f"[STATUS] Total de mensagens recebidas até agora: {i}")
                
                # Envia uma resposta para o cliente
                resposta = f"Pacote {numero_do_pacote} recebido com sucesso!"
                servidor_socket.sendto(resposta.encode(), endereco_cliente)
                logging.info(f"[RESPOSTA] Enviada para {endereco_cliente}: {resposta}")
            except Exception as e:
                logging.error(f"[ERRO] Falha ao processar pacote de {endereco_cliente}: {e}", exc_info=True)
                break

            except KeyboardInterrupt:
                    logging.info("[SERVIDOR] Encerrado manualmente pelo usuário.")
                    break
            except Exception as e:
                logging.error(f"[ERRO CRITICO] O servidor encontrou um erro: {e}", exc_info=True)
                break

if __name__ == "__main__":
    servidor_udp()
