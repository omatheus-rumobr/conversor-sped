import os
import zipfile
import tempfile
import io
import json
from pathlib import Path
from flask import Flask, request, send_file, jsonify
from loguru import logger
from flasgger import Swagger
from werkzeug.utils import secure_filename

from contribuicoes.modulos.bloco_0.r0000 import validar_0000
from contribuicoes.modulos.bloco_0.r0035 import validar_0035
from contribuicoes.modulos.bloco_0.r0100 import validar_0100
from contribuicoes.modulos.bloco_0.r0110 import validar_0110
from contribuicoes.modulos.bloco_0.r0111 import validar_0111
from contribuicoes.modulos.bloco_0.r0120 import validar_0120
from contribuicoes.modulos.bloco_0.r0140 import validar_0140
from contribuicoes.modulos.bloco_0.r0145 import validar_0145
from contribuicoes.modulos.bloco_0.r0150 import validar_0150
from contribuicoes.modulos.bloco_0.r0190 import validar_0190
from contribuicoes.modulos.bloco_0.r0200 import validar_0200
from contribuicoes.modulos.bloco_0.r0205 import validar_0205
from contribuicoes.modulos.bloco_0.r0206 import validar_0206
from contribuicoes.modulos.bloco_0.r0208 import validar_0208
from contribuicoes.modulos.bloco_0.r0400 import validar_0400
from contribuicoes.modulos.bloco_0.r0450 import validar_0450
from contribuicoes.modulos.bloco_0.r0500 import validar_0500
from contribuicoes.modulos.bloco_0.r0600 import validar_0600
from contribuicoes.modulos.bloco_0.r0900 import validar_0900

from contribuicoes.modulos.bloco_1.r1010 import validar_1010
from contribuicoes.modulos.bloco_1.r1011 import validar_1011
from contribuicoes.modulos.bloco_1.r1020 import validar_1020
from contribuicoes.modulos.bloco_1.r1050 import validar_1050
from contribuicoes.modulos.bloco_1.r1100 import validar_1100
from contribuicoes.modulos.bloco_1.r1101 import validar_1101
from contribuicoes.modulos.bloco_1.r1102 import validar_1102
from contribuicoes.modulos.bloco_1.r1200 import validar_1200
from contribuicoes.modulos.bloco_1.r1210 import validar_1210
from contribuicoes.modulos.bloco_1.r1220 import validar_1220
from contribuicoes.modulos.bloco_1.r1300 import validar_1300
from contribuicoes.modulos.bloco_1.r1500 import validar_1500
from contribuicoes.modulos.bloco_1.r1501 import validar_1501
from contribuicoes.modulos.bloco_1.r1502 import validar_1502
from contribuicoes.modulos.bloco_1.r1600 import validar_1600
from contribuicoes.modulos.bloco_1.r1610 import validar_1610
from contribuicoes.modulos.bloco_1.r1620 import validar_1620
from contribuicoes.modulos.bloco_1.r1700 import validar_1700
from contribuicoes.modulos.bloco_1.r1800 import validar_1800
from contribuicoes.modulos.bloco_1.r1809 import validar_1809
from contribuicoes.modulos.bloco_1.r1900 import validar_1900

from contribuicoes.modulos.bloco_a.ra010 import validar_a010
from contribuicoes.modulos.bloco_a.ra100 import validar_a100
from contribuicoes.modulos.bloco_a.ra110 import validar_a110
from contribuicoes.modulos.bloco_a.ra111 import validar_a111
from contribuicoes.modulos.bloco_a.ra120 import validar_a120
from contribuicoes.modulos.bloco_a.ra170 import validar_a170

from contribuicoes.modulos.bloco_c.rc010 import validar_c010
from contribuicoes.modulos.bloco_c.rc100 import validar_c100
from contribuicoes.modulos.bloco_c.rc110 import validar_c110
from contribuicoes.modulos.bloco_c.rc111 import validar_c111
from contribuicoes.modulos.bloco_c.rc120 import validar_c120
from contribuicoes.modulos.bloco_c.rc170 import validar_c170
from contribuicoes.modulos.bloco_c.rc175 import validar_c175
from contribuicoes.modulos.bloco_c.rc180 import validar_c180
from contribuicoes.modulos.bloco_c.rc181 import validar_c181
from contribuicoes.modulos.bloco_c.rc185 import validar_c185
from contribuicoes.modulos.bloco_c.rc188 import validar_c188
from contribuicoes.modulos.bloco_c.rc190 import validar_c190
from contribuicoes.modulos.bloco_c.rc191 import validar_c191
from contribuicoes.modulos.bloco_c.rc195 import validar_c195
from contribuicoes.modulos.bloco_c.rc198 import validar_c198
from contribuicoes.modulos.bloco_c.rc199 import validar_c199
from contribuicoes.modulos.bloco_c.rc380 import validar_c380
from contribuicoes.modulos.bloco_c.rc381 import validar_c381
from contribuicoes.modulos.bloco_c.rc385 import validar_c385
from contribuicoes.modulos.bloco_c.rc395 import validar_c395
from contribuicoes.modulos.bloco_c.rc396 import validar_c396
from contribuicoes.modulos.bloco_c.rc400 import validar_c400
from contribuicoes.modulos.bloco_c.rc405 import validar_c405
from contribuicoes.modulos.bloco_c.rc481 import validar_c481
from contribuicoes.modulos.bloco_c.rc485 import validar_c485
from contribuicoes.modulos.bloco_c.rc489 import validar_c489
from contribuicoes.modulos.bloco_c.rc491 import validar_c491
from contribuicoes.modulos.bloco_c.rc495 import validar_c495
from contribuicoes.modulos.bloco_c.rc499 import validar_c499
from contribuicoes.modulos.bloco_c.rc500 import validar_c500
from contribuicoes.modulos.bloco_c.rc501 import validar_c501
from contribuicoes.modulos.bloco_c.rc505 import validar_c505
from contribuicoes.modulos.bloco_c.rc509 import validar_c509
from contribuicoes.modulos.bloco_c.rc600 import validar_c600
from contribuicoes.modulos.bloco_c.rc601 import validar_c601
from contribuicoes.modulos.bloco_c.rc605 import validar_c605
from contribuicoes.modulos.bloco_c.rc609 import validar_c609
from contribuicoes.modulos.bloco_c.rc800 import validar_c800
from contribuicoes.modulos.bloco_c.rc810 import validar_c810
from contribuicoes.modulos.bloco_c.rc820 import validar_c820
from contribuicoes.modulos.bloco_c.rc830 import validar_c830
from contribuicoes.modulos.bloco_c.rc860 import validar_c860
from contribuicoes.modulos.bloco_c.rc870 import validar_c870
from contribuicoes.modulos.bloco_c.rc880 import validar_c880
from contribuicoes.modulos.bloco_c.rc890 import validar_c890

