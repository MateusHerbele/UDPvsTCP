import matplotlib.pyplot as plt
import sys

def plot_bar_chart(qntd_pacotes_tcp, qntd_pacotes_udp):
    """
    Gera um gráfico de barras comparando as velocidades das máquinas TCP e UDP.
    """
    labels = ["TCP", "UDP"]
    valores = [qntd_pacotes_tcp, qntd_pacotes_udp]
    cores = ["blue", "red", "black"]

    plt.figure(figsize=(8, 6))

    # Cria o gráfico de barras
    plt.bar(labels, valores, color=cores)

    # Configurações do gráfico
    plt.title("Comparação da Quantidade Efetiva de Pacotes Enviados entre TCP e UDP")
    plt.ylabel("Quantidade Pacotes")
    plt.ylim(0, max(valores) * 1.2)  # Ajusta o limite do eixo Y para melhor visualização
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salva o gráfico como imagem
    plt.savefig("comparacao_pacotes_efetivos_enviados.png")
    print("Gráfico salvo como 'comparacao_pacotes_efetivos_enviados.png'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python cliente_vazao.py <qntd_pacotes_TCP> <qntd_pacotes_UDP>")
        sys.exit(1)

    try:
        qntd_pacotes_tcp = float(sys.argv[1])
        qntd_pacotes_udp = float(sys.argv[2])
    except ValueError:
        print("Por favor, insira valores numéricos para as quantidades de pacotes.")
        sys.exit(1)

    plot_bar_chart(qntd_pacotes_tcp, qntd_pacotes_udp)
