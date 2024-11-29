import matplotlib.pyplot as plt
import sys

def plot_bar_chart(velocidade_t, velocidade_u):
    """
    Gera um gráfico de barras comparando as velocidades das máquinas T e U.
    """
    labels = ["TCP", "UDP"]
    valores = [velocidade_t, velocidade_u]
    cores = ["blue", "red"]

    plt.figure(figsize=(8, 6))

    # Cria o gráfico de barras
    plt.bar(labels, valores, color=cores)

    # Configurações do gráfico
    plt.title("Comparação de Tempo Total para 10 milhões de pacotes entre TCP e UDP")
    plt.ylabel("milisegundos")
    plt.ylim(0, max(valores) * 1.2)  # Ajusta o limite do eixo Y para melhor visualização
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salva o gráfico como imagem
    plt.savefig("comparacao_tempo_total.png")
    print("Gráfico salvo como 'comparacao_tempo_total.png'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python cliente_vazao.py <velocidade_T> <velocidade_U>")
        sys.exit(1)

    try:
        velocidade_t = float(sys.argv[1])
        velocidade_u = float(sys.argv[2])
    except ValueError:
        print("Por favor, insira valores numéricos para as velocidades.")
        sys.exit(1)

    plot_bar_chart(velocidade_t, velocidade_u)