from contribuicoes.modulos.bloco_d.rd010 import validar_d010
from contribuicoes.modulos.bloco_d.rd100 import validar_d100
from contribuicoes.modulos.bloco_d.rd101 import validar_d101
from contribuicoes.modulos.bloco_d.rd105 import validar_d105
from contribuicoes.modulos.bloco_d.rd111 import validar_d111
from contribuicoes.modulos.bloco_d.rd200 import validar_d200
from contribuicoes.modulos.bloco_d.rd201 import validar_d201
from contribuicoes.modulos.bloco_d.rd205 import validar_d205
from contribuicoes.modulos.bloco_d.rd209 import validar_d209
from contribuicoes.modulos.bloco_d.rd300 import validar_d300
from contribuicoes.modulos.bloco_d.rd309 import validar_d309
from contribuicoes.modulos.bloco_d.rd350 import validar_d350
from contribuicoes.modulos.bloco_d.rd359 import validar_d359
from contribuicoes.modulos.bloco_d.rd500 import validar_d500
from contribuicoes.modulos.bloco_d.rd501 import validar_d501
from contribuicoes.modulos.bloco_d.rd505 import validar_d505
from contribuicoes.modulos.bloco_d.rd509 import validar_d509
from contribuicoes.modulos.bloco_d.rd600 import validar_d600
from contribuicoes.modulos.bloco_d.rd601 import validar_d601
from contribuicoes.modulos.bloco_d.rd605 import validar_d605
from contribuicoes.modulos.bloco_d.rd609 import validar_d609

from contribuicoes.modulos.bloco_f.rf010 import validar_f010
from contribuicoes.modulos.bloco_f.rf100 import validar_f100
from contribuicoes.modulos.bloco_f.rf111 import validar_f111
from contribuicoes.modulos.bloco_f.rf120 import validar_f120
from contribuicoes.modulos.bloco_f.rf129 import validar_f129
from contribuicoes.modulos.bloco_f.rf130 import validar_f130
from contribuicoes.modulos.bloco_f.rf139 import validar_f139
from contribuicoes.modulos.bloco_f.rf150 import validar_f150
from contribuicoes.modulos.bloco_f.rf200 import validar_f200
from contribuicoes.modulos.bloco_f.rf205 import validar_f205
from contribuicoes.modulos.bloco_f.rf210 import validar_f210
from contribuicoes.modulos.bloco_f.rf211 import validar_f211
from contribuicoes.modulos.bloco_f.rf500 import validar_f500
from contribuicoes.modulos.bloco_f.rf509 import validar_f509
from contribuicoes.modulos.bloco_f.rf510 import validar_f510
from contribuicoes.modulos.bloco_f.rf519 import validar_f519
from contribuicoes.modulos.bloco_f.rf525 import validar_f525
from contribuicoes.modulos.bloco_f.rf550 import validar_f550
from contribuicoes.modulos.bloco_f.rf559 import validar_f559
from contribuicoes.modulos.bloco_f.rf560 import validar_f560
from contribuicoes.modulos.bloco_f.rf569 import validar_f569
from contribuicoes.modulos.bloco_f.rf600 import validar_f600
from contribuicoes.modulos.bloco_f.rf700 import validar_f700
from contribuicoes.modulos.bloco_f.rf800 import validar_f800

from contribuicoes.modulos.bloco_i.ri010 import validar_i010
from contribuicoes.modulos.bloco_i.ri100 import validar_i100
from contribuicoes.modulos.bloco_i.ri119 import validar_i119
from contribuicoes.modulos.bloco_i.ri200 import validar_i200
from contribuicoes.modulos.bloco_i.ri299 import validar_i299
from contribuicoes.modulos.bloco_i.ri300 import validar_i300
from contribuicoes.modulos.bloco_i.ri399 import validar_i399

from contribuicoes.modulos.bloco_p.rp010 import validar_p010
from contribuicoes.modulos.bloco_p.rp100 import validar_p100
from contribuicoes.modulos.bloco_p.rp110 import validar_p110
from contribuicoes.modulos.bloco_p.rp119 import validar_p199
from contribuicoes.modulos.bloco_p.rp200 import validar_p200
from contribuicoes.modulos.bloco_p.rp210 import validar_p210


VALIDADORES_BLOCO_0 = {
    '0000': validar_0000,
    '0035': validar_0035,
    '0100': validar_0100,
    '0110': validar_0110,
    '0111': validar_0111,
    '0120': validar_0120,
    '0140': validar_0140,
    '0145': validar_0145,
    '0150': validar_0150,
    '0190': validar_0190,
    '0200': validar_0200,
    '0205': validar_0205,
    '0206': validar_0206,
    '0208': validar_0208,
    '0400': validar_0400,
    '0450': validar_0450,
    '0500': validar_0500,
    '0600': validar_0600,
    '0900': validar_0900,
}

VALIDADORES_BLOCO_1 = {
    '1010': validar_1010,
    '1011': validar_1011,
    '1020': validar_1020,
    '1050': validar_1050,
    '1100': validar_1100,
    '1101': validar_1101,
    '1102': validar_1102,
    '1200': validar_1200,
    '1210': validar_1210,
    '1220': validar_1220,
    '1300': validar_1300,
    '1500': validar_1500,
    '1501': validar_1501,
    '1502': validar_1502,
    '1600': validar_1600,
    '1610': validar_1610,
    '1620': validar_1620,
    '1700': validar_1700,
    '1800': validar_1800,
    '1809': validar_1809,
    '1900': validar_1900,
}

VALIDADORES_BLOCO_A = {
    'A010': validar_a010,
    'A100': validar_a100,
    'A110': validar_a110,
    'A111': validar_a111,
    'A120': validar_a120,
    'A170': validar_a170,
}

