# Bloco 9 - Versão 3.1.8


BLOCO 9: CONTROLE E ENCERRAMENTO DO ARQUIVO DIGITAL
Este bloco representa os totais de registros e serve como forma de controle para batimentos e verificações.
REGISTRO 9001: ABERTURA DO BLOCO 9
Este registro deve sempre ser gerado e representa a abertura do bloco 9.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “9001”. C 004 - O
02 IND_MOV Indicador de movimento: N 001* - O
0 - Bloco com dados informados;
1 - Bloco sem dados informados.
Observações:
Nível hierárquico - 1
Ocorrência – um por Arquivo
Campo 01 (REG) - Valor Válido: [9001]
Campo 02 (IND_MOV) - Valor Válido: [0]
REGISTRO 9900: REGISTROS DO ARQUIVO.
Todos os registros referenciados neste arquivo, inclusive os posteriores a este registro, devem ter uma linha totalizadora do seu número de ocorrência.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “9900”. C 004 - O
02 REG_BLC Registro que será totalizado no próximo campo. C 004 - O
03 QTD_REG_BLC Total de registros do tipo informado no campo anterior. N - - O
Observações:
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [9900]
Campo 02 (REG_BLC) - Preenchimento: informar cada um dos códigos de registros válidos deste arquivo, que será totalizado no próximo campo QTD_REG_BLC.
Campo 03 (QTD_REG_BLC) - Validação: verifica se o número de linhas no arquivo do tipo informado no campo REG_BLC do registro 9900 é igual ao valor informado neste campo.
----
REGISTRO 9990: ENCERRAMENTO DO BLOCO 9
Este registro destina-se a identificar o encerramento do bloco 9 e a informar a quantidade de linhas (registros) existentes no bloco.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “9990”. C 004 - O
02 QTD_LIN_9 Quantidade total de linhas do Bloco 9. N - - O
Observações:
Nível hierárquico - 1
Ocorrência – um por Arquivo
Campo 01 (REG) - Valor Válido: [9990]
Campo 02 (QTD_LIN_9) - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco. Para este cálculo, o registro 9999, apesar de não pertencer ao Bloco 9, também deve ser contabilizado nesta soma.
Validação: o número de linhas (registros) existentes no bloco 9 é igual ao valor informado no campo QTD_LIN_9.
REGISTRO 9999: ENCERRAMENTO DO ARQUIVO DIGITAL.
Este registro destina-se a identificar o encerramento do arquivo digital e a informar a quantidade de linhas (registros) existentes no arquivo.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “9999”. C 004 - O
02 QTD_LIN Quantidade total de linhas do arquivo digital. N - - O
Observações:
Nível hierárquico - 0
Ocorrência – um por Arquivo
Campo 01 (REG) - Valor Válido: [9999]
Campo 02 (QTD_LIN) - Preenchimento: a quantidade de linhas a ser informada deve considerar também o próprio registro 9999.
Validação: o número de linhas (registros) existentes no arquivo inteiro é igual ao valor informado no campo QTD_LIN.
Seção 5 – Obrigatoriedade dos Registros
Os estabelecimentos obrigados à EFD-ICMS/IPI, mesmo com atividades paralisadas no período, ou seja, SEM MOVIMENTO, devem apresentar o arquivo informando, no mínimo, os registros obrigatórios. O histórico da obrigatoriedade dos registros consta nas tabelas do item 2.6.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e suas alterações (http://www.fazenda.gov.br/confaz/).
Os contribuintes do IPI situados em Pernambuco e no Distrito Federal (obrigados a enviar a EFD-ICMS/IPI, por força das Instruções Normativas RFB 1371/13 e 1685/17), até a definição de legislação específica quanto à obrigatoriedade da EFD
