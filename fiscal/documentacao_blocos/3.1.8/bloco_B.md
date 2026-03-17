# Bloco B - Versão 3.1.8

 
BLOCO B: ESCRITURAÇÃO E APURAÇÃO DO ISS  
 
----
REGISTRO B001: ABERTURA DO BLOCO B  
 
Este registro tem por objetivo identificar a abertura do bloco B, indicando se há informações sobre documentos fiscais.  
Os estabelecimentos NÃO  domiciliados no Distrito Federal deverão informar apenas os registros B001 e B990 (abertura – bloco 
sem dados informados e fechamento).  
 
Nº Campo  Descrição  Tipo Tam Dec  Obrig  
01 REG Texto fixo contendo "B001"  C 004* - O 
02 IND_DAD  Indicador de movimento:  
0 - Bloco com dados informados  
1 - Bloco sem dados informados  C 001* - O 
Observações:  
Nível hierárquico - 1 
Ocorrência - um por arquivo  
 
Campo 01 (REG) - Valor válido : [B001]  
Campo 02 (IND_DAD) - Valores válidos: [0, 1] 
Validação: se o valor for igual a “1” (um), somente podem ser informados os registros de abertura e encerramento do bloco. 
Se o valor for igual a “0” (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento 
do bloco.  
----
REGISTRO B020: NOTA FISCAL (CÓDIGO 01), NOTA FISCAL DE SERVIÇOS (CÓDIGO 03), 
NOTA FISCAL DE SERVIÇOS AVULSA (CÓDIGO 3B), NOTA FISCAL DE PRODUTOR 
(CÓDIGO 04), CONHECIMENTO DE TRANSPORTE RODOVIÁRIO DE CARGAS (CÓDIGO 
08), NF -e (CÓDIGO 55), NFC -e (CÓDIGO 65) e  NF3-e (CÓDIGO 66).  
 
Este registro deve ser gerado para cada documento fiscal código 01, 03, 3B, 04, 08, 55, 65 e 66, conforme item 
4.1.3 da Nota Técnica (Ato COTEPE/ICMS nº 44/2018 e alterações), para os registros das aquisições e prestações de serviços 
sujeitas ao ISS.  
Não deverão ser informados os documentos fiscais eletrônicos denegados ou com numeração inutilizada.  
 
Validação do Registro: Não podem ser informados, em um mesmo arquivo, dois ou mais registros B020 com a 
mesma combinação de valores dos campos formadores da chave do registro.  
 A chave do registro B020 é: IND_OPER, COD_PART, COD_MOD, SER, NUM_DOC e DT_DOC  
 
 
Nº Campo  Descrição  Tipo Tam Dec Entr   Saída  
01 REG Texto fixo contendo "B020"  C 004* - O O 
02 IND_OPER  Indicador do tipo de operação:  
0 - Aquisição;  
1 - Prestação  C 001* - O O 
03 IND_EMIT  
 Indicador do emitente do documento fiscal:  
0 - Emissão própria;  
1 - Terceiros  C 001* - O O 
04 COD_PART  Código do participante (campo 02 do 
Registro 0150):  
- do prestador, no caso de declarante na 
condição de tomador;  
- do tomador, no caso de declarante na 
condição de prestador  C 060 - O OC 
05 COD_MOD  Código do modelo do documento fiscal, 
conforme a Tabela 4.1.3  C 002* - O O 
06 COD_SIT  Código da situação do documento conforme 
tabela 4.1.2  N 002* - O O 
07 SER Série do documento fiscal  C 003 - OC OC 
08 NUM_DOC  Número do documento fiscal  N 009 - O O 
09 CHV_NFE  Chave da Nota Fiscal Eletrônica  N 044* - OC OC 
10 DT_DOC  Data da emissão do documento fiscal  N 008* - - O 
11 COD_MUN_SE
RV Código do município onde o serviço foi 
prestado, conforme a tabela IBGE.  C 007* - O O 
12 VL_CONT  Valor contábil (valor total do documento)  N - 02 O O 
13 VL_MAT_TER
C Valor do material fornecido por terceiros na 
prestação do serviço  N - 02 O O 
14 VL_SUB  Valor da subempreitada  N - 02 O O 
15 VL_ISNT_ISS  Valor das operações isentas ou não -
tributadas pelo ISS  N - 02 O O 
16 VL_DED_BC  Valor da dedução da base de cálculo  N - 02 O O 
17 VL_BC_ISS  Valor da base de cálculo do ISS  N - 02 O O 
18 VL_BC_ISS_RT  Valor da base de cálculo de retenção do ISS  N - 02 O O 
19 VL_ISS_RT  Valor do ISS retido pelo tomador  N - 02 O O 
20 VL_ ISS  Valor do ISS destacado  N - 02 O O 
21 COD_INF_OBS  Código da observação do lançamento   
fiscal (campo 02 do Registro 0460)  C 060 - OC OC 
Observações:  
Nível hierárquico - 2 
Ocorrência – vários (por arquivo)  
 
Campo 01 (REG) - Valor Válido: [B020]  
 
Campo 02 (IND_OPER) - Valores válidos : [0, 1]  
Preenchimento: No caso de aquisição de serviço pelo declarante, informar [0]; no caso de prestação de serviço pelo 
declarante, informar [1].  
 
Campo 03 (IND_EMIT) - Valores válidos : [0, 1]  
Preenchimento : No caso de emissão própria, informar [0]; no caso de emissão de terceiros, informar [1].  
Validação: se este campo tiver valor igual a “1” (um), o campo IND_OPER deve ser igual a “0” (zero).  
 
Campo 04 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150. Quando 
se tratar de NFC -e (modelo 65), o campo não deve ser preenchido. Quando se tratar de NF3 -e (modelo 66), o campo é 
obrigatório nos casos de aquisição de serviços (IND_OPER = “0’) e/ou  se houver retenção de ISS pelo tomador 
(VL_ISS_RT maior que zero), nas demais situações o preenchimento é facultativo.  
 
Campo 05 (COD_MOD) - Valores válidos : [01, 03, 3B, 04, 08, 55, 65, 66]  
Preenchimento : o valor informado deve constar na tabela 4.1.3 da Nota Técnica (Ato COTEPE/ICMS nº 44/2018 e 
alterações). O modelo “65” só pode ser informado no caso de prestação de serviço, ou seja, campo “IND_OPER” preenchido 
com “1”.  
 
Campo 06 (COD_SIT) - Valores válidos : [00, 02, 06, 08]  
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3. No caso da NF3 -e (modelo 66) não 
pode ser informado o COD_SIT = “06”.  
 
 
Campo 07 (SER)  – Validação: campo de preenchimento obrigatório com três posições para NF -e, COD_MOD igual a 
“55”, e para NF3 -e, COD_MOD igual a “66”, de emissão própria ou de terceiros e para NFC -e, COD_MOD igual a “65” 
de emissão própria. Se não existir Série para NF -e, NFC -e ou NF3 -e informar 000.  
 
Campo 08 (NUM_DOC) –Validação: o valor informado deve ser maior que “0” (zero).  
 
Campo 09 (CHV_NFE) - Preenchimento : campo  de preenchimento obrigatório para NF -e, COD_MOD igual a “55”, e 
para NF3 -e, COD_MOD igual a “66”, de emissão própria ou de terceiros e para NFC -e, COD_MOD igual a “65” de emissão 
própria.  
Validação: é conferido o dígito verificador (DV) da chave da NF -e, da NF3 -e e da NFC -e de emissão própria. Este campo 
é de preenchimento obrigatório para COD_MOD igual a “55”, “65” e “66”. Para confirmação inequívoca de que a chave 
da NF - e/NFC -e/NF3 -e corresponde ao s dados informados do documento, é comparado o CNPJ base existente na 
CHV_NFE com o campo CNPJ base do registro 0000, que corresponde ao CNPJ do informante do arquivo, no caso de 
IND_EMIT = 0 (emissão própria). São verificados a consistência da informação dos campos NUM_DOC e SER com o 
número do documento e série contidos na chave da NF -e. É também comparada a UF codificada na chave da NF -e com o 
campo UF informado no registro 0000.  
 
Campo 10 (DT_DOC) - Preenchimento : informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo -
se quaisquer caracteres de separação, tais como: “.”, “/”, “ -”.  
Validação: Para aquisição de serviços (campo “IND_OPER” preenchido com “0”) o valor informado no campo deve ser 
menor ou igual ao valor do campo “DT_FIN” do registro 0000. Para prestação de serviços (campo “IND_OPER” preenchido com “1”) o valor informado no campo deve ser maior ou igual ao valor do campo DT_INI do registro 0000 e 
menor ou igual ao valor do campo “DT_FIN” do registro 0000.  
 
Campo 11 (COD_MUN_SERV) – Validação: o valor informado no campo deve existir na Tabela de Municípios do 
IBGE, possuindo 7 dígitos.  
 
Campo 12 (VL_CONT) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_CONT_P” dos registros B025 filhos.  
 
Campo 15 (VL_ISNT_ISS) – Validação: o valor informado deve ser igual ao somatório dos valores informados no 
campo “VL_ISNT_ISS_P” dos registros B025 filhos.  
 
Campo 17 (VL_BC_ISS) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_BC_ISS_P” dos registros B025 filhos.  
 
Campo 19 (VL_ISS_RT) – Validação: Se COD_MOD for igual a “65”, o valor informado deve ser igual a zero.  
 
Campo 20 (VL_ISS) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_ISS_P” dos registros B025 filhos.  
 
Campo 21 (COD_INF_OBS) - Validação: o código informado deve constar do registro 0460.  
 
----
REGISTRO B025: DETALHAMENTO POR COMBINAÇÃO DE ALÍQUOTA E ITEM DA 
LISTA DE SERVIÇOS DA LC 116/2003)  
 