VALIDADORES_BLOCO_C = {
    "C010": validar_c010,
    "C100": validar_c100,
    "C110": validar_c110,
    "C111": validar_c111,
    "C120": validar_c120,
    "C170": validar_c170,
    "C175": validar_c175,
    "C180": validar_c180,
    "C181": validar_c181,
    "C185": validar_c185,
    "C188": validar_c188,
    "C190": validar_c190,
    "C191": validar_c191,
    "C195": validar_c195,
    "C198": validar_c198,
    "C199": validar_c199,
    "C380": validar_c380,
    "C381": validar_c381,
    "C385": validar_c385,
    "C395": validar_c395,
    "C396": validar_c396,
    "C400": validar_c400,
    "C405": validar_c405,
    "C481": validar_c481,
    "C485": validar_c485,
    "C489": validar_c489,
    "C491": validar_c491,
    "C495": validar_c495,
    "C499": validar_c499,
    "C500": validar_c500,
    "C501": validar_c501,
    "C505": validar_c505,
    "C509": validar_c509,
    "C600": validar_c600,
    "C601": validar_c601,
    "C605": validar_c605,
    "C609": validar_c609,
    "C800": validar_c800,
    "C810": validar_c810,
    "C820": validar_c820,
    "C830": validar_c830,
    "C860": validar_c860,
    "C870": validar_c870,
    "C880": validar_c880,
    "C890": validar_c890
}

VALIDADORES_BLOCO_D = {
    "D010": validar_d010,
    "D100": validar_d100,
    "D101": validar_d101,
    "D105": validar_d105,
    "D111": validar_d111,
    "D200": validar_d200,
    "D201": validar_d201,
    "D205": validar_d205,
    "D209": validar_d209,
    "D300": validar_d300,
    "D309": validar_d309,
    "D350": validar_d350,
    "D359": validar_d359,
    "D500": validar_d500,
    "D501": validar_d501,
    "D505": validar_d505,
    "D509": validar_d509,
    "D600": validar_d600,
    "D601": validar_d601,
    "D605": validar_d605,
    "D609": validar_d609
}

VALIDADORES_BLOCO_F = {
    "F010": validar_f010,
    "F100": validar_f100,
    "F111": validar_f111,
    "F120": validar_f120,
    "F129": validar_f129,
    "F130": validar_f130,
    "F139": validar_f139,
    "F150": validar_f150,
    "F200": validar_f200,
    "F205": validar_f205,
    "F210": validar_f210,
    "F211": validar_f211,
    "F500": validar_f500,
    "F509": validar_f509,
    "F510": validar_f510,
    "F519": validar_f519,
    "F525": validar_f525,
    "F550": validar_f550,
    "F559": validar_f559,
    "F560": validar_f560,
    "F569": validar_f569,
    "F600": validar_f600,
    "F700": validar_f700,
    "F800": validar_f800
}

VALIDADORES_BLOCO_I = {
    "I010": validar_i010,
    "I100": validar_i100,
    "I119": validar_i119,
    "I200": validar_i200,
    "I299": validar_i299,
    "I300": validar_i300,
    "I399": validar_i399
}

VALIDADORES_BLOCO_P = {
    "P010": validar_p010,
    "P100": validar_p100,
    "P110": validar_p110,
    "P199": validar_p199,
    "P200": validar_p200,
    "P210": validar_p210,
}


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', tempfile.gettempdir())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Microsserviço de Arquivos ZIP",
        "description": "API para receber e devolver arquivos ZIP",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.getenv('LOG_DIR', 'logs')

Path(LOG_DIR).mkdir(exist_ok=True)

logger.remove()
logger.add(
    f"{LOG_DIR}/app_{{time}}.log",
    rotation="10 MB",
    retention="10 days",
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    encoding="utf-8",
    enqueue=True
)

logger.add(
    lambda msg: print(msg, end=''),
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    colorize=True
)


def extrair_bloco_registro(linha):
    """
    Extrai o bloco de uma linha do arquivo SPED.
    
    Args:
        linha: String com a linha do arquivo SPED
        
    Returns:
        String com o identificador do bloco (F, 0, 1, 9, A, C, D, etc.) ou None
    """
    linha = linha.strip()
    if not linha or not linha.startswith('|'):
        return None
    
    partes = [p.strip() for p in linha.split('|') if p.strip()]
    
    if not partes:
        return None
    
    codigo_registro = partes[0]
    if not codigo_registro:
        return None
    
    primeiro_caractere = codigo_registro[0].upper()
    blocos_validos = ['0', '1', '9', 'A', 'C', 'D', 'F', 'I', 'M', 'P']
    
    if primeiro_caractere in blocos_validos:
        return primeiro_caractere
    
    return None


def verificar_bloco_f(conteudo_arquivo):
    """
    Verifica se o conteúdo do arquivo contém registros do bloco F.
    Segue o padrão de leitura usado em parser_bloco_d.py.
    
    Args:
        conteudo_arquivo: Bytes ou string com o conteúdo do arquivo
        
    Returns:
        True se contém bloco F, False caso contrário
    """
    logger.info("Iniciando verificação de bloco F")
    
    if isinstance(conteudo_arquivo, str):
        conteudo_bytes = conteudo_arquivo.encode('utf-8')
    else:
        conteudo_bytes = conteudo_arquivo
    
    encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
    arquivo = None
    
    for encoding in encodings:
        try:
            texto = conteudo_bytes.decode(encoding)
            arquivo = io.StringIO(texto)
            
            arquivo.readline()
            arquivo.seek(0)
            
            logger.info(f"Encoding detectado para verificação de bloco F: {encoding}")
            break
            
        except (UnicodeDecodeError, UnicodeError):
            if arquivo:
                arquivo.close()
            arquivo = None
            continue
    
    if arquivo is None:
        logger.warning("Não foi possível determinar o encoding do arquivo para verificar bloco F")
        return False
    
    try:
        linhas_verificadas = 0
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            
            if linha.startswith('|'):
                bloco = extrair_bloco_registro(linha)
                logger.debug(f"Bloco extraído na verificação de bloco F: {bloco}")
                if bloco == 'F':
                    partes = [p.strip() for p in linha.split('|') if p.strip()]
                    codigo_registro = partes[0] if partes else 'F'
                    logger.info(f"Bloco F encontrado no arquivo (registro: {codigo_registro}) - RETORNANDO TRUE")
                    return True
            
            linhas_verificadas += 1
            if linhas_verificadas % 1000 == 0:
                logger.debug(f"Verificadas {linhas_verificadas} linhas...")
        
        logger.info(f"Nenhum registro do bloco F encontrado após verificar {linhas_verificadas} linhas")
        return False
        
    except Exception as e:
        logger.error(f"Erro ao verificar bloco F: {str(e)}")
        return False
    finally:
        if arquivo:
            arquivo.close()


