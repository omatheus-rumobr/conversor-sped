import os
import sys
from pathlib import Path


def consolidar_sped(arquivo_entrada, arquivo_saida=None):
    """
    Lê um arquivo SPED e corrige campos vazios representados por pipes duplos (||),
    substituindo por |-| para que a automação possa identificar corretamente os campos.
    
    Args:
        arquivo_entrada: Caminho para o arquivo SPED original
        arquivo_saida: Caminho para o arquivo SPED corrigido (opcional, padrão: adiciona '_consolidado' ao nome)
    
    Returns:
        Caminho do arquivo gerado
    """
    # Verifica se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado!")
        return None
    
    # Define o nome do arquivo de saída se não foi fornecido
    if arquivo_saida is None:
        caminho_entrada = Path(arquivo_entrada)
        nome_base = caminho_entrada.stem
        extensao = caminho_entrada.suffix
        diretorio = caminho_entrada.parent
        arquivo_saida = os.path.join(diretorio, f"{nome_base}_consolidado{extensao}")
    
    # Tenta diferentes encodings para ler o arquivo
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    linhas = None
    encoding_usado = None
    
    for encoding in encodings:
        try:
            with open(arquivo_entrada, 'r', encoding=encoding) as f:
                linhas = f.readlines()
                encoding_usado = encoding
                print(f"Arquivo lido com encoding: {encoding}")
                break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if linhas is None:
        print(f"Erro: Não foi possível ler o arquivo '{arquivo_entrada}' com nenhum encoding testado!")
        return None
    
    # Processa cada linha substituindo || por |-|
    linhas_corrigidas = []
    total_corrigidas = 0
    
    for num_linha, linha in enumerate(linhas, 1):
        linha_original = linha
        # Substitui todas as ocorrências de || por |-|
        # Mas preserva o final da linha (quebras de linha)
        linha_corrigida = linha.rstrip('\n\r').replace('||', '|-|')
        
        # Se houve alteração, conta
        if linha_original.rstrip('\n\r') != linha_corrigida:
            total_corrigidas += 1
        
        # Adiciona a quebra de linha de volta
        linha_corrigida += '\n'
        linhas_corrigidas.append(linha_corrigida)
    
    # Escreve o arquivo corrigido
    try:
        with open(arquivo_saida, 'w', encoding=encoding_usado) as f:
            f.writelines(linhas_corrigidas)
        print(f"\nArquivo consolidado criado com sucesso!")
        print(f"Arquivo de entrada: {arquivo_entrada}")
        print(f"Arquivo de saída: {arquivo_saida}")
        print(f"Total de linhas processadas: {len(linhas)}")
        print(f"Total de linhas corrigidas: {total_corrigidas}")
        return arquivo_saida
    except Exception as e:
        print(f"Erro ao escrever arquivo: {e}")
        return None


def main():
    """
    Função principal para executar o script via linha de comando.
    Uso: python consolidar_sped.py [arquivo_entrada] [arquivo_saida]
    """
    if len(sys.argv) < 2:
        # Se não foi passado argumento, usa o arquivo padrão do diretório
        arquivo_padrao = "08589276000673-158880307-20240801-20240831-0-D2103F26E59FBF49F6C5651718CBF83BEB0806F3-SPED-EFD.txt"
        if os.path.exists(arquivo_padrao):
            print(f"Usando arquivo padrão: {arquivo_padrao}")
            arquivo_entrada = arquivo_padrao
        else:
            print("Uso: python consolidar_sped.py <arquivo_entrada> [arquivo_saida]")
            print("\nOu coloque o arquivo SPED no diretório atual com o nome padrão.")
            return
    else:
        arquivo_entrada = sys.argv[1]
    
    arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else None
    
    consolidar_sped(arquivo_entrada, arquivo_saida)


if __name__ == "__main__":
    main()