Este registro deve ser gerado para registrar de forma detalhada, por combinação de alíquota de incidência do ISS e 
Item da Lista de Serviços da Lei Complementar 116/2003, os valores informados no registro B020 “pai” (ou seja, o 
registro B020 que imediatame nte o antecede no arquivo).  
 
Validação do Registro: Não podem ser informados, para um mesmo B020 “pai”, dois ou mais registros B025 com 
a mesma combinação de valores dos campos: ALIQ_ISS e COD_SERV.  
 
Nº Campo  Descrição  Tipo Tam Dec Entr Saídas  
01 REG Texto fixo contendo “B025”  C 004* - O O 
02 VL_CONT_P  Parcela correspondente ao “Valor 
Contábil” referente à combinação 
da alíquota e item da lista  N - 02 O O 
03 VL_BC_ISS_P  Parcela correspondente ao “Valor 
da base de cálculo do ISS” 
referente à combinação da alíquota 
e item da lista  N - 02 O O 
04 ALIQ_ISS  Alíquota do ISS  N - 02 O O 
05 VL_ISS_P  Parcela correspondente ao “Valor 
do ISS” referente à combinação da 
alíquota e item da lista  N - 02 O O 
06 VL_ISNT_ISS_P  Parcela correspondente ao “Valor 
das operações isentas ou não -
tributadas pelo ISS” referente à 
combinação da alíquota e item da 
lista N - 02 O O 
07 COD_SERV  Item da lista de serviços, conforme 
Tabela 4.6.3  C 004* - O O 
Observações:  
Nível hierárquico – 3  
Ocorrência –1:N 
 
