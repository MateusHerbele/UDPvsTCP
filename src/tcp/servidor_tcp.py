import logging
import socket
import sys
import os

# Adiciona o caminho do diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from utils.configs import SERVER_IP, TCP_PORT, BUFFER_SIZE, LOG_LEVEL

# Configuração do logging
log_file = os.path.join(os.path.dirname(__file__), '../../data/logs/servidor_tcp.log')  # Define o arquivo de log

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log no console
        logging.FileHandler(log_file, mode='a', encoding='utf-8')  # Log no arquivo
    ]
)

def servidor_tcp():
    logging.info(f"[INICIALIZACAO] Servidor TCP em {SERVER_IP}:{TCP_PORT}")
    logging.info(f"[INICIALIZACAO] BUFFER_SIZE={BUFFER_SIZE}, LOG_LEVEL={LOG_LEVEL}")

    # Criação do socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        # Associa o socket a um endereço e porta
        servidor_socket.bind((SERVER_IP, TCP_PORT))
        servidor_socket.listen()

        while True:
            try:
                # Aceita a conexão do cliente
                cliente, endereco_cliente = servidor_socket.accept()
                logging.info(f"[CONEXAO] Nova conexão de {endereco_cliente}")
                i = 0 # Contador de mensagens
                # Recebe a mensagem do cliente
                while(True):
                    try:
                        dados = b""
                        while True:
                            parte = cliente.recv(BUFFER_SIZE)
                            #print("parte: " + parte.decode()) COMENTEI PRA VER COMO FICOU A SAIDA DO LOG
                            dados += parte
                            if len(parte) < BUFFER_SIZE:
                                break
                        
                        # Fecha a conexão com o cliente após a resposta
                        if dados.decode() == "FIM":
                            logging.info(f"[ENCERRAMENTO] Conexão encerrada com {endereco_cliente}")
                            cliente.close()
                            break
                            
                        numero_do_pacote = dados.decode().split(" ")[1]
                        #logging.debug(f"Mensagem {numero_do_pacote} recebida de {endereco_cliente}: {dados.decode()}") COMENTEI PRA VER COMO FICOU A SAIDA DO LOG
                        logging.info(f"[PACOTE] Mensagem #{numero_do_pacote} recebida de {endereco_cliente}")
                        i += 1
                        logging.info(f"[STATUS] Total de mensagens recebidas até agora: {i}")

                        # Envia uma resposta para o cliente
                        resposta = f"Pacote {numero_do_pacote} recebido com sucesso!"
                        cliente.send(resposta.encode())
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
    servidor_tcp()