def extrair_blocos_arquivo(conteudo_arquivo):
    """
    Extrai todos os blocos e registros de um arquivo SPED.
    Segue o padrão de leitura usado em parser_bloco_d.py.
    
    Args:
        conteudo_arquivo: Bytes ou string com o conteúdo do arquivo
        
    Returns:
        Dicionário com estrutura:
        {
            'blocos': {
                '0': {'0000': 1, '0001': 1, '0100': 5, ...},
                '1': {'1001': 2, '1010': 1, ...},
                'F': {'F001': 1, 'F010': 1, 'F120': 100, ...},
                ...
            },
            'total_registros': int,
            'blocos_encontrados': ['0', '1', 'F', ...]
        }
    """
    from collections import defaultdict
    
    blocos_dict = defaultdict(lambda: defaultdict(int))
    total_registros = 0
    
    if isinstance(conteudo_arquivo, str):
        conteudo_bytes = conteudo_arquivo.encode('utf-8')
    else:
        conteudo_bytes = conteudo_arquivo
    
    encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
    arquivo = None
    
    for encoding in encodings:
        try:
            texto = conteudo_bytes.decode(encoding)
            arquivo = io.StringIO(texto)
            arquivo.readline()
            arquivo.seek(0)
            logger.debug(f"Encoding detectado para extração de blocos: {encoding}")
            break
        except (UnicodeDecodeError, UnicodeError):
            if arquivo:
                arquivo.close()
            arquivo = None
            continue
    
    if arquivo is None:
        logger.warning("Não foi possível determinar o encoding do arquivo para extrair blocos")
        return {
            'blocos': {},
            'total_registros': 0,
            'blocos_encontrados': []
        }
    
    try:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            
            if linha.startswith('|'):
                bloco = extrair_bloco_registro(linha)
                if bloco:
                    partes = [p.strip() for p in linha.split('|') if p.strip()]
                    if partes:
                        codigo_registro = partes[0].upper()
                        blocos_dict[bloco][codigo_registro] += 1
                        total_registros += 1
        
        blocos_encontrados = sorted(blocos_dict.keys())
        
        resultado = {
            'blocos': dict(blocos_dict),
            'total_registros': total_registros,
            'blocos_encontrados': blocos_encontrados
        }
        
        logger.debug(f"Extraídos {total_registros} registros de {len(blocos_encontrados)} blocos")
        
        return resultado
        
    except Exception as e:
        logger.error(f"Erro ao extrair blocos: {str(e)}")
        return {
            'blocos': {},
            'total_registros': 0,
            'blocos_encontrados': []
        }
    finally:
        if arquivo:
            arquivo.close()


