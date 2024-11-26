import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """
    Configura um logger para um arquivo específico.
    """
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    
    # StreamHandler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # FileHandler para arquivo
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Configuração do logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

# Configuração do logger principal
LOG_DIR = os.path.join(os.path.dirname(__file__), '../../data/logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Logger compartilhado para TCP
tcp_log_file = os.path.join(LOG_DIR, 'cliente_tcp.log')
tcp_logger = setup_logger("tcp_logger", tcp_log_file)

# Logger compartilhado para UDP
udp_log_file = os.path.join(LOG_DIR, 'cliente_udp.log')
udp_logger = setup_logger("udp_logger", udp_log_file)
