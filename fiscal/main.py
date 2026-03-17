"""
Script para ler e separar arquivo SPED por blocos e sub-blocos.
O arquivo SPED é delimitado por pipes (|) e os blocos são identificados
pelo primeiro caractere do código do registro. Os sub-blocos são identificados
pelo código completo do registro (ex: D001, D010, D100).
"""

import os
from collections import defaultdict
from pathlib import Path


def extrair_bloco_e_subbloco(linha):
    """
    Extrai o bloco e o código completo do registro de uma linha do SPED.
    
    Args:
        linha: String com a linha do arquivo SPED
        
    Returns:
        Tupla (bloco, codigo_registro) ou (None, None) se inválido
        bloco: String com o identificador do bloco (0, 1, 9, A, C, D, F, I, M, P)
        codigo_registro: String com o código completo do registro (ex: D001, D010)
    """
    linha = linha.strip()
    if not linha or not linha.startswith('|'):
        return None, None

    partes = [p.strip() for p in linha.split('|') if p.strip()]
    
    if not partes:
        return None, None
    
    codigo_registro = partes[0]
    if not codigo_registro:
        return None, None

    primeiro_caractere = codigo_registro[0].upper()

    blocos_validos = ['0', '1', '9', 'A', 'C', 'D', 'F', 'I', 'M', 'P']
    
    if primeiro_caractere in blocos_validos:
        return primeiro_caractere, codigo_registro.upper()
    
    return None, None


def ler_e_separar_sped(arquivo_entrada, pasta_saida='blocos_separados'):
    """
    Lê o arquivo SPED e separa os registros por blocos e sub-blocos.
    
    Args:
        arquivo_entrada: Caminho do arquivo SPED de entrada
        pasta_saida: Nome da pasta onde serão salvos os arquivos por bloco
    """
    diretorio_arquivo = os.path.dirname(os.path.abspath(arquivo_entrada))
    pasta_saida_completa = os.path.join(diretorio_arquivo, pasta_saida)
    
    if not os.path.exists(pasta_saida_completa):
        os.makedirs(pasta_saida_completa)

    blocos = defaultdict(lambda: defaultdict(list))
    total_linhas = 0
    linhas_processadas = 0
    linhas_ignoradas = 0

    print(f"Lendo arquivo: {arquivo_entrada}")

    encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
    arquivo = None

    for encoding in encodings:
        try:
            arquivo = open(arquivo_entrada, 'r', encoding=encoding)
            arquivo.readline()
            arquivo.seek(0)
            print(f"Encoding detectado: {encoding}")
            break
        except (UnicodeDecodeError, UnicodeError):
            if arquivo:
                arquivo.close()
            continue
    
    if arquivo is None:
        print(f"Erro: Não foi possível determinar o encoding do arquivo!")
        return
    
    try:
        for linha in arquivo:
            total_linhas += 1
            bloco, codigo_registro = extrair_bloco_e_subbloco(linha)
            
            if bloco and codigo_registro:
                blocos[bloco][codigo_registro].append(linha.rstrip('\n'))
                linhas_processadas += 1
            else:
                linhas_ignoradas += 1

            if total_linhas % 10000 == 0:
                print(f"Processadas {total_linhas} linhas...")
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado!")
        return
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return
    finally:
        if arquivo:
            arquivo.close()

    print("\nSalvando blocos e sub-blocos em arquivos separados...")

    total_arquivos = 0
    for bloco in sorted(blocos.keys()):
        pasta_bloco = os.path.join(pasta_saida_completa, f"bloco_{bloco}")
        if not os.path.exists(pasta_bloco):
            os.makedirs(pasta_bloco)

        for sub_bloco in sorted(blocos[bloco].keys()):
            registros = blocos[bloco][sub_bloco]
            nome_arquivo = os.path.join(pasta_bloco, f"{sub_bloco}.txt")
            
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo_saida:
                arquivo_saida.write('\n'.join(registros))
                arquivo_saida.write('\n')
            
            total_arquivos += 1
            print(f"  Bloco {bloco} -> {sub_bloco}: {len(registros)} registros -> {nome_arquivo}")

    print("\n" + "="*60)
    print("ESTATÍSTICAS")
    print("="*60)
    print(f"Total de linhas no arquivo: {total_linhas}")
    print(f"Linhas processadas (com bloco válido): {linhas_processadas}")
    print(f"Linhas ignoradas: {linhas_ignoradas}")
    print(f"\nBlocos encontrados: {len(blocos)}")
    print(f"Total de sub-blocos: {sum(len(sub_blocos) for sub_blocos in blocos.values())}")
    print(f"Total de arquivos criados: {total_arquivos}")
    
    print("\nDetalhamento por bloco:")
    for bloco in sorted(blocos.keys()):
        total_registros_bloco = sum(len(registros) for registros in blocos[bloco].values())
        print(f"\n  Bloco {bloco}: {total_registros_bloco} registros em {len(blocos[bloco])} sub-blocos")
        for sub_bloco in sorted(blocos[bloco].keys()):
            qtd = len(blocos[bloco][sub_bloco])
            print(f"    - {sub_bloco}: {qtd} registros")
    
    print("="*60)