def validar_registros_blocos_0_1(conteudo_arquivo):
    """
    Valida os registros dos blocos 0, 1, A, C, D, F, I e P de um arquivo SPED Contribuições.
    
    Args:
        conteudo_arquivo: Bytes ou string com o conteúdo do arquivo
        
    Returns:
        Dicionário com estrutura:
        {
            'bloco_0': {
                '0000': [resultados_validacao],
                '0100': [resultados_validacao],
                ...
            },
            'bloco_1': {
                '1010': [resultados_validacao],
                '1100': [resultados_validacao],
                ...
            },
            'bloco_a': {
                'A010': [resultados_validacao],
                'A100': [resultados_validacao],
                ...
            },
            'bloco_c': {
                'C010': [resultados_validacao],
                'C100': [resultados_validacao],
                ...
            },
            'bloco_d': {
                'D010': [resultados_validacao],
                'D100': [resultados_validacao],
                ...
            },
            'bloco_f': {
                'F010': [resultados_validacao],
                'F100': [resultados_validacao],
                ...
            },
            'bloco_i': {
                'I010': [resultados_validacao],
                'I100': [resultados_validacao],
                ...
            },
            'bloco_p': {
                'P010': [resultados_validacao],
                'P100': [resultados_validacao],
                ...
            },
            'total_validacoes': int,
            'registros_validados': int
        }
    """
    resultado = {
        'bloco_0': {},
        'bloco_1': {},
        'bloco_a': {},
        'bloco_c': {},
        'bloco_d': {},
        'bloco_f': {},
        'bloco_i': {},
        'bloco_p': {},
        'total_validacoes': 0,
        'registros_validados': 0
    }
    
    if isinstance(conteudo_arquivo, str):
        conteudo_bytes = conteudo_arquivo.encode('utf-8')
    else:
        conteudo_bytes = conteudo_arquivo
    
    encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
    arquivo = None
    
    for encoding in encodings:
        try:
            texto = conteudo_bytes.decode(encoding)
            arquivo = io.StringIO(texto)
            arquivo.readline()
            arquivo.seek(0)
            logger.debug(f"Encoding detectado para validação: {encoding}")
            break
        except (UnicodeDecodeError, UnicodeError):
            if arquivo:
                arquivo.close()
            arquivo = None
            continue
    
    if arquivo is None:
        logger.warning("Não foi possível determinar o encoding do arquivo para validação")
        return resultado
    
    # Agrupa linhas por código de registro
    linhas_bloco_0 = {}
    linhas_bloco_1 = {}
    linhas_bloco_a = {}
    linhas_bloco_c = {}
    linhas_bloco_d = {}
    linhas_bloco_f = {}
    linhas_bloco_i = {}
    linhas_bloco_p = {}
    
    try:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or not linha.startswith('|'):
                continue
            
            bloco = extrair_bloco_registro(linha)
            if not bloco:
                continue
            
            partes = [p.strip() for p in linha.split('|') if p.strip()]
            if not partes:
                continue
            
            codigo_registro = partes[0].upper()
            
            # logger.info(f'Bloco -> {bloco}')
            
            # Agrupa linhas do bloco 0
            if bloco == '0' and codigo_registro in VALIDADORES_BLOCO_0:
                if codigo_registro not in linhas_bloco_0:
                    linhas_bloco_0[codigo_registro] = []
                linhas_bloco_0[codigo_registro].append(linha)
            
            # Agrupa linhas do bloco 1
            elif bloco == '1' and codigo_registro in VALIDADORES_BLOCO_1:
                if codigo_registro not in linhas_bloco_1:
                    linhas_bloco_1[codigo_registro] = []
                linhas_bloco_1[codigo_registro].append(linha)
            
            # Agrupa linhas do bloco A
            elif bloco == 'A' and codigo_registro in VALIDADORES_BLOCO_A:
                if codigo_registro not in linhas_bloco_a:
                    linhas_bloco_a[codigo_registro] = []
                linhas_bloco_a[codigo_registro].append(linha)
                
            # Agrupa linhas do bloco C (todos os registros, mesmo sem validador)
            elif bloco == 'C':
                if codigo_registro not in linhas_bloco_c:
                    linhas_bloco_c[codigo_registro] = []
                linhas_bloco_c[codigo_registro].append(linha)
            
            # Agrupa linhas do bloco D (todos os registros, mesmo sem validador)
            elif bloco == 'D':
                if codigo_registro not in linhas_bloco_d:
                    linhas_bloco_d[codigo_registro] = []
                linhas_bloco_d[codigo_registro].append(linha)
            
            # Agrupa linhas do bloco F (todos os registros, mesmo sem validador)
            elif bloco == 'F':
                if codigo_registro not in linhas_bloco_f:
                    linhas_bloco_f[codigo_registro] = []
                linhas_bloco_f[codigo_registro].append(linha)
            
            # Agrupa linhas do bloco I (todos os registros, mesmo sem validador)
            elif bloco == 'I':
                if codigo_registro not in linhas_bloco_i:
                    linhas_bloco_i[codigo_registro] = []
                linhas_bloco_i[codigo_registro].append(linha)

            # Agrupa linhas do bloco P (todos os registros, mesmo sem validador)
            elif bloco == 'P':
                if codigo_registro not in linhas_bloco_p:
                    linhas_bloco_p[codigo_registro] = []
                linhas_bloco_p[codigo_registro].append(linha)
            
        # logger.info(f'Linhas do bloco C -> {linhas_bloco_c}')
        # Valida registros do bloco 0
        for codigo_registro, linhas in linhas_bloco_0.items():
            try:
                validador = VALIDADORES_BLOCO_0[codigo_registro]
                resultado_validacao = validador(linhas)
                
                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_0'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_0'][codigo_registro] = []
                    
            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco 0: {str(e)}")
                resultado['bloco_0'][codigo_registro] = []
        
        # Valida registros do bloco 1
        for codigo_registro, linhas in linhas_bloco_1.items():
            try:
                validador = VALIDADORES_BLOCO_1[codigo_registro]
                resultado_validacao = validador(linhas)
                
                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_1'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_1'][codigo_registro] = []
                    
            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco 1: {str(e)}")
                resultado['bloco_1'][codigo_registro] = []
        
        # Valida registros do bloco A
        for codigo_registro, linhas in linhas_bloco_a.items():
            try:
                validador = VALIDADORES_BLOCO_A[codigo_registro]
                resultado_validacao = validador(linhas)
                
                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_a'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_a'][codigo_registro] = []
                    
            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco A: {str(e)}")
                resultado['bloco_a'][codigo_registro] = []
        
        # Valida registros do bloco C
        for codigo_registro, linhas in linhas_bloco_c.items():
            # Se não houver validador para este registro, retorna vazio
            if codigo_registro not in VALIDADORES_BLOCO_C:
                logger.debug(f"Nenhum validador encontrado para registro {codigo_registro} do bloco C, retornando vazio")
                resultado['bloco_c'][codigo_registro] = []
                continue
            
            try:
                validador = VALIDADORES_BLOCO_C[codigo_registro]
                resultado_validacao = validador(linhas)
                
                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_c'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_c'][codigo_registro] = []
                    
            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco C: {str(e)}")
                resultado['bloco_c'][codigo_registro] = []
        
        # Valida registros do bloco D
        for codigo_registro, linhas in linhas_bloco_d.items():
            # Se não houver validador para este registro, retorna vazio
            if codigo_registro not in VALIDADORES_BLOCO_D:
                logger.debug(f"Nenhum validador encontrado para registro {codigo_registro} do bloco D, retornando vazio")
                resultado['bloco_d'][codigo_registro] = []
                continue
            
            try:
                validador = VALIDADORES_BLOCO_D[codigo_registro]
                resultado_validacao = validador(linhas)
                
                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_d'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_d'][codigo_registro] = []
                    
            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco D: {str(e)}")
                resultado['bloco_d'][codigo_registro] = []
        
        # Valida registros do bloco F
        for codigo_registro, linhas in linhas_bloco_f.items():
            # Se não houver validador para este registro, retorna vazio
            if codigo_registro not in VALIDADORES_BLOCO_F:
                logger.debug(f"Nenhum validador encontrado para registro {codigo_registro} do bloco F, retornando vazio")
                resultado['bloco_f'][codigo_registro] = []
                continue
            
            try:
                validador = VALIDADORES_BLOCO_F[codigo_registro]
                resultado_validacao = validador(linhas)
                
                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_f'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_f'][codigo_registro] = []
                    
            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco F: {str(e)}")
                resultado['bloco_f'][codigo_registro] = []
        
        # Valida registros do bloco I
        for codigo_registro, linhas in linhas_bloco_i.items():
            # Se não houver validador para este registro, retorna vazio
            if codigo_registro not in VALIDADORES_BLOCO_I:
                logger.debug(f"Nenhum validador encontrado para registro {codigo_registro} do bloco I, retornando vazio")
                resultado['bloco_i'][codigo_registro] = []
                continue
            
            try:
                validador = VALIDADORES_BLOCO_I[codigo_registro]
                resultado_validacao = validador(linhas)
                
                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_i'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_i'][codigo_registro] = []
                    
            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco I: {str(e)}")
                resultado['bloco_i'][codigo_registro] = []

        # Valida registros do bloco P
        for codigo_registro, linhas in linhas_bloco_p.items():
            # Se não houver validador para este registro, retorna vazio
            if codigo_registro not in VALIDADORES_BLOCO_P:
                logger.debug(f"Nenhum validador encontrado para registro {codigo_registro} do bloco P, retornando vazio")
                resultado['bloco_p'][codigo_registro] = []
                continue

            try:
                validador = VALIDADORES_BLOCO_P[codigo_registro]
                resultado_validacao = validador(linhas)

                # Converte JSON string para objeto Python
                try:
                    resultado_json = json.loads(resultado_validacao)
                    resultado['bloco_p'][codigo_registro] = resultado_json
                    resultado['registros_validados'] += len(linhas)
                    resultado['total_validacoes'] += len(resultado_json) if isinstance(resultado_json, list) else 1
                except json.JSONDecodeError:
                    logger.warning(f"Erro ao decodificar JSON do registro {codigo_registro}")
                    resultado['bloco_p'][codigo_registro] = []

            except Exception as e:
                logger.error(f"Erro ao validar registro {codigo_registro} do bloco P: {str(e)}")
                resultado['bloco_p'][codigo_registro] = []
        
        logger.debug(f"Validação concluída: {resultado['registros_validados']} registros validados, "
                    f"{resultado['total_validacoes']} validações realizadas")
        
    except Exception as e:
        logger.error(f"Erro ao processar validação: {str(e)}")
    finally:
        if arquivo:
            arquivo.close()
    
    return resultado