Campo 01 (REG) - Valor Válido: [B025]  
 
Campo 02 (VL_CONT_P) - Preenchimento : informar o valor da parcela do valor contábil referente à combinação de alíquota 
e item da lista de serviço do documento fiscal informado no B020 “pai”.  
 
Campo 03 (VL_BC_ISS_P) - Preenchimento : informar o valor da parcela da base de cálculo referente à combinação de alíquota e item da lista de serviço do documento fiscal informado no B020 “pai”.  
Campo 04 (ALIQ_ISS) - Preenchimento : informar o valor da alíquota de incidência do ISS. A alíquota máxima do ISS é 5%.  
Validação: o valor informado deve ser menor ou igual a 5.  
Campo 05 (VL_ISS_P) - Preenchimento : informar o valor da parcela do ISS referente à combinação de alíquota e item da lista de serviço do documento fiscal informado no B020 “pai”. Validação: O valor deve ser igual ao produto da base de cálculo “VL_BC_ISS_P” pela alíquota “ALIQ_ISS”.  
Campo 06 (VL_ISNT_ISS_P) - Preenchimento : informar o valor da parcela isenta ou não tributada referente à combinação 
de alíquota e item da lista de serviço do documento fiscal informado no B020 “pai”.  
 
Campo 07 (COD_SERV) - Preenchimento : informar o item da lista da LC 116/03 correspondente ao serviço prestado.  
Validação: O código informado tem de constar da Tabela 4.6.3.  

----
REGISTRO B030: NOTA FISCAL DE SERVIÇOS SIMPLIFICADA (CÓDIGO 3A)  
 
Este registro deve ser gerado para registrar as informações referentes às prestações de serviços sujeitas ao ISS 
acobertadas por Nota Fiscal de Serviços modelo simplificado (Código 3A), conforme item 4.1.3 da Nota Técnica (Ato 
COTEPE/ICMS nº 44/2018 e alte rações).  
Cada registro B030 pode conter um conjunto de notas fiscais desde que a numeração seja contínua e a série e a data 
de emissão sejam as mesmas.  
 
Validação do Registro: Não podem ser informados, em um mesmo arquivo, dois ou mais registros B030 com a 
mesma combinação de valores dos campos formadores da chave do registro. A chave do registro B030 é: COD_MOD, 
SER, NUM_DOC_INI, NUM_DOC_FIN e DT_DOC.  
 
Nº Campo  Descrição  Tipo Tam Dec Entr Saída  
01 REG Texto fixo contendo “B030”  C 004* - Não 
informar  
 O 
02 COD_MOD  Código do modelo do documento 
fiscal, conforme a Tabela 4.1.3  C 002* - O 
03 SER Série do documento fiscal  C 003 - OC 
04 NUM_DOC_INI  Número do primeiro documento fiscal 
emitido no dia  N 009 - O 
05 NUM_DOC_FIN  Número do último documento fiscal 
emitido no dia  N 009 - O 
06 DT_DOC  Data da emissão dos documentos 
fiscais  N 008* - O 
07 QTD_CANC  Quantidade de documentos 
cancelados  N - - O 
08 VL_CONT  Valor contábil (valor total acumulado 
dos documentos)  N - 02 O 
09 VL_ISNT_ISS  Valor acumulado das operações 
isentas ou não -tributadas pelo ISS  N - 02 O 
10 VL_BC_ISS  Valor acumulado da base de cálculo 
do ISS  N - 02 O 
11 VL_ ISS  Valor acumulado do ISS destacado  N - 02 O 
12 COD_INF_OBS  Código da   observação   do   
lançamento   fiscal (campo 02 do 
Registro 0460)  C 060 - OC 
Observações:  
Nível hierárquico - 2 
Ocorrência – vários (por arquivo)  
 
Campo 01 (REG) - Valor Válido: [B030]  
 
Campo 02 (COD_MOD) - Valor válido : [3A]  
Preenchimento: o valor informado deve constar na tabela 4.1.3 da Nota Técnica (Ato COTEPE/ICMS nº 44/2018 e 
alterações). Só os documentos Código 3A devem ser informados nesse registro.  
 
Campo 03 (SER) - Preenchimento : informar a série dos documentos fiscais.  
 
Campo 04 (NUM_DOC_INI) - Validação: o valor tem de ser maior que zero.  
 
Campo 05 (NUM_DOC_FIN) - Validação: o valor tem de ser maior ou igual ao valor informado no campo 
NUM_DOC_INI.  
 
