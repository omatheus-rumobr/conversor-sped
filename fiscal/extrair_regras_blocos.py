from pathlib import Path
import json
import re
from typing import List, Tuple

try:
    import PyPDF2  # type: ignore
    PDF_LIBRARY = "PyPDF2"
except ImportError:
    try:
        import pdfplumber  # type: ignore
        PDF_LIBRARY = "pdfplumber"
    except ImportError:
        PDF_LIBRARY = None
        print("AVISO: Nenhuma biblioteca de PDF encontrada. Instale PyPDF2 ou pdfplumber:")
        print("  pip install PyPDF2")
        print("  ou")
        print("  pip install pdfplumber")


def parse_paginas(paginas_str: str) -> Tuple[int, int]:
    """
    Converte string de páginas (ex: "10-24") em tupla (inicio, fim).
    """
    match = re.match(r'(\d+)-(\d+)', paginas_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    raise ValueError(f"Formato de páginas inválido: {paginas_str}")


def extrair_texto_pypdf2(pdf_path: Path, pagina_inicio: int, pagina_fim: int) -> str:
    """
    Extrai texto de um PDF usando PyPDF2.
    """
    texto_completo = []
    
    with open(pdf_path, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        total_paginas = len(leitor.pages)
        
        # Ajusta índices (PDFs começam em 0, mas páginas do manual começam em 1)
        inicio_idx = max(0, pagina_inicio - 1)
        fim_idx = min(total_paginas, pagina_fim)
        
        for i in range(inicio_idx, fim_idx):
            pagina = leitor.pages[i]
            texto = pagina.extract_text()
            if texto:
                texto_completo.append(f"--- Página {i + 1} ---\n{texto}\n")
    
    return "\n".join(texto_completo)


def extrair_texto_pdfplumber(pdf_path: Path, pagina_inicio: int, pagina_fim: int) -> str:
    """
    Extrai texto de um PDF usando pdfplumber.
    """
    texto_completo = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_paginas = len(pdf.pages)
        
        # Ajusta índices (PDFs começam em 0, mas páginas do manual começam em 1)
        inicio_idx = max(0, pagina_inicio - 1)
        fim_idx = min(total_paginas, pagina_fim)
        
        for i in range(inicio_idx, fim_idx):
            pagina = pdf.pages[i]
            texto = pagina.extract_text()
            if texto:
                texto_completo.append(f"--- Página {i + 1} ---\n{texto}\n")
    
    return "\n".join(texto_completo)


def extrair_texto_pdf(pdf_path: Path, pagina_inicio: int, pagina_fim: int) -> str:
    """
    Extrai texto de um PDF usando a biblioteca disponível.
    """
    if PDF_LIBRARY == "PyPDF2":
        return extrair_texto_pypdf2(pdf_path, pagina_inicio, pagina_fim)
    elif PDF_LIBRARY == "pdfplumber":
        return extrair_texto_pdfplumber(pdf_path, pagina_inicio, pagina_fim)
    else:
        raise ImportError("Nenhuma biblioteca de PDF disponível")


def criar_markdown_bloco(versao: str, bloco: str, paginas: str, texto: str, data_criacao: str) -> str:
    """
    Cria o conteúdo markdown para um bloco.
    """
    conteudo = f"""# Bloco {bloco} - Versão {versao}

**Data de Criação:** {data_criacao}  
**Páginas:** {paginas}  
**Versão:** {versao}

---

{texto}
"""
    return conteudo


def processar_versoes():
    """
    Processa todas as versões e extrai as regras de cada bloco.
    """
    if PDF_LIBRARY is None:
        print("ERRO: Instale uma biblioteca de PDF antes de continuar.")
        return
    
    # Caminhos
    base_dir = Path(__file__).parent
    versoes_json = base_dir / "versoes.json"
    output_dir = base_dir / "documentacao_blocos"
    
    # Cria diretório de saída
    output_dir.mkdir(exist_ok=True)
    
    # Lê o arquivo JSON
    print(f"Lendo {versoes_json}...")
    with open(versoes_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    versoes = dados.get("versoes", [])
    print(f"Encontradas {len(versoes)} versões para processar.\n")
    
    # Processa cada versão
    for idx, versao_info in enumerate(versoes, 1):
        versao = versao_info["versao"]
        data_criacao = versao_info["data_criacao"]
        caminho_arquivo = versao_info["caminho_arquivo"]
        blocos = versao_info["blocos"]
        
        print(f"[{idx}/{len(versoes)}] Processando versão {versao}...")
        
        # Caminho do PDF
        pdf_path = base_dir / caminho_arquivo
        
        if not pdf_path.exists():
            print(f"  AVISO: PDF não encontrado: {pdf_path}")
            continue
        
        # Cria diretório para esta versão
        versao_dir = output_dir / versao
        versao_dir.mkdir(exist_ok=True)
        
        # Processa cada bloco
        for bloco_info in blocos:
            bloco = bloco_info["bloco"]
            paginas_str = bloco_info["paginas"]
            
            try:
                pagina_inicio, pagina_fim = parse_paginas(paginas_str)
                print(f"  Extraindo Bloco {bloco} (páginas {paginas_str})...")
                
                # Extrai texto do PDF
                texto = extrair_texto_pdf(pdf_path, pagina_inicio, pagina_fim)
                
                if not texto.strip():
                    print(f"    AVISO: Nenhum texto extraído do Bloco {bloco}")
                    continue
                
                # Cria conteúdo markdown
                conteudo_md = criar_markdown_bloco(versao, bloco, paginas_str, texto, data_criacao)
                
                # Salva arquivo markdown
                arquivo_md = versao_dir / f"bloco_{bloco}.md"
                with open(arquivo_md, 'w', encoding='utf-8') as f:
                    f.write(conteudo_md)
                
                print(f"    ✓ Salvo em: {arquivo_md.relative_to(base_dir)}")
                
            except Exception as e:
                print(f"    ERRO ao processar Bloco {bloco}: {e}")
                continue
        
        print()
    
    print(f"\n✓ Processamento concluído! Documentação salva em: {output_dir.relative_to(base_dir)}")


if __name__ == "__main__":
    processar_versoes()
