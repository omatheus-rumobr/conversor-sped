# Bloco G - Versão 3.1.8

BLOCO G – CONTROLE DO CRÉDITO DE ICMS DO ATIVO PERMANENTE CIAP
Bloco de registros dos dados relativos ao CIAP – Controle de Crédito do Ativo Permanente cujo objetivo é demonstrar
o cálculo da parcela do crédito de ICMS apropriada no mês, decorrente da entrada de mercadorias destinadas ao ativo
imobilizado, conforme previsto no art. 20, § 5º, da Lei Complementar nº 87, de 13 de setembro de 1996.
REGISTRO G001: ABERTURA DO BLOCO G
Este registro deve ser gerado para abertura do bloco G, indicando se há registros de informações no bloco.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "G001" C 004* - O
Indicador de movimento:
0- Bloco com dados informados;
02 IND_MOV 1- Bloco sem dados informados C 001* - O
Observações:
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Campo 01 (REG) - Valor Válido: [G001]
Campo 02 (IND_MOV) - Valores Válidos: [0, 1]
Validação: se preenchido com ”1” (um), devem ser informados os registros G001 e G990 (encerramento do bloco),
significando que não há escrituração do documento CIAP e, portanto, não há crédito a apropriar. Se preenchido com ”0” (zero),
então deverão ser informados, pelo menos, um registro G110 e respectivos registros filhos.
----
REGISTRO G110: ICMS – ATIVO PERMANENTE – CIAP
Este registro tem o objetivo de prestar informações sobre o CIAP:
a) saldo de ICMS do CIAP, composto pelo valor do ICMS de bens ou componentes (somente componentes cujo crédito
de ICMS já foi apropriado) que entraram anteriormente ao período de apuração. (campo 4);
b) o somatório das parcelas de ICMS passíveis de apropriação de cada bem ou componente, inclusive aqueles que
foram escriturados no CIAP em período anterior (campo 5);
c) o valor do índice de participação do somatório do valor das saídas tributadas e saídas para exportação no valor total
das saídas (campo 8) - (o valor é sempre igual ou menor que 1 (um);
d) o valor de ICMS a ser apropriado como crédito. Esse valor (campo 9) será apropriado diretamente no Registro de
Apuração do ICMS, como ajuste de apuração, salvo se a legislação obrigar à emissão de documento fiscal;
e) o valor de outras parcelas de ICMS a ser apropriado. Esse valor (campo 10) será apropriado diretamente no Registro
de Apuração do ICMS, como ajuste de apuração, salvo se a legislação obrigar à emissão de documento fiscal.
Não podem ser informados dois ou mais registros com a mesma combinação de conteúdo nos campos DT_INI e
DT_FIN e esta combinação deve ser igual à informada em um registro E100.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "G110" C 004* - O
02 DT_INI Data inicial a que a apuração se refere N 008* - O
03 DT_FIN Data final a que a apuração se refere N 008* - O
04 SALDO_IN_ICMS Saldo inicial de ICMS do CIAP, composto por ICMS de N - 02 O
bens que entraram anteriormente ao período de apuração
(somatório dos campos 05 a 08 dos registros G125)
05 SOM_PARC Somatório das parcelas de ICMS passível de apropriação de N - 02 O
cada bem (campo 10 do G125)
06 VL_TRIB_EXP Valor do somatório das saídas tributadas e saídas para N - 02 O
exportação
07 VL_TOTAL Valor total de saídas N - 02 O
08 IND_PER_SAI Índice de participação do valor do somatório das saídas N - 08 O
tributadas e saídas para exportação no valor total de saídas
(Campo 06 dividido pelo campo 07)
09 ICMS_APROP Valor de ICMS a ser apropriado na apuração do ICMS, N - 02 O
correspondente à multiplicação do campo 05 pelo campo 08.
10 SOM_ICMS_OC Valor de outros créditos a ser apropriado na Apuração do N - 02 O
ICMS, correspondente ao somatório do campo 09 do
registro G126.
Observações:
Nível hierárquico - 2
Ocorrência – um (por período de apuração)
Campo 01 (REG) - Valor Válido: [G110];
Campos 02 (DT_INI) - Preenchimento: informar a data no formato “ddmmaaaa” sem separadores de formatação e
compreendida no período informado no registro 0000;
Campos 03 (DT_FIN) - Preenchimento: informar a data no formato “ddmmaaaa” sem separadores de formatação e
compreendida no período informado no registro 0000;
Campo 04 (SALDO_IN_ICMS) – Preenchimento: O saldo inicial do período de apuração é composto pelo somatório de
créditos de ICMS de Ativo Imobilizado (campos VL_IMOB_ICMS_OP + VL_IMOB_ICMS_ST + VL_IMOB_ICMS_FRT +
VL_IMOB_ICMS_DIF do registro G125) de bens ou componentes que foram escriturados no CIAP em períodos anteriores ao
indicado nos campos 02 e 03, que já tiveram parcela do crédito apropriado. Estes bens ou componentes devem ser informados
com o tipo de movimentação “SI- Saldo Inicial de Bens Imobilizados” no registro G125, sendo que a data de movimentação a
ser informada neste registro deverá ser a data inicial do período de apuração.
Obs.: Não compõe o saldo inicial o valor dos créditos de ICMS escriturados em período anterior com tipo de
movimentação “IA – Imobilização em andamento”, cujos créditos somente serão apropriados a partir da conclusão do bem
principal.
Campo 05 (SOM_PARC) - Preenchimento: informar o somatório das parcelas de ICMS passível de apropriação (totalização
dos valores contidos no campo 10 do registro G125)
Validação: O valor preenchido corresponde ao somatório de todos os valores informados no campo 10 (VL_PARC_PASS)
dos registros G125.
Campo 06 (VL_TRIB_EXP) - Preenchimento: informar o somatório do valor das operações e/ou prestações tributadas pelo
ICMS e do valor das operações e/ou prestações relativas ao ICMS destinadas ao exterior, observada a legislação da unidade
federada.
Validação: o valor informado deve ser menor ou igual ao valor informado no campo VL_TOTAL deste registro.
Campo 07 (VL_TOTAL) - Preenchimento: Informar o valor total das operações e/ou prestações relativas ao ICMS realizadas
no período de apuração, observada a legislação da unidade federada.
Campo 08 (IND_PER_SAI) - Validação: informar o valor do índice de participação do valor das saídas tributadas/exportação
no valor total das saídas, correspondente ao resultado da divisão do campo VL_TRIB_EXP pelo campo VL_TOTAL.
Campo 09 (ICMS_APROP) - Preenchimento: informar o valor de ICMS a ser apropriado como crédito no período. Esse valor
será apropriado diretamente no Registro de Apuração do ICMS, como ajuste de apuração, salvo se a legislação obrigar à emissão
de documento fiscal.
Validação: o valor corresponde à multiplicação do valor constante no campo 05 (SOM_PARC) pelo índice calculado no campo
08 (IND_PER_SAI)
Campo 10 (SOM_ICMS_OC) - Preenchimento: informar o somatório de valores de outros créditos de ICMS de Ativo
Imobilizado apropriados no período e discriminados no registro G126. Esse somatório será apropriado diretamente no Registro
de Apuração do ICMS, como ajuste de apuração, salvo se a legislação obrigar à emissão de documento fiscal.
Validação: o valor preenchido corresponde ao somatório de todos os valores informados no campo 09 (VL_PARC_APROP)
dos registros G126.
----
REGISTRO G125: MOVIMENTAÇÃO DE BEM OU COMPONENTE DO ATIVO
IMOBILIZADO
Este registro tem o objetivo de informar as movimentações de bens ou componentes no CIAP e a apropriação de
parcelas de créditos de ICMS do Ativo Imobilizado.
Inclui-se no conceito de movimentação:
a) entrada de bem ou componente no CIAP;
b) saída de bem ou componente do CIAP;
c) baixa de bem ou componente do CIAP;
d) entrada no CIAP pela conclusão de bem que estava sendo construído pelo contribuinte (exceto quando o bem ou
componente gerar créditos a partir do momento de sua entrada).
Validação do Registro: Não podem ser informados dois ou mais registros com a mesma combinação de conteúdo nos
campos COD_IND_BEM e TIPO_MOV.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "G125" C 004* - O
02 COD_IND_BEM Código individualizado do bem ou componente adotado no C 060 - O
controle patrimonial do estabelecimento informante
03 DT_MOV Data da movimentação ou do saldo inicial N 008* - O
04 TIPO_MOV Tipo de movimentação do bem ou componente: C 002* - O
SI = Saldo inicial de bens imobilizados;
IM = Imobilização de bem individual;
IA = Imobilização em Andamento - Componente;
CI = Conclusão de Imobilização em Andamento – Bem
Resultante;
MC = Imobilização oriunda do Ativo Circulante;
BA = Baixa do bem - Fim do período de apropriação;
AT = Alienação ou Transferência;
PE = Perecimento, Extravio ou Deterioração;
OT = Outras Saídas do Imobilizado
05 VL_IMOB_ICMS_ Valor do ICMS da Operação Própria na entrada do bem ou N - 02 OC
OP componente
06 VL_IMOB_ICMS_ Valor do ICMS da Oper. por Sub. Tributária na entrada do N - 02 OC
ST bem ou componente
07 VL_IMOB_ICMS_ Valor do ICMS sobre Frete do Conhecimento de N - 02 OC
FRT Transporte na entrada do bem ou componente
08 VL_IMOB_ICMS_ Valor do ICMS - Diferencial de Alíquota, conforme Doc. N - 02 OC
DIF de Arrecadação, na entrada do bem ou componente
09 NUM_PARC Número da parcela do ICMS N 003 - OC
10 VL_PARC_PASS Valor da parcela de ICMS passível de apropriação (antes N - 02 OC
da aplicação da participação percentual do valor das saídas
tributadas/exportação sobre as saídas totais)
Observações: Os preenchimentos dos campos 09 e 10 indicarão sempre a escrituração e aproveitamento do crédito de ICMS
no período.
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [G125];
Campo 02 (COD_IND_BEM) - Validação: o código informado neste campo deve constar de um registro 0300;
Campo 03 (DT_MOV) - Preenchimento: informar a data no formato “ddmmaaaa”.
Validações:
a) quando o valor no campo TIPO_MOV for igual a “SI”, a data deve ser igual à data inicial constante do campo DT_INI do
registro G110;
b) quando o valor no campo TIPO_MOV for igual a “IA”, “IM”, “CI”, “MC”, “BA”, “AT”, “PE” ou “OT”, a data deve ser
igual ou menor à data final constante do campo DT_FIN do registro G110;
Campo 04 (TIPO_MOV) - Valores Válidos: [SI, IM, IA, CI, MC, BA, AT, PE, OT];
Preenchimento:
1) regras comuns a bem e a componente cujo crédito seja apropriado a partir do período que ocorrer a sua entrada ou
consumo no estabelecimento:
1.1) o bem ou componente que ainda possui parcela a ser apropriada e que foi escriturado em período anterior ao
período de apuração deve ser informado com o tipo de movimentação “SI”. A data de movimentação deve ser igual à
data inicial do período da apuração;
1.2) o bem que entrar no estabelecimento no período de apuração deve ser informado com o tipo de movimentação
“IM”;
1.3) o componente será informado com tipo de movimentação “IA” no mês da aquisição, devendo ser informados os
campos NUM_PARC e VL_PARC_PASS. Nos períodos seguintes deve ser informado com o tipo de movimentação
“SI” e a apropriação das parcelas deverá ser controlada pelo código individual desse componente até a sua respectiva
baixa. Quando da conclusão da construção do bem, não deverá ser apresentado o registro com tipo de movimentação
igual a “CI”;
1.4) a entrada de bem ou componente no CIAP oriunda de estoque do Ativo Circulante deverá ser informada com o
tipo de movimentação “MC”;
1.5) a baixa de bem ou componente pelo fim de apropriação de crédito deverá ocorrer no período de apropriação da
última parcela e, neste caso, deverão ser apresentados dois registros: um registro com tipo de movimentação “SI”, com
os campos NUM_PARC e VL_PARC_PASS preenchidos, representando a apropriação da última parcela, e o segundo
registro com o tipo de movimentação “BA”, representando a saída do CIAP. Esse 2º registro não poderá ter os campos:
VL_IMOB_ICMS_OP, VL_IMOB_ICMS_ST, VL_IMOB_ICMS_FRT, VL_IMOB_ICMS_DIF, NUM_PARC e
VL_PARC_PASS preenchidos;
1.6) a saída de um bem ou componente deve ser informada no período de ocorrência do fato. Deverão ser apresentados
02 registros: um registro com tipo de movimentação “SI” e um segundo registro com tipo de movimentação igual a
“AT”, “PE” ou “OT”, conforme o caso, representando a saída do CIAP. Nesse 2º registro os campos
VL_IMOB_ICMS_OP, VL_IMOB_ICMS_ST, VL_IMOB_ICMS_FRT, VL_IMOB_ICMS_DIF, NUM_PARC e
VL_PARC_PASS não podem ser informados.
Os campos NUM_PARC e VL_PARC_PASS do 1º registro com tipo de movimentação SI podem ser preenchidos,
representando a apropriação da parcela, desde que a legislação da unidade federada interprete pela possibilidade de
apropriação da parcela referente ao período de apuração em que ocorreu o fato (inciso V do § 5º do art. 20 da LC
87/96),
1.7) quando o tipo de movimentação for igual a “SI”, “IM”, “IA” ou “MC”, devem ser informados os campos
NUM_PARC e VL_PARC_PASS.
2) regras específicas para contribuinte localizado em UF que considere que o componente não atende as condições
para se ter direito ao crédito de ICMS, mas sim o bem móvel resultante que está sendo construído no estabelecimento
do contribuinte:
2.1) a entrada ou consumo de componente de um bem que está sendo construído no estabelecimento do contribuinte
deverá ser informado com o tipo de movimentação “IA”, no período de ocorrência do fato. Os campos NUM_PARC
e VL_PARC_PASS não podem ser informados;
2.2) a escrituração no CIAP do bem que foi construído no estabelecimento do contribuinte será informada com tipo
de movimentação igual a “CI” no período da sua conclusão.
2.3) no período de apuração em que se iniciar a obrigação de escrituração fiscal digital do CIAP ou quando isso ocorrer
de forma espontânea, os componentes que entraram ou foram consumidos antes desse período e cuja construção do
bem vinculado ainda não tenha sido concluída ou cujo bem vinculado ainda tenha parcela a ser apropriada devem ser
informados com o tipo de movimentação “IA”. Nos períodos de apuração posteriores, essa informação não deve mais
ser prestada.
2.4) a saída de um componente, cuja entrada ocorreu em mês anterior ao período da escrituração, deve ser informada
no período de ocorrência do fato, com a apresentação de 02 registros:
d) um registro com tipo de movimentação “SI”, representando a existência de componente que entrou em
período anterior, com os campos (VL_IMOB_ICMS_OP, VL_IMOB_ICMS_ST, VL_IMOB_ICMS_FRT,
VL_IMOB_ICMS_DIF) devidamente preenchidos e os campos NUM_PARC e VL_PARC_PASS não
preenchidos (recuperação da informação referente ao componente); e
e) outro registro com tipo de movimentação igual a “AT”, “PE” ou “OT”, conforme o caso, representando a
saída do CIAP. Nesse 2º registro os campos VL_IMOB_ICMS_OP, VL_IMOB_ICMS_ST,
VL_IMOB_ICMS_FRT, VL_IMOB_ICMS_DIF, NUM_PARC e VL_PARC_PASS não podem ser
informados.
Campos 05 (VL_IMOB_ICMS_OP) – Preenchimento:
1) quando o tipo de movimentação for referente a uma entrada dos tipos “SI”, “IM”, “IA” e “MC”, considerar-se-á o valor do
ICMS originado do documento fiscal inclusive de ICMS originado de documento fiscal complementar;
2) quando o tipo de movimentação for referente a uma entrada do tipo “CI”, considerar-se-á o valor do ICMS como o somatório
do valor do ICMS dos seus respectivos componentes, cujas imobilizações ocorreram com o tipo de movimentação “IA”;
3) para os tipos de movimentação igual a “SI”, “IM”, “IA”, “CI” ou “MC”, pelo menos um desses campos deve ser maior que
Zero;
4) quando o tipo de movimentação for igual a “BA”, “AT”, “PE” ou “OT”, esses campos não devem ser informados.
Validação: esse campo deve ser menor ou igual à soma dos campos VL_ICMS_OP_APLICADO dos registros G140
hierarquicamente inferiores, se houver.
Campos 06 (VL_IMOB_ICMS_ST) – Preenchimento:
1) quando o tipo de movimentação for referente a uma entrada dos tipos “SI”, “IM”, “IA” e “MC”, considerar-se-á o valor do
ICMS originado do documento fiscal inclusive de ICMS originado de documento fiscal complementar;
2) quando o tipo de movimentação for referente a uma entrada do tipo “CI”, considerar-se-á o valor do ICMS como o somatório
do valor do ICMS dos seus respectivos componentes, cujas imobilizações ocorreram com o tipo de movimentação “IA”;
3) para os tipos de movimentação igual a “SI”, “IM”, “IA”, “CI” ou “MC”, pelo menos um desses campos deve ser maior que
Zero;
4) quando o tipo de movimentação for igual a “BA”, “AT”, “PE” ou “OT”, esses campos não devem ser informados.
Validação: esse campo deve ser menor ou igual à soma dos campos VL_ICMS_ST_APLICADO dos registros G140
hierarquicamente inferiores, se houver.
Campos 07 (VL_IMOB_ICMS_FRT) – Preenchimento:
1) quando o tipo de movimentação for referente a uma entrada dos tipos “SI”, “IM”, “IA” e “MC”, considerar-se-á o valor do
ICMS originado do documento fiscal inclusive de ICMS originado de documento fiscal complementar;
2) quando o tipo de movimentação for referente a uma entrada do tipo “CI”, considerar-se-á o valor do ICMS como o somatório
do valor do ICMS dos seus respectivos componentes, cujas imobilizações ocorreram com o tipo de movimentação “IA”;
3) para os tipos de movimentação igual a “SI”, “IM”, “IA”, “CI” ou “MC”, pelo menos um desses campos deve ser maior que
Zero;
4) quando o tipo de movimentação for igual a “BA”, “AT”, “PE” ou “OT”, esses campos não devem ser informados. Validação:
esse campo deve ser menor ou igual à soma dos campos VL_ICMS_FRT_APLICADO dos registros G140 hierarquicamente
inferiores, se houver.
Campos 08 (VL_IMOB_ICMS_DIF) – Preenchimento:
1) quando o tipo de movimentação for referente a uma entrada dos tipos “SI”, “IM”, “IA” e “MC”, considerar-se-á o valor do
ICMS originado do documento fiscal inclusive de ICMS originado de documento fiscal complementar;
2) quando o tipo de movimentação for referente a uma entrada do tipo “CI”, considerar-se-á o valor do ICMS como o somatório
do valor do ICMS dos seus respectivos componentes, cujas imobilizações ocorreram com o tipo de movimentação “IA”;
3) para os tipos de movimentação igual a “SI”, “IM”, “IA”, “CI” ou “MC”, pelo menos um desses campos deve ser maior que
Zero;
4) quando o tipo de movimentação for igual a “BA”, “AT”, “PE” ou “OT”, esses campos não devem ser informados.
Validação: esse campo deve ser menor ou igual à soma dos campos VL_ICMS_DIF_APLICADO dos registros G140
hierarquicamente inferiores, se houver.
Campo 09 (NUM_PARC) – Preenchimento: informe o número da parcela que está sendo escriturada.
Validação: informação obrigatória quando o conteúdo do campo 10 - VL_PARC_PASS for maior que Zero. (Erro)
Campo 10 (VL_PARC_PASS) - Preenchimento – Informe o valor passível de apropriação do crédito (total de créditos de
ICMS do bem ou componente dividido pela quantidade de parcelas) antes da aplicação do índice de participação do valor das
saídas tributadas/exportação no valor total das saídas (campo 08 - IND_PER_SAI do reg. G110). O valor informado neste
campo, quando maior que Zero, indica a escrituração e apropriação de valor de crédito de ICMS no período, independentemente
da informação constante no campo 04 - TIPO_MOV (tipo de movimentação).
Validação:
a) o valor informado deve ser igual ou menor que o somatório dos campos VL_IMOB_ICMS_OP, VL_IMOB_ICMS_ST, VL_IMOB_ICMS_FRT, VL_IMOB_ICMS_DIF, dividido pelo valor informado no campo NR_PARC do registro 0300;
b) informação obrigatória quando o conteúdo do campo 09 – NUM_PARC for maior que Zero.
----
REGISTRO G126: OUTROS CRÉDITOS CIAP
Este registro tem por objetivo discriminar os demais valores a serem apropriados como créditos de ICMS de Ativo
Imobilizado que não foram escriturados nos períodos anteriores, quando a legislação permitir.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "G126" C 004* - O
02 DT_INI Data inicial do período de apuração N 008* - O
03 DT_FIM Data final do período de apuração N 008* O
04 NUM_PARC Número da parcela do ICMS N 003 - O
05 VL_PARC_PASS Valor da parcela de ICMS passível de apropriação - N - 02 O
antes da aplicação da participação percentual do valor
das saídas tributadas/exportação sobre as saídas totais
06 VL_TRIB_OC Valor do somatório das saídas tributadas e saídas para N - 02 O
exportação no período indicado neste registro
07 VL_TOTAL Valor total de saídas no período indicado neste registro N - 02 O
08 IND_PER_SAI Índice de participação do valor do somatório das saídas N - 08 O
tributadas e saídas para exportação no valor total de
saídas (Campo 06 dividido pelo campo 07)
09 VL_PARC_APROP Valor de outros créditos de ICMS a ser apropriado na N - 02 O
apuração (campo 05 vezes o campo 08)
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [G126];
Campos 02 (DT_INI) - Preenchimento: informar a data inicial do período de apuração a que se refere a apropriação no formato
“ddmmaaaa”;
Campos 03 (DT_FIM) - Preenchimento: informar a data final do período de apuração a que se refere a apropriação no formato
“ddmmaaaa”;
Campo 04 (NUM_PARC) – Preenchimento: informar o número da parcela que está sendo apropriada;
Campo 05 (VL_PARC_PASS) – Preenchimento: informar o valor do crédito de ICMS passível de apropriação.
Campo 06 (VL_TRIB_OC) - Preenchimento: informar o valor das saídas tributadas e para a exportação do período referido
neste registro.
Campo 07 (VL_TOTAL)- Preenchimento: Informar o valor total das saídas do período referido neste registro, conforme a
legislação da unidade federada.
Campo 08 (IND_PER_SAI) - Preenchimento: Informar o valor do índice de participação correspondente ao resultado da
divisão do campo VL_TRIB_EXP pelo campo VL_TOTAL.
Campo 09 (VL_PARC_APROP) - Preenchimento: Informar o valor do crédito de ICMS a ser apropriado na apuração do
imposto. Validação: O valor informado neste campo deve ser menor ou igual ao resultado da multiplicação do valor constante
no campo 05 (VL_PARC_PASS) pelo índice de participação calculado no campo 08 (IND_PER_SAI).
----
REGISTRO G130: IDENTIFICAÇÃO DO DOCUMENTO FISCAL
Este registro tem o objetivo de identificar o documento fiscal que acobertou a entrada ou a saída do bem ou componente
do CIAP.
Quando o tipo de movimentação – TIPO_MOV do registro G125 – for igual a "MC", "IM", "IA" ou "AT", este registro
é obrigatório.
Caso exista previsão legal de emissão de documento fiscal para os demais tipos de movimentação – TIPO_MOV do
registro G125 – esse registro deverá ser informado.
No período em que se iniciar a obrigação de escrituração fiscal digital do CIAP ou quando isso ocorrer de forma
espontânea, este registro é obrigatório nas seguintes situações:
a) quando o tipo de movimentação – TIPO_MOV do registro G125 – for igual a “SI” e esse “SI” for originado dos
tipos de movimentação “IM”, “IA” ou “MC”;
b) quando o tipo de movimentação – TIPO_MOV do registro G125 – for igual a “SI” e esse “SI” for originado do tipo
de movimentação “CI”, devem ser informados os documentos fiscais relativos ao tipo de movimentação “IA” dos seus
componentes que entraram antes desse período;
c) quando o tipo de movimentação – TIPO_MOV do registro G125 – for igual a “CI”, devem ser informados os
documentos fiscais relativos ao tipo de movimentação “IA” dos seus componentes que entraram antes desse período.
Validação do Registro: Independentemente das situações referidas, esse registro será informado uma única vez. Não
podem ser informados dois ou mais registros com a mesma combinação de conteúdo nos campos IND_EMIT, COD_PART,
COD_MOD, SERIE, NUM_DOC, CHV_NFE_CTE para o mesmo bem ou componente.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "G130" C 004 - O
02 IND_EMIT Indicador do emitente do documento fiscal: C 001* - O
0- Emissão própria;
1- Terceiros
03 COD_PART Código do participante: C 060 - O
- do emitente do documento ou do remetente das mercadorias,
no caso de entradas;
- do adquirente, no caso de saídas
04 COD_MOD Código do modelo de documento fiscal, conforme tabela 4.1.1 C 002* - O
05 SERIE Série do documento fiscal C 003 - OC
06 NUM_DOC Número de documento fiscal N 009 - O
07 CHV_NFE_CTE Chave do documento fiscal eletrônico N 044* - OC
08 DT_DOC Data da emissão do documento fiscal N 008* - O
09 NUM_DA Número do documento de arrecadação estadual, se houver C - - OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [G130].
Campo 03 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 04 (COD_MOD)- Valores Válidos: [01, 1B, 04, 07, 08, 8B, 09, 10, 26, 27, 55 e 57]. Quando se tratar de NF-e ou CT-
e, serão validadas as chaves eletrônicas do respectivo documento.
Campo 07 (CHV_NFE_CTE) - Preenchimento: Informar chave dos documentos eletrônicos.
Campo 08 (DT_DOC) - Preenchimento: informar a data no formato “ddmmaaaa” sem separadores de formatação.
----
REGISTRO G140: IDENTIFICAÇÃO DO ITEM DO DOCUMENTO FISCAL
Este registro tem o objetivo de identificar o item do documento fiscal informado no registro G130.
Validação do Registro: Não podem ser informados dois ou mais registros com o mesmo valor no campo NUM_ITEM
+ COD_ITEM.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "G140" C 004 - O
02 NUM_ITEM Número sequencial do item no documento fiscal N 003 - O
03 COD_ITEM Código correspondente do bem no documento fiscal C 060 - O
(campo 02 do registro 0200)
04 QTDE Quantidade, deste item da nota fiscal, que foi aplicada N - 05 O
neste bem, expressa na mesma unidade constante no
documento fiscal de entrada
05 UNID Unidade do item constante no documento fiscal de C 6 - O
entrada
06 VL_ICMS_OP_APLICADO Valor do ICMS da Operação Própria na entrada do item, N - 02 O
proporcional à quantidade aplicada no bem ou
componente.
07 VL_ICMS_ST_APLICADO Valor do ICMS ST na entrada do item, proporcional à N - 02 O
quantidade aplicada no bem ou componente.
08 VL_ICMS_FRT_APLICADO Valor do ICMS sobre Frete do Conhecimento de N - 02 O
Transporte na entrada do item, proporcional à
quantidade aplicada no bem ou componente.
09 VL_ICMS_DIF_APLICADO Valor do ICMS Diferencial de Alíquota, na entrada do N - 02 O
item, proporcional à quantidade aplicada no bem ou
componente.
Observações:
Nível hierárquico - 5
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [G140];
Campo 03 (COD_ITEM) - Validação: o valor informado neste campo deve existir no registro 0200.
Campo 05 (UNID) - Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida
informada seja diferente da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no
Registro 0220 o fator de conversão entre as unidades de medida.
----
REGISTRO G990: ENCERRAMENTO DO BLOCO G
Este registro deve ser gerado para o encerramento do bloco G e indica o número total de registros existentes neste
bloco.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "G990" C 004* - O
02 QTD_LIN_G Quantidade total de linhas do Bloco G N - - O
Observações:
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Campo 01 (REG) - valor válido: [G990].