Campo 06 (DT_DOC) - Preenchimento : informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo -
se quaisquer caracteres de separação, tais como: “.”, “/”, “ -”.  
Validação: O valor informado no campo deve ser maior ou igual ao valor do campo DT_INI do registro 0000 e menor 
ou igual ao valor do campo “DT_FIN” do registro 0000.  
 
Campo 07 (QTD_CANC) - Preenchimento: Informar a quantidade de documentos cancelados dentro da numeração 
compreendida entre o campo NUM_DOC_ INI e  o campo NUM_DOC_FIN.  
 
Campo 08 (VL_CONT) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_CONT_P” dos registros B035 filhos.  
 
Campo 09 (VL_ISNT_ISS) – Validação: o valor informado deve ser igual ao somatório dos valores informados no 
campo “VL_ISNT_ISS_P” dos registros B035 filhos.  
 
Campo 10 (VL_BC_ISS) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_BC_ISS_P” dos registros B035 filhos.  
 
Campo 11 (VL_ISS) –Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_ISS_P” dos registros B035 filhos.  
 
Campo 12 (COD_INF_OBS) - Validação: o código informado deve constar do registro 0460.  

----
REGISTRO B035: DETALHAMENTO POR COMBINAÇÃO DE ALÍQUOTA E ITEM DA 
LISTA DE SERVIÇOS DA LC 116/2003)  
 
Este registro deve ser gerado para registrar de forma detalhada, por combinação de alíquota de incidência do ISS e 
Item da Lista de Serviços da Lei Complementar 116/2003, os valores informados no registro B030 “pai” (ou seja, o registro 
B030 que imediatamente o antecede no arquivo).   
 
Validação do Registro: Não podem ser informados, para um mesmo B030 “pai”, dois ou mais registros B035 com 
a mesma combinação de valores dos campos: ALIQ_ISS e COD_SERV.  
 
Nº Campo  Descrição  Tipo Tam Dec Entr.  Saídas  
01 REG Texto fixo contendo “B035”  C 004* - Não 
informar  O 
02 VL_CONT_P  Parcela correspondente ao “Valor 
Contábil” referente à combinação 
da alíquota e item da lista  N - 02 O 
03 VL_BC_ISS_P  Parcela correspondente ao “Valor 
da base de cálculo do ISS” 
referente à combinação da 
alíquota e item da lista  N - 02 O 
04 ALIQ_ISS  Alíquota do ISS  N - 02 O 
05 VL_ISS_P  Parcela correspondente ao “Valor 
do ISS” referente à combinação 
da alíquota e item da lista  N - 02 O 
06 VL_ISNT_ISS_P  
 Parcela correspondente ao “Valor 
das operações isentas ou não -
tributadas pelo ISS” referente à 
combinação da alíquota e item da 
lista N - 02 O 
07 COD_SERV  Item da lista de serviços, 
conforme Tabela 4.6.3.  C 004* - O 
Observações:  
Nível hierárquico – 3  
Ocorrência – 1:N 
 
Campo 01 (REG) - Valor Válido: [B035]  
 
Campo 02 (VL_CONT_P) - Preenchimento : informar o valor da parcela do valor contábil referente à combinação de alíquota 
e item da lista de serviço dos documentos fiscais informados no B030 “pai”.  
 
Campo 03 (VL_BC_ISS_P) - Preenchimento : informar o valor da parcela da base de cálculo referente à combinação de 
alíquota e item da lista de serviço dos documentos fiscais informados no B030 “pai”.  
 
  Campo 04 (ALIQ_ISS) - Preenchimento : informar o valor da alíquota de incidência do ISS. A alíquota máxima do ISS é 
5%. Validação: o valor informado deve ser menor ou igual a 5.  
 
Campo 05 (VL_ISS_P) - Preenchimento : informar o valor da parcela do ISS referente à combinação de alíquota e item da 
lista de serviço dos documentos fiscais informados no B030 “pai”.  
Validação: O valor do deve ser igual ao produto da base de cálculo “VL_BC_ISS_P” pela alíquota “ALIQ_ISS”.  
 
Campo 06 (VL_ISNT_ISS_P) - Preenchimento : informar o valor da parcela isenta ou não tributada referente à combinação 
de alíquota e item da lista de serviço dos documentos fiscais informados no B030 “pai”.  
Campo 07 (COD_SERV) - Preenchimento : informar o item da lista da LC 116/03 correspondente ao serviço prestado. 
Validação: O código informado tem de constar da Tabela 4.6.3.  
----
REGISTRO B350: SERVIÇOS PRESTADOS POR INSTITUIÇÕES FINANCEIRAS  
 
Este registro deve ser gerado para registrar os valores das receitas auferidas com prestação de serviços por instituições 
financeiras com base no Plano Contábil das Instituições do Sistema Financeiro Nacional – COSIF disponibilizado pelo Banco 
Central do B rasil.  
 
Deverão ser lançadas no registro B350 todas as receitas referentes a serviços (classificação 7.1.7.00.00 -9 do COSIF), 
ainda que não incluídos no anexo da  LC 116/2003. Só deverão ser excluídas destas receitas as prestações acobertadas por Notas 
Fiscais de Serviço.  
 
Para os serviços prestados pelas instituições financeiras sujeitos à retenção do ISS pelo tomador, será necessária a 
emissão da Nota Fiscal de Serviços que será informada no registro B020. Estas prestações não serão informadas no registro 
B350, para que nã o sejam consideradas em duplicidade para os cálculos do ISS devido e do faturamento.  
 
