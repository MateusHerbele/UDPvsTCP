import sys
import os

def apagar_linhas(file_path, intervalo):
    # Abre o arquivo para leitura
    with open(file_path, "r") as file:
        linhas = file.readlines()

    # Cria uma nova lista de linhas, removendo as linhas a cada N
    linhas_restantes = [linha for i, linha in enumerate(linhas) if (i + 1) % intervalo != 0]

    # Cria o nome do arquivo de saída
    nome_saida = os.path.splitext(file_path)[0] + "_cut.log"
    
    # Escreve as linhas restantes no arquivo de saída
    with open(nome_saida, "w") as file:
        file.writelines(linhas_restantes)

    print(f"Linhas removidas a cada {intervalo} linhas. Arquivo de saída salvo como '{nome_saida}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python apagar_linhas.py <caminho_para_o_arquivo> <intervalo>")
        sys.exit(1)

    # Recebe o nome do arquivo e o intervalo como parâmetros
    file_path = sys.argv[1]
    intervalo = int(sys.argv[2])

    # Chama a função para apagar as linhas e salvar no arquivo de saída
    apagar_linhas(file_path, intervalo)