def exibir_resumo_blocos(arquivo_entrada):
    """
    Exibe um resumo dos blocos e sub-blocos encontrados no arquivo sem salvar arquivos.
    
    Args:
        arquivo_entrada: Caminho do arquivo SPED de entrada
    """
    blocos = defaultdict(lambda: defaultdict(list))
    total_linhas = 0

    print(f"Analisando arquivo: {arquivo_entrada}")

    encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
    arquivo = None

    for encoding in encodings:
        try:
            arquivo = open(arquivo_entrada, 'r', encoding=encoding)
            arquivo.readline()
            arquivo.seek(0)
            break
        except (UnicodeDecodeError, UnicodeError):
            if arquivo:
                arquivo.close()
            continue
    
    if arquivo is None:
        print(f"Erro: Não foi possível determinar o encoding do arquivo!")
        return
    
    try:
        for linha in arquivo:
            total_linhas += 1
            bloco, codigo_registro = extrair_bloco_e_subbloco(linha)
            if bloco and codigo_registro:
                blocos[bloco][codigo_registro].append(linha.strip())
    finally:
        if arquivo:
            arquivo.close()
    
    print("\n" + "="*60)
    print("RESUMO DOS BLOCOS E SUB-BLOCOS")
    print("="*60)
    print(f"Total de linhas: {total_linhas}")
    print(f"Blocos encontrados: {len(blocos)}")
    print(f"Total de sub-blocos: {sum(len(sub_blocos) for sub_blocos in blocos.values())}")
    
    print("\nDetalhamento por bloco:")
    for bloco in sorted(blocos.keys()):
        total_registros_bloco = sum(len(registros) for registros in blocos[bloco].values())
        print(f"\n  Bloco {bloco}: {total_registros_bloco} registros em {len(blocos[bloco])} sub-blocos")
        for sub_bloco in sorted(blocos[bloco].keys()):
            qtd = len(blocos[bloco][sub_bloco])
            print(f"    - {sub_bloco}: {qtd} registros")
    print("="*60)


if __name__ == "__main__":
    diretorio_script = Path(__file__).parent
    arquivo_sped = diretorio_script / "08589276000673-158880307-20240801-20240831-0-D2103F26E59FBF49F6C5651718CBF83BEB0806F3-SPED-EFD_consolidado.txt"

    if not arquivo_sped.exists():
        print(f"Arquivo '{arquivo_sped}' não encontrado!")
        print("Por favor, verifique se o arquivo está no diretório atual.")
    else:
        print("="*60)
        print("SEPARADOR DE BLOCOS SPED")
        print("="*60)
        ler_e_separar_sped(str(arquivo_sped))
