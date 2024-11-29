import matplotlib.pyplot as plt
import sys

def process_file(file_path):
    tamanhos = []
    tempos = []

    # Lê o arquivo e processa cada linha
    with open(file_path, "r") as file:
        for line in file:
            if "[TAMANHO]" in line:
                # Extraindo o tamanho
                tamanho = int(line.split(":")[-1].strip())
                tamanhos.append(tamanho)
            elif "[TEMPO]" in line:
                # Extraindo o tempo
                tempo = float(line.split("]")[-1].replace("ms", "").strip())
                tempos.append(tempo)
    
    return tamanhos, tempos

def plot_data(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    
    # Linha vermelha para o tamanho (eixo X) e tempo (eixo Y)
    plt.plot(tamanhos, tempos, label="Tempo de Resposta (ms)", color="blue")
    
    plt.xlabel("Tamanho do Pacote")
    plt.ylabel("Tempo de Resposta (ms)")
    plt.title("Tempo de Resposta por Tamanho do Pacote")
    plt.legend()
    plt.grid(True)
    
    # Salvar o gráfico como imagem
    plt.savefig("grafico_tamanho_tempo.png")
    print("Gráfico salvo como 'grafico_tamanho_tempo.png'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tempo_medio.py <caminho_para_o_arquivo>")
        sys.exit(1)

    file_path = sys.argv[1]
    tamanhos, tempos = process_file(file_path)
    plot_data(tamanhos, tempos)
