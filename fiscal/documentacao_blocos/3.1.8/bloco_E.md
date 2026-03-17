# Bloco E - Versão 3.1.8


BLOCO E: APURAÇÃO DO ICMS E DO IPI
Bloco de registros dos dados relativos à apuração do ICMS e do IPI.
REGISTRO E001: ABERTURA DO BLOCO E
Este registro tem por objetivo abrir o Bloco E e indica se há informações sobre apuração do ICMS e do IPI.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E001" C 004 - O
02 IND_MOV Indicador de movimento: C 001 - O
0- Bloco com dados informados;
1- Bloco sem dados informados
Observações:
Nível hierárquico - 1
Ocorrência – um por Arquivo
Campo 01 (REG) - Valor Válido: [E001]
Campo 02 (IND_MOV) - Valor Válido: [0]
Validação: além dos registros de abertura e encerramento, sempre devem ser informados os registros E100 (Período da
Apuração do ICMS) e E110 (Apuração do ICMS – Operações Próprias). Se campo 15 – IND_ATIV do registro 0000 – Abertura
do Arquivo Digital e Identificação da Entidade for igual a 0 – Industrial ou equiparado a industrial - deverão ser informados os
registros E500 (Período de Apuração do IPI) e seus filhos.
----
REGISTRO E100: PERÍODO DA APURAÇÃO DO ICMS
Este registro tem por objetivo informar o(s) período(s) de apuração do ICMS. Os períodos informados devem abranger
todo o intervalo da escrituração fiscal, sem sobreposição ou omissão de datas ou períodos.
Validação do Registro: Não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos 02 (DT_INI), 03 (DT_FIN). Não devem existir lacunas ou sobreposições de datas nos períodos de apuração
informados nestes registros, em comparação com as datas informadas no registro 0000.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E100" C 004 - O
02 DT_INI Data inicial a que a apuração se refere N 008* - O
03 DT_FIN Data final a que a apuração se refere N 008* - O
Observações:
Nível hierárquico – 2
Ocorrência – 1:N
Campo 01 (REG) - Valores válidos: [E100]
Campo 02 (DT_INI) - Preenchimento: informar a data inicial a que se refere a apuração, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000 e maior ou igual
ao valor no campo DT_INI do registro 0000. A data informada no campo deve ser menor ou igual à data informada no campo
DT_FIN do registro E100.
Campo 03 (DT_FIN) - Preenchimento: informar a data final a que se refere a apuração no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000 e maior ou igual
ao valor no campo DT_INI do registro 0000.
----
REGISTRO E110: APURAÇÃO DO ICMS – OPERAÇÕES PRÓPRIAS
Este registro tem por objetivo informar os valores relativos à apuração do ICMS referentes às operações próprias. O
registro deve ser apresentado inclusive nos casos de períodos sem movimento. Neste caso, os valores deverão ser apresentados
zerados.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E110" C 004 - O
02 VL_TOT_DEBITOS Valor total dos débitos por "Saídas e prestações com N - 02 O
débito do imposto"
03 VL_AJ_DEBITOS Valor total dos ajustes a débito decorrentes do documento N - 02 O
fiscal.
04 VL_TOT_AJ_DEBITOS Valor total de "Ajustes a débito" N - 02 O
05 VL_ESTORNOS_CRED Valor total de Ajustes “Estornos de créditos” N - 02 O
06 VL_TOT_CREDITOS Valor total dos créditos por "Entradas e aquisições com N - 02 O
crédito do imposto"
07 VL_AJ_CREDITOS Valor total dos ajustes a crédito decorrentes do N - 02 O
documento fiscal.
08 VL_TOT_AJ_CREDITOS Valor total de "Ajustes a crédito" N - 02 O
09 VL_ESTORNOS_DEB Valor total de Ajustes “Estornos de Débitos” N - 02 O
10 VL_SLD_CREDOR_ANT Valor total de "Saldo credor do período anterior" N - 02 O
11 VL_SLD_APURADO Valor do saldo devedor apurado N - 02 O
12 VL_TOT_DED Valor total de "Deduções" N - 02 O
13 VL_ICMS_RECOLHER Valor total de "ICMS a recolher (11-12) N - 02 O
14 VL_SLD_CREDOR_TRA Valor total de "Saldo credor a transportar para o período N - 02 O
NSPORTAR seguinte”
15 DEB_ESP Valores recolhidos ou a recolher, extra-apuração. N - 02 O
Observações:
Nível hierárquico – 3 – registro obrigatório
Ocorrência – um por período
Campo 01 (REG) - Valor Válido: [E110]
Campo 02 (VL_TOT_DEBITOS) - Validação: o valor informado deve corresponder ao somatório de todos os documentos
fiscais de saída que geram débito de ICMS. Deste somatório, estão excluídos os documentos extemporâneos (COD_SIT com
valor igual ‘01’), os documentos complementares extemporâneos (COD_SIT com valor igual ‘07’) e os documentos fiscais
com CFOP 5605 – Transferência de saldo devedor de ICMS de outro estabelecimento da mesma empresa. Devem ser incluídos
os documentos fiscais com CFOP igual a 1605 - Recebimento, por transferência, de saldo devedor do ICMS de outro
estabelecimento da mesma empresa.
O valor neste campo deve ser igual à soma dos VL_ICMS de todos os registros C190, C320, C390, C490, C590, C690, C790,
C850, C890, D190, D300, D390, D410, D590, D690, D696, D730, D760, com as datas dos campos DT_DOC (C300, C405,
C600, C800, C860, D300, D355, D400, D600, D700, D750) ou DT_E_S (C100, C500, D700) ou DT_DOC_FIN (C700, D695)
ou DT_A_P (D100, D500) dentro do período informado no registro E100.
Quando o campo DT_E_S ou DT_A_P não for informado, utilizar o campo DT_DOC.
Para os estados que utilizam como data da escrituração a data de emissão, todos os documentos devem ser declarados na
competência da emissão. Neste caso, se a data de saída (DT_E_S ou DT_A_P) for posterior à data final informada no campo
03 do registro E100, o campo referente à data de saída não deve ser preenchido.
Para os estados que utilizam como data da escrituração a data de efetiva saída, todos os documentos devem ser declarados na
competência específica da data de saída como documento regular (COD_SIT igual a ‘00’), obedecendo à legislação estadual
pertinente.
Campo 03 (VL_AJ_DEBITOS) - Validação: o valor informado deve corresponder ao somatório do campo VL_ICMS dos
registros C197, C597, C857, C897, D197 e D737 se o terceiro caractere do campo COD_AJ dos registros C197, C597, C857,
C897, D197 ou D737 for igual a ‘3’, ‘4’ ou ‘5’ e o quarto caractere for igual a “0”, “3”, “4”, “5”, “6”, “7” ou “8”. Deste
somatório, estão excluídos os documentos extemporâneos (COD_SIT com valor igual ‘01’) e os documentos complementares
extemporâneos (COD_SIT com valor igual ‘07’), cujos valores devem ser prestados no campo DEB_ESP acompanhado dos
demais valores extra-apuração.
Serão considerados os registros cujos documentos estejam compreendidos no período informado no registro E100, utilizando
para tanto o campo DT_E_S (C100, C500 ou D700) e DT_DOC ou DT_A_P (D100). Quando o campo DT_E_S (C100, C500
ou D700) for vazio, utilizar o campo DT_DOC.
Campo 04 (VL_TOT_AJ_DEBITOS) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR dos registros E111, se o terceiro caractere for igual a ‘0’ e o quarto caractere do campo COD_AJ_APUR do
registro E111 for igual a ‘0’.
Campo 05 (VL_ESTORNOS_CRED) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR dos registros E111, se o terceiro caractere for igual a ‘0’ e o quarto caractere do campo COD_AJ_APUR do
registro E111 for igual a ‘1’.
Campo 06 (VL_TOT_CREDITOS) - Validação: o valor informado deve corresponder ao somatório de todos os documentos
fiscais de entrada que geram crédito de ICMS. O valor neste campo deve ser igual à soma dos VL_ICMS de todos os registros
C190, C590, D190, D590, D730. Deste somatório, estão excluídos os documentos fiscais com CFOP 1605 - Recebimento, por
transferência, de saldo devedor do ICMS de outro estabelecimento da mesma empresa e incluídos os documentos fiscais com
CFOP 5605 – Transferência de saldo devedor de ICMS de outro estabelecimento da mesma empresa. Os documentos fiscais
devem ser somados conforme o período informado no registro E100 e a data informada no campo DT_E_S (C100, C500, D700)
ou campo DT_A_P (D100, D500), exceto se COD_SIT do documento for igual a “01” (extemporâneo) ou igual a 07 (NF
Complementar extemporânea), cujo valor será somado no primeiro período de apuração informado no registro E100.
Quando o campo DT_E_S ou DT_A_P não for informado, é utilizada a data constante no campo DT_DOC.
Campo 07 (VL_AJ_CREDITOS) - Validação: o valor informado deve corresponder ao somatório do campo VL_ICMS dos
registros C197, C597, C857, C897, D197 e D737, se o terceiro caractere do código de ajuste dos registros C197, C597, C857,
C897, D197 ou D737 for ‘0’, ‘1’ ou ‘2’ e o quarto caractere for ‘0’, “3”, “4”, “5”, “6”, “7” ou “8”. Devem ser considerados os
documentos fiscais compreendidos no período informado no registro E100, analisando-se as datas informadas no campo
DT_E_S do registro C100, C500 ou D700 e DT_DOC ou DT_A_P do registro D100, exceto se COD_SIT do registro C100 ou
C500 e D100 for igual a ‘01’ (extemporâneo) ou igual a ‘07’ (Complementar extemporânea), cujo valor deve ser somado no
primeiro período de apuração informado no registro E100.
Campo 08 (VL_TOT_AJ_CREDITOS) - Validação: o valor informado deve corresponder ao somatório dos valores constantes
dos registros E111, quando o terceiro caractere for igual a ‘0’ e o quarto caractere for igual a ‘2’, do COD_AJ_APUR do
registro E111.
Campo 09 (VL_ESTORNOS_DEB) - Validação: o valor informado deve corresponder ao somatório do VL_AJ_APUR dos
registros E111, quando o terceiro caractere for igual a ‘0’ e o quarto caractere for igual a ‘3’, do COD_AJ_APUR do registro
E111.
Campo 11 (VL_SLD_APURADO) - Validação: o valor informado deve ser preenchido com base na expressão: soma do total
de débitos (VL_TOT_DEBITOS) com total de ajustes (VL_AJ_DEBITOS +VL_TOT_AJ_DEBITOS) com total de estorno de
crédito (VL_ESTORNOS_CRED) menos a soma do total de créditos (VL_TOT_CREDITOS) com total de ajuste de créditos
(VL_AJ_CREDITOS + VL_TOT_AJ_CREDITOS) com total de estorno de débito (VL_ESTORNOS_DEB) com saldo credor
do período anterior (VL_SLD_CREDOR_ANT). Se o valor da expressão for maior ou igual a “0” (zero), então este valor deve
ser informado neste campo e o campo 14 (VL_SLD_CREDOR_TRANSPORTAR) deve ser igual a “0” (zero). Se o valor da
expressão for menor que “0” (zero), então este campo deve ser preenchido com “0” (zero) e o valor absoluto da expressão deve
ser informado no campo VL_SLD_CREDOR_TRANSPORTAR, adicionado ao valor total das deduções (VL_TOT_DED)
Campo 12 (VL_TOT_DED) - Validação: o valor informado deve corresponder ao somatório do campo VL_ICMS dos
registros C197, C597, C857, C897, D197 e D737, se o terceiro caractere do código de ajuste do registro C197, C597, C857,
C897, D197 ou D737, for ‘6’ e o quarto caractere for ‘0’, somado ao valor total informado nos registros E111, quando o
terceiro caractere for igual a ‘0’ e o quarto caractere for igual a ‘4’, do campo COD_AJ_APUR do registro E111.
Para o somatório do campo VL_ICMS dos registros C197, C597, C857, C897, D197 e D737 devem ser considerados os
documentos fiscais compreendidos no período informado no registro E100, comparando com a data informada no campo
DT_DOC do registro C800 ou C860, DT_E_S do registro C100, C500 ou D700 e DT_DOC ou DT_A_P do registro D100,
exceto se COD_SIT do registro C100 ou C500 for igual a ‘01’ (extemporâneo) ou igual a ‘07’ (Complementar extemporânea),
cujo valor deve ser somado no primeiro período de apuração informado no registro E100, quando houver mais de um período
de apuração. Quando o campo DT_E_S não for informado, utilizar o campo DT_DOC.
Neste campo são informados os valores que, segundo a legislação da UF, devam ser tratados como “Dedução do imposto”,
ainda que no campo VL_SLD_APURADO tenha como resultado o valor zero.
Campo 13 (VL_ICMS_RECOLHER) – Validação: o valor informado deve corresponder à diferença entre o campo
VL_SLD_APURADO e o campo VL_TOT_DED. Se o resultado dessa operação for negativo, informe o valor zero neste
campo, e o valor absoluto correspondente no campo VL_SLD_CREDOR_TRANSPORTAR. Verificar se a legislação da UF
permite que dedução seja maior que o saldo devedor.
O valor da soma deste campo com o campo DEB_ESP deve ser igual à soma dos valores do campo VL_OR do registro E116.
Campo 14 (VL_SLD_CREDOR_TRANSPORTAR) – Validação: se o valor da expressão: soma do total de débitos
(VL_TOT_DEBITOS) com total de ajustes (VL_AJ_DEBITOS + VL_TOT_AJ_DEBITOS) com total de estorno de crédito
(VL_ESTORNOS_CRED) menos a soma do total de créditos (VL_TOT_CREDITOS) com total de ajuste de créditos
(VL_AJ_CREDITOS + VL_TOT_AJ_CREDITOS) com total de estorno de débito (VL_ESTORNOS_DEB) com saldo credor
do período anterior (VL_SLD_CREDOR_ANT) com total de deduções (VL_TOT_DED) for maior que “0” (zero), este campo
deve ser preenchido com “0” (zero). Se for menor que “0” (zero), o valor absoluto do resultado deve ser informado neste campo.
Campo 15 (DEB_ESP) – Preenchimento: Informar o correspondente ao somatório dos valores:
a) de ICMS correspondentes aos documentos fiscais extemporâneos (COD_SIT igual a “01”) e dos documentos fiscais
complementares extemporâneos (COD_SIT igual a “07”). No PVA, estes valores podem ser verificados no resumo do
Relatório dos Registros Fiscais de Documentos de Saídas (totalização por CST_ICMS e CFOP), constante das últimas
páginas.
b) de ajustes do campo VL_ICMS dos registros C197, C597, C857, C897, D197 e D737, se o terceiro caractere do código
informado no campo COD_AJ do registro C197, C597, C857, C897, D197 e D737 for igual a “7” (débitos especiais)
e o quarto caractere for igual a “0” (operações próprias) referente aos documentos compreendidos no período a que se
refere a escrituração. No PVA, estes valores podem ser verificados nos resumos dos Relatórios dos Registros Fiscais
de Documentos de Saídas e de Entradas (totalização dos ajustes constante das últimas páginas); e
c) de ajustes do campo VL_AJ_APUR do registro E111, se o terceiro caractere do código informado no campo
COD_AJ_APUR do registro E111 for igual a “0” (apuração ICMS próprio) e o quarto caractere for igual a “5”(débito
especial). No PVA, estes valores podem ser verificados nos demonstrativos dos ajustes ao final do Relatório de
Registros Fiscais da Apuração do ICMS – Registro E111 - códigos específicos para débitos especiais. Validação: O
valor da soma deste campo com o campo VL_ICMS_RECOLHER deve ser igual à soma dos valores do campo
VL_OR do registro E116.
----
REGISTRO E111: AJUSTE/BENEFÍCIO/INCENTIVO DA APURAÇÃO DO ICMS
Este registro tem por objetivo discriminar todos os ajustes lançados nos campos VL_TOT_AJ_DEBITOS,
VL_ESTORNOS_CRED, VL_TOT_AJ_CREDITOS, VL_ESTORNOS_DEB, VL_TOT_DED e DEB_ESP, todos do registro E110.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E111" C 004 - O
02 COD_AJ_APUR Código do ajuste da apuração e dedução, conforme a Tabela C 008* - O
indicada no item 5.1.1.
03 DESCR_COMPL_AJ Descrição complementar do ajuste da apuração C - - OC
04 VL_AJ_APUR Valor do ajuste da apuração N - 02 O
Observações:
Nível hierárquico – 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E111]
Campo 02 (COD_AJ_APUR) - Preenchimento: o valor informado no campo deve existir na tabela de código do ajuste da
apuração e dedução de cada Secretaria de Fazenda, conforme a UF do declarante, campo UF do registro 0000 ou, não havendo
esta tabela, o valor informado no campo deve existir na tabela de código do ajuste da apuração e dedução, constante da
observação do Item 5.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
O código do ajuste utilizado deve ter seu terceiro caractere como “0” (zero), indicando ajuste de ICMS, não incluindo ajustes
de ICMS ST.
O quarto caractere deve ser preenchido, conforme item 5.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018
e alterações, com um dos códigos abaixo:
0 – Outros débitos;
1 – Estorno de créditos;
2 – Outros créditos;
3 – Estorno de débitos;
4 – Deduções do imposto apurado;
5 – Débitos Especiais.
Obs.: Na existência de mais de um tipo de crédito que se enquadre no mesmo código de ajuste, deverão ser apresentados tantos
registros E111 quantos forem os tipos de créditos.
Campo 03 (DESCR_COMPL_AJ) - Preenchimento: Sem prejuízo de outras situações definidas em legislação específica, o
contribuinte deverá fazer a descrição complementar de ajustes (tabela 5.1.1) sempre que informar códigos genéricos.
----
REGISTRO E112: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA APURAÇÃO DO ICMS
Este registro tem por objetivo detalhar os ajustes do registro E111 quando forem relacionados a processos judiciais ou
fiscais ou a documentos de arrecadação, observada a legislação estadual pertinente. Os valores recolhidos, com influência na
apuração do ICMS – Operações Próprias, devem ser detalhados neste registro, com identificação do documento de arrecadação
específico.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E112" C 004 - O
02 NUM_DA Número do documento de arrecadação estadual, se houver C - - OC
03 NUM_PROC Número do processo ao qual o ajuste está vinculado, se houver C 060 - OC
04 IND_PROC Indicador da origem do processo: C 001* - OC
0- Sefaz;
1- Justiça Federal;
2- Justiça Estadual;
9- Outros
05 PROC Descrição resumida do processo que embasou o lançamento C - - OC
06 TXT_COMPL Descrição complementar C - - OC
Observações:
Nível hierárquico – 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E112]
Campo 02 (NUM_DA) - Preenchimento: este campo deve ser preenchido se o ajuste for referente a um documento de
arrecadação, tais como pagamentos indevidos, pagamentos antecipados e outros.
Campo 03(NUM_PROC) - Preenchimento: o valor deve ter até 60 caracteres.
Campo 04 (IND_PROC) - Valores válidos: [0, 1, 2, 9]
Campo 06 (TXT_COMPL) - Preenchimento: Outras informações complementares.
----
REGISTRO E113: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA APURAÇÃO DO ICMS –
IDENTIFICAÇÃO DOS DOCUMENTOS FISCAIS
Este registro tem por objetivo identificar os documentos fiscais relacionados ao ajuste.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E113" C 004 - O
02 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - OC
- do emitente do documento ou do remetente das mercadorias, no
caso de entradas;
- do adquirente, no caso de saídas
03 COD_MOD Código do modelo do documento fiscal, conforme a Tabela 4.1.1 C 002* - O
04 SER Série do documento fiscal C 004 - OC
05 SUB Subsérie do documento fiscal N 003 - OC
06 NUM_DOC Número do documento fiscal N 009 - O
07 DT_DOC Data da emissão do documento fiscal N 008* - O
08 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC
09 VL_AJ_ITEM Valor do ajuste para a operação/item N - 02 O
10 CHV_DOCe Chave do Documento Eletrônico N 044* - OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E113]
Campo 02 (COD_PART) - Preenchimento: no caso de entrada, deve constar a informação referente ao emitente do documento
ou ao remetente das mercadorias ou serviços. No caso de saída, deve constar a informação referente ao destinatário.
Validação: quando o modelo de documento for igual a 59 (CF-e SAT), 63 (BP-e) ou 65 (NFC-e), deve ser apresentado conteúdo
VAZIO “||”. Quando o modelo de documento for igual a 06 (NF/CEE) ou 66 (NF3e), o seu preenchimento é facultativo. Campo
de preenchimento obrigatório para os demais modelos de documento
. O valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 (COD_MOD) - Validação: o valor informado no campo deve existir na tabela de Documentos Fiscais do ICMS,
conforme Item 4.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações. Ver tabela reproduzida na
subseção 1.4 deste guia.
Campo 06 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (DT_DOC) - Preenchimento: informar a data de emissão do documento fiscal, no formato “ddmmaaaa”, sem os
separadores de formatação.
Campo 08 (COD_ITEM) – Preenchimento: este campo só deve ser informado quando o ajuste se referir a um determinado
item/produto do documento.
Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
Campo 10 (CHV_DOCe) - Preenchimento: informar a chave da NF-e, para documentos de COD_MOD igual a “55”. A partir
de janeiro/2013, informar a chave da NFC-e, para documentos de COD_MOD igual a “65” ou informar a chave do CF-e-SAT,
para documentos de COD_MOD igual a “59”. A partir de janeiro/2017, informar a chave do conhecimento de transporte
eletrônico, para documentos de COD_MOD igual a “57”. A partir de abril/2017, informar a chave do CT-e OS, para
documentos de COD_MOD igual a 67. A partir de janeiro/2018, informar a chave do BP-e, para documentos de COD_MOD
igual a 63. A partir de janeiro/2020, informar a chave da NF3-e, para documentos de COD_MOD igual a “66”. A partir de
janeiro/2023, informar a chave da NFCom, para documentos de COD_MOD igual a 62.
Validação: quando se tratar de NF-e, NFC-e, CT-e, CT-e OS, BP-e, CF-e-SAT, NFCom ou NF3-e, é conferido o dígito
verificador (DV) da chave do documento eletrônico. Será verificada a consistência da informação dos campos NUM_DOC e
SER com o número do documento e série contidos na chave do documento eletrônico.
----
REGISTRO E115: INFORMAÇÕES ADICIONAIS DA APURAÇÃO – VALORES
DECLARATÓRIOS
Este registro tem o objetivo de informar os valores declaratórios relativos ao ICMS, conforme definição da legislação
estadual pertinente. Esses valores são meramente declaratórios e não são computados na apuração do ICMS.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E115" C 004 - O
02 COD_INF_ADIC Código da informação adicional conforme tabela a ser C 008* - O
definida pelas SEFAZ, conforme tabela definida no item 5.2.
03 VL_INF_ADIC Valor referente à informação adicional N - 02 O
04 DESCR_COMPL_AJ Descrição complementar do ajuste C - - OC
Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E115]
Campo 02 (COD_INF_ADIC) - Preenchimento: o código da informação adicional deve obedecer à tabela definida pelas
Secretarias de Fazenda dos Estados. Caso não haja publicação da referida tabela, o registro não deve ser apresentado.
----
REGISTRO E116: OBRIGAÇÕES DO ICMS RECOLHIDO OU A RECOLHER – OPERAÇÕES
PRÓPRIAS
Este registro tem o objetivo de discriminar os pagamentos realizados ou a realizar, referentes à apuração do ICMS –
Operações Próprias do período. A soma do valor das obrigações deste registro deve ser igual à soma dos campos
VL_ICMS_RECOLHER e DEB_ESP, do registro E110.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E116" C 004 - O
02 COD_OR Código da obrigação a recolher, conforme a Tabela 5.4 C 003* - O
03 VL_OR Valor da obrigação a recolher N - 02 O
04 DT_VCTO Data de vencimento da obrigação N 008* - O
05 COD_REC Código de receita referente à obrigação, próprio da unidade da C - - O
federação, conforme legislação estadual.
06 NUM_PROC Número do processo ou auto de infração ao qual a obrigação está C 060 - OC
vinculada, se houver.
07 IND_PROC Indicador da origem do processo: C 001* - OC
0- SEFAZ;
1- Justiça Federal;
2- Justiça Estadual;
9- Outros
08 PROC Descrição resumida do processo que embasou o lançamento C - - OC
09 TXT_COMPL Descrição complementar das obrigações a recolher. C - - OC
10 MES_REF* Informe o mês de referência no formato “mmaaaa” N 006* - O
Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E116]
Campo 02 (COD_OR) - Valores Válidos: [000, 003, 004, 005, 006, 090]
Campo 03 (VL_OR) – Preenchimento: o valor da soma deste campo deve corresponder à soma dos campos
VL_ICMS_RECOLHER e DEB_ESP do registro E110. Não informar acréscimos legais, se houver.
Campo 04 (DT_VCTO) - Preenchimento: informar a data de vencimento da obrigação, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: o valor informado no campo deve ser uma data válida.
Campo 06 (NUM_PROC) - Preenchimento: o valor deve ter até 60 caracteres.
Validação: se este campo estiver preenchido, os campos IND_PROC e PROC também devem estar preenchidos.
Campo 07 (IND_PROC) - Valores Válidos: [0, 1, 2, 9]
Campo 09 (TXT_COMPL) - Preenchimento: além de outras informações, para os arquivos com período de apuração (registro
0000) até dezembro/2010, quando este registro se referir a recolhimento extemporâneo, informar neste campo o mês e ano de
referência de cada um dos débitos extemporâneos do período, no formato mmaaaa, sem utilizar os caracteres especiais de
separação Exemplo: para débito extemporâneo do mês de abril de 2009 o campo deve ser preenchido, simplesmente, com os
caracteres 042009.
Campo 10 (MES_REF) – Preenchimento: para os arquivos com período de apuração (registro 0000) a partir de janeiro de
2011, informar neste campo o mês e ano de referência de cada um dos débitos do período, no formato mmaaaa, sem utilizar os
caracteres especiais de separação.
* O campo 10 – MES_REF somente deverá ser incluído no leiaute a partir de períodos de apuração de janeiro de 2011
Validação: O campo MES_REF* não pode ser superior à competência do campo DT_INI do registro 0000
----
REGISTRO E200: PERÍODO DA APURAÇÃO DO ICMS - SUBSTITUIÇÃO TRIBUTÁRIA
Este registro tem por objetivo informar o(s) período(s) de apuração do ICMS – Substituição Tributária para cada UF
onde o informante seja inscrito como substituto tributário, inclusive para o seu estado, nas operações internas que envolvam
substituição, e também para UF para a qual o declarante tenha comercializado e que não tenha inscrição como substituto. Os
períodos informados devem abranger todo o período previsto no registro 0000, sem haver sobreposição ou omissão de datas,
por UF.
Este registro também deve ser informado pelo substituído, se este for o responsável pelo recolhimento do imposto
devido nas operações subsequentes, quando recebe mercadoria de outra unidade da federação, sujeita ao regime de substituição
tributária, na hipótese de o remetente não estar obrigado à retenção do imposto.
Validação do Registro: o registro é obrigatório se a soma, por UF, dos valores do campo VL_ICMS_ST dos registros
C190, C590, C597, C690, C791, for maior que “0” (zero), ou se existir registro 0015 (substituto tributário) para a UF, ou se
existir algum registro C197 ou D197, onde o quarto caractere do código de ajuste (campo COD_AJ) for igual "1".Não pode
haver mais de um registro com a mesma combinação de valores para os campos UF, DT_INI e DT_FIN, nem sobreposição ou
omissão de períodos para a combinação.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E200" C 004 - O
02 UF Sigla da unidade da federação a que se refere a apuração do ICMS ST C 002* - O
03 DT_INI Data inicial a que a apuração se refere N 008* - O
04 DT_FIN Data final a que a apuração se refere N 008* - O
Observações:
Nível hierárquico - 2
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E200]
Campo 02 (UF) - Validação o valor informado no campo deve existir na tabela de UF.
Campo 03 (DT_INI) - Preenchimento: informar a data inicial a que a apuração se refere, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: verifica se a data informada é maior ou igual ao valor no campo DT_INI do registro 0000 e menor ou igual ao valor
no campo DT_FIN do registro 0000. A data informada no campo deve ser menor ou igual ao valor do campo DT_FIN deste
registro.
Campo 04 (DT_FIN) - Preenchimento: informar a data final a que a apuração se refere, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: verifica se a data informada é maior ou igual ao valor no campo DT_INI do registro 0000 e menor ou igual ao valor
no campo DT_FIN do registro 0000.
----
REGISTRO E210: APURAÇÃO DO ICMS – SUBSTITUIÇÃO TRIBUTÁRIA
Este registro tem por objetivo informar valores relativos à apuração do ICMS de substituição tributária, mesmo nos
casos de períodos sem movimento.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E210" C 004 - O
02 IND_MOV_ST Indicador de movimento: C 001 - O
0 – Sem operações com ST
1 – Com operações de ST
03 VL_SLD_CRED_ANT_ST Valor do "Saldo credor de período anterior – N - 02 O
Substituição Tributária"
04 VL_DEVOL_ST Valor total do ICMS ST de devolução de mercadorias N - 02 O
05 VL_RESSARC_ST Valor total do ICMS ST de ressarcimentos N - 02 O
06 VL_OUT_CRED_ST Valor total de Ajustes "Outros créditos ST" e N - 02 O
“Estorno de débitos ST”
07 VL_AJ_CREDITOS_ST Valor total dos ajustes a crédito de ICMS ST, N - 02 O
provenientes de ajustes do documento fiscal.
08 VL_RETENÇAO_ST Valor Total do ICMS retido por Substituição N - 02 O
Tributária
09 VL_OUT_DEB_ST Valor Total dos ajustes "Outros débitos ST" " e N - 02 O
“Estorno de créditos ST”
10 VL_AJ_DEBITOS_ST Valor total dos ajustes a débito de ICMS ST, N - 02 O
provenientes de ajustes do documento fiscal.
11 VL_SLD_DEV_ANT_ST Valor total de Saldo devedor antes das deduções N - 02 O
12 VL_DEDUÇÕES_ST Valor total dos ajustes "Deduções ST" N - 02 O
13 VL_ICMS_RECOL_ST Imposto a recolher ST (11-12) N - 02 O
14 VL_SLD_CRED_ST_TRANS Saldo credor de ST a transportar para o período N - 02 O
PORTAR seguinte [(03+04+05+06+07+12) – (08+09+10)].
15 DEB_ESP_ST Valores recolhidos ou a recolher, extra-apuração. N - 02 O
Observações:
Nível hierárquico - 3
Ocorrência – um por período
Campo 01 (REG) - Valor Válido: [E210]
Campo 02 (IND_MOV_ST) - Valores Válidos: [0, 1]
Campo 04 (VL_DEVOL_ST) - Validação: o valor informado deve corresponder à soma do campo VL_ICMS_ST do registro
C190, quando o valor do campo CFOP for igual a 1410, 1411, 1414, 1415, 1660, 1661, 1662, 2410, 2411, 2414, 2415, 2660,
2661 ou 2662 e para documentos com data (campo DT_E_S ou DT_DOC do registro C100) compreendida no período de
apuração do registro E200. Só será considerada a data do campo DT_DOC, quando o campo DT_E_S estiver em branco.
Obs.: O preenchimento deste campo deverá estar de acordo com o disposto na legislação tributária da unidade federada do
contribuinte substituído.
Campo 05 (VL_RESSARC_ST) – Preenchimento: só deve ser informado valor neste campo se o ressarcimento tiver origem
em documento fiscal.
Validação: o valor informado deve corresponder à soma do campo VL_ICMS_ST do registro C190, quando o valor do campo
CFOP for igual a 1603 ou 2603 e para documentos com data, campo DT_E_S ou campo DT_DOC do registro C100,
compreendida no período de apuração do registro E200. Só será considerada a data do campo DT_DOC, quando o campo
DT_E_S estiver em branco.
Campo 06 (VL_OUT_CRED_ST) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ_APUR
dos registros E220 quando o terceiro caractere for igual a ‘1’ e o quarto caractere do campo COD_AJ_APUR for igual a ‘2’
ou ‘3’ mais a soma do campo VL_ICMS_ST do registro C190 (demais CFOPs), quando o primeiro caractere do campo CFOP
for ‘1’ ou ‘2’, exceto se o valor do campo CFOP for 1410, 1411, 1414, 1415, 1660, 1661, 1662, 2410, 2411, 2414, 2415, 2660,
2661 ou 2662. Para documentos com data (campo DT_E_S ou DT_DOC do Registro C100) compreendida no período de
apuração do Registro E200. Só será considerada a data do Campo DT_DOC, quando o Campo DT_E_S estiver em branco.
Campo 07 (VL_AJ_CREDITOS_ST) – Validação: o valor informado deve corresponder ao somatório do campo VL_ICMS
dos registros C197, C597, C857, C897, D197 e D737, por UF, se o terceiro caractere do código de ajuste no campo COD_AJ
dos registros C197, C597, C857, C897, D197 e D737 for “0”, “1” ou “2” e o quarto caractere for “1”(um) para todos os
registros onde os documentos estejam compreendidos no período informado no registro E200, considerando a UF, utilizando
para tanto o campo DT_E_S (C100, C500 ou D700), DT_DOC ou DT_A_P (D100) e DT_DOC (C800, C860). Quando o
campo DT_E_S (C100, C500 ou D700) não estiver preenchido, a data considerada é a informada no campo DT_DOC.
Para os documentos extemporâneos (campo COD_SIT, do registro C100, com valor igual ‘01’), assim como para os
documentos complementares extemporâneos (campo COD_SIT, do registro C100, com valor igual ‘07’), estes valores devem
ser informados no primeiro período no registro E200, para a UF.
Campo 08 (VL_RETENÇAO_ST) – Validação: o valor informado deve corresponder ao somatório do campo VL_ICMS_ST
de todos os registros C190, C590, C690, C791 e dos campos VL_ICMS_UF de todos os registros D590 e D690, por UF, se o
primeiro caractere do campo CFOP for igual a 5 ou 6, considerando o período, por UF. Para o registro C791, o CFOP a ser
considerado é o do registro “pai” C790. Nesta soma, devem constar apenas os documentos fiscais compreendidos no período
informado no registro E200, utilizando-se, para tanto, os campos DT_DOC (C600, D600) ou DT_E_S (C100, C500, D500) ou
DT_DOC_FIN (C700, D695).
Quando a data do campo DT_E_S não for informada, será utilizada a data do campo DT_DOC.
Será considerada a UF do COD_PART do registro C100 ou UF do informante do arquivo, se houver ajustes relacionados, assim
como a UF do COD_PART para o registro D500; UF do COD_PART do registro C500, e se não for informado, a UF do
COD_MUN_DEST; e UF do campo COD_MUN para os registros C600 e D600 e campo UF para o registro C791
Caso exista o registro C105, a UF do registro E200 deverá corresponder a COD_UF do registro C105.
Campo 09 (VL_OUT_DEB_ST) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ_APUR
do registro E220, quando o terceiro caractere for igual a ‘1’ e o quarto for igual a ‘0’ ou ‘1’, ambos do campo COD_AJ_APUR
do registro E220.
Campo 10 (VL_AJ_DEBITOS_ST) - Validação: o valor informado deve corresponder ao somatório do campo VL_ICMS dos
registros C197, C597, C857, C897, D197 e D737 por UF, se o terceiro caractere do código de ajuste (campo COD_AJ) dos
registros C197, C597, C857, C897, D197 e D737 for ‘3’, ‘4’ ou ‘5’ e o quarto caractere for ‘1’, para todos os registros onde
os documentos estejam compreendidos no período informado no registro E200, por UF, utilizando-se, para tanto, o campo
DT_E_S (C100, C500 ou D700), DT_DOC ou DT_A_P (D100) e DT_DOC (C800, C860)
Quando a data do campo DT_E_S (C100, C500 ou D700) não estiver preenchida, é utilizada a data do campo DT_DOC.
Devem ser excluídos os documentos extemporâneos (campo COD_SIT do registro C100 com valor igual ‘01’) e os documentos
complementares extemporâneos (campo COD_SIT do registro C100 com valor igual ‘07’), cujos valores devem ser informados
no campo DEB_ESP_ST junto com os demais valores extra-apuração.
Campo 11 (VL_SLD_DEV_ANT_ST) - Validação: o valor informado deve ser preenchido com base na expressão: soma do
total de retenção por ST, campo VL_RETENCAO_ST, com total de outros débitos por ST, campo VL_OUT_DEB_ST, com
total de ajustes de débito por ST, campo VL_AJ_DEBITOS_ST, menos a soma do saldo credor do período anterior por ST,
campo VL_SLD_CRED_ANT_ST, com total de devolução por ST, campo VL_DEVOL_ST, com total de ressarcimento por
ST, campo VL_RESSARC_ST, com o total de outros créditos por ST, campo VL_OUT_CRED_ST, com o total de ajustes de
crédito por ST, campo VL_AJ_CREDITOS_ST. Se o valor da expressão for maior ou igual a “0” (zero), então este valor deve
ser informado neste campo. Se o valor da expressão for menor que “0” (zero), então este campo deve ser preenchido com “0”
(zero).
Campo 12 (VL_DEDUÇÕES_ST) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ_APUR
do registro E220, por UF, quando o terceiro caractere for igual a ‘1’ e o quarto caractere do campo COD_AJ_APUR for igual
a ‘4’, mais a soma do campo VL_ICMS dos registros C197, C597, C857, C897, D197 e D737, se o terceiro caractere do campo
COD_AJ for ‘6’ e o quarto caractere for ‘1’, para todos os registros onde os documentos estejam compreendidos no período
informado no registro E200, por UF, utilizando-se, para tanto, o campo DT_E_S, do registro C100, C500 ou C700 e DT_DOC
ou DT_A_P do registro D100.Quando o campo DT_E_S do registro C100, C500 ou C700 não estiver preenchido, utilizar o
campo DT_DOC do mesmo registro.
Campo 13 (VL_ICMS_RECOL_ST) - Validação: o valor informado deve corresponder à diferença entre o campo
VL_SLD_DEV_ANT_ST e o campo VL_DEDUCOES_ST.
O valor da soma deste campo com o campo DEB_ESP_ST deve corresponder à soma dos valores do campo VL_OR do registro
E250.
Campo 14 (VL_SLD_CRED_ST_TRANSPORTAR) - Validação: se o valor da expressão: soma do total de retenção por ST,
campo VL_RETENCAO_ST, com total de outros débitos por ST, campo VL_OUT_DEB_ST, com total de ajustes de débito
por ST, campo VL_AJ_DEBITOS_ST, menos a soma do saldo credor do período anterior por ST, campo
VL_SLD_CRED_ANT_ST, com total de devolução por ST, campo VL_DEVOL_ST, com total de ressarcimento por ST,
campo VL_RESSARC_ST, com o total de outros créditos por ST, campo VL_OUT_CRED_ST, com o total de ajustes de
crédito por ST, campo VL_AJ_CREDITOS_ST, com o total dos ajustes de deduções ST, campo VL_DEDUÇÕES_ST, for
maior ou igual a “0” (zero), este campo deve ser preenchido com “0” (zero). Se for menor que “0” (zero), o valor absoluto do
resultado deve ser informado.
Campo 15 (DEB_ESP_ST) – Preenchimento: Informar por UF, valor correspondente ao somatório dos valores:
a) de ICMS_ST referente aos documentos fiscais extemporâneos (COD_SIT igual a “01”) e das notas fiscais
complementares extemporâneas (COD_SIT igual a “07”);
b) de ajustes do campo VL_ICMS dos registros C197, C597, C857, C897, D197 e D737, se o terceiro caractere do código
informado no campo COD_AJ dos registros C197, C597, C857, C897, D197 e D737 for igual a “7” (débitos especiais)
e o quarto caractere for igual a “1” (operações por ST) referente aos documentos compreendidos no período a que se
refere a escrituração; e
c) de ajustes do campo VL_AJ_APUR do registro E220, se o terceiro caractere do código informado no campo
COD_AJ_APUR do registro E220 for igual a “1” (ICMS- ST) e o quarto caractere for igual a “5”(débito especial).
Validação: O valor da soma do campo DEB_ESP_ST com o campo VL_ICMS_RECOL_ST deve corresponder à soma dos
valores do campo VL_OR do registro E250.
----
REGISTRO E220: AJUSTE/BENEFÍCIO/INCENTIVO DA APURAÇÃO DO ICMS
SUBSTITUIÇÃO TRIBUTÁRIA
Este registro deve ser apresentado para discriminar os ajustes lançados nos campos VL_OUT_CRED_ST,
VL_OUT_DEB_ST e VL_DEDUÇOES_ST e os valores informados no campo DEB_ESP_ST, todos do registro E210.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E220" C 004 - O
02 COD_AJ_APUR Código do ajuste da apuração e dedução, conforme a C 008* - O
Tabela indicada no item 5.1.1
03 DESCR_COMPL_AJ Descrição complementar do ajuste da apuração C - - OC
04 VL_AJ_APUR Valor do ajuste da apuração N - 02 O
Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E220]
Campo 02 (COD_AJ_APUR) - o valor informado no campo deve existir na tabela de código do ajuste da apuração e dedução
de cada Secretaria de Fazenda, conforme a UF do contribuinte substituído ou, não havendo esta tabela, o valor informado no
campo deve existir na tabela de código do ajuste da apuração e dedução constante na observação do Item 5.1.1. da Nota Técnica,
instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações (tabela genérica).
O código do ajuste utilizado deve ter seu terceiro caractere como um, indicando ajuste de ICMS ST.
O quarto caractere deve ser preenchido, conforme item 5.1.1da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018
e alterações, com um dos códigos abaixo:
0 – Outros débitos;
1 – Estorno de créditos;
2 – Outros créditos;
3 – Estorno de débitos;
4 – Deduções do imposto apurado;
5 – Débitos Especiais.
Campo 03 (DESCR_COMPL_AJ) - Preenchimento: Sem prejuízo de outras situações definidas em legislação específica, o
contribuinte deverá fazer a descrição complementar de ajustes (tabela 5.1.1) sempre que informar códigos genéricos.
Campo 04 (VL_AJ_APUR) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
REGISTRO E230: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA APURAÇÃO DO ICMS
SUBSTITUIÇÃO TRIBUTÁRIA
Este registro deve ser apresentado para detalhar os ajustes do registro E220 quando forem relacionados a processos
judiciais ou fiscais ou a documentos de arrecadação, observada a legislação estadual pertinente. Valores recolhidos, com
influência na apuração do ICMS ST, devem ser informados neste registro, com identificação do documento de arrecadação
específico.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E230" C 004 - O
02 NUM_DA Número do documento de arrecadação estadual, se houver C - - OC
03 NUM_PROC Número do processo ao qual o ajuste está vinculado, se houver C 060 - OC
04 IND_PROC Indicador da origem do processo: N 001* - OC
0 - Sefaz;
1 - Justiça Federal;
2 - Justiça Estadual;
9 – Outros
05 PROC Descrição resumida do processo que embasou o lançamento C - - OC
06 TXT_COMPL Descrição complementar C - - OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E230]
Campo 02 (NUM_DA) - Preenchimento: este campo deve ser preenchido se o ajuste for referente a um documento de
arrecadação conforme dispuser a legislação pertinente.
Campo 03 (NUM_PROC) - Preenchimento: o valor deve ter até 60 caracteres.
Campo 04 (IND_PROC) - Valores válidos: [0, 1, 2, 9]
Campo 06 (TXT_COMPL) - Preenchimento: Outras informações complementares.
----
REGISTRO E240: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA APURAÇÃO DO ICMS
SUBSTITUIÇÃO TRIBUTÁRIA – IDENTIFICAÇÃO DOS DOCUMENTOS FISCAIS
Este registro deve ser apresentado para identificação dos documentos fiscais relacionados ao ajuste.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E240" C 004 - O
02 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - O
- do emitente do documento ou do remetente das mercadorias,
no caso de entradas;
- do adquirente, no caso de saídas
03 COD_MOD Código do modelo do documento fiscal, conforme a Tabela C 002* - O
4.1.1
04 SER Série do documento fiscal C 004 - OC
05 SUB Subsérie do documento fiscal N 003 - OC
06 NUM_DOC Número do documento fiscal N 009 - O
07 DT_DOC Data da emissão do documento fiscal N 008* - O
08 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC
09 VL_AJ_ITEM Valor do ajuste para a operação/item N - 02 O
10 CHV_DOCe Chave do Documento Eletrônico N 044* - OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E240]
Campo 02 (COD_PART) - Preenchimento: no caso de entrada, deve constar a informação referente ao emitente do documento
ou do remetente das mercadorias. No caso de saída, deve constar a informação referente ao adquirente. O valor deve ter até 15
caracteres.
Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 (COD_MOD) - Validação: o valor informado no campo deve existir na tabela de Documentos Fiscais do ICMS,
conforme Item 4.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações. – Ver tabela reproduzida
na subseção 1.4 deste guia.
Campo 06 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (DT_DOC) - Preenchimento: informar a data de emissão do documento fiscal, no formato “ddmmaaaa”, sem os
separadores de formatação.
Campo 08 (COD_ITEM) – Preenchimento: este campo só deve ser informado quando o ajuste se referir a um determinado
item/produto do documento.
Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
Campo 10 (CHV_DOCe) - Preenchimento: informar a chave da NF-e, para documentos de COD_MOD igual a “55”. A partir
de janeiro/2013, informar a chave da NFC-e, para documentos de COD_MOD igual a “65” ou informar a chave do CF-e-SAT,
para documentos de COD_MOD igual a “59”. A partir de janeiro/2017, informar a chave do conhecimento de transporte
eletrônico, para documentos de COD_MOD igual a “57”. A partir de abril/2017, informar a chave do CT-e OS, para
documentos de COD_MOD igual a 67. A partir de janeiro/2018, informar a chave do BP-e, para documentos de COD_MOD
igual a 63. A partir de janeiro/2020, informar a chave da NF3-e, para documentos de COD_MOD igual a “66”. A partir de
janeiro/2023, informar a chave da NFCom, para documentos de COD_MOD igual a 62.
Validação: quando se tratar de NF-e, NFC-e, CT-e, CT-e OS, BP-e, CF-e-SAT, NFCom ou NF3-e, é conferido o dígito
verificador (DV) da chave do documento eletrônico. Será verificada a consistência da informação dos campos NUM_DOC e
SER com o número do documento e série contidos na chave do documento eletrônico.
----
REGISTRO E250: OBRIGAÇÕES DO ICMS RECOLHIDO OU A RECOLHER –
SUBSTITUIÇÃO TRIBUTÁRIA
Este registro deve ser apresentado para discriminar os pagamentos realizados ou a realizar, referentes à apuração do
ICMS devido por Substituição Tributária do período, por UF. A soma do valor das obrigações a serem discriminadas neste
registro deve ser igual ao campo VL_ICMS_RECOL_ST (registro E210) somado ao campo DEB_ESP_ST (registro E210).
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "E250" C 004 - O
02 COD_OR Código da obrigação a recolher, conforme a Tabela 5.4 C 003* - O
03 VL_OR Valor da obrigação ICMS ST a recolher N - 02 O
04 DT_VCTO Data de vencimento da obrigação N 008* - O
05 COD_REC Código de receita referente à obrigação, próprio da unidade da C - - O
federação do contribuinte substituído.
06 NUM_PROC Número do processo ou auto de infração ao qual a obrigação está C 060 - OC
vinculada, se houver
07 IND_PROC Indicador da origem do processo: C 001* - OC
0- SEFAZ;
1- Justiça Federal;
2- Justiça Estadual;
9- Outros
08 PROC Descrição resumida do processo que embasou o lançamento C - - OC
09 TXT_COMPL Descrição complementar das obrigações a recolher C - - OC
10 MES_REF* Informe o mês de referência no formato “mmaaaa” N 006* - O
Observações:* O campo 10 – MES_REF somente foi incluído no leiaute a partir de períodos de apuração de janeiro de 2011.
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E250]
Campo 02 (COD_OR) - Valores válidos: [001, 002, 006, 999]
Campo 03 (VL_OR) – Validação: o valor da soma deste campo deve corresponder à soma dos campos
VL_ICMS_RECOL_ST e DEB_ESP_ST do registro E210. Não informar acréscimos legais, se houver.
Campo 04 (DT_VCTO) - Preenchimento: informar a data de vencimento da obrigação, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: o valor informado no campo deve ser uma data válida.
Campo 05 (COD_REC) - Validação: Quando o campo 02 (UF) do registro E200 for igual ao campo 09 (UF) do registro 0000,
se existir tabela de códigos de receita da UF, o valor informado deve existir na referida tabela.
Campo 06 (NUM_PROC) - Validação: se este campo estiver preenchido, os campos IND_PROC e PROC deverão estar
preenchidos. Se este campo não estiver preenchido, os campos IND_PROC e PROC não deverão estar preenchidos. O valor
deve ter até 60 caracteres.
Campo 07 (IND_PROC) - Valores válidos: [0, 1, 2, 9]
Campo 09 (TXT_COMPL) - Preenchimento: além de outras informações, para os arquivos com período de apuração (registro
0000) até dezembro/2010, quando este registro se referir a recolhimento extemporâneo, informar neste campo o mês e ano de
referência de cada um dos débitos extemporâneos do período, no formato “mmaaaa”, sem utilizar os caracteres especiais de
separação Exemplo: para débito extemporâneo do mês de abril de 2009 o campo deve ser preenchido, simplesmente, com os
caracteres 042009.
Campo 10 (MES_REF) – Preenchimento: para os arquivos com período de apuração (registro 0000) a partir de janeiro de
2011, informar neste campo o mês e ano de referência de cada um dos débitos do período, no formato “mmaaaa”, sem utilizar
os caracteres especiais de separação.
Validação: O campo MES_REF* não pode ser superior à competência do campo DT_INI do registro 0000
----
REGISTRO E300: PERÍODO DE APURAÇÃO DO FUNDO DE COMBATE À POBREZA E DO
ICMS DIFERENCIAL DE ALÍQUOTA – UF ORIGEM/DESTINO EC 87/15
Este registro tem por objetivo informar o(s) período(s) de apuração do ICMS – Diferencial de Alíquota por UF
origem/destino, segundo o disposto na Emenda Constitucional 87/2015.
Validação do Registro: O registro é obrigatório se a soma, por UF, dos valores dos campos VL_ICMS_UF_DEST
dos registros C101 e D101 for maior que zero; ou VL_ICMS_UF_REM for maior que zero; ou VL_FCP_UF_DEST dos
registros C101 e D101 for maior que zero ou ainda se houver um registro 0015 para a UF.
A partir de janeiro de 2019, deixa de ser obrigatória a apresentação do registro E300 para a UF de origem.
Os períodos informados no registro E300 deverão abranger todo o período da escrituração, para cada UF informada,
não sendo permitidos intervalos.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E300" C 004 - O
02 UF Sigla da unidade da federação a que se refere à apuração do FCP e do C 002 - O
ICMS Diferencial de Alíquota da UF de Origem/Destino
03 DT_INI Data inicial a que a apuração se refere N 008* - O
04 DT_FIN Data final a que a apuração se refere N 008* - O
Observações:
Nível hierárquico – 2
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E300]
Campo 02 (UF) - Validação o valor informado no campo deve existir na tabela de UF.
Campo 03 (DT_INI) - Preenchimento: informar a data inicial a que a apuração se refere, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: verifica se a data informada é maior ou igual ao valor no campo DT_INI do registro 0000 e menor ou igual ao valor
no campo DT_FIN do registro 0000. A data informada no campo deve ser menor ou igual ao valor do campo DT_FIN deste
registro.
Campo 04 (DT_FIN) - Preenchimento: informar a data final a que a apuração se refere, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: verifica se a data informada é maior ou igual ao valor no campo DT_INI do registro 0000 e menor ou igual ao valor
no campo DT_FIN do registro 0000.
----
REGISTRO E310: APURAÇÃO DO ICMS DIFERENCIAL DE ALÍQUOTA – UF
ORIGEM/DESTINO EC 87/15. (VÁLIDO ATÉ 31/12/2016)
Este registro tem por objetivo informar valores relativos à apuração do ICMS – Diferencial de Alíquota e Fundo de
Combate à Pobreza - FCP, por UF origem/destino, mesmo nos casos de períodos sem movimento. Registro obrigatório, se
existir o registro E300.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E310" C 004 - O
02 IND_MOV_DIFAL Indicador de movimento: C - - O
0 – Sem operações com ICMS Diferencial de
Alíquota da UF de Origem/Destino
1 – Com operações de ICMS Diferencial de Alíquota
da UF de Origem/Destino
03 VL_SLD_CRED_ANT_DIFAL Valor do "Saldo credor de período anterior – ICMS N - 02 O
Diferencial de Alíquota da UF de Origem/Destino"
04 VL_TOT_DEBITOS_DIFAL Valor total dos débitos por "Saídas e prestações com N - 02 O
débito do ICMS referente ao diferencial de alíquota
devido à UF do Remetente/Destinatário"
05 VL_OUT_DEB_DIFAL Valor Total dos ajustes "Outros débitos ICMS N - 02 O
Diferencial de Alíquota da UF de Origem/Destino" "
e “Estorno de créditos ICMS Diferencial de Alíquota
da UF de Origem/Destino
06 VL_TOT_DEB_FCP Valor total dos débitos FCP por "Saídas e prestações” N - 02 O
07 VL_TOT_CREDITOS_DIFAL Valor total dos créditos do ICMS referente ao N - 02 O
diferencial de alíquota devido à UF dos Remetente/
Destinatário
08 VL_TOT_CRED_FCP Valor total dos créditos FCP por Entradas N - 02 O
09 VL_OUT_CRED_DIFAL Valor total de Ajustes "Outros créditos ICMS N - 02 O
Diferencial de Alíquota da UF de Origem/Destino" e
“Estorno de débitos ICMS Diferencial de Alíquota da
UF de Origem/Destino”
10 VL_SLD_DEV_ANT_DIFAL Valor total de Saldo devedor ICMS Diferencial de N - 02 O
Alíquota da UF de Origem/Destino antes das
deduções
11 VL_DEDUÇÕES_DIFAL Valor total dos ajustes "Deduções ICMS Diferencial N - 02 O
de Alíquota da UF de Origem/Destino"
12 VL_RECOL Valor recolhido ou a recolher referente a FCP e N - 02 O
Imposto do Diferencial de Alíquota da UF de
Origem/Destino (10-11)
13 VL_SLD_CRED_TRANSPOR Saldo credor a transportar para o período seguinte N - 02 O
TAR referente a FCP e Imposto do Diferencial de Alíquota
da UF de Origem/Destino
14 DEB_ESP_DIFAL Valores recolhidos ou a recolher, extra-apuração. N - 02 O
Observações:
Nível hierárquico - 3
Ocorrência – um (por período)
Campo 01 (REG) - Valor Válido: [E310]
Campo 02 (IND_MOV_DIFAL) - Valores Válidos: [0, 1]
Campo 03 (VL_SLD_CRED_ANT_DIFAL) – Preenchimento: Valor do campo VL_SLD_CRED_TRANSPORTAR do
período de apuração anterior.
Campo 04 (VL_TOT_DEBITOS_DIFAL) - Validação: somatório de todos os valores do C101 e D101, cujos registros pai
C100 e D100 tenham IND_OPER = 1 (Saída), exceto aqueles cujos C100 e D100 utilizarem os COD_SIT 01 ou 07. Se o campo
2 – UF do registro E300 for a do registro 0000, então corresponde à somatória dos campos VL_ICMS_UF_REM. Se o campo
2 – UF do registro E300 for a do destinatário, então corresponde à somatória dos campos VL_ICMS_UF_DEST.
Campo 05 (VL_OUT_DEB_DIFAL) – Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR do registro E311, quando o terceiro caractere for igual a ‘2’ e o quarto for igual a ‘0’ ou ‘1’, ambos do campo
COD_AJ_APUR do registro E311.
Campo 06 (VL_TOT_DEB_FCP) – Validação: soma de todos os valores do C101 e D101, cujos registros pai C100 e D100
tenham IND_OPER = 1 (Saída), exceto aqueles cujos C100 e D100 utilizarem os COD_SIT 01 ou 07. Se o campo 2 – UF do
registro E300 for a do registro 0000, este valor será zero. Se o campo 2 – UF do registro E300 for a do destinatário, então
corresponde à somatória dos campos VL_FCP_UF_DEST.
Campo 07 (VL_TOT_CREDITOS_DIFAL) – Validação: soma de todos os valores do C101 e D101, cujos registros pai C100
e D100 tenham IND_OPER = 0 (Entrada). Se o campo 2 – UF do registro E300 for a do registro 0000, então corresponde à
somatória dos campos VL_ICMS_UF_DEST. Se o campo 2 – UF do registro E300 for a do remetente (em devolução), então
corresponde à somatória dos campos VL_ICMS_UF_REM.
Campo 08 (VL_TOT_CRED_FCP) – Validação: soma de todos os valores do C101 e D101, cujos registros pai C100 e D100
tenham IND_OPER = 0 (Entrada). Se o campo 2 – UF do registro E300 for a do registro 0000, este valor sempre será igual a
zero. Se o campo 2 – UF do registro E300 for a do remetente (em devolução), então corresponde à somatória dos campos
VL_FCP_UF_DEST.
Campo 09 (VL_OUT_CRED_DIFAL) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR dos registros E311, quando o terceiro caractere for igual a ‘2’ e o quarto caractere do campo COD_AJ_APUR
for igual a ‘2’ ou ‘3’.
Campo 10 (VL_SLD_DEV_ANT_DIFAL) - Validação: Se (VL_TOT_DEBITOS_DIFAL + VL_OUT_DEB_DIFAL+
VL_TOT_DEB_FCP) menos (VL_SLD_CRED_ANT_DIFAL + VL_TOT_CREDITOS_DIFAL + VL_OUT_CRED_DIFAL
+ VL_TOT_CRED_FCP) for maior ou igual a ZERO, então o resultado deverá ser igual ao VL_SLD_DEV_ANT_DIFAL;
senão VL_SLD_DEV_ANT_DIFAL deve ser igual a ZERO.
Campo 11 (VL_DEDUÇÕES_DIFAL) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR do registro E311, por UF, quando o terceiro caractere for igual a ‘2’ e o quarto caractere do campo
COD_AJ_APUR for igual a ‘4’.
Campo 12 (VL_RECOL) - Validação: Se (VL_SLD_DEV_ANT_DIFAL menos VL_DEDUCOES_DIFAL) for maior ou
igual a ZERO, então VL_RECOL é igual ao resultado da equação; senão o VL_RECOL deverá ser igual a ZERO.
VL_RECOL + DEB_ESP_DIFAL = soma do campo VL_OR (E316).
Campo 13 (VL_SLD_CRED_TRANSPORTAR) – Validação: Se (VL_SLD_CRED_ANT_DIFAL +
VL_TOT_CREDITOS_DIFAL + VL_OUT_CRED_DIFAL+ VL_TOT_CRED_FCP) menos (VL_TOT_DEBITOS_DIFAL+
VL_OUT_DEB_DIFAL+ VL_TOT_DEB_FCP) for maior que ZERO, então VL_SLD_CRED_TRANSPORTAR deve ser
igual ao resultado da equação; senão VL_SLD_CRED_TRANSPORTAR será ZERO.
Campo 14 (DEB_ESP_DIFAL) – Validação: Informar por UF:
Somatório dos campos VL_AJ_APUR dos registros E311, se o campo COD_AJ_APUR possuir o terceiro caractere do código
informado no registro E311 igual a “2” e o quarto caractere for igual a “5".
*Somente para o primeiro período de apuração:
Se a UF do Registro E300 for igual a UF do Registro 0000, a soma de todos os campos VL_ICMS_UF_REM dos Registros
C101 e D101 cujos registros pais C100 e D100 possuam o campo IND_OPER igual a 1 (Saída) e o campo COD_SIT igual a
“01” ou “07”.
Se a UF do Registro E300 for diferente da UF do Registro 0000, a soma dos campos VL_FCP_UF_DEST e
VL_ICMS_UF_DEST dos registros C101 e D101, cujos registros pais C100 e D100 possuem o campo IND_OPER igual a 1
(Saída) e o campo COD_SIT igual a “01” ou “07”.
----
REGISTRO E310: APURAÇÃO DO FUNDO DE COMBATE À POBREZA E DO ICMS
DIFERENCIAL DE ALÍQUOTA – UF ORIGEM/DESTINO EC 87/15. (VÁLIDO A PARTIR DE
01/01/2017)
Este registro tem por objetivo informar valores relativos à apuração do ICMS – Diferencial de Alíquota e Fundo de
Combate à Pobreza - FCP, por UF origem/destino, mesmo nos casos de períodos sem movimento. Registro obrigatório, se
existir o registro E300.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E310" C 004 - O
02 IND_MOV_FCP_DIFAL Indicador de movimento: C - - O
0 – Sem operações
1 – Com operações
03 VL_SLD_CRED_ANT_DIFAL Valor do "Saldo credor de período anterior – ICMS N - 02 O
Diferencial de Alíquota da UF de Origem/Destino"
04 VL_TOT_DEBITOS_DIFAL Valor total dos débitos por "Saídas e prestações com N - 02 O
débito do ICMS referente ao diferencial de alíquota
devido à UF de Origem/Destino"
05 VL_OUT_DEB_DIFAL Valor total dos ajustes "Outros débitos ICMS N - 02 O
Diferencial de Alíquota da UF de Origem/Destino" e
“Estorno de créditos ICMS Diferencial de Alíquota da
UF de Origem/Destino”
06 VL_TOT_CREDITOS_DIFAL Valor total dos créditos do ICMS referente ao N - 02 O
diferencial de alíquota devido à UF de
Origem/Destino
07 VL_OUT_CRED_DIFAL Valor total de Ajustes "Outros créditos ICMS N - 02 O
Diferencial de Alíquota da UF de Origem/Destino" e
“Estorno de débitos ICMS Diferencial de Alíquota da
UF de Origem/Destino”
08 VL_SLD_DEV_ANT_DIFAL Valor total de “Saldo devedor ICMS Diferencial de N - 02 O
Alíquota da UF de Origem/Destino antes das
deduções”
09 VL_DEDUÇÕES_DIFAL Valor total dos ajustes "Deduções ICMS Diferencial N - 02 O
de Alíquota da UF de Origem/Destino"
10 VL_RECOL_DIFAL Valor recolhido ou a recolher referente ao ICMS N - 02 O
Diferencial de Alíquota da UF de Origem/Destino
(08-09)
11 VL_SLD_CRED_TRANSPORT Saldo credor a transportar para o período seguinte N - 02 O
AR_DIFAL referente ao ICMS Diferencial de Alíquota da UF de
Origem/Destino
12 DEB_ESP_DIFAL Valores recolhidos ou a recolher, extra-apuração - N - 02 O
ICMS Diferencial de Alíquota da UF de
Origem/Destino.
13 VL_SLD_CRED_ANT_FCP Valor do "Saldo credor de período anterior – FCP" N - 02 O
14 VL_TOT_DEB_FCP Valor total dos débitos FCP por "Saídas e prestações” N - 02 O
15 VL_OUT_DEB_FCP Valor total dos ajustes "Outros débitos FCP" e N - 02 O
“Estorno de créditos FCP”
16 VL_TOT_CRED_FCP Valor total dos créditos FCP por Entradas N - 02 O
17 VL_OUT_CRED_FCP Valor total de Ajustes "Outros créditos FCP" e N - 02 O
“Estorno de débitos FCP”
18 VL_SLD_DEV_ANT_FCP Valor total de Saldo devedor FCP antes das deduções N - 02 O
19 VL_DEDUÇÕES_FCP Valor total das deduções "FCP" N - 02 O
20 VL_RECOL_FCP Valor recolhido ou a recolher referente ao FCP (18– N - 02 O
19)
21 VL_SLD_CRED_TRANSPORT Saldo credor a transportar para o período seguinte N - 02 O
AR_FCP referente ao FCP
22 DEB_ESP_FCP Valores recolhidos ou a recolher, extra-apuração - N - 02 O
FCP.
Observações:
Nível hierárquico - 3
Ocorrência – um (por período)
Campo 01 (REG) - Valor Válido: [E310]
Campo 02 (IND_MOV_FCP_DIFAL) - Valores Válidos: [0, 1]
Campo 03 (VL_SLD_CRED_ANT_DIFAL) – Preenchimento: Valor do campo
VL_SLD_CRED_TRANSPORTAR_DIFAL do período de apuração anterior.
Campo 04 (VL_TOT_DEBITOS_DIFAL) - Validação:
Somatório dos valores dos campos VL_ICMS_UF_REM dos registros C101 cujo registro pai, C100 tenham IND_OPER = 1
(Saída), exceto aqueles com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for a do registro 0000
Mais
Somatório dos valores dos campos VL_ICMS_UF_DEST dos registros C101 cujo registro pai, C100 tenham IND_OPER = 1
(Saída), exceto aqueles com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a UF do participante
informado no campo COD_PART do registro C100
Mais
Somatório dos valores dos campos VL_ICMS_UF_REM dos registros D101 cujo registro pai, D100 tenham IND_OPER = 1
(Prestação), exceto aqueles com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a do município
informado no campo COD_MUN_ORIG do registro D100
Mais
Somatório dos valores dos campos VL_ICMS_UF_DEST dos registros D101 cujo registro pai, D100 tenham IND_OPER = 1
(Prestação), exceto aqueles com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a do município
informado no campo COD_MUN_DEST do registro D100.
Os documentos fiscais devem ser somados conforme o período informado no registro E300 e a data informada no campo
DT_E_S (C100) ou campo DT_A_P (D100), exceto se COD_SIT do documento for igual a “01” (extemporâneo) ou igual a 07
(NF Complementar extemporânea) cujo valor será somado no campo “DEB_ESP_DIFAL” do primeiro período de apuração
informado no registro E300.
Quando o campo DT_E_S ou DT_A_P não for informado, é utilizada a data constante no campo DT_DOC.
Campo 05 (VL_OUT_DEB_DIFAL) – Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR do registro E311, quando o terceiro caractere for igual a ‘2’ e o quarto for igual a ‘0’ ou ‘1’, ambos do campo
COD_AJ_APUR do registro E311.
Campo 06 (VL_TOT_CREDITOS_DIFAL) – Validação:
Somatório dos valores dos campos VL_ICMS_UF_DEST dos registros C101 cujo registro pai, C100 tenham IND_OPER = 0
(Entrada), se o campo 2 – UF do registro E300 for a do registro 0000
Mais
Somatório dos valores dos campos VL_ICMS_UF_REM dos registros C101 cujo registro pai, C100 tenham IND_OPER = 0
(Entrada), se o campo 2 – UF do registro E300 for igual a UF do participante informado no campo COD_PART do registro
C100
Mais
Somatório dos valores dos campos VL_ICMS_UF_DEST dos registros D101 cujo registro pai, D100 tenham IND_OPER = 0
(Aquisição), se o campo 2 – UF do registro E300 for igual a do município informado no campo COD_MUN_DEST do registro
D100
Mais
Somatório dos valores dos campos VL_ICMS_UF_REM dos registros D101 cujo registro pai, D100 tenham IND_OPER = 0
(Aquisição), se o campo 2 – UF do registro E300 for igual a do município informado no campo COD_MUN_ORIG do registro
D100.
Os documentos fiscais devem ser somados conforme o período informado no registro E300 e a data informada no campo
DT_E_S (C100) ou campo DT_A_P (D100), exceto se COD_SIT do documento for igual a “01” (extemporâneo) ou igual a 07
(NF Complementar extemporânea), cujo valor será somado no primeiro período de apuração informado no registro E300.
Quando o campo DT_E_S ou DT_A_P não for informado, é utilizada a data constante no campo DT_DOC.
Campo 07 (VL_OUT_CRED_DIFAL) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR dos registros E311, quando o terceiro caractere for igual a ‘2’ e o quarto caractere do campo COD_AJ_APUR
for igual a ‘2’ ou ‘3’.
Campo 08 (VL_SLD_DEV_ANT_DIFAL) - Validação: Se (VL_TOT_DEBITOS_DIFAL + VL_OUT_DEB_DIFAL) menos
(VL_SLD_CRED_ANT_DIFAL + VL_TOT_CREDITOS_DIFAL + VL_OUT_CRED_DIFAL) for maior ou igual a ZERO,
então o resultado deverá ser igual ao VL_SLD_DEV_ANT_DIFAL; senão VL_SLD_DEV_ANT_DIFAL deve ser igual a
ZERO.
Campo 09 (VL_DEDUÇÕES_DIFAL) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR do registro E311, por UF, quando o terceiro caractere for igual a ‘2’ e o quarto caractere do campo
COD_AJ_APUR for igual a ‘4’.
Campo 10 (VL_RECOL_DIFAL) - Validação: Se (VL_SLD_DEV_ANT_DIFAL menos VL_DEDUCOES_DIFAL) for
maior ou igual a ZERO, então VL_RECOL_DIFAL é igual ao resultado da equação; senão o VL_RECOL_DIFAL deverá ser
igual a ZERO.
VL_RECOL_DIFAL + DEB_ESP_DIFAL + VL_RECOL_FCP + DEB_ESP_FCP = soma do campo VL_OR (E316).
Campo 11 (VL_SLD_CRED_TRANSPORTAR_DIFAL) – Validação: Se (VL_SLD_CRED_ANT_DIFAL +
VL_TOT_CREDITOS_DIFAL + VL_OUT_CRED_DIFAL + VL_DEDUÇÕES_DIFAL) menos
(VL_TOT_DEBITOS_DIFAL+ VL_OUT_DEB_DIFAL) for maior que ZERO, então
VL_SLD_CRED_TRANSPORTAR_DIFAL deve ser igual ao resultado da equação; senão
VL_SLD_CRED_TRANSPORTAR_DIFAL será ZERO.
Campo 12 (DEB_ESP_DIFAL) – Validação: Informar por UF:
Somatório dos campos VL_AJ_APUR dos registros E311, se o campo COD_AJ_APUR possuir o terceiro caractere do código
informado no registro E311 igual a “2” e o quarto caractere for igual a “5".
MAIS
Somente para o primeiro período de apuração:
Somatório dos valores dos campos VL_ICMS_UF_REM dos registros C101 cujo registro pai, C100, tenham IND_OPER = 1
(Saída) com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for a do registro 0000
Mais
Somatório dos valores dos campos VL_ICMS_UF_DEST dos registros C101 cujo registro pai, C100, tenham IND_OPER = 1
(Saída) com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a UF do participante informado no campo
COD_PART do registro C100
Mais
Somatório dos valores dos campos VL_ICMS_UF_REM dos registros D101 cujo registro pai, D100, tenham IND_OPER = 1
(Prestação) com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a do município informado no campo
COD_MUN_ORIG do registro D100
Mais
Somatório dos valores dos campos VL_ICMS_UF_DEST dos registros D101 cujo registro pai, D100, tenham IND_OPER = 1
(Prestação) com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a do município informado no campo
COD_MUN_DEST do registro D100.
Campo 13 (VL_SLD_CRED_ANT_FCP) – Validação: Valor do campo VL_SLD_CRED_TRANSPORTAR_FCP do período
de apuração anterior.
Campo 14 (VL_TOT_DEB_FCP) – Preenchimento: Se a UF do Registro E300 for igual à UF do Registro 0000, informar o
valor zero.
Validação: Somatório dos valores dos campos VL_FCP_UF_DEST dos registros C101 cujo registro pai, C100 tenham
IND_OPER = 1 (Saída), exceto aqueles com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a UF do
participante (destinatário) informado no campo COD_PART do registro C100.
Mais
Somatório dos valores dos campos VL_FCP_UF_DEST dos registros D101 cujo registro pai, D100 tenham IND_OPER = 1
(Prestação), exceto aqueles com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a do município
informado no campo COD_MUN_DEST do registro D100.
Se o campo 2 – UF do registro E300 for a do COD_MUN_ORIG, este valor será zero.
Os documentos fiscais devem ser somados conforme o período informado no registro E300 e a data informada no campo
DT_E_S (C100) ou campo DT_A_P (D100), exceto se COD_SIT do documento for igual a “01” (extemporâneo) ou igual a 07
(NF Complementar extemporânea) cujo valor será somado no campo “DEB_ESP_FCP” do primeiro período de apuração
informado no registro E300.
Quando o campo DT_E_S ou DT_A_P não for informado, é utilizada a data constante no campo DT_DOC.
Campo 15 (VL_OUT_DEB_FCP) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ_APUR
do registro E311, quando o terceiro caractere for igual a ‘3’ e o quarto for igual a ‘0’ ou ‘1’, ambos do campo COD_AJ_APUR
do registro E311.
Campo 16 (VL_TOT_CRED_FCP) – Preenchimento: Se a UF do Registro E300 for igual à UF do Registro 0000, informar
o valor zero.
Validação: Somatório dos valores dos campos VL_FCP_UF_DEST dos registros C101 cujo registro pai, C100 tenham
IND_OPER = 0 (Entrada) se o campo 2 – UF do registro E300 for a do remetente (em devolução);
Mais
Somatório dos valores dos campos VL_FCP_UF_DEST dos registros D101 cujo registro pai, D100 tenham IND_OPER = 0
(Aquisição) “devolução”, se o campo 2 – UF do registro E300 for igual a do município informado no campo COD_MUN_ORIG
do registro D100; se o campo 2 – UF do registro E300 for a do COD_MUN_DEST, este valor será igual a zero.
Os documentos fiscais devem ser somados conforme o período informado no registro E300 e a data informada no campo
DT_E_S (C100) ou campo DT_A_P (D100), exceto se COD_SIT do documento for igual a “01” (extemporâneo) ou igual a 07
(NF Complementar extemporânea), cujo valor será somado no primeiro período de apuração informado no registro E300.
Quando o campo DT_E_S ou DT_A_P não for informado, é utilizada a data constante no campo DT_DOC.
Campo 17 (VL_OUT_CRED_FCP) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ_APUR
dos registros E311, quando o terceiro caractere for igual a ‘3’ e o quarto caractere do campo COD_AJ_APUR for igual a ‘2’
ou ‘3’.
Campo 18 (VL_SLD_DEV_ANT_FCP) - Validação: Se (VL_TOT_DEB_FCP + VL_OUT_DEB_FCP) menos
(VL_SLD_CRED_ANT_FCP + VL_TOT_CRED_FCP + VL_OUT_CRED_FCP) for maior ou igual a ZERO, então o
resultado deverá ser igual ao VL_SLD_DEV_ANT_FCP; senão VL_SLD_DEV_ANT_FCP deve ser igual a ZERO.
Campo 19 (VL_DEDUÇÕES_FCP) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ_APUR
do registro E311, por UF, quando o terceiro caractere for igual a ‘3’ e o quarto caractere do campo COD_AJ_APUR for igual
a ‘4’.
Campo 20 (VL_RECOL_FCP) - Validação: Se (VL_SLD_DEV_ANT_FCP menos VL_DEDUCOES_FCP) for maior ou
igual a ZERO, então VL_RECOL_FCP é igual ao resultado da equação; senão o VL_RECOL_FCP deverá ser igual a ZERO.
VL_RECOL_DIFAL + DEB_ESP_DIFAL + VL_RECOL_FCP + DEB_ESP_FCP = soma do campo VL_OR (E316).
Campo 21 (VL_SLD_CRED_TRANSPORTAR_FCP) – Validação: Se (VL_SLD_CRED_ANT_FCP +
VL_TOT_CRED_FCP + VL_OUT_CRED_FCP + VL_DEDUÇÕES_FCP) menos (VL_TOT_DEB_FCP +
VL_OUT_DEB_FCP) for maior que ZERO, então VL_SLD_CRED_TRANSPORTAR_FCP deve ser igual ao resultado da
equação; senão VL_SLD_CRED_TRANSPORTAR_FCP será ZERO.
Campo 22 (DEB_ESP_FCP) – Validação: Somatório dos campos VL_AJ_APUR dos registros E311, se o campo
COD_AJ_APUR possuir o terceiro caractere do código informado no registro E311 igual a “3” e o quarto caractere for igual a
“5".
MAIS
Somente para o primeiro período da apuração: Somatório dos valores dos campos VL_FCP_UF_DEST dos registros C101 cujo
registro pai, C100 tenham IND_OPER = 1 (Saída) com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for
igual a UF do participante (destinatário) informado no campo COD_PART do registro C100.
Mais
Somatório dos valores dos campos VL_FCP_UF_DEST dos registros D101 cujo registro pai, D100 tenham IND_OPER = 1
(Prestação) com COD_SIT sejam 01 ou 07, se o campo 2 – UF do registro E300 for igual a do município informado no campo
COD_MUN_DEST do registro D100.
Se o campo 2 – UF do registro E300 for a do COD_MUN_ORIG, este valor será zero.
----
REGISTRO E311: AJUSTE/BENEFÍCIO/INCENTIVO DA APURAÇÃO DO FUNDO DE
COMBATE À POBREZA E DO ICMS DIFERENCIAL DE ALÍQUOTA UF ORIGEM/DESTINO
EC 87/15
Este registro deve ser apresentado para discriminar os ajustes lançados nos campos VL_OUT_CRED_DIFAL,
VL_OUT_DEB_DIFAL, VL_DEDUÇOES_DIFAL, VL_OUT_CRED_FCP, VL_OUT_DEB_FCP e VL_DEDUÇOES_FCP
e os valores informados nos campos DEB_ESP_DIFAL e DEB_ESP_FCP, todos do registro E310
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E311" C 004 - O
02 COD_AJ_APUR Código do ajuste da apuração e dedução, conforme a Tabela C 008* - O
indicada no item 5.1.1
03 DESCR_COMPL_AJ Descrição complementar do ajuste da apuração C - - OC
04 VL_AJ_APUR Valor do ajuste da apuração N - 02 O
Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E311]
Campo 02 (COD_AJ_APUR) – Preenchimento: Até 31/12/2016, o valor informado no campo deve existir na tabela de código
do ajuste da apuração e dedução de cada Secretaria de Fazenda – ICMS Difal e/ou FCP – da tabela 5.1.1 - Tabela de Códigos
de Ajuste da Apuração do ICMS do item 5.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações –
Ajustes dos Saldos da Apuração do ICMS:
XX209999 - Outros débitos para ajuste de apuração ICMS Difal/FCP para a UF XX;
XX219999 - Estorno de créditos para ajuste de apuração ICMS Difal/FCP para a UF XX;
XX229999 - Outros créditos para ajuste de apuração ICMS Difal/FCP para a UF XX;
XX239999 - Estorno de débitos para ajuste de apuração ICMS Difal/FCP para a UF XX;
XX249999 - Deduções do imposto apurado na apuração ICMS Difal/FCP para a UF XX;
XX259999 - Débito especial de ICMS Difal/FCP para a UF XX.
A partir de 01/01/2017, o valor informado no campo deve existir na tabela de código do ajuste da apuração e dedução
de cada Secretaria de Fazenda – ICMS Difal e/ou FCP – da tabela 5.1.1 - Tabela de Códigos de Ajuste da Apuração do ICMS
do item 5.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações – Ajustes dos Saldos da Apuração do
ICMS. Os códigos genéricos são os descritos a seguir, observando que, quando o 3º caracter for igual a “2”, deve ser utilizado
para DIFAL e, quando for igual a “3”, deve ser utilizado para FCP:
XX209999 - Outros débitos para ajuste de apuração ICMS Difal para a UF XX;
XX219999 - Estorno de créditos para ajuste de apuração ICMS Difal para a UF XX;
XX229999 - Outros créditos para ajuste de apuração ICMS Difal para a UF XX;
XX239999 - Estorno de débitos para ajuste de apuração ICMS Difal para a UF XX;
XX249999 - Deduções do imposto apurado na apuração ICMS Difal para a UF XX;
XX259999 - Débito especial de ICMS Difal para a UF XX;
XX309999 - Outros débitos para ajuste de apuração ICMS FCP para a UF XX;
XX319999 - Estorno de créditos para ajuste de apuração ICMS FCP para a UF XX;
XX329999 - Outros créditos para ajuste de apuração ICMS FCP para a UF XX;
XX339999 - Estorno de débitos para ajuste de apuração ICMS FCP para a UF XX;
XX349999 - Deduções do imposto apurado na apuração ICMS FCP para a UF XX;
XX359999 - Débito especial de ICMS FCP para a UF XX.
Campo 03 (DESCR_COMPL_AJ) - Preenchimento: Sem prejuízo de outras situações definidas em legislação específica, o
contribuinte deverá fazer a descrição complementar de ajustes (tabela 5.1.1) sempre que informar códigos genéricos.
Campo 04 (VL_AJ_APUR) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
REGISTRO E312: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA APURAÇÃO DO FUNDO
DE COMBATE À POBREZA E DO ICMS DIFERENCIAL DE ALÍQUOTA UF
ORIGEM/DESTINO EC 87/15
Este registro deve ser apresentado para detalhar os ajustes do registro E311 quando forem relacionados a processos
judiciais ou fiscais ou a documentos de arrecadação, observada a legislação estadual pertinente. Os valores recolhidos, com
influência na apuração do ICMS Difal e/ou FCP, devem ser informados neste registro, com identificação do documento de
arrecadação específico.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E312" C 004 - O
02 NUM_DA Número do documento de arrecadação estadual, se houver C - - OC
03 NUM_PROC Número do processo ao qual o ajuste está vinculado, se houver C 060 - OC
04 IND_PROC Indicador da origem do processo: N 001* - OC
0- Sefaz;
1- Justiça Federal;
2- Justiça Estadual;
9- Outros
05 PROC Descrição resumida do processo que embasou o lançamento C - - OC
06 TXT_COMPL Descrição complementar C - - OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E312]
Campo 02 (NUM_DA) - Preenchimento: este campo deve ser preenchido se o ajuste for referente a um documento de
arrecadação, conforme dispuser a legislação pertinente.
Campo 03 (NUM_PROC) - Preenchimento: o valor deve ter até 60 caracteres.
Campo 04 (IND_PROC) - Valores válidos: [0, 1, 2, 9]
Campo 06 (TXT_COMPL) - Preenchimento: Outras informações complementares.
----
REGISTRO E313: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA APURAÇÃO DO FUNDO
DE COMBATE À POBREZA E DO ICMS DIFERENCIAL DE ALÍQUOTA UF
ORIGEM/DESTINO EC 87/15 - IDENTIFICAÇÃO DOS DOCUMENTOS FISCAIS
Este registro deve ser apresentado para identificação dos documentos fiscais relacionados ao ajuste.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E313" C 004 - O
02 COD_PART Código do participante (campo 02 do Registro 0150) C 060 - OC
03 COD_MOD Código do modelo do documento fiscal, conforme a Tabela 4.1.1 C 002* - O
04 SER Série do documento fiscal C 004 - OC
05 SUB Subsérie do documento fiscal N 003 - OC
06 NUM_DOC Número do documento fiscal N 009 - O
07 CHV_DOCe Chave do Documento Eletrônico N 044* - OC
08 DT_DOC Data da emissão do documento fiscal N 008* - O
09 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC
10 VL_AJ_ITEM Valor do ajuste para a operação/item N - 02 O
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E313]
Campo 02 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Validação: o valor informado deve existir no campo COD_PART do registro 0150, exceto quando o modelo de documento
for igual a 63 (BP-e)
Campo 03 (COD_MOD) - Valores válidos: o valor informado no campo deve existir na tabela de Documentos Fiscais do
ICMS, conforme Item 4.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações – Ver tabela
reproduzida na subseção 1.4 deste guia.
Campo 06 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (CHV_DOCe) - Preenchimento: informar a chave da NF-e, para documentos de COD_MOD igual a “55”, ou
informar a chave do conhecimento de transporte eletrônico, para documentos de COD_MOD igual a “57”. A partir de abril/2017,
informar a chave do CT-e OS (COD_MOD igual a “67"). A partir de 01/01/2018, informar a chave do BP-e (COD_MOD igual
a “63”).
Validação: quando se tratar de NF-e, CT-e,
CT-e OS ou BP-e, é conferido o dígito verificador (DV) da chave do documento eletrônico. Será verificada a consistência da
informação dos campos NUM_DOC e SER com o número do documento e série contidos na chave do documento eletrônico.
Campo 08 (DT_DOC) - Preenchimento: informar a data de emissão do documento fiscal, no formato “ddmmaaaa”, sem os
separadores de formatação.
Campo 09 (COD_ITEM) – Preenchimento: este campo só deve ser informado quando o ajuste se referir a um determinado
item/produto do documento.
Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
Campo 10 (VL_AJ_ITEM) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
REGISTRO E316: OBRIGAÇÕES RECOLHIDAS OU A RECOLHER – FUNDO DE COMBATE
À POBREZA E ICMS DIFERENCIAL DE ALÍQUOTA UF ORIGEM/DESTINO EC 87/15
Este registro deve ser apresentado para discriminar os pagamentos realizados ou a realizar, referentes à apuração do
ICMS devido por diferencial de alíquota e/ou FCP do período, por UF. A soma do valor das obrigações a serem discriminadas
neste registro deve ser igual ao campo VL_RECOL (registro E310) somado ao campo DEB_ESP_DIFAL (registro E310) até
31/12/2016.
A partir de 01/01/2017, a soma do valor das obrigações a serem discriminadas neste registro deve ser igual ao
somatório dos campos: VL_RECOL_DIFAL + DEB_ESP_DIFAL + VL_RECOL_FCP + DEB_ESP_FCP.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "E316" C 004 - O
02 COD_OR Código da obrigação recolhida ou a recolher, conforme a Tabela 5.4 C 003* - O
03 VL_OR Valor da obrigação recolhida ou a recolher N - 02 O
04 DT_VCTO Data de vencimento da obrigação N 008* - O
05 COD_REC Código de receita referente à obrigação, próprio da unidade da C - - O
federação da origem/destino, conforme legislação estadual.
06 NUM_PROC Número do processo ou auto de infração ao qual a obrigação está C 060 - OC
vinculada, se houver
07 IND_PROC Indicador da origem do processo: C 001* - OC
0- SEFAZ;
1- Justiça Federal;
2- Justiça Estadual;
9- Outros
08 PROC Descrição resumida do processo que embasou o lançamento C - - OC
09 TXT_COMPL Descrição complementar das obrigações recolhidas ou a recolher C - - OC
10 MES_REF* Informe o mês de referência no formato “mmaaaa” N 006* - O
Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E316]
Campo 02 (COD_OR) - Valores válidos: [000, 003, 006, 090]
Campo 03 (VL_OR) – Validação: o valor da soma deste campo deve corresponder à soma dos campos VL_RECOL_DIFAL
+ DEB_ESP_DIFAL + VL_RECOL_FCP + DEB_ESP_FCP do registro E310. Não informar acréscimos legais, se houver.
Campo 04 (DT_VCTO) - Preenchimento: informar a data de vencimento da obrigação, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: o valor informado no campo deve ser uma data válida.
Campo 05 (COD_REC) - Validação: Quando o campo 02 (UF) do registro E300 for igual ao campo 09 (UF) do registro 0000,
se existir tabela de códigos de receita da UF, o valor informado deve existir na referida tabela.
Campo 06 (NUM_PROC) - Validação: se este campo estiver preenchido, os campos IND_PROC e PROC deverão estar
preenchidos. Se este campo não estiver preenchido, os campos IND_PROC e PROC não deverão estar preenchidos. O valor
deve ter até 60 caracteres.
Campo 07 (IND_PROC) - Valores válidos: [0, 1, 2, 9]
Campo 10 (MES_REF) – Preenchimento: formato mmaaaa, sem utilizar os caracteres especiais de separação.
Validação: O campo MES_REF* não pode ser superior à competência do campo DT_INI do registro 0000
----
REGISTRO E500: PERÍODO DE APURAÇÃO DO IPI
Este registro deve ser apresentado pelos estabelecimentos industriais ou equiparados, conforme dispõe o Regulamento
do IPI, para identificação do(s) período(s) de apuração. O(s) período(s) informado(s) deve(m) abranger todo o período previsto
no registro 0000.
Poderá coexistir um período mensal com períodos decendiais. Para os períodos decendiais, não poderá haver
sobreposição ou omissão de datas.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E500" C 004 - O
02 IND_APUR Indicador de período de apuração do IPI: C 1* - O
0 - Mensal;
1 - Decendial
03 DT_INI Data inicial a que a apuração se refere N 008* - O
04 DT_FIN Data final a que a apuração se refere N 008* - O
Observações:
Nível hierárquico - 2
Ocorrência –um ou vários (por arquivo)
Campo 01 (REG) - Valor Válido: [E500]
Campo 02 (IND_APUR) - Valores válidos: [0, 1]
Campo 03 (DT_INI) - Preenchimento: informar a data inicial a que a apuração se refere, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: verifica se a data informada é maior ou igual ao campo DT_INI do registro 0000 e menor ou igual ao valor no
campo DT_FIN do registro 0000.
Campo 04 (DT_FIN) - Preenchimento: informar a data final a que a apuração se refere, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: verifica se a data informada é maior ou igual ao valor no campo DT_INI do registro 0000 e menor ou igual ao valor
no campo DT_FIN do registro 0000.
----
REGISTRO E510: CONSOLIDAÇÃO DOS VALORES DO IPI
Este registro deve ser preenchido com os valores consolidados do IPI, de acordo com o período informado no registro
E500, tomando-se por base as informações prestadas no registro C170 ou, nos casos de notas fiscais eletrônicas de emissão
própria, no registro C100. A consolidação se dará pela sumarização do valor contábil, base de cálculo e imposto relativo a todas
as operações, conforme a combinação de CFOP e código da situação tributária do IPI (CST_IPI).
As informações oriundas dos itens dos documentos fiscais – registro C170 ou do documento NF-e de emissão própria
– serão consideradas no período de apuração mensal ou decendial, conforme preenchimento do campo IND_APUR.
Validação do Registro: Chave do registro: CFOP e CST_IPI
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E510" C 004 - O
02 CFOP Código Fiscal de Operação e Prestação do agrupamento de itens N 004* - O
03 CST_IPI Código da Situação Tributária referente ao IPI, conforme a Tabela C 002* - O
indicada no item 4.3.2.
04 VL_CONT_IPI Parcela correspondente ao "Valor Contábil" referente ao CFOP e N - 02 O
ao Código de Tributação do IPI
05 VL_BC_IPI Parcela correspondente ao "Valor da base de cálculo do IPI" N - 02 O
referente ao CFOP e ao Código de Tributação do IPI, para
operações tributadas
06 VL_IPI Parcela correspondente ao "Valor do IPI" referente ao CFOP e ao N - 02 O
Código de Tributação do IPI, para operações tributadas
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [E510]
Campo 02 (CFOP) - Preenchimento: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e
Prestação, conforme Ajuste SINIEF 07/01.
Campo 03 (CST_IPI) - Preenchimento: O campo deverá ser preenchido somente se o declarante for contribuinte do IPI. A
tabela do CST_IPI consta publicada na Instrução Normativa RFB nº 932, de 14/04/2009, atualizada pela IN RFB 1009/2010.
Código Descrição
00 Entrada com recuperação de crédito
01 Entrada tributada com alíquota zero
02 Entrada isenta
03 Entrada não-tributada
04 Entrada imune
05 Entrada com suspensão
49 Outras entradas
50 Saída tributada
51 Saída tributada com alíquota zero
52 Saída isenta
53 Saída não-tributada
54 Saída imune
55 Saída com suspensão
99 Outras saídas
Campo 06 (VL_IPI) - Validação: O total de créditos e dos débitos informados neste registro deverá ser igual ao total dos
créditos e débitos dos registros C190 e do registro E520.
----
REGISTRO E520: APURAÇÃO DO IPI
Este registro deve ser preenchido para demonstração da apuração do IPI no período.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "E520" C 004 - O
02 VL_SD_ANT_IPI Saldo credor do IPI transferido do período anterior N - 02 O
03 VL_DEB_IPI Valor total dos débitos por "Saídas com débito do imposto" N - 02 O
04 VL_CRED_IPI Valor total dos créditos por "Entradas e aquisições com crédito do N - 02 O
imposto"
05 VL_OD_IPI Valor de "Outros débitos" do IPI (inclusive estornos de crédito) N - 02 O
06 VL_OC_IPI Valor de "Outros créditos" do IPI (inclusive estornos de débitos) N - 02 O
07 VL_SC_IPI Valor do saldo credor do IPI a transportar para o período seguinte N - 02 O
08 VL_SD_IPI Valor do saldo devedor do IPI a recolher N - 02 O
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [E520]
Campo 03 (VL_DEB_IPI) - Validação: o valor informado deve corresponder ao somatório do campo VL_IPI do registro E510,
quando o CFOP iniciar por ‘5’ ou ‘6” dos registros C190.
Campo 04 (VL_CRED_IPI) - Validação: o valor informado deve corresponder ao somatório do campo VL_IPI do registro
E510, quando o CFOP iniciar por ‘1’, ‘2’ ou ‘3’ dos registros C190.
Campo 05 (VL_OD_IPI) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ do registro E530,
quando o campo IND_AJ do registro E530 for igual a ‘0’.
Campo 06 (VL_OC_IPI) - Validação: o valor informado deve corresponder ao somatório do campo VL_AJ do registro E530,
quando o campo IND_AJ do registro E530 for igual a ‘1’.
Campo 07 (VL_SC_IPI) - Validação: se a soma dos campos VL_DEB_IPI e VL_OD_IPI menos a soma dos campos
VL_SD_ANT_IPI, VL_CRED_IPI e VL_OC_IPI for menor que “0” (zero), então o campo VL_SC_IPI deve ser igual ao valor
absoluto da expressão, e o valor do campo VL_SD_IPI deve ser igual a “0” (zero).
Campo 08 (VL_SD_IPI) - Validação: se a soma dos campos VL_DEB_IPI e VL_OD_IPI menos a soma dos campos
VL_SD_ANT_IPI, VL_CRED_IPI e VL_OC_IPI for maior ou igual a “0” (zero), então o campo 08 (VL_SD_IPI) deve ser
igual ao resultado da expressão, e o valor do campo VL_SC_IPI deve ser igual a “0” (zero).
----
REGISTRO E530: AJUSTES DA APURAÇÃO DO IPI
Este registro deve ser apresentado para discriminar os ajustes lançados nos campos Outros Débitos e Outros Créditos
do registro E520.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E530" C 004 - O
02 IND_AJ Indicador do tipo de ajuste: C 001* - O
0- Ajuste a débito;
1- Ajuste a crédito
03 VL_AJ Valor do ajuste N - 02 O
04 COD_AJ Código do ajuste da apuração, conforme a Tabela indicada no item C 003* O
4.5.4.
05 IND_DOC Indicador da origem do documento vinculado ao ajuste: C 001* - O
0 - Processo Judicial;
1 - Processo Administrativo;
2 - PER/DCOMP;
3 – Documento Fiscal
9 – Outros.
06 NUM_DOC Número do documento / processo / declaração ao qual o ajuste está C - - OC
vinculado, se houver
07 DESCR_AJ Descrição detalhada do ajuste, com citação dos documentos fiscais. C - - O
Observações:
Nível hierárquico - 4
Ocorrência – 1:N por Período
Campo 01 (REG) - Valor Válido: [E530]
Campo 02 (IND_AJ) - Valores válidos: [0, 1]
Campo 03 (VL_AJ) – Preenchimento: informar o valor dos ajustes lançados nos campos "outros débitos" ou "outros créditos",
cujos valores não foram destacados nos documentos fiscais, ou seja, o IPI não foi informado nos registros C100, C170 e C190,
exceto no caso de transferência de crédito de IPI.
Campo 04 (COD_AJ) - Validação: o valor informado no campo deve existir na Tabela de Ajustes da Apuração IPI, publicada
pela RFB (Instrução Normativa RFB nº 932, de 14/04/2009, atualizada pela IN RFB 1009/2010) e possuir a mesma natureza
do valor informado no campo 02 – IND_AJ:
Código Descrição Natureza Detalhamento
(*)
001 Estorno de débito C Valor do débito do IPI estornado
002 Crédito recebido por transferência C Valor do crédito do IPI recebidos por transferência, de outro(s)
estabelecimento(s) da mesma empresa
010 Crédito Presumido de IPI - C valor do crédito presumido de IPI decorrente do ressarcimento do
ressarcimento do PIS/Pasep e da PIS/Pasep e da Cofins nas operações de exportação de produtos
Cofins - Lei nº 9.363/1996 industrializados (Lei nº 9.363/1996, art. 1º)
011 Crédito Presumido de IPI - C valor do crédito presumido de IPI decorrente do ressarcimento do
ressarcimento do PIS/Pasep e da PIS/Pasep e da Cofins nas operações de exportação de produtos
Cofins - Lei nº 10.276/2001 industrializados (Lei nº 10.276/2001, art. 1º)
012 Crédito Presumido de IPI - regiões C valor do crédito presumido relativo ao IPI incidente nas saídas, do
incentivadas - Lei nº 9.826/1999 estabelecimento industrial, dos produtos classificados nas posições
8702 a 8704 da Tipi (Lei nº 9.826/1999, art. 1º)
013 Crédito Presumido de IPI - frete - C valor do crédito presumido de IPI relativamente à parcela do frete
MP 2.158/2001 cobrado pela prestação do serviço de transporte dos produtos
classificados nos códigos 8433.53.00, 8433.59.1, 8701.10.00,
8701.30.00, 8701.90.00, 8702.10.00 Ex 01, 8702.90.90 Ex 01,
8703, 8704.2, 8704.3 e 87.06.00.20, da TIPI (MP nº 2.158/2001,
art. 56)
019 Crédito Presumido de IPI - outros C outros valores de crédito presumido de IPI
098 Créditos decorrentes de medida C valores de crédito de IPI decorrentes de medida judicial
judicial
099 Outros créditos C Valor de outros créditos do IPI
101 Estorno de crédito D Valor do crédito do IPI estornado
102 Transferência de crédito D Valor do crédito do IPI transferido no período, para outro(s)
estabelecimento(s) da mesma empresa, conforme previsto na
legislação tributária.
103 Ressarcimento / compensação de D Valor do crédito de IPI, solicitado junto à RFB/MF
créditos de IPI
199 Outros débitos D Valor de outros débitos do IPI
(*) Natureza: "C" - Crédito; "D" - Débito
Campo 05 (IND_DOC) - Valores válidos: [0, 1, 2, 3, 9]
Campo 06 (NUM_DOC) – Preenchimento: informar, conforme o campo IND_DOC, o número do processo judicial,
administrativo, PER/DCOMP ou outros. Quando se tratar de ajuste de documento fiscal, deixar o campo vazio e discriminar
todos os documentos fiscais nos registros E531.
Campo 07 (DESCR_AJ) – Preenchimento: informar a descrição resumida do ajuste, incluindo, se for o caso, o período a que
se refere o ajuste, especialmente quando se tratar de períodos de apuração anteriores.
----
REGISTRO E531: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA APURAÇÃO DO IPI –
IDENTIFICAÇÃO DOS DOCUMENTOS FISCAIS (01 e 55)
Este registro tem por objetivo identificar os documentos fiscais relacionados ao ajuste.
Validação do Registro: este registro somente deverá ser informado quando o Campo IND_DOC do Registro E530
for igual a 3.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E531" C 004 - O
02 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - OC
- do emitente do documento ou do remetente das mercadorias, no
caso de entradas;
- do adquirente, no caso de saídas
03 COD_MOD Código do modelo do documento fiscal, conforme a Tabela 4.1.1 C 002* - O
04 SER Série do documento fiscal C 004 - OC
05 SUB Subsérie do documento fiscal N 003 - OC
06 NUM_DOC Número do documento fiscal N 009 - O
07 DT_DOC Data da emissão do documento fiscal N 008* - O
08 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC
09 VL_AJ_ITEM Valor do ajuste para a operação/item N - 02 O
10 CHV_NFE Chave da Nota Fiscal Eletrônica (modelo 55) N 044* - OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [E531]
Campo 02 (COD_PART) - Preenchimento: no caso de entrada, deve constar a informação referente ao emitente do documento
ou ao remetente das mercadorias ou serviços. No caso de saída, deve constar a informação referente ao destinatário. O valor
deve ter até 60 caracteres.
Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 (COD_MOD) - Valores Válidos: [01, 55]
Validação: o valor informado no campo deve existir na tabela de Documentos Fiscais do ICMS, conforme Item 4.1.1. da Nota
Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e suas alterações. – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 04 (SER) – Validação: campo de preenchimento obrigatório com três posições para NF-e, COD_MOD igual a “55”,
de emissão própria ou de terceiros. Se não existir Série para NF-e , informar 000.
Campo 06 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (DT_DOC) - Preenchimento: informar a data de emissão do documento fiscal, no formato “ddmmaaaa”, sem os
separadores de formatação.
Campo 08 (COD_ITEM) – Preenchimento: este campo só deve ser informado quando o ajuste se referir a um determinado
item/produto do documento.
Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
Campo 10 (CHV_NFE) - Preenchimento: informar a chave do documento eletrônico para documentos de COD_MOD igual
a 55.
Validação: A informação da chave é obrigatória quando o COD_MOD = “55”.
Será conferido o dígito verificador (DV) da chave do documento eletrônico. Será verificada a consistência da informação dos
campos NUM_DOC e SER com o número do documento e série contidos na chave do documento eletrônico.
----
REGISTRO E990: ENCERRAMENTO DO BLOCO E
Este registro destina-se a identificar o encerramento do bloco “E” e a informar a quantidade de linhas (registros)
existentes no bloco.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "E990" C 004 - O
02 QTD_LIN_E Quantidade total de linhas do Bloco E N - - O
Observações:
Nível hierárquico - 1
Ocorrência – um por Arquivo
Campo 01 (REG) - Valor Válido: [E990]
Campo 02 (QTD_LIN_E) - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios
registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco E é igual ao valor informado no campo QTD_LIN_E.
