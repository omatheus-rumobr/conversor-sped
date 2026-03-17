# Bloco 9 - Versão 1.35

BLOCO 9: Controle e Encerramento do Arquivo Digital
Este bloco representa os totais de registros e serve como forma de controle para batimentos e verificações.
<!-- Start Registro 9001 -->
Registro 9001: Abertura do Bloco 9
Este registro deve sempre ser gerado e representa a abertura do Bloco 9.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “9001”. | C | 004* | - | S |
| 02 | IND_MOV | Indicador de movimento: 0- Bloco com dados informados; 1- Bloco sem dados informados. | N | 001* | - | S |

Observações: Registro obrigatório
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Campo 01 - Valor Válido: [9001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro 9001 -->
<!-- Start Registro 9900 -->
Registro 9900: Registros do Arquivo
Todos os registros referenciados neste arquivo, inclusive os posteriores a este registro, devem ter uma linha totalizadora do seu número de ocorrências.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “9900”. | C | 004* | - | S |
| 02 | REG_BLC | Registro que será totalizado no próximo campo. | C | 004 | - | S |
| 03 | QTD_REG_BLC | Total de registros do tipo informado no campo anterior. | N | - | - | S |

Observações: Registro obrigatório
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Campo 01 - Valor Válido: [9900]
Campo 02 - Preenchimento: informar cada um dos códigos de registros válidos deste arquivo, que será totalizado no próximo campo QTD_REG_BLC.
Campo 03 - Validação: verifica se o número de linhas no arquivo do tipo informado no campo REG_BLC do registro 9900 é igual ao valor informado neste campo.
<!-- End Registro 9900 -->
<!-- Start Registro 9990 -->
Registro 9990: Encerramento do Bloco 9
Este registro destina-se a identificar o encerramento do Bloco 9 e a informar a quantidade de linhas (registros) existentes no bloco.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “9990”. | C | 004* | - | S |
| 02 | QTD_LIN_9 | Quantidade total de linhas do Bloco 9. | N | - | - | S |

Observações: Registro obrigatório
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Campo 01 - Valor Válido: [9990]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco. Para este cálculo, o registro 9999, apesar de não pertencer ao Bloco 9, também deve ser contabilizado nesta soma.
Validação: o número de linhas (registros) existentes no bloco 9 é igual ao valor informado no campo QTD_LIN_9.
<!-- End Registro 9990 -->
<!-- Start Registro 9999 -->
Registro 9999: Encerramento do Arquivo Digital
Este registro destina-se a identificar o encerramento do arquivo digital da escrituração do PIS/Pasep, da Cofins e da Contribuição Previdenciária sobre a receita bruta, conforme o caso, bem como a informar a quantidade de linhas (registros) existentes no arquivo.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “9999”. | C | 004* | - | S |
| 02 | QTD_LIN | Quantidade total de linhas do arquivo digital. | N | - | - | S |

Observações: Registro obrigatório
Nível hierárquico - 0
Ocorrência - um (por arquivo)
Campo 01 - Valor Válido: [9999]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também a linha correspondente ao próprio registro 9999.
Validação: o número de linhas (registros) existentes no arquivo inteiro é igual ao valor informado no campo QTD_LIN.
<!-- End Registro 9999 -->