Validação do Registro: Não podem ser informados, em um mesmo arquivo, dois ou mais registros B350 com a 
mesma combinação de valores dos campos formadores da chave do registro. A chave do registro B350 é: COD_CTD, 
CTA_COSIF, COD_SERV e ALIQ_ISS.  
 
Nº Campo  Descrição  Tipo Ta
m Dec Entr  Saída  
01 REG Texto fixo contendo “B350”  C 004
* - Não 
informar  
 O 
02 COD_CTD  Código da conta do plano de contas  C - - O 
03 CTA_ISS  Descrição da conta no plano de contas  C - - O 
04 CTA_COSIF  Código COSIF a que está subordinada a 
conta do ISS das instituições financeiras  N 008
* - O 
05 QTD_OCOR  Quantidade de ocorrências na conta  N - - O 
06 COD_SERV  Item da lista de serviços, conforme 
Tabela 4.6.3.  N 004
* - O 
07 VL_CONT  Valor contábil  N - 02 O 
08 VL_BC_ISS  Valor da base de cálculo do ISS  N - 02 O 
09 ALIQ_ISS  Alíquota do ISS  N - 02 O 
10 VL_ISS  Valor do ISS  N - 02 O 
11 COD_INF_OBS  Código da observação do lançamento 
fiscal (campo 02 do Registro 0460)  C 060 - OC 
Observações:  
Nível hierárquico - 2 
Ocorrência – vários (por arquivo)  
 
Campo 01 (REG) - Valor Válido: [B350]  
 
Campo 02 (COD_CTD) - Preenchimento : informar o código da conta de receita referente ao serviço prestado no Plano 
de Contas do declarante.  
 
Campo 03 (CTA_ISS) – Preenchimento: Descrição da conta de receita no plano de contas do declarante.  
 
Campo 04 (CTA_COSIF) – Preenchimento: Informar o código COSIF referente à receita com prestação de serviço.  
Validação: O código informado tem de constar da Tabela 4.6.2.  
  
Campo 05 (QTD_OCOR) –Preenchimento: Informar a quantidade, no período, de Registros B350 que referenciaram o 
mesmo código de conta (COD_CTD).  
Validação: o valor tem de ser maior ou igual a 1.  
 
Campo 06 (COD_SERV)  - Preenchimento: informar o item da lista da LC 116/03 correspondente ao serviço prestado. 
Validação: O código informado tem de constar da Tabela 4.6.3.  
 
Campo 07 (VL_CONT) - Preenchimento: Informar o valor das prestações referentes à conta de receita.  
 
Campo 08 (VL_BC_ISS) - Preenchimento: Informar o valor da base de cálculo do ISS correspondente às prestações 
referentes à conta de receita.  
 
Campo 09 (ALIQ_ISS) - Preenchimento : informar o valor da alíquota de incidência do ISS. A alíquota máxima do ISS é 
5%. Validação: o valor informado deve ser menor ou igual a 5.  
 
Campo 10 (VL_ISS) - Validação: O valor deve ser igual ao produto da base de cálculo “VL_BC_ISS” pela alíquota 
“ALIQ_ISS”  
 
Campo 11 (COD_INF_OBS) - Validação: o código informado deve constar do registro 0460.  
 
----
REGISTRO B420: TOTALIZAÇÃO DOS VALORES DE SERVIÇOS PRESTADOS POR 
COMBINAÇÃO DE ALÍQUOTA E ITEM DA LISTA DE SERVIÇOS DA LC 116/2003  
 
 Este registro deve ser gerado para registrar de forma detalhada, por combinação de alíquota de incidência do ISS e 
Item da Lista de Serviços da Lei Complementar 116/2003, os valores totais das prestações de serviços realizadas no 
período.  
Validação do Registro: Não podem ser informados, em um mesmo arquivo, dois ou mais registros B420 com a 
mesma combinação de valores dos campos: ALIQ_ISS e COD_SERV.  
 
Nº Campo  Descrição  Tipo Tam Dec Entr Saídas  
01 REG Texto fixo contendo “B420”  C 004* - Não 
Informar  O 
02 VL_CONT  Totalização do Valor Contábil das 
prestações do declarante referente à 
combinação da alíquota e item da 
lista N - 02 O 
03 VL_BC_ISS  Totalização do Valor da base de 
cálculo do ISS das prestações do 
declarante referente à combinação 
da alíquota e item da lista  N - 02 O 
04 ALIQ_ISS  Alíquota do ISS  N - 02 O 
05 VL_ISNT_ISS  Totalização do valor das operações 
isentas ou não -tributadas pelo ISS 
referente à combinação da alíquota 
e item da lista  
 N - 02 O 
06 VL_ISS  Totalização, por combinação da 
alíquota e item da lista, do Valor do 
ISS N - 02 O 
07 COD_SERV  Item da lista de serviços, conforme 
Tabela 4.6.3.  C - - O 
Observações:  
Nível hierárquico - 2 
Ocorrência – vários (por arquivo)  
Campo 01 (REG) - Valor Válido: [B420]  
 
Campo 02 (VL_CONT) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_CONT_P” dos registros B025 (referentes às prestações do declarante, ou seja, com o campo IND_OPER do registro 
B020 “pai” preenchido com “1”), “VL_CONT_P” dos registros B035 e “VL_CONT” dos registros B350, para a combinação 
de alíquota e item da lista.  
 
