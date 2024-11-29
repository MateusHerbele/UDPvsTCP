import matplotlib.pyplot as plt
import sys
import re

def process_file(file_path):
    tamanhos = []
    tempos = []

    # Lê o arquivo e processa cada linha
    with open(file_path, "r") as file:
        linhas = file.readlines()

    for linha in linhas:
        if "[PACOTE]" in linha:
            # Extrai o tamanho do pacote usando regex
            match_tamanho = re.search(r"tamanho: (\d+)", linha)
            if match_tamanho:
                tamanhos.append(int(match_tamanho.group(1)))
        elif "[METRICA]" in linha:
            # Extrai o tempo de resposta usando regex
            match_tempo = re.search(r"Tempo p/ resposta do servidor: ([\d.]+)ms", linha)
            if match_tempo:
                tempos.append(float(match_tempo.group(1)))

    return tamanhos, tempos

def plot_data(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    
    # Linha azul para o tempo (eixo Y) e vermelho para o tamanho (eixo X)
    plt.plot(tamanhos, tempos, label="Tempo de Resposta (ms)", color="red")
    
    plt.xlabel("Tamanho do Pacote (bytes)")
    plt.ylabel("Tempo de Resposta (ms)")
    plt.title("(Cliente UDP) Tempo de Resposta por Tamanho do Pacote")
    plt.legend()
    plt.grid(True)
    
    # Salvar o gráfico como imagem
    plt.savefig("cliente_udp_tamanho_tempo.png")
    print("Gráfico salvo como 'cliente_udp_tamanho_tempo.png'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tempo_medio.py <caminho_para_o_arquivo>")
        sys.exit(1)

    file_path = sys.argv[1]
    tamanhos, tempos = process_file(file_path)
    plot_data(tamanhos, tempos)
