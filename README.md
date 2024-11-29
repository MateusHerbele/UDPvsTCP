# UDPvsTCP

Este projeto realiza uma comparação de desempenho entre os protocolos UDP e TCP. O fluxo principal envolve a execução de scripts Python que simulam clientes e servidores, permitindo a coleta de métricas de desempenho, como tempo de resposta, pacotes enviados e taxa de vazão, armazenados em logs.

## Estrutura do Projeto

A estrutura do diretório é organizada da seguinte forma:

UDPvsTCP/ ├── data/ │ ├── logs/ │ │ ├── cliente_tcp.log │ │ ├── cliente_udp.log │ │ ├── servidor_tcp.log │ │ └── servidor_udp.log │ └── resultados/ │ ├── cliente_tcp_tamanho_tempo.png │ ├── cliente_udp_tamanho_tempo.png │ ├── comparacao_pacotes_efetivos.png │ ├── comparacao_tempo_total.png │ └── comparacao_vazao.png ├── scripts/ │ ├── cliente_tempo_medio.py │ ├── comp_pacotes_enviados.py │ ├── comp_tempo_total_10m.py │ ├── comp_vazao.py │ └── cut.py ├── src/ │ ├── tcp/ │ │ ├── client.py │ │ └── servidor_tcp.py │ ├── udp/ │ │ ├── cliente_udp.py │ │ └── servidor_udp.py │ └── utils/ │ ├── configs.py │ ├── logger.py │ └── metrics.py ├── README.md └── .gitignore


## Como Executar

Para rodar o programa, siga estas etapas:

1. **Execute os Scripts dos Clientes e Servidores**:
   - Para o cliente e servidor TCP, execute:
     ```bash
     python3 client.py
     python3 servidor_tcp.py
     ```
   - Para o cliente e servidor UDP, execute:
     ```bash
     python3 cliente_udp.py
     python3 servidor_udp.py
     ```

2. **Testes e Métricas**:
   - Após executar os clientes, com os servidores devidamente estabelecidos, será fornecido a interface do respectivo protocolo, que permite realizar testes e a geração de logs.
   - As interfaces estão definidas em `src/utils/metricas.py`.

3. **Resultados**:
   - Os logs e resultados gerados durante os testes estarão armazenados nas pastas `data/logs/`.