Campo 03 (VL_BC_ISS) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_BC_ISS_P” dos registros B025 (referentes às prestações do declarante, ou seja, com o campo IND_OPER do registro 
B020 “pai” preenchido com “1”), no campo “VL_BC_ISS_P” dos reg istros B035 e no campo “VL_BC_ISS” dos registros 
B350 para a combinação de alíquota e item da lista.  
 
 Campo 04 (ALIQ_ISS) - Preenchimento : informar o valor da alíquota de incidência do ISS. A alíquota máxima do ISS no 
DF é 5%. Validação: o valor informado deve ser menor ou igual a 5.  
 
Campo 05 (VL_ISNT_ISS) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_ISNT_ISS_P” dos registros B025 (referentes às prestações do declarante, ou seja, com o campo IND_OPER do registro 
B020 “pai” preenchido com “1”), no campo “VL_ISNT_ISS_P” dos  registros B035 e da diferença entre os valores dos 
campos “VL_CONT” e “VL_BC_ISS” dos registros B350, para a combinação de alíquota e item da lista.  
 
Campo 06 (VL_ISS) - Validação: o valor informado deve ser igual ao somatório dos valores informados no campo “VL_ 
ISS_P” dos registros B025 (referentes às prestações do declarante, ou seja, com o campo IND_OPER do registro B020 “pai” 
preenchido com “1”), no campo “VL_ISS_P” dos registro s B035 e no campo “VL_ISS” dos registros B350, para a 
combinação de alíquota e item da lista.  
 
Campo 07 (COD_SERV) - Preenchimento : informar o item da lista da LC 116/03 correspondente ao serviço prestado. 
Validação: O código informado tem de constar da Tabela 4.6.3.  
 
----
REGISTRO B440: TOTALIZAÇÃO DOS VALORES RETIDOS  
 
 Este registro deve ser gerado para registrar os valores retidos tanto referentes às prestações (declarante na condição de 
prestador) quanto às aquisições (declarante na condição de tomador). Os valores são informados por tomador e/ou prestador 
conforme o t ipo de operação.  
  
 O registro deve ser informado ainda que não tenha havido retenção de ISS nas aquisições e prestações do declarante, 
neste caso, informar a base de cálculo de retenção e ISS retido zerados.  
 
Exceção 1:  Os valores referentes às prestações acobertadas por documento fiscal com COD_MOD "65" ou "3A" não devem 
ser considerados nas informações deste Registro.  
 
Validação do Registro: Não podem ser informados, em um mesmo arquivo, dois ou mais registros B440 com a 
mesma combinação de valores dos campos: IND_OPER e COD_PART.  
 
Nº Campo  Descrição  Tipo Tam Dec Entr Saídas  
01 REG Texto fixo contendo “B440”  C 004
* - O O 
02 IND_OPER  Indicador do tipo de operação:  
0 - Aquisição;  
1 - Prestação  N - 02 O O 
03 COD_PART  Código do participante (campo 02 
do Registro 0150):  C - - O O 
- do prestador, no caso de aquisição 
de serviço pelo declarante;  
- do tomador, no caso de prestação 
de serviço pelo declarante  
04 VL_CONT_RT  Totalização do Valor Contábil das 
prestações e/ou aquisições do 
declarante pela combinação de tipo 
de operação e participante.  N - 02 O O 
05 VL_BC_ISS_R
T Totalização do Valor da base de 
cálculo de retenção do ISS das 
prestações e/ou aquisições do 
declarante pela combinação de tipo 
de operação e participante.  N - 02 O O 
06 VL_ISS_RT  Totalização do Valor do ISS retido 
pelo tomador das prestações e/ou 
aquisições do declarante pela 
combinação de tipo de operação e 
participante.  N - 02 O O 
Observações:  
Nível hierárquico – 2 
Ocorrência – vários (por arquivo)  
Campo 01 (REG) - Valor Válido: [B440]  
 
Campo 02 (IND_OPER) - Valores válidos : [0, 1]  
Preenchimento: No caso de aquisição de serviço pelo declarante, informar [0]; no caso de prestação de serviço pelo 
declarante, informar [1].  
 
Campo 03 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.  
 
Campo 04 (VL_CONT_RT) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_CONT” dos registros B020 para a combinação de tipo da operação e participante.  
 
Campo 05 (VL_BC_ISS_RT) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_BC_ISS_RT” dos registros B020 para a combinação de tipo da operação e participante.  
 
Campo 06 (VL_ISS_RT) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_ISS_RT” dos registros B020 para a combinação de tipo da operação e participante.  
 
----
REGISTRO B460: DEDUÇÕES DO ISS  
 Este registro deve ser gerado para registrar as deduções do ISS que influenciarão na apuração dos valores a recolher 