def classificar_arquivo_sped(nome_arquivo, conteudo_arquivo):
    """
    Classifica um arquivo SPED como EFD Fiscal ou EFD Contribuições.
    
    Args:
        nome_arquivo: Nome do arquivo
        conteudo_arquivo: Conteúdo do arquivo (bytes)
        
    Returns:
        Tupla: (classificacao, blocos_info)
        classificacao: 'EFD_CONTRIBUICOES' ou 'EFD_FISCAL'
        blocos_info: Dicionário com informações dos blocos extraídos
    """
    logger.info(f"Iniciando classificação do arquivo '{nome_arquivo}'")
    tem_bloco_f = verificar_bloco_f(conteudo_arquivo)
    logger.info(f"Resultado da verificação de bloco F para '{nome_arquivo}': {tem_bloco_f}")
    
    blocos_info = extrair_blocos_arquivo(conteudo_arquivo)
    logger.info(f"Blocos encontrados em '{nome_arquivo}': {blocos_info['blocos_encontrados']}")
    
    if tem_bloco_f:
        logger.info(f"Arquivo '{nome_arquivo}' classificado como EFD Contribuições (contém bloco F)")
        return 'EFD_CONTRIBUICOES', blocos_info
    else:
        logger.info(f"Arquivo '{nome_arquivo}' classificado como EFD Fiscal (não contém bloco F)")
        return 'EFD_FISCAL', blocos_info


def processar_zip_arquivos(zip_path):
    """
    Processa um arquivo ZIP e classifica cada arquivo dentro dele, extraindo também os blocos.
    
    Args:
        zip_path: Caminho para o arquivo ZIP
        
    Returns:
        Dicionário com informações sobre os arquivos classificados e seus blocos:
        {
            'efd_fiscal': [
                {
                    'nome_arquivo': 'arquivo1.txt',
                    'blocos': {
                        'blocos': {'0': {'0000': 1, ...}, '1': {...}, ...},
                        'total_registros': 150,
                        'blocos_encontrados': ['0', '1', '9']
                    }
                },
                ...
            ],
            'efd_contribuicoes': [
                {
                    'nome_arquivo': 'arquivo2.txt',
                    'blocos': {
                        'blocos': {'0': {...}, 'F': {'F001': 1, 'F120': 50, ...}, ...},
                        'total_registros': 200,
                        'blocos_encontrados': ['0', 'F', 'M']
                    }
                },
                ...
            ],
            'total_arquivos': int,
            'arquivos_nao_processados': [lista de nomes de arquivos]
        }
    """
    resultado = {
        'efd_fiscal': [],
        'efd_contribuicoes': [],
        'total_arquivos': 0,
        'arquivos_nao_processados': []
    }
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            arquivos_zip = zip_ref.namelist()
            resultado['total_arquivos'] = len(arquivos_zip)
            
            logger.info(f"Processando {len(arquivos_zip)} arquivos do ZIP")
            
            for nome_arquivo in arquivos_zip:
                if nome_arquivo.endswith('/'):
                    continue
                
                try:
                    conteudo = zip_ref.read(nome_arquivo)
                    extensoes_sped = ['.txt', '.sped', '.efd']
                    tem_extensao_sped = any(nome_arquivo.lower().endswith(ext) for ext in extensoes_sped)
                    
                    if not tem_extensao_sped:
                        try:
                            conteudo.decode('latin-1')
                        except:
                            resultado['arquivos_nao_processados'].append(nome_arquivo)
                            logger.debug(f"Arquivo '{nome_arquivo}' não parece ser texto SPED, ignorado")
                            continue
                    
                    classificacao, blocos_info = classificar_arquivo_sped(nome_arquivo, conteudo)
                    
                    arquivo_info = {
                        'nome_arquivo': nome_arquivo,
                        'blocos': {
                            'blocos': blocos_info['blocos'],
                            'total_registros': blocos_info['total_registros'],
                            'blocos_encontrados': blocos_info['blocos_encontrados']
                        }
                    }
                    
                    # Se for EFD Contribuições, valida registros do bloco 0, 1, A, C, D, F, I e P
                    if classificacao == 'EFD_CONTRIBUICOES':
                        # Verifica se há blocos 0, 1, A, C, D, F, I ou P para validar
                        tem_bloco_0 = '0' in blocos_info['blocos_encontrados']
                        tem_bloco_1 = '1' in blocos_info['blocos_encontrados']
                        tem_bloco_a = 'A' in blocos_info['blocos_encontrados']
                        tem_bloco_c = 'C' in blocos_info['blocos_encontrados']
                        tem_bloco_d = 'D' in blocos_info['blocos_encontrados']
                        tem_bloco_f = 'F' in blocos_info['blocos_encontrados']
                        tem_bloco_i = 'I' in blocos_info['blocos_encontrados']
                        tem_bloco_p = 'P' in blocos_info['blocos_encontrados']
                        
                        if tem_bloco_0 or tem_bloco_1 or tem_bloco_a or tem_bloco_c or tem_bloco_d or tem_bloco_f or tem_bloco_i or tem_bloco_p:
                            logger.info(f"Validando registros dos blocos 0, 1, A, C, D, F, I e P do arquivo '{nome_arquivo}'")
                            validacoes = validar_registros_blocos_0_1(conteudo)
                            arquivo_info['validacoes'] = {
                                'bloco_0': validacoes['bloco_0'],
                                'bloco_1': validacoes['bloco_1'],
                                'bloco_a': validacoes.get('bloco_a', {}),
                                'bloco_c': validacoes.get('bloco_c', {}),
                                'bloco_d': validacoes.get('bloco_d', {}),
                                'bloco_f': validacoes.get('bloco_f', {}),
                                'bloco_i': validacoes.get('bloco_i', {}),
                                'bloco_p': validacoes.get('bloco_p', {}),
                                'total_validacoes': validacoes['total_validacoes'],
                                'registros_validados': validacoes['registros_validados']
                            }
                        else:
                            arquivo_info['validacoes'] = {
                                'bloco_0': {},
                                'bloco_1': {},
                                'bloco_a': {},
                                'bloco_c': {},
                                'bloco_d': {},
                                'bloco_f': {},
                                'bloco_i': {},
                                'bloco_p': {},
                                'total_validacoes': 0,
                                'registros_validados': 0
                            }
                        
                        resultado['efd_contribuicoes'].append(arquivo_info)
                    elif classificacao == 'EFD_FISCAL':
                        resultado['efd_fiscal'].append(arquivo_info)
                    else:
                        resultado['arquivos_nao_processados'].append(nome_arquivo)
                        
                except Exception as e:
                    logger.error(f"Erro ao processar arquivo '{nome_arquivo}' do ZIP: {str(e)}")
                    resultado['arquivos_nao_processados'].append(nome_arquivo)
    
    except Exception as e:
        logger.error(f"Erro ao processar ZIP: {str(e)}")
        raise
    
    logger.info(f"Classificação concluída: {len(resultado['efd_fiscal'])} EFD Fiscal, "
                f"{len(resultado['efd_contribuicoes'])} EFD Contribuições, "
                f"{len(resultado['arquivos_nao_processados'])} não processados")
    
    return resultado


