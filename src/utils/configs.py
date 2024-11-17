# configs.py
# Configurações gerais do projeto

# Configurações de rede
SERVER_IP = "127.0.0.1"  # IP do servidor (localhost para testes)
UDP_PORT = 5001          # Porta para o servidor UDP
TCP_PORT = 5002          # Porta para o servidor TCP

# Tamanhos do buffer
BUFFER_SIZE = 1024       # Tamanho do buffer para recepção/envio

# Outras configurações
TIMEOUT = 5              # Timeout para conexões (em segundos)
LOG_LEVEL = "DEBUG"      # Nível de logging. Opções: DEBUG, INFO, WARNING, ERROR, CRITICAL