do ISS Próprio, ISS substituto (devido pelas retenções referentes às aquisições do declarante) e ISS Uniprofissional, conform e 
o caso.  
Nº Campo  Descrição  Tipo Tam Dec Entr.  Saídas  
01 REG Texto fixo contendo "B460"  C 004* - O O 
02 IND_DED  Indicador do tipo de dedução:  
0 - Compensação do ISS 
calculado a maior;  
1 - Benefício fiscal por incentivo 
à cultura;  C 001* - O O 
2 - Decisão administrativa ou 
judicial;  
9 - Outros  
03 VL_DED  Valor da dedução  N - 02 O O 
04 NUM_PROC  Número do processo ao qual o 
ajuste está vinculado, se houver  C - - OC OC 
05 IND_PROC  Indicador da origem do 
processo:  
0 - Sefin;  
1 - Justiça Federal;  
2 - Justiça Estadual;  
9 - Outros  C 001* - OC OC 
06 PROC  Descrição do processo que 
embasou o lançamento  C - - OC OC 
07 COD_INF_OBS  Código da   observação   do  
lançamento   fiscal  
(campo 02 do Registro 0460)  C 060 - O O 
08 IND_OBR  Indicador da obrigação onde 
será aplicada a dedução:  
0 - ISS Próprio;  
 - ISS Substituto (devido pelas 
aquisições de serviços do 
declarante).  
 - ISS Uniprofissionais.  
 C 001* - O O 
Observações:  
Nível hierárquico – 2 
Ocorrência – vários (por arquivo)  
Campo 01 (REG) - Valor Válido: [B460]  
 
Campo 02 (IND_DED) - Valores válidos : [0, 1, 2, 9]  
Preenchimento: indicar o motivo da dedução.  
 
Campo 03 (VL_DED) - Preenchimento: informar o valor da dedução.  
 
Campos 04 a 06 - Preenchimento: indicar os dados do processo (se existir) vinculado à dedução.  
 
Campo 07 (COD_INF_OBS) - Validação: o código informado deve constar do registro 0460.  
 
Campo 08 (IND_OBR) – Preenchimento: indicar a qual obrigação se refere a dedução.  
Valores válidos : [0, 1, 2]  
 
----
REGISTRO B470: APURAÇÃO DO ISS  
 Este registro deve ser gerado para registrar os totais referentes às prestações de serviço do declarante e para apurar os 
valores a recolher do ISS próprio, do ISS retido pelo declarante na condição de tomador e do ISS Uniprofissional.  
Nº Campo  Descrição  Tipo Tam Dec Obrig  
01 REG Texto fixo contendo “B470”  C 004* - O 
02 VL_CONT  A - Valor total referente às prestações de 
serviço do período  N - 02 O 
03 VL_MAT_TERC  B - Valor total do material fornecido por 
terceiros na prestação do serviço  N - 02 O 
04 VL_MAT_PROP  C - Valor do material próprio utilizado na 
prestação do serviço  N - 02 O 
05 VL_SUB  D - Valor total das subempreitadas  N - 02 O 
06 VL_ISNT  E - Valor total das operações isentas ou 
não-tributadas pelo ISS  N - 02 O 
07 VL_DED_BC  F - Valor total das deduções da base de 
cálculo (B + C + D + E)  N - 02 O 
08 VL_BC_ISS  G - Valor total da base de cálculo do ISS  N - 02 O 
09 VL_BC_ISS_RT  H - Valor total da base de cálculo de 
retenção do ISS referente às prestações do 
declarante.  N - 02 O 
10 VL_ ISS  I - Valor total do ISS destacado  N - 02 O 
11 VL_ISS_RT  J - Valor total do ISS retido pelo tomador 
nas prestações do declarante  N - 02 O 
12 VL_DED  K - Valor total das deduções do ISS 
próprio  N - 02 O 
13 VL_ ISS_REC  L - Valor total apurado do ISS próprio a 
recolher (I - J - K) N - 02 O 
14 VL_ ISS_ST  M - Valor total do ISS substituto a 
recolher pelas aquisições do declarante 
(tomador)  N - 02 O 
15 VL_ISS_REC_UNI  N - Valor do ISS próprio a recolher pela 
Sociedade Uniprofissional  N - 02 O 
Observações:  
Nível hierárquico – 2 
Ocorrência – um (por arquivo)  
 
Campo 01 (REG) - Valor Válido: [B470]  
 
Campo 02 (VL_CONT) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_CONT” dos registros B420.  
 
Campo 06 (VL_ISNT) –Validação: o valor informado deve ser igual ao somatório dos valores informados  no campo 
“VL_ISNT_ISS” dos registros B420.  
 
Campo 07 (VL_DED_BC ) –Validação: o valor informado deve ser igual ao somatório dos valores dos campos 
VL_MAT_TERC, VL_MAT_PROP, VL_SUB e VL_ISNT.  
 
Campo 08 (VL_BC_ISS) –Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_BC_ISS” dos registros B420.  
 
Campo 09 (VL_BC_ISS_RT) –Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_BC_ISS_RT” dos registros B440 (referentes às prestações do declarante, ou seja, com o campo IND_OPER = “1”).  
 
Campo 10 (VL_ ISS ) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo “VL_ 
ISS” dos registros B420.  
 
Campo 11 (VL_ ISS_RT ) –Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_ISS_RT” dos registros B440 (referentes às prestações do declarante, ou seja, com o campo IND_OPER = “1”).  
 
Campo 12 (VL_DED ) – Validação: o valor informado deve ser igual ao somatório dos valores informados no campo 
“VL_DED” dos registros B460 referentes ao ISS Próprio (ou seja, com o campo IND_OBR= “0”).  
 
Campo 13 (VL_ ISS_REC ) –Validação: o valor informado deve coincidir com valor informado no campo VL_ ISS 
deduzidos os valores informados nos campos VL_ISS_RT e VL_DED , se o resultado for maior ou igual a zero. Se o resultado 
for negativo, informar zero.  
 
