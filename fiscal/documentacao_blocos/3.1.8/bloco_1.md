# Bloco 1 - Versão 3.1.8


REGISTRO 1001: ABERTURA DO BLOCO 1
Este registro deverá ser gerado para abertura do bloco 1 e indicará se há informações no bloco.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1001" C 004 - O
02 IND_MOV Indicador de movimento: N 001* - O
0- Bloco com dados informados;
1- Bloco sem dados informados
Observações:
Nível hierárquico – 1
Ocorrência - um por arquivo
Campo 01 (REG) - Valor Válido: [1001]
Campo 02 (IND_MOV) - Valores Válidos: [0, 1]
Validação: além dos registros de abertura e encerramento, sempre deve ser informado o registro 1010 (Obrigatoriedade de
Registros do Bloco 1).
----
REGISTRO 1010: OBRIGATORIEDADE DE REGISTROS DO BLOCO 1
Este registro deverá ser apresentado por todos os contribuintes. Caso a resposta seja “S”, o contribuinte está obrigado
à apresentação do registro respectivo. Se houver dispensa de apresentação do registro pela unidade federada, a resposta para o
campo específico do registro deverá ser “N”.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1010" C 004* - O
02 IND_EXP Reg. 1100 - Ocorreu averbação (conclusão) de exportação C 001* - O
no período:
S – Sim
N - Não
03 IND_CCRF Reg 1200 – Existem informações acerca de créditos de C 001* - O
ICMS a serem controlados, definidos pela Sefaz:
S – Sim
N - Não
04 IND_COMB Reg. 1300 – É comércio varejista de combustíveis com C 001* - O
movimentação e/ou estoque no período:
S – Sim
N - Não
05 IND_USINA Reg. 1390 – Usinas de açúcar e/álcool – O C 001* - O
estabelecimento é produtor de açúcar e/ou álcool
carburante com movimentação e/ou estoque no período:
S – Sim
N - Não
06 IND_VA Reg 1400 - Sendo o registro obrigatório em sua Unidade C 001* - O
de Federação, existem informações a serem prestadas
neste registro:
S – Sim;
N - Não
07 IND_EE Reg 1500 - A empresa é distribuidora de energia e ocorreu C 001* - O
fornecimento de energia elétrica para consumidores de
outra UF:
S – Sim;
N - Não
08 IND_CART Reg 1601 - Realizou vendas com instrumentos C 001* - O
eletrônicos de pagamento:
S – Sim;
N - Não
09 IND_FORM Reg. 1700 - Foram emitidos documentos fiscais em papel C 001* - O
no período em unidade da federação que exija o controle
de utilização de documentos fiscais:
S – Sim
N - Não
10 IND_AER Reg 1800 - A empresa prestou serviços de transporte aéreo C 001* - O
de cargas e de passageiros:
S – Sim
N - Não
11 IND_GIAF1 Reg. 1960 - Possui informações GIAF1? C 001* - O
S – Sim;
N – Não.
12 IND_GIAF3 Reg. 1970 - Possui informações GIAF3? C 001* - O
S – Sim;
N – Não.
13 IND_GIAF4 Reg. 1980 - Possui informações GIAF4? C 001* - O
S – Sim;
N – Não.
14 IND_REST_RESSARC Reg. 1250 – Possui informações consolidadas de saldos C 001* - O
_COMPL_ICMS de restituição, ressarcimento e complementação do
ICMS?
S – Sim;
N – Não.
Obs.: Até 31/12/2021 o campo 08 referiu-se ao registro 1600.
Nível hierárquico - 2
Ocorrência – 1
Campo 04 (IND_COMB) – Preenchimento: Se não houver movimentação e/ou estoque no período, informar Não.
Campo 05 (IND_USINA) – Preenchimento: Se não houver movimentação e/ou estoque no período, informar Não.
Campo 09 (IND_FORM) – Preenchimento: “S – Sim”, somente quando emitir documento fiscal em papel com autorização
de impressão.
Campos 11, 12 e 13 (IND_GIAFn) – Preenchimento: “S – Sim”, somente quando o estabelecimento informante for
domiciliado no estado de Pernambuco.
----
REGISTRO 1100: REGISTRO DE INFORMAÇÕES SOBRE EXPORTAÇÃO.
Este registro deve ser preenchido no mês em que se concluir a exportação direta ou indireta pelo efetivo exportador.
No caso de ocorrer mais de um Registro de Exportação (RE) para uma mesma Declaração de Exportação (DE), deve
ser informado um registro 1100 para cada RE.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “1100” C 004 - O
02 IND_DOC Informe o tipo de documento: N 001* - O
0 – Declaração de Exportação;
1 – Declaração Simplificada de Exportação;
2 – Declaração Única de Exportação.
03 NRO_DE Número da declaração C 014 - O
04 DT_DE Data da declaração (DDMMAAAA) N 008* - O
05 NAT_EXP Preencher com: N 001* - O
0 - Exportação Direta
1 - Exportação Indireta
06 NRO_RE Nº do registro de Exportação N 012 - OC
07 DT_RE Data do Registro de Exportação (DDMMAAAA) N 008* - OC
08 CHC_EMB Nº do conhecimento de embarque C 018 - OC
09 DT_CHC Data do conhecimento de embarque (DDMMAAAA) N 008* - OC
10 DT_AVB Data da averbação da Declaração de exportação (ddmmaaaa) N 008* - O
11 TP_CHC Informação do tipo de conhecimento de embarque: N 002* - O
01 – AWB;
02 – MAWB;
03 – HAWB;
04 – COMAT;
06 – R. EXPRESSAS;
07 – ETIQ. REXPRESSAS;
08 – HR. EXPRESSAS;
09 – AV7;
10 – BL;
11 – MBL;
12 – HBL;
13 – CRT;
14 – DSIC;
16 – COMAT BL;
17 – RWB;
18 – HRWB;
19 – TIF/DTA;
20 – CP2;
91 – NÂO IATA;
92 – MNAO IATA;
93 – HNAO IATA;
99 – OUTROS.
12 PAIS Código do país de destino da mercadoria (Preencher conforme N 003 - O
tabela do SISCOMEX)
Observações:
Nível hierárquico - 2
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1100]
Campo 02 (IND_DOC) – Preenchimento: quando for DE ou DDE, preencher com código 0.
Valores Válidos: [0, 1, 2]
Campo 03 (NRO_DE) – Preenchimento: as máscaras (caracteres especiais de formatação, tais como: ".", "/", "-", etc) não
devem ser informadas.
Campo 04 (DT_DE) - Preenchimento: informar a data da declaração no formato “ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 05 (NAT_EXP) - Valores Válidos: [0, 1]
Campo 06 (NRO_RE) – Preenchimento: este campo deve ser preenchido se o campo IND_DOC for “0” (zero).
Campo 07 (DT_RE) - Preenchimento: informar a data do registro de exportação no formato “ddmmaaaa”, sem separadores de formatação. Este campo deve ser preenchido se o campo IND_DOC for “0” (zero).
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 09 (DT_CHC) - Preenchimento: informar a data do conhecimento de embarque no formato “ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 10 (DT_AVB) - Preenchimento: informar a data da averbação da declaração de exportação no formato “ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 12 (PAIS) - Validação: O valor informado no campo deverá existir na tabela de Países do SISCOMEX, que corresponde aos segundo, terceiro e quarto dígitos da tabela BACEN, que possui cinco caracteres.
----
REGISTRO 1105: DOCUMENTOS FISCAIS DE EXPORTAÇÃO.
Este registro deve ser apresentado para discriminar os documentos fiscais vinculados à exportação.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1105" C 004 - O
02 COD_MOD Código do modelo da NF, conforme tabela 4.1.1 C 002* - O
03 SERIE Série da Nota Fiscal C 003 - OC
04 NUM_DOC Número de Nota Fiscal de Exportação emitida pelo Exportador N 009 - O
05 CHV_NFE Chave da Nota Fiscal Eletrônica N 044* - OC
06 DT_DOC Data da emissão da NF de exportação N 008* - O
07 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1105]
Campo 02 (COD_MOD) - Valores Válidos: [01, 55] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 04 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 05 (CHV_NFE) - Validação: se modelo da nota fiscal for 55, o campo é obrigatório e o dígito verificador da chave NF-e será validado.
Serão verificados a consistência da informação do campo NUM_DOC e o número do documento contido na chave da NF-e.
Campo 06 (DT_DOC) - Preenchimento: informar a data da emissão da nota fiscal de exportação no formato “ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 07 (COD_ITEM )- Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
----
REGISTRO 1110: OPERAÇÕES DE EXPORTAÇÃO INDIRETA – MERCADORIAS DE
TERCEIROS.
Este registro deve ser apresentado para informar a origem das mercadorias adquiridas para a exportação.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1110" C 004 - O
02 COD_PART Código do participante-Fornecedor da Mercadoria destinada à C 060 - O
exportação (campo 02 do Registro 0150)
03 COD_MOD Código do documento fiscal, conforme a Tabela 4.1.1 C 002* - O
O SER Série do documento fiscal recebido com fins específicos de C 004 - OC
04 exportação.
05 NUM_DOC Número do documento fiscal recebido com fins específicos de N 009 - O
exportação.
06 DT_DOC Data da emissão do documento fiscal recebido com fins específicos N 008* - O
de exportação
07 CHV_NFE Chave da Nota Fiscal Eletrônica N 044* - OC
08 NR_ MEMO Número do Memorando de Exportação N - - OC
09 QTD Quantidade do item efetivamente exportado. N - 03 O
10 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1110]
Campo 02 (COD_PART) - Validação: o valor fornecido deve estar no campo COD_PART do registro 0150.
Campo 03 (COD_MOD) - Valores Válidos: [01, 1B, 04, 55] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 05 (NUM_DOC) – Preenchimento: informar o número do documento fiscal emitido pelo participante para o
exportador.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 06 (DT_DOC) - Preenchimento: informar a data da emissão do documento fiscal no formato “ddmmaaaa”, sem
separadores de formatação.
Validação: o valor informado no campo deve ser uma data válida.
Campo 07 (CHV_NFE) – Preenchimento: informar a chave da NF-e emitida pelo participante para o exportador.
Validação: se o modelo da nota fiscal for 55, o campo é obrigatório. Serão verificados: o dígito verificador da chave de acesso,
o número do documento informado e o constante na chave.
Campo 08 (NR_ MEMO) - Preenchimento: informar o número do Memorando de Exportação, quando houver.
Campo 09 (QTD) - Validação: o valor informado no campo deve ser maior que “0” (zero)
Campo 10 (UNID) - Validação: o valor deve estar informado no registro 0190.
----
REGISTRO 1200: CONTROLE DE CRÉDITOS FISCAIS - ICMS.
Este registro demonstra a conta-corrente dos créditos fiscais de ICMS, controlados extra-apuração. Cada UF
determinará a obrigatoriedade de apresentação deste registro.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1200" C 004 - O
02 COD_AJ_APUR Código de ajuste, conforme informado na Tabela indicada no C 008* - O
item 5.1.1.
03 SLD_CRED Saldo de créditos fiscais de períodos anteriores N - 02 O
04 CRED_APR Total de crédito apropriado no mês N - 02 O
05 CRED_RECEB Total de créditos recebidos por transferência N - 02 O
06 CRED_UTIL Total de créditos utilizados no período N - 02 O
Saldo de crédito fiscal acumulado a transportar para o período N - 02 O
07 SLD_CRED_FIM
seguinte
Observações:
Nível hierárquico - 2
Ocorrência – 1:N
Campo 01(REG) - Valor Válido: [1200]
Campo 02 (COD_AJ_APUR) - Validação: O valor informado deve existir na Tabela 5.1.1 (Tabela de Códigos de Ajustes da
Apuração do ICMS) da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e suas alterações, que discrimina os
códigos de ajustes previstos pelos Estados para a apuração do ICMS.
A partir de janeiro de 2013, somente poderão ser utilizados os códigos nos quais o quarto caractere seja igual a “9”.
Campo 04 (CRED_APR) – Preenchimento: o valor a ser informado neste campo corresponde ao valor do crédito fiscal que
o contribuinte apropriou no período, exceto os recebidos por transferência que deverão ser informados no campo 5.
Campo 05 (CRED_RECEB) - Preenchimento: informar o valor total de créditos recebidos por transferência, no período, entre
estabelecimentos, mesmo que de terceiros.
Campo 06 (CRED_UTIL) – Preenchimento: o valor a ser informado neste campo corresponde ao valor total dos créditos
utilizados no período, que aparecem de forma detalhada nos registros 1210.
Validação: o valor informado neste campo deve ser igual ao somatório do campo VL_CRED_UTIL do registro 1210.
Campo 07 (SLD_CRED_FIM) – Preenchimento: informar o valor do saldo de crédito fiscal após a utilização (informado nos
registros 1210) no período, saldo este a ser transportado para o período seguinte. Este valor representa a soma dos campos
SLD_CRED, CRÉD_APR e CRED_RECEB, menos o campo CRED_UTIL.
Validação: o valor desse campo deve ser igual à soma dos valores dos campos SLD_CRED, CRED_APR e CRED_RECEB, diminuída do valor do campo CRED_UTIL.
----
REGISTRO 1210: UTILIZAÇÃO DE CRÉDITOS FISCAIS – ICMS.
Este registro deve ser apresentado para detalhar a utilização de créditos fiscais de ICMS no período. O somatório dos
valores do campo 04 deste registro deve corresponder ao informado no campo 06 do registro 1200.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1210" C 004 - O
02 TIPO_UTIL Tipo de utilização do crédito, conforme tabela indicada no C 004* - O
item 5.5.
03 NR_DOC Número do documento utilizado na baixa de créditos C - - OC
04 VL_CRED_UTIL Total de crédito utilizado N - 02 O
05 CHV_DOCe Chave do Documento Eletrônico N 044* - OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [1210]
Campo 02 (TIPO_UTIL) - Validação: o valor informado deve estar de acordo com a tabela publicada pela UF do informante
do arquivo. Em caso de não publicação, pela UF, a tabela a ser informada é a constante no item 5.5 da Nota Técnica, instituída
pelo Ato COTEPE/ICMS nº 44/2018 e suas alterações, constante também da subseção 1.5 deste guia.
Campo 04 (VL_CRED_UTIL) - Preenchimento: informar o total de crédito utilizado para esta situação, que é definida pelo
campo TIPO_UTIL deste registro.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 05 (CHV_DOCe) - Preenchimento: informar a chave da NF-e, para documentos de COD_MOD igual a “55”, ou informar a chave do conhecimento de transporte eletrônico, para documentos de COD_MOD igual a “57” ( a partir de 01/01/2017) ou igual a “67” (a partir de 01/04/2017)
Validação: quando se tratar de NF-e, CT-e ou CT-e OS, é conferido o dígito verificador (DV) da chave do documento eletrônico. Será verificada a consistência da informação do campo NR_DOC com o número do documento contido na chave do documento eletrônico.
----
REGISTRO 1250: INFORMAÇÕES CONSOLIDADAS DE SALDOS DE RESTITUIÇÃO,
RESSARCIMENTO E COMPLEMENTAÇÃO DO ICMS
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1250” C 004 - O
02 VL_CREDITO_ICMS_OP Informar o valor total do ICMS operação própria que o N - 02 O
informante tem direito ao crédito, na forma prevista na
legislação, referente às hipóteses de restituição em que há
previsão deste crédito.
03 VL_ICMS_ST_REST Informar o valor total do ICMS ST que o informante tem N - 02 O
direito ao crédito, na forma prevista na legislação, referente
às hipóteses de restituição em que há previsão deste crédito.
04 VL_FCP_ST_REST Informar o valor total do FCP_ST agregado ao valor do N - 02 O
ICMS ST informado no campo “VL_ICMS_ST_REST”.
05 VL_ICMS_ST_COMPL Informar o valor total do débito referente ao complemento do N - 02 O
imposto, nos casos previstos na legislação.
06 VL_FCP_ST_COMPL Informar o valor total do FCP_ST agregado ao valor N - 02 O
informado no campo “VL_ICMS_ST_COMPL”
Observações:
Nível hierárquico – 2
Ocorrência 1:1
Campo 01 (REG) - Valor Válido: [1250]
Campo 02 (VL_CREDITO_ICMS_OP) – Validação: o valor informado no campo deve corresponder à soma dos campos “VL_CREDITO_ICMS_OP_MOT” dos registros 1255.
Campo 03 (VL_ICMS_ST_REST) – Validação: o valor informado no campo deve corresponder à soma dos campos “VL_ICMS_ST_REST_MOT” dos registros 1255.
Campo 04 (VL_FCP_ST_REST) – Validação: o valor informado no campo deve corresponder à soma dos campos “VL_FCP_ST_REST_MOT” dos registros 1255.
Campo 05 (VL_ICMS_ST_COMPL) – Validação: o valor informado no campo deve corresponder à soma dos campos “VL_ICMS_ST_COMPL_MOT” dos registros 1255.
Campo 06 (VL_FCP_ST_COMPL) – Validação: o valor informado no campo deve corresponder à soma dos campos “VL_FCP_ST_COMPL_MOT” dos registros 1255.
-----
REGISTRO 1255: INFORMAÇÕES CONSOLIDADAS DE SALDOS DE RESTITUIÇÃO,
RESSARCIMENTO E COMPLEMENTAÇÃO DO ICMS POR MOTIVO
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte. A chave do
registro é o campo 02 (COD_MOT_REST_COMPL).
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “1255” C 004 - O
02 COD_MOT_REST_COMPL Código do motivo da restituição ou complementação C 005* 02 O
conforme Tabela 5.7
03 VL_CREDITO_ICMS_OP_MOT Informar o valor total do ICMS operação própria que o N - 02 O
informante tem direito ao crédito, na forma prevista na
legislação, referente às hipóteses de restituição em que
há previsão deste crédito, para o mesmo
“COD_MOT_REST_COMPL”
04 VL_ICMS_ST_REST_MOT Informar o valor total do ICMS ST que o informante N - 02 O
tem direito ao crédito, na forma prevista na legislação,
referente às hipóteses de restituição em que há previsão
deste crédito, para o mesmo
“COD_MOT_REST_COMPL”
05 VL_FCP_ST_REST_MOT Informar o valor total do FCP_ST agregado ao valor do N - 02 O
ICMS ST informado no campo
“VL_ICMS_ST_REST_MOT”
06 VL_ICMS_ST_COMPL_MOT Informar o valor total do débito referente ao N - 02 O
complemento do imposto, nos casos previstos na
legislação, para o mesmo
“COD_MOT_REST_COMPL”
07 VL_FCP_ST_COMPL_MOT Informar o valor total do FCP_ST agregado ao valor N - 02 O
informado no campo “VL_ICMS_ST_COMPL_MOT”
Observações:
Nível hierárquico – 3
Ocorrência 1:N
Campo 01 (REG) - Valor Válido: [1255]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo.
Campo 04 (VL_ICMS_ST_REST_MOT) – Validação: o valor informado no campo deve corresponder à soma dos campos
VL_UNIT_ICMS_ST_CONV_REST multiplicados pelo campo QUANT_CONV dos registros C181, C185, C330, C380,
C430, C480, C815 e C880 para cada código informado no campo COD_MOT_REST_COMPL.
Campo 05 (VL_FCP_ST_REST_MOT) – Validação: o valor informado no campo deve corresponder à soma dos campos
VL_UNIT_FCP_ST_CONV_REST multiplicados pelo campo QUANT_CONV dos registros C181, C185, C330, C380, C430,
C480, C815 e C880 para cada código informado no campo COD_MOT_REST_COMPL.
Campo 06 (VL_ICMS_ST_COMPL_MOT) – Validação: o valor informado no campo deve corresponder à soma dos campos
VL_UNIT_ICMS_ST_CONV_COMPL multiplicados pelo campo QUANT_CONV dos registros C181, C185, C330, C380,
C430, C480, C815 e C880 para cada código informado no campo COD_MOT_REST_COMPL.
Campo 07 (VL_FCP_ST_COMPL_MOT) – Validação: o valor informado no campo deve corresponder à soma dos campos
VL_UNIT_FCP_ST_CONV_COMPL multiplicados pelo campo QUANT_CONV dos registros C181, C185, C330, C380,
C430, C480, C815 e C880 para cada código informado no campo COD_MOT_REST_COMPL.
----
REGISTRO 1300: MOVIMENTAÇÃO DIÁRIA DE COMBUSTÍVEIS
Este registro deve ser apresentado pelos contribuintes do ramo varejista de combustíveis (postos de combustíveis),
para apresentar informações sobre a movimentação diária de combustíveis (Portaria DNC Nº 26, de 13/11/92, instituiu o LIVRO
DE MOVIMENTAÇÃO DE COMBUSTÍVEIS (LMC), pelo Posto Revendedor (PR), dos estoques e das movimentações de
compra e venda de gasolinas, óleo diesel, querosene iluminante, álcool etílico hidratado carburante e mistura óleo
diesel/biodiesel especificada pela ANP).
Deve ser informado apenas um registro por tipo de combustível e por data do fechamento da movimentação (campo
COD_ITEM e campo DT_FECH), independentemente de ocorrerem intervenções. Não pode haver mais de um registro com o
mesmo código de combustível e mesma data de fechamento.
Obs.: Não há previsão no livro para controle do GNV.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1300" C 004 - O
02 COD_ITEM Código do Produto, constante do registro 0200 C 060 - O
03 DT_FECH Data do fechamento da movimentação N 008* - O
04 ESTQ_ABERT Estoque no início do dia, em litros N - 03 O
05 VOL_ENTR Volume Recebido no dia (em litros) N - 03 O
06 VOL_DISP Volume Disponível (04 + 05), em litros N - 03 O
07 VOL_SAIDAS Volume Total das Saídas, em litros N - 03 O
08 ESTQ_ESCR Estoque Escritural (06 – 07), litros N - 03 O
09 VAL_AJ_PERDA Valor da Perda, em litros N - 03 O
10 VAL_AJ_GANHO Valor do ganho, em litros N - 03 O
11 FECH_FISICO Estoque de Fechamento, em litros N - 03 O
Observações:
Nível hierárquico – 2
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1300]
Campo 02 (COD_ITEM) - Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
Campo 03 (DT_FECH) - Preenchimento: informar a data da movimentação no formato “ddmmaaaa”, sem separadores de
formatação.
Validação: o valor informado no campo deve ser uma data válida.A data informada deve ser maior ou igual ao campo DT_INI
do registro 0000 e menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 04 (ESTQ_ABERT) - Preenchimento: informar o estoque do início do dia, mesmo que tenha ocorrido intervenção
posterior.
Campo 05 (VOL_ENTR )- Preenchimento: informar o volume de combustível recebido no dia da movimentação (registro
C171).
Campo 06 (VOL_DISP) - Preenchimento: informar o volume disponível, que corresponde à soma dos campos
ESTQ_ABERT e VOL_ENTR.
Campo 07 (VOL_SAIDAS) - Preenchimento: informar o volume (em litros) total das saídas, que corresponde à soma dos
registros de volume de vendas.
Campo 08 (ESTQ_ESCR) - Preenchimento: informar o estoque escritural, que corresponde ao valor constante no campo
VOL_DISP menos o valor constante no campo VOL_SAIDAS.
Campo 11 (FECH_FISICO) - Preenchimento: informar o estoque do fim do dia.
----
REGISTRO 1310: MOVIMENTAÇÃO DIÁRIA DE COMBUSTÍVEIS POR TANQUE
Este registro deve ser apresentado para informar a movimentação diária por tanque. Não pode haver mais de um
registro com o mesmo número de tanque.
Obs.: Nos casos em que dois ou mais tanques de combustíveis estiverem interligados ou a saída deles passe por um
único filtro de combustível, de forma que não seja possível identificar qual tanque alimentou um determinado “Bico”, os valores
dos tanques deverão ser agrupados (somados), como se fossem um único tanque e informados em um único registro 1310.
Neste caso, o campo NUM_TANQUE deverá, sempre, conter o número de um dos tanques, que deve ser referenciado no
registro 1370.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1310" C 004 - O
02 NUM_TANQUE Tanque que armazena o combustível. C 003 - O
03 ESTQ_ABERT Estoque no início do dia, em litros N - 03 O
04 VOL_ENTR Volume Recebido no dia (em litros) N - 03 O
05 VOL_DISP Volume Disponível (03 + 04), em litros N - 03 O
06 VOL_SAIDAS Volume Total das Saídas, em litros N - 03 O
07 ESTQ_ESCR Estoque Escritural(05 – 06), litros N - 03 O
08 VAL_AJ_PERDA Valor da Perda, em litros N - 03 O
09 VAL_AJ_GANHO Valor do ganho, em litros N - 03 O
10 FECH_FISICO Volume aferido no tanque, em litros. Estoque de fechamento N - 03 O
físico do tanque.
Observações:
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1310]
Campo 03 (ESTQ_ABERT) - Preenchimento: informar o estoque do início do dia para o tanque especificado no campo
NUM_TANQUE, mesmo que tenha ocorrido intervenção posterior na bomba.
Campo 04 (VOL_ENTR) - Preenchimento: o valor fornecido deve corresponder ao volume de combustível informado nos
documentos fiscais (registro C171), especificado por tanque, para o dia da movimentação.
Campo 05 (VOL_DISP) - Preenchimento: informar o volume disponível, que corresponde à soma dos campos
ESTQ_ABERT e VOL_ENTR, para o tanque especificado no campo NUM_TANQUE.
Campo 06 (VOL_SAIDAS) - Preenchimento: informar o volume (em litros) total das saídas, que corresponde à soma dos
registros de volume de vendas, para o tanque especificado no campo NUM_TANQUE.
Campo 07 (ESTQ_ESCR) - Preenchimento: informar o estoque escritural, que corresponde ao valor constante no campo VOL_DISP menos o valor constante no campo VOL_SAIDAS, para o tanque especificado no campo NUM_TANQUE.
Campo 10 (FECH_FISICO) - Preenchimento: informar o estoque do fim do dia para o tanque especificado no campo NUM_TANQUE.
Validação: A soma dos valores apresentados no campo 10 do registro 1310 deve ser igual ao valor apresentado no campo 11 do registro 1300.
----
REGISTRO 1320: VOLUME DE VENDAS
Este registro deve ser apresentado para discriminar o volume das vendas no dia, considerando-se vendas todas as saídas promovidas
a qualquer título. Não havendo intervenção, em princípio, haverá apenas um registro por bico e os campos NR_INTERV, MOT_INTERV,
NOM_INTERV, CNPJ_INTERV e CPF_INTERV estarão sem informação. Para cada intervenção ocorrida na bomba associada ao bico, um
novo registro deve ser preenchido com dados da intervenção e os valores totalizados desde a intervenção até uma próxima intervenção ou o
fim do dia.
Obs.: No caso em que o contador atingir o seu valor máximo de leitura, deverão ser informados dois registros 1320: o primeiro,
informando o valor da leitura inicial até o valor máximo de leitura do contador, e o segundo registro informando como valor inicial de leitura
o valor ZERO e informar o valor da leitura final.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1320" C 004 - O
02 NUM_BICO Bico Ligado à Bomba N - - O
03 NR_INTERV Número da intervenção N - - OC
04 MOT_INTERV Motivo da Intervenção C 050 - OC
05 NOM_INTERV Nome do Interventor C 030 - OC
06 CNPJ_INTERV CNPJ da empresa responsável pela intervenção N 014* - OC
07 CPF_INTERV CPF do técnico responsável pela intervenção N 011* - OC
08 VAL_FECHA Valor da leitura final do contador, no fechamento do bico. N - 03 O
09 VAL_ABERT Valor da leitura inicial do contador, na abertura do bico. N - 03 O
10 VOL_AFERI Aferições da Bomba, em litros N - 03 OC
11 VOL_VENDAS Vendas (08 – 09 - 10 ) do bico , em litros N - 03 O
Observações:
Nível hierárquico – 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1320]
Campo 02 (NUM_BICO) - Preenchimento: informar o número do bico associado ao tanque do respectivo registro pai.
Campo 03 (NR_INTERV) - Preenchimento: numeração atribuída à intervenção pelo órgão competente ou, na falta deste, um
número sequencial criado pelo próprio declarante. Se não ocorrer intervenção no bico, este campo não deverá ser preenchido.
Campo 04 (MOT_INTERV) – Preenchimento: nome da empresa responsável pela intervenção. Se não ocorrer intervenção
no bico, este campo não deverá ser preenchido.
Campo 05 (NOM_INTERV )- Preenchimento: NOM_INTERV: nome do técnico autorizado (mecânico) pelo INMETRO
(por meio de suas unidades estaduais) para atuar em manutenção de bombas medidoras de combustível (a autorização é
específica para essas). Se não ocorrer intervenção no bico, este campo não deverá ser preenchido.
Campo 06 (CNPJ_INTERV) – Preenchimento: CNPJ_INTERV: CNPJ da empresa responsável pelo contrato de manutenção, para quem o
técnico autorizado trabalha (quando houver). Se não ocorrer intervenção no bico, este campo não deverá ser preenchido.
Campo 07 (CPF_INTERV) - Preenchimento: CPF_INT ERV: CPF do técnico autorizado (mecânico), vinculado ao campo
[NOM_INTERV]. Se não ocorrer intervenção no bico, este campo não deverá ser preenchido.
Campo 08 (VAL_FECHA) - Preenchimento: fornecer a leitura final do contador (encerrante), no momento do fechamento.
O valor é o do contador.
Campo 09 (VAL_ABERT) - Preenchimento: fornecer a leitura inicial do contador (encerrante), no momento da abertura. O
valor é o do contador.
Campo 10 (VOL_AFERI) - Preenchimento: informar o volume, em litros, relativo às aferições efetuadas.
Campo 11 (VOL_VENDAS) - Preenchimento: informar o volume de vendas por bico, ligado ao tanque, que corresponde ao
valor fornecido no campo VAL_FECHA menos a soma do campo VAL_ABERT com o campo VOL_AFERI.
----
REGISTRO 1350: BOMBAS
Este registro deve ser apresentado para discriminar as bombas pertencentes ao varejista.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1350" C 004 - O
02 SERIE Número de Série da Bomba C - - O
03 FABRICANTE Nome do Fabricante da Bomba C 060 - O
04 MODELO Modelo da Bomba C - - O
05 TIPO_MEDICAO Identificador de medição: C 001 - O
0 – analógico
1 – digital
Observações:
Nível hierárquico – 2
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido [1350]
Campo 05 (TIPO_MEDICAO) - Valores Válidos: [0, 1]
----
REGISTRO 1360: LACRES DA BOMBA
Este registro deve ser apresentado para discriminar os lacres aplicados à bomba referenciada no registro pai.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1360" C 004 - O
02 NUM_LACRE Número do Lacre associado na Bomba C 020 - O
03 DT_APLICACAO Data de aplicação do Lacre N 008* - O
Observações: Informar um registro para cada lacre existente na bomba.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1360]
Campo 03 (DT_APLICACAO) - Preenchimento: informar a data de aplicação do lacre no formato “ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser uma data válida.
----
REGISTRO 1370: BICOS DA BOMBA
Este registro deve ser apresentado para discriminar os bicos pertencentes à bomba referenciada no registro pai.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1370" C 004 - O
02 NUM_BICO Número sequencial do bico ligado a bomba N 003 - O
03 COD_ITEM Código do Produto, constante do registro 0200 C 060 - O
04 NUM_TANQUE Tanque que armazena o combustível. C 003 - O
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido [1370]
Campo 02 (NUM_BICO) - Preenchimento: caso o tanque não esteja ligado a bicos de bomba, servindo apenas como
reservatório de combustível para as demais bombas, informar código “990” em diante.
Campo 03 (COD_ITEM) - Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
----
REGISTRO 1390: CONTROLE DE PRODUÇÃO DE USINA
Este registro deve ser apresentado pelos fabricantes de açúcar e álcool (Usinas) para controle de produção.
Validação do Registro: Não pode haver mais de um registro com o mesmo código de produto. Obs.: O registro somente poderá
ser informado em períodos de apuração posteriores a julho de 2012.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1390" C 004 - O
02 COD_PROD Código do produto conforme tabela 5.8 N 002* - O
Observações:
Nível hierárquico - 2
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [1390]
Campo 02 (COD_PROD) - Preenchimento: o valor informado no campo deve existir na tabela 5.8 de cada Secretaria de Fazenda, conforme a UF do declarante, campo UF do registro 0000 ou, não havendo esta tabela, o valor informado no campo deve existir na tabela 5.8 genérica.
----
REGISTRO 1391: PRODUÇÃO DIÁRIA DA USINA
Este registro deve ser apresentado para detalhar a produção diária de cada produto especificado no registro 1390.
Validação do Registro: Não pode haver mais de um registro com o mesmo código de item COD_ITEM para a mesma data de
produção DT_REGISTRO.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1391" C 004 - O
02 DT_REGISTRO Data de produção (DDMMAAAA) C 008* - O
03 QTD_MOID Quantidade de insumo esmagado (toneladas) N - 02 OC
04 ESTQ_INI Estoque inicial (litros / kg) N - 02 O
05 QTD_PRODUZ Quantidade produzida (litros / kg) N - 02 OC
06 ENT_ANID_HID Entrada de álcool anidro decorrente da transformação do N - 02 OC
álcool hidratado ou
Entrada de álcool hidratado decorrente da transformação
do álcool anidro (litros)
07 OUTR_ENTR Outras entradas (litros / kg) N - 02 OC
08 PERDA Evaporação (litros) ou Quebra de peso (kg) N - 02 OC
09 CONS Consumo (litros) N - 02 OC
10 SAI_ANI_HID Saída para transformação (litros). N - 02 OC
11 SAÍDAS Saídas (litros / kg) N - 02 OC
12 ESTQ_FIN Estoque final (litros / kg) N - 02 O
13 ESTQ_INI_MEL Estoque inicial de mel residual (kg) N - 02 OC
14 PROD_DIA_MEL Produção de mel residual (kg) e entradas de mel (kg) N - 02 OC
15 UTIL_MEL Mel residual utilizado (kg) e saídas de mel (kg) N - 02 OC
16 PROD_ALC_MEL Produção de álcool (litros) ou açúcar (kg) proveniente N - 02 OC
do mel residual.
17 OBS Observações C - - OC
18 COD_ITEM Informar o insumo conforme código do item (campo 02 C 060 - O
do Registro 0200)
19 TP_RESIDUO Tipo de resíduo produzido: N 002* - O
01 - Bagaço de cana
02 - DDG
03 – WDG
04 – (DDG + WDG)
20 QTD_RESIDUO Quantidade de resíduo produzido (toneladas) N - 02 O
21 QTD_RESIDUO_ DDG Quantidade de resíduo produzido de DDG (toneladas) N - 02 O
22 QTD_RESIDUO_ WDG Quantidade de resíduo produzido de WDG (toneladas) N - 02 O
23 QTD_RESIDUO_ Quantidade de resíduo produzido de bagaço de cana N - 02 O
CANA (toneladas)
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [1391]
Campo 02 (DT_REGISTRO) - Preenchimento: informar a data da produção, no formato “ddmmaaaa”, excluindo-se quaisquer
caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 03 (QTD_MOID) - Preenchimento: informar a quantidade total (toneladas) de insumo esmagado para fabricação do
produto especificado no registro 1390.
Campo 04 (ESTQ_INI) - Preenchimento: informar o estoque inicial do dia. O valor apresentado será em litros, se o
COD_PROD do registro 1390 for igual a 01 ou 02 (Álcool) e em quilogramas, se for igual a 03 (Açúcar).
Campo 05 (QTD_PRODUZ) - Preenchimento: informar a quantidade produzida. O valor apresentado será em litros, se o
COD_PROD do registro 1390 for igual a 01 ou 02 (Álcool) e em quilogramas, se for igual a 03(Açúcar).
Campo 06 (ENT_ANID_HID) - Preenchimento: informar a quantidade (litros) de álcool anidro resultante da transformação
do álcool hidratado (Se COD_PROD do registro 1390 for igual a 02) ou a quantidade (litros) de álcool hidratado resultante da
transformação do álcool anidro (Se COD_PROD do registro 1390 for igual a 01).
Validação: Deverá ser preenchido apenas se o COD_PROD do registro 1390 for igual a 01 ou 02.
Campo 07 (OUTR_ENTR) - Preenchimento: informar a quantidade de produto recebido de terceiros, devoluções e outras
entradas não especificadas. O valor apresentado será em litros, se o COD_PROD do registro 1390 for igual a 01 ou 02 (Álcool)
e em quilogramas, se for igual a 03 (Açúcar).
Campo 08 (PERDA) - Preenchimento: informar o total das perdas por evaporação (litros) no caso do álcool ou o total da
quebra de peso (kg) para o açúcar.
Campo 09 (CONS) - Preenchimento: informar a quantidade total (litros ou kg) utilizada para consumo próprio, conforme
produto especificado no campo 02 do registro 1390.
Campo 10 (SAI_ANI_HID) - Preenchimento: informar a quantidade (litros) de álcool anidro utilizada para transformação em
álcool hidratado (se campo 02 do registro 1390 for igual a 02) ou a quantidade (litros) de álcool hidratado utilizada para
transformação em álcool anidro (se campo 02 do registro 1390 for igual a 01).
Campo 11 (SAÍDAS) - Preenchimento: informar a quantidade total das saídas (litros ou kg).
Campo 12 (ESTQ_FIN) - Preenchimento: informar o estoque final do dia (litros ou kg).
Campo 13 (ESTQ_INI_MEL) – Preenchimento: informar a quantidade (kg) do estoque inicial de mel residual.
Validação: Deverá ser preenchido apenas se o campo 02 do registro 1390 for igual a 03 (Açúcar).
Campo 14 (PROD_DIA_MEL) – Preenchimento: informar a quantidade (kg) de todas as entradas de mel residual. Devem
ser consideradas a quantidade produzida e as demais entradas.
Validação: Deverá ser preenchido apenas se o campo 02 do registro 1390 for igual a 03 (Açúcar).
Campo 15 (UTIL_MEL) – Preenchimento: informar a quantidade (kg) de mel residual utilizado na produção e as demais
saídas.
Validação: Deverá ser preenchido apenas se o campo 02 do registro 1390 for igual a 03 (Açúcar).
Campo 16 (PROD_ALC_MEL) – Preenchimento: informar a quantidade de álcool produzida (litros) ou açúcar (kg) a partir
da utilização de mel residual.
Campo 18 (COD_ITEM) - Preenchimento: informar o insumo utilizado conforme códigos próprios do informante do
arquivo. Validação: O valor informado neste campo deve existir no registro 0200.
Campo 19 (TP_RESIDUO) – Informar o tipo de resíduo. Valores válidos: [01, 02, 03, 04].
Observação:
DDG – Dry distillers grain (resíduo seco)
WDG – Wet distillers grain (resíduo úmido)
Campo 20 (QTD_RESIDUO) – Preenchimento: Informar a quantidade de resíduo produzido (toneladas) resultante do
processo de produção.
Validação: o valor desse campo deve corresponder à soma dos campos 21 (QTD_RESIDUO_ DDG), 22 (QTD_RESIDUO_
WDG) e 23 (QTD_RESIDUO_ CANA).
Campo 21 (QTD_RESIDUO_ DDG) – Informar a quantidade de resíduo produzido de DDG (toneladas).
Observação:
DDG – Drydistillersgrain (resíduo seco)
Validação: O valor não pode ser maior que zero quando o campo 19 (TP_RESIDUO) for preenchido com os valores 01 ou
03.
Campo 22 (QTD_RESIDUO_ WDG) – Informar a quantidade de resíduo produzido de WDG (toneladas).
Observação:
WDG – Wet distillers grain (resíduo úmido)
Validação: O valor não pode ser maior que zero quando o campo 19 (TP_RESIDUO) for preenchido com os valores 01 ou
02.
Campo 23 (QTD_RESIDUO_ CANA) – Informar a quantidade de resíduo produzido de bagaço de cana. (toneladas).
Validação: O valor não pode ser maior que zero quando o campo 19 (TP_RESIDUO) for preenchido com os valores 02, 03
ou 04.
----
REGISTRO 1400: INFORMAÇÃO SOBRE VALORES AGREGADOS
Este registro tem como objetivo fornecer informações para o cálculo do valor adicionado por município, sendo
utilizado para subsidiar cálculos de índices de participação e deve ser apresentado apenas se a unidade federada do declarante
ou onde o declarante tenha inscrição de substituto tributário assim o exigir.
Deve ser preenchido pelos contribuintes conforme definido pela Secretaria de Fazenda de localização do
estabelecimento ou em que possua inscrição de substituto tributário.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1400" C 004 - O
02 COD_ITEM_IPM Código do item (Tabela 5.9.1 de Itens UF Índice de Participação C 060 - O
dos Municípios ou Tabela 5.9.2 de Itens UF_ST Índice de
participação dos Municípios) ou campo 02 do Registro 0200
03 MUN Código do Município de origem/destino N 007* - O
04 VALOR Valor mensal correspondente ao município N - 2 O
Observações: Tabela 5.9.1 de Itens UF Índice de Participação dos Municípios, se existir, válida a partir de 2015 ou Tabela
5.9.2 de Itens UF_ST Índice de participação dos Municípios, se existir.
Nível hierárquico - 2
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1400]
Campo 02 (COD_ITEM_IPM) - Preenchimento: Consulte a Secretaria de Fazenda de cada UF quanto ao município a ser
informado.
Validação:
a) Se o município no campo 03 (MUN) pertencer à UF informada no campo 09 do Registro 0000, o código informado deve
existir na Tabela 5.9.1 de Itens UF Índice de Participação dos Municípios, ou deve existir no campo COD_ITEM do registro
0200.
b) Se o município no campo 03 (MUN) pertencer a uma UF informada no campo 02 do Registro 0015, a Tabela 5.9.2 de Itens
UF_ST Índice de participação dos Municípios dessa UF deve conter o código informado.
Campo 03 (MUN) – Preenchimento: regras para os contribuintes obrigados, conforme definido pela Secretaria de Fazenda de
cada UF.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos. O município deve
pertencer:
a) à UF informada no campo 09 do Registro 0000 ou
b) a uma UF informada no campo 02 do Registro 0015.
Campo 04 (VALOR) – Preenchimento: Consulte a Secretaria de Fazenda de cada UF quanto aos valores a serem informados.
Validação: o valor informado no campo deve ser maior que “0” (zero). Se o valor for negativo ou zero, o contribuinte não deve
prestar a informação no mês.
----
REGISTRO 1500: NOTA FISCAL/CONTA DE ENERGIA ELÉTRICA (CÓDIGO 06) –
OPERAÇÕES INTERESTADUAIS.
Este registro deve ser apresentado, nas operações de saída interestaduais, pelos contribuintes do segmento de energia
elétrica, obrigados ao Convênio 115/2003.
Para apresentação do registro 1500 e filhos devem ser observadas as exceções abaixo relacionadas:
Exceção 1: Notas Fiscais Complementares e Notas Fiscais Complementares Extemporâneas (campo COD_SIT igual a “06” ou
“07”): nesta situação, somente os campos REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD, COD_SIT, SER, SUB,
NUM_DOC e DT_DOC são obrigatórios. Os demais campos são facultativos (se forem preenchidos, serão validados e
aplicadas as regras de campos existentes). Os registros filhos do registro 1500 deverão ser informados, se existirem.
Exceção 2: Notas Fiscais emitidas por regime especial ou norma específica (campo COD_SIT igual a “08”). Para documentos
fiscais emitidos com base em regime especial ou norma específica, deverá ser apresentado o registro 1500, obrigatoriamente,
e os registros “filhos”, se estes forem exigidos pela legislação fiscal. Nesta situação, somente os campos REG, IND_OPER,
IND_EMIT, COD_PART, COD_MOD, COD_SIT, SER, SUB, NUM_DOC e DT_DOC são obrigatórios. Os demais campos
são facultativos (se forem preenchidos, serão validados e aplicadas as regras de campos existentes).
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "1500" C 004 - O
02 IND_OPER Indicador do tipo de operação: C 001* - O
1- Saída
03 IND_EMIT Indicador do emitente do documento fiscal: C 001* - O
0- Emissão própria;
04 COD_PART Código do participante (campo 02 do Registro C 060 - O
0150):
- do adquirente, no caso das saídas.
05 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - O
Tabela 4.1.1
06 COD_SIT Código da situação do documento fiscal, conforme a N 002* - O
Tabela 4.1.2
07 SER Série do documento fiscal C 004 - OC
08 SUB Subsérie do documento fiscal N 003 - OC
09 COD_CONS Código de classe de consumo de energia elétrica: C 002* - O
01 - Comercial
02 - Consumo Próprio
03 - Iluminação Pública
04 - Industrial
05 - Poder Público
06 - Residencial
07 - Rural
08 - Serviço Público
10 NUM_DOC Número do documento fiscal N 009 - O
11 DT_DOC Data da emissão do documento fiscal N 008* - O
12 DT_E_S Data da entrada ou da saída N 008* - O
13 VL_DOC Valor total do documento fiscal N - 02 O
14 VL_DESC Valor total do desconto N - 02 OC
15 VL_FORN Valor total fornecido/consumido N - 02 O
16 VL_SERV_NT Valor total dos serviços não-tributados pelo ICMS N - 02 OC
17 VL_TERC Valor total cobrado em nome de terceiros N - 02 OC
18 VL_DA Valor total de despesas acessórias indicadas no N - 02 OC
documento fiscal
19 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS N - 02 OC
20 VL_ICMS Valor acumulado do ICMS N - 02 OC
21 VL_BC_ICMS_ST Valor acumulado da base de cálculo do ICMS N - 02 OC
substituição tributária
22 VL_ICMS_ST Valor acumulado do ICMS retido por substituição N - 02 OC
tributária
23 COD_INF Código da informação complementar do documento C 006 - OC
fiscal (campo 02 do Registro 0450)
24 VL_PIS Valor do PIS N - 02 OC
25 VL_COFINS Valor da COFINS N - 02 OC
26 TP_LIGACAO Código de tipo de Ligação N 001* - OC
1 - Monofásico
2 - Bifásico
3 - Trifásico
27 COD_GRUPO_TENSAO Código de grupo de tensão: C 002* - OC
01 - A1 - Alta Tensão (230kV ou mais)
02 - A2 - Alta Tensão (88 a 138kV)
03 - A3 - Alta Tensão (69kV)
04 - A3a - Alta Tensão (30kV a 44kV)
05 - A4 - Alta Tensão (2,3kV a 25kV)
06 - AS - Alta Tensão Subterrâneo 06
07 - B1 - Residencial 07
08 - B1 - Residencial Baixa Renda 08
09 - B2 - Rural 09
10 - B2 - Cooperativa de Eletrificação Rural
11 - B2 - Serviço Público de Irrigação
12 - B3 - Demais Classes
13 - B4a - Iluminação Pública - rede de distribuição
14 - B4b - Iluminação Pública - bulbo de lâmpada
Observações:
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Campo 01 (REG) - Valor válido: [1500]
Campo 02 (IND_OPER) - Valor válido: [1]
Campo 03 (IND_EMIT) - Valor válido: [0]
Campo 04 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 05 (COD_MOD) - Valor válido: [06] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 06 (COD_SIT) - Valores válidos: [00, 01, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3.
Campo 09 (COD_CONS) - Valores válidos: [“01”, “02”, “03’, “04”, “05”, “06”, “07”, “08”]
Campo 10 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 11 (DT_DOC) - Preenchimento: data de emissão da nota fiscal no formato “ddmmaaaa”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 12 (DT_E_S) - Preenchimento: data de entrada ou saída da nota fiscal no formato “ddmmaaaa”.
Campo 13 (VL_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 15 (VL_FORN) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 23 (COD_INF) - Validação: o valor informado no campo deve existir no registro 0450.
Campo 24 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo.
Campo 25 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo.
Campo 26 (TP_LIGACAO) - Valores válidos: [1, 2, 3]
Campo 27 (COD_GRUPO_TENSAO) - Valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14]
----
REGISTRO 1510: ITENS DO DOCUMENTO NOTA FISCAL/CONTA ENERGIA ELÉTRICA
(CÓDIGO 06)
Este registro deve ser apresentado para informar os itens das Notas Fiscais/Contas de Energia Elétrica (código 06 da Tabela
Documentos Fiscais do ICMS) apresentadas nos registros 1500.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "1510" C 004 - O
02 NUM_ITEM Número sequencial do item no documento fiscal N 003 - O
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
04 COD_CLASS Código de classificação do item de energia elétrica, conforme N 004* - O
a Tabela 4.4.1
05 QTD Quantidade do item N - 03 OC
06 UNID Unidade do item (Campo 02 do registro 0190) C 006 - OC
07 VL_ITEM Valor do item N - 02 O
08 VL_DESC Valor total do desconto N - 02 OC
09 CST_ICMS Código da Situação Tributária, conforme a Tabela indicada no N 003* - O
item 4.3.1
10 CFOP Código Fiscal de Operação e Prestação N 004* - O
11 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 OC
12 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
13 VL_ICMS Valor do ICMS creditado/debitado N - 02 OC
14 VL_BC_ICMS_ST Valor da base de cálculo referente à substituição tributária N - 02 OC
15 ALIQ_ST Alíquota do ICMS da substituição tributária na unidade da N - 02 OC
federação de destino
16 VL_ICMS_ST Valor do ICMS referente à substituição tributária N - 02 OC
17 IND_REC Indicador do tipo de receita: C 001* - O
0- Receita própria;
1- Receita de terceiros
18 COD_PART Código do participante receptor da receita, terceiro da operação C 060 OC
(campo 02 do Registro 0150)
19 VL_PIS Valor do PIS N - 02 OC
20 VL_COFINS Valor da COFINS N - 02 OC
21 COD_CTA Código da conta analítica contábil debitada/creditada C - - OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1510]
Campo 03 (COD_ITEM) - Validação: o valor informado no campo deve existir no registro 0200, campo COD_ITEM.
Campo 04 (COD_CLASS) - Validação: o valor informado no campo deve existir na Tabela de Classificação de Itens de
Energia Elétrica, Serviços de Comunicação e Telecomunicação, constante no item 4.4.1 da Nota Técnica, instituída pelo Ato
COTEPE/ICMS nº 44/2018 e suas alterações.
Campo 06 (UNID) - Validação: o valor deve estar informado no registro 0190.
Campo 09 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao
ICMS, referenciada no item 4.3.1da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018.
Campo 10 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01.
O primeiro caractere do CFOP deve ser igual a 6.
O primeiro caractere do CFOP deve ser o mesmo para todos os itens do documento.
Não podem ser utilizados códigos que correspondam aos títulos dos agrupamentos de CFOP.
Campo 17 (IND_REC) - Valores válidos: [0, 1]
Campo 18 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 19 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 20 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
REGISTRO 1600: TOTAL DAS OPERAÇÕES COM CARTÃO DE CRÉDITO E/OU DÉBITO,
LOJA (PRIVATE LABEL) E DEMAIS INSTRUMENTOS DE PAGAMENTOS ELETRÔNICOS
(VÁLIDO ATÉ 31/12/2021)
Este registro destina-se a identificar o valor total das operações de vendas realizadas pelo declarante por meio de cartão
de débito ou de crédito, de loja (private label) e demais instrumentos de pagamentos eletrônicos, discriminado por instituição
financeira e de pagamento, integrante ou não do Sistema de Pagamentos Brasileiro – SPB (Convênio ICMS nº 134/2016).
Deve-se consultar o contrato firmado entre a instituição e o informante do arquivo, para se ratificar a existência da
prestação do serviço. Deve ser informado o valor total destas vendas, excluídos os estornos, cancelamentos e outros
recebimentos não vinculados à sua atividade operacional.
A obrigatoriedade deste registro deve ser verificada junto a cada uma das unidades federativas.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1600" C 004 - O
02 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - O
identificação da instituição financeira e/ou de pagamento
03 TOT_CREDITO Valor total das operações de crédito realizadas no período N - 002 O
04 TOT_DEBITO Valor total das operações de débito realizadas no período N - 002 O
Observações:
Nível hierárquico – 2
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1600]
Campo 02 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
----
REGISTRO 1601: OPERAÇÕES COM INSTRUMENTOS DE PAGAMENTOS ELETRÔNICOS
(VÁLIDO A PARTIR DE 01/01/2022)
Este registro destina-se a identificar o valor total recebido pelo declarante, relativo a operações e prestações de serviços,
realizadas por meio de instrumentos de pagamentos eletrônicos, discriminado por instituição financeira e de pagamento,
integrante ou não do Sistema de Pagamentos Brasileiro – SPB (Convênio ICMS nº 134/2016).
Deve-se consultar o contrato firmado entre a instituição e o informante do arquivo, para se ratificar a existência da
prestação do serviço, quando couber.
Deve ser informado o valor total destas operações, excluídos os estornos e cancelamentos. A informação desse registro
é facultativa para as escriturações do exercício de 2.022. A obrigatoriedade deste registro deve ser verificada junto a cada uma
das unidades federativas a partir de 2.023.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1601" C 004 - O
02 COD_PART_IP Código do participante (campo 02 do Registro 0150): C 060 - O
identificação da instituição que efetuou o pagamento
03 COD_PART_IT Código do participante (campo 02 do Registro 0150): C 060 - OC
identificação do intermediador da transação
04 TOT_VS Valor total bruto das vendas e/ou prestações de N - 002 O
serviços no campo de incidência do ICMS, incluindo
operações com imunidade do imposto.
05 TOT_ISS Valor total bruto das prestações de serviços no campo N - 002 O
de incidência do ISS
06 TOT_OUTROS Valor total de operações deduzido dos valores dos N - 002 O
campos TOT_VS e TOT_ISS.
Observações:
Nível hierárquico – 2
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1601]
Campo 02 (COD_PART_IP) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Preenchimento: Informar o CNPJ da instituição que efetuou o pagamento.
Campo 03 (COD_PART_IT) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Preenchimento: informar o CNPJ do intermediador de transação (agenciador, plataforma de delivery, marketplace e similar)
de serviços e de negócios.
Campo 04 (TOT_VS) - Preenchimento: o valor informado deve ser o valor total bruto das vendas e/ou prestações de serviços,
no campo de incidência do ICMS, ainda que a venda ou prestação seja considerada imune, isenta ou não tributada, independente
do meio de pagamento utilizado.
Campo 05 (TOT_ISS) – Preenchimento: o valor informado deve ser o valor total bruto das prestações de serviços, no campo
de incidência do ISS, ainda que a prestação seja considerada imune, isenta ou não tributada, independente do meio de
pagamento utilizado.
Campo 06 (TOT_OUTROS) – Preenchimento: o valor informado deve ser o valor bruto das operações que não estejam no
campo de incidência do ICMS ou ISS, independente do meio de pagamento utilizado. Incluem neste caso compras de cartão
presente, saques, pagamentos de fatura de telefone etc.
----
REGISTRO 1700: DOCUMENTOS FISCAIS UTILIZADOS
Neste registro devem ser informados os dispositivos autorizados e utilizados na emissão de documentos fiscais no
período da EFD-ICMS/IPI.
A obrigatoriedade deste registro deve ser verificada junto a cada uma das unidades federativas.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo “1700”. C 004 - O
02 COD_DISP Código dispositivo autorizado: C 002* - O
00 - Formulário de Segurança – impressor autônomo
01 - FS-DA – Formulário de Segurança para Impressão de
DANFE
02 – Formulário de segurança - NF-e
03 - Formulário Contínuo
04 – Blocos
05 - Jogos Soltos
03 COD_MOD Código do modelo do dispositivo autorizado, conforme a C 002* - O
Tabela 4.1.1
04 SER Série do dispositivo autorizado C 004 - OC
05 SUB Subsérie do dispositivo autorizado C 003 - OC
06 NUM_DOC_INI Número do dispositivo autorizado (utilizado) inicial N 012 - O
07 NUM_DOC_FIN Número do dispositivo autorizado (utilizado) final N 012 - O
08 NUM_AUT Número da autorização, conforme dispositivo autorizado N 060 - O
Observações:
Nível hierárquico - 2
Ocorrência – V
Campo 01 (REG) - Valor Válido: [1700]
Campo 02 (COD_DISP) - Valores Válidos: [“00”,“01”,“02”,“03”,“04”,“05”]
00 – Formulário de Segurança – Formulário utilizado pelo impressor autônomo nos termos dos Convênios ICMS nº 58/95 e
131/95 (vigentes até 30/06/2009) e Convênio ICMS nº 96/09 (com efeitos a partir de 01/07/2010);
01 - FS-DA – Formulário de Segurança para Impressão de Documento Auxiliar de Documentos Fiscais eletrônicos (NF-e, CT-
e)– Formulário utilizado para contingência de Documentos Fiscais eletrônicos, conforme Convênio ICMS nº 110/08 (vigente
até 30/06/2009) e Convênio ICMS nº 96/0909 (com efeitos a partir de 01/07/2010).
02 – Formulário de Segurança - NF-e - Formulário autorizado nos termos dos Convênios ICMS 58/95 e 131/95 (vigentes até
30/06/2009) e utilizados para emissão de NF-e em contingência, conforme Convênio ICMS 110/08 (vigente até 30/06/2009) e
Convênio ICMS 96/0909 (com efeitos a partir de 01/07/2010) e Ajuste SINIEF nº 07/2005 e suas alterações.
Campo 03 (COD_MOD) - Preenchimento: o valor informado deve constar na tabela 4.1.1 da Nota Técnica, instituída pelo
Ato COTEPE/ICMS nº 44/2018 e suas alterações. – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 06 (NUM_DOC_INI) - Preenchimento: Número inicial do intervalo do documento, informado no campo 02, utilizado
no período da EFD-ICMS/IPI.
Nos casos de documentos eletrônicos deverão ser informados a seriação, se existir, e os números pré-impressos nos respectivos
documentos utilizados.
Campo 07 (NUM_DOC_FIN) - Preenchimento: Número final do intervalo do documento, informado no campo 02, utilizado
no período da EFD-ICMS/IPI.
Nos casos de documentos eletrônicos deverão ser informados a seriação, se existir, e os números pré-impressos nos respectivos
documentos utilizados.
Campo 08 (NUM_AUT) - Preenchimento: Número da autorização, emitida pela Secretaria estadual, para utilização dos
documentos informados no campo 2, do respectivo intervalo informado.
----
REGISTRO 1710: DOCUMENTOS FISCAIS CANCELADOS/INUTILIZADOS
Neste registro devem ser informados os documentos cancelados/inutilizados no intervalo constante do registro 1700.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo “1710”. C 004 - O
02 NUM_DOC_INI Número do dispositivo autorizado (inutilizado) inicial N 012 - O
03 NUM_DOC_FIN Número do dispositivo autorizado (inutilizado) final N 012 - O
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [1710]
Campo 02 (NUM_DOC_INI) - Preenchimento: Número inicial do documento cancelado ou intervalo, informado no campo
02.
Nos casos de documentos eletrônicos deverão ser informados a seriação, se existir, e os números pré-impressos nos respectivos
documentos utilizados.
Observação: Quando o cancelamento não for contínuo, o número inicial deverá ser igual ao número final.
Exemplo: Reg 1700 Campo 06 35; Campo 07 55 Canceladas: 45; 50 a 52.
Então, teremos: Reg 1710 Campo 02 45; Campo 03 45
Reg 1710 Campo 02 50; Campo 03 52
Campo 03 (NUM_DOC_FIN) - Preenchimento: Número final do documento ou intervalo, informado no campo 02.
Nos casos de documentos eletrônicos deverão ser informados a seriação, se existir, e os números pré-impressos nos respectivos
documentos utilizados.
----
REGISTRO 1800: DCTA – DEMONSTRATIVO DE CRÉDITO DO ICMS SOBRE
TRANSPORTE AÉREO
Este registro deve ser informado, pelas empresas de transporte aéreo, para explicitar os estornos de créditos de
ICMS.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo “1800”. C 004* - O
02 VL_CARGA Valor das prestações cargas (Tributado) N - 02 O
03 VL_PASS Valor das prestações passageiros/cargas (Não Tributado) N - 02 O
04 VL_FAT Valor total do faturamento (2+3) N - 02 O
05 IND_RAT Índice para rateio(2 / 4) N 008 06 O
06 VL_ICMS_ANT Valor total dos créditos do ICMS N - 02 O
07 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 O
08 VL_ICMS_APUR Valor do ICMS apurado no cálculo (5 x 6) N - 02 O
09 VL_BC_ICMS_APUR Valor da base de cálculo do ICMS apurada (5 x 7) N - 02 O
10 Valor da diferença a ser levada a estorno de crédito na 02 O
VL_DIF N -
apuração (6 - 8)
Observações:
Nível hierárquico - 2
Ocorrência – 1
Campo 01 (REG) - Valor Válido: [1800]
----
REGISTRO 1900: INDICADOR DE SUB-APURAÇÃO DO ICMS
Este registro tem por objetivo escriturar o ICMS de operações especificadas em legislação estadual como obrigadas a
apurações em separado. Este registro deverá ser apresentado somente pelos contribuintes obrigados por legislação específica
de cada UF.
Este registro, a critério da legislação de cada UF, pode ser utilizado também para a apuração da diferença entre o preço
praticado na operação a consumidor final e a base de cálculo utilizada para o cálculo do débito de responsabilidade por
substituição tributária (ressarcimento/restituição/complemento).
Registro obrigatório, se houver registro C197, C597, C857, C897, D197 ou D737, onde o 4º (quarto) dígito do campo
02 - COD_AJ, for “3”, “4”, “5”, “6”, “7” ou “8”, ou na existência de saldo credor no campo 08- VL_SLD_CREDOR_ANT_OA
do registro 1920, em valor maior que Zero.
Validação do Registro: Não podem ser informados dois ou mais registros com o mesmo código de indicador de
apuração (campo 2 – IND_APUR_ICMS).
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "1900" C 004 - O
02 IND_APUR_ICMS Indicador de outra apuração do ICMS: C 001* - O
3 – APURAÇÃO 1;
4 – APURAÇÃO 2;
5 – APURAÇÃO 3;
6 – APURAÇÃO 4;
7 – APURAÇÃO 5;
8 – APURAÇÃO 6.
03 DESCR_COMPL_OUT_APUR Descrição complementar de Outra Apuração do C - - O
ICMS
Observações: As Apurações 4, 5 e 6 serão válidas a partir de 01/01/2014.
Nível hierárquico - 2
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1900]
Campo 02 (IND_APUR_ICMS) - Valores Válidos: [“3”,“4”,“5”. “6”, “7”, “8”]
Código “3” –Apuração em separado 1 (tem que haver pelo menos um registro C197, C850, D197 ou D737
onde o 4º (quarto) dígito do COD_AJ, campo 02, seja 3, ou valor maior que “zero” no campo 08-
VL_SLD_CREDOR_ANT_OA do registro 1920).
Código “4” – Apuração em separado 2 (tem que haver pelo menos um registro C197, C857, C897, D737 ou
D197 onde o 4º (quarto) dígito do COD_AJ, campo 02, seja 4, ou valor maior que “zero” no campo 08-
VL_SLD_CREDOR_ANT_OA do registro 1920).
Código “5” – Apuração em separado 3 (tem que haver pelo menos um registro C197, C857, C897, D737 ou
D197 onde o 4º (quarto) dígito do COD_AJ, campo 02, seja 5, ou valor maior que “zero” no campo 08-
VL_SLD_CREDOR_ANT_OA do registro 1920).
Código “6” – Apuração em separado 4 (tem que haver pelo menos um registro C197, C857, C897, D737 ou
D197 onde o 4º (quarto) dígito do COD_AJ, campo 02, seja 6, ou valor maior que “zero” no campo 08-
VL_SLD_CREDOR_ANT_OA do registro 1920).
Código “7” – Apuração em separado 5 (tem que haver pelo menos um registro C197, C857, C897, D737 ou
D197 onde o 4º (quarto) dígito do COD_AJ, campo 02, seja 7, ou valor maior que “zero” no campo 08-
VL_SLD_CREDOR_ANT_OA do registro 1920).
Código “8” – Apuração em separado 6 (tem que haver pelo menos um registro C197, C857, C897, D737 ou
D197 onde o 4º (quarto) dígito do COD_AJ, campo 02, seja 8, ou valor maior que “zero” no campo 08-
VL_SLD_CREDOR_ANT_OA do registro 1920).
Observação: os códigos 0, 1 e 2 são utilizados para apuração do ICMS próprio, ST e outras.
Campo 03 (DESCR_COMPL_OUT_APUR) - Preenchimento: Descrever a norma legal que exige esta apuração em separado.
----
REGISTRO 1910: PERÍODO DA SUB-APURAÇÃO DO ICMS
Este registro tem por objetivo informar o(s) período(s) das apurações em separado do ICMS. Os períodos informados
devem abranger todo o intervalo da escrituração fiscal, sem sobreposição ou omissão de datas ou períodos.
Validação do Registro: Não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos 02 (DT_INI) e 03 (DT_FIN). Não devem existir lacunas ou sobreposições de datas nos períodos de apuração
informados nestes registros, em comparação com as datas informadas no registro 0000.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1910" C 004 - O
02 DT_INI Data inicial da sub-apuração N 008* - O
03 DT_FIN Data final da sub-apuração N 008* - O
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor válido: [1910]
Campo 02 (DT_INI) - Preenchimento: informar a data inicial a que se refere a apuração em separado (sub-apuração), no
formato “ddmmaaaa”, sem os separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000 e maior ou igual
ao valor no campo DT_INI do registro 0000. A data informada no campo deve ser menor ou igual à data informada no campo
DT_FIN do registro E100.
Campo 03 (DT_FIN) - Preenchimento: informar a data final a que se refere a apuração em separado (sub-apuração) no formato
“ddmmaaaa”, sem os separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000 e maior ou igual
ao valor no campo DT_INI do registro 0000.
----
REGISTRO 1920: SUB-APURAÇÃO DO ICMS
Este registro tem por objetivo informar os valores relativos a apurações especificadas no registro 1900, que se referem
aos valores do ICMS das operações próprias estornados do registro E110 por meio de ajustes decorrentes de documentos, nos
campos 03 (VL_AJ_DEBITOS) e 07 (VL_AJ_CREDITOS), e por meio de ajustes de apuração nos campos 05
(VL_ESTORNOS_CRED) e 09 (VL_ESTORNOS_DEB).
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1920" C 004 - O
02 VL_TOT_TRANSF_DEBITOS_OA Valor total dos débitos por “Saídas e N - 02 O
prestações com débito do imposto”
03 VL_TOT_AJ_DEBITOS_OA Valor total de “Ajustes a débito” N - 02 O
04 VL_ESTORNOS_CRED_OA Valor total de Ajustes “Estornos de N - 02 O
créditos”
05 VL_TOT_TRANSF_CREDITOS_OA Valor total dos créditos por “Entradas e N - 02 O
aquisições com crédito do imposto”
06 VL_TOT_AJ_CREDITOS_OA Valor total de “Ajustes a crédito” N - 02 O
07 VL_ESTORNOS_DEB_OA Valor total de Ajustes “Estornos de N - 02 O
Débitos”
08 VL_SLD_CREDOR_ANT_OA Valor total de “Saldo credor do período N - 02 O
anterior”
09 VL_SLD_APURADO_OA Valor do saldo devedor apurado N - 02 O
10 VL_TOT_DED Valor total de “Deduções” N - 02 O
11 VL_ICMS_RECOLHER_OA Valor total de "ICMS a recolher (09-10) N - 02 O
12 VL_SLD_CREDOR_TRANSP_OA Valor total de “Saldo credor a transportar N - 02 O
para o período seguinte”
13 DEB_ESP_OA Valores recolhidos ou a recolher, extra- N - 02 O
apuração.
Observações:
Nível hierárquico - 4
Ocorrência - um (por período)
Campo 01 (REG) - Valor Válido: [1920]
Campo 02 (VL_TOT_TRANSF_DEBITOS_OA) - Validação: Se o campo 02- IND_APUR_ICMS do registro 1900 for igual
a:
a) “3” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “2” e “3”;
b) “4” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “2” e “4”;
c) “5” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “2” e “5”;
d) “6” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “2” e “6”;
e) “7” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “2” e “7”;
f) “8” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “2” e “8”.
Os citados registros C197 e D197 devem ser originados em documentos fiscais de saídas que geraram débitos de ICMS de
operações próprias.
Ficam excluídos os documentos extemporâneos (COD_SIT com valor igual ‘01’) e os documentos complementares
extemporâneos (COD_SIT com valor igual ‘07’).
Serão considerados os registros cujos documentos estejam compreendidos no período informado no registro 1910
utilizando, para tanto, o campo DT_E_S (C100) e DT_DOC ou DT_A_P (D100). Quando o campo DT_E_S ou DT_A_P do
registro C100 não for informado, utilizar o campo DT_DOC.
Campo 03 (VL_TOT_AJ_DEBITOS_OA) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR dos registros 1921, se o terceiro caractere for igual a ‘0’ e o quarto caractere do campo COD_AJ_APUR do
registro 1921 for igual a ‘0’.
Campo 04 (VL_ESTORNOS_CRED_OA) - Validação: o valor informado deve corresponder ao somatório do campo
VL_AJ_APUR dos registros 1921, se o terceiro caractere for igual a ‘0’ e o quarto caractere do campo COD_AJ_APUR do
registro 1921 for igual a ‘1’.
Campo 05 (VL_TOT_TRANSF_CREDITOS_OA) - Validação: Se o campo 02- IND_APUR_ICMS do registro 1900 for
igual a:
a) “3” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “5” e “3”;
b) “4” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “5” e “4”;
c) “5” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “5” e “5”;
d) “6” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “5” e “6”;
e) “7” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “5” e “7”;
f) “8” - o valor informado deve corresponder ao somatório dos valores do campo 07- VL_ICMS dos registros C197 e D197
onde o terceiro e quarto caracteres do código de ajuste forem iguais a “5” e “8”.
Os citados registros C197 e D197 devem ser originados em documentos fiscais de entradas que geraram créditos de ICMS
de operações próprias.
Os documentos fiscais devem ser somados conforme o período informado no registro 1910 e a data informada no campo
DT_E_S (C100) ou campo DT_A_P (D100), exceto se COD_SIT do documento for igual a “01” (extemporâneo) ou igual a 07
(NF Complementar extemporânea), cujo valor será somado no primeiro período de apuração informado no registro 1910.
Quando o campo DT_E_S ou DT_A_P não for informado, é utilizada a data constante no campo DT_DOC.
Campo 06 (VL_TOT_AJ_CREDITOS_OA) - Validação: o valor informado deve corresponder ao somatório dos valores
constantes dos registros 1921, quando o terceiro caractere for igual a ‘0’ e o quarto caractere for igual a ‘2’, do
COD_AJ_APUR do registro 1921.
Campo 07 (VL_ESTORNOS_DEB_OA) - Validação: o valor informado deve corresponder ao somatório do VL_AJ_APUR
dos registros 1921, quando o terceiro caractere for igual a ‘0’ e o quarto caractere for igual a ‘3’, do COD_AJ_APUR do
registro 1921.
Campo 08 (VL_SLD_CREDOR_ANT_OA) - Preenchimento: Informar o saldo credor do período anterior da respectiva
apuração em separado (sub-apuração).
Campo 09 (VL_SLD_APURADO_OA) - Validação: o valor informado deve ser preenchido com base na expressão: soma do
total de débitos transferidos (VL_TOT_TRANSF_DEBITOS_OA) com total de ajustes a débito (VL_TOT_AJ_DEBITOS_OA)
com total de estorno de crédito (VL_ESTORNOS_CRED_OA) menos a soma do total de créditos transferidos
(VL_TOT_TRANSF_CREDITOS_OA) com total de ajustes a crédito (VL_AJ_CREDITOS_OA) com total de estorno de
débito (VL_ESTORNOS_DEB_OA) com saldo credor do período anterior (VL_SLD_CREDOR_ANT_OA). Se o valor da
expressão for maior ou igual a “0” (zero), então este valor deve ser informado neste campo e o campo 12
(VL_SLD_CREDOR_TRANSP_OA) deve ser igual a “0” (zero). Se o valor da expressão for menor que “0” (zero), então este
campo deve ser preenchido com “0” (zero) e o valor absoluto da expressão deve ser informado no campo
VL_SLD_CREDOR_TRANSP_OA.
Campo 10 (VL_TOT_DED) - Validação: o valor informado deve corresponder ao somatório do campo VL_ICMS dos
registros C197 e D197, se o terceiro caractere do código de ajuste dos registros C197 e D197, for “6”’ e o quarto caractere
for “3”, “4” “5”, “6”, “7” ou “8”,, somado ao valor total informado nos registros 1921, quando o terceiro caractere for igual a
‘0’ e o quarto caractere for igual a ‘4’, do campo COD_AJ_APUR do registro 1921.
Para o somatório do campo VL_ICMS dos registros C197 e D197 devem ser considerados os documentos fiscais
compreendidos no período informado no registro 1910, comparando com a data constante no campo DT_E_S do registro C100
e DT_DOC ou DT_A_P do registro D100, exceto se COD_SIT do registro C100 for igual a ‘01’ (extemporâneo) ou igual a
‘07’ (Complementar extemporânea), cujo valor deve ser somado no primeiro período de apuração informado no registro 1910,
quando houver mais de um período de apuração. Quando o campo DT_E_S não for informado, utilizar o campo DT_DOC.
Campo 11 (VL_ICMS_RECOLHER_OA) – Validação: o valor informado deve corresponder à diferença entre o campo
VL_SLD_APURADO_OA e o campo VL_TOT_DED. O valor da soma deste campo com o campo DEB_ESP_OA deve ser
igual à soma dos valores do campo VL_OR do registro 1926.
Campo 12 (VL_SLD_CREDOR_TRANSP_OA) – Validação: se o valor da expressão: “soma do total de débitos
(VL_TOT_TRANSF_DEBITOS_OA) mais total de ajustes a débito (VL_AJ_DEBITOS_OA) mais total de estorno de crédito
(VL_ESTORNOS_CRED_OA)” menos “a soma do total de créditos transferidos (VL_TOT_TRANSF_CREDITOS_OA) mais
total de ajuste a crédito (VL_AJ_CREDITOS_OA) mais total de estorno de débito (VL_ESTORNOS_DEB_OA) mais saldo
credor do período anterior (VL_SLD_CREDOR_ANT_OA)”, for maior que ZERO, este campo deve ser preenchido com “0”
(zero) e o campo 11 (VL_SLD_APURADO) deve ser igual ao valor do resultado. Se for menor que “0” (zero), o valor absoluto
do resultado deve ser informado neste campo e o campo VL_SLD_APURADO deve ser informado com “0” (zero).
Campo 13 (DEB_ESP_OA) – Preenchimento: Informar o correspondente ao somatório dos valores:
a) de ICMS correspondentes aos documentos fiscais extemporâneos (COD_SIT igual a “01”) e dos documentos fiscais
complementares extemporâneos (COD_SIT igual a “07”), referentes às apurações em separado;
b) de ajustes do campo VL_ICMS dos registros C197 e D197, se o terceiro caractere do código informado no campo
COD_AJ dos registros C197 e D197 for igual a “7” (débitos especiais) e o quarto caractere for igual a “3”, “4”, “5”,
“6”, “7” ou “8”, (“Apuração 1 – Bloco 1900” ou “Apuração 2 – Bloco 1900” ou “Apuração 3 – Bloco 1900” ou
“Apuração 4 – Bloco 1900” ou “Apuração 5 – Bloco 1900” ou “Apuração 6 – Bloco 1900”) referente aos documentos
compreendidos no período a que se refere a escrituração; e
c) de ajustes do campo VL_AJ_APUR do registro 1921, se o terceiro caractere do código informado no campo
COD_AJ_APUR do registro 1921 for igual a “0” (apuração ICMS próprio) e o quarto caractere for igual a “5”(débito
especial).
Validação: O valor da soma deste campo com o campo VL_ICMS_RECOLHER_OA deve ser igual à soma dos valores do
campo VL_OR do registro 1926.
----
REGISTRO 1921: AJUSTE/BENEFÍCIO/INCENTIVO DA SUB-APURAÇÃO DO ICMS
Este registro tem por objetivo discriminar todos os ajustes lançados nos campos VL_TOT_AJ_DEBITOS_OA,
VL_ESTORNOS_CRED_OA, VL_TOT_AJ_CREDITOS_OA, VL_ESTORNOS_DEB_OA, VL_TOT_DED e
DEB_ESP_OA, todos do registro 1920.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1921" C 004 - O
02 COD_AJ_APUR Código do ajuste da SUB-APURAÇÃO e dedução, C 008* - O
conforme a Tabela indicada no item 5.1.1.
03 DESCR_COMPL_AJ Descrição complementar do ajuste da apuração. C - - OC
04 VL_AJ_APUR Valor do ajuste da apuração N - 02 O
Observações:
Nível hierárquico - 5
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1921]
Campo 02 (COD_AJ_APUR) - Preenchimento: o valor informado no campo deve existir na tabela de código do ajuste da
apuração e dedução de cada Secretaria de Fazenda, conforme a UF do declarante, campo UF do registro 0000 ou, não havendo
esta tabela, o valor informado no campo deve existir na tabela de código do ajuste da apuração e dedução, constante da
observação do Item 5.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e suas alterações.
O código do ajuste utilizado deve ter seu terceiro caractere como “0” (zero), indicando ajuste de ICMS, não incluindo ajustes
de ICMS ST.
O quarto caractere deve ser preenchido, conforme item 5.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018
e suas alterações, com um dos códigos abaixo:
0 – Outros débitos;
1 – Estorno de créditos;
2 – Outros créditos;
3 – Estorno de débitos;
4 – Deduções do imposto apurado;
5 – Débitos Especiais.
Campo 03 (DESCR_COMPL_AJ) - Preenchimento: Sem prejuízo de outras situações definidas em legislação específica, o
contribuinte deverá fazer a descrição complementar de ajustes (tabela 5.1.1) sempre que informar códigos genéricos.
----
REGISTRO 1922: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA SUB-APURAÇÃO DO
ICMS
Este registro tem por objetivo detalhar os ajustes do registro 1921 quando forem relacionados a processos judiciais ou
fiscais ou a documentos de arrecadação, observada a legislação estadual pertinente. Os valores recolhidos, com influência nesta
apuração em separado (sub-apuração) do ICMS, devem ser detalhados neste registro, com identificação do documento de
arrecadação específico.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "1922" C 004 - O
02 NUM_DA Número do documento de arrecadação estadual, se houver C - - OC
03 NUM_PROC Número do processo ao qual o ajuste está vinculado, se houver C 060 - OC
04 IND_PROC Indicador da origem do processo: C 001* - OC
0- SEFAZ;
1- Justiça Federal;
2- Justiça Estadual;
9- Outros
05 PROC Descrição resumida do processo que embasou o lançamento C - - OC
06 TXT_COMPL Descrição complementar C - - OC
Observações:
Nível hierárquico - 6
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1922]
Campo 02 (NUM_DA) - Preenchimento: este campo deve ser preenchido se o ajuste for referente a um documento de
arrecadação, tais como pagamentos indevidos, pagamentos antecipados e outros.
Campo 03 (NUM_PROC) - Preenchimento: o valor deve ter até 60 caracteres.
Campo 04 (IND_PROC) - Valores válidos: [0, 1, 2, 9]
Campo 06 (TXT_COMPL) - Preenchimento: Outras informações complementares.
----
REGISTRO 1923: INFORMAÇÕES ADICIONAIS DOS AJUSTES DA SUB-APURAÇÃO DO
ICMS – IDENTIFICAÇÃO DOS DOCUMENTOS FISCAIS
Este registro tem por objetivo identificar os documentos fiscais relacionados ao ajuste.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1923" C 004 - O
02 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - O
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
Nível hierárquico - 6
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1923]
Campo 02 (COD_PART) - Preenchimento: no caso de entrada, deve constar a informação referente ao emitente do documento
ou ao remetente das mercadorias ou serviços. No caso de saída, deve constar a informação referente ao destinatário. O valor
deve ter até 60 caracteres.
Validação: o valor informado deve existir no campo COD_PART do registro 0150. Quando se tratar de NFC-e (modelo 65),
o campo não deve ser preenchido.
Campo 03 (COD_MOD) - Validação: o valor informado no campo deve existir na tabela de Documentos Fiscais do ICMS,
conforme Item 4.1.1. da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e suas alterações. – Ver tabela
reproduzida na subseção 1.4 deste guia.
Campo 06 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (DT_DOC) - Preenchimento: informar a data de emissão do documento fiscal, no formato “ddmmaaaa”, sem os
separadores de formatação.
Campo 08 (COD_ITEM) – Preenchimento: este campo só deve ser informado quando o ajuste se referir a um determinado
item/produto do documento.
Validação: o valor informado no campo deve existir no campo COD_ITEM do registro 0200.
Campo 10 (CHV_DOCe) - Preenchimento: informar a chave da NF-e, para documentos de COD_MOD igual a “55”, ou
informar a chave do conhecimento de transporte eletrônico, para documentos de COD_MOD igual a “57” (a vigorar a partir de
01/01/2017). A partir de abril/2017, informar a chave do CT-e OS.
Validação: quando se tratar de NF-e, CT-e ou CT-e OS, é conferido o dígito verificador (DV) da chave do documento
eletrônico. Será verificada a consistência da informação dos campos NUM_DOC e SER com o número do documento e série
contidos na chave do documento eletrônico.
----
REGISTRO 1925: INFORMAÇÕES ADICIONAIS DA SUB-APURAÇÃO – VALORES
DECLARATÓRIOS
Este registro tem o objetivo de informar os valores declaratórios relativos ao ICMS desta apuração em separado (sub-
apuração), conforme definição da legislação estadual pertinente. Esses valores são meramente declaratórios e não são
computados nesta apuração em separado (sub-apuração) do ICMS.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "1925" C 004 - O
02 COD_INF_ADIC Código da informação adicional conforme tabela a ser C 008* - O
definida pelas SEFAZ, conforme tabela definida no item
5.2.
03 VL_INF_ADIC Valor referente à informação adicional N - 02 O
04 DESCR_COMPL_AJ Descrição complementar do ajuste C - - OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [1925]
Campo 02 (COD_INF_ADIC) - Preenchimento: o código da informação adicional deve obedecer à tabela definida pelas
Secretarias de Fazenda dos Estados. Caso não haja publicação da referida tabela, o registro não deve ser apresentado.
----
REGISTRO 1926: OBRIGAÇÕES DO ICMS A RECOLHER – OPERAÇÕES REFERENTES À
SUB-APURAÇÃO
Este registro tem o objetivo de discriminar os pagamentos realizados ou a realizar, referentes à apuração em separado
(sub-apuração) do ICMS identificada no registro 1900. A soma do valor das obrigações deste registro deve ser igual à soma
dos campos VL_ICMS_RECOLHER_OA e DEB_ESP_OA, do registro 1920.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1926" C 004 - O
02 COD_OR Código da obrigação a recolher, conforme a Tabela 5.4 C 003* - O
03 VL_OR Valor da obrigação a recolher N - 02 O
04 DT_VCTO Data de vencimento da obrigação N 008* - O
05 COD_REC Código de receita referente à obrigação, próprio da C - - O
unidade da federação, conforme legislação estadual,
06 NUM_PROC Número do processo ou auto de infração ao qual a C 060 - OC
obrigação está vinculada, se houver.
07 IND_PROC Indicador da origem do processo: C 001* - OC
0- SEFAZ;
1- Justiça Federal;
2- Justiça Estadual;
9- Outros
08 PROC Descrição resumida do processo que embasou o C - - OC
lançamento
09 TXT_COMPL Descrição complementar das obrigações a recolher. C - - OC
10 MES_REF* Informe o mês de referência no formato “mmaaaa” N 006* - O
Observações:
* O campo 10 – MES_REF somente deverá ser incluído no leiaute a partir de períodos de apuração de janeiro de 2011.
Nível hierárquico – 5
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [1926]
Campo 02 (COD_OR) - Valores válidos: [000, 003, 004, 005, 006, 090]
Campo 03 (VL_OR) – Preenchimento: o valor da soma deste campo deve corresponder à soma dos campos
VL_ICMS_RECOLHER_OA e DEB_ESP_OA do registro 1920. Não informar acréscimos legais, se houver.
Campo 04 (DT_VCTO) - Preenchimento: informar a data de vencimento da obrigação, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: o valor informado no campo deve ser uma data válida.
Campo 06 (NUM_PROC) - Preenchimento: o valor deve ter até 60 caracteres.
Validação: se este campo estiver preenchido, os campos IND_PROC e PROC também devem estar preenchidos.
Campo 07 (IND_PROC) - Valores válidos: [0, 1, 2, 9]
Campo 09 (TXT_COMPL) - preenchimento: quando este registro se referir a recolhimento extemporâneo, informar neste
campo o mês e ano de referência de cada um dos débitos extemporâneos do período, no formato mmaaaa, sem utilizar os
caracteres especiais de separação. Exemplo: para débito extemporâneo do mês de abril de 2009 o campo deve ser preenchido,
simplesmente, com os caracteres 042009.
Campo 10 (MES_REF) – Preenchimento: formato mmaaaa, sem utilizar os caracteres especiais de separação.
Validação: O campo MES_REF* não pode ser superior à competência do campo DT_INI do registro 0000
----
REGISTRO 1960: GIAF 1 - GUIA DE INFORMAÇÃO E APURAÇÃO DE INCENTIVOS
FISCAIS E FINANCEIROS: INDÚSTRIA (CRÉDITO PRESUMIDO)
Este registro deverá ser apresentado somente pelos contribuintes obrigados por legislação específica de cada UF.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal dois ou mais registros com o
mesmo conteúdo no campo IND_AP.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1960" C 004 - O
02 IND_AP Indicador da sub-apuração por tipo de benefício (conforme tabela N 002* - O
4.7.1)
03 G1_01 Percentual de crédito presumido N - 02 O
04 G1_02 Saídas não incentivadas de PI N - 02 O
05 G1_03 Saídas incentivadas de PI N - 02 O
06 G1_04 Saídas incentivadas de PI para fora do Nordeste N - 02 O
07 G1_05 Saldo devedor do ICMS antes das deduções do incentivo N - 02 O
08 G1_06 Saldo devedor do ICMS relativo à faixa incentivada de PI N - 02 O
09 G1_07 Crédito presumido nas saídas incentivadas de PI para fora do Nordeste N - 02 O
10 G1_08 Saldo devedor relativo à faixa incentivada de PI após o crédito N - 02 O
presumido nas saídas para fora do Nordeste
11 G1_09 Crédito presumido N - 02 O
12 G1_10 Dedução de incentivo da Indústria (crédito presumido) N - 02 O
13 G1_11 Saldo devedor do ICMS após deduções N - 02 O
Observações:
Nível hierárquico - 2
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [1960]
Campo 02 (IND_AP) - Preenchimento: O valor informado no campo deve existir na tabela 4.7.1 - Indicador da sub-apuração
por tipo de benefício.
Campo 03 (G1_01) – Preenchimento: O valor corresponderá ao percentual de crédito presumido que será aplicado como
incentivo, conforme estabelecido pelo respectivo decreto concessivo.
Campo 04 (G1_02) – Preenchimento: o valor total das saídas de produtos incentivados (PI) fora da faixa de incentivo,
conforme estabelecido pelo respectivo decreto concessivo.
Campo 05 (G1_03) – Preenchimento: o valor total das saídas de produtos incentivados (PI) dentro da faixa de incentivo,
conforme estabelecido pelo respectivo decreto concessivo.
Campo 06 (G1_04) – Preenchimento: o valor total das saídas de produtos incentivados (PI) dentro da faixa de incentivo para
fora da Região Nordeste.
Validação: O valor desse campo não pode ser superior ao do campo G1_03 (Saídas incentivadas de PI).
Campo 07 (G1_05) – Preenchimento: o saldo do ICMS a ser calculado conforme a informação de entradas e saídas e dos
ajustes da apuração para o código de apuração informado no IND_AP.
Campo 08 (G1_06) – Preenchimento: o saldo do ICMS correspondente à comercialização de produtos incentivados dentro
da faixa de incentivo.
Validação: O valor desse campo não pode ser superior ao do campo G1_05 (Saldo devedor do ICMS antes das deduções do
incentivo).
Campo 09 (G1_07) – Preenchimento: O crédito presumido será lançado para compensação do frete nas operações com
produtos incentivados para fora do NE.
Validação: O valor desse campo não pode ser superior a 5% do valor do campo G1_04 (Saídas incentivadas de PI para fora
do Nordeste). E quando o campo G1_06 (Saldo devedor do ICMS relativo à faixa incentivada de PI) for igual a “0” (zero), este
campo deve ser igual a “0” (zero).
Campo 10 (G1_08) – Validação: o valor deve ser igual ao campo G1_06 (saldo devedor do ICMS relativo à faixa incentivada
de PI) subtraído do campo G1_07 (crédito presumido nas saídas incentivadas de PI para fora do Nordeste), por sub-apuração.
Campo 11 (G1_09) – Validação: o valor deve ser menor ou igual ao produto dos campos G1_01 (percentual de crédito
presumido) e G1_08 (saldo devedor do ICMS relativo à faixa incentivada de PI após o crédito presumido nas saídas para fora
do Nordeste), por sub-apuração.
Campo 12 (G1_10) – Validação: o valor deve ser igual ao informado no campo G1_07 (crédito presumido nas saídas
incentivadas de PI para fora do Nordeste) acrescido do campo G1_09 (crédito presumido), por sub-apuração. O valor deste
campo deve ser igual ao valor do ajuste informado no campo VL_AJ_APUR do Registro E111, com o COD_AJ_APUR igual
a “UF04XX11”, onde “XX” é referente à sub-apuração informada no campo 02-IND_AP deste registro.
Campo 13 (G1_11) – Validação: Este campo deve ser igual ao campo G1_05 (saldo devedor do ICMS antes das deduções do
incentivo) subtraído do campo G1_10 (dedução de incentivo da Indústria - crédito presumido), por sub-apuração.
----
REGISTRO 1970: GIAF 3 - GUIA DE INFORMAÇÃO E APURAÇÃO DE INCENTIVOS
FISCAIS E FINANCEIROS: IMPORTAÇÃO (DIFERIMENTO NA ENTRADA E CRÉDITO
PRESUMIDO NA SAÍDA SUBSEQUENTE)
Este registro deverá ser apresentado somente pelos contribuintes obrigados por legislação específica de cada UF.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal dois ou mais registros com o
mesmo conteúdo no campo IND_AP.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1970" C 004 - O
02 IND_AP Indicador da sub-apuração por tipo de benefício (conforme tabela N 002* - O
4.7.1)
03 G3_01 Importações com ICMS diferido N - 02 O
04 G3_02 ICMS diferido nas importações N - 02 O
05 G3_03 Saídas não incentivadas de PI N - 02 O
06 G3_04 Percentual de incentivo nas saídas para fora do Estado N - 02 O
07 G3_05 Saídas incentivadas de PI para fora do Estado N - 02 O
08 G3_06 ICMS das saídas incentivadas de PI para fora do Estado N - 02 O
09 G3_07 Crédito presumido nas saídas para fora do Estado. N - 02 O
10 G3_T Dedução de incentivo da Importação (crédito presumido) N - 02 O
11 G3_08 Saldo devedor do ICMS antes das deduções do incentivo N - 02 O
12 G3_09 Saldo devedor do ICMS após deduções do incentivo N - 02 O
Observações:
Nível hierárquico - 2
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [1970]
Campo 02 (IND_AP) - Preenchimento: O valor informado no campo deve existir na tabela 4.7.1 - Indicador da sub-apuração
por tipo de benefício.
Campo 03 (G3_01) – Preenchimento: informar o valor total das importações com ICMS diferido de acordo com o previsto
no respectivo decreto concessivo do incentivo.
Campo 04 (G3_02) – Preenchimento: informar o valor total do ICMS diferido nas importações, de acordo com o previsto no
respectivo decreto concessivo do benefício na importação.
Validação: Este campo deve ser menor ou igual ao campo G3_01 (importação com ICMS diferido), por sub-apuração.
Campo 05 (G3_03) – Preenchimento: informar o valor total das saídas de produtos incentivados (PI) fora da faixa de incentivo,
conforme estabelecido pelo respectivo decreto concessivo.
Campo 06 (G3_04) – Preenchimento: informar o percentual do incentivo nas operações interestaduais, de acordo com o
respectivo decreto concessivo.
Campo 07 (G3_05) – Preenchimento: informar o valor total das saídas interestaduais de produtos incentivados (PI) dentro da
faixa de incentivo, conforme estabelecido pelo respectivo decreto concessivo.
Campo 08 (G3_06) – Preenchimento: informar o valor total do ICMS destacado nas notas fiscais relativas às saídas
interestaduais incentivadas.
Validação: Este campo deve ser menor ou igual que o campo G3_05 (saídas incentivadas de PI para fora do Estado), por sub-
apuração.
Campo 09 (G3_07) – Validação: o valor informado deve ser menor ou igual ao produto dos campos G3_04 (percentual de
incentivo nas saídas para fora do Estado) e G3_06 (ICMS das saídas incentivadas de PI para fora do Estado), por sub-apuração.
Campo 10 (G3_T) – Validação: o valor informado deve ser igual ao campo G3_07 (crédito presumido nas saídas para fora do
Estado) acrescido de todas as ocorrências do campo G3_12 (crédito presumido nas saídas internas), por sub-apuração. O valor
deste campo deve ser igual ao valor do ajuste informado no campo VL_AJ_APUR do Registro E111, com o COD_AJ_APUR
igual a “UF04XX13”, onde “XX” é referente a sub-apuração informada no campo 02-IND_AP deste registro.
Campo 11 (G3_08) – Preenchimento: informar o saldo do ICMS, calculado de acordo com os débitos e créditos e os ajustes
da apuração correspondentes às operações informadas para o código de apuração constante do campo IND_AP.
Campo 12 (G3_09) – Validação: o valor informado deve ser igual ao campo G3_08 (saldo devedor do ICMS antes das
deduções do incentivo) subtraído do campo G3_T (Dedução de incentivo da Importação - crédito presumido), por sub-apuração.
----
REGISTRO 1975: GIAF 3 - GUIA DE INFORMAÇÃO E APURAÇÃO DE INCENTIVOS
FISCAIS E FINANCEIROS: IMPORTAÇÃO (SAÍDAS INTERNAS POR FAIXA DE ALÍQUOTA)
Deve existir um Registro 1975 para cada ALIQ_IMP_BASE, ainda que os campos G3_10, G3_11 e G3_12 sejam
iguais a “0” (zero).
Validação do Registro: Não podem ser informados, para um mesmo documento fiscal, dois ou mais registros com o
mesmo conteúdo no campo ALIQ_IMP_BASE.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1975" C 004 - O
02 ALIQ_IMP_BASE Alíquota incidente sobre as importações-base N - 02 O
03 G3_10 Saídas incentivadas de PI N - 02 O
04 G3_11 Importações-base para o crédito presumido N - 02 O
05 G3_12 Crédito presumido nas saídas internas N - 02 O
Observações:
Nível hierárquico - 3
Ocorrência – 1:4
Campo 01 (REG) - Valor Válido: [1975]
Campo 02 (ALIQ_IMP_BASE) - Valores Válidos: [3,50; 6,00; 8,00; 10,00]
Campo 03 (G3_10) – Preenchimento: informar o valor total das saídas internas de produtos incentivados dentro da faixa de
incentivo.
Campo 04 (G3_11) – Preenchimento: informar o valor das importações dos produtos com saídas incentivadas de acordo com
o informado no campo G3_10.
Campo 05 (G3_12) – Validação: o valor informado deve ser menor ou igual ao produto dos ALIQ_IMP_BASE e G3_11
----
REGISTRO 1980: GIAF 4 GUIA DE INFORMAÇÃO E APURAÇÃO DE INCENTIVOS FISCAIS
E FINANCEIROS: CENTRAL DE DISTRIBUIÇÃO (ENTRADAS/SAÍDAS)
Este registro deverá ser apresentado somente pelos contribuintes obrigados por legislação específica de cada UF.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1980" C 004 - O
02 IND_AP Indicador da sub-apuração por tipo de benefício (conforme Tabela N 002* - O
4.7.1)
03 G4_01 Entradas (percentual de incentivo) N - 02 O
04 G4_02 Entradas não incentivadas de PI N - 02 O
05 G4_03 Entradas incentivadas de PI N - 02 O
06 G4_04 Saídas (percentual de incentivo) N - 02 O
07 G4_05 Saídas não incentivadas de PI N - 02 O
08 G4_06 Saídas incentivadas de PI N - 02 O
09 G4_07 Saldo devedor do ICMS antes das deduções do incentivo (PI e N - 02 O
itens não incentivados)
10 G4_08 Crédito presumido nas entradas incentivadas de PI N - 02 O
11 G4_09 Crédito presumido nas saídas incentivadas de PI N - 02 O
12 G4_10 Dedução de incentivo da Central de Distribuição (entradas/saídas) N - 02 O
13 G4_11 Saldo devedor do ICMS após deduções do incentivo N - 02 O
14 G4_12 Índice de recolhimento da central de distribuição N - 02 O
Observações:
Nível hierárquico - 2
Ocorrência – 1
Campo 01 (REG) - Valor Válido: [1980]
Campo 02 (IND_AP) - Valor válido: [02]
Campo 03 (G4_01) – Preenchimento: informar o percentual de incentivo na entrada por transferência da indústria ou produtor,
de acordo com o estabelecido no respectivo decreto concessivo.
Validação: o valor informado deve ser maior ou igual a 3, e menor ou igual a 4.
Campo 04 (G4_02) – Preenchimento: informar o valor total das entradas de produtos incentivados (PI) fora da faixa de
incentivo, conforme estabelecido pelo respectivo decreto concessivo.
Campo 05 (G4_03) – Preenchimento: informar o valor total das entradas de produtos incentivados (PI) dentro da faixa de
incentivo, conforme estabelecido pelo respectivo decreto concessivo.
Campo 06 (G4_04) – Preenchimento: informar o percentual de incentivo na saída interestadual, de acordo com o estabelecido
no respectivo decreto concessivo.
Validação: o valor informado deve ser maior ou igual a 2, e menor ou igual a 4.
Campo 07 (G4_05) – Preenchimento: informar o valor total das saídas de produtos incentivados (PI) fora da faixa de incentivo,
conforme estabelecido pelo respectivo decreto concessivo.
Campo 08 (G4_06) – Preenchimento: informar o valor total das saídas de produtos incentivados (PI) dentro da faixa de
incentivo, conforme estabelecido pelo respectivo decreto concessivo.
Campo 09 (G4_07) – Preenchimento: informar o saldo do ICMS (débitos - créditos) relativo aos produtos com e sem incentivo,
calculado de acordo com as entradas e saídas e os ajustes da apuração no código de apuração informado no campo IND_ESP.
Campo 10 (G4_08) – Validação: o valor informado deve ser menor ou igual que o produto dos campos G4_01 (entradas -
percentual de incentivo) e G4_03 (entradas incentivadas de PI) por sub-apuração.
Campo 11 (G4_09) – Validação: o valor informado deve ser menor ou igual que o produto dos campos G4_04 (saídas -
percentual de incentivo) e G4_06 (saídas incentivadas de PI) por sub-apuração.
Campo 12 (G4_10) – Validação: o valor informado deve ser igual ao campo G4_08 (crédito presumido nas entradas
incentivadas de PI) acrescido do campo G4_09 (crédito presumido nas saídas incentivadas de PI), por sub-apuração. O valor
deste campo deve ser igual ao valor do ajuste informado no campo VL_AJ_APUR do Registro E111, com o COD_AJ_APUR
igual a “UF04XX14”, onde “XX” é referente a sub-apuração informada no campo 02-IND_AP deste registro.
Campo 13 (G4_11) – Validação: o valor informado deve ser igual ao campo G4_07 (saldo devedor do ICMS antes das
deduções do incentivo - PI e itens não incentivados) subtraído do campo G4_10 (dedução de incentivo da Central de
Distribuição), por sub-apuração.
Campo 14 (G4_12) – Preenchimento: informar o índice de recolhimento, conforme estabelecido pelo respectivo decreto
concessivo.
----
REGISTRO 1990: ENCERRAMENTO DO BLOCO 1
Este registro destina-se a identificar o encerramento do bloco 1 e a informar a quantidade de linhas (registros)
existentes no bloco.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "1990" C 004 - O
02 QTD_LIN_1 Quantidade total de linhas do Bloco 1 N - - O
Observações:
Nível hierárquico - 1
Ocorrência – um por Arquivo
Campo 01 (REG) - Valor Válido: [1990]
Campo 02 (QTD_LIN_1) - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco 1 é igual ao valor informado no campo QTD_LIN_1.
