# Bloco D - Versão 3.1.8

----
REGISTRO D001: ABERTURA DO BLOCO D
Este registro deve ser gerado para abertura do bloco D e indica se há informações sobre prestações ou contratações de
serviços de comunicação, transporte interestadual e intermunicipal, com o devido suporte do correspondente documento fiscal.
Validação do Registro: registro obrigatório e único. Se o campo IND_MOV tiver valor igual a 1 (um), só devem ser
informados este registro de abertura e o registro D990, que é o registro de fechamento do Bloco D.
Nº Campo Descrição Tipo Tam Dec Entr
01 REG Texto fixo contendo "D001" C 004 - O
02 IND_MOV Indicador de movimento: C 001 - O
0 - Bloco com dados informados;
1 - Bloco sem dados informados
Observações:
Nível hierárquico - 1
Ocorrência - um por arquivo
Campo 01 (REG) - Valor válido: [D001]
Campo 02 (IND_MOV) - Valores válidos: [0,1]
Preenchimento: quando houver aquisições ou prestações de serviços de comunicação, transporte interestadual e intermunicipal, deve-se gerar esse bloco utilizando a opção 0. Quando não houver aquisições ou prestações de serviços de comunicação, transporte interestadual e intermunicipal, deve-se gerar esse bloco com a opção 1.
----
REGISTRO D100: NOTA FISCAL DE SERVIÇO DE TRANSPORTE (CÓDIGO 07) E CONHECIMENTOS DE TRANSPORTE RODOVIÁRIO DE CARGAS (CÓDIGO 08),
CONHECIMENTOS DE TRANSPORTE DE CARGAS AVULSO (CÓDIGO 8B), AQUAVIÁRIO DE CARGAS (CÓDIGO 09), AÉREO (CÓDIGO 10), FERROVIÁRIO DE CARGAS (CÓDIGO 11), MULTIMODAL DE CARGAS (CÓDIGO 26), NOTA FISCAL DE TRANSPORTE FERROVIÁRIO DE CARGA (CÓDIGO 27), CONHECIMENTO DE TRANSPORTE ELETRÔNICO – CT-e (CÓDIGO 57), CONHECIMENTO DE TRANSPORTE ELETRÔNICO PARA OUTROS SERVIÇOS - CT-e OS (CÓDIGO 67) E BILHETE DE PASSAGEM ELETRÔNICO – BP-e (CÓDIGO 63)
Este registro deve ser apresentado por todos os contribuintes adquirentes ou prestadores dos serviços que utilizem os
documentos especificados.
O campo CHV_CTE passa a ser de preenchimento obrigatório a partir de abril de 2012 em todas as situações, exceto para COD_SIT
= 5 (numeração inutilizada).
A partir da vigência do Ajuste SINIEF 28/2021 e 39/2021 (01/12/2021) deixa de ser obrigatória a informação referente aos documentos fiscais eletrônicos denegados ou com numeração inutilizada.
A partir de janeiro de 2023, os códigos de situação de documento 04 (NF-e ou CT-e denegado) e 05 (NF-e ou CT-e
Numeração inutilizada) da tabela 4.1.2 - Tabela Situação do Documento serão descontinuados.
IMPORTANTE: para documentos de entrada, os campos de valor de imposto/contribuição, base de cálculo e alíquota só devem ser
informados se o adquirente tiver direito à apropriação do crédito (enfoque do declarante).
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos:
1. emissão de terceiros: IND_EMIT+NUM_DOC+COD_MOD+SER+SUB+COD_PART;
2. emissão própria: IND_EMIT+NUM_DOC+COD_MOD+SER+SUB.
3. A partir de 01/01/2014, foi incluído o campo CHV_CTE para compor a chave do registro.
Para cada documento emitido e, portanto, para cada registro D100, obrigatoriamente deve ser apresentado, pelo menos,
um registro D190, observadas as exceções abaixo relacionadas:
Exceção 1: Para documentos com código de situação (campo COD_SIT) cancelado (código “02”), cancelado extemporâneo
(código “03”) ou Conhecimento de Transporte Eletrônico (CT-e) denegado (código “04”), preencher somente os campos REG,
IND_OPER, IND_EMIT, COD_MOD, COD_SIT, SER, SUB, NUM_DOC e CHV_CTE. Para CT-e e CT-e OS com COD_SIT
igual a “05” (numeração inutilizada), devem ser informados todos os campos referidos anteriormente, exceto o campo
CHV_CTE. Demais campos deverão ser apresentados com conteúdo VAZIO “||”. Não deverão ser informados registros filhos.
A partir de janeiro de 2012, no caso de CT-e de emissão própria com código de situação (campo COD_SIT) cancelado (código
“02”) e cancelado extemporâneo (código “03”) deverão ser informados os campos acima citados incluindo ainda a chave do
CT-e. O CT-e OS será válido a partir de abril/2017. O BP-e com evento “Autorizado BP-e de Substituição”, bem como o “BP-
e Substituição” deverão ser escriturados conforme orientação da SEFAZ de domicílio do informante.
Exceção 2: Documentos de transporte complementares e documentos de transporte escriturados extemporaneamente
(campo COD_SIT igual a “06” ou “07”): nesta situação, somente os campos REG, IND_OPER, IND_EMIT, COD_PART,
COD_MOD, COD_SIT, SER, SUB, NUM_DOC, CHV_CTE e DT_DOC são obrigatórios. Os demais campos são facultativos
(se forem preenchidos, serão validados e aplicadas as regras de campos existentes). A apresentação do registro D190 é
obrigatória, devendo ser preenchidos todos os campos obrigatórios. Os demais campos e registros filhos do registro D100 serão
informados, se existirem.
Exceção 3: Documentos de transporte emitidos por regime especial ou norma específica (campo COD_SIT igual a “08”).
Para documentos fiscais emitidos com base em regime especial ou norma específica, deverão ser apresentados os registros
D100 e D190, obrigatoriamente, e os demais registros “filhos”, se estes forem exigidos pela legislação fiscal. Nesta situação,
no registro D100, somente os campos REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD, COD_SIT, SER, SUB,
NUM_DOC e DT_DOC são obrigatórios. A partir do mês de referência abril de 2012 a informação do campo CHV_CTE passa
a ser obrigatória neste caso para modelo 57. O CT-e OS será válido a partir de abril/2017. Os demais campos são facultativos
(se forem preenchidos serão validados e aplicadas as regras de campos existentes).
Exceção 4: Conhecimento de Transporte Eletrônico - CT-e e CT-e OS de emissão própria: neste caso, devem ser apresentados
somente os registros D100 e D190, e se for o caso, informar os registros D195 e D197. Para CT-e, informar os registros D195
e D197 a partir de julho de 2012. O registro D101 deverá ser informado, a partir de janeiro/2016, nas operações interestaduais
que destinem bens e serviços a consumidor final não contribuinte do ICMS, conforme EC 87/15. O CT-e OS será válido a partir
de abril/2017.
A partir de janeiro/2025, para o CT-e Simplificado-modelo 57, conforme estabelecido pelo Ajuste Sinief nº 46/2023, deverão
ser informados os respectivos Registros D130 na escrituração das prestações de saída.
Exceção 5: Escrituração de documentos emitidos por terceiro: os casos de escrituração de documentos fiscais, inclusive CT-
e e CT-e OS, emitidos por terceiros, (como por exemplo, o consórcio constituído nos termos do disposto nos arts. 278 e 279 da
Lei nº 6.404, de 15 de dezembro de 1976), devem ser informados como emissão de terceiros, com o código de situação do
documento igual a “08 - Documento Fiscal emitido com base em Regime Especial ou Norma Específica”. O PVA-EFD-
ICMS/IPI exibirá a mensagem de Advertência para esses documentos.
Obs. Os documentos fiscais emitidos pelas filiais das empresas que possuam inscrição estadual única ou sejam autorizadas
pelos fiscos estaduais a centralizar suas escriturações fiscais deverão ser informados como sendo de emissão própria e código
de situação igual a “00 – Documento regular”.
Exceção 6 - Para bilhete de passagem eletrônico (BP-e), modelo 63: no registro D100, não devem ser informados os campos
COD_PART, SUB, IND_FRT. Os demais campos seguirão a obrigatoriedade definida pelo registro. Os BP-e não devem ser
escriturados nas entradas.
Nº Campo Descrição Tipo Tam Dec Entr Saídas
01 REG Texto fixo contendo "D100" C 004 - O O
02 IND_OPER Indicador do tipo de operação: C 001* - O O
0 - Aquisição;
1 - Prestação
03 IND_EMIT Indicador do emitente do documento fiscal: C 001* - O O
0 - Emissão própria;
1 - Terceiros
04 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - O O
- do prestador de serviço, no caso de aquisição de
serviço;
- do tomador do serviço, no caso de prestação de
serviços.
05 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - O O
Tabela 4.1.1
06 COD_SIT Código da situação do documento fiscal, conforme a N 002* - O O
Tabela 4.1.2
07 SER Série do documento fiscal C 004 - OC OC
08 SUB Subsérie do documento fiscal C 003 - OC OC
09 NUM_DOC Número do documento fiscal N 009 - O O
10 CHV_CTE Chave do Conhecimento de Transporte Eletrônico ou N 044* - OC OC
do Bilhete de Passagem Eletrônico
11 DT_DOC Data da emissão do documento fiscal N 008* - O O
12 DT_A_P Data da aquisição ou da prestação do serviço N 008* - O OC
13 TP_CT-e Tipo de Conhecimento de Transporte Eletrônico N 001* - OC OC
conforme definido no Manual de Integração do CT-e ou
do Bilhete de Passagem Eletrônico conforme definido
no Manual de Integração do BP-e
14 CHV_CTE_REF Chave do Documento Eletrônico Substituído N 044* - OC OC
15 VL_DOC Valor total do documento fiscal N - 02 O O
16 VL_DESC Valor total do desconto N - 02 OC OC
17 IND_FRT Indicador do tipo do frete: C 001* - O OC
0 - Por conta de terceiros;
1 - Por conta do emitente;
2 - Por conta do destinatário;
9 - Sem cobrança de frete.
Obs.: A partir de 01/07/2012 passará a ser:
Indicador do tipo do frete:
0 - Por conta do emitente;
1 - Por conta do destinatário/remetente;
2 - Por conta de terceiros;
9 - Sem cobrança de frete.
18 VL_SERV Valor total da prestação de serviço N - 02 O O
19 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 OC OC
20 VL_ICMS Valor do ICMS N - 02 OC OC
21 VL_NT Valor não-tributado N - 02 OC OC
22 COD_INF Código da informação complementar do documento C 006 - OC OC
fiscal (campo 02 do Registro 0450)
23 COD_CTA Código da conta analítica contábil debitada/creditada C - - OC OC
24 COD_MUN_ORIG Código do município de origem do serviço, conforme a N 007* - OC O
tabela IBGE (Preencher com 9999999, se Exterior)
25 COD_MUN_DEST Código do município de destino, conforme a tabela N 007* - OC O
IBGE (Preencher com 9999999, se Exterior)
Observações:
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor válido: [D100]
Campo 02 (IND_OPER) - Valores válidos: [0,1]
Campo 03 (IND_EMIT) - Valores válidos: [0, 1]
Preenchimento: informar o emitente do documento fiscal. Consideram-se de emissão própria somente os documentos fiscais
emitidos pelo estabelecimento informante (campo CNPJ do registro 0000) da EFD-ICMS/IPI. Documentos emitidos por outros
estabelecimentos, ainda que da mesma empresa, devem ser considerados como documentos emitidos por terceiros, exceto os
emitidos pelas filiais das empresas que possuam inscrição estadual única ou sejam autorizadas pelos fiscos estaduais a
centralizar suas escriturações fiscais, que deverão ser informados como sendo de emissão própria e código de situação igual a
“00 – Documento regular”.
Se a legislação estadual a que estiver submetido o contribuinte obrigá-lo a escriturar conhecimentos de transporte avulsos, este
campo deve ser informado com valor igual a “0” (zero).
Validação: se este campo tiver valor igual a 1 (terceiros), então o campo IND_OPER deve ser igual a 0 (entradas). Se este
campo tiver valor igual a 0 (emissão própria), então o campo IND_OPER poderá ser igual a 0 (entradas) ou 1 (prestação).
Campo 04 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150, exceto quando
se tratar de BP-e (modelo 63).
Campo 05 (COD_MOD) - Valores válidos: [07, 08, 8B, 09, 10, 11, 26, 27, 57, 63 e 67] - Ver tabela reproduzida na subseção
1.4 deste guia.
Campo 06 (COD_SIT) - Valores válidos: [00, 01, 02, 03, 04, 05, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3.
Campo 07 (SER) – Validação: campo de preenchimento obrigatório com três posições para CT-e e CT-e OS, COD_MOD
iguais a “57” e “67”, respectivamente, de emissão própria ou de terceiros. Se não existir Série para CT-e e CT-e OS, informar
000.
Campo 09 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 10 (CHV_CTE) - Preenchimento: informar a chave do conhecimento de transporte eletrônico, para documentos de
COD_MOD iguais a “57”, “63” e “67” de emissão própria ou de terceiros. A chave de acesso do CT-e passa a ser informação
obrigatória para todos os documentos a partir de abril de 2012, exceto para CT-e com numeração inutilizada (COD_SIT = 05).
O CT-e OS será válido a partir de abril/2017.
O BP-e será válido a partir de janeiro/2018.
Validação: é conferido o dígito verificador (DV) da chave do CT-e, do BP-e e do CT-e OS. Este campo é de preenchimento
obrigatório para COD_MOD iguais a “57”, “63” e “67”. Para confirmação inequívoca de que a chave do CT-e, BP-e ou do
CT-e OS corresponde aos dados informados do documento, será comparado o CNPJ base existente na CHV_CTE com o campo
CNPJ base do registro 0000, que corresponde ao CNPJ do informante do arquivo, no caso de IND_EMIT = 0 (emissão própria).
Será verificada a consistência da informação dos campos NUM_DOC e SER com o número do documento e série contidos na
chave do CT-e ou do CT-e OS. Será também comparada a UF codificada na chave do CT-e, BP-e ou do CT-e OS com o campo
UF informado no registro 0000.
Campo 11 (DT_DOC) - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”; excluindo-se
quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Se o Campo “COD_MOD” for igual a 07, 09, 10, 11, 26 ou 27, a data informada deverá ser menor que 01/01/2019.
Campo 12 (DT_A_P) - Preenchimento: informar a data de aquisição ou prestação, conforme a operação, no formato
“ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Se operação de aquisição, este campo deve ser menor ou igual a DT_FIN do registro 0000. Para operações de aquisição de
serviço este valor deve ser maior ou igual à data de emissão (DT_DOC). Para operações de prestação de serviços, este valor,
se informado, deve ser maior ou igual à data de emissão (DT_DOC).
Importante: Se a legislação do ICMS definir que o imposto deve ser apropriado com base na data de emissão dos documentos
fiscais, proceder da seguinte forma: todos os documentos de prestação de serviços de transportes com código de situação de
documento igual a “00” (documento regular) devem ser lançados no período de apuração informado no registro 0000,
considerando a data de emissão do documento, e, se a data de prestação for maior que a data final do período de apuração, este
campo não pode ser preenchido.
Se a legislação do ICMS definir que o imposto deve ser apropriado com base na data de prestação de serviços de transportes,
proceder da seguinte forma: todos os documentos de prestação de serviços com código de situação de documento igual a “00”
(documento regular) devem ser lançados no período de apuração informado no registro 0000, considerando a data da prestação
informada no documento.
Campo 13 (TP_CT-e) Preenchimento: informar o tipo de CT-e, BP-e ou CT-e OS, quando o modelo do documento for “57”,
“63” ou “67”, respectivamente.
Campo 14 (CHV_CTE_REF) – Validação: Quando o campo 13 (TP_CT-e) for igual a “3 ou 6”, informar a chave do
documento substituído. Nas demais situações o campo não deve ser preenchido.
Campo 17 (IND_FRT) – Valores válidos: [0, 1, 2, 9]
Preenchimento: até 30/06/2012, usar o valor 0 (por conta de terceiros) para os casos em que o tomador é diferente do emitente
e destinatário (do documento fiscal que deu origem ao conhecimento de transporte). Após 01/07/2012 usar o valor 2 (por conta
de terceiros).
Tem-se por tomador quem efetuou o contrato junto à transportadora, arcando com o valor do serviço. Somente a este deve ser
enviada a primeira via do conhecimento e só ele terá direito ao crédito.
O campo não deve ser preenchido para “COD_MOD” BP-e (modelo 63), sendo obrigatório para os demais modelos.
Campo 18 (VL_SERV) – Preenchimento: o valor informado, em havendo, deve englobar pedágio e demais despesas.
Validação: Se CT-e simplificado (COD_MOD 57 e TP_CT-e 5 ou 6) e IND_OPER = 1, o valor deve ser igual à soma do
campo VL_FRT do(s) registro(s) D130 existentes.
Campo 22 (COD_INF) - Validação: o valor informado no campo deve existir no registro 0450.
Campo 23 (COD_CTA) - Preenchimento: deve ser a conta credora ou devedora principal, podendo ser informada a conta
sintética (nível acima da conta analítica).
Campo 24 (COD_MUN_ORIG) – Preenchimento: preencher com o código do município de origem do serviço, conforme a
tabela IBGE. Preencher com 9999999, se Exterior. Preencher com “9999998” quando se tratar de CT-e simplificado ou
substituição de CT-e simplificado.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos. Campo
obrigatório nas saídas para todos os modelos (a partir de 2022). Campo obrigatório nas entradas, se
“COD_MOD” do registro D100 for “57”, “63” ou “67”.
Se “COD_MOD” do registro D100 for igual a “63”, o código “COD_MUN_OR” deve pertencer à UF do Registro 0000.
Campo 25 (COD_MUN_DEST) – Preenchimento: preencher com o código do município de destino do serviço, conforme a
tabela IBGE. Preencher com 9999999, se Exterior. Preencher com “9999998” quando se tratar de CT-e simplificado ou
substituição de CT-e simplificado.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos. Campo
obrigatório nas entradas, se “COD_MOD” do registro D100 for “57”, “63” ou “67”.
----
REGISTRO D101: INFORMAÇÃO COMPLEMENTAR DOS DOCUMENTOS FISCAIS
QUANDO DAS PRESTAÇÕES INTERESTADUAIS DESTINADAS A CONSUMIDOR FINAL
NÃO CONTRIBUINTE EC 87/15 (CÓDIGOS 57, 63 e 67)
Este registro deve ser apresentado, a partir de janeiro/2016, para prestar informações complementares do CT-e em
operações interestaduais destinadas a consumidor final NÃO contribuinte de ICMS, segundo dispôs a Emenda Constitucional
87/2015, para o CT-e OS, a partir de abril/2017 e para o BP-e a partir de janeiro/2018. Deverão ser informadas as apurações
nos registros E300 e filhos para as UF de origem e destino da operação.
A partir de janeiro de 2018, este registro não deverá ser apresentado se os dois primeiros dígitos do código informado
nos campos COD_MUN_ORIG e COD_MUN_DEST do Registro D100 forem iguais ou se um dos campos for igual a 9999999
(transporte internacional).
Nas operações em que os dois primeiros dígitos do código informado nos campos COD_MUN_ORIG e
COD_MUN_DEST do Registro D100 forem distintos (transporte interestadual) e diferente de 9999999 (transporte
internacional) e campo COD_MOD = 63, deve ser obrigatória a apresentação do registro D101.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D101" C 004 - O O
02 VL_FCP_UF_DEST Valor total relativo ao Fundo de Combate à N - 02 O O
Pobreza (FCP) da UF de destino
03 VL_ICMS_UF_DES Valor total do ICMS Interestadual para a UF de N - 02 O O
T destino
04 VL_ICMS_UF_REM Valor total do ICMS Interestadual para a UF do N - 02 O O
remetente
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor válido: [D101]
----
REGISTRO D110: ITENS DO DOCUMENTO – NOTA FISCAL DE SERVIÇOS DE
TRANSPORTE (CÓDIGO 07)
Este registro deve ser apresentado para informar os itens das Notas Fiscais de Serviços de Transporte (Código 07)
fornecidas no registro D100.
Validação do Registro: não podem ser informados dois ou mais registros com o mesmo valor para o campo
NUM_ITEM.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D110" C 004 - Não O
02 NUM_ITEM Número sequencial do item no documento fiscal N 003 - Apresentar O
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
04 VL_SERV Valor do serviço N - 02 O
05 VL_OUT Outros valores N - 02 OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor válido: [D110]
Campo 03 (COD_ITEM) - Validação: o valor informado no campo deve existir no Registro 0200.
----
REGISTRO D120: COMPLEMENTO DA NOTA FISCAL DE SERVIÇOS DE TRANSPORTE
(CÓDIGO 07)
Este registro deve ser apresentado para informar o complemento das Notas Fiscais de Serviços de Transporte (Código 07), com
municípios de origem e destino do transporte.
Obs. Para operações que envolvem destinos ou origens em cidades fora do Brasil, os campos COD_MUN_ORIG ou
COD_MUN_DEST dos registros D120, D130, D140, D150, D160, D170 e D180 deverão ser preenchidos com o código
“9999999”.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D120" C 004 - Não O
02 COD_MUN_ORIG Código do município de origem do serviço, N 007* - apresentar O
conforme a tabela IBGE (Preencher com
9999999, se Exterior)
03 COD_MUN_DEST Código do município de destino, conforme a N 007* - O
tabela IBGE (Preencher com 9999999, se
Exterior)
04 VEIC_ID Placa de identificação do veículo C 007 - OC
05 UF_ID Sigla da UF da placa do veículo C 002 - OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor válido: [D120]
Campo 02 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 03 (COD_MUN_DEST) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
----
REGISTRO D130: COMPLEMENTO DO CONHECIMENTO RODOVIÁRIO DE CARGAS
(CÓDIGO 08), DO CONHECIMENTO RODOVIÁRIO DE CARGAS AVULSO (CÓDIGO 8B) E
DO CONHECIMENTO DE TRANSPORTE ELETRÔNICO SIMPLIFICADO (CÓDIGO 57)
Este registro tem por objetivo informar o complemento do Conhecimento de Transporte Rodoviário de Cargas (Código
08), Conhecimento de Transporte de Cargas Avulso (Código 8B) e, a partir de janeiro de 2025, o Conhecimento de Transporte
Eletrônico Simplificado (Código 57, TP_CT-e 5 e 6).
Em relação ao Conhecimento de Transporte Eletrônico Simplificado, este registro tem por objetivo identificar
individualmente cada entrega/prestação abrangida neste documento.
Obs.: Para operações que envolvem destinos ou origens em cidades fora do Brasil, os campos COD_MUN_ORIG ou
COD_MUN_DEST dos registros D120, D130, D140, D150, D160, D170 e D180 deverão ser preenchidos com o código
“9999999”.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D130" C 004 - Não O
02 COD_PART_CONSG Código do participante (campo 02 do C 060 - apresentar OC
Registro 0150):
- consignatário, se houver
03 COD_PART_RED Código do participante (campo 02 do C 060 - OC
Registro 0150):
- redespachado, se houver
04 IND_FRT_RED Indicador do tipo do frete da operação de C 001* - O
redespacho:
0 – Sem redespacho;
1 - Por conta do emitente;
2 - Por conta do destinatário;
9 – Outros.
05 COD_MUN_ORIG Código do município de origem do N 007* - O
serviço, conforme a tabela
IBGE(Preencher com 9999999, se
Exterior)
06 COD_MUN_DEST Código do município de destino, N 007* - O
conforme a tabela IBGE(Preencher com
9999999, se Exterior)
07 VEIC_ID Placa de identificação do veículo C 007 - OC
08 VL_LIQ_FRT Valor líquido do frete N - 02 O
09 VL_SEC_CAT Soma de valores de Sec/Cat (serviços de N - 02 OC
coleta/custo adicional de transporte)
10 VL_DESP Soma de valores de despacho N - 02 OC
11 VL_PEDG Soma dos valores de pedágio N - 02 OC
12 VL_OUT Outros valores N - 02 OC
13 VL_FRT Valor total do frete N - 02 O
14 UF_ID Sigla da UF da placa do veículo C 002 - OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor válido: [D130]
Campo 02 (COD_PART_CONSG) - Preenchimento: preencher com a informação constante no corpo do Conhecimento de
Transporte Rodoviário de Cargas (CTRC) no campo consignatário ou no campo tomador do CT-e simplificado.
Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 (COD_PART_RED) - Preenchimento: preencher com a informação constante no corpo do CTRC ou do CT-e
simplificado no campo redespacho.
Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 04 (IND_FRT_RED) – Preenchimento: inclusive subcontratação, que é a contratação de outra transportadora para
cumprir todo o trecho do frete. Neste caso, para subcontratação, o valor do campo pode ser qualquer um dos valores previstos.
No redespacho ou subcontratação, a subcontratada fornecerá na sua declaração o D100 correspondente ao D130 fornecido pela
empresa que contratou o redespacho ou subcontratou a prestação.
Valores válidos: [0, 1, 2, 9]
Campo 05 (COD_MUN_ORIG) – Preenchimento: Caso trate de item de CT-e simplificado, preencher com o município de
origem da prestação a que se refere este item.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
Campo 06 (COD_MUN_DEST) - Preenchimento: Caso trate de item de CT-e simplificado, preencher com o município de
destino da prestação a que se refere este item.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos
Campo 08 (VL_LIQ_FRT) - Validação: o valor informado no campo deve ser maior que “0” (zero), se o campo IND_FRT
do registro D100 for diferente de 9 (Sem frete).
Campo 13 (VL_FRT) - Validação: o valor informado no campo deve ser maior que “0” (zero), se o campo IND_FRT do
registro D100 for diferente de 9 (Sem frete).
----
REGISTRO D140: COMPLEMENTO DO CONHECIMENTO AQUAVIÁRIO DE CARGAS
(CÓDIGO 09)
Este registro tem por objetivo informar o complemento do Conhecimento de Transporte Aquaviário de Cargas (Código
09).
Obs.: Para operações que envolvem destinos ou origens em cidades fora do Brasil, os campos COD_MUN_ORIG ou
COD_MUN_DEST dos registros D120, D130, D140, D150, D160, D170 e D180 deverão ser preenchidos com o código
“9999999”.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D140" C 004 - Não O
02 COD_PART_CONSG Código do participante (campo 02 do Registro C 060 - apresentar OC
0150):
- consignatário, se houver
03 COD_MUN_ORIG Código do município de origem do serviço, N 007* - O
conforme a tabela IBGE(Preencher com
9999999, se Exterior)
04 COD_MUN_DEST Código do município de destino, conforme a N 007* - O
tabela IBGE(Preencher com 9999999, se
Exterior)
05 IND_VEIC Indicador do tipo do veículo transportador: C 001* - O
0- Embarcação;
1- Empurrador/rebocador
06 VEIC_ID Identificação da embarcação (IRIM ou Registro C - - OC
CPP)
07 IND_NAV Indicador do tipo da navegação: C 001* - O
0- Interior;
1- Cabotagem
08 VIAGEM Número da viagem N - - OC
09 VL_FRT_LIQ Valor líquido do frete N - 02 O
10 VL_DESP_PORT Valor das despesas portuárias N - 02 OC
11 VL_DESP_CAR_DE Valor das despesas com carga e descarga N - 02 OC
SC
12 VL_OUT Outros valores N - 02 OC
13 VL_FRT_BRT Valor bruto do frete N - 02 O
14 VL_FRT_MM Valor adicional do frete para renovação da N - 02 OC
Marinha Mercante
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor válido: [D140]
Campo 02 (COD_PART_CONSG) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 04 (COD_MUN_DEST) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 05 (IND_VEIC) - Valores válidos: [0, 1]
Campo 07 (IND_NAV) - Valores válidos: [0, 1]
----
REGISTRO D150: COMPLEMENTO DO CONHECIMENTO AÉREO (CÓDIGO 10)
Este registro tem por objetivo informar o complemento do Conhecimento de Transporte Aéreo de Cargas (Código 10).
Obs.: Para operações que envolvem destinos ou origens em cidades fora do Brasil, os campos COD_MUN_ORIG ou
COD_MUN_DEST dos registros D120, D130, D140, D150, D160, D170 e D180 deverão ser preenchidos com o código
“9999999”.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D150" C 004 - Não O
02 COD_MUN_ORIG Código do município de origem do serviço, N 007* - apresentar O
conforme a tabela IBGE (Preencher com
9999999, se Exterior)
03 COD_MUN_DEST Código do município de destino, conforme a N 007* - O
tabela IBGE (Preencher com 9999999, se
Exterior)
04 VEIC_ID Identificação da aeronave (DAC) C - - OC
05 VIAGEM Número do vôo. N - - OC
06 IND_TFA Indicador do tipo de tarifa aplicada: C 001* - O
0- Exp.;
1- Enc.;
2- C.I.;
9- Outra
07 VL_PESO_TX Peso taxado N - 02 O
08 VL_TX_TERR Valor da taxa terrestre N - 02 OC
09 VL_TX_RED Valor da taxa de redespacho N - 02 OC
10 VL_OUT Outros valores N - 02 OC
11 VL_TX_ADV Valor da taxa "ad valorem" N - 02 OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor válido: [D150]
Campo 02 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 03 (COD_MUN_DEST) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 06 (IND_TFA) - Valores válidos: [0, 1, 2, 9]
----
REGISTRO D160: CARGA TRANSPORTADA (CÓDIGO 08, 8B, 09, 10, 11, 26 e 27)
Neste registro devem ser apresentados dados sobre o transporte da carga, objeto dos conhecimentos de transporte aqui
especificados.
Obs. Para operações que envolvem destinos ou origens em cidades fora do Brasil, os campos COD_MUN_ORIG ou
COD_MUN_DEST dos registros D120, D130, D140, D150, D160, D170 e D180 deverão ser preenchidos com o código
“9999999”.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D160" C 004 - Não O
02 DESPACHO Identificação do número do despacho C - - apresentar OC
03 CNPJ_CPF_REM CNPJ ou CPF do remetente das mercadorias que N 014 - OC
constam na nota fiscal.
04 IE_REM Inscrição Estadual do remetente das mercadorias C 014 - OC
que constam na nota fiscal.
05 COD_MUN_ORI Código do Município de origem, conforme N 007* - O
tabela IBGE (Preencher com 9999999, se
exterior)
06 CNPJ_CPF_DEST CNPJ ou CPF do destinatário das mercadorias N 014 - OC
que constam na nota fiscal.
07 IE_DEST Inscrição Estadual do destinatário C 014 - OC
das mercadorias que constam na nota fiscal.
08 COD_MUN_DEST Código do Município de destino, conforme N 007* - O
tabela IBGE (Preencher com 9999999, se
Exterior)
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor válido: [D160]
Campo 02 (DESPACHO) – Preenchimento: Informar o número do despacho quando se tratar de transporte ferroviário de
cargas.
Campo 03 (CNPJ_CPF_REM) - Validação: se forem informados 14 caracteres, o campo será validado como CNPJ. Se forem
informados 11 caracteres, o campo será validado como CPF.
Campo 04 (IE_REM) - Validação: a inscrição estadual será validada considerando-se a UF codificada nos dois primeiros
caracteres do campo COD_MUN_ORI. O preenchimento torna-se obrigatório se o Campo COD_MOD for ‘01’ ou ‘55’.
Campo 06 (CNPJ_CPF_DEST) – Preenchimento: informar o CNPJ, com 14 dígitos, ou o CPF, com 11 dígitos, do destinatário.
Validação: se forem informados 14 caracteres, o campo será validado como CNPJ. Se forem informados 11 caracteres, o
campo será validado como CPF.
Campo 07 (IE_DEST) - Validação: a inscrição estadual será validada considerando-se a UF codificada nos dois primeiros
caracteres do campo COD_MUN_DEST
----
REGISTRO D161: LOCAL DA COLETA E ENTREGA (CÓDIGO 08, 8B, 09, 10, 11 e 26)
Este registro tem por objetivo informar o local de coleta e/ou entrega quando esse for diferente do endereço do
remetente e/ou destinatário.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D161" C 004 - Não O
Indicador do tipo de transporte da carga apresentar O
coletada:
0-Rodoviário
1-Ferroviário
02 IND_CARGA 2-Rodo-Ferroviário N 001* -
3-Aquaviário
4-Dutoviário
5-Aéreo
9-Outros
03 CNPJ_CPF_COL Número do CNPJ ou CPF do local da coleta C 014 - OC
04 IE_COL Inscrição Estadual do contribuinte do local de coleta C 014 - OC
Código do Município do local de coleta, O
05 COD_MUN_COL conforme tabela IBGE (Preencher com 9999999, N 007* -
se Exterior)
06 CNPJ_CPF_ENTG Número do CNPJ ou CPF do local da entrega C 014 - OC
Inscrição Estadual do contribuinte do local de OC
07 IE_ENTG C 014 -
entrega
Código do Município do local de entrega, O
08 COD_MUN_ENTG conforme tabela IBGE (Preencher com 9999999, N 007* -
se Exterior)
Observações:
Nível hierárquico - 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [D161]
Campo 02 (IND_CARGA) - Valores Válidos: [0, 1, 2, 3, 4, 5, 9]
Campo 03 (CNPJ_CPF_COL) - Preenchimento: informar o número do CNPJ do contribuinte do local de coleta.
Validação: será conferido o dígito verificador (DV) do CNPJ informado.
Campo 04 (IE_COL) - Validação: a inscrição estadual será validada considerando-se a UF codificada nos dois primeiros
caracteres do campo COD_MUN_COL.
Campo 05 (COD_MUN_COL) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 06 (CNPJ_CPF_ENTG) - Preenchimento: informar o número do CNPJ do contribuinte do local de entrega.
Validação: será conferido o dígito verificador (DV) do CNPJ informado.
Campo 07 (IE_ENTG) - Validação: a inscrição estadual será validada considerando-se a UF codificada nos dois primeiros
caracteres do campo COD_MUN_ENTG.
Campo 08 (COD_MUN_ENTG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
----
REGISTRO D162: IDENTIFICAÇÃO DOS DOCUMENTOS FISCAIS (CÓDIGOS 08, 8B, 09, 10,
11, 26 E 27)
Neste registro devem ser apresentados dados dos documentos fiscais que acobertam a carga transportada, objeto dos
conhecimentos de transporte previstos no registro D160.
Não informar este registro caso o CFOP do conhecimento de transporte seja 5359 ou 6359.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D162" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - apresentar OC
Tabela 4.1.1
03 SER Série do documento fiscal C 004 - OC
04 NUM_DOC Número do documento fiscal N 009 - O
05 DT_DOC Data da emissão do documento fiscal N 008* - OC
06 VL_DOC Valor total do documento fiscal N - 02 OC
07 VL_MERC Valor das mercadorias constantes no documento N - 02 OC
fiscal
08 QTD_VOL Quantidade de volumes transportados N - - O
09 PESO_BRT Peso bruto dos volumes transportados (em kg) N - 02 OC
10 PESO_LIQ Peso líquido dos volumes transportados (em kg) N - 02 OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) – valor válido: [D162]
Campo 02 (COD_MOD) - Valores válidos: [01, 1B, 04 e 55]
Preenchimento: o valor informado deve constar na tabela 4.1.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº
44/2018 e alterações, reproduzida na subseção 1.4 deste guia. O “código” a ser informado não é exatamente o “modelo” do
documento. Exemplo: o código “01” deve ser utilizado para as notas fiscais modelo “01” ou “1A".
Campo 04 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero)
Campo 05 (DT_DOC) - Preenchimento: informar o período de validade das informações contidas neste registro, no formato
“ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao campo DT_FIN do registro 0000.
Campo 07 (VL_MERC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
REGISTRO D170: COMPLEMENTO DO CONHECIMENTO MULTIMODAL DE CARGAS
(CÓDIGO 26)
Este registro tem por objetivo informar o complemento do Conhecimento Multimodal de Cargas (Código 26).
Obs. Para operações que envolvem destinos ou origens em cidades fora do Brasil, os campos COD_MUN_ORIG ou
COD_MUN_DEST dos registros D120, D130, D140, D150, D160, D170 e D180 deverão ser preenchidos com o código
“9999999”.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D170" C 004 - Não O
02 COD_PART_CONSG Código do participante (campo 02 do C 060 - apresentar OC
Registro 0150):
- consignatário, se houver
03 COD_PART_RED Código do participante (campo 02 do C 060 - OC
Registro 0150):
- redespachante, se houver
04 COD_MUN_ORIG Código do município de origem do serviço, N 007* - O
conforme a tabela IBGE(Preencher com
9999999, se Exterior)
05 COD_MUN_DEST Código do município de destino, conforme a N 007* - O
tabela IBGE(Preencher com 9999999, se
Exterior)
06 OTM Registro do operador de transporte C - - O
multimodal
07 IND_NAT_FRT Indicador da natureza do frete: C 001* - O
0- Negociável;
1- Não negociável
08 VL_LIQ_FRT Valor líquido do frete N - 02 O
09 VL_GRIS Valor do gris (gerenciamento de risco) N - 02 OC
10 VL_PDG Somatório dos valores de pedágio N - 02 OC
11 VL_OUT Outros valores N - 02 OC
12 VL_FRT Valor total do frete N - 02 O
13 VEIC_ID Placa de identificação do veículo C 007 - OC
14 UF_ID Sigla da UF da placa do veículo C 002 - OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [D170]
Campo 02 (COD_PART_CONSG) - Preenchimento: preencher com a informação constante no corpo do CTRC no campo consignatário.
Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 (COD_PART_RED) - Preenchimento: preencher com a informação constante no corpo do CTRC no campo de
redespacho.
Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 04 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 05 (COD_MUN_DEST) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 06 (OTM) - Preenchimento: número de registro do operador de transporte multimodal junto à ANTT. O valor é
numérico e possui 8 dígitos.
Campo 07 (IND_NAT_FRT) - Valores Válidos: [0, 1]
Preenchimento: o Complemento do Conhecimento Multimodal de Cargas pode ser negociado em instituição financeira, em
um processo semelhante ao desconto de duplicata bancária.
----
REGISTRO D180: MODAIS (CÓDIGO 26)
Este registro tem por objetivo identificar todos os transportadores e seus documentos fiscais emitidos durante o
transporte multimodal.
Obs.: Para operações que envolvem destinos ou origens em cidades fora do Brasil, os campos COD_MUN_ORIG ou
COD_MUN_DEST dos registros D120, D130, D140, D150, D160, D170 e D180 deverão ser preenchidos com o código
“9999999”.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D180" C 004 - Não O
02 NUM_SEQ Número de ordem sequencial do modal N - - apresentar O
03 IND_EMIT Indicador do emitente do documento fiscal: C 001* - O
0 - Emissão própria;
1 - Terceiros
04 CNPJ_CPF_EMIT CNPJ ou CPF do participante emitente do N 014 - O
modal
05 UF_EMIT Sigla da unidade da federação do participante C 002* - O
emitente do modal
06 IE_EMIT Inscrição Estadual do participante emitente do C 014 - OC
modal
07 COD_MUN_ORIG Código do município de origem do serviço, N 007* - O
conforme a tabela IBGE(Preencher com
9999999, se Exterior)
08 CNPJ_CPF_TOM CNPJ/CPF do participante tomador do serviço N 014 - O
09 UF_TOM Sigla da unidade da federação do participante C 002* - O
tomador do serviço
10 IE_TOM Inscrição Estadual do participante tomador do C 014 - OC
serviço
11 COD_MUN_DEST Código do município de destino, conforme a N 007* - O
tabela IBGE(Preencher com 9999999, se
Exterior)
12 COD_MOD Código do modelo do documento fiscal, C 002* - O
conforme a Tabela 4.1.1
13 SER Série do documento fiscal C 004 - O
14 SUB Subsérie do documento fiscal N 003 - OC
15 NUM_DOC Número do documento fiscal N 009 - O
16 DT_DOC Data da emissão do documento fiscal N 008* - O
17 VL_DOC Valor total do documento fiscal N - 02 O
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [D180]
Campo 03 (IND_EMIT) - Valores Válidos: [0, 1]
Campo 04 (CNPJ_CPF_EMIT) - Preenchimento: informar o CNPJ, com 14 dígitos, ou o CPF, com 11 dígitos, do tomador
de serviço.
Validação: se forem informados 14 caracteres, o campo será validado como CNPJ. Se forem informados 11 caracteres, o
campo será validado como CPF. O preenchimento com outra quantidade de caracteres será considerado inválido.
Campo 05 (UF_EMIT) - Validação: o valor informado no campo deve existir na tabela de UF.
Campo 06 (IE_EMIT) – Validação: a inscrição estadual será validada considerando-se a UF informada no campo UF_EMIT
do registro.
Campo 07 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 08 (CNPJ_CPF_TOM) - Preenchimento: informar o CNPJ, com 14 dígitos, ou o CPF, com 11 dígitos, do tomador de
serviço.
Validação: se forem informados 14 caracteres, o campo será validado como CNPJ. Se forem informados 11 caracteres, o
campo será validado como CPF. O preenchimento com outra quantidade de caracteres será considerado inválido.
Campo 09 (UF_TOM) - Validação: o valor informado no campo deve existir na tabela de UF.
Campo 10 (IE_TOM) - Validação: a inscrição estadual será validada considerando-se a UF informada no campo UF_TOM
do registro.
Campo 11 (COD_MUN_DEST) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Campo 15 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 16 (DT_DOC) - Preenchimento: informar a data de emissão do documento fiscal, no formato “ddmmaaaa”, excluindo-
se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao campo DT_FIN do registro 0000.
----
REGISTRO D190: REGISTRO ANALÍTICO DOS DOCUMENTOS (CÓDIGO 07, 08, 8B, 09, 10,
11, 26, 27, 57, 63 e 67)
Este registro tem por objetivo informar as Notas Fiscais de Serviço de Transporte (Código 07) e demais documentos
elencados no título deste registro e especificados no registro D100, totalizados pelo agrupamento das combinações dos valores
de CST, CFOP e Alíquota dos itens de cada documento.
Obs.: Nas operações de entradas, informar o CST sob o enfoque do declarante.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D190" C 004 - O O
02 CST_ICMS Código da Situação Tributária, conforme a tabela N 003* - O O
indicada no item 4.3.1
Código Fiscal de Operação e Prestação, conforme a O O
03 CFOP N 004* -
tabela indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
VL_OPR Valor da operação correspondente à combinação de O O
05 N - 02
CST_ICMS, CFOP, e alíquota do ICMS.
Parcela correspondente ao "Valor da base de cálculo O O
06 VL_BC_ICMS do ICMS" referente à combinação CST_ICMS, N - 02
CFOP, e alíquota do ICMS
Parcela correspondente ao "Valor do ICMS" O O
07 VL_ICMS referente à combinação CST_ICMS, CFOP e N - 02
alíquota do ICMS
08 VL_RED_BC Valor não tributado em função da redução da base de N - 02 O O
cálculo do ICMS, referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
09 COD_OBS Código da observação do lançamento fiscal (campo C 006 - OC OC
02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [D190]
Campo 02 (CST_ICMS) - Preenchimento: Nos documentos fiscais de emissão própria o campo deverá ser preenchido com o
código da Situação Tributária sob o enfoque do declarante. Nas operações de entradas (documentos de terceiros), informar o
CST que constar no documento fiscal de aquisição de serviços. A partir de julho de 2012, nas operações de aquisições de
serviços o CST_ICMS deverá ser informado sob o enfoque do declarante.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, indicada no item
4.3.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações, sendo que o primeiro caractere sempre será
Zero.
O campo VL_RED_BC só pode ser preenchido se os dois últimos dígitos do campo CST_ICMS forem iguais a 20 ou 70. O
primeiro caractere do código do CST deverá ser igual a 0 (zero).
Campo 03 (CFOP) - Preenchimento: informar o código aplicável à prestação de serviço constante no documento. Não podem
ser utilizados códigos que correspondam aos títulos dos agrupamentos de CFOP (códigos com caracteres finais 00 ou 50. Por
exemplo: 5100).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01.
Se o campo IND_OPER do registro D100 for igual a “0” (zero), então o primeiro caractere do CFOP deve ser igual a 1, 2 ou
3. Se campo IND_OPER do registro D100 for igual a “1” (um), então o primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
Campo 06 (VL_BC_ICMS) - Validação: o valor informado deve ser igual ao valor do campo VL_BC_ICMS do registro D100,
pai deste registro D190.
Campo 07 (VL_ICMS) - Validação: o valor informado deve ser igual ao valor do campo VL_ICMS do registro D100, pai
deste registro D190.
Campo 08 (VL_RED_BC) - Validação: o campo VL_RED_BC só pode ser preenchido se o campo CST_ICMS for igual a 20
ou 70.
----
REGISTRO D195: OBSERVAÇÕES DO LANÇAMENTO FISCAL (CÓDIGO 07, 08, 8B, 09, 10,
11, 26, 27, 57, 63 e 67)
Este registro deve ser informado quando, em decorrência da legislação estadual, houver ajustes nos documentos fiscais.
(Exemplo: informações sobre diferencial de alíquota).
Estas informações equivalem às observações que são lançadas na coluna “Observações” dos Livros Fiscais previstos
no Convênio SN/70 – SINIEF, art. 63, I a IV.
Sempre que existir um ajuste por documento deverá, conforme dispuser a legislação estadual, ocorrer uma observação.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo “D195” C 004 - O O
02 COD_OBS Código da observação do lançamento fiscal (campo 02 do C 006 - O O
Registro 0460)
03 TXT_COMPL Descrição complementar do código de observação. C - - OC OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [D195]
Campo 02 (COD_OBS) – Preenchimento: Informar o código da observação do lançamento.
Validação: o código informado deve constar do registro 0460.
Campo 03 (TXT_COMPL) - Preenchimento: utilizado para complementar a observação do lançamento fiscal, quando a
descrição do código do lançamento informado no registro 0460 for de informação genérica.
----
REGISTRO D197: OUTRAS OBRIGAÇÕES TRIBUTÁRIAS, AJUSTES E INFORMAÇÕES DE
VALORES PROVENIENTES DE DOCUMENTO FISCAL
Este registro tem por objetivo detalhar outras obrigações tributárias, ajustes e informações de valores do documento fiscal do
registro D195, que podem ou não alterar o cálculo do valor do imposto.
Os valores de ICMS ou ICMS ST (campo 07-VL_ICMS) serão somados diretamente na apuração, no registro E110,
campo VL_AJ_DEBITOS, campo VL_AJ_CREDITOS ou no campo DEB_ESP e no registro E210, campo
VL_AJ_CREDITOS_ST, campo VL_AJ_DEBITOS_ST ou no campo DEB_ESP_ST, de acordo com a especificação do
TERCEIRO CARACTERE do Código do Ajuste (Tabela 5.3 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018
e alterações).
Obs.: Este registro será utilizado ainda por contribuinte onde a Administração Tributária Estadual exige, por meio de
legislação específica, apuração em separado (sub-apuração). Neste caso o Estado publicará a Tabela 5.3 com códigos que
contenham os dígitos “3”; “4”, “5”, “6”, “7” e “8” no quarto caractere (“Tipos de Apuração de ICMS”), sendo que cada um
dos dígitos possibilitará a escrituração de uma apuração em separado (sub-apuração) no registro 1900 e filhos. Para que haja a
apuração em separado do ICMS de determinadas operações ou itens de mercadorias, os valores do ICMS das prestações terão
de ser estornados da Apuração Normal (E110) e transferidos para as sub-apurações constantes do registro 1900 e filhos por
meio de lançamentos de ajustes neste registro. Isto ocorrerá quando:
1. o terceiro caractere do código de ajuste (tabela 5.3) do reg. D197 for igual a “2 – Estorno de Débito” e
o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gera um ajuste a crédito (campo 07- VL_AJ_CREDITOS) no registro E110 e
também um outro lançamento a débito no registro 1920 (campo 02 -
VL_TOT_TRANSF_DEBITOS_OA) da apuração em separado (sub-apuração) definida no campo 02-
IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4” ou “5”, que deverá coincidir com o
quarto caractere do COD_AJ; e
2. o terceiro caractere do código de ajuste (tabela 5.3) do reg. D197 for igual a “5 – Estorno de Crédito”
e o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gera um ajuste a débito (campo 03- VL_AJ_DEBITOS) no registro E110 e
também um outro lançamento a crédito no registro 1920 (campo 05 -
VL_TOT_TRANSF_CRÉDITOS_OA) da apuração em separado (sub-apuração) que for definida no
campo 02 - IND_APUR_ICMS do registro 1900 por meio dos códigos “3”; “4”, “5”, “6”, “7” e “8”, que
deverá coincidir com o quarto caractere do COD_AJ.
Os valores que gerarem crédito ou débito de ICMS (ou seja, aqueles que não são simplesmente informativos) serão
somados na apuração, assim como os registros D190.
Este registro somente deve ser informado para as UF que publicarem a tabela constante no item 5.3 da Nota Técnica,
instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Nº Campo Descrição Tipo Tam Dec Entr Saídas
01 REG Texto fixo contendo “D197” C 004 - O O
02 COD_AJ Código do ajustes/benefício/incentivo, conforme C 010* - O O
tabela indicada no item 5.3.
03 DESCR_COMPL_AJ Descrição complementar do ajuste do documento C - - OC OC
fiscal
04 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC OC
05 VL_BC_ICMS N - 02 OC OC
Base de cálculo do ICMS ou do ICMS ST
06 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
07 VL_ICMS Valor do ICMS ou do ICMS ST N - 02 OC OC
08 VL_OUTROS Outros valores N - 02 OC OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [D197]
Campo 02 (COD_AJ) - Validação: verifica se o COD_AJ está de acordo com a Tabela da UF do informante do arquivo.
Campo 03 (DESCR_COMPL_AJ) - Preenchimento: Sem prejuízo de outras situações definidas em legislação específica, o
contribuinte deverá fazer a descrição complementar de ajustes (tabela 5.3) sempre que informar códigos genéricos.
Campo 04 (COD_ITEM) - Preenchimento: pode ser informado se o ajuste/benefício for relacionado ao serviço constante na
nota fiscal de serviço de transporte (código 07) de saída. Para demais situações, não preencher.
Campo 07 (VL_ICMS) - Preenchimento: valor do montante do ajuste do imposto. Para ajustes referentes a ICMS ST, o campo
VL_ICMS deve conter o valor do ICMS ST. Os dados que gerarem crédito ou débito (ou seja, aqueles que não são simplesmente
informativos) serão somados na apuração, assim como os registros C190.
Campo 08 (VL_OUTROS) - Preenchimento: preencher com outros valores, quando o código do ajuste for informativo,
conforme Tabela 5.3 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
----
REGISTRO D300: REGISTRO ANALÍTICO DOS BILHETES CONSOLIDADOS DE
PASSAGEM RODOVIÁRIO (CÓDIGO 13), DE PASSAGEM AQUAVIÁRIO (CÓDIGO 14), DE
PASSAGEM E NOTA DE BAGAGEM (CÓDIGO 15) E DE PASSAGEM FERROVIÁRIO
(CÓDIGO 16)
Este registro deve ser apresentado pelos contribuintes prestadores dos serviços de transporte de passageiros e bagagens,
conforme dispuser a legislação estadual. Os documentos fiscais informados no registro D300 não podem ser repetidos no
registro D400.
A consolidação deve ser feita obedecendo à combinação CST, CFOP e Alíquota, considerando o modelo, série e
subsérie. A numeração dos documentos cancelados deve estar inclusa em cada consolidação.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_MOD, SER, SUB, NUM_DOC_INI e NUM_DOC_FIN. Não é permitida a sobreposição de intervalos de
documentos.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D300" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, C 002* - apresentar O
conforme a Tabela 4.1.1
03 SER Série do documento fiscal C 004 - O
04 SUB Subsérie do documento fiscal N 004 - OC
05 NUM_DOC_INI Número do primeiro documento fiscal emitido N 006 - O
(mesmo modelo, série e subsérie)
06 NUM_DOC_FI Número do último documento fiscal emitido N - - O
N (mesmo modelo, série e subsérie)
07 CST_ICMS Código da Situação Tributária, conforme a N 003* - O
Tabela indicada no item 4.3.1
08 CFOP Código Fiscal de Operação e Prestação conforme N 004* - O
tabela indicada no item 4.2.2
09 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
10 DT_DOC Data da emissão dos documentos fiscais N 008* - O
11 VL_OPR Valor total acumulado das operações N - 02 O
correspondentes à combinação de CST_ICMS,
CFOP e alíquota do ICMS, incluídas as despesas
acessórias e acréscimos.
12 VL_DESC Valor total dos descontos N - 02 OC
13 VL_SERV Valor total da prestação de serviço N - 02 O
14 VL_SEG Valor de seguro N - 02 OC
15 VL_OUT DESP Valor de outras despesas N - 02 OC
16 VL_BC_ICMS Valor total da base de cálculo do ICMS N - 02 O
17 VL_ICMS Valor total do ICMS N - 02 O
18 VL_RED_BC Valor não tributado em função da redução da N - 02 O
base de cálculo do ICMS, referente à
combinação de CST_ICMS, CFOP e alíquota do
ICMS.
19 COD_OBS Código da observação do lançamento fiscal C 006 - OC
(campo 02 do Registro 0460)
20 COD_CTA Código da conta analítica contábil C - - OC
debitada/creditada
Observações:
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [D300]
Campo 02 (COD_MOD) - Valores válidos: [13, 14, 15, 16] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 05 (NUM_DOC_INI) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 06 (NUM_DOC_FIN) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (CST_ICMS)- Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde o
1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação: ICMS Normal:
a) se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero);
b) se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos
campos VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
c) se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores ou iguais a “0” (zero).
d) O campo VL_RED_BC só pode ser preenchido se os dois últimos dígitos do campo CST_ICMS
forem iguais a 20, 70 ou 90. O primeiro caractere do código do CST deverá ser igual a 0 (zero)
Campo 08 (CFOP) - Preenchimento: informar o código aplicável à prestação de serviço constante no documento. Não podem
ser utilizados códigos que correspondam aos títulos dos agrupamentos de CFOP (códigos com caracteres finais 00 ou 50. Por
exemplo: 5100).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01.
O primeiro caractere do CFOP deve ser igual a 5.
Campo 10 (DT_DOC) - Preenchimento: informar a data de emissão dos documentos fiscais contidos neste registro; no
formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao valor informado no campo DT_FIN do registro 0000.
Campo 11 (VL_OPR) – Preenchimento: este valor deve corresponder à soma dos campos VL_SERV, VL_SEG e
VL_OUT_DESP, subtraindo o valor do campo VL_DESC.
Validação: o valor informado nesse campo deve ser maior que “0” (zero).
Campo 13 (VL_SERV) – Preenchimento: é o valor do serviço prestado, sem considerar despesas acessórias, seguros e demais
acréscimos.
Validação: o valor informado nesse campo deve ser maior que “0” (zero).
O valor informado neste campo deve ser igual à soma do valor do campo VL_SERV do registro D310 (agrupamento por
município).
Campo 16 (VL_BC_ICMS) - Validação: o valor informado neste campo deve ser igual à soma do valor do campo
VL_BC_ICMS do registro D310 (agrupamento por município).
Campo 17 (VL_ICMS) - Validação: o valor informado neste campo deve ser igual à soma do valor do campo VL_ICMS do
registro D310 (agrupamento por município).
Campo 18 (VL_RED_BC) - Validação: este campo só pode ser preenchido se os dois últimos dígitos do campo 07
(CST_ICMS) forem iguais a 20, 70 ou 90.
----
REGISTRO D301: DOCUMENTOS CANCELADOS DOS BILHETES DE PASSAGEM
RODOVIÁRIO (CÓDIGO 13), DE PASSAGEM AQUAVIÁRIO (CÓDIGO 14), DE PASSAGEM
E NOTA DE BAGAGEM (CÓDIGO 15) E DE PASSAGEM FERROVIÁRIO (CÓDIGO 16).
Este registro tem por objetivo informar os números dos documentos fiscais cancelados no intervalo constante no
registro pai.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D301" C 004 - Não O
02 NUM_DOC_CANC Número do documento fiscal cancelado N - - apresentar O
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D301]
Campo 02 (NUM_DOC_CANC) - Validação: o valor informado nesse campo deve ser maior que “0” (zero).
----
REGISTRO D310: COMPLEMENTO DOS BILHETES (CÓDIGO 13, 14, 15 E 16).
Este registro tem por objetivo agrupar por município de origem os valores dos documentos fiscais resumidos no
registro D300.
Validação do Registro: não podem ser informados dois ou mais registros com o mesmo valor para o campo
COD_MUN_ORIG.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D310" C 004 - Não O
02 COD_MUN_ORIG Código do município de origem do serviço, N 007* - apresentar O
conforme a tabela IBGE
03 VL_SERV Valor total da prestação de serviço N - 02 O
04 VL_BC_ICMS Valor total da base de cálculo do ICMS N - 02 OC
05 VL_ICMS Valor total do ICMS N - 02 OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D310]
Campo 02 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
----
REGISTRO D350: EQUIPAMENTO ECF (CÓDIGOS 2E, 13, 14, 15 e 16).
Este registro tem por objetivo identificar os equipamentos de ECF por todos os contribuintes que emitam Cupom
Fiscal Bilhete de Passagem (Código 2E), Bilhete de Passagem Rodoviário (13), Bilhete de Passagem Aquaviário (14), Bilhete
de Passagem e Nota de Bagagem (15) e Bilhete de Passagem Ferroviário (16).
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D350" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - apresentar O
Tabela 4.1.1
03 ECF_MOD Modelo do equipamento C 020 - O
04 ECF_FAB Número de série de fabricação do ECF C 021 - O
05 ECF_CX Número do caixa atribuído ao ECF N 003 - O
Observações:
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor válido: [D350]
Campo 02 (COD_MOD) - Valores válidos: [2E, 13, 14, 15, 16] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 05 (ECF_CX) - Preenchimento: informar o número do caixa atribuído pelo estabelecimento ao Equipamento
Emissor de Cupom Fiscal.
Validação: o valor informado no campo deve ser maior que “0” (zero).
----
REGISTRO D355: REDUÇÃO Z (CÓDIGOS 2E, 13, 14, 15 e 16).
Este registro deve ser apresentado com as informações da Redução Z de cada equipamento em funcionamento na data
das prestações à qual se refere a redução. Este registro inclui todos os documentos ficais, totalizados na Redução Z, incluindo
as prestações realizadas durante o período de tolerância do Equipamento ECF.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D355" C 004 - Não O
02 DT_DOC Data do movimento a que se refere a Redução N 008* - apresentar O
Z
03 CRO Posição do Contador de Reinício de Operação N 003 - O
04 CRZ Posição do Contador de Redução Z N 006 - O
05 NUM_COO_FIN Número do Contador de Ordem de Operação N 009 - O
do último documento emitido no dia. (Número
do COO na Redução Z)
06 GT_FIN Valor do Grande Total final N - 02 O
07 VL_BRT Valor da venda bruta N - 02 O
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor válido: [D355]
Campo 02 (DT_DOC) - Preenchimento: considerar a data do movimento, que inclui as operações de venda realizadas durante
o período de tolerância do Equipamento ECF, no formato “ddmmaaaa”, sem os caracteres de separação, tais como: ".", "/", "-
".
Validação: o valor informado deve ser menor ou igual à DT_FIN deste arquivo.
Campo 03 (CRO) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 04 (CRZ) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 05 (NUM_COO_FIN) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 06 (GT_FIN) - Validação: o valor deste campo deve ser igual ou maior que o valor do campo VL_BRT.
Campo 07 (VL_BRT) - Preenchimento: valor acumulado no totalizador de venda bruta.
Validação: deve ser igual ao somatório do campo VLR_ACUM_TOT do registro D365 para os valores informados no campo
COD_TOT_PAR do registro D365.
----
REGISTRO D360: PIS E COFINS TOTALIZADOS NO DIA (CÓDIGOS 2E, 13, 14, 15 e 16).
Este registro somente deve ser apresentado para informar os valores de PIS e COFINS totalizados no dia. Os
contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do registro 0000 estão dispensados
do preenchimento deste registro.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D360" C 004 - Não O
02 VL_PIS Valor total do PIS N - 02 apresentar OC
03 VL_COFINS Valor total da COFINS N - 02 OC
Observações:
Nível hierárquico - 4
Ocorrência – 1:1
Campo 01 (REG) - Valor Válido: [D360]
----
REGISTRO D365: REGISTRO DOS TOTALIZADORES PARCIAIS DA REDUÇÃO Z
(CÓDIGOS 2E, 13, 14, 15 e 16).
Este registro deve ser apresentado para discriminar os valores por código de totalizador da Redução Z.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_TOT_PAR e NR_TOT.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D365" C 004 - Não O
02 COD_TOT_PAR Código do totalizador, conforme Tabela C 007 - apresentar O
4.4.6
03 VLR_ACUM_TOT Valor acumulado no totalizador, relativo à N - 02 O
respectiva Redução Z.
04 NR_TOT Número do totalizador quando ocorrer mais N 002 - OC
de uma situação com a mesma carga
tributária efetiva.
05 DESCR_NR_TOT Descrição da situação tributária relativa ao C - - OC
totalizador parcial, quando houver mais de
um com a mesma carga tributária efetiva.
Observações:
Nível hierárquico - 4
Ocorrência - vários (por arquivo)
Campo 01 (REG) - Valor válido: [D365]
Campo 02 (COD_TOT_PAR) - Preenchimento: informar o código de totalizador parcial da Redução Z.
Para totalizadores tributáveis pelo ICMS, o conteúdo deste campo deve ser somente “Tnnnn”, onde “nnnn” corresponde à
alíquota informada no campo ALIQ_ICMS do registro D390. O valor “xx”, do formato “xxTnnnn”, conforme Convênio 80/07,
para código de totalizador tributável pelo ICMS, deve ser informado no campo NR_TOT deste registro.
Validação: o valor informado deve existir na Tabela 4.4.6 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e
alterações, que discrimina os códigos dos Totalizadores Parciais da REDUÇÃO Z, prevista também na subseção 6.6 deste guia.
Campo 03 (VLR_ACUM_TOT) - Preenchimento: informar o valor acumulado no totalizador da situação tributária/alíquota.
Validação: somente para os totalizadores tributáveis pelo ICMS (campo COD_TOT_PAR) deste registro, com valor “Tnnnn”
ou “xxTnnnn”, o valor deste campo deve ser igual à soma do campo VL_BC_ICMS do registro D390 e também deve ser igual
à soma do campo VL_SERV do registro D370.
Campo 04 (NR_TOT) - Validação: o valor “xx”, do formato “xxTnnnn”, conforme Convênio 80/07, para código de totalizador
tributável pelo ICMS, deve ser informado no campo NR_TOT deste registro. Da mesma forma, este campo somente deve ser
preenchido com o número do totalizador parcial quando o campo COD_TOT_PARC for igual a xxTnnnn e houver totalizadores
distintos com a mesma carga tributária efetiva. O valor informado deve ser maior que “0” (zero).
Campo 05 (DESCR_NR_TOT) - Validação: só deve ser preenchido se o campo NR_TOT estiver preenchido.
----
REGISTRO D370: COMPLEMENTO DOS DOCUMENTOS INFORMADOS (CÓDIGOS 13, 14,
15 e 16 e 2E)
Este registro tem por objetivo agrupar por município de origem os valores dos totalizadores parciais da redução Z.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D370" C 004 - Não O
02 COD_MUN_ORIG Código do município de origem do serviço, N 007* - apresentar O
conforme a tabela IBGE
03 VL_SERV Valor total da prestação de serviço N - 02 O
04 QTD_BILH Quantidade de bilhetes emitidos N - - O
05 VL_BC_ICMS Valor total da base de cálculo do ICMS N - 02 OC
06 VL_ICMS Valor total do ICMS N - 02 OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor válido: [D370]
Campo 02 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
Validação de Registro: registro obrigatório quando o valor no campo COD_TOT_PAR, do registro D365, seguir o formato
xxTnnnn, Tnnnn, Fn, In, Nn.
----
REGISTRO D390: REGISTRO ANALÍTICO DO MOVIMENTO DIÁRIO (CÓDIGOS 13, 14, 15,
16 E 2E).
Este registro representa a escrituração dos documentos fiscais emitidos por ECF e totalizados pela combinação de
CST, CFOP e Alíquota.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D390" C 004 - Não O
02 CST_ICMS Código da Situação Tributária, conforme a Tabela N 003* - apresentar O
indicada no item 4.3.1.
03 CFOP Código Fiscal de Operação e Prestação N 004* - O
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
05 VL_OPR Valor da operação correspondente à combinação N - 02 O
de CST_ICMS, CFOP, e alíquota do ICMS,
incluídas as despesas acessórias e acréscimos
06 VL_BC_ISSQN Valor da base de cálculo do ISSQN N - 02 OC
07 ALIQ_ISSQN Alíquota do ISSQN N 006 02 OC
08 VL_ISSQN Valor do ISSQN N - 02 OC
09 VL_BC_ICMS Base de cálculo do ICMS acumulada relativa à N - 02 O
alíquota informada
10 VL_ICMS Valor do ICMS acumulado relativo à alíquota N - 02 O
informada
11 COD_OBS Código da observação do lançamento fiscal C 006 - OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor válido: [D390]
Campo 02 (CST_ICMS) – Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde
o 1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação:
a) se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero);
b) se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
c) se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS
e VL_ICMS deverão ser maiores ou iguais a “0” (zero).
O primeiro caractere do código do CST deverá ser igual a 0 (zero).
Campo 03 (CFOP) - Preenchimento: informar o código aplicável à prestação de serviço constante no documento. Não podem
ser utilizados códigos que correspondam aos títulos dos agrupamentos de CFOP (códigos com caracteres finais 00 ou 50. Por
exemplo: 5100).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01.
O primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
----
REGISTRO D400: RESUMO DE MOVIMENTO DIÁRIO - RMD (CÓDIGO 18).
Este registro deve ser apresentado pelos contribuintes prestadores dos serviços de transporte de passageiros e bagagens
que adotarem o Resumo de Movimento Diário (código 18), exceto se o fisco estadual dispuser de outro modo de escrituração.
Deverão ser informados os RMD que englobam a emissão dos documentos fiscais de Bilhete de Passagem Rodoviário (Código
13), Bilhete de Passagem Aquaviário (Código 14), Bilhete de Passagem Ferroviário (Código 16) e Bilhete de Passagem e Nota
de Bagagem (Código 15), não emitidos por ECF. A informação deverá ser prestada por agências, postos, filiais ou veículos
do estabelecimento que executam serviços de transporte com inscrição centralizada, quando autorizados pelo fisco estadual.
A prestação de serviços de transporte de passageiros e bagagens, realizados por meio de contadores (catracas ou
similar), deve ser informada neste registro.
Os documentos fiscais informados no registro D400 não podem ser repetidos no registro D300.
Para cada registro D400, obrigatoriamente deve ser apresentado, pelo menos, um registro D410, observadas as
exceções abaixo relacionadas:
Exceção 1: Para documentos com código de situação (campo COD_SIT) cancelado (código “02”) ou cancelado extemporâneo
(código “03”), preencher somente os campos REG, COD_SIT, COD_MOD, SER, SUB e NUM_DOC. Demais campos deverão
ser apresentados com conteúdo VAZIO “||”.
Exceção 2: RMD Complementares e RMD Complementares Extemporâneas (campo COD_SIT igual a “06” ou “07”): nesta
situação, somente os campos REG, COD_PART, COD_MOD, COD_SIT, SER, SUB, NUM_DOC e DT_DOC são obrigatórios.
Os demais campos são facultativos (se forem preenchidos, serão validados e aplicadas as regras de campos existentes). Demais
registros filhos deverão ser informados, se houver.
Exceção 3: RMD emitidos por regime especial ou norma específica (campo COD_SIT igual a “08”). Para documentos fiscais
emitidos com base em regime especial ou norma específica, deverá ser apresentado o registro D400, obrigatoriamente, e os
demais registros “filhos”, se estes forem exigidos pela legislação fiscal. Nesta situação, somente os campos REG, COD_PART,
COD_MOD, COD_SIT, SER, SUB, NUM_DOC e DT_DOC são obrigatórios. Os demais campos são facultativos (se forem
preenchidos, serão validados e aplicadas as regras de campos existentes).
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_PART, SER, NUM_DOC e DT_DOC.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D400" C 004 - Não O
02 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - apresentar O
- agência, filial ou posto
03 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - O
Tabela 4.1.1
04 COD_SIT Código da situação do documento fiscal, conforme a N 002* - O
Tabela 4.1.2
05 SER Série do documento fiscal C 004 - OC
06 SUB Subsérie do documento fiscal N 003 - OC
07 NUM_DOC Número do documento fiscal resumo. N 006 - O
08 DT_DOC Data da emissão do documento fiscal N 008* - O
09 VL_DOC Valor total do documento fiscal N - 02 O
10 VL_DESC Valor acumulado dos descontos N - 02 OC
11 VL_SERV Valor acumulado da prestação de serviço N - 02 O
12 VL_BC_ICM Valor total da base de cálculo do ICMS N - 02 OC
S
13 VL_ICMS Valor total do ICMS N - 02 OC
14 VL_PIS Valor do PIS N - 02 OC
15 VL_COFINS Valor da COFINS N - 02 OC
16 COD_CTA Código da conta analítica contábil debitada/creditada C - - OC
Observações:
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [D400]
Campo 02 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 (COD_MOD) - Valor Válido: [18] - – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 04 (COD_SIT) - Valores Válidos: [00, 01, 02, 03, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento (RMD – Código 18) na Subseção 1.3.
Campo 05 (SER) - Preenchimento: Série do RMD – Código 18.
Campo 06 (SUB) - Preenchimento: Subsérie do RMD – Código 18.
Campo 07 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Preenchimento: Número do RMD – Código 18
Campo 08 (DT_DOC) - Preenchimento: informar a data no formato “ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 09 (VL_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 14 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 15 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 16 (COD_CTA) – Preenchimento: informar o código da conta analítica. Exemplos: estoques, receitas, despesas, ativos.
Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
----
REGISTRO D410: DOCUMENTOS INFORMADOS (CÓDIGOS 13, 14, 15 E 16).
Este registro tem por objetivo informar os documentos consolidados no Resumo de Movimento Diário (Código 18).
Neste registro, deverão ser informados os documentos Bilhete de Passagem Rodoviário (Código 13), Bilhete de Passagem
Aquaviário (Código 14), Bilhete de Passagem Ferroviário (Código 16) e Bilhete de Passagem e Nota de Bagagem (Código 15),
não emitidos por ECF. A partir de julho/2012, alterada a obrigatoriedade de apresentação dos registros D410 e D411, nas
operações de saídas, também para o perfil B,, tabela 2.6.1.3.
No caso de uso da catraca, deverão ser seguidas as seguintes orientações:
I. No campo COD_MOD informar o código do documento fiscal que representa o serviço prestado (13, 14, 15 ou
16);
II. No campo SER informar “9999”;
III. Deixar o campo SUB vazio;
IV. A numeração do documento fiscal referenciada no campo NUM_DOC_ INI será sempre 0 (zero);
V. A numeração do documento fiscal referenciada no campo NUM_DOC_FIN informará a quantidade diária de
passageiros de todas as catracas.
VI. O valor no campo DT_DOC deve ser igual ao valor do campo DT_DOC do registro D400
Validação: Campo 05 – o valor informado no campo deve ser maior que “0” (zero), exceto se campo SER deste registro for igual a “9999”,
quando este campo deve ser igual a zero.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_MOD, SER, SUB, NUM_DOC_INI, NUM_DOC_FIN, CST_ICMS, CFOP e ALIQ_ICMS.
O valor no campo DT_DOC deve ser igual ao valor do campo DT_DOC do registro D400.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D410" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, conforme C 002* - apresentar O
a Tabela 4.1.1
03 SER Série do documento fiscal C 004 - O
04 SUB Subsérie do documento fiscal N 003 - OC
05 NUM_DOC_INI Número do documento fiscal inicial (mesmo N 006 - O
modelo, série e subsérie)
06 NUM_DOC_FIN Número do documento fiscal final (mesmo N - - O
modelo, série e subsérie)
07 DT_DOC Data da emissão dos documentos fiscais N 008* - O
08 CST_ICMS Código da Situação Tributária, conforme a Tabela N 003* - O
indicada no item 4.3.1
09 CFOP Código Fiscal de Operação e Prestação N 004* - O
10 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
11 VL_OPR Valor total acumulado das operações N - 02 O
correspondentes à combinação de CST_ICMS,
CFOP e alíquota do ICMS, incluídas as despesas
acessórias e acréscimos.
12 VL_DESC Valor acumulado dos descontos N - 02 OC
13 VL_SERV Valor acumulado da prestação de serviço N - 02 O
14 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS N - 02 OC
15 VL_ICMS Valor acumulado do ICMS N - 02 OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D410]
Campo 02 (COD_MOD) - Valor Válido: [13, 14, 15, 16] - – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 05 (NUM_DOC_INI) - Validação: o valor informado no campo deve ser maior que “0” (zero), exceto se campo SER
for igual “9999” deste registro, quando este campo deve ser igual a zero.
Campo 06 (NUM_DOC_FIN) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (DT_DOC) - Preenchimento: informar a data da emissão dos documentos fiscais, no formato “ddmmaaaa”, sem
separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 08 (CST_ICMS) – Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde
o 1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, constante do Artigo
5º do Convênio SN/70. O primeiro caractere do código do CST deverá ser igual a 0 (zero).
Campo 09 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Anexo do Convênio SN/70.
O primeiro caractere do CFOP deve ser igual a 5 ou 6.
----
REGISTRO D411: DOCUMENTOS CANCELADOS DOS DOCUMENTOS INFORMADOS
(CÓDIGO 13, 14, 15 e 16).
Este registro tem por objetivo informar os números dos documentos fiscais cancelados. A numeração constante do
campo 02 deve estar compreendida no intervalo dos campos NUM_DOC_INI e NUM_DOC_FIN do registro D410.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D411" C 004 - Não O
02 NUM_DOC_CANC Número do documento fiscal cancelado N - - Apresentar O
Observações:
Nível hierárquico - 4
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [D411]
Campo 02 (NUM_DOC_CANC) - Validação: o valor informado no campo deve ser maior que “0” (zero) e estar contido no
intervalo dos documentos informados no registro D410.
----
REGISTRO D420: COMPLEMENTO DOS DOCUMENTOS INFORMADOS (CÓDIGO 13, 14,
15 e 16).
Este registro tem por objetivo agrupar por município de origem os valores resumidos no registro D400.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D420" C 004 - Não O
02 COD_MUN_ORIG Código do município de origem do serviço, N 007* - apresentar O
conforme a tabela IBGE
03 VL_SERV Valor total da prestação de serviço N - 02 O
04 VL_BC_ICMS Valor total da base de cálculo do ICMS N - 02 OC
05 VL_ICMS Valor total do ICMS N - 02 OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D420]
Campo 02 (COD_MUN_ORIG) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos.
----
REGISTRO D500: NOTA FISCAL DE SERVIÇO DE COMUNICAÇÃO (CÓDIGO 21) E NOTA
FISCAL DE SERVIÇO DE TELECOMUNICAÇÃO (CÓDIGO 22).
Este registro tem por objetivo apresentar as notas fiscais de serviços de comunicações. Na aquisição de serviço, será
utilizado por todos os contribuintes; nas prestações de serviço, pelos contribuintes não enquadrados no Convênio ICMS 115/03.
Empresas sujeitas ao disposto no Convênio ICMS 115/03 deverão utilizar este registro para informar os documentos emitidos
nos modelos 21 e 22, nos casos não previstos no referido convênio, se houver.
IMPORTANTE: para documentos de entrada, os campos de valor de imposto/contribuição, base de cálculo e
alíquota só devem ser informados se o adquirente tiver direito à apropriação do crédito (enfoque do declarante).
Para cada registro D500, obrigatoriamente deve ser apresentado, pelo menos, um registro D590, observadas as
exceções abaixo relacionadas:
Exceção 1: Para documentos com código de situação (campo COD_SIT) cancelado (código “02”) ou cancelado extemporâneo
(código “03”), preencher somente os campos REG, IND_OPER, IND_EMIT, COD_MOD, COD_SIT, SER, NUM_DOC e
DT_DOC. Demais campos deverão ser informados com conteúdo VAZIO “||”.
Exceção 2: Notas Fiscais emitidas por regime especial ou norma específica (campo COD_SIT igual a “08”). Para documentos
fiscais emitidos com base em regime especial ou norma específica, deverão ser apresentados os registros D500 e D590,
obrigatoriamente, e os demais registros “filhos”, se estes forem exigidos pela legislação fiscal. Nesta situação, no registro D500,
somente os campos REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD, COD_SIT, SER, NUM_DOC e DT_DOC são
obrigatórios. Os demais campos são facultativos (se forem preenchidos, serão validados e aplicadas as regras de campos
existentes). No registro D590 deverão ser observados os campos obrigatórios.
Exceção 03: Notas Fiscais Complementares e Notas Fiscais Complementares Extemporâneas (campo COD_SIT igual a “06”
ou “07”): nesta situação, somente os campos (do registro D500) REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD,
COD_SIT, SER, NUM_DOC e DT_DOC são obrigatórios. Os demais campos são facultativos (se forem preenchidos, serão
validados e aplicadas as regras de campos existentes). O registro D590 é obrigatório e deverá ser observada a obrigatoriedade
de preenchimento de todos os campos. Os demais campos e registros filhos do registro D500 deverão ser informados, se
existirem.
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos IND_OPER, IND_EMIT, COD_PART, SER, SUB, NUM_DOC e DT_DOC.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D500" C 004 - O O
02 IND_OPER Indicador do tipo de operação: C 001* - O O
0- Aquisição;
1- Prestação
03 IND_EMIT Indicador do emitente do documento fiscal: C 001* - O O
0- Emissão própria;
1- Terceiros
04 COD_PART Código do participante (campo 02 do Registro 0150): C 060 - O O
- do prestador do serviço, no caso de aquisição;
- do tomador do serviço, no caso de prestação.
05 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - O O
Tabela 4.1.1
06 COD_SIT Código da situação do documento fiscal, conforme a N 002* - O O
Tabela 4.1.2
07 SER Série do documento fiscal C 004 - OC OC
08 SUB Subsérie do documento fiscal C 003 - OC OC
09 NUM_DOC Número do documento fiscal N 009 - O O
10 DT_DOC Data da emissão do documento fiscal N 008* - O O
11 DT_A_P Data da entrada (aquisição) ou da saída (prestação do N 008* - OC OC
serviço)
12 VL_DOC Valor total do documento fiscal N - 02 O O
13 VL_DESC Valor total do desconto N - 02 OC OC
14 VL_SERV Valor da prestação de serviços N - 02 O O
15 VL_SERV_NT Valor total dos serviços não-tributados pelo ICMS N - 02 OC O
16 VL_TERC Valores cobrados em nome de terceiros N - 02 OC O
17 VL_DA Valor de outras despesas indicadas no documento N - 02 OC O
fiscal
18 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 OC OC
19 VL_ICMS Valor do ICMS N - 02 OC OC
20 COD_INF Código da informação complementar (campo 02 do C 006 - OC OC
Registro 0450)
21 VL_PIS Valor do PIS N - 02 OC OC
22 VL_COFINS Valor da COFINS N - 02 OC OC
23 COD_CTA Código da conta analítica contábil debitada/creditada C - - OC OC
24 TP_ASSINANTE Código do Tipo de Assinante: N 001* - OC O
1 - Comercial/Industrial
2 - Poder Público
3 - Residencial/Pessoa física
4 - Público
5 - Semi-Público
6 - Outros
Observações: registro obrigatório nas operações de saídas, apenas para documentos emitidos fora do Convênio ICMS nº
115/2003, ou quando dispensados pela SEFAZ da entrega do arquivo previsto naquele convênio.
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [D500]
Campo 02 (IND_OPER) - Valores Válidos: [0,1]
Campo 03 (IND_EMIT) - Valores Válidos: [0,1]
Campo 04 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 05 (COD_MOD) - Valores Válidos: [21, 22] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 06 (COD_SIT) - Valores Válidos: [00, 01, 02, 03, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3.
Campo 09 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 10 (DT_DOC) - Preenchimento: informar a data da emissão dos documentos fiscais, no formato “ddmmaaaa”, sem
separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 11 ( DT_A_P) - Preenchimento: informar a data da entrada ou saída da prestação do serviço, no formato “ddmmaaaa”,
sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 20 (COD_INF) - Validação: o valor informado deve existir no campo COD_INF do registro 0450.
Campo 21 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 22 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 24 (TP_ASSINANTE) - Valores Válidos: [1, 2, 3, 4, 5, 6]
----
REGISTRO D510: ITENS DO DOCUMENTO – NOTA FISCAL DE SERVIÇO DE
COMUNICAÇÃO (CÓDIGO 21) E SERVIÇO DE TELECOMUNICAÇÃO (CÓDIGO 22).
Este registro tem por objetivo informar os itens das Notas Fiscais de Serviços de Comunicação (código 21 da Tabela
Documentos Fiscais do ICMS) e Notas Fiscais de Serviços de Telecomunicação (código 22 da Tabela Documentos Fiscais do
ICMS). Não deve ser informado pelos adquirentes dos serviços.
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos NUM_ITEM, COD_ITEM e COD_CLASS. O primeiro caractere do campo CFOP deve ser o mesmo para todos os
itens do documento.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D510" C 004 - Não O
02 NUM_ITEM Número sequencial do item no documento fiscal N 003 - apresentar O
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
04 COD_CLASS Código de classificação do item do serviço de N 004* - O
comunicação ou de telecomunicação, conforme
a Tabela 4.4.1
05 QTD Quantidade do item N - 03 O
06 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
07 VL_ITEM Valor do item N - 02 O
08 VL_DESC Valor total do desconto N - 02 OC
09 CST_ICMS Código da Situação Tributária, conforme a N 003* - O
Tabela indicada no item 4.3.1
10 CFOP Código Fiscal de Operação e Prestação N 004* - O
11 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 OC
12 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
13 VL_ICMS Valor do ICMS creditado/debitado N - 02 OC
14 VL_BC_ICMS_UF Valor da base de cálculo do ICMS de outras N - 02 OC
UFs
15 VL_ICMS_UF Valor do ICMS de outras UFs N - 02 OC
16 IND_REC Indicador do tipo de receita: C 001* - O
0- Receita própria - serviços prestados;
1- Receita própria - cobrança de débitos;
2- Receita própria - venda de mercadorias;
3- Receita própria - venda de serviço pré-pago;
4- Outras receitas próprias;
5- Receitas de terceiros (co-faturamento);
9- Outras receitas de terceiros
17 COD_PART Código do participante (campo 02 do Registro C 060 - OC
0150) receptor da receita, terceiro da operação,
se houver.
18 VL_PIS Valor do PIS N - 02 OC
19 VL_COFINS Valor da COFINS N - 02 OC
20 COD_CTA Código da conta analítica contábil C - - OC
debitada/creditada
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D510]
Campo 03 (COD_ITEM) - Validação: o valor informado deve existir no campo COD_ITEM do registro 0200.
Campo 04 (COD_CLASS) - Validação: o valor informado no campo deve existir na Tabela de Classificação de itens de
Energia Elétrica, Serviços de Comunicação e Telecomunicação, constante no item 4.4.1 da Nota Técnica, instituída pelo Ato
COTEPE/ICMS nº 44/2018 e alterações.
Campo 06 (UNID) -Preenchimento: o valor informado deve constar no registro 0190, campo UNID.
Campo 07 (VL_ITEM) - Preenchimento: informar o valor total do item (equivalente à quantidade x preço unitário).
Campo 09 (CST_ICMS) - Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde o
1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, constante do Artigo
5º do Convênio SN/70. O primeiro caractere do código do CST deverá ser igual a 0 (zero).
Campo 10 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01.
Não podem ser utilizados os títulos dos agrupamentos de CFOP.
Campo 11 (VL_BC_ICMS) – Validação: Este campo deve ser igual a “0” (zero) caso o valor do Campo IND_REC seja 1, 5
ou 9.
Campo 12 (ALIQ_ICMS) – Validação: Este campo deve ser igual a “0” (zero) caso o valor do Campo IND_REC seja 1, 5 ou
9.
Campo 13 (VL_ICMS) – Validação: Este campo deve ser igual a “0” (zero) caso o valor do Campo IND_REC seja 1, 5 ou 9.
Campo 16 (IND_REC) - Valores Válidos: [0, 1, 2, 3, 4, 5, 9]
Validação: se o valor for 1, 5 ou 9, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser iguais
a “0” (zero).
Campo 17 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 18 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 19 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 20 (COD_CTA) - Preenchimento: deve ser a conta credora ou devedora principal, podendo ser informada a conta
sintética (nível acima da conta analítica).
----
REGISTRO D530: TERMINAL FATURADO.
Este registro tem por objetivo informar o terminal faturado de Nota Fiscal de Serviços de Comunicação (código 21 da
Tabela Documentos Fiscais do ICMS) e Nota Fiscal de Serviços de Telecomunicação (código 22 da Tabela Documentos Fiscais
do ICMS).
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D530" C 004 - Não O
02 IND_SERV Indicador do tipo de serviço prestado: C 001* - apresentar O
0 - Telefonia;
1 - Comunicação de dados;
2 - TV por assinatura;
3 - Provimento de acesso à Internet;
4 - Multimídia;
9 - Outros
03 DT_INI_SERV Data em que se iniciou a prestação do serviço N 008* - OC
04 DT_FIN_SERV Data em que se encerrou a prestação do serviço N 008* - OC
05 PER_FISCAL Período fiscal da prestação do serviço N 006* - O
(MMAAAA)
06 COD_AREA Código de área do terminal faturado C - - OC
07 TERMINAL Identificação do terminal faturado N - - OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D530]
Campo 02 (IND_SERV) - Valores Válidos: [0, 1, 2, 3, 4, 9]
Campo 03 (DT_INI_SERV) - Preenchimento: informar a data em que se iniciou a prestação de serviços, no formato
“ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 04 (DT_FIN_SERV) - Preenchimento: informar a data em que foi encerrada a prestação de serviços, no formato
“ddmmaaaa”, sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 05 (PER_FISCAL) - Preenchimento: informar o período fiscal da prestação do serviço, no formato “mmaaaa”.
----
REGISTRO D590: REGISTRO ANALÍTICO DO DOCUMENTO (CÓDIGO 21 E 22).
Este registro tem por objetivo apresentar a escrituração das Notas Fiscais de Serviços de Comunicação (código 21 da
Tabela Documentos Fiscais do ICMS) e Notas Fiscais de Serviços de Telecomunicação (código 22 da Tabela Documentos
Fiscais do ICMS), prestadas no registro D500 e totalizados pela combinação de CST, CFOP e Alíquota.
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS para o mesmo documento. A combinação CST_ICMS, CFOP e ALIQ_ICMS deve
existir no respectivo registro de itens do C510, quando este registro for exigido.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D590" C 004 - O O
02 CST_ICMS Código da Situação Tributária, conforme a tabela N 003* - O O
indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação, conforme a N 004* - O O
tabela indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
05 VL_OPR Valor da operação correspondente à combinação de N - 02 O O
CST_ICMS, CFOP, e alíquota do ICMS, incluídas as
despesas acessórias e acréscimos
06 VL_BC_ICMS Parcela correspondente ao "Valor da base de cálculo N - 02 O O
do ICMS" referente à combinação CST_ICMS,
CFOP, e alíquota do ICMS
07 VL_ICMS Parcela correspondente ao "Valor do ICMS" N - 02 O O
referente à combinação CST_ICMS, CFOP, e
alíquota do ICMS
08 VL_BC_ICMS_UF Parcela correspondente ao valor da base de cálculo N - 02 O O
do ICMS de outras UFs, referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
09 VL_ICMS_UF Parcela correspondente ao valor do ICMS de outras N - 02 O O
UFs, referente à combinação de CST_ICMS, CFOP,
e alíquota do ICMS.
10 VL_RED_BC Valor não tributado em função da redução da base de N - 02 O O
cálculo do ICMS, referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
11 COD_OBS Código da observação (campo 02 do Registro 0460) C 006 - OC OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D590]
Campo 02 (CST_ICMS) - Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde o
1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, constante do Artigo
5º do Convênio SN/70. O primeiro caractere do código do CST deverá ser igual a 0 (zero).
Campo 03 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme anexo do Convênio SN/70.
Se o campo IND_OPER do registro D500 for igual a “0” (zero), então o primeiro caractere do CFOP deve ser igual a 1, 2 ou
3. Se campo IND_OPER do registro D500 for igual a “1” (um), então o primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
Campo 05 (VL_OPR) - Preenchimento: Na combinação de CST_ICMS, CFOP e ALIQ_ICMS, informar neste campo o valor
dos serviços e outras despesas acessórias, subtraído o desconto incondicional.
Campo 06 (VL_BC_ICMS) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_BC_ICMS dos registros D510 (itens), se existirem, que possuam a mesma combinação dos campos CST_ICMS, CFOP e
ALIQ_ICMS deste registro.
Campo 07 (VL_ICMS) - Preenchimento: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_ICMS dos registros D510 (itens), que possuam a mesma combinação de CST, CFOP e Alíquota deste registro.
Campo 10 (VL_RED_BC) – Preenchimento: o valor deste campo só pode ser preenchido se os dois últimos dígitos do campo
CST_ICMS forem iguais a 20, 70 ou 90.
Validação: o valor informado neste campo deve ser maior que “0” (zero), se os dois últimos dígitos do campo CST_ICMS
forem iguais a 20 ou 70.
Campo 11 (COD_OBS) - Validação: o valor informado neste campo deve existir no campo COD_OBS do registro 0460.
Preenchimento: informar o código da observação.
----
REGISTRO D600: CONSOLIDAÇÃO DA PRESTAÇÃO DE SERVIÇOS - NOTAS DE SERVIÇO
DE COMUNICAÇÃO (CÓDIGO 21) E DE SERVIÇO DE TELECOMUNICAÇÃO (CÓDIGO 22).
Este registro tem por objetivo consolidar as Notas Fiscais de Serviço de Comunicação (Código 21 da Tabela
Documentos Fiscais do ICMS) e Notas Fiscais de Serviço de Telecomunicação (Código 22 da Tabela Documentos Fiscais do
ICMS) para empresas não obrigadas ao Convênio ICMS 115/2003. Este registro deve ser fornecido apenas para prestações de
saída.
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos COD_MOD, COD_MUN, SER, SUB, COD_CONS e DT_DOC.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D600" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - apresentar O
Tabela 4.1.1
03 COD_MUN Código do município dos terminais faturados, N 007* - O
conforme a tabela IBGE
04 SER Série do documento fiscal C 004 - O
05 SUB Subsérie do documento fiscal N 003 - OC
06 COD_CONS Código de classe de consumo dos serviços de N 002* - O
comunicação ou de telecomunicação, conforme a
Tabela 4.4.4
07 QTD_CONS Quantidade de documentos consolidados neste N - - O
registro
08 DT_DOC Data dos documentos consolidados N 008* - O
09 VL_DOC Valor total acumulado dos documentos fiscais N - 02 O
10 VL_DESC Valor acumulado dos descontos N - 02 OC
11 VL_SERV Valor acumulado das prestações de serviços tributados N - 02 O
pelo ICMS
12 VL_SERV_NT Valor acumulado dos serviços não-tributados pelo N - 02 OC
ICMS
13 VL_TERC Valores cobrados em nome de terceiros N - 02 OC
14 VL_DA Valor acumulado das despesas acessórias N - 02 OC
15 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS N - 02 OC
16 VL_ICMS Valor acumulado do ICMS N - 02 OC
17 VL_PIS Valor do PIS N - 02 OC
18 VL_COFINS Valor da COFINS N - 02 OC
Observações: registro obrigatório nas operações de saídas, apenas para documentos emitidos fora do Convênio ICMS nº
115/2003, ou quando dispensados pela SEFAZ da entrega do arquivo previsto naquele convênio.
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [D600]
Campo 02 (COD_MOD) - Valores Válidos: [21, 22]
Preenchimento: informar o código do modelo do documento fiscal, conforme a Tabela 4.1.1 - – Ver tabela reproduzida na
subseção 1.4 deste guia.
Campo 03 (COD_MUN) - Preenchimento: informar o código do município dos terminais faturados.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
Campo 06 (COD_CONS) - Validação: o valor informado no campo deve existir na Tabela 4.4.4 da Nota Técnica, instituída
pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 07 (QTD_CONS) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 08 (DT_DOC) - Preenchimento: informar a data dos documentos consolidados, no formato “ddmmaaaa”, sem os
separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo 05 (DT_FIN) do registro 0000.
Campo 17 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 18 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
REGISTRO D610: ITENS DO DOCUMENTO CONSOLIDADO (CÓDIGO 21 E 22).
Este registro tem por objetivo informar os itens das Notas Fiscais de Serviços de Comunicação (código 21 da Tabela
Documentos Fiscais do ICMS) e Notas Fiscais de Serviços de Telecomunicação (código 22 da Tabela Documentos Fiscais do
ICMS) consolidadas no registro D600.
Validação do Registro: o primeiro caractere do CFOP deve ser o mesmo para todos os itens do documento. Não
podem ser informados dois ou mais registros com o mesmo valor para o campo COD_ITEM, na combinação COD_ITEM,
CST_ICMS, CFOP e ALIQ_ICMS.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D610" C 004 - Não O
Código de classificação do item do serviço de apresentar
02 COD_CLASS comunicação ou de telecomunicação, N 004* - O
conforme a Tabela 4.4.1
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
04 QTD Quantidade acumulada do item N - 03 O
05 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
06 VL_ITEM Valor acumulado do item N - 02 O
07 VL_DESC Valor acumulado dos descontos N - 02 OC
Código da Situação Tributária, conforme a
08 CST_ICMS N 003* - O
Tabela indicada no item 4.3.1
Código Fiscal de Operação e Prestação
09 CFOP N 004* - O
conforme tabela indicada no item 4.2.2.
10 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
11 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS N - 02 OC
12 VL_ICMS Valor acumulado do ICMS debitado N - 02 OC
Valor da base de cálculo do ICMS de outras
13 VL_BC_ICMS_UF N - 02 OC
UFs
14 VL_ICMS_UF Valor do ICMS de outras UFs N - 02 OC
Valor não tributado em função da redução da
base de cálculo do ICMS, referente à
15 VL_RED_BC N - 02 OC
combinação de CST_ICMS, CFOP e alíquota
do ICMS.
16 VL_PIS Valor acumulado do PIS N - 02 OC
17 VL_COFINS Valor acumulado da COFINS N - 02 OC
18 COD_CTA Código da conta analítica contábil C - - OC
debitada/creditada
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D610]
Campo 02 (COD_CLASS) - Preenchimento: informar o código de classificação do item do serviço de comunicação ou de
telecomunicação, conforme a Tabela 4.4.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 03 (COD_ITEM) - Validação: o valor informado deve constar no campo 02 (COD_ITEM) do registro 0200.
Campo 05 (UNID) - Validação: o valor informado deve existir no registro 0190.
Campo 08 (CST_ICMS) - Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde o
1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, constante do Anexo
do Convênio SN/70 e obedecer às seguintes regras:
ICMS Normal:
se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS
e VL_ICMS deverão ser iguais a “0” (zero);
se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS e
VL_ICMS deverão ser maiores ou iguais a “0” (zero).
O primeiro caractere do código do CST deverá ser igual a 0 (zero).
Campo 09 (CFOP) - Preenchimento: informar o Código Fiscal de Operação e Prestação.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme anexo
Convênio SN/70.
O primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
Campo 16 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 17 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 18 (COD_CTA) - Preenchimento: informar o código da conta analítica contábil debitada/creditada.
----
REGISTRO D690: REGISTRO ANALÍTICO DOS DOCUMENTOS (CÓDIGOS 21 e 22).
Este registro tem por objetivo apresentar a escrituração da consolidação das Notas Fiscais de Serviços de Comunicação
(código 21 da Tabela Documentos Fiscais do ICMS) e Notas Fiscais de Serviços de Telecomunicação (código 22 da Tabela
Documentos Fiscais do ICMS), prestadas no registro D600 e totalizadas pela combinação de CST, CFOP e Alíquota.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS. A combinação CST_ICMS, CFOP e ALIQ_ICMS deve existir no respectivo
registro de itens do (reg. D610), quando este registro for exigido.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "D690" C 004 - Não O
02 CST_ICMS Código da Situação Tributária, conforme a N 003* - apresentar O
tabela indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação, N 004* - O
conforme a tabela indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
05 VL_OPR Valor da operação correspondente à N - 02 O
combinação de CST_ICMS, CFOP, e alíquota
do ICMS, incluídas as despesas acessórias e
acréscimos
06 VL_BC_ICMS Parcela correspondente ao “Valor da base de N - 02 O
cálculo do ICMS” referente à combinação
CST_ICMS, CFOP, e alíquota do ICMS
07 VL_ICMS Parcela correspondente ao "Valor do ICMS" N - 02 O
referente à combinação CST_ICMS, CFOP, e
alíquota do ICMS
VL_BC_ICMS_UF Parcela correspondente ao valor da base de N - 02 O
cálculo do ICMS de outras UFs, referente à
08
combinação de CST_ICMS, CFOP e alíquota
do ICMS.
VL_ICMS_UF Parcela correspondente ao valor do ICMS de N - 02 O
09 outras UFs, referente à combinação de CST
ICMS, CFOP, e alíquota do ICMS.
10 VL_RED_BC Valor não tributado em função da redução da N - 02 O
base de cálculo do ICMS, referente à
combinação de CST_ICMS, CFOP e alíquota
do ICMS.
11 COD_OBS Código da observação do lançamento fiscal C 006 - OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D690]
Campo 02 (CST_ICMS) – Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde
o 1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, constante do Artigo
5º Anexo do Convênio SN/70 e obedecer às seguintes regras:
ICMS Normal:
se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero);
se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS
e VL_ICMS deverão ser maiores ou iguais a “0” (zero).
O primeiro caractere do código do CST deverá ser igual a 0 (zero).
Campo 03 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Anexo do Convênio SN/70.
O primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
Campo 06 (VL_BC_ICMS) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
BC_ICMS dos registros D610 (itens), se existirem, que possuam a mesma combinação de valores dos campos CST_ICMS,
CFOP e ALIQ_ICMS deste registro.
Campo 07 (VL_ICMS) – Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_ICMS dos registros D610 (itens), que possuam a mesma combinação de valores dos campos CST, CFOP e Alíquota deste
registro.
Campo 08 (VL_BC_ICMS_UF) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_BC_ICMS dos registros D610 (itens), que possuam a mesma combinação de valores dos campos CST, CFOP e Alíquota
deste registro.
Campo 09 (VL_ICMS_UF) – Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_ICMS dos registros D610 (itens), que possuam a mesma combinação de valores dos campos CST, CFOP e Alíquota deste
registro.
Campo 10 (VL_RED_BC) - Preenchimento: o valor deste campo só pode ser preenchido se os dois últimos dígitos do campo
CST_ICMS forem iguais a 20, 70 ou 90.
Validação: o valor informado neste campo deve ser maior que “0” (zero), se os dois últimos dígitos do campo CST_ICMS
forem iguais a 20 ou 70.
Campo 11 (COD_OBS) - Validação: O valor informado deve existir no campo COD_OBS do registro 0460.
----
REGISTRO D695: CONSOLIDAÇÃO DA PRESTAÇÃO DE SERVIÇOS – NOTAS DE SERVIÇO
DE COMUNICAÇÃO (CÓDIGO 21) E DE SERVIÇO DE TELECOMUNICAÇÃO (CÓDIGO 22)
(EMPRESAS OBRIGADAS À ENTREGA DOS ARQUIVOS PREVISTOS NO CONVÊNIO ICMS
115/03).
Este registro tem por objetivo apresentar a consolidação das Notas Fiscais de Serviços de Comunicação (código 21 da
Tabela Documentos Fiscais do ICMS) e Notas Fiscais de Serviços de Telecomunicação (código 22 da Tabela Documentos
Fiscais do ICMS) pelas empresas obrigadas ao Convênio ICMS 115/2003.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_MOD, SER, NRO_ORD_INI e NRO_ORD_FIN. Não pode ocorrer sobreposição de intervalos para a mesma
série.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D695" C 004 - O
Código do modelo do documento fiscal, Não O
02 COD_MOD C 002* -
conforme a Tabela 4.1.1. apresentar
03 SER Série do documento fiscal C 004 - O
04 NRO_ORD_INI Número de ordem inicial N 009 - O
05 NRO_ORD_FIN Número de ordem final N 009 - O
Data de emissão inicial dos documentos / Data O
06 DT_DOC_INI N 008* -
inicial de vencimento da fatura
Data de emissão final dos documentos / Data O
07 DT_DOC_FIN N 008* -
final do vencimento da fatura
08 NOM_MEST Nome do arquivo Mestre de Documento Fiscal C 033 - O
Chave de codificação digital do arquivo Mestre O
09 CHV_COD_DIG C 032 -
de Documento Fiscal
Observações:
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [D695]
Campo 02 (COD_MOD) - Valores Válidos: [21, 22]
Preenchimento: informar o código do modelo do documento fiscal, conforme a Tabela 4.1.1. – Ver tabela reproduzida na
subseção 1.4 deste guia.
Campo 06 (DT_DOC_INI) - Preenchimento: informar a data de emissão inicial dos documentos, no formato “ddmmaaaa”,
sem os separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 07 (DT_DOC_FIN) - Preenchimento: informar a data de emissão final dos documentos, no formato “ddmmaaaa”,
sem os separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 08 (NOM_MEST) - Preenchimento: informar o nome do volume do arquivo mestre de documento fiscal, conforme
Convênio ICMS 115/03. Até 31/12/2016, o campo tinha tamanho 015.
Campo 09 (CHV_COD_DIG) - Preenchimento: informar a chave de codificação digital do arquivo mestre de documento
fiscal, conforme Parágrafo Único da Cláusula Quinta do Convênio ICMS 115/2003. Informar sempre o hash do arquivo extraído
(Convênio ICMS 52/05) entregue na UF do tomador de serviços quando diferente do prestador.
----
REGISTRO D696: REGISTRO ANALÍTICO DOS DOCUMENTOS (CÓDIGO 21 E 22).
Este registro representa a escrituração da consolidação das Notas Fiscais de Serviços de Comunicação (código 21 da
Tabela Documentos Fiscais do ICMS) e das Notas Fiscais de Serviços de Telecomunicação (código 22 da Tabela Documentos
Fiscais do ICMS) informadas no registro D695 e totalizadas pela combinação de CST, CFOP e Alíquota, em conformidade
com os documentos constantes dos arquivos referentes ao Convênio ICMS nº 115/03.
Nos casos de Serviços não-medidos – TV por Assinatura (Convênio ICMS nº 52/05), os valores apresentados neste
registro (campos VL_BC_ICMS, VL_ICMS, VL_BC_ICMS_UF e VL_ICMS_UF) não refletem os valores de ICMS devidos
a cada UF, sendo apenas as totalizações dos documentos fiscais constantes dos arquivos a que se refere o Convênio ICMS nº
115/03.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D696" C 004 - Não O
Código da Situação Tributária, conforme a tabela N 003* - Apresentar O
02 CST_ICMS
indicada no item 4.3.1
Código Fiscal de Operação e Prestação, conforme a O
03 CFOP N 004* -
tabela indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
VL_OPR Valor da operação correspondente à combinação de O
05 CST_ICMS, CFOP, e alíquota do ICMS, incluídas as N - 02
despesas acessórias e acréscimos
Parcela correspondente ao "Valor da base de cálculo O
06 VL_BC_ICMS do ICMS" referente à combinação CST_ICMS, N - 02
CFOP, e alíquota do ICMS
Parcela correspondente ao "Valor do ICMS" O
07 VL_ICMS referente à combinação CST_ICMS, CFOP, e N - 02
alíquota do ICMS
Parcela correspondente ao valor da base de cálculo O
VL_BC_ICMS_
08 do ICMS de outras UFs, referente à combinação de N - 02
UF
CST_ICMS, CFOP e alíquota do ICMS
Parcela correspondente ao valor do ICMS de outras O
09 VL_ICMS_UF UFs, referente à combinação de CST_ICMS, CFOP, N - 02
e alíquota do ICMS
10 VL_RED_BC Valor não tributado em função da redução da base de N - 02 O
cálculo do ICMS, referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
11 COD_OBS Código da observação do lançamento fiscal (campo C 006 - OC
02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D696]
Campo 02 (CST_ICMS) – Preenchimento: o código de Situação Tributária é composto de três dígitos na forma ABB, onde
o 1º dígito deve ser sempre 0 (zero), para este registro, e os 2º e 3º dígitos indicam a tributação pelo ICMS, com base na Tabela
B constante no Anexo do Convênio SN/70.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, constante do Anexo
do Convênio SN/70 e obedecer às seguintes regras:
ICMS Normal:
a) se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero);
b) se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
c) se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores ou iguais a “0” (zero).
Campo 03 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme anexo do Convênio SN/70.
Validação: O primeiro caractere do CFOP deve ser igual a 5 ou 6.
Campo 06 (VL_BC_ICMS) – Preenchimento (Orientações exclusivas para empresas prestadoras de serviços de TV por
assinatura – via satélite):
1. Na unidade federada do prestador de serviços: informar o valor correspondente ao somatório da base de cálculo
utilizada de todos os documentos do volume do arquivo referente ao Convênio ICMS nº 115/03.
2. Na unidade federada do tomador dos serviços: informar o valor correspondente ao somatório da base de cálculo
utilizada dos documentos emitidos referentes a clientes da UF do tomador de serviços e constantes do volume do
arquivo extraído, citado no Convênio ICMS nº 52/05.
Campo 07 (VL_ICMS) – Preenchimento (Orientações exclusivas para empresas prestadoras de serviços de TV por assinatura
– via satélite):
1. na unidade federada do prestador de serviços: informar o valor correspondente ao somatório dos valores de ICMS de
todos os documentos do volume do arquivo referente ao Convênio ICMS nº 115/03.
2. na unidade federada do tomador dos serviços: informar o valor correspondente ao somatório dos valores de ICMS dos
documentos emitidos referentes a clientes da UF do tomador de serviços e constantes do volume do arquivo extraído,
citado no Convênio ICMS nº 52/05.
Campo 08 (VL_BC_ICMS_UF) – Preenchimento (Orientações exclusivas para empresas prestadoras de serviços de TV por
assinatura – via satélite): Informar somente na unidade federada do prestador de serviços - informar o valor correspondente ao
somatório da base de cálculo utilizada de todos os documentos emitidos para clientes situados nas demais UFs e constantes do
volume do arquivo citado no Convênio ICMS nº 115/03.
Preencher com Zero quando for EFD-ICMS/IPI da UF do tomador de serviços.
Campo 09 (VL_ICMS_UF) – Preenchimento (Orientações exclusivas para empresas prestadoras de serviços de TV por
assinatura – via satélite): Informar somente na unidade federada do prestador de serviços - informar o valor correspondente ao
somatório do valor do ICMS de todos os documentos emitidos para clientes situados nas demais UFs e constantes do volume
do arquivo citado no Convênio ICMS nº 115/03.
Preencher com Zero quando for EFD-ICMS/IPI da UF do tomador de serviços.
Campo 10 (VL_RED_BC) – Validação: o valor informado neste campo deve ser maior que “0” (zero) se os dois últimos
dígitos do campo CST_ICMS forem iguais a 20 ou 70.
Campo 11 (COD_OBS) - Validação: o valor informado deve existir no campo COD_OBS do registro 0460.
----
REGISTRO D697: REGISTRO DE INFORMAÇÕES DE OUTRAS UFs, RELATIVAMENTE
AOS SERVIÇOS “NÃO-MEDIDOS” DE TELEVISÃO POR ASSINATURA VIA SATÉLITE.
Este registro deve ser apresentado para a UF do prestador de serviços pelas empresas do setor para informar os valores
da base de cálculo e o valor de ICMS, totalizados por UF dos tomadores de serviços, conforme documentos emitidos e
constantes dos arquivos do Convênio ICMS nº 115/03.
Nos casos de Serviços não-medidos – TV por Assinatura (Convênio ICMS nº 52/05), os valores apresentados neste
registro não refletem os valores de ICMS devidos a cada UF, sendo apenas as totalizações dos documentos fiscais constantes
dos arquivos a que se refere o Convênio ICMS nº 115/03. O valor de ICMS devido será o demonstrado nos registros de apuração.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "D697" C 004 - O
02 UF Sigla da unidade da federação C 002* - Não O
03 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 apresentar O
04 VL_ICMS Valor do ICMS N - 02 O
Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D697]
Campo 02 (UF) - Validação: o valor deve ser a sigla de uma unidade da federação (UF) válida.
Campo 03 (VL_BC_ICMS) – Preenchimento: informar o somatório dos valores de base de cálculo de ICMS de todos os
documentos emitidos para a UF informada no campo 02, incluída a parcela correspondente à unidade federada do prestador de
serviços (Convênio ICMS nº 52/05).
Campo 04 (VL_ICMS) – Preenchimento: informar o somatório dos valores de ICMS correspondentes aos documentos
emitidos para assinantes da UF informada no campo 02. O valor efetivo de ICMS a recolher a cada uma das unidades federadas
será demonstrado nos registros de apuração.
----
REGISTRO D700: NOTA FISCAL FATURA ELETRÔNICA DE SERVIÇOS DE
COMUNICAÇÃO – NFCom (CÓDIGO 62).
Este registro tem por objetivo escriturar notas de comunicação individualizadas, de entradas e saídas. As notas normais
de saída - emitidas com a tag finalidade de emissão com valor 0 - devem ser escrituradas neste registro quando não for
obrigatório escriturá-las de forma consolidada.
Nos casos em que a escrituração das notas de saída for definida pela legislação da UF com a escrituração consolidada, apenas
as notas de entrada, de substituição e de ajuste serão escrituradas individualmente.
As notas canceladas não devem ser escrituradas. De acordo com o Manual de Orientação ao Contribuinte (MOC) da
NFCom, o prazo para cancelamento de notas é limitado ao quinto dia após o mês da emissão (120 horas). Esse limite foi
estabelecido de forma que as notas emitidas indevidamente, ou com erro de valores, sejam canceladas antes de iniciada a
apuração e a escrituração digital dos livros de entrada e de saída. Por isso, a formação do arquivo de EFD deve ocorrer após a
conclusão desse processo com o cancelamento e a eventual emissão de outra nota.
Nas entradas, a informação dos campos VL_DOC, VL_DESC, VL_SERV, VL_SERV_NT, VL_TERC e VL_DA não
deve levar em conta os serviços com cClass 110, 120 e 130.
IMPORTANTE: para documentos de entrada, os campos de valor de imposto, base de cálculo e alíquota só devem ser
informados se o adquirente tiver direito à apropriação do crédito (enfoque do declarante).
A NFCom que contenha apenas itens sem a indicação de Código de Situação Tributária – CST não deve ser escriturada.
Exceção 1: Para as Notas Fiscais emitidas por regime especial ou norma específica (campo COD_SIT igual a “08”), no registro
D700, somente os campos REG, IND_OPER, IND_EMIT, COD_PART (nas entradas), COD_MOD, COD_SIT, SER,
NUM_DOC e DT_DOC são obrigatórios. Os demais campos são facultativos (se forem preenchidos, serão validadas e aplicadas
as regras de campos existentes). No registro D730 deverão ser observados os campos obrigatórios.
0.
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos campos
IND_OPER, IND_EMIT, COD_PART, SER, NUM_DOC e DT_DOC, quando o campo COD_PART for preenchido. Caso
contrário, não podem ser informados dois ou mais registros com a combinação de mesmos valores dos campos IND_OPER,
IND_EMIT, SER, NUM_DOC e DT_DOC.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
1 REG Texto fixo contendo "D700". C 4 - O O
Indicador do tipo de prestação:
2 IND_OPER 0: Entrada C 001* - O O
1: Saída
Indicador do emitente do documento fiscal:
3 IND_EMIT 0: Emissão própria; C 001* - O O
1: Terceiros.
Código do participante (Campo 02 do Registro 0150)
4 COD_PART C 60 - O -
do prestador, no caso de entradas.
Código do modelo do documento fiscal, conforme
5 COD_MOD C 002* - O O
a Tabela 4.1.1.
Código da situação do documento fiscal, conforme
6 COD_SIT N 002* - O O
a Tabela 4.1.2.
7 SER Série do documento fiscal. N 3 - O O
8 NUM_DOC Número do documento fiscal. N 9 - O O
9 DT_DOC Data da emissão do documento fiscal. N 008* - O O
10 DT_E_S Data da entrada ou da saída N 008* - OC -
11 VL_DOC Valor do documento fiscal. N - 2 O O
12 VL_DESC Valor do desconto. N - 2 OC OC
13 VL_SERV Valor dos serviços tributados pelo ICMS. N - 2 O O
Valores cobrados em nome do prestador sem destaque
14 VL_SERV_NT N - 2 OC OC
de ICMS.
15 VL_TERC Valores cobrados em nome de terceiros. N - 2 OC OC
Valor de despesas acessórias indicadas no documento
16 VL_DA N - 2 OC OC
fiscal.
17 VL_BC_ICMS Valor da Base de Cálculo (BC) do ICMS. N - 2 OC OC
18 VL_ICMS Valor do ICMS N - 2 OC OC
Código da informação complementar do documento
19 COD_INF C 6 - OC OC
fiscal (campo 02 do Registro 0450).
20 VL_PIS Valor do PIS/Pasep. N - 2 OC OC
21 VL_COFINS Valor do Cofins. N - 2 OC OC
Chave da Nota Fiscal Fatura de Serviço de
22 CHV_DOCe N 044* - O O
Comunicação Eletrônica.
Finalidade da emissão do documento eletrônico:
0 - NFCom Normal;
23 FIN_DOCe N 001* - O O
3 - NFCom de Substituição;
4 - NFCom de Ajuste;
Tipo de faturamento do documento eletrônico:
0 - Faturamento Normal;
24 TIP_FAT N 001* - O O
1 - Faturamento centralizado;
2 - Cofaturamento
Código do modelo do documento fiscal referenciado,
25 COD_MOD_DOC_REF N 002* - OC OC
conforme a Tabela 4.1.1.
26 CHV_DOCe_REF Chave da nota referenciada. N 044* - OC OC
Código de autenticação digital do registro, campo 36
27 HASH_DOC_REF do registro do Arquivo tipo mestre de documento fiscal, C 32 - OC OC
conforme definido no Convênio 115/2003.
28 SER_DOC_REF Série do documento fiscal referenciado. C 4 - OC OC
29 NUM_DOC_REF Número do documento fiscal referenciado. N 9 - OC OC
Mês e ano da emissão do documento fiscal
30 MES_DOC_REF N 006* - OC OC
referenciado.
Código do município do destinatário conforme a tabela
31 COD_MUN_DEST N 007* - N O
do IBGE.
32 DED Deduções N - 2 OC OC
Nível hierárquico – 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [D700]
Campo 02 (IND_OPER) - Valores Válidos: [0,1]
Campo 03 (IND_EMIT) - Valores Válidos: [0,1]
Campo 04 (COD_PART) - Validação: Obrigatório quando o campo 02 (IND_OPER) tiver valor 0 – Entrada. O valor
informado deve existir no campo COD_PART do registro 0150. Não pode ser informado quando o campo 02 (IND_OPER)
tiver valor 1 – Saída.
Campo 05 (COD_MOD) - Valores Válidos: [62] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 06 (COD_SIT) - Valores Válidos: [00, 08]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3.
Campo 08 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 09 (DT_DOC) - Preenchimento: informar a data da emissão dos documentos fiscais, no formato “ddmmaaaa”, sem
separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 10 (DT_E_S) - Preenchimento: informar a data da entrada ou saída da prestação do serviço, no formato “ddmmaaaa”,
sem separadores de formatação.
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 11 (VL_DOC) – Preenchimento: Antes de 2025: corresponde à soma dos campos VL_SERV, VL_SERV_NT e
VL_TERC subtraído das deduções da NFCom.
Validação: (A partir de 2025) corresponde à soma dos campos VL_SERV, VL_SERV_NT e VL_TERC subtraído do campo
DED.
Campo 12 (VL_DESC) – Preenchimento: informar o valor total dos descontos, conforme preenchido na NFCom.
Campo 13 (VL_SERV) – Preenchimento: informar o valor total dos itens relacionados aos serviços próprios, com destaque
de ICMS, conforme preenchido na NFCom.
Campo 14 (VL_SERV_NT) – Preenchimento: informar o valor total dos itens relacionados aos serviços próprios, sem
destaque de ICMS, conforme preenchido na NFCom.
Campo 15 (VL_TERC) – Preenchimento: informar o valor total das cobranças em nome de terceiros, conforme preenchido
na NFCom.
Campo 16 (VL_DA) – Preenchimento: informar o valor total das despesas acessórias, conforme preenchido na NFCom.
Campo 17 (VL_BC_ICMS) – Preenchimento: informar o valor total da base de cálculo de ICMS.
Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_BC_ICMS do registro D730.
Campo 18 (VL_ICMS) - Preenchimento: informar o valor do ICMS creditado na operação de entrada ou o valor do ICMS
debitado na operação de saída.
Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_ICMS do registro D730.
Campo 20 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 21 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 23 (FIN_DOCe) – Valores Válidos: [0, 3, 4]
Campo 24 (TIP_FAT) – Valores Válidos: [0, 1, 2]
Campo 25 (COD_MOD_DOC_REF) - Valores válidos: [21, 22, 62]
Validação: deve ser informado quando o campo FIN_DOCe for igual a “3 - Substituição”. Não informar nas demais situações.
Campo 26 (CHV_DOCe_REF) – Preenchimento: deve ser informada a chave do documento substituído, se eletrônico. Nos
demais casos, não preencher.
Validação: obrigatório quando COD_MOD_DOC_REF for igual a “62”. Será conferido o dígito verificador (DV) da chave do
documento eletrônico.
Campo 27 (HASH_DOC_REF) - Preenchimento: deve ser preenchido com o código de autenticação digital do registro, campo
36 do registro do Arquivo tipo mestre de documento fiscal, conforme definido no Convênio 115/2003, se o documento
substituído for modelo 21 ou 22 e tenha sido emitido conforme sistemática do Convênio 115/2003.
Validação: Não deve ser informado quando COD_MOD_DOC_REF for diferente de “21” e “22”. Quando
COD_MOD_DOC_REF for igual a “21” ou “22”, é obrigatória a informação simultânea de SER_DOC_REF,
NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF. Se HASH_DOC_REF for informado, este
campo deve ter conteúdo VAZIO “||”.
Campo 28 (SER_DOC_REF) - Preenchimento: série do documento fiscal substituído. Informar zero para série única.
Validação: Não deve ser informado quando COD_MOD_DOC_REF for diferente de “21” e “22”. Quando
COD_MOD_DOC_REF for igual a “21” ou “22”, é obrigatória a informação simultânea de SER_DOC_REF,
NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF. Se HASH_DOC_REF for informado, este
campo deve ter conteúdo VAZIO “||”.
Campo 29 (NUM_DOC_REF) - Preenchimento: número do documento fiscal substituído.
Validação: O valor informado no campo deve ser maior que “0” (zero). Não deve ser informado quando
COD_MOD_DOC_REF for diferente de “21” e “22”. Quando COD_MOD_DOC_REF for igual a “21” ou “22”, é obrigatória
a informação simultânea de SER_DOC_REF, NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF.
Se HASH_DOC_REF for informado, este campo deve ter conteúdo VAZIO “||”.
Campo 30 (MES_DOC_REF) - Preenchimento: mês e ano da emissão do documento fiscal referenciado no formato
“mmaaaa”.
Validação: Não deve ser informado quando COD_MOD_DOC_REF for diferente de “21” e “22”. Quando
COD_MOD_DOC_REF for igual a “21” ou “22”, é obrigatória a informação simultânea de SER_DOC_REF,
NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF. Se HASH_DOC_REF for informado, este
campo deve ter conteúdo VAZIO “||”.
Campo 32 (DED) - Preenchimento: deve ser informado quando houver itens lançados com código do grupo 590, conforme
Tabela de classificação de produtos da NFCom (cClass)
----
REGISTRO D730: REGISTRO ANALÍTICO NOTA FISCAL FATURA ELETRÔNICA DE
SERVIÇOS DE COMUNICAÇÃO – NFCom (CÓDIGO 62).
Este registro tem por objetivo representar a escrituração dos documentos fiscais informados no registro D700
totalizados pela combinação de CST, CFOP e Alíquota de ICMS.
Relativamente às Notas Fiscais Fatura de Serviços de Comunicação Eletrônica (NFCom), não devem ser apresentados
neste registro os itens sem a indicação de Código de Situação Tributária – CST
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS para o mesmo documento.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo " D730" C 004 - O O
02 CST_ICMS Código da Situação Tributária, conforme a tabela N 003* - O O
indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação, conforme a N 004* - O O
tabela indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
05 VL_OPR Valor total dos itens relacionados aos serviços próprios, N - 02 O O
com destaque de ICMS, correspondente à combinação
de CST_ICMS, CFOP, e alíquota do ICMS.
06 VL_BC_ICMS Parcela correspondente ao "Valor da base de cálculo do N - 02 O O
ICMS" referente à combinação CST_ICMS, CFOP, e
alíquota do ICMS
07 VL_ICMS Parcela correspondente ao "Valor do ICMS" referente à N - 02 O O
combinação CST_ICMS, CFOP, e alíquota do ICMS,
incluindo o FCP, quando aplicável, referente à
combinação de CST_ICMS, CFOP e alíquota do ICMS.
08 VL_RED_BC Valor não tributado em função da redução da base de N - 02 O O
cálculo do ICMS, referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
09 COD_OBS Código da observação (campo 02 do Registro 0460) C 006 - OC OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D730]
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao
ICMS, constante do Artigo 5º do Convênio SN/70.
Campo 03 (CFOP) - Preenchimento: nas operações de entradas, devem ser registrados os códigos de operação que
correspondem ao tratamento tributário relativo à destinação do item.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01. Se o campo IND_OPER do registro D700 for igual a “0” (zero), então o primeiro caractere do CFOP deve ser
igual a 1, 2 ou 3. Se campo IND_OPER do registro D700 for igual a “1” (um), então o primeiro caractere do CFOP deve ser
igual a 5, 6 ou 7.
Campo 05 (VL_OPR) - Preenchimento: Na combinação de CST_ICMS, CFOP e ALIQ_ICMS, informar o valor total dos
itens relacionados aos serviços próprios, com destaque de ICMS, conforme preenchido na NFCom.
Campo 06 (VL_BC_ICMS) - Preenchimento: informar a base de cálculo do ICMS, referente à combinação dos campos
CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Campo 07 (VL_ICMS) - Preenchimento: informar o valor do ICMS referente à combinação dos campos CST_ICMS, CFOP
e ALIQ_ICMS deste registro.
Campo 08 (VL_RED_BC) - Preenchimento: informar o valor não tributado em função da redução da base de cálculo do
ICMS, referente à combinação dos campos CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Validação:. O campo VL_RED_BC deve ser maior que zero se o 2º e 3º caracteres do CST_ICMS forem iguais a 20.
Campo 09 (COD_OBS) - Preenchimento: este campo só deve ser informado pelos contribuintes localizados em UF que
determine em sua legislação o seu preenchimento.
Validação: o código informado deve constar do registro 0460.
----
REGISTRO D731: INFORMAÇÕES DO FUNDO DE COMBATE À POBREZA – FCP –
(CÓDIGO 62)
Este registro tem por objetivo prestar informações do Fundo de Combate à Pobreza (FCP), constante na NFCom. Os
valores deste registro são meramente informativos e não são contabilizados na apuração dos registros no bloco E.
A obrigatoriedade e forma de apresentação de cada campo deste registro deve ser verificada junto às unidades
federativas.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D731" C 004 - O O
02 VL_FCP_OP Valor do Fundo de Combate à Pobreza (FCP) vinculado à N - 02 O O
operação própria, na combinação de CST_ICMS, CFOP e
alíquota do ICMS
Observações:
Nível hierárquico – 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [D731]
----
REGISTRO D735: OBSERVAÇÕES DO LANÇAMENTO FISCAL (CÓDIGO 62)
Este registro deve ser informado quando, em decorrência da legislação estadual, houver ajustes nos documentos fiscais.
(Exemplo: informações sobre diferencial de alíquota).
Estas informações equivalem às observações que são lançadas na coluna “Observações” dos Livros Fiscais previstos
no Convênio SN/70 – SINIEF, art. 63, I a IV.
Sempre que existir um ajuste por documento deverá, conforme dispuser a legislação estadual, ocorrer uma observação.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo “D735” C 004 - O O
02 COD_OBS Código da observação do lançamento fiscal (campo 02 do C 006 - O O
Registro 0460)
03 TXT_COMPL Descrição complementar do código de observação. C - - OC OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [D735]
Campo 02 (COD_OBS) – Preenchimento: Informar o código da observação do lançamento.
Validação: o código informado deve constar do registro 0460.
Campo 03 (TXT_COMPL) - Preenchimento: utilizado para complementar a observação do lançamento fiscal, quando a
descrição do código do lançamento informado no registro 0460 for de informação genérica.
----
REGISTRO D737: OUTRAS OBRIGAÇÕES TRIBUTÁRIAS, AJUSTES E INFORMAÇÕES DE
VALORES PROVENIENTES DE DOCUMENTO FISCAL
Este registro tem por objetivo detalhar outras obrigações tributárias, ajustes e informações de valores do documento
fiscal do registro D735, que podem ou não alterar o cálculo do valor do imposto.
Os valores de ICMS (campo 07-VL_ICMS) serão somados diretamente na apuração, no registro E110, campo
VL_AJ_DEBITOS, campo VL_AJ_CREDITOS ou no campo DEB_ESP, de acordo com a especificação do TERCEIRO
CARACTERE do Código do Ajuste (Tabela 5.3 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações).
Este registro será utilizado também por contribuinte para o qual a Administração Tributária Estadual exija, por meio
de legislação específica, apuração em separado (sub-apuração). Neste caso o Estado publicará a Tabela 5.3 com códigos que
contenham os dígitos “3”, “4”, “5”, “6”, “7” e “8” no quarto caractere (“Tipos de Apuração de ICMS”), sendo que cada um
dos dígitos possibilitará a escrituração de uma apuração em separado (sub-apuração) no registro 1900 e filhos. Para que haja a
apuração em separado do ICMS de determinadas operações ou itens de mercadorias, estes valores terão de ser estornados da
Apuração Normal (E110) e transferidos para as sub-apurações constantes do registro 1900 e filhos por meio de lançamentos de
ajustes neste registro. Isto ocorrerá quando:
1. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C737 for igual a “2 – Estorno de Débito” e
o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no campo
07 - VL_ICMS gerará um ajuste a crédito (campo 07- VL_AJ_CREDITOS) no registro E110 e também um
outro lançamento a débito no registro 1920 (campo 02 - VL_TOT_TRANSF_DEBITOS_OA) da apuração
em separado (sub-apuração) definida no campo 02- IND_APUR_ICMS do registro 1900 por meio dos
códigos “3”, “4”, “5”, “6”, “7” e “8”, que deverá coincidir com o quarto caractere do COD_AJ; e
2. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C737 for igual a “5 – Estorno de Crédito”
e o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gerará um ajuste a débito (campo 03- VL_AJ_DEBITOS) no registro E110 e
também um outro lançamento a crédito no registro 1920 (campo 05 -
VL_TOT_TRANSF_CRÉDITOS_OA) da apuração em separado (sub-apuração) que for definida no
campo 02 - IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4” “5”, “6”, “7” e “8”, que
deverá coincidir com o quarto caractere do COD_AJ.
Os valores que gerarem crédito ou débito de ICMS (ou seja, aqueles que não são simplesmente informativos) serão
somados na apuração, assim como os registros D730.
Este registro somente deve ser informado para as UF que publicarem a tabela constante no item 5.3 da Nota Técnica,
instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Nº Campo Descrição Tipo Tam Dec Entr Saídas
01 REG Texto fixo contendo “D737” C 004 - O O
02 COD_AJ Código do ajustes/benefício/incentivo, conforme tabela C 010* - O O
indicada no item 5.3.
03 DESCR_COMPL_AJ Descrição complementar do ajuste do documento fiscal C - - OC OC
04 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC OC
05 VL_BC_ICMS Base de cálculo do ICMS N - 02 OC OC
06 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
07 VL_ICMS Valor do ICMS N - 02 OC OC
08 VL_OUTROS Outros valores N - 02 OC OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [D737]
Campo 02 (COD_AJ) - Validação: verifica se o COD_AJ está de acordo com a Tabela 5.3 da UF do informante do arquivo.
Campo 03 (DESCR_COMPL_AJ) - Preenchimento: Sem prejuízo de outras situações definidas em legislação específica, o
contribuinte deverá fazer a descrição complementar de ajustes (tabela 5.3) sempre que informar códigos genéricos.
Campo 04 (COD_ITEM) - Preenchimento: pode ser informado se o ajuste/benefício for relacionado ao serviço constante na
nota fiscal de serviço de comunicação. O COD_ITEM deverá ser informado no registro 0200.
Campo 07 (VL_ICMS) - Preenchimento: valor do montante do ajuste do imposto. Os dados que gerarem crédito ou débito
(ou seja, aqueles que não são simplesmente informativos) serão somados na apuração, assim como os registros D730.
Campo 08 (VL_OUTROS) - Preenchimento: preencher com outros valores, quando o código do ajuste for informativo,
conforme Tabela 5.3 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
----
REGISTRO D750: ESCRITURAÇÃO CONSOLIDADA DA NOTA FISCAL FATURA
ELETRÔNICA DE SERVIÇOS DE COMUNICAÇÃO - NFCom (CÓDIGO 62)
Este registro deve ser apresentado quando a legislação da UF determinar a escrituração consolidada. A consolidação
deve ser apenas de notas emitidas com a finalidade Normal, emitidas com a tag finalidade de emissão com valor 0, de saída,
que não tenham sido canceladas. Apenas os documentos que se enquadrem na tabela 4.1.2 com o código da situação do
documento igual a 00 - Documento regular podem ser informados nesse registro.
A NFCom que contenha apenas itens sem a indicação de Código de Situação Tributária – CST não deve ser escriturada.
As notas informadas no Registro D700 não devem ser escrituradas de forma consolidada.
As notas a seguir devem ser informadas no Registro D700 e não podem ser informadas nesse registro:
• Notas de ajuste
• Notas de substituição
• Notas que representem operação de entrada
• Notas que tenham ajustes de apuração por documento, utilizando a tabela 5.3
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos COD_MOD, SER, DT_DOC, IND_PREPAGO
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D750" C 004 - - O
Código do modelo do documento fiscal, conforme a - O
02 COD_MOD C 002* -
Tabela 4.1.1
03 SER Série do documento fiscal N 003 - - O
04 DT_DOC Data da emissão dos documentos N 008* - - O
05 QTD_CONS Quantidade de documentos consolidados neste registro N - - - O
Forma de pagamento: - O
06 IND_PREPAGO 0 – pré pago N 001 -
1 – pós pago
07 VL_DOC Valor total dos documentos N - 02 - O
08 VL_SERV Valor dos serviços tributados pelo ICMS. N - 02 - O
Valores cobrados em nome do prestador sem destaque de
09 VL_SERV_NT N - 002 - O
ICMS.
10 VL_TERC Valor total cobrado em nome de terceiros N - 02 - O
11 VL_DESC Valor total dos descontos N - 02 - O
12 VL_DA Valor total das despesas acessórias N - 02 - O
13 VL_BC_ICMS Valor total da base de cálculo do ICMS N - 02 - O
14 VL_ICMS Valor total do ICMS N - 02 - O
15 VL_PIS Valor total do PIS N - 02 - OC
16 VL_COFINS Valor total da COFINS N - 02 - OC
17 DED Deduções N - 02 - OC
Observações:
Nível hierárquico - 2
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D750]
Campo 02 (COD_MOD) - Valores Válidos: [62] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 07 (VL_DOC) – Preenchimento: Antes de 2025: corresponde à soma dos campos VL_SERV, VL_SERV_NT e
VL_TERC subtraído das deduções da NFCom.
Validação: (A partir de 2025) corresponde à soma dos campos VL_SERV, VL_SERV_NT e VL_TERC subtraído do campo
DED.
Campo 08 (VL_SERV) – Preenchimento: informar o valor total dos itens relacionados aos serviços próprios, com destaque
de ICMS, conforme preenchido na NFCom.
Campo 09 (VL_SERV_NT) – Preenchimento: informar o valor total dos itens relacionados aos serviços próprios, sem
destaque de ICMS, conforme preenchido na NFCom.
Campo 10 (VL_TERC) – Preenchimento: informar o valor total das cobranças em nome de terceiros, conforme preenchido
na NFCom.
Campo 11 (VL_DESC) – Preenchimento: informar o valor total dos descontos, conforme preenchido na NFCom.
Campo 12 (VL_DA) – Preenchimento: informar o valor total das despesas acessórias, conforme preenchido na NFCom.
Campo 13 (VL_BC_ICMS) – Preenchimento: informar o valor total da base de cálculo de ICMS.
Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_BC_ICMS do registro D760.
Campo 14 (VL_ICMS) – Preenchimento: informar o valor total do ICMS.
Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_ICMS do registro D760.
Campo 15 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 16 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 17 (DED) - Preenchimento: deve ser informado quando houver itens lançados com código do grupo 590, conforme
Tabela de classificação de produtos da NFCom (cClass)
----
REGISTRO D760: REGISTRO ANALÍTICO DA ESCRITURAÇÃO CONSOLIDADA DA NOTA
FISCAL FATURA ELETRÔNICA DE SERVIÇOS DE COMUNICAÇÃO - NFCom (CÓDIGO 62)
Este registro tem por objetivo representar a escrituração dos documentos fiscais informados no registro D750
totalizados pela combinação de CST, CFOP e Alíquota de ICMS.
Relativamente às Notas Fiscais Fatura de Serviços de Comunicação Eletrônica (NFCom), não devem ser apresentados
neste registro os itens sem a indicação de Código de Situação Tributária – CST
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS para o mesmo documento.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D760" C 004 - O O
02 CST_ICMS Código da Situação Tributária, conforme a tabela indicada N 003* - O O
no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação, conforme a tabela N 004* - O O
indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
05 VL_OPR Valor total dos itens relacionados aos serviços próprios, N - 02 O O
com destaque de ICMS, correspondente à combinação de
CST_ICMS, CFOP, e alíquota do ICMS.
06 VL_BC_ICMS Parcela correspondente ao "Valor da base de cálculo do N - 02 O O
ICMS" referente à combinação CST_ICMS, CFOP, e
alíquota do ICMS
07 VL_ICMS Parcela correspondente ao "Valor do ICMS", incluindo o N - 02 O O
FCP, quando aplicável, referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
08 VL_RED_BC Valor não tributado em função da redução da base de N - 02 O O
cálculo do ICMS, referente à combinação de CST_ICMS,
CFOP e alíquota do ICMS.
09 COD_OBS Código da observação (campo 02 do Registro 0460) C 006 - OC OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [D760]
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao
ICMS, constante do Artigo 5º do Convênio SN/70.
Campo 03 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01. Os valores de CFOP informados poderão ser iniciados com 5, 6 ou 7.
Campo 05 (VL_OPR) - Preenchimento: Na combinação de CST_ICMS, CFOP e ALIQ_ICMS, informar o valor total dos
itens relacionados aos serviços próprios, com destaque de ICMS, conforme preenchido na NFCom.
Campo 06 (VL_BC_ICMS) - Preenchimento: informar a base de cálculo do ICMS, referente à combinação dos campos
CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Campo 07 (VL_ICMS) - Preenchimento: informar o valor do ICMS referente à combinação dos campos CST_ICMS, CFOP
e ALIQ_ICMS deste registro.
Campo 08 (VL_RED_BC) - Preenchimento: informar o valor não tributado em função da redução da base de cálculo do
ICMS, referente à combinação dos campos CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Validação:. O campo VL_RED_BC deve ser maior que zero se o 2º e 3º caracteres do CST_ICMS forem iguais a 20.
Campo 09 (COD_OBS) - Preenchimento: este campo só deve ser informado pelos contribuintes localizados em UF que
determine em sua legislação o seu preenchimento.
Validação: o código informado deve constar do registro 0460.
----
REGISTRO D761: INFORMAÇÕES DO FUNDO DE COMBATE À POBREZA – FCP –
(CÓDIGO 62)
Este registro tem por objetivo prestar informações do Fundo de Combate à Pobreza (FCP), constante na NFCom. Os
valores deste registro são meramente informativos e não são contabilizados na apuração dos registros no bloco E.
A obrigatoriedade e forma de apresentação de cada campo deste registro deve ser verificada junto às unidades federativas.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D761" C 004 - O O
02 VL_FCP_OP Valor do Fundo de Combate à Pobreza (FCP) vinculado à N - 02 O O
operação própria, na combinação de CST_ICMS, CFOP e
alíquota do ICMS
Observações:
Nível hierárquico – 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [D761]
----
REGISTRO D990: ENCERRAMENTO DO BLOCO D.
Este registro tem por objetivo identificar o encerramento do bloco D e informar a quantidade de linhas (registros)
existentes no bloco.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo "D990" C 004 - O O
02 QTD_LIN_D Quantidade total de linhas do Bloco D N - - O O
Observações:
Nível hierárquico - 1
Ocorrência – um por arquivo
Campo 01 (REG) - Valor Válido: [D990]
Campo 02 (QTD_LIN_D) - Preenchimento: A quantidade de linhas a ser informada deve considerar também os próprios
registros de abertura e encerramento do bloco.
Validação: O número de linhas (registros) existentes no bloco D é igual ao valor informado no campo QTD_LIN_D.
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