Campo 14 (VL_ ISS_ST ) – Validação: o valor informado deve coincidir com a diferença entre o somatório dos valores 
informados no campo “VL_ISS_RT” dos registros B440 (referentes às aquisições de serviço do declarante, ou seja, com o 
campo IND_OPER = “0”) e o somatório dos valores informados nos campos “VL_DED” dos registros B460 referentes ao 
ISS ST (ou seja, com o Campo IND_OBR= “1”), se o resultado for maior ou igual a zero. Se o resultado for negativo, 
informar zero.  
 
Campo 15 (VL_ ISS_REC_UNI) – Validação: o valor informado deve coincidir com a diferença entre o valor informado 
no campo “VL_OR” do registro B500 e o somatório dos valores informados nos campos “VL_DED” dos registros B460 
referentes ao ISS Uniprofisionais (ou seja, com o Campo IND_OBR= “2”), se o resultado for maior ou igual a zero. Se o 
resultado for negativo, informar zero.  
 
----
REGISTRO B500: APURAÇÃO DO ISS SOCIEDADE UNIPROFISSIONAL  
 
 Este registro deve ser gerado para registrar o valor das receitas, a quantidade de profissionais habilitados e o valor do 
ISS a recolher das Sociedades Uniprofissionais.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig  
01 REG Texto fixo contendo “B500”  C 004* - O 
02 VL_REC  Valor mensal das receitas auferidas pela sociedade 
uniprofissional  N - 02 O 
03 QTD_PROF  Quantidade de profissionais habilitados  N - - O 
04 VL_OR  Valor do ISS devido  N - 02 O 
Observações:  
Nível hierárquico – 2 
Ocorrência – um (por arquivo)  
 
Campo 01 (REG) - Valor Válido: [B500]  
 
Campo 02 (VL_REC) –Preenchimento : informar o total das receitas da sociedade uniprofissional.  
 
Campo 03 (QTD_PROF) –Validação:  o valor informado deve coincidir com a quantidade de profissionais habilitados 
registros B510 informados com o Campo 02 (IND_PROF) preenchido com “0”.  
 
Campo 04 (VL_OR ) –Validação: o valor informado deve ser igual ao produto do valor do Campo QTD_PROF com o valor 
mensal devido por profissional habilitado para o exercício (Tabela 4.6.1).  
 
----
REGISTRO B510: UNIPROFISSIONAL - EMPREGADOS E SÓCIOS  
  
 Este registro deve ser gerado para registrar as informações de cada um dos profissionais (sócios, empregados 
habilitados e empregados não habilitados) da sociedade uniprofissional.  

Validação do Registro:  
 
a) Não podem ser informados, em um mesmo arquivo, dois ou mais registros B510 com o mesmo valor do campo 
CPF.  
b) O número de sócios tem de ser maior ou igual a um (ou seja, se existir no arquivo registros B510, pelo menos 
um deles tem de ter o campo “IND_SOC” com valor “0”).  
c) O número de profissionais não habilitados não pode ser maior que o dobro do número de sócios (ou seja, a 
quantidade de registros B510 com o campo “IND_PROF” preenchido com “1” tem de ser menor ou igual ao 
dobro da quantidade de registros B510 com o campo “ IND_SOC” preenchido  com “0”).  
 
Nº Campo  Descrição  Tipo Tam Dec  Obrig  
01 REG Texto fixo contendo “B510”  C 004* - O 
02 IND_PROF  Indicador de habilitação:  
0- Profissional habilitado  
1- Profissional não habilitado  C 001* - O 
03 IND_ESC  Indicador de escolaridade:  
0- Nível superior  
1- Nível médio  C 001* - O 
04 IND_SOC  Indicador de participação societária:  
0 - Sócio  
1 - Não sócio  C 001* - O 
05 CPF Número de inscrição do profissional no CPF.  N 011* - O 
06 NOME  Nome do profissional  C 100 - O 
Observações:  
Nível hierárquico – 3 
Ocorrência – vários (por arquivo)  
Campo 01 (REG) - Valor Válido: [B510]  
 
Campo 02 (IND_PROF) - Valores válidos : [0, 1]  
Preenchimento: indicar se o profissional é ou não habilitado.  
 
Campo 03 (IND_ESC) - Valores válidos : [0, 1]  
Preenchimento: indicar o nível de escolaridade do profissional.  
 
Campo 04 (IND_SOC) - Valores válidos : [0, 1]  
Preenchimento: indicar se o profissional é ou não sócio da declarante.  
Validação:  O profissional sócio necessariamente tem de ser habilitado (campo IND_PROF preenchido com “0”)  
 
Campo 05 (CPF) - Preenchimento: informar o número de inscrição do profissional no cadastro do CPF.  
Validação: será conferido o dígito verificador (DV) do CPF informado.  
 
Campo 06 (NOME) - Preenchimento: informar o nome do profissional.  
 
----
REGISTRO B990: ENCERRAMENTO DO BLOCO B  
 
Este registro destina -se a identificar o encerramento do bloco B e informar a quantidade de linhas (registros) 
existentes no bloco.  
 
Nº Campo  Descrição  Tipo Tam Dec Entr Saída  Obrig  
01 REG Texto fixo contendo "B990"  C 004* - O O O 
02  QTD_LIN_B  Quantidade total de linhas 
do Bloco B  N - - O O O 
Observações:  
Nível hierárquico - 1 
Ocorrência – um por arquivo  