@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check
    ---
    tags:
      - Health
    responses:
      200:
        description: Serviço está funcionando
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
    """
    logger.info("Health check realizado")
    return jsonify({"status": "ok"}), 200


@app.route('/upload-zip', methods=['POST'])
def upload_zip():
    """
    Recebe um arquivo ZIP
    ---
    tags:
      - Arquivos ZIP
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: Arquivo ZIP a ser enviado
    responses:
      200:
        description: Arquivo recebido com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Arquivo recebido com sucesso"
            filename:
              type: string
              example: "arquivo.zip"
            size:
              type: integer
              example: 1024
            files_count:
              type: integer
              example: 5
            classificacao:
              type: object
              properties:
                efd_fiscal:
                  type: object
                  properties:
                    quantidade:
                      type: integer
                      example: 3
                    arquivos:
                      type: array
                      items:
                        type: object
                        properties:
                          nome_arquivo:
                            type: string
                            example: "arquivo1.txt"
                          blocos:
                            type: object
                            properties:
                              blocos:
                                type: object
                                description: "Blocos encontrados no arquivo, agrupados por tipo de bloco"
                                example:
                                  "0": {"0000": 1, "0001": 1, "0100": 5}
                                  "1": {"1001": 2, "1010": 1}
                                  "9": {"9001": 1, "9990": 1}
                              total_registros:
                                type: integer
                                example: 150
                              blocos_encontrados:
                                type: array
                                items:
                                  type: string
                                example: ["0", "1", "9"]
                efd_contribuicoes:
                  type: object
                  properties:
                    quantidade:
                      type: integer
                      example: 2
                    arquivos:
                      type: array
                      items:
                        type: object
                        properties:
                          nome_arquivo:
                            type: string
                            example: "arquivo3.txt"
                          blocos:
                            type: object
                            properties:
                              blocos:
                                type: object
                                description: "Blocos encontrados no arquivo, agrupados por tipo de bloco"
                                example:
                                  "0": {"0000": 1, "0001": 1}
                                  "F": {"F001": 1, "F010": 1, "F120": 50}
                                  "M": {"M100": 10, "M200": 5}
                              total_registros:
                                type: integer
                                example: 200
                              blocos_encontrados:
                                type: array
                                items:
                                  type: string
                                example: ["0", "F", "M"]
                          validacoes:
                            type: object
                            description: "Resultados das validações dos registros dos blocos 0, 1, A, C, D, F e I"
                            properties:
                              bloco_0:
                                type: object
                                description: "Validações dos registros do bloco 0"
                                example:
                                  "0000": [{"REG": {"titulo": "Registro", "valor": "0000"}}]
                                  "0100": [{"REG": {"titulo": "Registro", "valor": "0100"}}]
                              bloco_1:
                                type: object
                                description: "Validações dos registros do bloco 1"
                                example:
                                  "1010": [{"REG": {"titulo": "Registro", "valor": "1010"}}]
                                  "1100": [{"REG": {"titulo": "Registro", "valor": "1100"}}]
                              bloco_a:
                                type: object
                                description: "Validações dos registros do bloco A"
                                example:
                                  "A010": [{"REG": {"titulo": "Registro", "valor": "A010"}}]
                                  "A100": [{"REG": {"titulo": "Registro", "valor": "A100"}}]
                              bloco_c:
                                type: object
                                description: "Validações dos registros do bloco C"
                                example:
                                  "C010": [{"REG": {"titulo": "Registro", "valor": "C010"}}]
                                  "C100": [{"REG": {"titulo": "Registro", "valor": "C100"}}]
                                  "C001": []
                              bloco_d:
                                type: object
                                description: "Validações dos registros do bloco D"
                                example:
                                  "D010": [{"REG": {"titulo": "Registro", "valor": "D010"}}]
                                  "D100": [{"REG": {"titulo": "Registro", "valor": "D100"}}]
                                  "D001": []
                              bloco_f:
                                type: object
                                description: "Validações dos registros do bloco F"
                                example:
                                  "F010": [{"REG": {"titulo": "Registro", "valor": "F010"}}]
                                  "F100": [{"REG": {"titulo": "Registro", "valor": "F100"}}]
                                  "F001": []
                              bloco_i:
                                type: object
                                description: "Validações dos registros do bloco I"
                                example:
                                  "I010": [{"REG": {"titulo": "Registro", "valor": "I010"}}]
                                  "I100": [{"REG": {"titulo": "Registro", "valor": "I100"}}]
                                  "I001": []
                              total_validacoes:
                                type: integer
                                example: 150
                              registros_validados:
                                type: integer
                                example: 50
                nao_processados:
                  type: object
                  properties:
                    quantidade:
                      type: integer
                      example: 0
                    arquivos:
                      type: array
                      items:
                        type: string
                      example: []
      400:
        description: Erro na requisição
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Nenhum arquivo foi enviado"
      500:
        description: Erro interno do servidor
    """
    try:
        if 'file' not in request.files:
            logger.warning("Tentativa de upload sem arquivo")
            return jsonify({"error": "Nenhum arquivo foi enviado"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            logger.warning("Tentativa de upload com nome de arquivo vazio")
            return jsonify({"error": "Nenhum arquivo foi selecionado"}), 400
        
        if not file.filename.lower().endswith('.zip'):
            logger.warning(f"Tentativa de upload de arquivo não ZIP: {file.filename}")
            return jsonify({"error": "Apenas arquivos ZIP são aceitos"}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                files_count = len([f for f in zip_ref.namelist() if not f.endswith('/')])
                logger.info(f"Arquivo ZIP recebido: {filename} ({file_size} bytes, {files_count} arquivos)")
        except zipfile.BadZipFile:
            logger.error(f"Arquivo ZIP inválido: {filename}")
            os.remove(filepath)
            return jsonify({"error": "Arquivo ZIP inválido ou corrompido"}), 400
        
        try:
            resultado_classificacao = processar_zip_arquivos(filepath)
            
            resposta = {
                "message": "Arquivo recebido e processado com sucesso",
                "filename": filename,
                "size": file_size,
                "total_arquivos": resultado_classificacao['total_arquivos'],
                "classificacao": {
                    "efd_fiscal": {
                        "quantidade": len(resultado_classificacao['efd_fiscal']),
                        "arquivos": [
                            {
                                "nome_arquivo": arquivo['nome_arquivo'],
                                "blocos": arquivo['blocos']
                            }
                            for arquivo in resultado_classificacao['efd_fiscal']
                        ]
                    },
                    "efd_contribuicoes": {
                        "quantidade": len(resultado_classificacao['efd_contribuicoes']),
                        "arquivos": [
                            {
                                "nome_arquivo": arquivo['nome_arquivo'],
                                "blocos": arquivo['blocos'],
                                "validacoes": arquivo.get('validacoes', {
                                    'bloco_0': {},
                                    'bloco_1': {},
                                    'bloco_a': {},
                                    'bloco_c': {},
                                    'bloco_d': {},
                                    'bloco_f': {},
                                    'bloco_i': {},
                                    'total_validacoes': 0,
                                    'registros_validados': 0
                                })
                            }
                            for arquivo in resultado_classificacao['efd_contribuicoes']
                        ]
                    },
                    "nao_processados": {
                        "quantidade": len(resultado_classificacao['arquivos_nao_processados']),
                        "arquivos": resultado_classificacao['arquivos_nao_processados']
                    }
                }
            }
            
            logger.info(f"Processamento concluído: {len(resultado_classificacao['efd_fiscal'])} EFD Fiscal, "
                       f"{len(resultado_classificacao['efd_contribuicoes'])} EFD Contribuições")
            
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.debug(f"Arquivo temporário removido: {filepath}")
            except Exception as e:
                logger.warning(f"Erro ao remover arquivo temporário: {str(e)}")
            
            return jsonify(resposta), 200
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivos do ZIP: {str(e)}")
            return jsonify({
                "message": "Arquivo recebido, mas houve erro ao processar",
                "filename": filename,
                "size": file_size,
                "error": f"Erro ao processar arquivos: {str(e)}"
            }), 500
        
    except Exception as e:
        logger.error(f"Erro ao processar upload: {str(e)}")
        return jsonify({"error": f"Erro ao processar arquivo: {str(e)}"}), 500


@app.route('/download-zip', methods=['GET'])
def download_zip():
    """
    Devolve um arquivo ZIP
    ---
    tags:
      - Arquivos ZIP
    parameters:
      - in: query
        name: filename
        type: string
        required: false
        description: Nome do arquivo ZIP a ser baixado (opcional)
    responses:
      200:
        description: Arquivo ZIP retornado com sucesso
        schema:
          type: file
      404:
        description: Arquivo não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Arquivo não encontrado"
      500:
        description: Erro interno do servidor
    """
    try:
        # Obtém o nome do arquivo da query string (opcional)
        requested_filename = request.args.get('filename', 'output.zip')
        filename = secure_filename(requested_filename)
        
        # Cria um arquivo ZIP temporário com alguns arquivos de exemplo
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_zip_path = temp_zip.name
        temp_zip.close()
        
        try:
            # Cria um ZIP com arquivos de exemplo
            with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                # Adiciona alguns arquivos de exemplo
                zip_ref.writestr('exemplo1.txt', 'Este é um arquivo de exemplo 1')
                zip_ref.writestr('exemplo2.txt', 'Este é um arquivo de exemplo 2')
                zip_ref.writestr('exemplo3.txt', 'Este é um arquivo de exemplo 3')
            
            logger.info(f"Arquivo ZIP gerado: {filename}")
            
            return send_file(
                temp_zip_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            logger.error(f"Erro ao criar arquivo ZIP: {str(e)}")
            if os.path.exists(temp_zip_path):
                os.remove(temp_zip_path)
            return jsonify({"error": f"Erro ao criar arquivo ZIP: {str(e)}"}), 500
            
    except Exception as e:
        logger.error(f"Erro ao processar download: {str(e)}")
        return jsonify({"error": f"Erro ao processar download: {str(e)}"}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handler para arquivos muito grandes"""
    logger.warning("Tentativa de upload de arquivo muito grande")
    return jsonify({"error": "Arquivo muito grande. Tamanho máximo: 100MB"}), 413


@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas"""
    logger.warning(f"Rota não encontrada: {request.path}")
    return jsonify({"error": "Rota não encontrada"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    logger.error(f"Erro interno: {str(error)}")
    return jsonify({"error": "Erro interno do servidor"}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info("Iniciando microsserviço Flask em modo desenvolvimento...")
    logger.info(f"Swagger disponível em: http://localhost:{port}/swagger")
    logger.warning("ATENÇÃO: Modo desenvolvimento ativado. Use Gunicorn em produção!")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
