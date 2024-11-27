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
        servidor_socket.bind((SERVER_IP, TCP_PORT))
        servidor_socket.listen()

        while True:
            try:
                # Aceita a conexão do cliente
                cliente, endereco_cliente = servidor_socket.accept()
                logging.info(f"[CONEXAO] Nova conexão de {endereco_cliente}")
                buffer_recebido = ""  # Buffer para armazenar os dados recebidos
                i = 0  # Contador de mensagens
                
                while True:
                    try:
                        # Recebe uma parte da mensagem
                        parte = cliente.recv(BUFFER_SIZE).decode()
                        if not parte:  # Conexão foi fechada pelo cliente
                            logging.info(f"[ENCERRAMENTO] Conexão encerrada por {endereco_cliente}")
                            cliente.close()
                            break
                        
                        # Adiciona a parte recebida ao buffer
                        buffer_recebido += parte
                        
                        # Verifica se a mensagem completa foi recebida
                        if "FIM]" in buffer_recebido:
                            # Processa a mensagem completa até o delimitador
                            mensagens = buffer_recebido.split("FIM]")
                            for mensagem in mensagens[:-1]:  # Todas as mensagens completas
                                mensagem_completa = mensagem.strip()
                                if mensagem_completa:
                                    i += 1
                                    logging.info(f"[PACOTE] Mensagem recebida de {endereco_cliente}, tamanho: {len(mensagem)}.")
                                    logging.info(f"[STATUS] Total de mensagens recebidas até agora: {i}")
                                    
                                    # Extrai o número do pacote (assumindo o formato correto)
                                    try:
                                        numero_do_pacote = mensagem_completa.split(" ")[1].strip("#")
                                    except IndexError:
                                        numero_do_pacote = "desconhecido"
                                        logging.warning(f"[FORMATO INVALIDO] Mensagem malformada")
                                    
                                    # Envia resposta ao cliente
                                    resposta = f"Pacote {numero_do_pacote} recebido com sucesso!"
                                    cliente.send(resposta.encode())
                                    logging.info(f"[RESPOSTA] Enviada para {endereco_cliente}: {resposta}")
                            
                            # Retém apenas a parte não processada do buffer
                            buffer_recebido = mensagens[-1]
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