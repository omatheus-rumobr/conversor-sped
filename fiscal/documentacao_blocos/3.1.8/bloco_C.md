# Bloco C - Versão 3.1.8

BLOCO C: DOCUMENTOS FISCAIS I – MERCADORIAS (ICMS/IPI)
----
# REGISTRO C001: ABERTURA DO BLOCO C
Este registro tem por objetivo identificar a abertura do bloco C, indicando se há informações sobre documentos fiscais.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "C001" C 004 - O
02 IND_MOV Indicador de movimento: C 001 - O
0- Bloco com dados informados;
1- Bloco sem dados informados
Observações:
Nível hierárquico - 1
Ocorrência - um por arquivo
Campo 01 (REG) - Valor válido: [C001]
Campo 02 (IND_MOV) - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a “1” (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a “0” (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
----
# REGISTRO C100: NOTA FISCAL (CÓDIGO 01), NOTA FISCAL AVULSA (CÓDIGO 1B),
NOTA FISCAL DE PRODUTOR (CÓDIGO 04), NF-e (CÓDIGO 55) e NFC-e (CÓDIGO 65).
Este registro deve ser gerado para cada documento fiscal código 01, 1B, 04, 55 e 65 (saída), conforme item 4.1.1 da Nota Técnica (Ato COTEPE/ICMS nº 44/2018 e alterações), registrando a entrada ou saída de produtos ou outras situações que envolvam a emissão dos documentos fiscais mencionados. As NFC-e (código 65) não devem ser escrituradas nas entradas. A partir do mês de referência abril de 2012, a informação do campo CHV_NFE passa a ser obrigatória em todas as situações, exceto para NF-e com numeração inutilizada (COD_SIT = 05).
A partir da vigência dos Ajustes SINIEF 34/2021 e 38/2021 (01/12/2021) deixa de ser obrigatória a informação referente aos documentos fiscais eletrônicos denegados ou com numeração inutilizada.
A partir de janeiro de 2023, os códigos de situação de documento 04 (NF-e ou CT-e denegado) e 05 (NF-e ou CT-e Numeração inutilizada) da tabela 4.1.2 - Tabela Situação do Documento serão descontinuados.
As informações para a escrituração do ICMS monofásico foram descritas na Nota Orientativa – 01/2023 – ICMS monofásico – setor de combustíveis, disponíveis no site http://sped.rfb.gov.br, módulo EFD ICMS IPI -> Downloads -> Notas Orientativas.
IMPORTANTE: para documentos de entrada, os campos de valor de imposto, base de cálculo e alíquota só devem ser
informados se o adquirente tiver direito à apropriação do crédito (enfoque do declarante).
Para cada registro C100, obrigatoriamente deve ser apresentado, pelo menos, um registro C170 e um registro C190,
observadas as exceções abaixo relacionadas:
Exceção 1: Para documentos com código de situação (campo COD_SIT) cancelado (código “02”), cancelado extemporâneo
(código “03”), Nota Fiscal Eletrônica (NF-e) denegada (código “04”), preencher somente os campos REG, IND_OPER,
IND_EMIT, COD_MOD, COD_SIT, SER, NUM_DOC e CHV_NF-e. Para COD-SIT = 05 (numeração inutilizada), todos os
campos referidos anteriormente devem ser preenchidos, exceto o campo CHV_NF-e. Demais campos deverão ser apresentados
com conteúdo VAZIO “||”. Não informar registros filhos. A partir de janeiro de 2011, no caso de NF-e de emissão própria com código de situação (campo COD_SIT) cancelado (código “02”) e cancelado extemporâneo (código “03”) deverão ser informados os campos acima citados incluindo ainda a chave da NF-e.
Exceção 2: Notas Fiscais Eletrônicas - NF-e de emissão própria: regra geral, devem ser apresentados somente os registros C100 e C190, e, se existirem ajustes de documento fiscais determinados por legislação estadual (tabela 5.3 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações), devem ser apresentados também os registros C195 e C197;somente será admitida a informação do registro C170 quando também houver sido informado o registro C176, C180, C181 ou o Registro C177 (no caso de haver informações complementares do item, a partir de 01/01/2019 - Tabela 5.6). A critério de cada UF, informar os registros C110 e C120, a partir de julho de 2012. O registro C101 deverá ser informado, a partir de janeiro/2016, nas operações interestaduais que destinem bens e serviços a consumidor final não contribuinte do ICMS, conforme EC 87/15. A partir de janeiro de 2020, também poderá ser informado o Registro C185, a critério de cada UF. A partir de janeiro de 2021, poderá ser informado o Registro C186, a critério de cada UF.
Exceção 3: Notas Fiscais Complementares e Notas Fiscais Complementares escrituradas extemporaneamente (campo
COD_SIT igual a “06” ou “07”): nesta situação, somente os campos REG, IND_EMIT, COD_PART, COD_MOD, COD_SIT,
NUM_DOC, CHV_NFE e DT_DOC são de preenchimento obrigatório, devendo ser preenchida a data de efetiva saída, para
os contribuintes das UF que utilizam a data de saída para a apuração. Os demais campos são facultativos (se forem preenchidos, inclusive com valores iguais a zero, serão validadas e aplicadas as regras de campos existentes). O registro C190 é sempre obrigatório e deve ser preenchido. Os demais campos e registros filhos do registro C100 serão informados, quando houver informação a ser prestada. Se for informado o registro C170 o campo NUM_ITEM deve ser preenchido.
Exceção 4: Notas Fiscais emitidas por regime especial ou norma específica (campo COD_SIT igual a “08”). Para documentos fiscais emitidos com base em regime especial ou norma específica, deverão ser apresentados os registros C100 e C190, obrigatoriamente, e os demais registros “filhos”, se estes forem exigidos pela legislação fiscal. Nesta situação, para o registro C100, somente os campos REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD, COD_SIT, NUM_DOC e DT_DOC são de preenchimento obrigatório. A partir do mês de referência abril de 2012 a informação do campo CHV_NFE passa a ser obrigatória neste caso para modelo 55. Os demais campos, com exceção do campo NUM_ITEM do registro C170, são facultativos (se forem preenchidos, inclusive com valores iguais a Zero, serão validados e aplicadas as regras de campos existentes) e deverão ser preenchidos, quando houver informação a ser prestada. Exemplos: a) Nota fiscal emitida em substituição ao cupom fiscal – CFOP igual a 5.929 ou 6.929 – (lançamento efetuado em decorrência de emissão de documento fiscal relativo à operação ou à prestação também registrada em equipamento Emissor de Cupom Fiscal – ECF, exceto para o contribuinte do Estado do Paraná, que deve efetuar a escrituração de acordo com a regra estabelecida na tabela de código de ajustes e para outras UF onde a regulamentação seja diferente); b) Nos casos em que a legislação estadual permitir a emissão de NF sem informações do destinatário, preencher os dados do próprio emitente. Obs.: a partir de janeiro de 2012, para todos os documentos não eletrônicos e com COD_SIT igual a “08”, deverá ser informada no registro C110 a norma legal que autoriza o preenchimento do documento fiscal nessa situação.
Exceção 5: Para os documentos fiscais emitidos de acordo com o estabelecido em regimes especiais ou normas específicas, devidamente autorizados pelo fisco (campo COD_SIT igual a “08”), será permitida a informação de data de emissão de documento maior que a data de entrada ou saída. Exemplo: aquisição de cana-de-açúcar, venda de derivados de petróleo, etc. Será emitida Advertência pelo PVA-EFD-ICMS/IPI.
Exceção 6: Venda de produtos que geram direito a ressarcimento com utilização de NF-e: Nos casos de vendas, para outro
estado, de produtos tributados por ST na operação anterior o contribuinte deverá indicar no registro C176 os dados para futura solicitação de ressarcimento. O registro C170 deverá ser preenchido apenas com os itens da NF que gerem direito ao pedido de ressarcimento, devendo também ser preenchido o registro C176 (utilização a partir de 01/06/2009). A UF determinará a obrigatoriedade deste registro.
Exceção 7: Escrituração de documentos emitidos por terceiros: os casos de escrituração de documentos fiscais, inclusive NF-e e NFC-e, emitidos por terceiros (como por exemplo. o consórcio constituído nos termos do disposto nos artigos. 278 e 279 da Lei nº 6.404, de 15 de dezembro de 1976) e das NF-e “avulsas” emitidas pelas UF (séries 890 a 899) devem ser informados como emissão de terceiros, com o código de situação do documento igual a “08 - Documento Fiscal emitido com base em Regime Especial ou Norma Específica”. O PVA-EFD-ICMS/IPI exibirá a mensagem de Advertência para esses documentos.
Obs.: Os documentos fiscais emitidos pelas filiais das empresas que possuam inscrição estadual única ou sejam autorizadas pelos fiscos estaduais a centralizar suas escriturações fiscais deverão ser informados como sendo de emissão própria e código de situação igual a “00 – Documento regular”. Excepcionalmente, até junho de 2012, poderão ser informados como sendo de emissão de terceiros e código de situação de documento como sendo “08”.
Exceção 8: NF-e com o campo UF de consumo preenchido: nos casos de NF-e de emissão própria, quando o campo UF de
consumo for preenchido (onde a UF de consumo é diversa da UF do destinatário), deve ser informado no registro C105.
Exceção 9: Notas fiscais eletrônicas ao consumidor final - NFC-e (modelo 65): via de regra, devem ser apresentados somente os registros C100 e C190 e, se existirem ajustes de documento fiscais determinados por legislação estadual (tabela 5.3 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações), devem ser apresentados também os registros C195 e C197. No registro C100, não devem ser informados os campos COD_PART, VL_BC_ICMS_ST, VL_ICMS_ST, VL_IPI, VL_PIS, VL_COFINS, VL_PIS_ST e VL_COFINS_ST. Os demais campos seguirão a obrigatoriedade definida pelo registro.
As NFC-e não devem ser escrituradas nas entradas. A partir de janeiro de 2020, também poderá ser informado o Registro
C185, a critério de cada UF.
Exceção 10: nos casos em que houver informações complementares do item (tabela 5.6 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações) a serem prestadas no Registro C177 (utilização a partir de 01/01/2019), o registro C170 deverá ser informado, inclusive para NF-e de emissão própria. A UF determinará a obrigatoriedade deste registro.
Validação do Registro: Não podem ser informados, para um mesmo documento fiscal, dois ou mais registros com a mesma
combinação de valores dos campos formadores da chave do registro. A chave deste registro é:
• para documentos com campo IND_EMIT igual a “1-Terceiros”: campo IND_OPER, campo IND_EMIT, campo COD_PART, campo COD_MOD, campo COD_SIT, campo SER, campo NUM_DOC e campo CHV_NFE;
• para documentos com campo (IND_EMIT igual “0-Emissão Própria”: campo IND_OPER, campo IND_EMIT, campo COD_MOD, campo COD_SIT, campo SER, campo NUM_DOC e campo CHV_NFE. Será emitida mensagem de advertência quando houver dois ou mais registros C100 com a mesma combinação de campos IND_EMIT, COD_SIT, COD_PART, SER e NUM_DOC, exceto se forem dois ou mais C100 com COD_MOD igual a 55 ou
65.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Entr | Saída |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C100" | C | 004 | - | O | O |
| 02 | IND_OPER | Indicador do tipo de operação:<br>0 - Entrada;<br>1 - Saída | C | 001* | - | O | O |
| 03 | IND_EMIT | Indicador do emitente do documento fiscal:<br>0 - Emissão própria;<br>1 - Terceiros | C | 001* | - | O | O |
| 04 | COD_PART | Código do participante (campo 02 do Registro 0150):<br>- do emitente do documento ou do remetente das mercadorias, no caso de entradas;<br>- do adquirente, no caso de saídas | C | 060 | - | O | O |
| 05 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | O | O |
| 06 | COD_SIT | Código da situação do documento fiscal, conforme a Tabela 4.1.2 | N | 002* | - | O | O |
| 07 | SER | Série do documento fiscal | C | 003 | - | OC | OC |
| 08 | NUM_DOC | Número do documento fiscal | N | 009 | - | O | O |
| 09 | CHV_NFE | Chave da Nota Fiscal Eletrônica | N | 044* | - | OC | OC |
| 10 | DT_DOC | Data da emissão do documento fiscal | N | 008* | - | O | O |
| 11 | DT_E_S | Data da entrada ou da saída | N | 008* | - | O | OC |
| 12 | VL_DOC | Valor total do documento fiscal | N | - | 02 | O | O |
| 13 | IND_PGTO | Indicador do tipo de pagamento:<br>0 - À vista;<br>1 - A prazo;<br>9 - Sem pagamento.<br><br>Obs.: A partir de 01/07/2012 passará a ser:<br>0 - À vista;<br>1 - A prazo;<br>2 - Outros | C | 001* | - | O | O |
| 14 | VL_DESC | Valor total do desconto | N | - | 02 | OC | OC |
| 15 | VL_ABAT_NT | Abatimento não tributado e não comercial<br>Por exemplo: desconto ICMS nas remessas para ZFM. | N | - | 02 | OC | OC |
| 16 | VL_MERC | Valor total das mercadorias e serviços | N | - | 02 | O | OC |
| 17 | IND_FRT | Indicador do tipo do frete:<br>0 - Por conta de terceiros;<br>1 - Por conta do emitente;<br>2 - Por conta do destinatário;<br>9 - Sem cobrança de frete.<br><br>Obs.: A partir de 01/01/2012 passará a ser:<br>0 - Por conta do emitente;<br>1 - Por conta do destinatário/remetente;<br>2 - Por conta de terceiros;<br>9 - Sem cobrança de frete.<br><br>Obs: A partir de 01/01/2018 passará a ser:<br>0 - Contratação do Frete por conta do Remetente (CIF);<br>1 - Contratação do Frete por conta do Destinatário (FOB);<br>2 - Contratação do Frete por conta de Terceiros;<br>3 - Transporte Próprio por conta do Remetente;<br>4 - Transporte Próprio por conta do Destinatário;<br>9 - Sem Ocorrência de Transporte. | C | 001* | - | O | O |
| 18 | VL_FRT | Valor do frete indicado no documento fiscal | N | - | 02 | OC | OC |
| 19 | VL_SEG | Valor do seguro indicado no documento fiscal | N | - | 02 | OC | OC |
| 20 | VL_OUT_DA | Valor de outras despesas acessórias | N | - | 02 | OC | OC |
| 21 | VL_BC_ICMS | Valor da base de cálculo do ICMS | N | - | 02 | OC | OC |
| 22 | VL_ICMS | Valor do ICMS | N | - | 02 | OC | OC |
| 23 | VL_BC_ICMS_ST | Valor da base de cálculo do ICMS substituição tributária | N | - | 02 | OC | OC |
| 24 | VL_ICMS_ST | Valor do ICMS retido por substituição tributária | N | - | 02 | OC | OC |
| 25 | VL_IPI | Valor total do IPI | N | - | 02 | OC | OC |
| 26 | VL_PIS | Valor total do PIS | N | - | 02 | OC | OC |
| 27 | VL_COFINS | Valor total da COFINS | N | - | 02 | OC | OC |
| 28 | VL_PIS_ST | Valor total do PIS retido por substituição tributária | N | - | 02 | OC | OC |
| 29 | VL_COFINS_ST | Valor total da COFINS retido por substituição tributária | N | - | 02 | OC | OC |
Observações:
Nível hierárquico – 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C100]
Campo 02 (IND_OPER) - Valores válidos: [0, 1]
Preenchimento: indicar a operação, conforme os códigos. Podem ser informados como documentos de entrada os emitidos
por terceiros ou pelo próprio informante da EFD-ICMS/IPI.
Campo 03 (IND_EMIT) - Valores válidos: [0, 1]
Preenchimento: consideram-se de emissão própria somente os documentos fiscais emitidos pelo estabelecimento informante
(campo CNPJ do registro 0000) da EFD-ICMS/IPI. Documentos emitidos por outros estabelecimentos ainda que da mesma
empresa, devem ser considerados como documentos emitidos por terceiros. Nos casos de escrituração de documentos fiscais
de terceiros em operações de saídas (exemplo: consórcios de empresas), deve ser informado no campo 06 (COD_SIT) o código
“08”.
Se a legislação estadual a que estiver submetido o contribuinte obrigá-lo a escriturar notas fiscais avulsas em operação de saída,
este campo deve ser informado com valor igual a “0” (zero).
Validação: se este campo tiver valor igual a “1” (um), o campo IND_OPER deve ser igual a “0” (zero).
Campo 04 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150. Quando se
tratar de NFC-e (modelo 65), o campo não deve ser preenchido
Campo 05 (COD_MOD) - Valores válidos: [01, 1B, 04, 55, 65]
Preenchimento: o valor informado deve constar na tabela 4.1.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº
44/2018 e alterações, reproduzida na subseção 1.4 deste guia. O “código” a ser informado não é exatamente o “modelo” do
documento, devendo ser consultada a tabela 4.1.1. Exemplo: o código “01” deve ser utilizado para os modelos “1” ou “1A".
Campo 06 (COD_SIT) - Valores válidos: [00, 01, 02, 03, 04, 05, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3. Para todo documento diferente de NF-e de
emissão própria com COD_SIT igual a “08” é obrigatório preencher o registro C110 para informar os dispositivos legais que
permitem a emissão do documento fiscal naquela situação. Os valores “04” e “05” somente são possíveis para NF-e ou NFC-e
até 31/12/2022.
Validação: os valores “04” e “05” somente são possíveis para NF-e ou NFC-e.
Campo 07 (SER) – Validação: campo de preenchimento obrigatório com três posições para NF-e, COD_MOD igual a “55”,
de emissão própria ou de terceiros e para NFC-e, COD_MOD igual a “65” de emissão própria. Se não existir Série para NF-e
ou NFC-e, informar 000.
Campo 08 (NUM_DOC) – Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 09 (CHV_NFE) - Preenchimento: campo de preenchimento obrigatório para NF-e, COD_MOD igual a “55”, de
emissão própria ou de terceiros e para NFC-e, COD_MOD igual a “65” de emissão própria. A partir de abril de 2012, a chave
da NF-e é obrigatória em todas as situações, exceto para NFe com numeração inutilizada (COD_SIT = 05).
Validação: é conferido o dígito verificador (DV) da chave da NF-e e da NFC-e de emissão própria. Este campo é de
preenchimento obrigatório para COD_MOD igual a “55” e “65”. Para confirmação inequívoca de que a chave da NF-e/NFC-e
corresponde aos dados informados do documento, é comparado o CNPJ base existente na CHV_NFE com o campo CNPJ base
do registro 0000, que corresponde ao CNPJ do informante do arquivo, no caso de IND_EMIT = 0 (emissão própria). São
verificados a consistência da informação dos campos NUM_DOC e SER com o número do documento e série contidos na
chave da NF-e. É também comparada a UF codificada na chave da NF-e com o campo UF informado no registro 0000.
Campo 10 (DT_DOC) - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se
quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 11 (DT_E_S) - Preenchimento: informar a data de entrada ou saída, conforme a operação, no formato ddmmaaaa;
excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”. Quando o campo IND_OPER indicar operação de
“saída”, este campo será informado apenas se o contribuinte possuir este dado em seus sistemas.
Validação: este campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000. Para operações de entrada ou
saída este valor deve ser maior ou igual à data de emissão (campo DT_DOC).
Nas operações de entradas de produtos este campo é sempre de preenchimento obrigatório.
Importante: Se a legislação do ICMS definir que o imposto deve ser apropriado com base na data de emissão dos documentos
fiscais, proceder da seguinte forma: todos os documentos de saídas com código de situação de documento igual a “00”
(documento regular) devem ser lançados no período de apuração informado no registro 0000, considerando a data de emissão
do documento, e, se a data de saída for maior que a data final do período de apuração, este campo não pode ser preenchido.
Se a legislação do ICMS definir que o imposto deve ser apropriado com base na data da saída dos produtos, proceder da seguinte
forma: todos os documentos de saídas com código de situação de documento igual a “00” (documento regular) devem ser
lançados no período de apuração informado no registro 0000, considerando a data de saída do produto informada no documento.
Campo 12 (VL_DOC) – Validação: o valor informado neste campo deve ser igual à soma do campo VL_OPR dos registros
C190 (“filhos” deste registro C100). Nos casos em que houver divergência entre o valor total da nota fiscal e o somatório dos
valores da operação informados no Registro C190, serão exibidas mensagens de “Advertência”.
Campo 13 (IND_PGTO) - Valores válidos: [0, 1, 2, 9]
Campo 14 (VL_DESC) - Preenchimento: informar o valor do desconto incondicional discriminado na nota fiscal.
Campo 15 (VL_ABAT_NT) - Preenchimento: o valor informado deve corresponder ao somatório dos valores do Campo
VL_ABAT_NT dos Registros C170.
Campo 16 (VL_MERC) - Validação: se o campo COD_MOD for diferente de “55”, campo IND_EMIT for diferente de “0”
e o campo COD_SIT for igual a “00” ou “01”, o valor informado no campo deve ser igual à soma do campo VL_ITEM dos
registros C170 (“filhos” deste registro C100).
Campo 17 (IND_FRT) - Valores válidos: [0, 1, 2, 9]
Preenchimento: Em operações tais como: remessas simbólicas, faturamento simbólico, transporte próprio, venda balcão,
informar o código “9 - sem frete”, ou seja, operações sem cobrança de frete.
Quando houver transporte com mais de um responsável pelo seu pagamento, deve ser informado o indicador do frete relativo
ao responsável pelo primeiro percurso.
A partir de 01/01/2018: Valores válidos: [0, 1, 2, 3, 4, 9]
Campo 21 (VL_BC_ICMS) - Validação: a soma dos valores do campo VL_BC_ICMS dos registros analíticos (C190) deve
ser igual ao valor informado neste campo.
Campo 22 (VL_ICMS) – Preenchimento: informar o valor do ICMS creditado na operação de entrada ou o valor do ICMS
debitado na operação de saída.
Validação: a soma dos valores do campo VL_ICMS dos registros analíticos (C190) deve ser igual ao valor informado neste
campo.
Campo 23 (VL_BC_ICMS_ST) - Validação: a soma dos valores do campo VL_BC_ICMS_ST dos registros analíticos (C190)
deve ser igual ao valor informado neste campo.
Campo 24 (VL_ICMS_ST) - Preenchimento: informar o valor do ICMS creditado/debitado por substituição tributária, nas
operações de entrada ou saída, conforme legislação aplicada.
Validação: A soma dos valores do campo VL_ICMS_ST dos registros analíticos (C190) deve ser igual ao valor informado
neste campo.
Campo 25 (VL_IPI) - Validação: a soma dos valores do campo VL_IPI dos registros analíticos (C190) deve ser igual ao valor
informado neste campo.
Campo 26 (VL_PIS) - Preenchimento: informar o valor do montante creditado, se existente, nas operações de entrada e o
montante debitado, se existente, nas operações de saída. Os contribuintes que entregarem a EFD-Contribuições relativa ao
mesmo período de apuração do registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO
“||”.
Atualização: 31 de outubro de 2024
Campo 27 (VL_COFINS) - Preenchimento: informar o valor do montante creditado, se existente, nas operações de entrada e
o montante debitado, se existente, nas operações de saída. Os contribuintes que entregarem a EFD-Contribuições relativa ao
mesmo período de apuração do registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO
“||”.
Campo 28 (VL_PIS_ST) - Preenchimento: informar o valor do montante creditado, se existente, nas operações de entrada e
o montante debitado, se existente, nas operações de saída. Os contribuintes que entregarem a EFD-Contribuições relativa ao
mesmo período de apuração do registro 0000 estão dispensados do preenchimento deste campo.
Campo 29 (VL_COFINS_ST) - Preenchimento: informar o valor do montante creditado, se existente, nas operações de
entrada e o montante debitado, se existente, nas operações de saída. Os contribuintes que entregarem a EFD-Contribuições
relativa ao mesmo período de apuração do registro 0000 estão dispensados do preenchimento deste campo.
Informações adicionais:
1) Como deve ser a apresentação da nota fiscal nesse registro quando ocorrerem situações em que a legislação disponha que
alguns valores devem ser zerados na escrituração da nota fiscal? Deve seguir a mesma regra de escrituração dos livros fiscais?
Ou deve ser apresentado o valor conforme destacado no documento?
Resposta: O contribuinte obrigado à EFD-ICMS/IPI deve seguir as regras estaduais de escrituração existentes, lançando ou não
o ICMS e o ICMS ST a ser efetivamente debitado ou creditado.
2) Campo 15 - Valor do abatimento não tributado e não comercial: além do exemplo do desconto da ZFM em qual outra
situação deve ser preenchido?
Resposta: Cada legislação estadual prevê situações específicas. Abaixo, exemplo de duas situações previstas no Regulamento
do ICMS/MG.
Sit. 1 - Quando a aplicação da redução de base de cálculo ficar condicionada ao repasse para o contribuinte do valor equivalente
ao imposto dispensado na operação. Exemplo: SEF MG - RICMS/02, Anexo IV, item 2 (condição 2.1, b).
Sit. 2 - Isenção com repasse para o contribuinte na saída, em operação interna, de mercadoria ou bem destinado a órgãos da
administração pública estadual direta, suas fundações e autarquias. Exemplo: SEF MG - RICMS/02, Anexo I, item 136.
3) Nos registros de entrada, os valores de ICMS ST e IPI destacados nos documentos fiscais, quando o informante não tem
direito ao crédito, devem ser incorporados ao valor das mercadorias?
Resposta: Sim, nestes casos, os valores do ICMS ST e/ou IPI destacados devem ser adicionados ao valor das mercadorias que
é informado no campo 16 – “VL_MERC” do registro C100, bem como no campo 07 – “VL_ITEM” do registro C170, uma vez
que compõem o custo das mercadorias. Como o informante não tem direito à apropriação do crédito, os campos “VL_ICMS_ST”
e/ou “VL_IPI” dos registros C100, C170 e C190 não devem ser informados.”
----
# REGISTRO C101: INFORMAÇÃO COMPLEMENTAR DOS DOCUMENTOS FISCAIS
QUANDO DAS OPERAÇÕES INTERESTADUAIS DESTINADAS A CONSUMIDOR FINAL
NÃO CONTRIBUINTE EC 87/15 (CÓDIGO 55)
Este registro tem por objetivo prestar informações complementares constantes da NF-e quando das operações
interestaduais destinadas a consumidor final NÃO contribuinte do ICMS, segundo dispôs a Emenda Constitucional 87/2015.
Deverão ser informadas as apurações do E300 e filhos para as UF de origem e destino da operação.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo “C101” C 004 - O O
02 VL_FCP_UF_DEST Valor total relativo ao Fundo de Combate à N - 02 O O
Pobreza (FCP) da UF de destino
03 VL_ICMS_UF_DEST Valor total do ICMS Interestadual para a UF de N - 02 O O
destino
04 VL_ICMS_UF_REM Valor total do ICMS Interestadual para a UF N - 02 O O
do remetente
Nível hierárquico – 3
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C101]
Exemplo de lançamento quando ocorre devolução:
Em caso de devolução de bens vendidos a não contribuinte do ICMS localizado em outra UF, via de regra o vendedor deverá emitir nota fiscal de entrada, já que o adquirente, por não ser contribuinte do ICMS, não emite nota fiscal. Com a emissão pelo próprio vendedor da NF-e de entrada, o lançamento na EFD no registro C101 ficará assim, considerando no exemplo que as duas notas, tanto de saída quanto de entrada, do estado “A” para o estado “B”, e em seguida devolvida para o estado “A” (se a devolução for feita através de NF-e Avulsa, o procedimento para o lançamento da EFD é o mesmo):
a. No Registro C101 referentes à nota fiscal de saídas – do estado “A” para o estado “B”: Registro C101 Valor FCP UF Campo “VL_FCP_UF_DEST” 10,00* Destino Valor ICMS UF Campo “VL_ICMS_UF_DEST” 40,00 Destino Valor ICMS UF Campo “VL_ICMS_UF_REM” 60,00 Remetente
b. No Registro C101 referente à nota fiscal de entrada (devolução):
Registro C101
Valor FCP UF Campo “VL_FCP_UF_DEST” 10,00*
Remetente
Valor ICMS UF Campo “VL_ICMS_UF_DEST” 60,00
Destino
Valor ICMS UF Campo “VL_ICMS_UF_REM” 40,00
Remetente
*FCP
O valor referente ao Fundo de Combate à Pobreza, que nestas operações é devido exclusivamente ao estado de destino (B),
deve ser informado para anular a operação anterior, caso o estado de destino (B) permita o lançamento a crédito para anular a
operação anterior. Maiores esclarecimentos, consultar a Secretaria de Fazenda da unidade referida.
Observe que o princípio da origem e destino foi mantido. Como na devolução há a inversão, o vendedor que é origem na venda
passa a ser destino na devolução.
ICMS DA ORIGEM
Com isso, o PVA dará o tratamento adequado, anulando a operação anterior. Na venda, o valor de R$ 60,00 é informado no
registro C101 no campo destinado ao estado de origem (A). Já na devolução, o mesmo valor de R$ 60,00 é informado no
registro C101 no campo destinado ao estado de destino (A).
ICMS DO DESTINO
O mesmo tratamento é dado ao ICMS devido no destino (B), já que na venda, o valor de R$ 40,00 é informado no registro
C101 no campo destinado à UF de destino (B) e na devolução o mesmo valor de R$ 40,00 é informado no registro C101 no
campo destinado ao estado de origem (remetente) (B).
----
# REGISTRO C105: OPERAÇÕES COM ICMS ST RECOLHIDO PARA UF DIVERSA DO
DESTINATÁRIO DO DOCUMENTO FISCAL (CÓDIGO 55).
Este registro tem por objetivo identificar a UF destinatária do recolhimento do ICMS ST, quando esta for diversa da
UF do destinatário do produto. Exemplo: Leasing de veículo quando a entidade financeira está localizada em uma UF e o
destinatário do produto em outra UF.
Durante o ano de 2009, as empresas sujeitas ao recolhimento a UFs diferentes do destinatário dos produtos deverão
estornar o débito correspondente à UF do destinatário do documento fiscal e deverão adicionar o valor correspondente na
apuração do ICMS ST para a UF do recolhimento do tributo.
A partir de período de apuração de janeiro de 2010, essas empresas deverão utilizar o registro C105 para que possa
ser identificada a UF de destino do ICMS ST.
Na hipótese de recusa de recebimento em que a legislação determine que a nota de retorno, escriturada no Registro
C100, campo 03 (IND_EMIT) com valor “0 - Emissão própria”, seja emitida com as informações do emitente nos campos do
destinatário, este registro pode ser utilizado para que o ICMS ST seja creditado na apuração da UF em que se situa o contribuinte
que efetuou a recusa, desde que essa UF seja indicada nos campos específicos de local de retirada, que seja indicada a finalidade
de emissão da NFe como devolução de mercadoria, que os CFOPs dos itens correspondam a operação de devolução previstos
na validação do campo 04 (VL_DEVOL_ST), do Registro E210, e seja indicada no campo de documento fiscal referenciado a
chave da NFe de remessa que foi recusada.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 REG Texto fixo contendo “C105” C 004 - O O
02 OPER Indicador do tipo de operação: N 001* - O O
0 - Combustíveis e Lubrificantes;
1 - Leasing de veículos ou faturamento direto.
2 - Recusa de recebimento (de acordo com as
condições descritas nas instruções do Registro)
03 UF Sigla da UF de destino do ICMS_ST C 002* - O O
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C105]
Campo 02 (OPER) - Valores Válidos: [0, 1, 2]
Campo 03 (UF) - Validação: o valor deve ser a sigla da unidade da federação (UF) de destino do ICMS ST.
----
# REGISTRO C110: INFORMAÇÃO COMPLEMENTAR DA NOTA FISCAL (CÓDIGO 01, 1B, 04
e 55).
Este registro tem por objetivo identificar os dados contidos no campo Informações Complementares da Nota Fiscal,
que sejam de interesse do fisco, conforme dispõe a legislação. Devem ser discriminadas em registros “filhos próprios” as
informações relacionadas com documentos fiscais, processos, cupons fiscais, documentos de arrecadação e locais de entrega
ou coleta que foram explicitamente citadas no campo “Informações Complementares” da Nota Fiscal.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o
mesmo conteúdo no campo COD_INF.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C110" C 004 - O O
02 COD_INF Código da informação complementar do C 006 - O O
documento fiscal (campo 02 do Registro 0450)
03 TXT_COMPL Descrição complementar do código de referência. C - - OC OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor válido: [C110]
Campo 02 (COD_INF) - Validação: o valor informado no campo deve existir no registro 0450 - Tabela de informação complementar.
----
# REGISTRO C111: PROCESSO REFERENCIADO
Este registro deve ser apresentado, obrigatoriamente, quando no campo – “Informações Complementares” da nota
fiscal - constar a discriminação de processos referenciados no documento fiscal.
Validação do Registro: Não podem ser informados dois ou mais registros com o mesmo conteúdo no campo
NUM_PROC para um mesmo registro C110.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C111" C 004 - O O
02 NUM_PROC Identificação do processo ou ato concessório. C 060 - O O
03 IND_PROC Indicador da origem do processo: C 001* - O O
0 - SEFAZ;
1 - Justiça Federal;
2 - Justiça Estadual;
3 - SECEX/SRF
9 - Outros.
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C111]
Campo 03 (IND_PROC) - Valores válidos: [0, 1, 2, 3, 9]
----
# REGISTRO C112: DOCUMENTO DE ARRECADAÇÃO REFERENCIADO
Este registro deve ser apresentado, obrigatoriamente, quando no campo – “Informações Complementares” da nota
fiscal - constar a identificação de um documento de arrecadação.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C112" C 004 - O O
02 COD_DA Código do modelo do documento de arrecadação: C 001* - O O
0 – Documento estadual de arrecadação
1 – GNRE
03 UF Unidade federada beneficiária do recolhimento C 002* - O O
04 NUM_DA Número do documento de arrecadação C - - OC OC
05 COD_AUT Código completo da autenticação bancária C - - OC OC
06 VL_DA Valor do total do documento de arrecadação N - 02 O O
(principal, atualização monetária, juros e multa)
07 DT_VCTO Data de vencimento do documento de arrecadação N 008* - O O
08 DT_PGTO Data de pagamento do documento de arrecadação, N 008* - O O
ou data do vencimento, no caso de ICMS
antecipado a recolher.
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C112]
Campo 02 (COD_DA) - Valores válidos: [0, 1]
Campo 03 (UF) – Validação: o valor deve ser a sigla da UF beneficiária do recolhimento.
Campo 05 (COD_AUT) - Validação: se não for informado valor no campo NUM_DA, obrigatoriamente, o campo COD_AUT deve ser informado.
Campo 06 (VL_DA) - Preenchimento: informar o valor total do documento de arrecadação, ainda que este documento seja referenciado em mais de uma nota fiscal, situação em que haverá um registro C112, idêntico e vinculado a cada nota fiscal (C100).
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 (DT_VCTO) - Preenchimento: informar a data de vencimento do documento de arrecadação no formato “ddmmaaaa”.
Campo 08 (DT_PGTO) - Preenchimento: informar a data de pagamento do documento de arrecadação no formato “ddmmaaaa”.
Como a data de pagamento é uma informação obrigatória, deve ser preenchida mesmo que o documento de arrecadação ainda não tenha sido pago, situação em que a data de vencimento deve ser informada neste campo. Por exemplo, nos casos de ICMS antecipado.
----
# REGISTRO C113: DOCUMENTO FISCAL REFERENCIADO
Este registro tem por objetivo informar, detalhadamente, outros documentos fiscais que tenham sido mencionados nas
informações complementares do documento que está sendo escriturado no registro C100, exceto cupons fiscais, que devem ser
informados no registro C114. Exemplos: nota fiscal de remessa de mercadoria originária de venda para entrega futura e nota
fiscal de devolução de compras.
Validação do Registro: Não podem ser informados, para um mesmo documento fiscal, dois ou mais registros com a
mesma combinação de valores dos campos formadores da chave do registro. A chave deste registro é: Para documentos emitidos
por terceiros: campos IND_EMIT, COD_PART, COD_MOD, SER e NUM_DOC. Para documentos de emissão própria:
campos IND_EMIT, COD_MOD, SER e NUM_DOC.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C113" C 004 - O O
02 IND_OPER Indicador do tipo de operação: C 001* - O O
0- Entrada/aquisição;
1- Saída/prestação
03 IND_EMIT Indicador do emitente do título: C 001* - O O
0- Emissão própria;
1- Terceiros
04 COD_PART Código do participante emitente (campo 02 C 060 - O O
do Registro 0150) do documento
referenciado.
05 COD_MOD Código do documento fiscal, conforme a C 002* - O O
Tabela 4.1.1
06 SER Série do documento fiscal C 004 - OC OC
07 SUB Subsérie do documento fiscal N 003 - OC OC
08 NUM_DOC Número do documento fiscal N 009 - O O
09 DT_DOC Data da emissão do documento fiscal. N 008* - O O
10 CHV_DOCe Chave do Documento Eletrônico N 044* - OC OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C113]
Campo 02 (IND_OPER) - Valores válidos: [0, 1]
Campo 03 (IND_EMIT) - Valores válidos: [0, 1]
Validação: se o valor neste campo for igual a “1” (um), então o campo IND_OPER deve ser igual a “0” (zero).
Campo 04 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150. Quando se tratar de NFC-e (modelo 65), o campo não deve ser preenchido.
Campo 05 (COD_MOD) - Preenchimento: informar o código do documento fiscal, conforme tabela 4.1.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações, reproduzida na subseção 1.4 deste guia.
Validação: o valor informado no campo deve existir na Tabela de Documentos Fiscais do ICMS (tabela 4.1.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações). O valor informado neste campo deve ser diferente de “2D”, “02” e “2E”.
Campo 08 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 09 (DT_DOC) - Preenchimento: data da emissão da NF no formato “ddmmaaaa”.
Validação: o valor informado neste campo deve ser menor ou igual ao valor do campo DT_DOC do registro C100.
Campo 10 (CHV_DOCe) - Preenchimento: informar a chave da NF-e, para documentos de COD_MOD igual a “55”, ou informar a chave do conhecimento de transporte eletrônico para documentos de COD_MOD igual a “57” (a vigorar a partir de 01/01/2017). A partir de abril/2017, informar a chave do CT-e OS.
Validação: quando se tratar de NF-e, CT-e ou CT-e OS, é conferido o dígito verificador (DV) da chave do documento
eletrônico. Será verificada a consistência da informação dos campos NUM_DOC e SER com o número do documento e série
contidos na chave do documento eletrônico.
----
# REGISTRO C114: CUPOM FISCAL REFERENCIADO
Este registro será utilizado para informar, detalhadamente, nas operações de saídas, cupons fiscais que tenham sido
mencionados nas informações complementares do documento que está sendo escriturado no registro C100. Nas operações de
entradas, somente informar quando o emitente do cupom fiscal for o próprio informante do arquivo.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com a
mesma combinação de conteúdo nos campos ECF_FAB, NUM_DOC e DT_DOC.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C114" C 004 - O O
02 COD_MOD Código do modelo do documento fiscal, C 002* - O O
conforme a tabela indicada no item 4.1.1
03 ECF_FAB Número de série de fabricação do ECF C 021 - O O
04 ECF_CX Número do caixa atribuído ao ECF N 003 - O O
05 NUM_DOC Número do documento fiscal N 009 O O
06 DT_DOC Data da emissão do documento fiscal N 008* - O O
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C114]
Campo 02 (COD_MOD) - Valores válidos: [02, 2D, 2E] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 04 (ECF_CX) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 05 (NUM_DOC) - Preenchimento: número do Contador de Ordem de Operação (COO). Validação: o valor
informado no campo deve ser maior que “0” (zero).
Campo 06 (DT_DOC) - Preenchimento: data da emissão do cupom no formato “ddmmaaaa”. Validação: o valor informado
neste campo deve ser menor ou igual ao valor do campo DT_DOC do registro C100.
----
# REGISTRO C115: LOCAL DA COLETA E/OU ENTREGA (CÓDIGO 01, 1B E 04)
Este registro tem por objetivo informar o local de coleta, quando este for diferente do endereço do emitente do
documento fiscal e/ou local de entrega, quando este for diferente do endereço do destinatário do documento fiscal, além de
informar a modalidade de transporte utilizada. As informações prestadas referem-se a transporte próprio ou de terceiros.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C115" C 004 - Não O
Indicador do tipo de transporte: Apresentar O
0 – Rodoviário;
1 – Ferroviário;
2 – Rodo-Ferroviário;
02 IND_CARGA N 001* -
3 – Aquaviário;
4 – Dutoviário;
5 – Aéreo;
9 – Outros.
Número do CNPJ do contribuinte do local OC
03 CNPJ_COL N 014* -
de coleta
Inscrição Estadual do contribuinte do local OC
04 IE_COL C 014 -
de coleta
CPF_COL CPF do contribuinte do local de coleta das OC
05 N 011* -
mercadorias
06 COD_MUN_COL Código do Município do local de coleta N 007* - OC
Número do CNPJ do contribuinte do local OC
07 CNPJ_ENTG N 014* -
de entrega
Inscrição Estadual do contribuinte do local OC
08 IE_ENTG C 014 -
de entrega
09 CPF_ENTG CPF do contribuinte do local de entrega N 011* - OC
COD_MUN_ENT OC
10 Código do Município do local de entrega N 007* -
G
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C115]
Campo 02 (IND_CARGA) - Valores Válidos: [0, 1, 2, 3, 4, 5, 9]
Campo 03 (CNPJ_COL) – Preenchimento: não utilizar os caracteres especiais de formatação, tais como: “.”, “/”, “-”.
Validação: é conferido se o dígito verificador é válido.
Somente um dos campos CPF_COL ou CNPJ_COL deve ser preenchido.
Campo 04 (IE_COL) - Preenchimento: não utilizar os caracteres especiais de formatação, tais como: “.”, “/”, “-”.
Validação: é conferido o dígito verificador da Inscrição Estadual, considerando-se a UF obtida no código de município
informado no campo COD_MUN_COL.
Campo 05 (CPF_COL) - Preenchimento: não utilizar os caracteres especiais de formatação, tais como: “.”, “/”, “-”.
Validação: é conferido se o dígito verificador é válido.
Campo 06 (COD_MUN_COL) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos. Mesmo não havendo dados de coleta, este campo deve ser preenchido.
Campo 07 (CNPJ_ENTG) - Preenchimento: não utilizar os caracteres especiais de formatação, tais como: “.”, “/”, “-”.
Validação: é conferido se o dígito verificador é válido.
Somente um dos campos CPF_ENTG ou CNPJ_ENTG deve ser preenchido.
Campo 08 (IE_ENTG) - Preenchimento: não utilizar os caracteres especiais de formatação, tais como: “.”, “/”, “-”.
Validação: é conferido o dígito verificador da inscrição estadual, considerando-se a UF obtida no código de município
informado no campo COD_MUN_ENTG.
Campo 09 (CPF_ENTG) - Preenchimento: não utilizar os caracteres especiais de formatação, tais como: “.”, “/”, “-”.
Validação: é conferido se o dígito verificador é válido.
Campo 10 (COD_MUN_ENTG) – Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE,
possuindo 7 dígitos. Mesmo não havendo dados de entrega, este campo deve ser preenchido.
----
# REGISTRO C116: CUPOM FISCAL ELETRÔNICO REFERENCIADO
Este registro será utilizado para informar, detalhadamente, nas operações de saídas, cupons fiscais eletrônicos
que tenham sido mencionados nas informações complementares do documento que está sendo escriturado no registro C100.
Nas operações de entradas no registro C100, somente informar quando o emitente do cupom fiscal for o próprio informante do
arquivo. Este registro está relacionado ao documento fiscal informado no registro C800 ou C860.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal, dois ou mais registros
com a mesma combinação de conteúdo nos campos NR_SAT, NUM_CFE e DT_DOC.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C116" C 004 - O O
02 COD_MOD Código do modelo do documento fiscal, conforme a C 002 -
O O
Tabela 4.1.1
03 NR_SAT Número de Série do equipamento SAT N 009 - O O
04 CHV_CFE Chave do Cupom Fiscal Eletrônico N 044 - O O
05 NUM_CFE Número do cupom fiscal eletrônico N 006 - O O
06 DT_DOC Data da emissão do documento fiscal N 008 - O O
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) – Valor Válido: [C116]
Campo 02 (COD_MOD) – Preenchimento: deve corresponder ao código Cupom Fiscal Eletrônico (Valor Válido: [59])- –
Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 04 (CHV_CFE) – Validação: é conferido o dígito verificador (DV) da chave do CF-e. Para confirmação inequívoca
de que a chave da NF-e corresponde aos dados informados no documento, será comparado o CNPJ existente na CHV_CFE
com o campo CNPJ do registro 0000, que corresponde ao CNPJ do informante do arquivo. Serão verificados a consistência da
informação do campo NUM_CFE e o número do documento contido na chave do CF-e, bem como comparado se a informação
do AAMM de emissão contido na chave do CFE corresponde ao ano e mês da data de emissão do CF-e. Será também comparada
a UF codificada na chave do CF-e com o campo UF informado no registro 0000.
Campo 06 (DT_DOC) – Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se
quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
----
# REGISTRO C120: COMPLEMENTO DE DOCUMENTO - OPERAÇÕES DE IMPORTAÇÃO
(CÓDIGOS 01 e 55)
Este registro tem por objetivo informar detalhes das operações de importação, que estejam sendo documentadas pela
nota fiscal escriturada no registro C100, quando o campo IND_OPER for igual a “0” (zero), indicando operação de entrada.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o
mesmo conteúdo no campo NUM_DOC__IMP e NUM_ACDRAW.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C120" C 004 - O Não apresentar
02 COD_DOC_IMP Documento de importação: C 001* - O
0 – Declaração de Importação;
1 – Declaração Simplificada de Importação.
03 NUM_DOC_IMP Número do documento de Importação. C 015 - O
04 PIS_IMP Valor pago de PIS na importação N - 02 OC
05 COFINS IMP Valor pago de COFINS na importação N 02 OC
06 NUM_ACDRAW Número do Ato Concessório do regime C 020 - OC
Drawback
Observações: Alteração do tamanho do campo 06 – NUM_ACDRAW de 11 para 20 caracteres a partir de 01/01/2011.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C120]
Campo 02 (COD_DOC_IMP) - Valores válidos: [0, 1]
Campo 04 (PIS_IMP) – Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 05 (COFINS_IMP) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração
do registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C130: ISSQN, IRRF E PREVIDÊNCIA SOCIAL
Este registro tem por objetivo informar dados da prestação de serviços sob não-incidência ou não tributados pelo ICMS
e ainda detalhes sobre a retenção de Imposto de Renda Retido na Fonte (IRRF) e de contribuições previdenciárias.
Essas três situações possuem características próprias e tratamentos específicos na legislação, não guardando nenhuma
relação entre elas.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C130" C 004 - Não O
02 VL_SERV_NT Valor dos serviços sob não-incidência ou N - 02 apresentar O
não-tributados pelo ICMS
03 VL_BC_ISSQN Valor da base de cálculo do ISSQN N - 02 O
04 VL_ISSQN Valor do ISSQN N - 02 OC
05 VL_BC_IRRF Valor da base de cálculo do Imposto de N - 02 OC
Renda Retido na Fonte
06 VL_ IRRF Valor do Imposto de Renda - Retido na N - 02 OC
Fonte
07 VL_BC_PREV Valor da base de cálculo de retenção da N - 02 OC
Previdência Social
08 VL_ PREV Valor destacado para retenção da N - 02 OC
Previdência Social
Observações:
Nível hierárquico - 3
Ocorrência – 1:1
Campo 01 (REG) - Valor Válido: [C130]
----
# REGISTRO C140: FATURA (CÓDIGO 01)
Este registro tem por objetivo informar dados da fatura comercial, sempre que a aquisição ou venda de mercadorias
for a prazo, por meio de notas fiscais modelo 1 ou 1A. Devem ser consideradas as informações quando da emissão do
documento fiscal, incluindo a parcela paga no ato da operação, se for o caso.
Nos casos onde uma única fatura diz respeito a diversas notas fiscais, para cada nota apresentada no C100, a fatura
deve aqui ser informada, sempre com o seu valor original, sem nenhum rateio.
Havendo mais de um tipo de título, informar o campo IND_TIT com o código ‘99’ (Outros). No campo DESC_TIT
identificar cada um dos títulos, com números e valores. No campo VL_TIT informar o valor total da fatura.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C140" C 004 - O O
02 IND_EMIT Indicador do emitente do título: C 001* - O O
0 - Emissão própria;
1 - Terceiros
03 IND_TIT Indicador do tipo de título de crédito: C 002* - O O
00 - Duplicata;
01 - Cheque;
02 - Promissória;
03 - Recibo;
99 - Outros (descrever)
04 DESC_TIT Descrição complementar do título de C - - OC OC
crédito
05 NUM_TIT Número ou código identificador do título C - - O O
de crédito
06 QTD_PARC Quantidade de parcelas a receber/pagar N 002 - O O
07 VL_TIT Valor total dos títulos de créditos N - 02 O O
Observações:
Nível hierárquico - 3
Ocorrência – 1:1
Campo 01 (REG) - Valor Válido: [C140]
Campo 02 (IND_EMIT) - Valores válidos: [0, 1]
Campo 03 (IND_TIT) - Valores válidos: [00, 01, 02, 03, 99]
Preenchimento: informar o tipo de título de crédito e utilizar o indicador “99” (Outros) quando houver diversos tipos de títulos,
inclusive documentos eletrônicos, descrevendo os tipos no campo seguinte.
Campo 06 (QTD_PARC) - Validação: o valor neste campo corresponde ao total de ocorrências dos registros C141.
Campo 07 (VL_TIT) - Preenchimento: o valor neste campo corresponde ao valor original do título, mesmo nos casos onde
uma única fatura diz respeito a diversas notas fiscais.
----
# REGISTRO C141: VENCIMENTO DA FATURA (CÓDIGO 01)
Este registro deve ser apresentado, obrigatoriamente, sempre que for informado o registro C140, devendo ser
discriminados o valor e a data de vencimento de cada uma das parcelas.
Validação do Registro: Não podem ser informados dois ou mais registros com o mesmo conteúdo para o campo
NUM_PARC.
Nº Campo Descrição Tipo Tam Dec Entr. Saída
01 REG Texto fixo contendo "C141" C 004 - O O
02 NUM_PARC Número da parcela a receber/pagar N 002 - O O
03 DT_VCTO Data de vencimento da parcela N 008* - O O
04 VL_PARC Valor da parcela a receber/pagar N - 02 O O
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor válido: [C141]
Campo 03 (DT_VCTO) - Preenchimento: informar a data de vencimento da parcela, no formato “ddmmaaaa”.
Validação: o valor neste campo deve ser maior ou igual ao valor do campo DT_DOC do registro C100.
----
# REGISTRO C160: VOLUMES TRANSPORTADOS (CÓDIGO 01 E 04) - EXCETO
COMBUSTÍVEIS.
Este registro tem por objetivo informar detalhes dos volumes, do transportador e do veículo empregado no transporte nas operações
de saídas.
Nº Campo Descrição Tipo Tam Dec Entr. Saída
01 REG Texto fixo contendo "C160" C 004 - Não O
02 COD_PART Código do participante (campo 02 do Registro C 060 - apresentar OC
0150):
- transportador, se houver
03 VEIC_ID Placa de identificação do veículo automotor C 007 - OC
04 QTD_VOL Quantidade de volumes transportados N - - O
05 PESO_BRT Peso bruto dos volumes transportados (em kg) N - 02 O
06 PESO_LIQ Peso líquido dos volumes transportados (em kg) N - 02 O
07 UF_ID Sigla da UF da placa do veículo C 002 - OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C160]
Campo 02 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150. Quando o
transportador for o próprio emitente do documento, este campo não deve ser preenchido.
Campo 03 (VEIC_ID) - Preenchimento: informar a placa do veículo transportador, quando disponível nos sistemas de
informação do contribuinte. Este campo se refere à placa do veículo tracionado (com cadastro no RENAVAM), quando se
tratar de reboque ou semi-reboque deste tipo de veículo. Quando houver mais de um veículo tracionado, a placa deve ser
indicada no registro C110. Na hipótese de veículo não rodoviário, não é necessário preencher.
----
# REGISTRO C165: OPERAÇÕES COM COMBUSTÍVEIS (CÓDIGO 01).
Este registro deve ser apresentado pelas empresas do segmento de combustíveis (distribuidoras, refinarias,
revendedoras) em operações de saída. Postos de combustíveis não devem apresentar este registro.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com a
mesma combinação de conteúdo nos campos COD_PART e VEIC_ID.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C165” C 004 - Não O
COD_PART Código do participante (campo 02 do C 060 - apresentar OC
02 Registro 0150):
- transportador, se houver
03 VEIC_ID Placa de identificação do veículo C 007 - O
Código da autorização fornecido pela OC
04 COD_AUT C - -
SEFAZ (combustíveis)
05 NR_PASSE Número do Passe Fiscal C - - OC
06 HORA Hora da saída das mercadorias N 006* - O
Temperatura em graus Celsius utilizada para OC
07 TEMPER N - 01
quantificação do volume de combustível
08 QTD_VOL Quantidade de volumes transportados N - - O
PESO_BRT Peso bruto dos volumes transportados (em N - 02 O
09
kg)
PESO_LIQ Peso líquido dos volumes transportados (em N - 02 O
10
kg)
11 NOM_MOT Nome do motorista C 060 - OC
12 CPF CPF do motorista N 011* - OC
13 UF_ID Sigla da UF da placa do veículo C 002 - OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C165]
Campo 02 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 06 (HORA) - Preenchimento: informar, conforme o padrão “hhmmss”, excluindo-se quaisquer caracteres de
separação, tais como: ".", ":", "-", " ", etc.
Campo 12 (CPF) - Preenchimento: não utilizar os caracteres especiais de formatação, tais como: “.”, “/”, “-”.
Validação: se preenchido, é conferido se o dígito verificador é válido.
----
# REGISTRO C170: ITENS DO DOCUMENTO (CÓDIGO 01, 1B, 04 e 55).
Registro obrigatório para discriminar os itens da nota fiscal (mercadorias e/ou serviços constantes em notas
conjugadas), inclusive em operações de entrada de mercadorias acompanhadas de Nota Fiscal Eletrônica (NF-e) de emissão de
terceiros.
Conforme item 2.4.2.2.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações, o termo “item”
é aplicado às operações fiscais que envolvam mercadorias, serviços, produtos ou quaisquer outros itens concernentes às
transações fiscais suportadas pelo documento, como, por exemplo, nota fiscal complementar, nota fiscal de ressarcimento,
transferências de créditos e outros casos.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal dois ou mais registros com o
mesmo conteúdo no campo NUM_ITEM.
IMPORTANTE: para documentos de entrada, os campos de valor de imposto, base de cálculo e alíquota só devem ser
informados se o adquirente tiver direito à apropriação do crédito (enfoque do declarante).
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C170" C 004 - O O
02 NUM_ITEM Número sequencial do item no documento fiscal N 003 - O O
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O O
04 DESCR_COMPL Descrição complementar do item como adotado C - - OC OC
no documento fiscal
05 QTD Quantidade do item N - 05 O O
06 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O O
07 VL_ITEM Valor total do item (mercadorias ou serviços) N - 02 O O
08 VL_DESC Valor do desconto comercial N - 02 OC OC
09 IND_MOV Movimentação física do ITEM/PRODUTO: C 001* - O O
0. SIM
1. NÃO
10 CST_ICMS Código da Situação Tributária referente ao N 003* - O O
ICMS, conforme a Tabela indicada no item 4.3.1
11 CFOP Código Fiscal de Operação e Prestação N 004* - O O
12 COD_NAT Código da natureza da operação (campo 02 do C 010 - OC OC
Registro 0400)
13 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 OC OC
14 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
15 VL_ICMS Valor do ICMS creditado/debitado N - 02 OC OC
16 VL_BC_ICMS_ST Valor da base de cálculo referente à substituição N - 02 OC OC
tributária
17 ALIQ_ST Alíquota do ICMS da substituição tributária na N - 02 OC OC
unidade da federação de destino
18 VL_ICMS_ST Valor do ICMS referente à substituição tributária N - 02 OC OC
19 IND_APUR Indicador de período de apuração do IPI: C 001* - OC OC
0 - Mensal;
1 - Decendial
20 CST_IPI Código da Situação Tributária referente ao IPI, C 002* - OC OC
conforme a Tabela indicada no item 4.3.2.
21 COD_ENQ Código de enquadramento legal do IPI, C 003* - OC OC
conforme tabela indicada no item 4.5.3.
22 VL_BC_IPI Valor da base de cálculo do IPI N - 02 OC OC
23 ALIQ_IPI Alíquota do IPI N 006 02 OC OC
24 VL_IPI Valor do IPI creditado/debitado N - 02 OC OC
25 CST_PIS Código da Situação Tributária referente ao PIS. N 002* - OC OC
26 VL_BC_PIS Valor da base de cálculo do PIS N - 02 OC OC
27 ALIQ_PIS Alíquota do PIS (em percentual) N 008 04 OC OC
28 QUANT_BC_PIS Quantidade – Base de cálculo PIS N - 03 OC OC
29 ALIQ_PIS Alíquota do PIS (em reais) N - 04 OC OC
30 VL_PIS Valor do PIS N - 02 OC OC
31 CST_COFINS Código da Situação Tributária referente ao N 002* - OC OC
COFINS.
32 VL_BC_COFINS Valor da base de cálculo da COFINS N - 02 OC OC
33 ALIQ_COFINS Alíquota do COFINS (em percentual) N 008 04 OC OC
34 QUANT_BC_COF Quantidade – Base de cálculo COFINS N - 03 OC OC
INS
35 ALIQ_COFINS Alíquota da COFINS (em reais) N - 04 OC OC
36 VL_COFINS Valor da COFINS N - 02 OC OC
37 COD_CTA Código da conta analítica contábil C - - OC OC
debitada/creditada
38 VL_ABAT_NT Valor do abatimento não tributado e não N - 02 OC OC
comercial
Observações:
Nível hierárquico - 3
Ocorrência - 1:N (um ou vários por registro C100)
Campo 01 (REG) - Valor Válido: [C170]
Campo 02 (NUM_ITEM) – Preenchimento: preencher com o mesmo número do item utilizado no documento fiscal.
Campo 03 (COD_ITEM) - Validação: o valor informado neste campo deve existir no registro 0200. Atentar para a premissa
de que a informação deve ser prestada pela ótica do contribuinte, ou seja, nas operações de entradas de mercadorias, os códigos
informados devem ser os definidos pelo próprio informante e não aqueles constantes do documento fiscal.
Campo 05 (QTD) - Preenchimento: informar a quantidade do item constante no documento fiscal, tanto na entrada como na
saída, expressa na unidade de medida informada no campo UNID.
Validação: o valor informado no campo deve ser maior que “0” (zero), exceto para o COD_SIT igual a 6 (complementar) ou
7 (complementar extemporâneo), para os quais o valor deve ser maior ou igual a “0” (zero).
Campo 06 (UNID) - Preenchimento: informar a unidade de medida de comercialização do item utilizada no documento fiscal,
tanto na entrada como na saída. Caso a unidade de medida do documento fiscal seja diferente da unidade de medida de controle
de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de conversão entre as unidades de
medida.
Validação:
a) o valor informado neste campo deve existir no registro 0190.
b) Caso a unidade de medida do documento fiscal seja diferente da unidade de medida de controle de estoque informada no
Registro 0200, o valor informado deve existir no registro 0220 para o código do item (Campo 03 - COD_ITEM desse registro)
com a correspondente conversão, exceto se o campo 07 - TIPO_ITEM do registro 0200 for igual a 07 (Material de Uso e
Consumo).
Campo 07 (VL_ITEM) - Preenchimento: informar o valor total do item/produto (via de regra, o valor das mercadorias é
equivalente à multiplicação da quantidade pelo preço unitário) ou do serviço.
Validação: a soma de valores dos registros C170 deve ser igual ao valor informado no campo VL_MERC do registro C100.
Campo 08 (VL_DESC) - Preenchimento: informar o valor do desconto comercial, ou seja, os descontos incondicionais
constantes do próprio documento fiscal.
Campo 09 (IND_MOV) - Valores válidos: [0, 1]
Preenchimento: indicar a movimentação física do item ou produto. Será informado o código “1” em todas as situações em que
não houver movimentação de mercadorias, por exemplo: notas fiscais complementares, simples faturamento, remessas
simbólicas, etc.
Campo 10 (CST_ICMS) – Preenchimento: o campo deverá ser preenchido com o código da Situação Tributária sob o enfoque
do declarante. Exemplo 1 - Aquisição de mercadorias tributadas para uso e consumo - informar código “90” da tabela B.
Exemplo 2 - Aquisição de mercadorias para comercialização com ICMS retido por ST - informar código “60” da tabela B. Nas
operações de aquisição de produtos de empresas do Simples Nacional, deverá ser indicado o CST_ICMS definido pelo
Convênio S/N de 1970.
Para os estabelecimentos informantes da EFD-ICMS/IPI, optantes pelo Simples Nacional e que recolham o ICMS por este
regime, na escrituração de documentos fiscais de saída deverá ser utilizada a Tabela B do CSOSN e na escrituração dos
documentos fiscais de entrada, informar o CST_ICMS sob o enfoque do declarante.
Até 30-06-2012, nas operações de entradas (documentos de terceiros), poderá ser informado o CST que constar no documento
fiscal de aquisição dos produtos.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, constante do Artigo
5º do Convênio SN/70 e/ou Ajuste SINIEF nº 03/2010.
Outras regras a serem executadas somente nas operações de saídas:
ICMS Normal:
a) se os dois últimos dígitos deste campo forem iguais a 30, 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” = (zero);
b) se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
c) se os dois últimos dígitos deste campo forem iguais a 20, 51 ou 90, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores ou iguais a “0” (zero). ICMS ST:
a) se os dois últimos caracteres deste campo forem 10, 30 ou 70, os valores dos campos VL_BC_ST, ALIQ_ST e VL_ICMS_ST deverão ser maiores ou iguais a “0” (zero).
b) se os dois últimos caracteres deste campo forem diferentes de 10, 30 ou 70, os valores dos campos VL_BC_ST,
ALIQ_ST e VL_ICMS_ST deverão ser iguais a “0” (zero).
Campo 11 (CFOP) - Preenchimento: nas operações de entradas, devem ser registrados os códigos de operação que
correspondem ao tratamento tributário relativo à destinação do item.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01.
Se o campo IND_OPER do registro C100 for igual a “0” (zero), então o primeiro caractere do CFOP deve ser igual a 1, 2 ou
3. Se campo IND_OPER do registro C100 for igual a “1” (um), então o primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
O primeiro caractere deve ser o mesmo para todos os itens de um documento fiscal.
Campo 12 (COD_NAT) - Validação: o valor informado no campo deve existir no registro 0400 -Tabela de Natureza da
Operação.
Campo 14 (ALIQ_ICMS) - Validação: nas operações de saídas, se os dois últimos caracteres do CST_ICMS forem 00, 10,
20 ou 70, o campo ALIQ_ICMS deve ser maior que “0” (zero).
Campo 19 (IND_APUR) - Valores válidos: [0, 1]
Preenchimento: informar o período de apuração do IPI (0-Mensal ou 1-Decendial). Este campo servirá para identificar quais
documentos serão considerados em cada apuração do IPI para períodos distintos no mesmo mês, nos casos em que um mesmo
contribuinte esteja submetido simultaneamente a mais de uma apuração.
Campo 20 (CST_IPI) - Preenchimento: O campo deverá ser preenchido somente se o declarante for contribuinte do IPI. A
tabela do CST_IPI consta publicada na Instrução Normativa RFB nº 932, de 14/04/2009. A partir de 01 de abril de 2010, IN
RFB nº 1009, de 10 de fevereiro de 2010.
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
Campo 21 (COD_ENQ) - Não preencher.
Campo 22 (VL_BC_IPI) - Preenchimento: O frete e despesas acessórias, quando destacados no documento fiscal, devem ser
rateados por item de mercadoria e compõem a base de cálculo do IPI.
Campo 23 (ALIQ_IPI) - Preenchimento: preencher com a alíquota do IPI estabelecida na TIPI e NÃO preencher, quando a
forma de tributação do IPI for fixada em reais e calculada por unidade ou por determinada quantidade de produto.
Campo 24 (VL_IPI) - Preenchimento: Deverão ser destacados e informados neste campo todos os débitos e/ou créditos de
IPI da operação. Esses valores serão totalizados para o registro C190, na combinação de CST_ICMS + CFOP +
ALIQ_ICMS, bem como, comparados com o total informado no registro C100.
Campo 25 (CST_PIS) - Validação: o valor deve constar da Tabela de Código da Situação Tributária referente ao PIS, constante
da Instrução Normativa RFB nº 932, de 14/04/2009.
Obs.: Nos casos de regime cumulativo na apuração do PIS ou COFINS os campos 25 a 36 podem ser informados como campos
de conteúdo VAZIO, ou seja, “||”.Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração
do registro 0000 estão dispensados do preenchimento dos campos 25 a 36. Apresentar conteúdo VAZIO “||”.
Código Descrição
01 Operação Tributável (base de cálculo = valor da operação alíquota normal (cumulativo/não cumulativo).
02 Operação Tributável (base de cálculo = valor da operação (alíquota diferenciada).
03 Operação Tributável (base de cálculo = quantidade vendida x alíquota por unidade de produto).
04 Operação Tributável (tributação monofásica (alíquota zero).
06 Operação Tributável (alíquota zero).
07 Operação Isenta da Contribuição.
08 Operação Sem Incidência da Contribuição.
09 Operação com Suspensão da Contribuição.
99 Outras Operações.
A partir de 01 de abril de 2010, Instrução Normativa RFB nº 1009, de 10 de fevereiro de 2010.
Código Descrição
01 Operação Tributável com Alíquota Básica
02 Operação Tributável com Alíquota Diferenciada
03 Operação Tributável com Alíquota por Unidade de Medida de Produto
04 Operação Tributável Monofásica - Revenda a Alíquota Zero
05 Operação Tributável por Substituição Tributária
06 Operação Tributável a Alíquota Zero
07 Operação Isenta da Contribuição
08 Operação sem Incidência da Contribuição
09 Operação com Suspensão da Contribuição
49 Outras Operações de Saída
50 Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno
51 Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno
52 Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação
53 Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno
54 Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação
55 Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação
56 Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de
Exportação
60 Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno
61 Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado
Interno
62 Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação
63 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno
64 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação
65 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de
Exportação
66 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno,
e de Exportação
67 Crédito Presumido - Outras Operações
70 Operação de Aquisição sem Direito a Crédito
71 Operação de Aquisição com Isenção
72 Operação de Aquisição com Suspensão
73 Operação de Aquisição a Alíquota Zero
74 Operação de Aquisição sem Incidência da Contribuição
75 Operação de Aquisição por Substituição Tributária
98 Outras Operações de Entrada
99 Outras Operações
Campo 28 (QUANT_BC_PIS) - Preenchimento: Neste campo deverá ser informada a quantidade de produtos vendidos na
unidade de tributação prevista na legislação.
De acordo com a legislação em vigor em fevereiro de 2009, a apuração das contribuições sociais, com base de cálculo
determinada sobre a quantidade de produtos vendidos, alcança:
1. As receitas decorrentes da venda e da produção sob encomenda de embalagens para bebidas (refrigerantes,
cervejas e águas, classificadas nas posições 22.01, 22.02 e 22.03 da TIPI) pelas pessoas jurídicas industriais ou comerciais e
pelos importadores, conforme disposto no art. 51 da Lei nº 10.833/03;
2. As receitas decorrentes da venda de bebidas frias (refrigerantes, cervejas e águas, classificadas nas posições 22.01,
22.02 e 22.03 da TIPI) e preparações compostas classificadas no código 2106.90.10, ex 02, da TIPI, pelas pessoas jurídicas
industriais e pelos importadores, conforme disposto no art. 52 da Lei nº 10.833/03 (fatos geradores até 31.12.2008) e pela Lei
nº 10.865/04;
3. As receitas decorrentes da venda de bebidas frias (refrigerantes, cervejas e águas, classificadas nas posições 22.01,
22.02 e 22.03 da TIPI) e preparações compostas classificadas no código 2106.90.10, ex 02, da TIPI, pelas pessoas jurídicas
industriais e pelos importadores, conforme disposto nos arts. 58-A a 58-U2 da Lei nº 10.833/03, incluídos pela lei nº 11.727
(fatos geradores a partir de 01.01.2009) e pela Lei nº 10.865/04;
4. As receitas decorrentes da venda de gasolinas e suas correntes, exceto gasolina de aviação, de óleo diesel e suas
correntes, de gás liquefeito de petróleo - GLP, derivado de petróleo e de gás natura e de querosene de aviação, pelas pessoas
jurídicas industriais e pelos importadores, conforme disposto no art. 23 da Lei nº 10.865/04 e pela Lei nº 10.865/04.
Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do registro 0000 estão
dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 31 (CST_COFINS) - Validação: o valor deve constar da Tabela de Código da Situação Tributária referente ao COFINS,
constante da Instrução Normativa RFB nº 932, de 14/04/2009.
Código Descrição
01 Operação Tributável (base de cálculo = valor da operação alíquota normal (cumulativo/não cumulativo).
02 Operação Tributável (base de cálculo = valor da operação (alíquota diferenciada).
03 Operação Tributável (base de cálculo = quantidade vendida x alíquota por unidade de produto).
04 Operação Tributável (tributação monofásica (alíquota zero).
06 Operação Tributável (alíquota zero).
07 Operação Isenta da Contribuição.
08 Operação Sem Incidência da Contribuição.
09 Operação com Suspensão da Contribuição.
99 Outras Operações.
A partir de 01 de abril de 2010, Instrução Normativa RFB nº 1009, de 10 de fevereiro de 2010.
Código Descrição
01 Operação Tributável com Alíquota Básica
02 Operação Tributável com Alíquota Diferenciada
03 Operação Tributável com Alíquota por Unidade de Medida de Produto
04 Operação Tributável Monofásica - Revenda a Alíquota Zero
05 Operação Tributável por Substituição Tributária
06 Operação Tributável a Alíquota Zero
07 Operação Isenta da Contribuição
08 Operação sem Incidência da Contribuição
09 Operação com Suspensão da Contribuição
49 Outras Operações de Saída
50 Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno
51 Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno
52 Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação
53 Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno
54 Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação
55 Operação com Direito a Crédito - Vinculada a Receitas Não Tributadas no Mercado Interno e de Exportação
56 Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e de
Exportação
60 Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno
61 Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno
62 Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação
63 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno
64 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação
65 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação
66 Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e
de Exportação
67 Crédito Presumido - Outras Operações
70 Operação de Aquisição sem Direito a Crédito
71 Operação de Aquisição com Isenção
72 Operação de Aquisição com Suspensão
73 Operação de Aquisição a Alíquota Zero
74 Operação de Aquisição sem Incidência da Contribuição
75 Operação de Aquisição por Substituição Tributária
98 Outras Operações de Entrada
99 Outras Operações
***Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do registro 0000 estão dispensados do preenchimento deste campo. Ou seja, deverá ser apresentados com conteúdo VAZIO “||”.
Campo 34 (QUANT_BC_COFINS) - Preenchimento: Idem campo 28.
Campo 37 (COD_CTA) - Preenchimento: informar o Código da Conta Analítica. Exemplos: estoques, receitas, despesas, ativos. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
----
# REGISTRO C171: ARMAZENAMENTO DE COMBUSTÍVEIS (código 01, 55).
Este registro deve ser apresentado pelas empresas do comércio varejista de combustíveis, somente nas operações de
entrada, para informar o volume recebido (em litros), por item do documento fiscal, conforme Livro de Movimentação de
Combustíveis (LMC), Ajuste SINIEF 01/92.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o
mesmo conteúdo no campo NUM_TANQUE.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C171" C 004 - O não apresentar
02 NUM_TANQUE Tanque onde foi armazenado o combustível C 003 - O
03 QTDE Quantidade ou volume armazenado N - 03 O
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C171]
Campo 03 (QTDE) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
# REGISTRO C172: OPERAÇÕES COM ISSQN (CÓDIGO 01)
Este registro tem por objetivo informar dados da prestação de serviços.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo “C172” C 004 - Não O
02 VL_BC_ISSQN Valor da base de cálculo do ISSQN N - 02 apresentar O
03 ALIQ_ISSQN Alíquota do ISSQN N 006 02 O
04 VL_ISSQN Valor do ISSQN N - 02 O
Observações:
Nível hierárquico - 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C172]
----
# REGISTRO C173: OPERAÇÕES COM MEDICAMENTOS (CÓDIGO 01 e 55)
Este registro deve ser apresentado pelas empresas do segmento farmacêutico (distribuidoras, indústrias, revendedoras
e importadoras), exceto comércio varejista. A obrigatoriedade deriva do §26 do art. 19 do Convênio S/N de 1970:
“Nova redação dada ao § 26 pelo Ajuste 07/04, efeitos a partir de 01.01.05.
§ 26. A Nota Fiscal emitida por fabricante, importador ou distribuidor, relativamente à saída para
estabelecimento atacadista ou varejista, dos produtos classificados nos códigos 3002, 3003, 3004 e
3006.60 da Nomenclatura Brasileira de Mercadoria/Sistema Harmonizado – NBM/SH, exceto se
relativa às operações com produtos veterinários, homeopáticos ou amostras grátis, deverá conter, na
descrição prevista na alínea “b” do inciso IV deste artigo, a indicação do valor correspondente ao
preço constante da tabela, sugerido pelo órgão competente para venda a consumidor e, na falta deste
preço, o valor correspondente ao preço máximo de venda a consumidor sugerido ao público pelo
estabelecimento industrial.”
Em caso de NF-e emitida por terceiros, a informação é obrigatória, desde que não seja destinado a comércio varejista.
Validação do Registro: Não podem ser informados, para um mesmo item do documento fiscal (Registro C170), dois
ou mais registros com a mesma combinação de valores dos campos: LOTE_MED e QTD_ITEM.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C173" C 004 - O O
02 LOTE_MED Número do lote de fabricação do C - - O O
medicamento
03 QTD_ITEM Quantidade de item por lote N - 003 O O
04 DT_FAB Data de fabricação do medicamento N 008* - O O
05 DT_VAL Data de expiração da validade do N 008* - O O
medicamento
06 IND_MED Indicador de tipo de referência da base de C 001* - O O
cálculo do ICMS (ST) do produto
farmacêutico:
0 - Base de cálculo referente ao preço
tabelado ou preço máximo sugerido;
1 - Base cálculo – Margem de valor
agregado;
2 - Base de cálculo referente à Lista
Negativa;
3 - Base de cálculo referente à Lista Positiva;
4 - Base de cálculo referente à Lista Neutra
07 TP_PROD Tipo de produto: C 1* - O O
0 - Similar;
1 - Genérico;
2 - Ético ou de marca;
08 VL_TAB_MAX Valor do preço tabelado ou valor do preço N - 02 O O
máximo
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C173]
Campo 04 (DT_FAB) - Preenchimento: informar a data de fabricação do medicamento no formato “ddmmaaaa”.
Campo 05 (DT_VAL) - Preenchimento: informar a data de expiração da validade do medicamento no formato “ddmmaaaa”.
Campo 06 (IND_MED) - Valores válidos: [0, 1, 2, 3, 4]
Campo 07 (TP_PROD) - Valores válidos: [0, 1, 2] O código 2 é utilizado quando o tipo de produto for medicamento de
referência.
Campo 08 (VL_TAB_MAX) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
# REGISTRO C174: OPERAÇÕES COM ARMAS DE FOGO (CÓDIGO 01)
Este registro deve ser apresentado pelas empresas que realizam operações com armas de fogo (indústria, comércio e
demais) e deve ser fornecido apenas para operações de saída.
Validação do Registro: Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o
mesmo valor do campo NUM_ARM.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C174" C 004 - Não O
02 IND_ARM Indicador do tipo da arma de fogo: C 001* - apresentar O
0 - Uso permitido;
1 - Uso restrito
03 NUM_ARM Numeração de série de fabricação da arma C - - O
04 DESCR_COMPL Descrição da arma, compreendendo: número do C - - O
cano, calibre, marca, capacidade de cartuchos,
tipo de funcionamento, quantidade de canos,
comprimento, tipo de alma, quantidade e sentido
das raias e demais elementos que permitam sua
perfeita identificação
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C174]
Campo 02 (IND_ARM) - Valores válidos: [0, 1]
----
# REGISTRO C175: OPERAÇÕES COM VEÍCULOS NOVOS (CÓDIGO 01 e 55)
Este registro deve ser apresentado pelas empresas do segmento automotivo (montadoras-capítulo 87 da NCM,
concessionárias e importadoras) para informar os itens relativos aos veículos novos. Deve ser informado nas operações de
entrada e saída (exceto pelos contribuintes emissores de NF-e), exceto quando se tratar de operações de exportação.
É considerada faturamento direto toda operação efetuada nos termos do Convênio ICMS nº 51/2000.
Validação do Registro: Não podem ser informados, para um mesmo registro C175, dois ou mais registros com o
mesmo valor do campo CHASSI_VEIC.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C175" C 004 - O O
02 IND_VEIC_OPER Indicador do tipo de operação com veículo: C 001* - O O
0 - Venda para concessionária;
1 - Faturamento direto;
2 - Venda direta;
3 - Venda da concessionária;
9 - Outros
03 CNPJ CNPJ da Concessionária N 014* - OC OC
04 UF Sigla da unidade da federação da C 002* - OC OC
Concessionária
05 CHASSI_VEIC Chassi do veículo C 017 - O O
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C175]
Campo 02 (IND_VEIC_OPER) - Valores válidos: [0, 1, 2, 3, 9]
Campo 03 (CNPJ) - Preenchimento: informar o CNPJ da concessionária envolvida na operação. Não utilizar os caracteres
especiais de formatação, tais como: “.”, “/”, “-”.
Validação: se o valor no campo IND_VEIC_OPER for igual a “1” (um), o campo CNPJ é obrigatório. O dígito verificador é
validado.
Campo 04 (UF) - Validação: o valor deve ser a sigla da UF da concessionária.
----
# REGISTRO C176: RESSARCIMENTO DE ICMS E FUNDO DE COMBATE À POBREZA (FCP)
EM OPERAÇÕES COM SUBSTITUIÇÃO TRIBUTÁRIA (CÓDIGO 01, 55)
Este registro deve ser informado quando da escrituração de documento fiscal, que acoberte operação que represente
desfazimento de substituição tributária realizada em operações anteriores.
O documento informado neste registro deverá ser diferente do documento informado no registro pai (C100), pois é o
documento referente à(s) última(s) aquisição(ões) da mercadoria e à retenção do imposto. Caso a legislação determine o cálculo
do ressarcimento com base na respectiva aquisição, não deverá ser informada a última aquisição no registro C176, mas aquela
indicada pela legislação.
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte,
inclusive sobre a apresentação dos campos CHAVE_NFE_RET; COD_PART_NFE_RET; SER_NFE_RET; NUM_NFE_RET;
ITEM_NFE_RET, COD_MOT_RES e VL_UNIT_RES_FCP_ST.
Este registro não se aplica aos contribuintes que utilizam o SCANC.
Nº Campo Descrição Tipo Tam Dec Entr. Saída
01 REG Texto fixo contendo "C176” C 004 - Não O
02 COD_MOD_ULT_E Código do modelo do documento fiscal C 002* - apresentar O
relativa a última entrada
03 NUM_DOC_ULT_E Número do documento fiscal relativa a N 009 - O
última entrada
04 SER_ULT_E Série do documento fiscal relativa a última C 003 - OC
entrada
05 DT_ULT_E Data relativa a última entrada da mercadoria N 008* - O
06 COD_PART_ULT_E Código do participante (do emitente do C 060 - O
documento relativa a última entrada)
07 QUANT_ULT_E Quantidade do item relativa a última entrada N - 03 O
08 VL_UNIT_ULT_E Valor unitário da mercadoria constante na N - 03 O
NF relativa a última entrada inclusive
despesas acessórias.
09 VL_UNIT_BC_ST Valor unitário da base de cálculo do imposto N - 03 O
pago por substituição.
10 CHAVE_NFE_ULT_ Número completo da chave da NFe relativo N 044* - OC
E à última entrada
11 NUM_ITEM_ULT_E Número sequencial do item na NF entrada N 003 - OC
que corresponde à mercadoria objeto de
pedido de ressarcimento
12 VL_UNIT_BC_ICMS Valor unitário da base de cálculo da N - 02 O
_ULT_E operação própria do remetente sob o regime
comum de tributação
13 ALIQ_ICMS_ULT_E Alíquota do ICMS aplicável à última entrada N - 02 O
da mercadoria
14 VL_UNIT_LIMITE_B Valor unitário da base de cálculo do ICMS N - 02 O
C_ICMS_ULT_E relativo à última entrada da mercadoria,
limitado ao valor da BC da retenção
(corresponde ao menor valor entre os
campos VL_UNIT_BC_ST e
VL_UNIT_BC_ICMS_ULT_E )
15 VL_UNIT_ICMS_UL Valor unitário do crédito de ICMS sobre N - 03 O
T_E operações próprias do remetente, relativo à
última entrada da mercadoria, decorrente da
quebra da ST – equivalente a multiplicação
entre os campos 13 e 14
16 ALIQ_ST_ULT_E Alíquota do ICMS ST relativa à última N - 02 OC
entrada da mercadoria
17 VL_UNIT_RES Valor unitário do ressarcimento (parcial ou N - 03 OC
completo) de ICMS decorrente da quebra da
ST
18 COD_RESP_RET Código que indica o responsável pela N 001* - OC
retenção do ICMS ST:
1 - Remetente Direto Regime Comum
2 - Remetente Indireto
3 - Próprio Declarante
4 – Remetente Direto Simples Nacional
19 COD_MOT_RES Código do motivo do ressarcimento: N 001* - OC
1 - Saída para outra UF;
2 -Saída amparada por isenção ou não
incidência;
3 - Perda ou deterioração;
4 - Furto ou roubo;
5 - Exportação;
6 - Venda interna para Simples Nacional
9 - Outros
20 CHAVE_NFE_RET Número completo da chave da NF-e emitida N 044* - OC
pelo substituto, na qual consta o valor do
ICMS ST retido
21 COD_PART_NFE_R Código do participante do emitente da NF-e C 060 - OC
ET em que houve a retenção do ICMS ST –
campo 02 do registro 0150
22 SER_NFE_RET Série da NF-e em que houve a retenção do C 003 - OC
ICMS ST
23 NUM_NFE_RET Número da NF-e em que houve a retenção N 009 - OC
do ICMS ST
24 ITEM_NFE_RET Número sequencial do item na NF-e em que N 003 - OC
houve a retenção do ICMS ST, que
corresponde à mercadoria objeto de pedido
de ressarcimento
25 COD_DA Código do modelo do documento de C 001* - OC
arrecadação:
0 – Documento estadual de arrecadação
1 – GNRE
26 NUM_DA Número do documento de arrecadação C - - OC
estadual, se houver
27 VL_UNIT_RES_FCP Valor unitário do ressarcimento (parcial ou N - 03 OC
_ST completo) de FCP decorrente da quebra da
ST
Observação: Os campos 10 a 26 são válidos a partir de 01/01/2017 e o campo 27 a partir de 01/01/2019. Estes campos serão
utilizados conforme critério da UF do domicílio do contribuinte.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C176]
Campo 02 (COD_MOD_ULT_E) - Valores Válidos: [01, 55]
Campo 03 (NUM_DOC_ULT_E) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 05 (DT_ULT_E) - Validação: o valor informado deve ser no formato “ddmmaaaa”. O valor informado no campo deve
ser menor ou igual ao valor no Campo10 (DT_DOC) do registro C100.
Campo 06 (COD_PART_ULT_E) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 07 (QUANT_ULT_E) –Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 08 (VL_UNIT_ULT_E) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 09 (VL_UNIT_BC_ST) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 10 (CHAVE_ULT_NFE) - Preenchimento: campo de preenchimento obrigatório para NF-e, COD_MOD igual a “55”.
Validação: é conferido o dígito verificador (DV) da chave da NF-e. Este campo é de preenchimento obrigatório para
COD_MOD igual a “55”. Para confirmação inequívoca de que a chave da NF-e corresponde aos dados informados do
documento, é comparado o CNPJ base existente na CHV_ULT_NFE com o campo CNPJ base do registro 0150, que
corresponde ao CNPJ do participante. São verificados a consistência da informação dos campos NUM_DOC e SER com o
número do documento e série contidos na chave da NF-e. É também comparada a UF codificada na chave da NF-e com o
campo UF informado no registro 0150.
Campo 11 (NUM_ITEM_ULT_E) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 12 (VL_UNIT_BC_ICMS_ULT_E) - Preenchimento: Se o emitente informado no campo COD_PART_ULT_E
deste registro for o substituto, informar o valor unitário destacado no documento fiscal a título de base de cálculo do ICMS.
Caso o substituto tributário seja contribuinte enquadrado no Simples Nacional, informar o valor unitário que seria atribuído à
base de cálculo do ICMS se a operação estivesse submetida ao regime comum de tributação; ou se o emitente informado no
campo COD_PART_ULT_E deste registro for o substituído, informar o valor unitário que seria atribuído à base de cálculo do
ICMS na operação própria do remetente, caso esta fosse submetida ao regime comum de tributação.
Campo 13 (ALIQ_ICMS_ULT_E) - Preenchimento: informar a alíquota do ICMS incidente na operação própria do
documento fiscal de entrada.
Campo 14 (VL_UNIT_LIMITE_BC_ICMS_ULT_E)
Preenchimento: Se o emitente informado no campo COD_PART_ULT_E deste registro for o substituto, informar o valor
unitário da base de cálculo destacada no documento fiscal; ou caso o substituto seja contribuinte enquadrado no Simples
Nacional, informar o valor unitário que seria atribuído à base de cálculo do ICMS se a operação estivesse submetida ao regime
comum de tributação;
Se o emitente informado no campo COD_PART_ULT_E deste registro for o substituído, informar o menor dos valores entre
o unitário informado no documento fiscal, a título de base de cálculo do ICMS ST (campo VL_UNIT_BC_ST), ou o unitário
da base de cálculo do ICMS que seria atribuído na operação própria do remetente, caso esta fosse submetida ao regime comum
de tributação (campo VL_UNIT_BC_ICMS_ULT_E).
Validação: deve corresponder ao menor valor entre os campos VL_UNIT_BC_ST e VL_UNIT_BC_ICMS_ULT_E, quando
o campo COD_RESP_RET for igual a “2 – Remetente Indireto”
Campo 15 (VL_UNIT_ICMS_ULT_E)
Preenchimento: Se o emitente informado no campo COD_PART_ULT_E deste registro for o substituto, informar o valor
unitário destacado no documento fiscal a título de ICMS, ou caso o substituto seja contribuinte enquadrado no Simples Nacional,
informar o valor unitário que seria destacado se a operação estivesse submetida ao regime comum de tributação;
Se o emitente informado no campo COD_PART_ULT_E deste registro for o substituído, informar o valor unitário do ICMS
que seria atribuído à operação própria do remetente caso estivesse submetida ao regime comum de tributação, limitado ao valor
unitário da retenção;
Validação: deve corresponder a multiplicação entre os campos ALIQ_ICMS_ULT_E e
VL_UNIT_LIMITE_BC_ICMS_ULT_E
Campo 16 (ALIQ_ST_ULT_E) - Preenchimento: informar alíquota interna do produto a ser aplicada na apuração do ICMS
ST.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 17 (VL_UNIT_RES) - Preenchimento: valor unitário destacado no documento fiscal de entrada a título de ICMS ST
ou valor unitário do ICMS ST informado a título de reembolso.
Validação: o valor informado no campo deve ser maior ou igual que “0” (zero), e deve corresponder a multiplicação entre os
campos VL_UNIT_BC_ST e ALIQ_ST_ULT_E, subtraindo, deste resultado, o campo VL_UNIT_ICMS_ULT_E.
Campo 18 (COD_RESP_RET)
Validação: Valores válidos: [1,2,3]
Campo 19 (COD_MOT_RES)
Validação: Valores válidos: [1, 2, 3, 4, 5, 6, 9]
Campo 20 (CHAVE_NFE_RET) - Preenchimento: informar a chave da NF-e em que houve a retenção do ICMS ST. Informar
este campo caso a informação seja diferente da relativa à última entrada informada no campo CHAVE_NFE_ULT_E deste
registro.
Validação: é conferido o dígito verificador (DV) da chave da NF-e. Este campo somente poderá ser apresentado quando
COD_RESP_RET=2.
Campo 21 (COD_PART_NFE_RET) - Preenchimento: o valor informado deve existir no campo COD_PART do registro
0150. Informar este campo caso a informação seja diferente da relativa à última entrada e o informante da EFD não teve acesso
ao número da chave solicitado no campo CHAVE_NFE_RET.
Validação: se informado o campo CHAVE_NFE_RET, este campo não deve ser preenchido. O valor informado deve existir
no campo COD_PART do registro 0150. Este campo somente poderá ser apresentado quando COD_RESP_RET=2.
Campo 22 (SER_NFE_RET) - Preenchimento: informar a série da NF-e. Informar este campo caso a informação seja diferente
da relativa à última entrada e o informante da EFD não teve acesso ao número da chave solicitado no campo
CHAVE_NFE_RET.
Validação: se informado o campo CHAVE_NFE_RET, este campo não deve ser preenchido. Se informado o campo
COD_PART_NFE_RET, este campo deve ser preenchido.
Campo 23 (NUM_NFE_RET) - Preenchimento: informar o número da NF-e. Informar este campo caso a informação seja
diferente da relativa à última entrada e o informante da EFD não teve acesso ao número da chave solicitado no campo
CHAVE_NFE_RET.
Validação: se informado o campo CHAVE_NFE_RET, este campo não deve ser preenchido. Se informado o campo
COD_PART_NFE_RET, este campo deve ser preenchido.
Campo 24 (ITEM_NFE_RET) - Preenchimento: informar o número do item da NF-e correspondente ao ressarcimento.
Informar este campo caso a informação seja diferente da relativa à última entrada.
Validação: se informado o campo CHAVE_NFE_RET ou o COD_PART_NFE_RET, este campo deve ser preenchido
Campo 25 (COD_DA) - Valores válidos: [0, 1]
Campo 27 (VL_UNIT_RES_FCP_ST) - Preenchimento: valor unitário destacado no documento fiscal de entrada a título de
FCP ST ou valor unitário do FCP ST informado a título de reembolso.
----
# REGISTRO C177: OPERAÇÕES COM PRODUTOS SUJEITOS A SELO DE CONTROLE IPI
(VÁLIDO ATÉ 31/12/2018)
Este registro tem por objetivo informar o tipo e a quantidade de selo de controle utilizada na saída dos produtos sujeitos
ao selo de controle, pelos fabricantes ou importadores desses produtos. Exemplo: bebidas quentes, cigarros e relógios. Se o
produto vendido está sujeito à selagem, o registro é obrigatório.
O registro não deve ser informado nas operações de aquisição de produtos.
Nº Campo Descrição Tipo Tam Dec Entr. Saída
01 REG Texto fixo contendo "C177" C 004 - Não O
02 COD_SELO_IPI Código do selo de controle do IPI, conforme C 006* - Apresentar O
Tabela 4.5.2
03 QT_SELO_IPI Quantidade de selo de controle do IPI aplicada N 012 - O
Observações:
Nível hierárquico - 4
Ocorrência – 1:1
Campo 01 (REG) - Valor Válido: [C177]
Campo 02 (COD_SELO_IPI) - Validação: o valor informado no campo deve constar da Tabela de Código do Selo de Controle
do IPI.
----
# REGISTRO C177: COMPLEMENTO DE ITEM - OUTRAS INFORMAÇÕES (código 01, 55) -
(VÁLIDO A PARTIR DE 01/01/2019)
Este registro deverá ser apresentado somente pelos contribuintes obrigados por legislação específica de cada UF,
com o objetivo de agregar informações adicionais ao item, de acordo com tabela a ser publicada pela UF.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C177" C 004 - O O
02 COD_INF_ITE Código da informação adicional de acordo com C 008* - O O
M tabela a ser publicada pelas SEFAZ, conforme
tabela definida no item 5.6.
Observações:
Nível hierárquico - 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C177]
Campo 02 (COD_INF_ITEM) - Preenchimento: o código informado deve constar na tabela 5.6 – Tabela de Informações
Adicionais dos Itens do Documento Fiscal.
----
# REGISTRO C178: OPERAÇÕES COM PRODUTOS SUJEITOS À TRIBUTAÇÃO DE IPI POR
UNIDADE OU QUANTIDADE DE PRODUTO
O registro tem por objetivo fornecer informações adicionais sobre os produtos cuja forma de tributação do IPI, fixada
em reais, seja calculada por unidade ou por determinada quantidade de produto, conforme tabelas de classes de valores.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C178" C 004 - Não O
02 CL_ENQ Código da classe de enquadramento do IPI, C 005 - apresentar O
conforme Tabela 4.5.1.
03 VL_UNID Valor por unidade padrão de tributação N - 02 O
04 QUANT_PAD Quantidade total de produtos na unidade padrão de N - 03 O
tributação
Observações:
Nível hierárquico - 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C178]
----
# REGISTRO C179: INFORMAÇÕES COMPLEMENTARES ST (CÓDIGO 01)
Este registro tem por objetivo informar operações que envolvam repasse, dedução e complemento de ICMS_ST nas
operações interestaduais e nas operações com substituído intermediário.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C179” C 004 - Não O
Valor da base de cálculo ST na apresentar O
02 BC_ST_ORIG_DEST origem/destino em operações N - 02
interestaduais.
Valor do ICMS ST a repassar/deduzir em O
03 ICMS_ST_REP N - 02
operações interestaduais
Valor do ICMS ST a complementar à UF de OC
04 ICMS_ST_COMPL N - 02
destino
Valor da BC de retenção em remessa OC
05 BC_RET N - 02
promovida por Substituído intermediário
Valor da parcela do imposto retido em OC
06 ICMS_RET remessa promovida por substituído N’ - 02
intermediário
Observações:
Nível hierárquico - 4
Ocorrência – 1:1
Campo 01 (REG) - Valor Válido: [C179]
----
# REGISTRO C180: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE ENTRADA
DE MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CÓDIGO 01, 1B, 04 e 55).
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte. O campo
“IND_OPER” do registro pai C100 deve ser igual a “0” - Entrada. Este registro não poderá ser informado se houver um registro
C181 preenchido.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C180” C 004 - O Não apresentar
Código que indica o responsável pela
retenção do ICMS ST:
02 COD_RESP_RET 1-Remetente Direto N 001* - O
2-Remetente Indireto
3-Próprio declarante
03 QUANT_CONV Quantidade do item N - 06 O
Unidade adotada para informar o campo
04 UNID C 006 - O
QUANT_CONV.
Valor unitário da mercadoria,
05 VL_UNIT_CONV considerando a unidade utilizada para N - 06 O
informar o campo “QUANT_CONV”.
Valor unitário do ICMS operação
própria que o informante teria direito ao
crédito caso a mercadoria estivesse sob
06 VL_UNIT_ICMS_OP_CONV N - 06 O
o regime comum de tributação,
considerando unidade utilizada para
informar o campo “QUANT_CONV”.
Valor unitário da base de cálculo do
imposto pago ou retido anteriormente
VL_UNIT_BC_ICMS_ST por substituição, considerando a unidade
07 N - 06 O
_CONV utilizada para informar o campo
“QUANT_CONV”, aplicando-se
redução, se houver.
Valor unitário do imposto pago ou
retido anteriormente por substituição,
08 VL_UNIT_ICMS_ST_CONV inclusive FCP se devido, considerando a N - 06 O
unidade utilizada para informar o campo
“QUANT_CONV”.
Valor unitário do FCP_ST agregado ao
09 VL_UNIT_FCP_ST_CONV valor informado no campo N - 06 OC
“VL_UNIT_ICMS_ST_CONV”
Código do modelo do documento de
arrecadação:
10 COD_DA C 001* - OC
0 – Documento estadual de arrecadação
1 – GNRE
Número do documento de arrecadação,
11 NUM_DA C - - OC
se houver
Observação:
Nível hierárquico - 4
Ocorrência 1:1
Campo 01 (REG) - Valor Válido: [C180]
Campo 02 (COD_RESP_RET) - Valores válidos: [1,2,3]
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou a unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: informar a unidade de medida adotada para o controle de ressarcimento/restituição de
ICMS ST (unidade informada no registro 0200 ou de comercialização, a critério de cada UF). O campo UNID do registro C170
não é necessariamente igual ao campo UNID deste registro. No registro C170, deve corresponder à unidade de medida de
comercialização do item utilizada no documento fiscal. Nos documentos emitidos por fornecedores (terceiros), a unidade de
comercialização adotada pode não ser à unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (VL_UNIT_CONV) – Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos
e acréscimos incondicionais aplicados sobre o valor bruto). O valor unitário do campo 05 não inclui o ICMS ST na aquisição
de participante substituto ou nas hipóteses em que o informante é responsável pela substituição.
Validação: Caso a unidade informada no campo “VL_UNIT_CONV” seja diferente da informada no registro 0200, deve existir
um registro 0220 correspondente.
Campo 06 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: corresponde ao valor do campo 05 (VL_UNIT_CONV),
aplicando-se, se houver, a redução da base de cálculo na tributação de ICMS ST, multiplicado pela alíquota estabelecida na
legislação da UF, conforme a operação (interna, interestadual).
Campo 5 (VL_UNIT_CONV), com redução de base de cálculo, conforme a legislação da UF
* alíq. interna
= Campo 06 (VL_UNIT_ICMS_OP_CONV)
Quando o campo 07 (VL_UNIT_BC_ICMS_ST _CONV) for menor que o campo 05 (VL_UNIT_CONV), o valor unitário da
base de cálculo da retenção do ICMS ST deve ser utilizado no lugar do valor unitário da mercadoria:
Campo 07 (VL_UNIT_BC_ICMS_ST _CONV), com redução de base de cálculo, conforme a
legislação da UF
* alíq. interna
= Campo 06 (VL_UNIT_ICMS_OP_CONV)
Nos casos em que a nota do fornecedor vier preenchida com CST 60 e CSOSN 500 (ICMS cobrado anteriormente por
substituição tributária), o valor desse campo não corresponde ao valor preenchido no campo N26b (vICMSSubstituto), Valor
do ICMS próprio do Substituto.
Campo 08 (VL_UNIT_ICMS_ST_CONV) - Preenchimento: Informar o valor unitário do ICMS ST pago ou retido limitado
à parcela do ICMS ST correspondente ao fato gerador presumido que ainda não se realizou. Corresponde ao campo 07
(VL_UNIT_BC_ICMS_ST _CONV), aplicada a redução de base de cálculo se houver, multiplicada pela alíquota interna (com
o adicional de FCP), estabelecida pela legislação da UF, subtraída do campo 06 (VL_UNIT_ICMS_OP_CONV).
Campo 07 (VL_UNIT_BC_ICMS_ST _CONV), com redução, conforme a legislação da UF
* alíq. interna (incluindo o adicional de FCP)
- Campo 06 (VL_UNIT_ICMS_OP_CONV)
= Campo 08 (VL_UNIT_ICMS_ST_CONV)
Campo 09 (VL_UNIT_FCP_ST_CONV) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza (FCP)
vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV”, considerando a unidade utilizada
para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 10 (COD_DA) - Valores válidos: [0, 1]
----
# REGISTRO C181: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE
DEVOLUÇÃO DE SAÍDAS DE MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA
(CÓDIGO 01, 1B, 04 e 55).
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte. O campo
“IND_OPER” do registro pai C100 deve ser igual a “0” - Entrada. Este registro não poderá ser informado se houver um registro
C180 preenchido.
A chave desse registro é definida pelo campo 05 COD_MOD_SAIDA (para um mesmo C170):
• Para documentos eletrônicos (modelos 55, 59, 60 e 65):
CHV_DFE_SAIDA + NUM_ITEM_SAIDA
• Para documentos em papel (modelos 01, 1B e 04):
COD_MOD_SAIDA + SERIE_SAIDA + NUM_DOC_SAIDA + DT_DOC_SAIDA + NUM_ITEM_SAIDA
Para documentos em papel (modelos 02, 2D):
COD_MOD_SAIDA + ECF_FAB_SAIDA + NUM_DOC_SAIDA + DT_DOC_SAIDA + NUM_ITEM_SAIDA
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C181” C 004 - O Não apresentar
Código do motivo da restituição ou
02 COD_MOT_REST_COMPL C 005* - O
complementação conforme Tabela 5.7
03 QUANT_CONV Quantidade do item N - 06 O
Unidade adotada para informar o campo
04 UNID C 006 - O
QUANT_CONV.
Código do modelo do documento fiscal de
05 COD_MOD_SAIDA saída, conforme a tabela indicada no item C 002* - O
4.1.1
Número de série do documento de saída em
06 SERIE_SAIDA C 003 - OC
papel
Número de série de fabricação do
07 ECF_FAB_SAIDA C 021 OC
equipamento ECF
08 NUM_DOC_SAIDA Número do documento fiscal de saída N 009 - OC
09 CHV_DFE_SAIDA Chave do documento fiscal eletrônico de saída N 044* OC
10 DT_DOC_SAIDA Data da emissão do documento fiscal de saída N 008* - O
Número do item em que foi escriturada a saída
em um registro C185, C380, C480 ou C815
11 NUM_ITEM_SAIDA N 003 - OC
quando o contribuinte informar a saída em um
arquivo de perfil A.
Valor unitário da mercadoria, considerando a
unidade utilizada para informar o campo
12 VL_UNIT_CONV_SAIDA “QUANT_CONV”, correspondente ao valor N - 06 OC
do campo VL_UNIT_CONV, preenchido na
ocasião da saída
Valor médio unitário do ICMS OP, das
mercadorias em estoque, correspondente ao
VL_UNIT_ICMS_OP_EST
13 valor do campo N - 06 OC
OQUE_CONV_SAIDA
VL_UNIT_ICMS_OP_ESTOQUE_CONV,
preenchido na ocasião da saída
Valor médio unitário do ICMS ST, incluindo
FCP ST, das mercadorias em estoque,
VL_UNIT_ICMS_ST_EST
14 correspondente ao valor do campo N - 06 OC
OQUE_CONV_SAIDA
VL_UNIT_ICMS_ST_ESTOQUE_CONV,
preenchido na ocasião da saída
Valor médio unitário do FCP ST agregado ao
ICMS das mercadorias em estoque,
VL_UNIT_FCP_ICMS_ST_
15 correspondente ao valor do campo N - 06 OC
ESTOQUE_CONV_SAIDA
VL_UNIT_FCP_ICMS_ST_ESTOQUE_CON
V, preenchido na ocasião da saída
Valor unitário para o ICMS na operação,
VL_UNIT_ICMS_NA_OPE correspondente ao valor do campo
16 N - 06 OC
RACAO_CONV_SAIDA VL_UNIT_ICMS_NA_OPERACAO_CONV,
preenchido na ocasião da saída
Valor unitário do ICMS correspondente ao
VL_UNIT_ICMS_OP_CON valor do campo
17 N - 06 OC
V_SAIDA VL_UNIT_ICMS_OP_CONV, preenchido na
ocasião da saída
Valor unitário do total do ICMS ST, incluindo
VL_UNIT_ICMS_ST_CON FCP ST, a ser restituído/ressarcido,
18 N - 06 OC
V_REST correspondente ao estorno do complemento
apurado na operação de saída.
Valor unitário correspondente à parcela de
ICMS FCP ST que compõe o campo
VL_UNIT_FCP_ST_CONV
19 “VL_UNIT_ICMS_ST_CONV_REST”, N - 06 OC
_REST
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
Valor unitário do estorno do
VL_UNIT_ICMS_ST_CON
20 ressarcimento/restituição, incluindo FCP ST, N - 06 OC
V_COMPL
apurado na operação de saída.
Valor unitário correspondente à parcela de
ICMS FCP ST que compõe o campo
VL_UNIT_FCP_ST_CONV
21 “VL_UNIT_ICMS_ST_CONV_COMPL”, N - 06 OC
_COMPL
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
Observação:
Nível hierárquico - 4
Ocorrência 1:N
Campo 01 (REG) - Valor Válido: [C181]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere for igual a 5, 6, 7 ou 8.
Para os campos de valores unitários não obrigatórios, se o terceiro caractere do código preenchido no campo
“COD_MOT_REST_COMPL” for:
a) igual a 5, os campos 13, 14 e 15 devem ser preenchidos e os campos 16 a 21 não devem ser preenchidos.
b) igual a 6, os campos 13, 14, 15, 16, 20 e 21 devem ser preenchidos e os campos 17, 18 e 19 não devem ser
preenchidos.
c) igual a 7, os campos 13, 14, 15, 17, 20 e 21 devem ser preenchidos e os campos 18 e 19 não devem ser preenchidos.
d) igual a 8, os campos 13, 14, 15, 16, 18 e 19 devem ser preenchidos e os campos 17, 20 e 21 não devem ser
preenchidos.
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou a unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: informar a unidade de medida adotada para o controle de ressarcimento/restituição de
ICMS ST (unidade informada no registro 0200 ou de comercialização, a critério de cada UF). O campo UNID do registro C170
não é necessariamente igual ao campo UNID deste registro. No registro C170, deve corresponder à unidade de medida de
comercialização do item utilizada no documento fiscal. Nos documentos emitidos por fornecedores (terceiros), a unidade de
comercialização adotada pode não ser à unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (COD_MOD_SAIDA) - Valores válidos: [01, 1B, 02, 2D, 04, 55, 59, 60, 65]
Preenchimento: o valor informado deve constar na tabela 4.1.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº
44/2018 e alterações, reproduzida na subseção 1.4 deste guia. O “código” a ser informado não é exatamente o “modelo” do
documento, devendo ser consultada a tabela 4.1.1. Exemplo: o código “01” deve ser utilizado para os modelos “1” ou “1A".
Campo 06 (SERIE_SAIDA)
Validação: Este campo deve ser preenchido apenas quando o campo 05 (COD_MOD_SAIDA) for igual a 01, 1B ou 04.
Campo 07 (ECF_FAB_SAIDA)
Validação: Este campo deve ser preenchido apenas quando o campo 05 (COD_MOD_SAIDA) for igual de 02 ou 2D.
Campo 08 (NUM_DOC_SAIDA)
Validação: Este campo deve ser preenchido apenas quando o campo 05 (COD_MOD_SAIDA) for igual a 01, 1B, 02, 2D ou
04.
Campo 09 (CHV_DFE_SAIDA)
Validação: Este campo deve ser preenchido quando o campo 05 (COD_MOD_SAIDA) for igual a 55, 59, 60 ou 65.
Campo 10 (DT_DOC_SAIDA) - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”,
excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: O valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 12 (VL_UNIT_CONV_SAIDA) – Preenchimento: A obrigatoriedade de informação deste campo deve seguir a
legislação de cada UF.
Campo 13 (VL_UNIT_ICMS_OP_ESTOQUE_CONV_SAIDA) - Preenchimento: A obrigatoriedade de informação deste
campo deve seguir a legislação de cada UF.
Campo 14 (VL_UNIT_ICMS_ST_ESTOQUE_CONV_SAIDA) - Preenchimento: A obrigatoriedade de informação deste
campo deve seguir a legislação de cada UF.
Campo 15 (VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV_SAIDA) - Preenchimento: A obrigatoriedade de informação
deste campo deve seguir a legislação de cada UF.
Campo 16 (VL_UNIT_ICMS_NA_OPERACAO_CONV_SAIDA) – Preenchimento: A obrigatoriedade de informação deste
campo deve seguir a legislação de cada UF.
Campo 17 (VL_UNIT_ICMS_OP_CONV_SAIDA) – Preenchimento: Nos casos de devolução em que houve direito a
crédito do imposto pela não ocorrência do fato gerador presumido e desfazimento da ST, e a legislação da UF do informante
adota o preenchimento desse campo, informar o valor preenchido no campo VL_UNIT_ICMS_OP_CONV da escrituração do
documento de saída. Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor
expresso no campo 13 (VL_UNIT_ICMS_OP_ESTOQUE_CONV_SAIDA), seu preenchimento será facultativo. O valor deste
campo, quando obrigatório pela legislação da UF, será utilizado para o cálculo do valor do estorno do ressarcimento/restituição
do campo (VL_UNIT_ICMS_ST_CONV_COMPL), conforme fórmula a seguir:
Campo 13 (VL_UNIT_ICMS_OP_ESTOQUE_CONV_SAIDA)
+ Campo 14 (VL_UNIT_ICMS_ST_ESTOQUE_CONV_SAIDA)
- Campo 17 (VL_UNIT_ICMS_OP_CONV_SAIDA)
= Campo 20 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 18 (VL_UNIT_ICMS_ST_CONV_REST) – Preenchimento: Valor do estorno do complemento cobrado em saída
anterior cuja devolução é escriturada no Registro C181.
Validação: Quando o preenchimento dos campos 13, 14, 15 e 16 for obrigatório de acordo com a legislação da UF, o valor do
estorno do complemento é calculado conforme as orientações a seguir:
Campo 16 (VL_UNIT_ICMS_NA_OPERACAO_CONV_SAIDA)
- Campo 13 (VL_UNIT_ICMS_OP_ESTOQUE_CONV_SAIDA)
- Campo 14 (VL_UNIT_ICMS_ST_ESTOQUE_CONV_SAIDA)
= Campo 18 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 20 (VL_UNIT_ICMS_ST_CONV_COMPL) – Validação: O estorno do valor ressarcido / restituído em operação de
saída anterior, cuja devolução é escriturada no Registro C181, é calculado conforme as orientações a seguir.
a) Nos casos em que não houve ocorrência do fato gerador presumido:
a.1) Quando o preenchimento dos campos 13, 14, 15 e 17 for obrigatório de acordo com a legislação da UF,
correspondente ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 13 (VL_UNIT_ICMS_OP_ESTOQUE_CONV_SAIDA)
+ Campo 14 (VL_UNIT_ICMS_ST_ESTOQUE_CONV_SAIDA)
- Campo 17 (VL_UNIT_ICMS_OP_CONV_SAIDA)
= Campo 20 (VL_UNIT_ICMS_ST_CONV_COMPL)
a.2) Quando o campo 17 (VL_UNIT_ICMS_OP_CONV_SAIDA) não for obrigatório e o preenchimento do campo
14 for obrigatório, de acordo com a legislação da UF, corresponde ao valor no campo 14
(VL_UNIT_ICMS_ST_ESTOQUE_CONV_SAIDA)
b) Nos casos em que houve direito ao crédito do imposto, calculada com base no valor de saída da mercadoria
inferior ao valor da BC ICMS ST, quando o preenchimento dos campos 13, 14, 15 e 16 for obrigatório de acordo
com a legislação da UF, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a
unidade utilizada para informar o campo “QUANT_CONV”:
Campo 13 (VL_UNIT_ICMS_OP_ESTOQUE_CONV_SAIDA)
+ Campo 14 (VL_UNIT_ICMS_ST_ESTOQUE_CONV_SAIDA)
- Campo 16 (VL_UNIT_ICMS_NA_OPERACAO_CONV_SAIDA)
= Campo 20 (VL_UNIT_ICMS_ST_CONV_ COMPL)
----
# REGISTRO C185: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE SAÍDA DE
MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CÓDIGO 01, 1B, 04, 55 e 65).
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte. O campo
“IND_OPER” do registro pai C100 deve ser igual a “1” – Saída. Este registro não poderá ser informado se houver um registro
C186 preenchido.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C185” Não
C 004 - O
apresentar
02 NUM_ITEM Número sequencial do item no
N 003 - O
documento fiscal
03 COD_ITEM Código do item (campo 02 do Registro
C 060 - O
0200)
04 CST_ICMS Código da Situação Tributária referente
N 003* - O
ao ICMS
05 CFOP Código Fiscal de Operação e Prestação N 004* - O
06 COD_MOT_REST_COMPL Código do motivo da restituição ou
C 005* - O
complementação conforme Tabela 5.7
07 QUANT_CONV Quantidade do item N - 06 O
08 UNID Unidade adotada para informar o campo
C 006 - O
QUANT_CONV.
09 VL_UNIT_CONV Valor unitário da mercadoria,
considerando a unidade utilizada para N - 06 O
informar o campo “QUANT_CONV”.
10 VL_UNIT_ICMS_NA_OPER Valor unitário para o ICMS na
ACAO_CONV operação, caso não houvesse a ST,
considerando unidade utilizada para
informar o campo “QUANT_CONV”, N - 06 OC
considerando redução da base de
cálculo do ICMS ST na tributação, se
houver.
11 VL_UNIT_ICMS_OP_CONV Valor unitário do ICMS OP calculado
conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”,
utilizado para cálculo de
N - 06 OC
ressarcimento/restituição de ST, no
desfazimento da substituição tributária,
quando se utiliza a fórmula descrita nas
instruções de preenchimento do campo
15, no item a1).
12 VL_UNIT_ICMS_OP_ESTO Valor médio unitário do ICMS que o
QUE_CONV contribuinte teria se creditado referente
à operação de entrada das mercadorias
em estoque caso estivesse submetida ao
N - 06 OC
regime comum de tributação, calculado
conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”
13 VL_UNIT_ICMS_ST_ESTO Valor médio unitário do ICMS ST,
QUE_CONV incluindo FCP ST, das mercadorias em
estoque, considerando a unidade N - 06 OC
utilizada para informar o campo
“QUANT_CONV”
14 VL_UNIT_FCP_ICMS_ST_E Valor médio unitário do FCP ST
STOQUE_CONV agregado ao ICMS das mercadorias em
estoque, considerando a unidade N - 06 OC
utilizada para informar o campo
“QUANT_CONV”
15 VL_UNIT_ICMS_ST_CONV Valor unitário do total do ICMS ST,
_REST incluindo FCP ST, a ser
restituído/ressarcido, calculado
N - 06 OC
conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
16 VL_UNIT_FCP_ST_CONV_ Valor unitário correspondente à parcela
REST de ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_REST
N - 06 OC
”, considerando a unidade utilizada
para informar o campo
“QUANT_CONV”.
17 VL_UNIT_ICMS_ST_CONV Valor unitário do complemento do
_COMPL ICMS, incluindo FCP ST,
N - 06 OC
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
18 VL_UNIT_FCP_ST_CONV_ Valor unitário correspondente à parcela
COMPL de ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_COM
N - 06 OC
PL”, considerando unidade utilizada
para informar o campo
“QUANT_CONV”.
Observação:
Nível hierárquico - 3
Ocorrência: 1:N
Campo 01: (REG) - Valor Válido: [C185]
Campo 02: (NUM_ITEM) – Preenchimento: o campo NUM_ITEM não precisa ser sequencial. Apenas os itens controlados
para a restituição/ressarcimento e complemento de ICMS ST devem ter este registro preenchido.
Campo 03 (COD_ITEM) - Validação: o valor informado neste campo deve existir no Registro 0200 e constantes do documento
fiscal.
Campo 04 (CST_ICMS) – Preenchimento: o campo deverá ser preenchido com o código da Situação Tributária
correspondente ao informado no documento fiscal.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referenciada no item 4.3.1, da Nota
Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 05 (CFOP) - Preenchimento: informar o código de operação que consta no documento fiscal.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01, sendo que o primeiro caractere do CFOP deve ser igual a 5, 6 ou 7. O primeiro caractere deve ser o mesmo para
todos os itens de um documento fiscal.
Campo 06 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere igual a 0, 1, 2 ou 3.Se o terceiro caractere do código preenchido no
campo “COD_MOT_REST_COMPL” for:
a) igual a 0, os campos 12, 13 e 14 devem ser preenchidos e os campos 10, 11 e 15 a 18 não devem ser preenchidos.
b) igual a 1, os campos 10, 12, 13, 14, 15 e 16 devem ser preenchidos e os campos 11, 17 e 18 não devem ser preenchidos
c) igual a 2, os campos 12, 13, 14, 15 e 16 devem ser preenchidos e os campos 10, 17 e 18 não devem ser preenchidos. O campo
11 pode ser preenchido de acordo com a legislação de cada UF.
d) igual a 3, os campos 10, 12, 13, 14, 17 e 18 devem ser preenchidos e os campos 11, 15 e 16 não devem ser preenchidos
Campo 07 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 08 (UNID) - Preenchimento: informar a unidade de medida adotada para o controle de ressarcimento/restituição de
ICMS ST (unidade informada no registro 0200 ou de comercialização, a critério de cada UF).
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 09 (VL_UNIT_CONV) – Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos
e acréscimos incondicionais aplicados sobre o valor bruto) na unidade utilizada para informar o campo “QUANT_CONV”.
Campo 10 (VL_UNIT_ICMS_NA_OPERACAO_CONV) – Preenchimento: Valor correspondente à multiplicação da
alíquota interna (incluindo FCP) (informado no registro 0200) da mercadoria pelo valor correspondente à operação de saída
que seria tributada se não houvesse ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”, aplicando-
se a mesma redução da base de cálculo do ICMS ST na tributação, se houver.
Campo 11 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: Nos casos de direito a crédito do imposto pela não ocorrência
do fato gerador presumido e desfazimento da ST, corresponde ao valor do ICMS da operação própria do sujeito passivo por
substituição do qual a mercadoria tenha sido recebida diretamente ou o valor do ICMS que seria atribuído à operação própria
do contribuinte substituído do qual a mercadoria tenha sido recebida, caso estivesse submetida ao regime comum de tributação,
calculado conforme a legislação de cada UF, considerando unidade utilizada para informar o campo “QUANT_CONV”.
Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor expresso no campo 12
(VL_UNIT_ICMS_OP_ESTOQUE_CONV), seu preenchimento será facultativo. O valor deste campo, quando obrigatório na
UF, será utilizado para o cálculo do valor do ressarcimento/restituição do Campo 15 (VL_UNIT_ICMS_ST_CONV_REST),
conforme fórmula abaixo:
Campo 12 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 11 (VL_UNIT_ICMS_OP_CONV)
= Campo 15 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 12 (VL_UNIT_ICMS_OP_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário de ICMS OP, das
mercadorias em estoque.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário do ICMS ST,
incluindo FCP ST, pago ou retido, das mercadorias em estoque. Quando a mercadoria estiver sujeita ao FCP adicionado ao
ICMS ST, neste campo deve ser informado o valor médio unitário da parcela do ICMS ST + a parcela do FCP.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 14 (VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV) -: Preenchimento: Informar o valor médio unitário da parcela
do FCP adicionado ao ICMS que tenha sido informado no campo “VL_UNIT_ICMS_ST_ESTOQUE_CONV”.
Campo 15 (VL_UNIT_ICMS_ST_CONV_REST) – Validação: O valor a ser ressarcido / restituído é calculado conforme as
orientações a seguir:
a) Nos casos de direito ao crédito do imposto, por não ocorrência do fato gerador presumido:
a.1) Quando o campo 11 (VL_UNIT_ICMS_OP_CONV) for obrigatório, de acordo com a legislação da UF,
correspondente ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 12 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 11 (VL_UNIT_ICMS_OP_CONV)
= Campo 15 (VL_UNIT_ICMS_ST_CONV_REST)
a.2) Quando o campo 11(VL_UNIT_ICMS_OP_CONV) não for obrigatório, de acordo com a legislação da UF,
corresponde ao valor no campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
Nos casos de direito ao crédito do imposto, calculada com base no valor de saída da mercadoria inferior ao valor da
BC ICMS ST, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a unidade utilizada
para informar o campo “QUANT_CONV”:
Campo 12 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 10 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
= Campo 15 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 16 (VL_UNIT_FCP_ST_CONV_REST) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza
(FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a
unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 17 (VL_UNIT_ICMS_ST_CONV_COMPL) – Validação: Nos casos de complemento, informar o valor unitário de
ICMS correspondente ao cálculo a seguir. O valor a ser ressarcido / restituído é calculado conforme as orientações a seguir:
Campo 10 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
- Campo 12 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
- Campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
= Campo 17 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 18 (VL_UNIT_FCP_ST_CONV_COMPL) – Preenchimento: Informar o valor unitário do Fundo de Combate à
Pobreza (FCP) vinculado à substituição tributária que compõe o campo 17 “VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando a unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
----
# REGISTRO C186: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE
DEVOLUÇÃO DE ENTRADAS DE MERCADORIAS SUJEITAS À SUBSTITUIÇÃO
TRIBUTÁRIA (CÓDIGO 01, 1B, 04 e 55).
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte. O campo
“IND_OPER” do registro pai C100 deve ser igual a “1” - Saída. Este registro não poderá ser informado se houver um registro
C185 preenchido.
A chave desse registro é definida pelo campo 09 COD_MOD_ ENTRADA (para um mesmo C100):
• Para documentos eletrônicos (modelos 55, 59 e 65):
CHV_DFE_ENTRADA + NUM_ITEM_ENTRADA
• Para documentos em papel (modelos 01, 1B e 04):
COD_MOD_ENTRADA + SERIE_ENTRADA + NUM_DOC_ENTRADA + DT_DOC_ENTRADA + NUM_ITEM_ENTRADA
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C186” C 004 - Não O
apresentar
02 NUM_ITEM Número sequencial do item no documento N 003 - O
fiscal de saída
03 COD_ITEM Código do item (campo 02 do Registro C 060 - O
0200)
04 CST_ICMS Código da Situação Tributária referente ao N 003* -
ICMS no documento fiscal de saída
05 CFOP Código Fiscal de Operação e Prestação no N 004* - O
documento fiscal de saída
06 COD_MOT_REST_COMPL Código do motivo da restituição ou C 005* - O O
complementação conforme Tabela 5.7
07 QUANT_CONV Quantidade do item no documento fiscal de N - 06 O
saída de acordo com as instruções de
preenchimento.
08 UNID Unidade adotada para informar o campo C 006 - O
QUANT_CONV.
09 COD_MOD_ENTRADA Código do modelo do documento fiscal de C 002* - O
entrada, conforme a tabela indicada no
item 4.1.1
10 SERIE_ENTRADA Número de série do documento de entrada C 003 - OC
em papel
11 NUM_DOC_ENTRADA Número do documento fiscal de entrada N 009 OC
12 CHV_DFE_ENTRADA Chave do documento fiscal eletrônico de N 044* - OC
entrada
13 DT_DOC_ENTRADA Data da emissão do documento fiscal de N 008* - O
entrada
14 NUM_ITEM_ENTRADA Item do documento fiscal de entrada N 003 - O
15 VL_UNIT_CONV_ENTRADA Valor unitário da mercadoria, N - 06 OC
considerando a unidade utilizada para
informar o campo “QUANT_CONV”,
correspondente ao valor do campo
VL_UNIT_CONV, preenchido na ocasião
da entrada
16 VL_UNIT_ICMS_OP_CONV_ Valor unitário do ICMS correspondente ao N - 06 OC
ENTRADA valor do campo
VL_UNIT_ICMS_OP_CONV, preenchido
na ocasião da entrada
17 VL_UNIT_BC_ICMS_ST Valor unitário da base de cálculo do N - 06 OC
_CONV_ENTRADA imposto pago ou retido anteriormente
por substituição, correspondente ao valor
do campo
VL_UNIT_BC_ICMS_ST_CONV,
preenchido na ocasião da entrada
18 VL_UNIT_ICMS_ST_CONV_ Valor unitário do imposto pago ou retido N - 06 OC
ENTRADA anteriormente por substituição, inclusive
FCP se devido, correspondente ao valor do
campo VL_UNIT_ICMS_ST_CONV,
preenchido na ocasião da entrada
19 VL_UNIT_FCP_ST_CONV_E Valor unitário do FCP_ST, correspondente N - 06 OC
NTRADA ao valor do campo
VL_UNIT_FCP_ST_CONV, preenchido
na ocasião da entrada
Observação:
Nível hierárquico - 3
Ocorrência 1:N
Campo 01 (REG) - Valor Válido: [C186]
Campo 06 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere for igual a 4.
Campo 07 (QUANT_CONV) – Preenchimento: Quantidade do item devolvido na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 09 (COD_MOD_ENTRADA) - Valores válidos: [01, 1B, 04, 55]
Preenchimento: o valor informado deve constar na tabela 4.1.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº
44/2018 e alterações, reproduzida na subseção 1.4 deste guia. O “código” a ser informado não é exatamente o “modelo” do
documento, devendo ser consultada a tabela 4.1.1. Exemplo: o código “01” deve ser utilizado para os modelos “1” ou “1A".
Campo 10 (SERIE_ENTRADA)
Validação: Este campo deve ser preenchido apenas quando o campo 09 (COD_MOD_ENTRADA) for diferente de 55.
Campo 11 (NUM_DOC_ENTRADA)
Validação: Este campo deve ser preenchido apenas quando o campo 09 (COD_MOD_ENTRADA) for diferente de 55.
Campo 12 (CHV_DFE_ENTRADA)
Validação: Este campo deve ser preenchido quando o campo 09 (COD_MOD_ENTRADA) for igual a 55.
Campo 13 (DT_DOC_ENTRADA) - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”,
excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: O valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 15 (VL_UNIT_CONV_ENTRADA) - Preenchimento: A obrigatoriedade de informação deste campo deve seguir a
legislação de cada UF.
Campo 16 (VL_UNIT_ICMS_OP_CONV_ENTRADA) - Preenchimento: A obrigatoriedade de informação deste campo
deve seguir a legislação de cada UF.
Campo 17 (VL_UNIT_BC_ICMS_ST _CONV_ENTRADA) - Preenchimento: A obrigatoriedade de informação deste campo
deve seguir a legislação de cada UF.
Campo 18 (VL_UNIT_ICMS_ST_CONV_ENTRADA) - Preenchimento: A obrigatoriedade de informação deste campo
deve seguir a legislação da UF de domicílio do contribuinte.
Campo 19 (VL_UNIT_FCP_ST_CONV_ENTRADA) - Preenchimento: A obrigatoriedade de informação deste campo deve
seguir a legislação de cada UF.
----
# REGISTRO C190: REGISTRO ANALÍTICO DO DOCUMENTO (CÓDIGO 01, 1B, 04, 55 e 65)
Este registro tem por objetivo representar a escrituração dos documentos fiscais totalizados por CST, CFOP e Alíquota de ICMS.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos campos: CST_ICMS, CFOP e ALIQ_ICMS. A combinação dos valores dos campos CST_ICMS, CFOP e ALIQ_ICMS deve existir nos respectivos registros de itens do C170, quando este registro for exigido.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C190" C 004 - O O
02 CST_ICMS Código da Situação Tributária, conforme a Tabela N 003* - O O
indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação do N 004* - O O
agrupamento de itens
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
05 VL_OPR Valor da operação na combinação de CST_ICMS, N - 02 O O
CFOP e alíquota do ICMS, correspondente ao
somatório do valor das mercadorias, despesas
acessórias (frete, seguros e outras despesas
acessórias), ICMS_ST, FCP_ST e IPI.
06 VL_BC_ICMS Parcela correspondente ao "Valor da base de N - 02 O O
cálculo do ICMS" referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
07 VL_ICMS Parcela correspondente ao "Valor do ICMS", N - 02 O O incluindo o FCP, quando aplicável, referente à combinação de CST_ICMS, CFOP e alíquota do ICMS.
08 VL_BC_ICMS_ Parcela correspondente ao "Valor da base de N - 02 O O
ST cálculo do ICMS" da substituição tributária
referente à combinação de CST_ICMS, CFOP e
alíquota do ICMS.
09 VL_ICMS_ST Parcela correspondente ao valor N - 02 O O
creditado/debitado do ICMS da substituição
tributária, incluindo o FCP_ ST, quando
aplicável, referente à combinação de CST_ICMS,
CFOP, e alíquota do ICMS.
10 VL_RED_BC Valor não tributado em função da redução da base N - 02 O O
de cálculo do ICMS, referente à combinação de
CST_ICMS, CFOP e alíquota do ICMS.
11 VL_IPI Parcela correspondente ao "Valor do IPI" N - 02 O O
referente à combinação CST_ICMS, CFOP e
alíquota do ICMS.
12 COD_OBS Código da observação do lançamento fiscal C 006 - OC OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C190]
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao
ICMS, constante do Artigo 5º do Convênio SN/70.
Campo 03 (CFOP) - Preenchimento: nas operações de entradas, devem ser registrados os códigos de operação que
correspondem ao tratamento tributário relativo à destinação do item.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01. Para Notas Fiscais Eletrônicas ao Consumidor Final (NFC-e) só poderão ser informados CFOP iniciados com 5.
Se o campo IND_OPER do registro C100 for igual a “0” (zero), então o primeiro caractere do CFOP deve ser igual a 1, 2 ou
3. Se campo IND_OPER do registro C100 for igual a “1” (um), então o primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
Campo 05 (VL_OPR) - Preenchimento: Na combinação de CST_ICMS, CFOP e ALIQ_ICMS, informar neste campo o valor
das mercadorias somadas aos valores de fretes, seguros e outras despesas acessórias e os valores de ICMS_ST, FCP_ST e IPI
(somente quando o IPI está destacado na NF), subtraídos o desconto incondicional e o abatimento não tributado e não comercial.
Validação: O somatório dos valores deste campo deve, em princípio, corresponder ao valor total do documento informado no
registro C100. Na ocorrência de divergência entre os valores será emitida uma “Advertência” pelo PVA-EFD-ICMS/IPI, o que
não impedirá a assinatura e transmissão do arquivo.
Campo 06 (VL_BC_ICMS) - Preenchimento: informar a base de cálculo do ICMS, referente à combinação dos campos
CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Validação: o valor constante neste campo deve corresponder à soma dos valores do Campo VL_BC_ICMS dos registros C170
(itens), se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste registro.
Campo 07 (VL_ICMS) - Preenchimento: informar o valor do ICMS referente à combinação dos campos CST_ICMS, CFOP
e ALIQ_ICMS deste registro.
Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_ICMS do registro C170 (itens),
se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste registro.
Campo 08 (VL_BC_ICMS_ST) - Preenchimento: informar a base de cálculo do ICMS ST referente à combinação dos campos
CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_BC_ICMS ST do registro C170
(itens), se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste registro.
Campo 09 (VL_ICMS_ST) - Preenchimento: informar o valor creditado/debitado do ICMS da substituição tributária,
referente à combinação dos campos CST_ICMS, CFOP, e ALIQ_ICMS deste registro.
Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_ICMS ST do registro C170
(itens), se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste registro.
Campo 10 (VL_RED_BC) - Preenchimento: informar o valor não tributado em função da redução da base de cálculo do
ICMS, referente à combinação dos campos CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Validação: Quando o campo COD_SIT do registro mestre for igual a “00” ou “01” então o campo VL_RED_BC deve ser
maior que zero se o 2º e 3º caracteres do CST_ICMS forem iguais a 20 ou 70.
Campo 11 (VL_IPI) - Preenchimento: informar o valor do IPI referente à combinação dos campos CST_ICMS, CFOP e
ALIQ_ICMS deste registro.
Campo 12 (COD_OBS) - Preenchimento: este campo só deve ser informado pelos contribuintes localizados em UF que
determine em sua legislação o seu preenchimento.
Validação: o código informado deve constar do registro 0460.
----
# REGISTRO C191: INFORMAÇÕES DO FUNDO DE COMBATE À POBREZA – FCP – NA NF-
e (CÓDIGO 55) E NA NFC-e (CÓDIGO 65)
Este registro tem por objetivo prestar informações do Fundo de Combate à Pobreza (FCP), constante na NF-e e na
NFC-e. Os valores deste registro são meramente informativos e não são contabilizados na apuração dos registros no bloco E.
A obrigatoriedade e forma de apresentação de cada campo deste registro deve ser verificada junto às unidades federativas.
Este registro não se aplica aos valores já informados no registro C101, relativos ao Fundo de Combate à Pobreza (FCP)
nas hipóteses de aplicabilidade da EC 87/15.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
1 REG Texto fixo contendo "C191" C 004 - O O
2 VL_FCP_OP Valor do Fundo de Combate à Pobreza (FCP) vinculado à N - 02 OC OC
operação própria, na combinação de CST_ICMS, CFOP e
alíquota do ICMS
3 VL_FCP_ST Valor do Fundo de Combate à Pobreza (FCP) vinculado à N - 02 OC OC
operação de substituição tributária, na combinação de
CST_ICMS, CFOP e alíquota do ICMS.
4 VL_FCP_RET Valor relativo ao Fundo de Combate à Pobreza (FCP) N - 02 OC OC
retido anteriormente nas operações com Substituição
Tributárias, na combinação de CST_ICMS, CFOP e
alíquota do ICMS
Observações:
Nível hierárquico – 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C191]
Campo 02 (VL_FCP_OP) – Preenchimento: informar o valor total do Fundo de Combate à Pobreza (FCP) vinculado à
operação própria, relativo aos itens com mesma combinação de CST_ICMS, CFOP e alíquota do ICMS informada no registro
pai, C190.
Validação: Só pode ser preenchido quando o campo CST_ICMS do registro C190 assumir o valor x00, x10, x20, x51, x70 ou
x90.
Campo 03 (VL_FCP_ST) – Preenchimento: informar o valor do Fundo de Combate à Pobreza (FCP) vinculado à operação
de substituição tributária, relativo aos itens com mesma combinação de CST_ICMS, CFOP e alíquota do ICMS informada no
registro pai, C190.
Validação: Só pode ser preenchido quando o campo CST_ICMS do registro C190 assumir o valor x10, x30, x70, x90, 201,
202, 203 ou 900.
Campo 04 (VL_FCP_RET) – Preenchimento: informar o valor do Fundo de Combate à Pobreza (FCP) retido anteriormente,
relativo aos itens com mesma combinação de CST_ICMS, CFOP e alíquota do ICMS informada no registro pai, C190.
Validação: Só pode ser preenchido quando o campo CST_ICMS do registro C190 assumir o valor x60 ou 500.
----
# REGISTRO C195: OBSERVAÇÕES DO LANÇAMENTO FISCAL (CÓDIGO 01, 1B, 04, 55 E 65)
Este registro deve ser informado quando, em decorrência da legislação estadual, houver ajustes nos documentos fiscais,
informações sobre diferencial de alíquota, antecipação de imposto e outras situações. Estas informações equivalem às
observações que são lançadas na coluna “Observações” dos Livros Fiscais previstos no Convênio SN/70 – SINIEF, art. 63, I a
IV.
Sempre que existir um ajuste (lançamentos referentes aos impostos que têm o cálculo detalhado em Informações
Complementares da NF; ou aos impostos que estão definidos na legislação e não constam na NF; ou aos recolhimentos
antecipados dos impostos), deve, conforme dispuser a legislação estadual, ocorrer uma observação.
Obs.: Não precisam ser informadas neste registro, salvo disposição contrária da legislação estadual, as informações que
constam do quadro Dados Adicionais das notas fiscais modelo 1 ou 1A que não interfiram na Apuração do ICMS.
Situação especial: Este registro será gerado também pelas empresas que são obrigadas a elaborar outras apurações
nos estados do Espírito Santo, Pará e Amazonas.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C195" C 004 - O O
02 COD_OBS Código da observação do lançamento fiscal (campo 02 do C 006 - O O
Registro 0460)
03 TXT_COMPL Descrição complementar do código de observação. C - - OC OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C195]
Campo 02 (COD_OBS) – Preenchimento: as observações de lançamento devem ser informadas neste campo, exceto
quando a legislação estadual prever o preenchimento do campo COD_OBS do registro C190.
Validação: o código informado deve constar do registro 0460.
Campo 03 (TXT_COMPL) - Preenchimento: utilizado para complementar observação, cujo código é de informação genérica.
----
# REGISTRO C197: OUTRAS OBRIGAÇÕES TRIBUTÁRIAS, AJUSTES E INFORMAÇÕES DE
VALORES PROVENIENTES DE DOCUMENTO FISCAL.
Este registro tem por objetivo detalhar outras obrigações tributárias, ajustes e informações de valores do documento
fiscal do registro C195, que podem ou não alterar o cálculo do valor do imposto.
Os valores de ICMS ou ICMS ST (campo 07-VL_ICMS) serão somados diretamente na apuração, no registro E110 –
Apuração do ICMS – Operações Próprias, campo VL_AJ_DEBITOS ou campo VL_AJ_CREDITOS, e no registro E210 –
Apuração do ICMS – Substituição Tributária, campo VL_AJ_CREDITOS_ST e campo VL_AJ_DEBITOS_ST, de acordo com
a especificação do TERCEIRO CARACTERE do Código do Ajuste (Tabela 5.3 -Tabela de Ajustes e Valores provenientes do
Documento Fiscal).
Este registro será utilizado também por contribuinte para o qual a Administração Tributária Estadual exija, por meio
de legislação específica, apuração em separado (sub-apuração). Neste caso o Estado publicará a Tabela 5.3 com códigos que
contenham os dígitos “3”, “4”, “5”, “6”, “7” e “8” no quarto caractere (“Tipos de Apuração de ICMS”), sendo que cada um
dos dígitos possibilitará a escrituração de uma apuração em separado (sub-apuração) no registro 1900 e filhos. Para que haja a
apuração em separado do ICMS de determinadas operações ou itens de mercadorias, estes valores terão de ser estornados da
Apuração Normal (E110) e transferidos para as sub-apurações constantes do registro 1900 e filhos por meio de lançamentos de
ajustes neste registro. Isto ocorrerá quando:
1. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C197 for igual a “2 – Estorno de Débito” e
o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gerará um ajuste a crédito (campo 07- VL_AJ_CREDITOS) no registro E110 e
também um outro lançamento a débito no registro 1920 (campo 02 -
VL_TOT_TRANSF_DEBITOS_OA) da apuração em separado (sub-apuração) definida no campo 02-
IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4”, “5”, “6”, “7” e “8”, que deverá
coincidir com o quarto caractere do COD_AJ; e
2. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C197 for igual a “5 – Estorno de Crédito”
e o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gerará um ajuste a débito (campo 03- VL_AJ_DEBITOS) no registro E110 e
também um outro lançamento a crédito no registro 1920 (campo 05 -
VL_TOT_TRANSF_CRÉDITOS_OA) da apuração em separado (sub-apuração) que for definida no
campo 02 - IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4” “5”, “6”, “7” e “8”, que
deverá coincidir com o quarto caractere do COD_AJ.
Os valores que gerarem crédito ou débito de ICMS (ou seja, aqueles que não são simplesmente informativos) serão
somados na apuração, assim como os registros C190.
Este registro somente deve ser informado para as UF que publicarem a tabela constante no item 5.3 da Nota Técnica,
instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C197" C 004 - O O
02 COD_AJ Código dos ajustes/benefício/incentivo, conforme C 010* - O O
tabela indicada no item 5.3.
03 DESCR_COMPL_AJ Descrição complementar do ajuste do documento C - - OC OC
fiscal
04 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC OC
05 VL_BC_ICMS Base de cálculo do ICMS ou do ICMS ST N - 02 OC OC
06 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
07 VL_ICMS Valor do ICMS ou do ICMS ST N - 02 OC OC
08 VL_OUTROS Outros valores N - 02 OC OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C197]
Campo 02 (COD_AJ) - Validação: verifica se o COD_AJ está de acordo com a Tabela da UF do informante do arquivo.
Campo 03 (DESCR_COMPL_AJ): Preenchimento: O contribuinte deverá fazer a descrição complementar de ajustes (tabela
5.3) sempre que informar códigos genéricos.
Campo 04 (COD_ITEM) - Preenchimento: deve ser informado se o ajuste/benefício for relacionado ao produto. Porém,
quando não houver registro C170, como NF-e de emissão própria, o COD_ITEM deverá ser informado no registro 0200.
Campo 07 (VL_ICMS) - Preenchimento: valor do montante do ajuste do imposto. Para ajustes referentes a ICMS ST, o campo
VL_ICMS deve conter o valor do ICMS ST. Os dados que gerarem crédito ou débito (ou seja, aqueles que não são simplesmente
informativos) serão somados na apuração, assim como os registros C190.
Campo 08 (VL_OUTROS) - Preenchimento: preencher com outros valores, quando o código do ajuste for informativo,
conforme Tabela 5.3.
----
# REGISTRO C300: RESUMO DIÁRIO DAS NOTAS FISCAIS DE VENDA A CONSUMIDOR
(CÓDIGO 02)
Este registro deve ser apresentado pelos contribuintes que utilizam notas fiscais de venda ao consumidor, não emitidas
por ECF. Trata-se de um resumo diário, por série e subsérie do documento fiscal, de todas as operações praticadas. Existirão
tantos registros C300 quantos forem os agrupamentos de séries e subséries dos documentos fiscais emitidos no dia. Os valores
de documentos fiscais cancelados não devem ser computados no valor total dos documentos (campo VL_DOC).
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos SER, SUB, NUM_DOC_INI e NUM_DOC_FIN. Não é permitida a intersecção (sobreposição) de intervalos entre os
registros C300 informados com a mesma combinação de valores dos campos SER, SUB, NUM_DOC_INI e NUM_DOC_FIN.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C300" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, C 002* - apresentar O
conforme a Tabela 4.1.1
03 SER Série do documento fiscal C 004 - O
04 SUB Subsérie do documento fiscal C 003 - OC
05 NUM_DOC_INI Número do documento fiscal inicial N 006 - O
06 NUM_DOC_FIN Número do documento fiscal final N 006 - O
07 DT_DOC Data da emissão dos documentos fiscais N 008* - O
08 VL_DOC Valor total dos documentos N - 02 O
09 VL_PIS Valor total do PIS N - 02 OC
10 VL_COFINS Valor total da COFINS N - 02 OC
11 COD_CTA Código da conta analítica contábil C - - OC
debitada/creditada
Observações:
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C300]
Campo 02 (COD_MOD) - Valor Válido: [02] - – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 05 (NUM_DOC_INI) – Validação: valor informado deve ser maior que “0” (zero). O número do documento inicial
deve ser menor ou igual ao número do documento final.
Campo 06 (NUM_DOC_FIN) - Validação: valor informado deve ser maior que “0” (zero).
Campo 07 (DT_DOC) - Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do
registro 0000.
Campo 08 (VL_DOC) - Validação: o valor informado no campo deve ser igual à soma do campo VL_ITEM dos registros
C321.
Campo 09 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 10 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C310: DOCUMENTOS CANCELADOS DE NOTAS FISCAIS DE VENDA A
CONSUMIDOR (CÓDIGO 02).
Este registro tem por objetivo informar os números dos documentos fiscais cancelados.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C310" C 004 - Não O
02 NUM_DOC_CANC Número do documento fiscal cancelado N - - apresentar O
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C310]
Campo 02 (NUM_DOC_CANC) - Validação: o número do documento cancelado deve estar contido no intervalo informado
no registro C300, campos NUM_DOC_INI e NUM_DOC_FIN.
----
# REGISTRO C320: REGISTRO ANALÍTICO DO RESUMO DIÁRIO DAS NOTAS FISCAIS DE
VENDA A CONSUMIDOR (CÓDIGO 02).
Este registro tem por objetivo informar a consolidação diária dos valores das notas fiscais de venda ao consumidor,
não emitidas por ECF, e deve ser apresentado de forma agrupada na combinação CST_ICMS, CFOP e Alíquota de ICMS.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C320" C 004 - Não O
02 CST_ICMS Código da Situação Tributária, conforme a N 003* - apresentar O
Tabela indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação N 004* - O
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
05 VL_OPR Valor total acumulado das operações N - 02 O
correspondentes à combinação de
CST_ICMS, CFOP e alíquota do ICMS,
incluídas as despesas acessórias e acréscimos.
06 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS, N - 02 O
referente à combinação de CST_ICMS,
CFOP, e alíquota do ICMS.
07 VL_ICMS Valor acumulado do ICMS, referente à N - 02 O
combinação de CST_ICMS, CFOP e alíquota
do ICMS.
08 VL_RED_BC Valor não tributado em função da redução da N - 02 O
base de cálculo do ICMS, referente à
combinação de CST_ICMS, CFOP, e alíquota
do ICMS.
09 COD_OBS Código da observação do lançamento fiscal C 006 - OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C320]
Campo 02 (CST_ICMS) - Validação: o valor informado neste campo deve existir na Tabela da Situação Tributária referente
ao ICMS, constante do Artigo 5º do Convênio SN/70, sendo que o primeiro caractere sempre será Zero.
Campo 03 (CFOP) – Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01. Não podem ser utilizados os títulos dos agrupamentos de CFOP e os códigos devem ser
iniciados por “5”.
Preenchimento: deve referir-se apenas a operações de saídas internas.
Campo 06 (VL_BC_ICMS) - Validação: deve ser igual à soma do campo VL_BC_ICMS do registro C321.
Campo 07 (VL_ICMS) - Validação: deve ser igual à soma do campo VL_ICMS do registro C321.
----
# REGISTRO C321: ITENS DO RESUMO DIÁRIO DOS DOCUMENTOS (CÓDIGO 02).
Este registro é o detalhamento, por itens de mercadoria, da consolidação diária dos valores das notas fiscais de venda
ao consumidor, não emitidas por ECF.
Validação do Registro: não podem ser informados dois ou mais registros C321 com o mesmo valor para o campo
COD_ITEM.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C321" C 004 - Não O
02 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - apresentar O
03 QTD Quantidade acumulada do item N - 03 O
04 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
05 VL_ITEM Valor acumulado do item N - 02 O
06 VL_DESC Valor do desconto acumulado N - 02 OC
07 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS N - 02 OC
08 VL_ICMS Valor acumulado do ICMS debitado N - 02 OC
09 VL_PIS Valor acumulado do PIS N - 02 OC
10 VL_COFINS Valor acumulado da COFINS N - 02 OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C321]
Campo 05 (VL_ITEM) - Preenchimento: valor líquido acumulado do item, já considerado o valor do desconto incondicional.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 06 (VL_DESC) - Preenchimento: informar o valor do desconto acumulado. Valor meramente informativo.
Campo 09 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 10 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C330: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE SAÍDA DE
MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CÓDIGO 02)
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C330” C 004 - Não O
apresentar
02 COD_MOT_REST_COMPL Código do motivo da restituição ou C 005* - O
complementação conforme Tabela 5.7
03 QUANT_CONV Quantidade do item N - 06 O
04 UNID Unidade adotada para informar o campo C 006 - O
QUANT_CONV.
05 VL_UNIT_CONV Valor unitário da mercadoria, N - 06 O
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
06 VL_UNIT_ICMS_NA_OPER Valor unitário para o ICMS na operação, N - 06 OC
ACAO_CONV caso não houvesse a ST, considerando
unidade utilizada para informar o campo
“QUANT_CONV”, aplicando-se a mesma
redução da base de cálculo do ICMS ST na
tributação, se houver.
07 VL_UNIT_ICMS_OP_CON Valor unitário do ICMS OP calculado N - 06 OC
V conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”,
utilizado para cálculo de
ressarcimento/restituição de ST, no
desfazimento da substituição tributária,
quando se utiliza a fórmula descrita nas
instruções de preenchimento do campo 11,
no item a1).
08 VL_UNIT_ICMS_OP_ESTO Valor médio unitário do ICMS que o N - 06 OC
QUE_CONV contribuinte teria se creditado referente à
operação de entrada das mercadorias em
estoque caso estivesse submetida ao
regime comum de tributação, calculado
conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”
09 VL_UNIT_ICMS_ST_ESTO Valor médio unitário do ICMS ST, N - 06 OC
QUE_CONV incluindo FCP ST, das mercadorias em
estoque, considerando unidade utilizada
para informar o campo
“QUANT_CONV”.
10 VL_UNIT_FCP_ICMS_ST_ Valor médio unitário do FCP ST agregado N - 06 OC
ESTOQUE_CONV ao ICMS das mercadorias em estoque,
considerando unidade utilizada para
informar o campo “QUANT_CONV”
11 VL_UNIT_ICMS_ST_CONV Valor unitário do total do ICMS ST, N - 06 OC
_REST incluindo FCP ST, a ser
restituído/ressarcido, calculado conforme a
legislação de cada UF, considerando a
unidade utilizada para informar o campo
“QUANT_CONV”.
12 VL_UNIT_FCP_ST_CONV_ Valor unitário correspondente à parcela de N - 06 OC
REST ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_REST”,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
13 VL_UNIT_ICMS_ST_CONV Valor unitário do complemento do ICMS, N - 06 OC
_COMPL incluindo FCP ST, considerando a
unidade utilizada para informar o campo
“QUANT_CONV”.
14 VL_UNIT_FCP_ST_CONV_ Valor unitário correspondente à parcela de N - 06 OC
COMPL ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_COMPL”
, considerando unidade utilizada para
informar o campo “QUANT_CONV”.
Observação:
Nível hierárquico - 5
Ocorrência 1:1
Campo 01 (REG) - Valor Válido: [C330]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere igual a 0, 1, 2 ou 3.
Se o terceiro caractere do código preenchido no campo “COD_MOT_REST_COMPL” for:
a) igual a 0, os campos 08, 09 e 10 devem ser preenchidos e os campos 06, 07, 11 a 14 não devem ser preenchidos.
b) igual a 1, os campos 06, 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 07, 13 e 14 não devem ser preenchidos.
c) igual a 2, os campos 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 06, 13 e 14 não devem ser preenchidos. O campo
07 pode ser preenchido de acordo com a legislação de cada UF.
d) igual a 3, os campos 06, 08, 09, 10, 13 e 14 devem ser preenchidos e os campos 07, 11 e 12 não devem ser preenchidos.
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: O campo UNID do registro pai não é necessariamente igual ao campo UNID deste
registro. No registro C321, deve corresponder à unidade de medida de comercialização do item utilizada no documento fiscal,
que pode não ser a unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (VL_UNIT_CONV) - Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos
e acréscimos incondicionais aplicados sobre o valor bruto) na unidade utilizada para informar o campo “QUANT_CONV”.
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV) – Preenchimento: Valor correspondente à multiplicação da
alíquota interna (incluindo FCP) (informado no registro 0200) da mercadoria pelo valor correspondente à operação de saída
que seria tributada se não houvesse ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”, aplicando-
se a mesma redução da base de cálculo do ICMS ST na tributação, se houver.
Campo 07 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: Nos casos de direito a crédito do imposto pela não ocorrência
do fato gerador presumido e desfazimento da ST, corresponde ao valor do ICMS da operação própria do sujeito passivo por
substituição do qual a mercadoria tenha sido recebida diretamente ou o valor do ICMS que seria atribuído à operação própria
do contribuinte substituído do qual a mercadoria tenha sido recebida, caso estivesse submetida ao regime comum de tributação,
calculado conforme a legislação de cada UF, considerando unidade utilizada para informar o campo “QUANT_CONV”.
Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor expresso no campo 12
(VL_UNIT_ICMS_OP_ESTOQUE_CONV), seu preenchimento será facultativo. O valor deste campo, quando obrigatório na
UF, será utilizado para o cálculo do valor do ressarcimento/restituição do Campo 15 (VL_UNIT_ICMS_ST_CONV_REST),
conforme fórmula abaixo:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 12 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário de ICMS OP, das
mercadorias em estoque.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV) - Preenchimento: Informar o valor médio unitário do ICMS ST,
incluindo FCP ST, pago ou retido, das mercadorias em estoque. Quando a mercadoria estiver sujeita ao FCP adicionado ao
ICMS ST, neste campo deve ser informado o valor médio unitário da parcela do ICMS ST + a parcela do FCP.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 10 (VL_UNIT_FCP_ CONV) - Preenchimento: Informar o valor médio unitário da parcela do FCP adicionado ao
ICMS que tenha sido informado no campo “VL_UNIT_ICMS_ST_ESTOQUE_CONV”.
Campo 11 (VL_UNIT_ICMS_ST_CONV_REST) – Validação: O valor a ser ressarcido / restituído é calculado conforme as
orientações a seguir:
a) Nos casos de direito ao crédito do imposto, por não ocorrência do fato gerador presumido:
a.1) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) for obrigatório, de acordo com a legislação da UF,
correspondente ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 12 (VL_UNIT_ICMS_ST_CONV_REST)
a.2) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) não for obrigatório, de acordo com a legislação da UF, o campo
VL_UNIT_ICMS_ST_CONV_REST corresponde ao valor no campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
b) Nos casos de direito ao crédito do imposto, calculada com base no valor de saída da mercadoria inferior ao
valor da BC ICMS ST, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a
unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
= Campo 12 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 12 (VL_UNIT_FCP_ST_CONV_REST) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza
(FCP) vinculado à substituição tributária que compõe o campo “ VL_UNIT_ICMS_ST_CONV_REST”, considerando a
unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL) – Validação: Nos casos de complemento, informar o valor unitário de
ICMS correspondente ao cálculo a seguir. O valor a ser ressarcido / restituído é calculado conforme as orientações a seguir:
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
- Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
- Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
= Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 14 (VL_UNIT_ICMS_ST_CONV_COMPL) – Preenchimento: Informar o valor unitário do Fundo de Combate à
Pobreza (FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando a unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF
----
# REGISTRO C350: NOTA FISCAL DE VENDA A CONSUMIDOR (CÓDIGO 02)
Este registro deve ser apresentado pelos contribuintes que utilizam notas fiscais de venda ao consumidor, não emitidas
por ECF. As notas fiscais canceladas não devem ser informadas.
Os CNPJ e CPF citados neste registro NÃO devem ser informados no registro 0150.
Nº Campo Descrição Tipo Tam Dec Entr. Saída
01 REG Texto fixo contendo "C350" C 004 - Não O
02 SER Série do documento fiscal C 003 - apresentar OC
03 SUB_SER Subsérie do documento fiscal C 003 - OC
04 NUM_DOC Número do documento fiscal N 006 - O
05 DT_DOC Data da emissão do documento fiscal N 008* O
06 CNPJ_CPF CNPJ ou CPF do destinatário N 014 - OC
VL_MERC Valor das mercadorias constantes no documento N - 02
07 O
fiscal
08 VL_DOC Valor total do documento fiscal N - 02 O
09 VL_DESC Valor total do desconto N - 02 OC
10 VL_PIS Valor total do PIS N - 02 OC
11 VL_COFINS Valor total da COFINS N - 02 OC
COD_CTA Código da conta analítica contábil C - - OC
12
debitada/creditada
Observações:
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C350]
Campo 05 (DT_DOC) - Preenchimento: o valor informado deve ser no formato “ddmmaaaa”.
Campo 06 (CNPJ_CPF) - Validação: se forem informados 14 caracteres, o campo será validado como CNPJ. Se forem
informados 11 caracteres, o campo será validado como CPF.
Campo 10 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 11 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração
do registro 0000 estão dispensados do preenchimento deste campo.
----
# REGISTRO C370: ITENS DO DOCUMENTO (CÓDIGO 02)
Este registro é o detalhamento por itens das notas fiscais de venda ao consumidor, modelo 2.
Validação do Registro: A chave deste registro é formada pelos campos NUM_ITEM e COD_ITEM.
Nº Campo Descrição Tipo Tam Dec Entr. Saída
01 REG Texto fixo contendo "C370" C 004 - Não O
Número sequencial do item no documento apresentar O
02 NUM_ITEM N 003 -
fiscal
03 COD_ITEM Código do Item (campo 02 do registro 0200) C 060 - O
04 QTD Quantidade do item N - 3 O
05 UNID Unidade do item (campo 02 do registro 0190) C 006 - O
06 VL_ITEM Valor total do item N - 2 O
07 VL_DESC Valor total do desconto no item N - 2 OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C370]
Campo 02 (NUM_ITEM) - Validação: deve iniciar com “1” e incrementada de “1”.
Campo 03 (COD_ITEM) - Validação: o valor informado neste campo deve existir no registro 0200.
Campo 05 (UNID) - Validação: o valor informado neste campo deve existir no registro 0190.
----
# REGISTRO C380: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE SAÍDA DE
MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CÓDIGO 02)
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C380” C 004 - Não O
apresentar
02 COD_MOT_REST_CO Código do motivo da restituição ou C 005* - O
MPL complementação conforme Tabela 5.7
03 QUANT_CONV Quantidade do item N - 06 O
04 UNID Unidade adotada para informar o campo C 006 - O
QUANT_CONV.
05 VL_UNIT_CONV Valor unitário da mercadoria, considerando a N - 06 O
unidade utilizada para informar o campo
“QUANT_CONV”.
06 VL_UNIT_ICMS_NA_O Valor unitário para o ICMS na operação, caso N - 06 OC
PERACAO_CONV não houvesse a ST, considerando unidade
utilizada para informar o campo
“QUANT_CONV”, aplicando-se a mesma
redução da base de cálculo do ICMS ST na
tributação, se houver.
07 VL_UNIT_ICMS_OP_C Valor unitário do ICMS OP calculado N - 06 OC
ONV conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”,
utilizado para cálculo de
ressarcimento/restituição de ST, no
desfazimento da substituição tributária,
quando se utiliza a fórmula descrita nas
instruções de preenchimento do campo 11, no
item a1).
08 VL_UNIT_ICMS_OP_E Valor médio unitário do ICMS que o N - 06 OC
STOQUE_CONV contribuinte teria se creditado referente à
operação de entrada das mercadorias em
estoque caso estivesse submetida ao regime
comum de tributação, calculado conforme a
legislação de cada UF, considerando a unidade
utilizada para informar o campo
“QUANT_CONV”
09 VL_UNIT_ICMS_ST_ES Valor médio unitário do ICMS ST, incluindo N - 06 OC
TOQUE_CONV FCP ST, das mercadorias em estoque,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
10 VL_UNIT_FCP_ICMS_S Valor médio unitário do FCP ST agregado N - 06 OC
T_ESTOQUE_CONV ao ICMS das mercadorias em estoque,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
11 VL_UNIT_ICMS_ST_C Valor unitário do total do ICMS ST, N - 06 OC
ONV_REST incluindo FCP ST, a ser restituído/ressarcido,
calculado conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
12 VL_UNIT_FCP_ST_CO Valor unitário correspondente à parcela de N - 06 OC
NV_REST ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_REST”,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
13 VL_UNIT_ICMS_ST_C Valor unitário do complemento do ICMS, N - 06 OC
ONV_COMPL incluindo FCP ST, considerando a unidade
utilizada para informar o campo
“QUANT_CONV”.
14 VL_UNIT_FCP_ST_CO Valor unitário correspondente à parcela de N - 06 OC
NV_COMPL ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
15 CST_ICMS Código da Situação Tributária referente ao N 003* - O
ICMS
16 CFOP Código Fiscal de Operação e Prestação N 004* - O
Observação:
Nível hierárquico - 4
Ocorrência 1:1
Campo 01 (REG) - Valor Válido: [C380]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere igual a 0, 1, 2 ou 3.
Se o terceiro caractere do código preenchido no campo “COD_MOT_REST_COMPL” for:
a) igual a 0, os campos 08, 09 e 10 devem ser preenchidos e os campos 06, 07, 11 a 14 não devem ser preenchidos.
b) igual a 1, os campos 06, 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 07, 13 e 14 não devem ser preenchidos.
c) igual a 2, os campos 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 06, 13 e 14 não devem ser preenchidos. O campo
07 pode ser preenchido de acordo com a legislação de cada UF.
d) igual a 3, os campos 06, 08, 09, 10, 13 e 14 devem ser preenchidos e os campos 07, 11 e 12 não devem ser preenchidos.
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: O campo UNID do registro pai não é necessariamente igual ao campo UNID deste
registro. No registro C370, deve corresponder à unidade de medida de comercialização do item utilizada no documento fiscal,
que pode não ser a unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (VL_UNIT_CONV) - Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos
e acréscimos incondicionais aplicados sobre o valor bruto) na unidade utilizada para informar o campo “QUANT_CONV”.
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV) – Preenchimento: Valor correspondente à multiplicação da
alíquota interna (incluindo FCP) (informado no registro 0200) da mercadoria pelo valor correspondente à operação de saída
que seria tributada se não houvesse ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”, aplicando-
se a mesma redução da base de cálculo do ICMS ST na tributação, se houver.
Campo 07 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: Nos casos de direito a crédito do imposto pela não ocorrência
do fato gerador presumido e desfazimento da ST, corresponde ao valor do ICMS da operação própria do sujeito passivo por
substituição do qual a mercadoria tenha sido recebida diretamente ou o valor do ICMS que seria atribuído à operação própria
do contribuinte substituído do qual a mercadoria tenha sido recebida, caso estivesse submetida ao regime comum de tributação,
calculado conforme a legislação de cada UF, considerando unidade utilizada para informar o campo “QUANT_CONV”.
Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor expresso no campo 12
(VL_UNIT_ICMS_OP_ESTOQUE_CONV), seu preenchimento será facultativo. O valor deste campo, quando obrigatório na
UF, será utilizado para o cálculo do valor do ressarcimento/restituição do Campo 15 (VL_UNIT_ICMS_ST_CONV_REST),
conforme fórmula abaixo:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário de ICMS OP, das
mercadorias em estoque.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV) - Preenchimento: Informar o valor médio unitário do ICMS ST,
incluindo FCP ST, pago ou retido, das mercadorias em estoque. Quando a mercadoria estiver sujeita ao FCP adicionado ao
ICMS ST, neste campo deve ser informado o valor médio unitário da parcela do ICMS ST + a parcela do FCP.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 10 (VL_UNIT_FCP_ CONV) - Preenchimento: Informar o valor médio unitário da parcela do FCP adicionado ao
ICMS que tenha sido informado no campo “VL_UNIT_ICMS_ST_ESTOQUE_CONV”.
Campo 11 (VL_UNIT_ICMS_ST_CONV_REST) – Validação: O valor a ser ressarcido / restituído é calculado conforme as
orientações a seguir:
a) Nos casos de direito ao crédito do imposto, por não ocorrência do fato gerador presumido:
a.1) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) for obrigatório, de acordo com a legislação da UF,
correspondente ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
a.2) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) não for obrigatório, de acordo com a legislação da UF,
corresponde ao valor no campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
b) Nos casos de direito ao crédito do imposto, calculada com base no valor de saída da mercadoria inferior ao
valor da BC ICMS ST, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a
unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 12 (VL_UNIT_FCP_ST_CONV_REST) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza
(FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_REST”, considerando a
unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL) –Validação: Nos casos de complemento, informar o valor unitário de
ICMS correspondente ao cálculo a seguir. O valor a ser ressarcido / restituído é calculado conforme as orientações a seguir:
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
- Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
- Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
= Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 14 (VL_UNIT_FCP_ST_CONV_COMPL) – Preenchimento: Informar o valor unitário do Fundo de Combate à
Pobreza (FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando a unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 15 (CST_ICMS) – Preenchimento: o campo deverá ser preenchido com o código da Situação Tributária
correspondente ao informado no documento fiscal.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referenciada no item 4.3.1, da Nota
Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 16 (CFOP) - Preenchimento: informar o código de operação que consta no documento fiscal.7
----
# REGISTRO C390: REGISTRO ANALÍTICO DAS NOTAS FISCAIS DE VENDA A
CONSUMIDOR (CÓDIGO 02)
Este registro tem por objetivo informar as notas fiscais de venda ao consumidor, não emitidas por ECF, e deve ser apresentado de
forma agrupada na combinação CST_ICMS, CFOP e Alíquota de ICMS.
Nº Campo Descrição Tipo Tam Dec Entr. Saída
01 REG Texto fixo contendo "C390" C 004 - Não O
02 CST_ICMS Código da Situação Tributária, conforme a Tabela N 003* - apresentar O
indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação N 004* - O
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
05 VL_OPR Valor total acumulado das operações N - 02 O
correspondentes à combinação de CST_ICMS,
CFOP e alíquota do ICMS, incluídas as despesas
acessórias e acréscimos.
06 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS, N - 02 OC
referente à combinação de CST_ICMS, CFOP, e
alíquota do ICMS.
07 VL_ICMS Valor acumulado do ICMS, referente à N - 02 OC
combinação de CST_ICMS, CFOP e alíquota do
ICMS.
08 VL_RED_BC Valor não tributado em função da redução da base N - 02 OC
de cálculo do ICMS, referente à combinação de
CST_ICMS, CFOP, e alíquota do ICMS.
09 COD_OBS Código da observação do lançamento fiscal (campo C 006 - OC
02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C390]
Campo 02 (CST_ICMS) - Validação: o valor informado neste campo deve existir na Tabela da Situação Tributária referente
ao ICMS, constante do Artigo 5º do Convênio SN/70, sendo que o primeiro caractere sempre será Zero.
Campo 03 (CFOP) – Preenchimento: deve se referir apenas a operações de saídas internas.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01. Não podem ser utilizados os títulos dos agrupamentos de CFOP e os códigos devem ser iniciados por “5”.
----
# REGISTRO C400: EQUIPAMENTO ECF (CÓDIGO 02, 2D e 60)
Este registro tem por objetivo identificar os equipamentos de ECF e deve ser informado por todos os contribuintes que utilizem tais
equipamentos na emissão de documentos fiscais.
Validação do Registro: não podem ser informados dois ou mais registros C400 com a mesma combinação de valores
dos campos COD_MOD, ECF_MOD e ECF_FAB.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C400" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - apresentar O
Tabela 4.1.1
03 ECF_MOD Modelo do equipamento C 020 - O
04 ECF_FAB Número de série de fabricação do ECF C 021 - O
05 ECF_CX Número do caixa atribuído ao ECF N 003 - O
Observações:
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C400]
Campo 02 (COD_MOD) - Valores válidos: [02, 2D, 60] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 05 (ECF_CX) - Preenchimento: informar o número do caixa atribuído, pelo estabelecimento, ao equipamento emissor
de documento fiscal. Um mesmo valor do campo ECF_CX não pode ser usado por dois equipamentos ECF ao mesmo tempo.
Contudo, se o uso de um número for cessado, este mesmo número pode ser atribuído a outro equipamento de ECF, no período.
----
# REGISTRO C405: REDUÇÃO Z (CÓDIGO 02, 2D e 60)
Este registro deve ser apresentado com as informações da Redução Z de cada equipamento em funcionamento na data
das operações de venda à qual se refere a redução. Inclui todos os documentos fiscais totalizados na Redução Z, inclusive as
operações de
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C405" C 004 - Não O
02 DT_DOC Data do movimento a que se refere a Redução Z N 008* - Apresentar O
03 CRO Posição do Contador de Reinício de Operação N 003 - O
04 CRZ Posição do Contador de Redução Z N 006 - O
05 NUM_COO_FI Número do Contador de Ordem de Operação do N 009 - O
N último documento emitido no dia. (Número do
COO na Redução Z)
06 GT_FIN Valor do Grande Total final N - 02 O
07 VL_BRT Valor da venda bruta N - 02 O
Observações: No caso de intervenção técnica no ECF, deve ser informado um registro para cada redução Z emitida.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C405]
Campo 02 (DT_DOC) - Preenchimento: considerar a data do movimento, que inclui as operações de vendas realizadas durante
o período de tolerância do equipamento ECF.
Validação: o valor informado deve ser menor ou igual à DT_FIN deste arquivo.
Campo 03 (CRO) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 04 (CRZ) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 05 (NUM_COO_FIN) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 06 (GT_FIN) - Preenchimento: valor acumulado no totalizador geral final.
Validação: o campo GT_FIN deve ser maior ou igual ao campo VL_BRT, exceto se houver reinício de operação. Quando o
GT_FIN for menor que o VL_BRT será exibida mensagem de “Advertência”.
Campo 07 (VL_BRT) - Preenchimento: valor acumulado no totalizador de venda bruta. Se o valor da venda bruta for igual a
“0” (zero), não devem ser apresentados registros filhos e o registro C490.
Validação: deve ser igual ao somatório do campo VLR_ACUM_TOT do registro C420 para os valores informados no campo
COD_TOT_PAR do registro C420, exceto "AT" (Acréscimo – ICMS), "AS" (Acréscimo – ISSQN), “OPNF” (Operações não
fiscais), “DO” (Desconto Operações não fiscais), “AO” (Acréscimo de operações não fiscais), “Can-O” (Cancelamento de
operações não fiscais) e “IOF” (Imposto Sobre Operações Financeiras).]
----
# REGISTRO C410: PIS E COFINS TOTALIZADOS NO DIA (CÓDIGO 02 e 2D)
Este registro deve ser apresentado sempre que houver produtos totalizados na Redução Z que acarretem valores de
PIS e COFINS a serem informados. Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de
apuração do registro 0000 estão dispensados do preenchimento deste registro.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C410" C 004 - Não O
02 VL_PIS Valor total do PIS N - 02 Apresentar OC
03 VL_COFINS Valor total da COFINS N - 02 OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C410]
----
REGISTRO C420: REGISTRO DOS TOTALIZADORES PARCIAIS DA REDUÇÃO Z (COD 02,
2D e 60)
Este registro tem por objetivo discriminar os valores por código de totalizador da Redução Z.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_TOT_PAR e NR_TOT.
Nº Campo Descrição Tip Tam Dec Entr Saída
o
01 REG Texto fixo contendo "C420" C 004 - Não O
02 COD_TOT_PAR Código do totalizador, conforme Tabela 4.4.6 C 007 - apresentar O
03 VLR_ACUM_TOT Valor acumulado no totalizador, relativo à N - 02 O
respectiva Redução Z.
04 NR_TOT Número do totalizador quando ocorrer mais N 002 - OC
de uma situação com a mesma carga
tributária efetiva.
05 DESCR_NR_TOT Descrição da situação tributária relativa ao C - - OC
totalizador parcial, quando houver mais de um
com a mesma carga tributária efetiva.
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C420]
Campo 02 (COD_TOT_PAR) - Preenchimento: informar o código de totalizador parcial da Redução Z, que deve existir na
Tabela 4.4.6 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações, prevista também na subseção 6.6
deste guia. Deverão ser informados todos os totalizadores parciais da Redução Z, que foram movimentados no dia.
Para totalizadores tributáveis pelo ICMS, o conteúdo deste campo deve ser “Tnnnn” ou “xxTnnnn”, onde “nnnn” corresponde
à alíquota informada no campo ALIQ_ICMS do registro C490. Caso o equipamento ECF seja autorizado a emitir cupom fiscal
com serviço tributado pelo município (ISS), os totalizadores desse serviço também deverão ser informados nesse campo cujo
conteúdo será Snnnn ou xxSnnnn, onde "nnnn" representa a carga tributária efetiva do imposto com duas casas
decimais.Validação: o valor informado deve existir na Tabela 4.4.6 , que discrimina os códigos dos Totalizadores Parciais da
REDUÇÃO Z.
Campo 03 (VLR_ACUM_TOT) - Preenchimento: informar o valor acumulado no totalizador (venda líquida) da situação
tributária/alíquota. Validação: o valor deste campo deve ser igual à soma dos campos VL_OPER dos registros C490, para os
totalizadores tributáveis pelo ICMS e/ou ISS, indicado pelo campo COD_TOT_PAR com valor igual a “xxTnnnn” , “Tnnnn”,
xxSnnnn e Snnnn.
Se o declarante estiver enquadrado no Perfil B, o conteúdo deste campo deve ser igual à soma do campo VL_ITEM dos registros
C425.
Para os totalizadores OPNF, DO, AO, Can-T, Can-S e Can-O, não informar o registro C490.
Campo 04 (NR_TOT) - Validação: o valor “xx”, do formato “xxTnnnn” ou “xxSnnnn”, conforme Convênio 80/07, para
código de totalizador tributável pelo ICMS e/ou ISS, deve ser informado no campo NR_TOT deste registro. Da mesma forma,
este campo deve ser preenchido quando ocorrer cargas tributárias efetivas idênticas. Existindo apenas um totalizador, informar
1Tnnnn. O valor informado deve ser maior que “0” (zero). Ex: T1700 com NR_TOT igual a “1”(carga tributária de 17%);
T1700 com NR_TOT igual a 2 (carga tributária efetiva de 17% decorrente de redução de base de cálculo).
Campo 05 (DESCR_NR_TOT) - Validação: Só deve ser informado, se o campo NR_TOT estiver preenchido.
----
# REGISTRO C425: RESUMO DE ITENS DO MOVIMENTO DIÁRIO (CÓDIGO 02 e 2D)
Este registro tem por objetivo identificar os produtos comercializados na data da movimentação relativa à Redução Z
informada, sendo obrigatório, quando os totalizadores forem iguais a xxTnnnn, Tnnnn, Fn, In, Nn.
Validação do Registro: não podem ser informados dois ou mais registros com o mesmo valor para o campo
COD_ITEM para cada C420. É obrigatória a apresentação deste registro, se o valor no campo COD_TOT_PAR do registro
C420 for Tnnnn, xxTnnnn, Fn, In ou Nn.
Este registro não deverá ser informado quando o campo 02 do Registro C420 for igual a OPNF, Can-T, Can-S e Can-
O.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C425" C 004 - Não O
02 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - apresentar O
03 QTD Quantidade acumulada do item N - 03 O
04 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
05 VL_ITEM Valor acumulado do item N - 02 O
06 VL_PIS Valor do PIS N - 02 OC
07 VL_COFINS Valor da COFINS N - 02 OC
Observações:
Nível hierárquico - 5
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C425]
Campo 03 (QTD) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Validação:
a) o valor deve ser informado no registro 0190.
b) Caso a unidade de medida do documento fiscal seja diferente da unidade de medida de controle de estoque informada no
Registro 0200, o valor informado deve existir no registro 0220 para o código do item (Campo 03 -COD_ITEM desse registro)
com a correspondente conversão.
Campo 05 (VL_ITEM) - Validação: o valor informado no campo deve ser maior que “0” (zero) e corresponder ao somatório
dos valores líquidos de cada produto.
Campo 06 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 07 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C430: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE SAÍDA DE
MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CÓDIGO 02, 2D e 60)
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte
Nº Campo Descrição Tip Tam Dec Entr Saída
o
01 REG Texto fixo contendo "C430” C 004 - Não O
apresentar
02 COD_MOT_REST_COMP Código do motivo da restituição ou C 005* - O
L complementação conforme Tabela 5.7
03 QUANT_CONV Quantidade do item N - 06 O
04 UNID Unidade adotada para informar o campo C 006 - O
QUANT_CONV.
05 VL_UNIT_CONV Valor unitário da mercadoria, considerando a N - 06 O
unidade utilizada para informar o campo
“QUANT_CONV”.
06 VL_UNIT_ICMS_NA_OPE Valor unitário para o ICMS na operação, caso N - 06 OC
RACAO_CONV não houvesse a ST, considerando unidade
utilizada para informar o campo
“QUANT_CONV”, considerando redução da
base de cálculo do ICMS ST na tributação, se
houver.
07 VL_UNIT_ICMS_OP_CO Valor unitário do ICMS OP calculado N - 06 OC
NV conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”,
utilizado para cálculo de
ressarcimento/restituição de ST, no
desfazimento da substituição tributária,
quando se utiliza a fórmula descrita nas
instruções de preenchimento do campo 11, no
item a1).
08 VL_UNIT_ICMS_OP_EST Valor médio unitário do ICMS que o N - 06 OC
OQUE_CONV contribuinte teria se creditado referente à
operação de entrada das mercadorias em
estoque caso estivesse submetida ao regime
comum de tributação, calculado conforme a
legislação de cada UF, considerando a unidade
utilizada para informar o campo
“QUANT_CONV”
09 VL_UNIT_ICMS_ST_EST Valor médio unitário do ICMS ST, incluindo N - 06 OC
OQUE_CONV FCP ST, das mercadorias em estoque,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
10 VL_UNIT_FCP_ICMS_ST Valor médio unitário do FCP ST agregado N - 06 OC
_ESTOQUE_CONV ao ICMS das mercadorias em estoque,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
11 VL_UNIT_ICMS_ST_CON Valor unitário do total do ICMS ST, incluindo N - 06 OC
V_REST FCP ST, a ser restituído/ressarcido, calculado
conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
12 VL_UNIT_FCP_ST_CONV Valor unitário correspondente à parcela de N - 06 OC
_REST ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_REST”,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
13 VL_UNIT_ICMS_ST_CON Valor unitário do complemento do ICMS, N - 06 OC
V_COMPL incluindo FCP ST, considerando a unidade
utilizada para informar o campo
“QUANT_CONV”.
14 VL_UNIT_FCP_ST_CONV Valor unitário correspondente à parcela de N - 06 OC
_COMPL ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
15 CST_ICMS Código da Situação Tributária referente ao N 003* - O
ICMS
16 CFOP Código Fiscal de Operação e Prestação N 004* - O
Observação:
Nível hierárquico - 6
Ocorrência 1:N
Campo 01 (REG) - Valor Válido: [C430]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere igual a 0, 1, 2 ou 3.
Se o terceiro caractere do código preenchido no campo “COD_MOT_REST_COMPL” for:
a) igual a 0, os campos 08, 09 e 10 devem ser preenchidos e os campos 06, 07, 11 a 14 não devem ser preenchidos.
b) igual a 1, os campos 06, 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 07, 13 e 14 não devem ser preenchidos.
c) igual a 2, os campos 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 06, 13 e 14 não devem ser preenchidos. O campo
07 pode ser preenchido de acordo com a legislação de cada UF.
d) igual a 3, os campos 06, 08, 09, 10, 13 e 14 devem ser preenchidos e os campos 07, 11 e 12 não devem ser preenchidos.
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: O campo UNID do registro pai não é necessariamente igual ao campo UNID deste
registro. No registro C425, deve corresponder à unidade de medida de comercialização do item utilizada no documento fiscal,
que pode não ser a unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (VL_UNIT_CONV) - Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos
e acréscimos incondicionais aplicados sobre o valor bruto) na unidade utilizada para informar o campo “QUANT_CONV”.
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV) – Preenchimento: Valor correspondente à multiplicação da
alíquota interna (incluindo FCP) (informado no registro 0200) da mercadoria pelo valor correspondente à operação de saída
que seria tributada se não houvesse ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”, aplicando-
se a mesma redução da base de cálculo do ICMS ST na tributação, se houver.
Campo 07 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: Nos casos de direito a crédito do imposto pela não ocorrência
do fato gerador presumido e desfazimento da ST, corresponde ao valor do ICMS da operação própria do sujeito passivo por
substituição do qual a mercadoria tenha sido recebida diretamente ou o valor do ICMS que seria atribuído à operação própria
do contribuinte substituído do qual a mercadoria tenha sido recebida, caso estivesse submetida ao regime comum de tributação,
calculado conforme a legislação de cada UF, considerando unidade utilizada para informar o campo “QUANT_CONV”.
Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor expresso no campo 12
(VL_UNIT_ICMS_OP_ESTOQUE_CONV), seu preenchimento será facultativo. O valor deste campo, quando obrigatório na
UF, será utilizado para o cálculo do valor do ressarcimento/restituição do Campo 15 (VL_UNIT_ICMS_ST_CONV_REST),
conforme fórmula abaixo:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário de ICMS OP, das
mercadorias em estoque.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV) - Preenchimento: Informar o valor médio unitário do ICMS ST,
incluindo FCP ST, pago ou retido, das mercadorias em estoque. Quando a mercadoria estiver sujeita ao FCP adicionado ao
ICMS ST, neste campo deve ser informado o valor médio unitário da parcela do ICMS ST + a parcela do FCP.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc
Campo 10 (VL_UNIT_FCP_ CONV) - Preenchimento: Informar o valor médio unitário da parcela do FCP adicionado ao
ICMS que tenha sido informado no campo “VL_UNIT_ICMS_ST_ESTOQUE_CONV”.
Campo 11 (VL_UNIT_ICMS_ST_CONV_REST) – Validação: O valor a ser ressarcido / restituído é calculado conforme as
orientações a seguir:
a) Nos casos de direito ao crédito do imposto, por não ocorrência do fato gerador presumido:
a.1) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) for obrigatório, de acordo com a legislação da UF, correspondente
ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
a.2) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) não for obrigatório, de acordo com a legislação da UF,
corresponde ao valor no campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
b) Nos casos de direito ao crédito do imposto, calculada com base no valor de saída da mercadoria inferior ao
valor da BC ICMS ST, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a
unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 12 (VL_UNIT_FCP_ST_CONV_REST) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza
(FCP) vinculado à substituição tributária que compõe o campo “ VL_UNIT_ICMS_ST_CONV_REST”, considerando a
unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL) – Validação: Nos casos de complemento, informar o valor unitário de
ICMS correspondente ao cálculo a seguir. O valor a ser ressarcido / restituído é calculado conforme as orientações a seguir:
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
- Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
- Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
= Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 14 (VL_UNIT_FCP_ST_CONV_COMPL) – Preenchimento: Informar o valor unitário do Fundo de Combate à
Pobreza (FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando a unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 15 (CST_ICMS) – Preenchimento: o campo deverá ser preenchido com o código da Situação Tributária
correspondente ao informado no documento fiscal.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referenciada no item 4.3.1, da Nota
Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 16 (CFOP) - Preenchimento: informar o código de operação que consta no documento fiscal. O código CFOP deve
iniciar-se por “5”
----
# REGISTRO C460: DOCUMENTO FISCAL EMITIDO POR ECF (CÓDIGO 02, 2D e 60)
Este registro deve ser apresentado para a identificação dos documentos fiscais emitidos pelos usuários de
equipamentos ECF, que foram totalizados na Redução Z.
Para cupom fiscal cancelado, informar somente os campos COD_MOD, COD_SIT e NUM_DOC, sem os registros
filhos.
Obs.: Os CNPJ e CPF citados neste registro NÃO devem ser informados no registro 0150.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_MOD, NUM_DOC e DT_DOC.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C460" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, conforme a C 002* - apresentar O
Tabela 4.1.1
03 COD_SIT Código da situação do documento fiscal, conforme a N 002* - O
Tabela 4.1.2
04 NUM_DOC Número do documento fiscal (COO) N 009 - O
05 DT_DOC Data da emissão do documento fiscal N 008* - O
06 VL_DOC Valor total do documento fiscal N - 02 O
07 VL_PIS Valor do PIS N - 02 OC
08 VL_COFINS Valor da COFINS N - 02 OC
09 CPF_CNPJ CPF ou CNPJ do adquirente N 014 - OC
10 NOM_ADQ Nome do adquirente C 060 - OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C460]
Campo 02 (COD_MOD) - Valores Válidos: [02, 2D, 60] - – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 03 (COD_SIT) - Valores Válidos: [00, 01, 02]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3.Validação: se o valor neste campo for igual
a 02, informar somente os campos REG, COD_MOD, NUM_DOC, e não deve ser apresentado o registro C470.
Campo 04 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 05 (DT_DOC) - Preenchimento: em casos excepcionais, conforme Convênio 85/01, a data de emissão do documento
fiscal pode ser imediatamente posterior à data de movimentação relativa à Redução Z, em decorrência do período de duas horas
de tolerância dos equipamentos de ECF.
Campo 06 (VL_DOC) - Validação: o valor informado deve ser maior que “0” (zero). O valor informado deve ser igual à soma
do campo VL_ITEM dos registros C470.
Campo 07 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 08 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 09 (CPF_CNPJ) - Preenchimento: informar o CNPJ, com 14 dígitos, ou o CPF, com 11 dígitos, do adquirente.
Validação: se forem informados 14 caracteres, o campo será validado como CNPJ. Se forem informados 11 caracteres, o
campo será validado como CPF. O preenchimento com outra quantidade de caracteres será considerado inválido.
REGISTRO C465: COMPLEMENTO DO CUPOM FISCAL ELETRÔNICO EMITIDO POR
ECF – CF-e-ECF (CÓDIGO 60)
Este registro deve ser apresentado para a identificação adicional dos cupons fiscais eletrônicos emitidos pelos usuários de
equipamentos ECF, que foram totalizados na Redução Z.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C465" C 004 - Não O
02 CHV_CFE Chave do Cupom Fiscal Eletrônico N 044 - apresentar O
03 NUM_CCF Número do Contador de Cupom Fiscal N 009 - O
Observações:
Nível hierárquico - 5
Ocorrência - 1:1
Campo 01 (REG) – Valor Válido: [C465]
Campo 02 (CHV_CFE) – Validação: é conferido o dígito verificador (DV) da chave do Cupom Fiscal Eletrônico.
Campo 03 (NUM_CCF) – Validação: campo deve ser maior que zero.
----
# REGISTRO C470: ITENS DO DOCUMENTO FISCAL EMITIDO POR ECF (CÓDIGO 02 e 2D)
Este registro deve ser apresentado para informar os itens dos documentos fiscais emitidos pelos usuários de
equipamentos ECF, que foram totalizados na Redução Z. O serviço de competência municipal (sujeito ao ISSQN) também
deverá ser informado nesse registro. Para tanto, deverá ser criado o correspondente item no registro 0200, cujo conteúdo do
campo TIPO_ITEM será igual “09” (Serviços). Não informar o registro para o item cuja venda foi totalmente cancelada.
Não informar este registro no caso de Cupom Fiscal Eletrônico emitido por ECF - CF-e-ECF (Código 60).
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C470" C 004 - Não O
02 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - apresentar O
03 QTD Quantidade do item N - 03 O
04 QTD_CANC Quantidade cancelada, no caso de cancelamento N - 03 OC
parcial de item
05 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
06 VL_ITEM Valor total do item N - 02 O
07 CST_ICMS Código da Situação Tributária, conforme a Tabela N 003* - O
indicada no item 4.3.1.
08 CFOP Código Fiscal de Operação e Prestação N 004* - O
09 ALIQ_ICMS Alíquota do ICMS – Carga tributária efetiva em N 006 02 OC
percentual
10 VL_PIS Valor do PIS N - 02 OC
11 VL_COFINS Valor da COFINS N - 02 OC
Observações:
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C470]
Campo 03 (QTD) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 04 (QTD_CANC) - Validação: o valor do campo deve ser menor que o valor do campo QTD.
Campo 05 (UNID) - Validação: o valor deve ser informado no registro 0190.
Campo 06 (VL_ITEM) - Validação: o valor informado deve ser maior que “0” (zero) e corresponder ao valor líquido do item
no cupom.
Campo 07 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária do ICMS
referenciada no item 4.3.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 08 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01. O código CFOP deve iniciar-se por “5”.
Campo 09 (ALIQ_ICMS) – Preenchimento: informar a carga tributária efetiva em percentual com dois decimais.
Campo 10 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 11 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C480: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE SAÍDA DE
MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CÓDIGO 02, 2D e 60)
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C480” C 004 - Não O
apresentar
02 COD_MOT_REST_C Código do motivo da restituição ou C 005* - O
OMPL complementação conforme Tabela 5.7
03 QUANT_CONV Quantidade do item N - 06 O
04 UNID Unidade adotada para informar o campo C 006 - O
QUANT_CONV.
05 VL_UNIT_CONV Valor unitário da mercadoria, considerando a N - 06 O
unidade utilizada para informar o campo
“QUANT_CONV”.
06 VL_UNIT_ICMS_NA Valor unitário para o ICMS na operação, caso N - 06 OC
_OPERACAO_CONV não houvesse a ST, considerando unidade
utilizada para informar o campo
“QUANT_CONV”, aplicando-se a mesma
redução da base de cálculo do ICMS ST na
tributação, se houver.
07 VL_UNIT_ICMS_OP Valor unitário do ICMS OP calculado N - 06 OC
_CONV conforme a legislação de cada UF,
considerando a unidade utilizada para informar
o campo “QUANT_CONV”, utilizado para
cálculo de ressarcimento/restituição de ST, no
desfazimento da substituição tributária,
quando se utiliza a fórmula descrita nas
instruções de preenchimento do campo 11, no
item a1).
08 VL_UNIT_ICMS_OP Valor médio unitário do ICMS que o N - 06 OC
_ESTOQUE_CONV contribuinte teria se creditado referente à
operação de entrada das mercadorias em
estoque caso estivesse submetida ao regime
comum de tributação, calculado conforme a
legislação de cada UF, considerando a unidade
utilizada para informar o campo
“QUANT_CONV”
09 VL_UNIT_ICMS_ST_ Valor médio unitário do ICMS ST, incluindo N - 06 OC
ESTOQUE_CONV FCP ST, das mercadorias em estoque,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
10 VL_UNIT_FCP_ICM Valor médio unitário do FCP ST agregado N - 06 OC
S_ST_ESTOQUE_CO ao ICMS das mercadorias em estoque,
NV considerando unidade utilizada para informar
o campo “QUANT_CONV”.
11 VL_UNIT_ICMS_ST_ Valor unitário do total do ICMS ST, incluindo N - 06 OC
CONV_REST FCP ST, a ser restituído/ressarcido, calculado
conforme a legislação de cada UF,
considerando a unidade utilizada para informar
o campo “QUANT_CONV”.
12 VL_UNIT_FCP_ST_C Valor unitário correspondente à parcela de N - 06 OC
ONV_REST ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_REST”,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
13 VL_UNIT_ICMS_ST_ Valor unitário do complemento do ICMS, N - 06 OC
CONV_COMPL incluindo FCP ST, considerando a unidade
utilizada para informar o campo
“QUANT_CONV”.
14 VL_UNIT_FCP_ST_C Valor unitário correspondente à parcela de N - 06 OC
ONV_COMPL ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando unidade utilizada para informar
o campo “QUANT_CONV”.
15 CST_ICMS Código da Situação Tributária referente ao N 003* - O
ICMS
16 CFOP Código Fiscal de Operação e Prestação N 004* - O
Observação:
Nível hierárquico - 6
Ocorrência 1:1
Campo 01 (REG) - Valor Válido: [C480]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere igual a 0, 1, 2 ou 3.
Se o terceiro caractere do código preenchido no campo “COD_MOT_REST_COMPL” for:
a) igual a 0, os campos 08, 09 e 10 devem ser preenchidos e os campos 06, 07, 11 a 14 não devem ser preenchidos.
b) igual a 1, os campos 06, 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 07, 13 e 14 não devem ser preenchidos.
c) igual a 2, os campos 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 06, 13 e 14 não devem ser preenchidos. O campo
07 pode ser preenchido de acordo com a legislação de cada UF.
d) igual a 3, os campos 06, 08, 09, 10, 13 e 14 devem ser preenchidos e os campos 07, 11 e 12 não devem ser preenchidos.
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: O campo UNID do registro pai não é necessariamente igual ao campo UNID deste
registro. No registro C470, deve corresponder à unidade de medida de comercialização do item utilizada no documento fiscal,
que pode não ser a unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (VL_UNIT_CONV) - Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos
e acréscimos incondicionais aplicados sobre o valor bruto) na unidade utilizada para informar o campo “QUANT_CONV”.
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV) – Preenchimento: Valor correspondente à multiplicação da
alíquota interna (incluindo FCP) (informado no registro 0200) da mercadoria pelo valor correspondente à operação de saída
que seria tributada se não houvesse ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”, aplicando-
se a mesma redução da base de cálculo do ICMS ST na tributação, se houver.
Campo 07 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: Nos casos de direito a crédito do imposto pela não ocorrência
do fato gerador presumido e desfazimento da ST, corresponde ao valor do ICMS da operação própria do sujeito passivo por
substituição do qual a mercadoria tenha sido recebida diretamente ou o valor do ICMS que seria atribuído à operação própria
do contribuinte substituído do qual a mercadoria tenha sido recebida, caso estivesse submetida ao regime comum de tributação,
calculado conforme a legislação de cada UF, considerando unidade utilizada para informar o campo “QUANT_CONV”.
Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor expresso no campo 12
(VL_UNIT_ICMS_OP_ESTOQUE_CONV), seu preenchimento será facultativo. O valor deste campo, quando obrigatório na
UF, será utilizado para o cálculo do valor do ressarcimento/restituição do Campo 15 (VL_UNIT_ICMS_ST_CONV_REST),
conforme fórmula abaixo:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário de ICMS OP, das
mercadorias em estoque.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV) - Preenchimento: Informar o valor médio unitário do ICMS ST,
incluindo FCP ST, pago ou retido, das mercadorias em estoque. Quando a mercadoria estiver sujeita ao FCP adicionado ao
ICMS ST, neste campo deve ser informado o valor médio unitário da parcela do ICMS ST + a parcela do FCP.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 10 (VL_UNIT_FCP_ CONV) - Preenchimento: Informar o valor médio unitário da parcela do FCP adicionado ao
ICMS que tenha sido informado no campo “VL_UNIT_ICMS_ST_ESTOQUE_CONV”.
Campo 11 (VL_UNIT_ICMS_ST_CONV_REST) – Validação: O valor a ser ressarcido / restituído é calculado conforme as
orientações a seguir:
a) Nos casos de direito ao crédito do imposto, por não ocorrência do fato gerador presumido:
a.1) Quando o campo 11 (VL_UNIT_ICMS_OP_CONV) for obrigatório, de acordo com a legislação da UF, correspondente
ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
a.2) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) não for obrigatório, de acordo com a legislação da UF,
corresponde ao valor no campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
b) Nos casos de direito ao crédito do imposto, calculada com base no valor de saída da mercadoria inferior ao
valor da BC ICMS ST, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a
unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 12 (VL_UNIT_FCP_ST_CONV_REST) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza
(FCP) vinculado à substituição tributária que compõe o campo “ VL_UNIT_ICMS_ST_CONV_REST”, considerando a
unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL) – Validação: Nos casos de complemento, informar o valor unitário de
ICMS correspondente ao cálculo a seguir. O valor a ser ressarcido / restituído é calculado conforme as orientações a seguir:
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
- Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
- Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
= Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 14 (VL_UNIT_FCP_ST_CONV_COMPL) – Preenchimento: Informar o valor unitário do Fundo de Combate à
Pobreza (FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando a unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 15 (CST_ICMS) – Preenchimento: o campo deverá ser preenchido com o código da Situação Tributária
correspondente ao informado no documento fiscal.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referenciada no item 4.3.1, da Nota
Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 16 (CFOP) - Preenchimento: informar o código de operação que consta no documento fiscal. O código CFOP deve
iniciar-se por “5”
----
# REGISTRO C490: REGISTRO ANALÍTICO DO MOVIMENTO DIÁRIO (CÓDIGO 02, 2D e 60)
Este registro tem por objetivo representar a escrituração dos documentos fiscais emitidos por ECF e totalizados pela
combinação de CST, CFOP e Alíquota. Não informar este registro para os totalizadores OPNF, DO, AO, Can-T, Can-S e Can-
O informados no C420.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS. A combinação CST_ICMS, CFOP e ALIQ_ICMS deve existir no respectivo
registro de itens do C470, quando este registro for exigido.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C490" C 004 - Não O
02 CST_ICMS Código da Situação Tributária, conforme a N 003* - apresentar O
Tabela indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação N 004* - O
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
05 VL_OPR Valor da operação correspondente à combinação N - 02 O
de CST_ICMS, CFOP, e alíquota do ICMS,
incluídas as despesas acessórias e acréscimos
06 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS, N - 02 O
referente à combinação de CST_ICMS, CFOP, e
alíquota do ICMS.
07 VL_ICMS Valor acumulado do ICMS, referente à N - 02 O
combinação de CST_ICMS, CFOP e alíquota do
ICMS.
08 COD_OBS Código da observação do lançamento fiscal C 006 - OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C490]
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária do ICMS,
referenciada no item 4.3.1da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
ICMS Normal: a) se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero); b) se os dois últimos dígitos deste campo forem
diferentes de 30, 40, 41, 50, e 60, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores
que “0” (zero); c) se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores ou iguais a “0” (zero).
Campo 03 (CFOP) – Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01. O código CFOP deve iniciar-se por “5”.
Campo 04 (ALIQ_ICMS) – Preenchimento: informar a carga tributária efetiva da operação.
Campo 05 (VL_OPR) - Preenchimento: valor líquido da operação, incluídas as despesas acessórias e acréscimos, excluídos
os descontos incondicionais.
Campo 06 (VL_BC_ICMS) - Validação: se o campo IND_PERFIL do registro 0000 for igual a “A”, o valor deste campo deve
ser igual à soma do campo VL_ITEM dos registros C470 que possuam a mesma combinação de valores para os campos
CST_ICMS, CFOP e ALIQ_ICMS deste registro.
Campo 07 (VL_ICMS) - Validação: O valor do ICMS corresponde ao resultado da multiplicação da carga tributária efetiva
pelo valor da base de cálculo.
----
# REGISTRO C495: RESUMO MENSAL DE ITENS DO ECF POR ESTABELECIMENTO
(CÓDIGO 02 e 2D)
Este registro deve ser apresentado pelo contribuinte domiciliado no estado da Bahia até 31/12/2013, resumindo todas
as informações num único registro por item de mercadorias, não dispensando a apresentação do registro C400 e registros filhos.
A partir de 01/01/2014, os contribuintes situados na Bahia não apresentam este registro e devem apresentar o registro C425.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_ITEM e ALIQ_ICMS.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C495" C 004 - Não O
02 ALIQ_ICMS Alíquota do ICMS N 006 02 apresentar OC
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
04 QTD Quantidade acumulada do item N - 03 O
05 QTD_CANC Quantidade cancelada acumulada, no caso de N - 03 OC
cancelamento parcial de item
06 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
07 VL_ITEM Valor acumulado do item N - 02 O
08 VL_DESC Valor acumulado dos descontos N - 02 OC
09 VL_CANC Valor acumulado dos cancelamentos N - 02 OC
10 VL_ACMO Valor acumulado dos acréscimos N - 02 OC
11 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS N - 02 OC
12 VL_ICMS Valor acumulado do ICMS N - 02 OC
13 VL_ISEN Valor das saídas isentas do ICMS N - 02 OC
14 VL_NT Valor das saídas sob não-incidência ou não- N - 02 OC
tributadas pelo ICMS
15 VL_ICMS_ST Valor das saídas de mercadorias adquiridas com N - 02 OC
substituição tributária do ICMS
Observações:
Nível hierárquico - 2
Ocorrência - vários
Campo 01 (REG) - Valor Válido: [C495]
Campo 02 (ALIQ_ICMS) – Preenchimento: informar a carga tributária efetiva da operação.
Campo 03 (COD_ITEM) - Validação: o valor informado no campo deve existir no registro 0200, Campo COD_ITEM.
Campo 04 (QTD) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 05 (QTD_CANC) - Preenchimento: informar a quantidade acumulada cancelada, no caso de cancelamento parcial de
item.
Campo 06 (UNID) - Validação: o valor deve ser informado no registro 0190.
Campo 07 (VL_ITEM) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
# REGISTRO C500: NOTA FISCAL/CONTA DE ENERGIA ELÉTRICA (CÓDIGO 06), NOTA
FISCAL DE ENERGIA ELÉTRICA ELETRÔNICA – NF3e (CÓDIGO 66), NOTA
FISCAL/CONTA DE FORNECIMENTO D'ÁGUA CANALIZADA (CÓDIGO 29) E NOTA
FISCAL CONSUMO FORNECIMENTO DE GÁS (CÓDIGO 28).
Este registro deve ser apresentado, nas operações de saída, pelos contribuintes do segmento de energia elétrica e não
obrigados ao Convênio ICMS 115/03, pelos contribuintes do segmento de fornecimento de gás e, nas operações de entrada, por
todos os contribuintes adquirentes.
A partir de janeiro de 2020, deve ser apresentado também pelos contribuintes que emitirem a NF3e (modelo 66),
mesmo que obrigados ao Convênio 115/03.
IMPORTANTE: para documentos de entrada, os campos de valor de imposto, base de cálculo e alíquota só devem
ser informados se o adquirente tiver direito à apropriação do crédito (enfoque do declarante).
A NF3e que contenha apenas itens sem a indicação de Código de Situação Tributária – CST não deve ser escriturada.
Nas emissões de documentos para cada registro C500, obrigatoriamente devem ser apresentados, pelo menos, um
registro C510 e um registro C590, observadas as exceções abaixo relacionadas:
Exceção 1: Para documentos com código de situação (campo COD_SIT) cancelado (código “02”) ou cancelado extemporâneo
(código “03”), preencher somente os campos REG, IND_OPER, IND_EMIT, COD_MOD, COD_SIT, SER, NUM_DOC e
DT_DOC. A partir de 01/01/2020, se o campo COD_MOD for igual a ”66” o campo CHV_DOCe é obrigatório. Demais
campos deverão ser apresentados com conteúdo VAZIO “||”. Para esse documento não poderá ser apresentado nenhum registro
“filho”.
Exceção 2: Notas Fiscais de Energia Elétrica Eletrônicas (NF3e) de emissão própria não devem ter registros C510.
Exceção 3: Notas Fiscais Complementares e Notas Fiscais Complementares Extemporâneas (campo COD_SIT igual a “06” ou
“07”): nesta situação, somente os campos (do registro C500) REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD,
COD_SIT, SER, NUM_DOC e DT_DOC são obrigatórios. Os demais campos são facultativos (se forem preenchidos, serão
validados e aplicadas as regras de campos existentes). O registro C590 é obrigatório e deverá ser observada a obrigatoriedade
de preenchimento de todos os campos. Os demais campos e registros filhos do registro C500 deverão ser informados, se
existirem.
Exceção 4: Notas Fiscais emitidas por regime especial ou norma específica (campo COD_SIT igual a “08”). Para documentos
fiscais emitidos com base em regime especial ou norma específica, deverão ser apresentados os registros C500 e C590,
obrigatoriamente, e os demais registros “filhos”, se estes forem exigidos pela legislação fiscal. Nesta situação, somente os
campos (do registro C500) REG, IND_OPER, IND_EMIT, COD_PART, COD_MOD, COD_SIT, SER, NUM_DOC e
DT_DOC são obrigatórios. A partir de 01/01/2020, se o campo COD_MOD for igual a ”66” o campo CHV_DOCe é
obrigatório. Os demais campos são facultativos (se forem preenchidos, serão validados e aplicadas as regras de campos
existentes). No registro C590, exceto o campo ALIQ_ICMS que é facultativo, preencher os demais campos obrigatoriamente.
Exceção 5: Notas Fiscais de Energia Elétrica Eletrônicas (NF3e) de saída de emissão de terceiros: os casos de escrituração em
operações de saída de documentos fiscais eletrônicos emitidos por terceiros (como por exemplo, o consórcio constituído nos
termos do disposto nos arts. 278 e 279 da Lei nº 6.404, de 15 de dezembro de 1976), devem ser informados com o código de
situação do documento igual a “08 - Documento Fiscal emitido com base em Regime Especial ou Norma Específica”. O PVA-
EFD-ICMS/IPI exibirá a mensagem de advertência para esses documentos.
Obs.: Os documentos fiscais emitidos pelas filiais das empresas que possuam inscrição estadual única ou sejam autorizadas
pelos fiscos estaduais a centralizarem suas escriturações fiscais deverão ser informados como sendo de emissão própria e código
de situação igual a “00 – Documento regular”.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos IND_OPER, IND_EMIT, COD_PART, SER, SUB, NUM_DOC e DT_DOC. A partir de 01/01/2020 fica incluído o
campo CHV_DOCe.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C500" C 004 - O O
02 IND_OPER Indicador do tipo de operação: C 001* - O O
0 - Entrada;
1 - Saída
03 IND_EMIT Indicador do emitente do documento C 001* - O O
fiscal:
0 - Emissão própria;
1 - Terceiros
04 COD_PART Código do participante (campo 02 do C 060 - O O
Registro 0150):
- do adquirente, no caso das saídas;
- do fornecedor no caso de entradas
05 COD_MOD Código do modelo do documento fiscal, C 002* - O O
conforme a Tabela 4.1.1
06 COD_SIT Código da situação do documento fiscal, N 002* - O O
conforme a Tabela 4.1.2
07 SER Série do documento fiscal C 004 - OC OC
08 SUB Subsérie do documento fiscal N 003 - OC OC
09 COD_CONS - Código de classe de consumo de energia C 002* - OC OC
elétrica ou gás:
01 - Comercial
02 - Consumo Próprio
03 - Iluminação Pública
04 - Industrial
05 - Poder Público
06 - Residencial
07 - Rural
08 - Serviço Público.
- Código de classe de consumo de
Fornecimento D´água – Tabela 4.4.2.
10 NUM_DOC Número do documento fiscal N 009 - O O
11 DT_DOC Data da emissão do documento fiscal N 008* - O O
12 DT_E_S Data da entrada ou da saída N 008* - O O
13 VL_DOC Valor total do documento fiscal N - 02 O O
14 VL_DESC Valor total do desconto N - 02 OC OC
15 VL_FORN Valor total fornecido/consumido N - 02 O O
16 VL_SERV_NT Valor total dos serviços não-tributados N - 02 OC OC
pelo ICMS
17 VL_TERC Valor total cobrado em nome de terceiros N - 02 OC OC
18 VL_DA Valor total de despesas acessórias N - 02 OC OC
indicadas no documento fiscal
19 VL_BC_ICMS Valor acumulado da base de cálculo do N - 02 OC OC
ICMS
20 VL_ICMS Valor acumulado do ICMS N - 02 OC OC
21 VL_BC_ICMS_ST Valor acumulado da base de cálculo do N - 02 OC OC
ICMS substituição tributária
22 VL_ICMS_ST Valor acumulado do ICMS retido por N - 02 OC OC
substituição tributária
23 COD_INF Código da informação complementar do C 006 - OC OC
documento fiscal (campo 02 do Registro
0450)
24 VL_PIS Valor do PIS N - 02 OC OC
25 VL_COFINS Valor da COFINS N - 02 OC OC
26 TP LIGACAO Código de tipo de Ligação N 001* - OC OC
1 - Monofásico
2 - Bifásico
3 - Trifásico
27 COD_GRUPO_TENSAO Código de grupo de tensão: C 002* - OC OC
01 - A1 - Alta Tensão (230kV ou mais)
02 - A2 - Alta Tensão (88 a 138kV)
03 - A3 - Alta Tensão (69kV)
04 - A3a - Alta Tensão (30kV a 44kV)
05 - A4 - Alta Tensão (2,3kV a 25kV)
06 - AS - Alta Tensão Subterrâneo 06
07 - B1 - Residencial 07
08 - B1 - Residencial Baixa Renda 08
09 - B2 - Rural 09
10 - B2 - Cooperativa de Eletrificação
Rural
11 - B2 - Serviço Público de Irrigação
12 - B3 - Demais Classes
13 - B4a - Iluminação Pública - rede de
distribuição
14 - B4b - Iluminação Pública - bulbo de
lâmpada
CHV_DOCe Chave da Nota Fiscal de Energia Elétrica
28 Eletrônica N 044* - OC OC
FIN_DOCe Finalidade da emissão do documento
29 eletrônico: N 001* - OC OC
1 – Normal
2 – Substituição
3 – Normal com ajuste
CHV_DOCe_REF Chave da nota referenciada.
30 N 044* - OC OC
IND_DEST Indicador do Destinatário/Acessante:
31 1 – Contribuinte do ICMS; N 001* - N O
2 – Contribuinte Isento de Inscrição no
Cadastro de Contribuintes do ICMS;
9 – Não Contribuinte.
COD_MUN_DEST Código do município do destinatário
32 conforme a tabela do IBGE. N 007* - N O
COD_CTA Código da conta analítica contábil
33 debitada/creditada C - - OC OC
34 COD_MOD_DOC_REF Código do modelo do documento fiscal N 002* - OC OC
referenciado, conforme a Tabela 4.1.1
35 HASH_DOC_REF Código de autenticação digital do registro C 32 - OC OC
(Convênio 115/2003).
36 SER_DOC_REF Série do documento fiscal referenciado. C 004 - OC OC
37 NUM_DOC_REF Número do documento fiscal N 009 - OC OC
referenciado.
38 MES_DOC_REF Mês e ano da emissão do documento N 006* - OC OC
fiscal referenciado.
39 ENER_INJET Energia injetada N - 2 OC OC
40 OUTRAS_DED Outras deduções N - 2 OC OC
Observações: registro obrigatório nas operações de saídas, apenas para documentos emitidos fora do Convênio ICMS nº
115/2003, ou quando dispensados pela SEFAZ da entrega do arquivo previsto naquele convênio. Também é obrigatório nas
operações acobertadas por NF3e (modelo 66).
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C500]
Campo 02 (IND_OPER) - Valores válidos: [0, 1]
Campo 03 (IND_EMIT) - Valores válidos: [0, 1]
Campo 04 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Validação: Quando o COD_MOD for “66” e IND_OPER for “1”, este campo só deve ser informado se o campo IND_DEST
for “1”.
Campo 05 (COD_MOD) - Valores válidos: [06, 28, 29, 66] - Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 06 (COD_SIT) - Valores válidos: [00, 01, 02, 03, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3.
Campo 08 (SUB) - Validação: quando o campo COD_MOD for “66”, este campo não deve ser preenchido.
Campo 09 (COD_CONS) - Valores válidos e validação: Se o modelo for 06 (energia elétrica) ou 28 (gás canalizado), os
valores válidos são [01, 02, 03, 04, 05, 06, 07, 08]. Se o modelo for 29 (água canalizada), o valor deve constar da Tabela 4.4.2
da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações. Se o modelo do documento for 66, o campo não
deve ser preenchido.
Campo 10 (NUM_DOC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 11 (DT_DOC) - Preenchimento: data de emissão da nota fiscal no formato “ddmmaaaa”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 12 (DT_E_S) - Preenchimento: data de entrada ou saída da nota fiscal no formato “ddmmaaaa”.
Validação: Este campo deve ser menor ou igual ao valor do campo DT_FIN do registro “0000” e maior ou igual ao campo
DT_DOC.
Campo 13 (VL_DOC) - Validação: O valor deste campo deve corresponder ao somatório dos campos VL_FORN, VL_DA,
VL_SERV_NT e VL_TERC subtraído do somatório de VL_DESC, ENER_INJET e OUTRAS_DED.
Campo 15 (VL_FORN) - Preenchimento: Deve ser informado quando houver itens lançados na NF3e com código do grupo
060, 061, 062, 063, 064, 065, 085 ou 087, conforme Tabela de Código de Itens da NF3e (cClass)
Campo 16 (VL_SERV_NT) - Preenchimento: Deve ser informado quando houver itens lançados na NF3e com código do
grupo 070, 084, 085 ou 087, conforme Tabela de Código de Itens da NF3e (cClass).
Campo 17 (VL_TERC) - Preenchimento: Deve ser informado quando houver itens lançados na NF3e com código do grupo
080, 081, 085, 086 ou 087, conforme Tabela de Código de Itens da NF3e (cClass).
Campo 20 (VL_ICMS) – Preenchimento: informar o valor do ICMS creditado na operação de entrada ou o valor do ICMS
debitado na operação de saída.
Validação: a soma dos valores do campo VL_ICMS dos registros analíticos (C590) deve ser igual ao valor informado neste
campo.
Campo 22 (VL_ICMS_ST) - Preenchimento: informar o valor do ICMS creditado/debitado por substituição tributária, nas
operações de entrada ou saída, conforme legislação aplicada.
Validação: A soma dos valores do campo VL_ICMS_ST dos registros analíticos (C590) deve ser igual ao valor informado
neste campo.
Campo 23 (COD_INF) - Validação: o valor informado no campo deve existir no registro 0450.
Campo 24 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 25 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 26 (TP_LIGACAO) - Valores válidos: [1, 2, 3]
Validação: a informação é obrigatória nas operações de saídas, se COD_MOD igual a “06”. Se COD_MOD for “66”, o campo
não deve ser preenchido.
Campo 27 (COD_GRUPO_TENSAO) - Valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14]
Validação: a informação é obrigatória nas operações de saídas quando COD_MOD for igual a “06”. Se COD_MOD igual a
“66”, o campo não deve ser preenchido.
Campo 28 (CHV_DOCe) - Preenchimento: Informar a chave do documento eletrônico. A partir de 01/01/2020, o campo é
obrigatório quando COD_MOD for igual a “66”.
Validação: será conferido o dígito verificador (DV) da chave do documento eletrônico. Será verificada a consistência da raiz
de CNPJ do registro 0000 do declarante com a raiz de CNPJ contida na chave do documento eletrônico quando o campo
IND_EMIT for igual a “0” (emissão própria). Será verificada a consistência da informação dos campos COD_MOD,
NUM_DOC e SER com o número do documento e série contidos na chave da NF3e. Será também comparada a UF codificada
na chave do documento eletrônico com o campo UF informado no registro 0000.
Campo 29 (FIN_DOCe) - Valores Válidos: [1, 2, 3]
Preenchimento: o campo deve ser informado quando o campo COD_MOD for “66”. Para os demais modelos, não deve ser
informado.
Campo 30 (CHV_DOCe_REF) – Preenchimento: deve ser informada a chave do documento substituído, se eletrônico. Nos
demais casos, não preencher.
Validação: obrigatório quando COD_MOD_DOC_REF for igual a “66”. Será conferido o dígito verificador (DV) da chave do
documento eletrônico.
Campo 31 (IND_DEST) - Valores Válidos: [1, 2, 9].
Campo 32 (COD_MUN_DEST) -
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
Campo 33 (COD_CTA) - Preenchimento: informar o código da conta analítica contábil debitada/creditada.
Campo 34 (COD_MOD_DOC_REF) - Valores válidos: [06, 66] - Ver tabela reproduzida na subseção 1.4 deste guia.
Validação: deve ser informado quando o campo FIN_DOCe for igual a “2”. Não informar nas demais situações.
Campo 35 (HASH_DOC_REF) - Preenchimento: deve ser preenchido com o código de autenticação digital do registro, se o
documento substituído for modelo 6 e tenha sido emitido conforme sistemática do Convênio 115/2003. Validação: Não deve
ser informado quando COD_MOD_DOC_REF for diferente de “06”.
Quando COD_MOD_DOC_REF for igual a “06”, é obrigatória a informação deste campo ou a informação simultânea de
SER_DOC_REF, NUM_DOC_REF e MES_DOC_REF. Se qualquer um dos três campos for informado, este campo deverá
ter conteúdo VAZIO “||”
Campo 36 (SER_DOC_REF) - Preenchimento: série do documento fiscal substituído. Informar zero para série única.
Validação: Não deve ser informado quando COD_MOD_DOC_REF for diferente de “06”.
Quando COD_MOD_DOC_REF for igual a “06”, é obrigatória a informação simultânea de SER_DOC_REF,
NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF. Se HASH_DOC_REF for informado, este
campo deve ter conteúdo VAZIO “||”.
Campo 37 (NUM_DOC_REF) - Preenchimento: número do documento fiscal substituído. Validação: O valor informado no
campo deve ser maior que “0” (zero). Não deve ser informado quando COD_MOD_DOC_REF for diferente de “06”.
Quando COD_MOD_DOC_REF for igual a “06”, é obrigatória a informação simultânea de SER_DOC_REF,
NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF. Se HASH_DOC_REF for informado, este
campo deve ter conteúdo VAZIO “||”.
Campo 38 (MES_DOC_REF) - Preenchimento: mês e ano da emissão do documento fiscal referenciado no formato
“mmaaaa”. Validação: Não deve ser informado quando COD_MOD_DOC_REF for diferente de “06”.
Quando COD_MOD_DOC_REF for igual a “06”, é obrigatória a informação simultânea de SER_DOC_REF,
NUM_DOC_REF e MES_DOC_REF, ou a informação de HASH_DOC_REF. Se HASH_DOC_REF for informado, este
campo deve ter conteúdo VAZIO “||”.
Campo 39 (ENERG_INJET) – Preenchimento: deve ser informado quando houver itens lançados na NF3e com código do
grupo 560, 085 ou 087, conforme Tabela de Código de Itens da NF3e (cClass).
Campo 40 (OUTRAS_DED) – Preenchimento: deve ser informado quando houver itens lançados na NF3e com código do
grupo 590, 085 ou 087, conforme Tabela de Código de Itens da NF3e (cClass).
----
# REGISTRO C510: ITENS DO DOCUMENTO NOTA FISCAL/CONTA ENERGIA ELÉTRICA
(CÓDIGO 06), NOTA FISCAL/CONTA DE FORNECIMENTO D'ÁGUA CANALIZADA
(CÓDIGO 29) E NOTA FISCAL/CONTA DE FORNECIMENTO DE GÁS (CÓDIGO 28).
Este registro deve ser apresentado para informar os itens das Notas Fiscais/Contas de Energia Elétrica (código 06 da
Tabela Documentos Fiscais do ICMS), Notas Fiscais/Contas de fornecimento de água canalizada (código 29) e Notas Fiscais
Consumo Fornecimento de Gás (código 28 da Tabela Documentos Fiscais do ICMS), nas operações de saída.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos NUM_ITEM e COD_ITEM. Este registro não deve ser informado nas operações com documento fiscal eletrônico.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C510" C 004 - Não O
02 NUM_ITEM Número sequencial do item no documento N 003 - apresentar O
fiscal
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
04 COD_CLASS Código de classificação do item de energia N 004* - OC
elétrica, conforme a Tabela 4.4.1
05 QTD Quantidade do item N - 03 OC
06 UNID Unidade do item (Campo 02 do registro C 006 - OC
0190)
07 VL_ITEM Valor do item N - 02 O
08 VL_DESC Valor total do desconto N - 02 OC
09 CST_ICMS Código da Situação Tributária, conforme a N 003* - O
Tabela indicada no item 4.3.1
10 CFOP Código Fiscal de Operação e Prestação N 004* - O
11 VL_BC_ICMS Valor da base de cálculo do ICMS N - 02 OC
12 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
13 VL_ICMS Valor do ICMS creditado/debitado N - 02 OC
14 VL_BC_ICMS_S Valor da base de cálculo referente à N - 02 OC
T substituição tributária
15 ALIQ_ST Alíquota do ICMS da substituição tributária N 006 02 OC
na unidade da federação de destino
16 VL_ICMS_ST Valor do ICMS referente à substituição N - 02 OC
tributária
17 IND_REC Indicador do tipo de receita: C 001* - O
0- Receita própria;
1- Receita de terceiros
18 COD_PART Código do participante receptor da receita, C 060 OC
terceiro da operação (campo 02 do Registro
0150)
19 VL_PIS Valor do PIS N - 02 OC
20 VL_COFINS Valor da COFINS N - 02 OC
21 COD_CTA Código da conta analítica contábil C - - OC
debitada/creditada
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C510]
Campo 03 (COD_ITEM) - Validação: o valor informado no campo deve existir no registro 0200, campo COD_ITEM.
Campo 04 (COD_CLASS) - Validação: Somente deve ser informado se for energia elétrica e o valor informado no campo
deve existir na Tabela de Classificação de itens de Energia Elétrica, Serviços de Comunicação e Telecomunicação, constante
no item 4.4.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações. Para demais documentos o campo
deve ser apresentado como campo “vazio”.
Campo 06 (UNID) - Validação: o valor deve estar informado no registro 0190.
Campo 07 (VL_ITEM) - Preenchimento: informar o valor total do item (equivalente à quantidade x preço unitário).
Campo 09 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao
ICMS, referenciada no item 4.3.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
ICMS Normal:
a) se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero);
b) se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
c) se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores ou iguais a “0” (zero);
ICMS ST:
a) se os dois últimos caracteres deste campo forem 10, 30 ou 70, os valores dos campos VL_BC_ST, ALIQ_ST
e VL_ICMS_ST deverão ser maiores ou iguais “0” (zero).
b) se os dois últimos caracteres deste campo forem diferentes de 10, 30 ou 70, os valores dos campos VL_BC_ST,
ALIQ_ST e VL_ICMS_ST deverão ser iguais a “0” (zero).
Campo 10 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01.
Se o campo IND_OPER do registro C500 for igual a “0” (entrada), então o primeiro caractere do CFOP deve ser igual a 1, 2
ou 3. Se o campo IND_OPER do registro C500 for igual a “1” (saída), então o primeiro caractere do CFOP deve ser igual a 5,
6 ou 7.
O primeiro caractere do CFOP deve ser o mesmo para todos os itens do documento.
Não podem ser utilizados códigos que correspondam aos títulos dos agrupamentos de CFOP (códigos com caracteres finais 00
ou 50. Por exemplo: 5100).
Campo 17 (IND_REC) - Valores válidos: [0, 1]
Campo 18 (COD_PART) - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 19 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 20 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C590: REGISTRO ANALÍTICO DO DOCUMENTO – NOTA FISCAL/CONTA DE
ENERGIA ELÉTRICA (CÓDIGO 06), NOTA FISCAL DE ENERGIA ELÉTRICA
ELETRÔNICA – NF3e (CÓDIGO 66), NOTA FISCAL/CONTA DE FORNECIMENTO D'ÁGUA
CANALIZADA (CÓDIGO 29) E NOTA FISCAL CONSUMO FORNECIMENTO DE GÁS
(CÓDIGO 28).
Este registro representa a escrituração dos documentos fiscais dos modelos especificados no C500, totalizados pelo
agrupamento das combinações dos valores de CST, CFOP e Alíquota dos itens de cada documento. Deve haver um registro
C590 com os totais de cada combinação de valores de CST, CFOP e Alíquota.
Relativamente às Notas Fiscais de Energia Elétrica Eletrônica (NF3e), não devem ser apresentados neste registro os
itens sem a indicação de Código de Situação Tributária – CST, nem itens referentes à energia injetada. Quando essa energia
injetada implicar isenção incidente sobre a energia fornecida, a parcela beneficiada pela isenção deverá ser vinculada ao
CST_ICMS 40, contendo valor zero nos campos VL_BC_ICMS e VL_ICMS. Para mais informações, consulte o arquivo de
perguntas frequentes. Permanecendo dúvida, consulte a SEFAZ de sua jurisdição, por meio do e-mail corporativo localizado
no endereço: http://sped.rfb.gov.br/pagina/show/1577
As distribuidoras de energia estabelecidas no DF deverão apresentar a consolidação dos itens de NF3e referentes às
prestações de serviços dentro do campo de incidência do ISS (CFOP 5933), informando o valor zero nos campos VL_BC_ICMS,
VL_ICMS, VL_BC_ICMS_ST, VL_ICMS_ST.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS. A combinação CST_ICMS, CFOP e ALIQ_ICMS deve existir no respectivo
registro de itens do C510, quando este registro for exigido.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C590" C 004 - O O
02 CST_ICMS Código da Situação Tributária, conforme a N 003* - O O
Tabela indicada no item 4.3.1.
03 CFOP Código Fiscal de Operação e Prestação do N 004* - O O
agrupamento de itens
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
05 VL_OPR Valor da operação correspondente à N - 02 O O
combinação de CST_ICMS, CFOP, e alíquota
do ICMS.
06 VL_BC_ICMS Parcela correspondente ao "Valor da base de cálculo N - 02 OC O
do ICMS" referente à combinação de CST_ICMS,
CFOP e alíquota do ICMS.
07 VL_ICMS Parcela correspondente ao "Valor do ICMS" N - 02 OC O
referente à combinação de CST_ICMS, CFOP
e alíquota do ICMS.
08 VL_BC_ICMS_ST Parcela correspondente ao "Valor da base de N - 02 OC O
cálculo do ICMS" da substituição tributária
referente à combinação de CST_ICMS, CFOP
e alíquota do ICMS.
09 VL_ICMS_ST Parcela correspondente ao valor N - 02 OC O
creditado/debitado do ICMS da substituição
tributária, referente à combinação de
CST_ICMS, CFOP, e alíquota do ICMS.
10 VL_RED_BC Valor não tributado em função da redução da N - 02 OC O
base de cálculo do ICMS, referente à
combinação de CST_ICMS, CFOP e alíquota
do ICMS.
11 COD_OBS Código da observação do lançamento fiscal C 006 - OC OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência - 1:N (um ou vários por registro C500)
Campo 01 (REG) - Valor Válido: [C590]
Campo 02 (CST_ICMS) - Preenchimento: Nos documentos fiscais de emissão própria o campo deverá ser preenchido com o
código da Situação Tributária sob o enfoque do declarante. Nas operações de entradas (documentos de terceiros), informar o
CST que constar no documento fiscal de aquisição dos produtos.
A partir julho de 2012, nas operações de aquisições de mercadorias o CST_ICMS deverá ser informado sob o enfoque do
declarante. Exemplo 1 – Aquisição de mercadorias tributadas para uso e consumo informar código “90” da tabela B. Exemplo
2 – Aquisição de mercadorias para comercialização com ICMS retido por ST informar código “60” da tabela B.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao ICMS, referenciada no item
4.3.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
ICMS Normal:
a) se os dois últimos dígitos deste campo forem 30, 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero);
b) se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
c) se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores ou iguais a “0” (zero);
ICMS ST:
a) se os dois últimos caracteres deste campo forem 10, 30 ou 70, os valores dos campos 16 (VL_BC_ST), 17 (ALIQ_ST)
e 18 (VL_ICMS_ST) deverão ser maiores ou iguais a “0” (zero).
b) se os dois últimos caracteres deste campo forem diferentes de 10, 30 ou 70, os valores dos campos 16 (VL_BC_ST),
17 (ALIQ_ST) e 18 (VL_ICMS_ST) deverão ser iguais a “0” (zero).
Campo 03 (CFOP) - Preenchimento: em se tratando de operações de entrada, devem ser registrados os códigos de operação
que correspondam ao tratamento tributário relativo à destinação do item.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01.
Não podem ser utilizados códigos que correspondam aos títulos dos agrupamentos de CFOP (códigos com caracteres finais 00
ou 50. Por exemplo: 5100).
Se o campo IND_OPER do registro C500 for igual a “0” (zero), então o primeiro caractere do CFOP deve ser igual a 1, 2 ou
3. Se campo IND_OPER do registro C500 for igual a “1” (um), então o primeiro caractere do CFOP deve ser igual a 5,6,7.
Campo 05 (VL_OPR) – Preenchimento: Na combinação de CST_ICMS, CFOP e ALIQ_ICMS, informar neste campo o valor
fornecido somado aos valores de outras despesas acessórias, subtraído o desconto incondicional.
Campo 06 (VL_BC_ICMS) - Validação: o valor constante neste campo deve corresponder à soma dos valores do Campo
VL_BC_ICMS dos registros C510 (itens), se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste
registro.
Campo 07 (VL_ICMS) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo VL_ICMS
dos registros C510 (itens), se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste registro.
Campo 08 (VL_BC_ICMS_ST) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_BC_ICMS_ST dos registros C510 (itens), se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste
registro.
Campo 09 (VL_ICMS_ST) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_ICMS_ST dos registros C510 (itens), se existirem, que possuam a mesma combinação de CST, CFOP e Alíquota deste
registro.
Campo 10 (VL_RED_BC) - Validação: este campo só pode ser preenchido, se os dois últimos dígitos do campo CST_ICMS
forem iguais a 20 ou 70.
Campo 11 (COD_OBS) - Validação: o valor informado no campo deve existir no registro 0460.
----
# REGISTRO C591: INFORMAÇÕES DO FUNDO DE COMBATE À POBREZA – FCP NA NF3e
(CÓDIGO 66)
Este registro tem por objetivo prestar informações do Fundo de Combate à Pobreza (FCP), constante na NF3e. Os
valores deste registro são meramente informativos e não são contabilizados na apuração dos registros no bloco E.
A obrigatoriedade e forma de apresentação de cada campo deste registro deve ser verificada junto às unidades
federativas.
Nº Campo Descrição Tipo Tam Dec Entr. Saídas
01 Texto fixo contendo "C591"
REG C 004 - O O
Valor do Fundo de Combate à Pobreza (FCP) vinculado à operação
02 VL_FCP_OP
própria, na combinação de CST_ICMS, CFOP e alíquota do ICMS N - 02 OC OC
Valor do Fundo de Combate à Pobreza (FCP) vinculado à operação
03 VL_FCP_ST de substituição tributária, na combinação de CST_ICMS, CFOP e
N - 02 OC OC
alíquota do ICMS.
Observações:
Nível hierárquico – 4
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [C591]
Campo 02 (VL_FCP_OP) – Preenchimento: informar o valor total do Fundo de Combate à Pobreza (FCP) vinculado à
operação própria, relativo aos itens com mesma combinação de CST_ICMS, CFOP e alíquota do ICMS informada no registro
pai, C590.
Validação: Somente pode ser preenchido quando o campo CST_ICMS do registro C590 assumir o valor x00 ou x20.
Campo 03 (VL_FCP_ST) – Preenchimento: informar o valor do Fundo de Combate à Pobreza (FCP) vinculado à operação
de substituição tributária, relativo aos itens com mesma combinação de CST_ICMS, CFOP e alíquota do ICMS informada no
registro pai, C590.
Validação: Somente pode ser preenchido quando o campo CST_ICMS do registro C590 assumir o valor x10.
----
# REGISTRO C595: OBSERVAÇÕES DO LANÇAMENTO FISCAL (CÓDIGOS 06, 28, 29 e 66)
Este registro deve ser informado quando, em decorrência da legislação estadual, houver ajustes nos documentos fiscais
eletrônicos, informações sobre diferencial de alíquota, antecipação de imposto e outras situações. Estas informações equivalem
às observações que são lançadas na coluna “Observações” dos Livros Fiscais previstos no Convênio SN/70 – SINIEF, art. 63,
I a IV.
Sempre que existir um ajuste (lançamentos referentes aos impostos que têm o cálculo detalhado em Informações
Complementares da NF; ou aos impostos que estão definidos na legislação e não constam na NF; ou aos recolhimentos
antecipados dos impostos), deve, conforme dispuser a legislação estadual, ocorrer uma observação.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C595" C 004 - O O
Código da observação do lançamento fiscal (campo 02 do Registro
02 COD_OBS C 006 - O O
0460)
03 TXT_COMPL Descrição complementar do código de observação. C - - OC OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C595]
Campo 02 (COD_OBS) – Preenchimento: as observações de lançamento devem ser informadas neste campo, exceto quando
a legislação estadual prever o preenchimento do campo COD_OBS do registro C590.
Validação: o código informado deve constar do registro 0460.
Campo 03 (TXT_COMPL) - Preenchimento: utilizado para complementar observação cujo código seja de informação
genérica.
----
# REGISTRO C597: OUTRAS OBRIGAÇÕES TRIBUTÁRIAS, AJUSTES E INFORMAÇÕES DE
VALORES PROVENIENTES DE DOCUMENTO FISCAL
Este registro tem por objetivo detalhar outras obrigações tributárias, ajustes e informações de valores do documento
fiscal do registro C595, que podem ou não alterar o cálculo do valor do imposto.
Os valores de ICMS ou ICMS ST (campo 07 - VL_ICMS) serão somados diretamente na apuração, no registro E110
– Apuração do ICMS – Operações Próprias, campo VL_AJ_DEBITOS ou campo VL_AJ_CREDITOS, e no registro E210 –
Apuração do ICMS – Substituição Tributária, campo VL_AJ_CREDITOS_ST e campo VL_AJ_DEBITOS_ST, de acordo com
a especificação do TERCEIRO CARACTERE do Código do Ajuste (Tabela 5.3 - Tabela de Ajustes e Valores provenientes do
Documento Fiscal).
Este registro será utilizado também por contribuinte para o qual a Administração Tributária Estadual exija, por meio
de legislação específica, apuração em separado (sub-apuração). Neste caso o Estado publicará a Tabela 5.3 com códigos que
contenham os dígitos “3”, “4”, “5”, “6”, “7” e “8” no quarto caractere (“Tipos de Apuração de ICMS”), sendo que cada um
dos dígitos possibilitará a escrituração de uma apuração em separado (sub-apuração) no registro 1900 e filhos. Para que haja a
apuração em separado do ICMS de determinadas operações ou itens de mercadorias, estes valores terão de ser estornados da
Apuração Normal (E110) e transferidos para as sub-apurações constantes do registro 1900 e filhos por meio de lançamentos de
ajustes neste registro. Isto ocorrerá quando:
1. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C597 for igual a “2 – Estorno de Débito” e
o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gerará um ajuste a crédito (campo 07- VL_AJ_CREDITOS) no registro E110 e
também um outro lançamento a débito no registro 1920 (campo 02 -
VL_TOT_TRANSF_DEBITOS_OA) da apuração em separado (sub-apuração) definida no campo 02-
IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4”, “5”, “6”, “7” e “8”, que deverá
coincidir com o quarto caractere do COD_AJ; e
2. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C597 for igual a “5 – Estorno de Crédito”
e o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gerará um ajuste a débito (campo 03- VL_AJ_DEBITOS) no registro E110 e
também um outro lançamento a crédito no registro 1920 (campo 05 -
VL_TOT_TRANSF_CRÉDITOS_OA) da apuração em separado (sub-apuração) que for definida no
campo 02 - IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4” “5”, “6”, “7” e “8”, que
deverá coincidir com o quarto caractere do COD_AJ.
Os valores que gerarem crédito ou débito de ICMS (ou seja, aqueles que não sejam simplesmente informativos) serão
somados na apuração, assim como os registros C590.
Este registro somente deve ser informado para as UF que publicarem a tabela 5.3 – Tabela de Ajustes e Valores
provenientes do Documento Fiscal.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C597" C 004 - O O
02 COD_AJ Código dos ajustes/benefício/incentivo, conforme tabela C 010* - O O
indicada no item 5.3.
03 DESCR_COMPL_AJ Descrição complementar do ajuste do documento fiscal C - - OC OC
04 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC OC
05 VL_BC_ICMS Base de cálculo do ICMS ou do ICMS ST N - 02 OC OC
06 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
07 VL_ICMS Valor do ICMS ou do ICMS ST N - 02 OC OC
08 VL_OUTROS Outros valores N - 02 OC OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C597]
Campo 02 (COD_AJ) - Validação: verifica se o COD_AJ está de acordo com a Tabela 5.3 da UF do informante do arquivo.
Campo 03 (DESCR_COMPL_AJ): Preenchimento: O contribuinte deverá fazer a descrição complementar de ajustes (Tabela
5.3) sempre que informar códigos genéricos.
Campo 04 (COD_ITEM) - Preenchimento: deve ser informado se o ajuste/benefício for relacionado ao produto.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 07 (VL_ICMS) - Preenchimento: valor do montante do ajuste do imposto. Para ajustes referentes a ICMS ST, o campo
VL_ICMS deve conter o valor do ICMS ST. Os dados que gerarem crédito ou débito (ou seja, aqueles que não são simplesmente
informativos) serão somados na apuração, assim como os registros C590.
Campo 08 (VL_OUTROS) - Preenchimento: preencher com outros valores, quando o código do ajuste for informativo,
conforme Tabela 5.3.
----
# REGISTRO C600: CONSOLIDAÇÃO DIÁRIA DE NOTAS FISCAIS/CONTAS DE ENERGIA
ELÉTRICA (CÓDIGO 06), NOTA FISCAL/CONTA DE FORNECIMENTO D'ÁGUA
CANALIZADA (CÓDIGO 29) E NOTA FISCAL/CONTA DE FORNECIMENTO DE GÁS
(CÓDIGO 28) (EMPRESAS NÃO OBRIGADAS AO CONVÊNIO ICMS 115/03).
Este registro deve ser apresentado na consolidação diária de Notas Fiscais/Conta de Energia Elétrica (código 06 da
Tabela Documentos Fiscais do ICMS), Notas Fiscais de Fornecimento D’Água (código 29 da Tabela Documentos Fiscais do
ICMS) e Notas Fiscais/Conta de Fornecimento de Gás (código 28 da Tabela Documentos Fiscais do ICMS) para empresas não
obrigadas ao Convênio ICMS 115/2003.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_MOD, COD_MUN e COD_CONS. A apresentação deste registro implica a não apresentação do registro C700
e C500.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C600" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, C 002* - apresentar O
conforme a Tabela 4.1.1
03 COD_MUN Código do município dos pontos de N 007* - O
consumo, conforme a tabela IBGE
04 SER Série do documento fiscal C 004 - OC
05 SUB Subsérie do documento fiscal N 003 - OC
06 COD_CONS - Código de classe de consumo de C 002* - O
energia elétrica ou gás:
01 - Comercial
02 - Consumo Próprio
03 - Iluminação Pública
04 - Industrial
05 - Poder Público
06 - Residencial
07 - Rural
08 -Serviço Público.
- Código de classe de consumo de
Fornecimento D´água – Tabela 4.4.2.
07 QTD_CONS Quantidade de documentos consolidados N - - O
neste registro
08 QTD_CANC Quantidade de documentos cancelados N - - OC
09 DT_DOC Data dos documentos consolidados N 008* - O
10 VL_DOC Valor total dos documentos N - 02 O
11 VL_DESC Valor acumulado dos descontos N - 02 OC
12 CONS Consumo total acumulado, em kWh N - - OC
(Código 06)
13 VL_FORN Valor acumulado do fornecimento N - 02 OC
14 VL_SERV_NT Valor acumulado dos serviços não- N - 02 OC
tributados pelo ICMS
15 VL_TERC Valores cobrados em nome de terceiros N - 02 OC
16 VL_DA Valor acumulado das despesas acessórias N - 02 OC
17 VL_BC_ICMS Valor acumulado da base de cálculo do N - 02 OC
ICMS
18 VL_ICMS Valor acumulado do ICMS N - 02 OC
19 VL_BC_ICMS_ST Valor acumulado da base de cálculo do N - 02 OC
ICMS substituição tributária
20 VL_ICMS_ST Valor acumulado do ICMS retido por N - 02 OC
substituição tributária
21 VL_PIS Valor acumulado do PIS N - 02 OC
22 VL_COFINS Valor acumulado COFINS N - 02 OC
Observações: registro obrigatório nas operações de saídas, apenas para documentos emitidos fora do Convênio ICMS nº
115/2003, ou quando dispensados pela SEFAZ da entrega do arquivo previsto naquele convênio.
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C600]
Campo 02 (COD_MOD) - Valores válidos: [06, 28, 29] - – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 03 (COD_MUN) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo
7 dígitos.
Campo 06 (COD_CONS) - Valores válidos e validação: Se o modelo for 06 (energia elétrica) ou 28 (gás canalizado), os
valores válidos são [01, 02, 03, 04, 05, 06, 07, 08]. Se o modelo for 29 (água canalizada), o valor deve constar da Tabela 4.4.2
da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 07 (QTD_CONS) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 08 (QTD_CANC) - Validação: o valor deve ser menor ou igual ao valor do campo QTD_CONS, pois a quantidade de
documentos cancelados não pode ser maior que a quantidade de documentos consolidados. Este valor deve ser igual à
quantidade de ocorrências do registro C601 (documentos cancelados).
Campo 09 (DT_DOC) - Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do
registro 0000.
Campo 17 (VL_BC_ICMS) - Validação: o valor informado deve ser igual à soma do campo VL_BC_ICMS dos registros
C610 (itens).
Campo 18 (VL_ICMS) - Validação: o valor informado deve ser igual à soma do campo VL_ICMS dos registros C610 (itens).
Campo 19 (VL_BC_ICMS_ST) - Validação: o valor informado deve ser igual à soma do campo VL_BC_ICMS_ST dos
registros C610 (itens).
Campo 20 (VL_ICMS_ST) - Validação: o valor informado deve ser igual à soma do campo VL_ICMS_ST dos registros C610
(itens).
Campo 21 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 22 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C601: DOCUMENTOS CANCELADOS – CONSOLIDAÇÃO DIÁRIA DE NOTAS
FISCAIS/CONTAS DE ENERGIA ELÉTRICA (CÓDIGO 06), NOTA FISCAL/CONTA DE
FORNECIMENTO D'ÁGUA CANALIZADA (CÓDIGO 29) E NOTA FISCAL/CONTA DE
FORNECIMENTO DE GÁS (CÓDIGO 28)
Este registro tem por objetivo informar a numeração dos documentos cancelados da consolidação diária dos
documentos fiscais do C600.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C601" C 004 - Não O
02 NUM_DOC_CANC Número do documento fiscal cancelado N 009 - apresentar O
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C601]
Campo 02 (NUM_DOC_CANC) - Validação: o valor informado no campo deve ser maior que “0” (zero).
----
# REGISTRO C610: ITENS DO DOCUMENTO CONSOLIDADO (CÓDIGO 06), NOTA
FISCAL/CONTA DE FORNECIMENTO D'ÁGUA CANALIZADA (CÓDIGO 29) E NOTA
FISCAL/CONTA DE FORNECIMENTO DE GÁS (CÓDIGO 28) (EMPRESAS NÃO
OBRIGADAS AO CONVÊNIO ICMS 115/03).
Este registro tem por objetivo discriminar por item os registros consolidados apresentados no C600.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos COD_CLASS, COD_ITEM e ALIQ_ICMS.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo “C610” C 004 - Não O
02 COD_CLASS Código de classificação do item de energia N 004* - apresentar OC
elétrica, conforme Tabela 4.4.1
03 COD_ITEM Código do item (campo 02 do Registro C 060 - O
0200)
04 QTD Quantidade acumulada do item N - 03 O
05 UNID Unidade do item (Campo 02 do registro C 006 - O
0190)
06 VL_ITEM Valor acumulado do item N - 02 O
07 VL_DESC Valor acumulado dos descontos N - 02 OC
08 CST_ICMS Código da Situação Tributária, conforme a N 003* - O
Tabela indicada no item 4.3.1
09 CFOP Código Fiscal de Operação e Prestação N 004* - O
conforme tabela indicada no item 4.2.2.
10 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
11 VL_BC_ICMS Valor acumulado da base de cálculo do N - 02 OC
ICMS
12 VL_ICMS Valor acumulado do ICMS debitado N - 02 OC
13 VL_BC_ICMS_ST Valor da base de cálculo do ICMS N - 02 OC
substituição tributária
14 VL_ICMS_ST Valor do ICMS retido por substituição N - 02 OC
tributária
15 VL_PIS Valor do PIS N - 02 OC
16 VL_COFINS Valor da COFINS N - 02 OC
17 COD_CTA Código da conta analítica contábil C - - OC
debitada/creditada
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C610]
Campo 02 (COD_CLASS) – Preenchimento: só deve ser preenchido no caso do campo COD_MOD do registro C600 ser
igual a 06 (Energia Elétrica). Para demais modelos previstos, o campo deve ser apresentado como campo “vazio”.
Validação: Se o código de modelo de documentos for igual a “06”, então o valor informado no campo deve existir na Tabela
4.4.1.
Campo 03 (COD_ITEM) - Validação: o valor informado no campo deve existir no registro 0200, campo COD_ITEM.
Campo 04 (QTD) - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 05 (UNID) - Validação: o valor deve estar informado no registro 0190.
Campo 08 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao
ICMS, referenciada no item 4.3.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 alterações.
ICMS Normal:
se os dois últimos dígitos deste campo forem iguais a 30, 40, 41, 50, ou 60, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser iguais a “0” (zero);
se os dois últimos dígitos deste campo forem diferentes de 30, 40, 41, 50, e 60, então os valores dos campos
VL_BC_ICMS, ALIQ_ICMS e VL_ICMS deverão ser maiores que “0” (zero);
se os dois últimos dígitos deste campo forem iguais a 51 ou 90, então os valores dos campos VL_BC_ICMS,
ALIQ_ICMS e VL_ICMS deverão ser maiores ou iguais a “0” (zero);
ICMS ST:
a) se os dois últimos caracteres deste campo forem 10, 30 ou 70 os valores dos campos VL_BC_ST, ALIQ_ST
e VL_ICMS_ST deverão ser maiores ou iguais a “0” (zero).
b) se os dois últimos caracteres deste campo forem diferentes de 10, 30 ou 70, os valores dos campos VL_BC_ST,
ALIQ_ST e VL_ICMS_ST deverão ser iguais a “0” (zero).
Campo 09 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01.
O primeiro caractere do CFOP deve ser igual a 5, 6 ou 7.
Campo 15 (VL_PIS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 16 (VL_COFINS) - Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do
registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C690: REGISTRO ANALÍTICO DOS DOCUMENTOS (NOTAS FISCAIS/CONTAS
DE ENERGIA ELÉTRICA (CÓDIGO 06), NOTA FISCAL/CONTA DE FORNECIMENTO
D’ÁGUA CANALIZADA (CÓDIGO 29) E NOTA FISCAL/CONTA DE FORNECIMENTO DE
GÁS (CÓDIGO 28)
Este registro tem por objetivo representar a escrituração dos documentos fiscais dos modelos especificados no C600,
totalizados pelo agrupamento das combinações dos valores de CST, CFOP e Alíquota dos itens de cada registro consolidado.
Existirá um registro C690 para cada combinação de valores de CST, CFOP e Alíquota que existir nos itens (registro C610),
totalizando estes itens.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS. A combinação CST_ICMS, CFOP e ALIQ_ICMS deve existir no respectivo
registro de itens do C610, quando este registro for exigido.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C690" C 004 - Não O
02 CST_ICMS Código da Situação Tributária, conforme a N 003* - apresentar O
tabela indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação, N 004* - O
conforme a tabela indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 2 OC
05 VL_OPR Valor da operação correspondente à N - 2 O
combinação de CST_ICMS, CFOP, e
alíquota do ICMS.
06 VL_BC_ICMS Parcela correspondente ao "Valor da base de N - 2 O
cálculo do ICMS" referente à combinação
CST_ICMS, CFOP e alíquota do ICMS
07 VL_ICMS Parcela correspondente ao "Valor do ICMS" N - 2 O
referente à combinação CST_ICMS, CFOP
e alíquota do ICMS
08 VL_RED_BC Valor não tributado em função da redução N - 02 O
da base de cálculo do ICMS, referente à
combinação de CST_ICMS, CFOP e
alíquota do ICMS.
09 VL_BC_ICMS_ST Valor da base de cálculo do ICMS N - 02 O
substituição tributária
10 VL_ICMS_ST Valor do ICMS retido por substituição N - 02 O
tributária
11 COD_OBS Código da observação do lançamento fiscal C 006 - OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C690]
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária do ICMS,
referenciada no item 4.3.1da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 03 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01.
Campo 06 (VL_BC_ICMS) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_BC_ICMS dos registros C610 (itens), se existirem, para a mesma combinação de valores dos campos CST_ICMS, CFOP
e ALIQ_ICMS.
Campo 07 (VL_ICMS) – Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_ICMS dos registros C610 (itens), para a mesma combinação de valores dos campos CST_ICMS, CFOP e ALIQ_ICMS.
Campo 08 (VL_RED_BC) - Validação: o campo VL_RED_BC só pode ser preenchido se o valor do campo CST_ICMS for
igual a 20 ou 70.
Campo 09 (VL_BC_ICMS_ST) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_BC_ICMS_ST dos registros C610 (itens), para a mesma combinação de valores dos campos CST_ICMS, CFOP e
ALIQ_ICMS.
Campo 10 (VL_ICMS_ST) - Validação: o valor constante neste campo deve corresponder à soma dos valores do campo
VL_ICMS_ST dos registros C610 (itens), para a mesma combinação de valores dos campos CST_ICMS, CFOP e ALIQ_ICMS.
Campo 11 (COD_OBS) - Validação: o valor informado no campo COD_OBS deve existir no registro 0460.
----
# REGISTRO C700: CONSOLIDAÇÃO DOS DOCUMENTOS NF/CONTA ENERGIA ELÉTRICA
(CÓD 06), EMITIDAS EM VIA ÚNICA (EMPRESAS OBRIGADAS À ENTREGA DO ARQUIVO
PREVISTO NO CONVÊNIO ICMS 115/03), NOTA FISCAL/CONTA DE FORNECIMENTO DE
GÁS CANALIZADO (CÓDIGO 28) e NOTA FISCAL DE ENERGIA ELÉTRICA ELETRÔNICA
– NF3e (CÓDIGO 66)
Este registro deve ser apresentado com a consolidação das Notas Fiscais/Conta de Energia Elétrica (código 06 da
Tabela Documentos Fiscais do ICMS) pelas empresas obrigadas à entrega do arquivo previsto no Convênio ICMS 115/2003 e
código 66 da Tabela de Documentos Fiscais do ICMS.
Para a escrituração de documentos fiscais do modelo 66, este registro consolida o total das notas, por data de emissão
e série, que não utilizarem ajustes da tabela 5.3, para as UF cuja legislação permitir a escrituração consolidada.
Este registro deve ser apresentado pelas empresas fornecedoras de gás canalizado domiciliadas nas unidades federadas
que utilizam o Convênio ICMS 115/2003.
Informações interestaduais devem estar englobadas na consolidação deste registro e também devem ser informadas no
registro 1500. Neste caso, as informações repetidas no 1500 terão apenas efeito declaratório, não sendo consideradas no cálculo
da apuração.
A apresentação deste registro implica a não apresentação do registro C600. O documento informado de forma
individualizada no C500 não deve ser considerado na informação consolidada deste registro.
A NF3e que contenha apenas itens sem a indicação de Código de Situação Tributária – CST não deve ser escriturada.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos SER, NRO_ORD_INI e NRO_ORD_FIN. Exceto para o código 66, não pode haver sobreposição de intervalos para a
mesma série.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C700" C 004 - Não O
Código do modelo do documento fiscal, apresentar O
02 COD_MOD C 002* -
conforme a Tabela 4.1.1
03 SER Série do documento fiscal C 004 - OC
04 NRO_ORD_INI Número de ordem inicial N 009 - O
05 NRO_ORD_FIN Número de ordem final N 009 - O
Data de emissão inicial dos documentos / Data O
06 DT_DOC_INI N 008* -
inicial de vencimento da fatura
Data de emissão final dos documentos / Data O
07 DT_DOC_FIN N 008* -
final do vencimento da fatura
08 NOM_MEST Nome do arquivo Mestre de Documento Fiscal C 033 - OC
Chave de codificação digital do arquivo Mestre OC
09 CHV_COD_DIG C 032 -
de Documento Fiscal
Observações:
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C700]
Campo 02 (COD_MOD) - Valor Válido: [06, 28, 66] – Ver tabela reproduzida na subseção 1.4 deste guia.
Campo 04 (NRO_ORD_INI) - Validação: o valor informado deve ser maior que “0” (zero).
Campo 05 (NRO_ORD_FIN) - Validação: o valor informado deve ser igual ou maior que o valor no campo NRO_ORD_INI.
Campo 06 (DT_DOC_INI) - Preenchimento: informar data de emissão inicial dos documentos, formato “ddmmaaaa” ou a
data inicial do vencimento da fatura, conforme disposto na legislação estadual. Para a escrituração de documentos fiscais
modelo 66, esse campo indica a data de emissão em que foram totalizados os documentos.
Validação: a data informada no campo deve ser maior ou igual ao valor no campo DT_INI do registro 0000. Este valor deve
ser menor ou igual ao valor do campo DT_DOC_FIN.
Campo 07 (DT_DOC_FIN) - Preenchimento: informar data de emissão final dos documentos, formato “ddmmaaaa” ou a data
final do vencimento da fatura, conforme disposto na legislação estadual.
Para a escrituração de documentos fiscais modelo 66, esse campo deve ter o mesmo valor do campo 06 (DT_DOC_INI).
Validação: o valor informado no campo deve ser menor ou igual ao valor no campo DT_FIN do registro 0000.
Campo 08 (NOM_MEST) - Preenchimento: informar o nome do volume do arquivo mestre de documento fiscal, conforme
item 4.5 do Anexo Único (Manual de Orientação) do Convênio ICMS 115/2003. Até 31/12/2016, o campo tinha tamanho 015.
Esse campo não deve ser preenchido somente para documentos fiscais modelo 66.
Campo 09 (CHV_COD_DIG) - Preenchimento: chave de codificação digital do arquivo Mestre de Documento Fiscal,
conforme Parágrafo Único da Cláusula Segunda do Convênio ICMS 115/2003. Esse campo não deve ser preenchido somente
para documentos fiscais modelo 66.
----
# REGISTRO C790: REGISTRO ANALÍTICO DOS DOCUMENTOS (CÓDIGOS 06, 28 e 66).
Este registro representa a escrituração dos documentos fiscais dos modelos especificados no C700, totalizados pelo
agrupamento das combinações dos valores de CST, CFOP e Alíquota dos itens de cada registro consolidado.
Relativamente às Notas Fiscais de Energia Elétrica Eletrônica (NF3e), não devem ser apresentados neste registro os
itens sem a indicação de Código de Situação Tributária – CST, nem itens referentes à energia injetada. Quando essa energia
injetada implicar isenção incidente sobre a energia fornecida, a parcela beneficiada pela isenção deverá ser vinculada ao
CST_ICMS 40, contendo valor zero nos campos VL_BC_ICMS e VL_ICMS. Para mais informações, consulte o arquivo de
perguntas frequentes. Permanecendo dúvida, consulte a SEFAZ de sua jurisdição, por meio do e-mail corporativo localizado
no endereço: http://sped.rfb.gov.br/pagina/show/1577
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos
campos CST_ICMS, CFOP e ALIQ_ICMS.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C790" C 004 - Não O
02 CST_ICMS Código da Situação Tributária, conforme a N 003* - Apresentar O
tabela indicada no item 4.3.1
Código Fiscal de Operação e Prestação, O
03 CFOP N 004* -
conforme a tabela indicada no item 4.2.2
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
VL_OPR Valor da operação correspondente à O
05 combinação de CST_ICMS, CFOP, e N - 02
alíquota do ICMS
Parcela correspondente ao “Valor da base de O
06 VL_BC_ICMS cálculo do ICMS” referente à combinação N - 02
CST_ICMS, CFOP, e alíquota do ICMS
Parcela correspondente ao “Valor do ICMS” O
07 VL_ICMS referente à combinação CST_ICMS, CFOP e N - 02
alíquota do ICMS
Valor da base de cálculo do ICMS O
08 VL_BC_ICMS_ST N - 02
substituição tributária
Valor do ICMS retido por substituição O
09 VL_ICMS_ST N - 02
tributária
10 VL_RED_BC Valor não tributado em função da redução da N - 02 O
base de cálculo do ICMS, referente à
combinação de CST_ICMS, CFOP e alíquota
do ICMS
11 COD_OBS Código da observação do lançamento fiscal C 006 - OC
(campo 02 do Registro 0460)
Observações:
Nível hierárquico - 3
Ocorrência - 1:N (um ou vários por registro C700)
Campo 01 (REG) - Valor Válido: [C790]
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária do ICMS,
referenciada no item 4.3.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 03 (CFOP) - Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação,
conforme Ajuste SINIEF 07/01. Somente deve ser preenchido com CFOP indicador de operação de saída.
Campo 10 (VL_RED_BC) - Validação: este campo só pode ser preenchido se os dois últimos dígitos do campo CST_ICMS
forem iguais a 20 ou 70.
Campo 11 (COD_OBS) - Validação: o valor informado no campo deve existir no registro 0460.
----
# REGISTRO C791: REGISTRO DE INFORMAÇÕES DE ST POR UF (CÓDIGOS 06 e 66)
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C791" C 004 - Não O
02 UF Sigla da unidade da federação a que se refere a C 002* -
apresentar
O
retenção ST
03 VL_BC_ICMS_ST Valor da base de cálculo do ICMS substituição N - 02 O
tributária
04 VL_ICMS_ST Valor do ICMS retido por substituição tributária N - 02 O
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C791]
Campo 02 (UF) - Validação: o valor informado no campo deve existir na tabela de UF.
REGISTRO C800: CUPOM FISCAL ELETRÔNICO – SAT (CF-E-SAT) (CÓDIGO 59)
Este registro deve ser gerado para cada CF-e-SAT (Código 59) emitido por equipamento SAT-CF-e, conforme Ajuste
SINIEF no 11, de 24 de setembro de 2010.
Não poderão ser informados dois ou mais registros com a mesma combinação de COD_SIT + NUM_CFE +
NUM_SAT + DT_DOC.
Para cupom fiscal eletrônico cancelado, informar somente os campos REG, COD_MOD, COD_SIT, NUM_CFE,
NR_SAT e CHV_CFE.
Para cada registro C800 deve ser apresentado obrigatoriamente, pelo menos, um registro C850 observada a exceção
abaixo indicada:
Exceção 1: Para documentos com código de situação (campo COD_SIT) cancelado (código “02”) ou cancelado
extemporâneo (código “03”), não apresentar o registro filho (C850).
Exceção 2: Os documentos fiscais emitidos pelas filiais das empresas que possuam inscrição estadual única ou sejam
autorizadas pelos fiscos estaduais a centralizar suas escriturações fiscais deverão ser informados como sendo de emissão própria
e código de situação igual a “00 – Documento regular”.
Nº Campo Descrição Tipo Tam Dec Entr Saídas
01 REG Texto fixo contendo "C800" C 004 - O
02 COD_MOD Código do modelo do documento fiscal, conforme C 002 - O
a Tabela 4.1.1
03 COD_SIT Código da situação do documento fiscal, N 002 - O
conforme a Tabela 4.1.2
04 NUM_CFE Número do Cupom Fiscal Eletrônico N 006 - O
05 DT_DOC Data da emissão do Cupom Fiscal Eletrônico N 008 - O
06 VL_CFE Valor total do Cupom Fiscal Eletrônico N - 02 O
07 VL_PIS Valor total do PIS N - 02 OC
08 VL_COFINS Valor total da COFINS N - 02 Não OC
09 CNPJ_CPF CNPJ ou CPF do destinatário N 14 - Apresentar OC
10 NR_SAT Número de Série do equipamento SAT N 009 - O
11 CHV_CFE Chave do Cupom Fiscal Eletrônico N 044 - O
12 VL_DESC Valor total de descontos N - 02 O
13 VL_MERC Valor total das mercadorias e serviços N - 02 O
14 VL_OUT_DA Valor total de outras despesas acessórias e N - 02 O
acréscimos
15 VL_ICMS Valor do ICMS N - 02 O
16 VL_PIS_ST Valor total do PIS retido por subst. trib. N - 02 O
17 VL_COFINS_ST Valor total da COFINS retido por subst. trib. N - 02 O
Observações:
Nível hierárquico: 2
Ocorrência: Vários
Campo 01 (REG) – Valor Válido: [C800]
Campo 02 (COD_MOD) – Preenchimento: deve corresponder ao código CF-e-SAT (Valor Válido: 59). Ver tabela
reproduzida na subseção 1.4 deste guia.
Campo 03 (COD_SIT) – Valores válidos: [00, 01, 02, 03]
Preenchimento: verificar a descrição da situação do documento na Subseção 1.3, respeitando os valores válidos acima
indicados.
Campo 05 (DT_DOC) – Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se
quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 06 (VL_CFE) – Preenchimento: corresponde ao campo Valor total do CF-e-SAT, constante do leiaute do CF-e-SAT.
Validação: o valor informado neste campo deve ser igual à soma do campo VL_OPR dos registros C850 (“filhos” deste registro
C800).
Campo 07 (VL_PIS) – Preenchimento: corresponde ao campo Valor Total do PIS, constante do leiaute do CF-e-SAT. Os
contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do registro 0000 estão dispensados
do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 08 (VL_COFINS) – Preenchimento: corresponde ao campo Valor Total do COFINS, constante do leiaute do CF-e-
SAT. Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de apuração do registro 0000 estão
dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 09 (CNPJ_CPF) – Validação: Esse campo não deve ser informado.
Campo 11 (CHV_CFE) – Validação: é conferido o dígito verificador (DV) da chave do CF-e-SAT. Para confirmação
inequívoca de que a chave do CF-e-SAT corresponde aos dados informados no documento, será comparado o CNPJ existente
na CHV_CFE com o campo CNPJ do registro 0000, que corresponde ao CNPJ do informante do arquivo. Serão verificados a
consistência da informação do campo NUM_CFE e o número do documento contido na chave do CF-e-SAT, bem como
comparado se a informação do AAMM de emissão contido na chave do CFE corresponde ao ano e mês da data de emissão do
CF-e-SAT. Será também comparada a UF codificada na chave do CF-e-SAT com o campo UF informado no registro 0000.
Formação da chave:
Campo Tamanho Obs.
Código da UF 2
AAMM da emissão 4
CNPJ do emitente 14
Modelo do documento fiscal 2 Código para o CF-e
Número de série do SAT 9 Número sequencial atribuído pela SEFAZ, iniciando em 000000001
Número do CF-e 6 Numeração sequencial para cada equipamento
Código numérico 6 Número aleatório gerado pelo SAT para cada CF-e
DV 1 Módulo 11
Total 44
Campo 12 (VL_DESC) – Preenchimento: corresponde ao campo Valor Total dos Descontos sobre item, constante do leiaute
do CF-e-SAT.
Campo 13 (VL_MERC) – Preenchimento: corresponde ao campo Valor Total dos Produtos e Serviços, constante do leiaute
do CF-e-SAT.
Campo 14 (VL_OUT_DA) – Preenchimento: corresponde ao campo Valor Total de Outras Despesas Acessórias sobre item,
constante do leiaute do CF-e-SAT.
Campo 15 (VL_ICMS) – Preenchimento: corresponde ao campo Valor Total do ICMS, constante do leiaute do CF-e-SAT.
Validação: o valor informado neste campo deve ser igual à soma do campo VL_ICMS dos registros C850 (“filhos” deste
registro C800).
Campo 16 (VL_PIS_ST) – Preenchimento: corresponde ao campo Valor Total do PIS retido por substituição tributária,
constante do leiaute do CF-e-SAT. Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período de
apuração do registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
Campo 17 (VL_COFINS_ST) – Preenchimento: corresponde ao campo Valor Total do COFINS retido por substituição
tributária, constante do leiaute do CF-e-SAT. Os contribuintes que entregarem a EFD-Contribuições relativa ao mesmo período
de apuração do registro 0000 estão dispensados do preenchimento deste campo. Apresentar conteúdo VAZIO “||”.
----
# REGISTRO C810: ITENS DO DOCUMENTO DO CUPOM FISCAL ELETRÔNICO – SAT (CF-
E-SAT) (CÓDIGO 59):
Este registro deve ser informado apenas quando houver um registro filho C815.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C810” C 004 - Não O
apresentar
02 NUM_ITEM Número do item no documento fiscal N 003 - O
03 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - O
04 QTD Quantidade do item N - 05 O
05 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
06 VL_ITEM Valor total do item (mercadorias ou serviços) N 02 O
07 CST_ICMS Código da Situação Tributária referente ao N 003* - O
ICMS
08 CFOP Código Fiscal de Operação e Prestação N 004* - O
Observação:
Nível hierárquico - 3
Ocorrência 1:N
Campo 07 (CST_ICMS) – Preenchimento: o campo deverá ser preenchido com o código da Situação Tributária
correspondente ao informado no documento fiscal.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referenciada no item 4.3.1, da Nota
Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 08 (CFOP) - Preenchimento: informar o código de operação que consta no documento fiscal. O código CFOP deve
iniciar-se por “5”
----
# REGISTRO C815: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE SAÍDA DE
MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CF-E-SAT) (CÓDIGO 59)
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C815” C 004 - Não O
apresentar
02 COD_MOT_REST_COMPL Código do motivo da restituição ou C 005* - O
complementação conforme Tabela 5.7
03 QUANT_CONV Quantidade do item N - 06 O
04 UNID Unidade adotada para informar o campo C 006 - O
QUANT_CONV.
05 VL_UNIT_CONV Valor unitário da mercadoria, N - 06 O
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
06 VL_UNIT_ICMS_NA_OPE Valor unitário para o ICMS na operação, N - 06 OC
RACAO_CONV caso não houvesse a ST, considerando
unidade utilizada para informar o campo
“QUANT_CONV”, aplicando-se a mesma
redução da base de cálculo do ICMS ST na
tributação, se houver.
07 VL_UNIT_ICMS_OP_CON Valor unitário do ICMS OP calculado N - 06 OC
V conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”,
utilizado para cálculo de
ressarcimento/restituição de ST, no
desfazimento da substituição tributária,
quando se utiliza a fórmula descrita nas
instruções de preenchimento do campo 11,
no item a1).
08 VL_UNIT_ICMS_OP_EST Valor médio unitário do ICMS que o N - 06 OC
OQUE_CONV contribuinte teria se creditado referente à
operação de entrada das mercadorias em
estoque caso estivesse submetida ao
regime comum de tributação, calculado
conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”
09 VL_UNIT_ICMS_ST_ESTO Valor médio unitário do ICMS ST, N - 06 OC
QUE_CONV incluindo FCP ST, das mercadorias em
estoque, considerando unidade utilizada
para informar o campo
“QUANT_CONV”.
10 VL_UNIT_FCP_ICMS_ST_ Valor médio unitário do FCP ST N - 06 OC
ESTOQUE_CONV agregado ao ICMS das mercadorias em
estoque, considerando unidade utilizada
para informar o campo
“QUANT_CONV”.
11 VL_UNIT_ICMS_ST_CON Valor unitário do total do ICMS ST, N - 06 OC
V_REST incluindo FCP ST, a ser
restituído/ressarcido, calculado conforme
a legislação de cada UF, considerando a
unidade utilizada para informar o campo
“QUANT_CONV”.
12 VL_UNIT_FCP_ST_CONV Valor unitário correspondente à parcela N - 06 OC
_REST de ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_REST”,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
13 VL_UNIT_ICMS_ST_CON Valor unitário do complemento do ICMS, N - 06 OC
V_COMPL incluindo FCP ST, considerando a
unidade utilizada para informar o campo
“QUANT_CONV”.
14 VL_UNIT_FCP_ST_CONV Valor unitário correspondente à parcela N - 06 OC
_COMPL de ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_COMPL
”, considerando unidade utilizada para
informar o campo “QUANT_CONV”.
Observação:
Nível hierárquico - 4
Ocorrência 1:1
Campo 01 (REG) - Valor Válido: [C815]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere igual a 0, 1, 2 ou 3.
Se o terceiro caractere do código preenchido no campo “COD_MOT_REST_COMPL” for:
a) igual a 0, os campos 08, 09 e 10 devem ser preenchidos e os campos 06, 07, 11 a 14 não devem ser preenchidos.
b) igual a 1, os campos 06, 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 07, 13 e 14 não devem ser preenchidos.
c) igual a 2, os campos 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 06, 13 e 14 não devem ser preenchidos. O campo
07 pode ser preenchido de acordo com a legislação de cada UF.
d) igual a 3, os campos 06, 08, 09, 10, 13 e 14 devem ser preenchidos e os campos 07, 11 e 12 não devem ser preenchidos.
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: O campo UNID do registro pai não é necessariamente igual ao campo UNID deste
registro. No registro C810, deve corresponder à unidade de medida de comercialização do item utilizada no documento fiscal,
que pode não ser a unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (VL_UNIT_CONV) - Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos
e acréscimos incondicionais aplicados sobre o valor bruto) na unidade utilizada para informar o campo “QUANT_CONV”.
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV) – Preenchimento: Valor correspondente à multiplicação da
alíquota interna (incluindo FCP) (informado no registro 0200) da mercadoria pelo valor correspondente à operação de saída
que seria tributada se não houvesse ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”, aplicando-
se a mesma redução da base de cálculo do ICMS ST na tributação, se houver.
Campo 07 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: Nos casos de direito a crédito do imposto pela não ocorrência
do fato gerador presumido e desfazimento da ST, corresponde ao valor do ICMS da operação própria do sujeito passivo por
substituição do qual a mercadoria tenha sido recebida diretamente ou o valor do ICMS que seria atribuído à operação própria
do contribuinte substituído do qual a mercadoria tenha sido recebida, caso estivesse submetida ao regime comum de tributação,
calculado conforme a legislação de cada UF, considerando unidade utilizada para informar o campo “QUANT_CONV”.
Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor expresso no campo 12
(VL_UNIT_ICMS_OP_ESTOQUE_CONV), seu preenchimento será facultativo. O valor deste campo, quando obrigatório na
UF, será utilizado para o cálculo do valor do ressarcimento/restituição do Campo 15 (VL_UNIT_ICMS_ST_CONV_REST),
conforme fórmula abaixo:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário de ICMS OP, das
mercadorias em estoque.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV) - Preenchimento: Informar o valor médio unitário do ICMS ST,
incluindo FCP ST, pago ou retido, das mercadorias em estoque. Quando a mercadoria estiver sujeita ao FCP adicionado ao
ICMS ST, neste campo deve ser informado o valor médio unitário da parcela do ICMS ST + a parcela do FCP.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 10 (VL_UNIT_FCP_ CONV) -: Preenchimento: Informar o valor médio unitário da parcela do FCP adicionado ao
ICMS que tenha sido informado no campo “VL_UNIT_ICMS_ST_ESTOQUE_CONV”.
Campo 11 (VL_UNIT_ICMS_ST_CONV_REST) – Validação: O valor a ser ressarcido / restituído é calculado conforme as
orientações a seguir:
a) Nos casos de direito ao crédito do imposto, por não ocorrência do fato gerador presumido:
a.1) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) for obrigatório, de acordo com a legislação da UF, correspondente
ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
a.2) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) não for obrigatório, de acordo com a legislação da UF,
corresponde ao valor no campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
b) Nos casos de direito ao crédito do imposto, calculada com base no valor de saída da mercadoria inferior ao
valor da BC ICMS ST, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a
unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 12 (VL_UNIT_FCP_ST_CONV_REST) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza
(FCP) vinculado à substituição tributária que compõe o campo “ VL_UNIT_ICMS_ST_CONV_REST”, considerando a
unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL) – Validação: Nos casos de complemento, informar o valor unitário de
ICMS correspondente ao cálculo a seguir. O valor a ser ressarcido / restituído é calculado conforme as orientações a seguir:
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
- Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
- Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
= Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 14 (VL_UNIT_FCP_ST_CONV_COMPL) – Preenchimento: Informar o valor unitário do Fundo de Combate à
Pobreza (FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando a unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
----
# REGISTRO C850: REGISTRO ANALÍTICO DO CF-E-SAT (CODIGO 59)
Este registro tem por objetivo representar a escrituração do CF-e-SAT (código 59) segmentado por CST, CFOP e
Alíquota do ICMS.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C850" C 004 - O
02 CST_ICMS Código da Situação Tributária, conforme a Tabela N 003 -
O
indicada no item 4.3.1
03 CFOP Código Fiscal de Operação e Prestação do N 004 -
O
agrupamento de itens
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
05 VL_OPR “Valor total do CF-e” na combinação de CST_ICMS, N - 02
CFOP e alíquota do ICMS, correspondente ao O
Não
somatório do valor líquido dos itens.
apresentar
06 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS, N - 2
referente à combinação de CST_ICMS, CFOP, e O
alíquota do ICMS.
07 VL_ICMS Parcela correspondente ao “Valor do ICMS” referente N - 02
à combinação de CST_ICMS, CFOP e alíquota do O
ICMS.
08 COD_OBS Código da observação do lançamento fiscal (campo 02 C 006 -
OC
do registro 0460)
Observações:
Nível hierárquico: 3
Ocorrência – 1:N
Campo 01 (REG) - Valor Válido: [C850]
Validação: não poderão existir dois ou mais registros, para cada CF-e-SAT, para um mesmo conjunto CST_ICMS, CFOP e
ALIQ_ICMS.
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária do ICMS,
referenciada no item 4.3.1 da Nota Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
ICMS Normal:
a) se os dois últimos dígitos deste campo forem 40, 41, 50, ou 60, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS
e VL_ICMS deverão ser iguais a “0” (zero);
b) se os dois últimos dígitos deste campo forem iguais a 00, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS e
VL_ICMS deverão ser maiores que “0”(zero);
c) se os dois últimos dígitos deste campo forem iguais a 20 ou 90, então os valores dos campos VL_BC_ICMS, ALIQ_ICMS
e VL_ICMS deverão ser maiores ou iguais a “0”(zero);
Campo 03 (CFOP) - Preenchimento: pelo fato de o CF-e-SAT referir-se apenas a operações de saídas internas, deve ser
preenchido como CFOP iniciado por 5 (ex: 5102, 5405, etc.).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01 e iniciar com dígito “5”.
Campo 05 (VL_OPR) - Validação: O somatório dos valores deste campo, considerando todos os registros C850 de um
determinado CF-e-SAT, deve corresponder ao respectivo valor total do CF-e-SAT informado no reg. C800.
Campo 06 (VL_BC_ICMS) – Preenchimento: Tendo em vista o uso da alíquota efetiva, seu valor, caso seja maior que “0”,
corresponde ao valor indicado Campo 05.
Validação: Caso maior que “0” (zero), o somatório dos valores deste campo, considerando todos os registros C850 de um
determinado CF-e-SAT, deve corresponder ao valor total do CF-e-SAT informado no reg. C800.
Campo 07 (VL_ICMS) - Validação: O somatório dos valores deste campo, considerando todos os registros C850 de um
determinado CF-e-SAT, deve corresponder ao valor total do ICMS informado no reg. C800.
Campo 08 (COD_OBS) - Preenchimento: este campo só deve ser informado pelos contribuintes localizados em UF que
determine em sua legislação o seu preenchimento.
Validação: o código informado deve constar do registro 0460.
----
# REGISTRO C855: OBSERVAÇÕES DO LANÇAMENTO FISCAL (CÓDIGO 59)
Este registro deve ser informado quando, em decorrência da legislação estadual, houver ajustes nos documentos fiscais,
informações sobre diferencial de alíquota, antecipação de imposto e outras situações. Estas informações equivalem às
observações que são lançadas na coluna “Observações” dos Livros Fiscais previstos no Convênio SN/70 – SINIEF, art. 63, I a
IV.
Sempre que existir um ajuste (lançamentos referentes aos impostos que têm o cálculo detalhado em Informações
Complementares da NF; ou aos impostos que estão definidos na legislação e não constam na NF; ou aos recolhimentos
antecipados dos impostos), deve, conforme dispuser a legislação estadual, ocorrer uma observação.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C855" C 004 - O O
02 COD_OBS Código da observação do lançamento fiscal (campo 02 do C 006 - O O
Registro 0460)
03 TXT_COMPL Descrição complementar do código de observação. C - - OC OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C855]
Campo 02 (COD_OBS) – Preenchimento: as observações de lançamento devem ser informadas neste campo, exceto
quando a legislação estadual prever o preenchimento do campo COD_OBS do registro C850.
Validação: o código informado deve constar do registro 0460.
Campo 03 (TXT_COMPL) - Preenchimento: utilizado para complementar observação, cujo código é de informação genérica.
----
# REGISTRO C857: OUTRAS OBRIGAÇÕES TRIBUTÁRIAS, AJUSTES E INFORMAÇÕES DE
VALORES PROVENIENTES DE DOCUMENTO FISCAL.
Este registro tem por objetivo detalhar outras obrigações tributárias, ajustes e informações de valores do documento
fiscal do registro C855, que podem ou não alterar o cálculo do valor do imposto.
Os valores de ICMS ou ICMS ST (campo 07-VL_ICMS) serão somados diretamente na apuração, no registro E110 –
Apuração do ICMS – Operações Próprias, campo VL_AJ_DEBITOS ou campo VL_AJ_CREDITOS, e no registro E210 –
Apuração do ICMS – Substituição Tributária, campo VL_AJ_CREDITOS_ST e campo VL_AJ_DEBITOS_ST, de acordo com
a especificação do TERCEIRO CARACTERE do Código do Ajuste (Tabela 5.3 -Tabela de Ajustes e Valores provenientes do
Documento Fiscal).
Este registro será utilizado também por contribuinte para o qual a Administração Tributária Estadual exija, por meio
de legislação específica, apuração em separado (sub-apuração). Neste caso o Estado publicará a Tabela 5.3 com códigos que
contenham os dígitos “3”, “4”, “5”, “6”, “7” e “8” no quarto caractere (“Tipos de Apuração de ICMS”), sendo que cada um
dos dígitos possibilitará a escrituração de uma apuração em separado (sub-apuração) no registro 1900 e filhos. Para que haja a
apuração em separado do ICMS de determinadas operações ou itens de mercadorias, estes valores terão de ser estornados da
Apuração Normal (E110) e transferidos para as sub-apurações constantes do registro 1900 e filhos por meio de lançamentos de
ajustes neste registro. Isto ocorrerá quando:
1. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C857 for igual a “2 – Estorno de Débito” e
o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no campo
07 - VL_ICMS gerará um ajuste a crédito (campo 07- VL_AJ_CREDITOS) no registro E110 e também um
outro lançamento a débito no registro 1920 (campo 02 - VL_TOT_TRANSF_DEBITOS_OA) da apuração
em separado (sub-apuração) definida no campo 02- IND_APUR_ICMS do registro 1900 por meio dos
códigos “3”, “4”, “5”, “6”, “7” e “8”, que deverá coincidir com o quarto caractere do COD_AJ; e
2. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C857 for igual a “5 – Estorno de Crédito”
e o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gerará um ajuste a débito (campo 03- VL_AJ_DEBITOS) no registro E110 e
também um outro lançamento a crédito no registro 1920 (campo 05 -
VL_TOT_TRANSF_CRÉDITOS_OA) da apuração em separado (sub-apuração) que for definida no
campo 02 - IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4” “5”, “6”, “7” e “8”, que
deverá coincidir com o quarto caractere do COD_AJ.
Os valores que gerarem crédito ou débito de ICMS (ou seja, aqueles que não são simplesmente informativos) serão
somados na apuração, assim como os registros C850.
Este registro somente deve ser informado para as UF que publicarem a tabela constante no item 5.3 da Nota Técnica,
instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C857" C 004 - O O
02 COD_AJ Código do ajustes/benefício/incentivo, conforme C 010* - O O
tabela indicada no item 5.3.
03 DESCR_COMPL_AJ Descrição complementar do ajuste do documento C - - OC OC
fiscal
04 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC OC
05 VL_BC_ICMS Base de cálculo do ICMS ou do ICMS ST N - 02 OC OC
06 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
07 VL_ICMS Valor do ICMS ou do ICMS ST N - 02 OC OC
08 VL_OUTROS Outros valores N - 02 OC OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C857]
Campo 02 (COD_AJ) - Validação: verifica se o COD_AJ está de acordo com a Tabela da UF do informante do arquivo.
Campo 03 (DESCR_COMPL_AJ): Preenchimento: O contribuinte deverá fazer a descrição complementar de ajustes (tabela
5.3) sempre que informar códigos genéricos.
Campo 04 (COD_ITEM) - Preenchimento: deve ser informado se o ajuste/benefício for relacionado ao produto. O
COD_ITEM deverá ser informado no registro 0200.
Campo 07 (VL_ICMS) - Preenchimento: valor do montante do ajuste do imposto. Para ajustes referentes a ICMS ST, o campo
VL_ICMS deve conter o valor do ICMS ST. Os dados que gerarem crédito ou débito (ou seja, aqueles que não são simplesmente
informativos) serão somados na apuração, assim como os registros C850.
Campo 08 (VL_OUTROS) - Preenchimento: preencher com outros valores, quando o código do ajuste for informativo,
conforme Tabela 5.3.
----
# REGISTRO C860: IDENTIFICAÇÃO DO EQUIPAMENTO SAT-CF-E
Este registro tem por objetivo identificar os equipamentos SAT-CF-e e deve ser informado por todos os contribuintes
que utilizem tais equipamentos na emissão de documentos fiscais.
Validação do Registro: não poderão ser informados dois ou mais registros com a mesma combinação COD_MOD,
NR_SAT, DOC_INI e DOC_FIM.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C860" C 004 - Não O
02 COD_MOD Código do modelo do documento fiscal, conforme a C 002 - Apresentar O
Tabela 4.1.1
03 NR_SAT Número de Série do equipamento SAT N 009 - O
04 DT_DOC Data de emissão dos documentos fiscais N 008 - O
05 DOC_INI Número do documento inicial N 006 - O
06 DOC_FIM Número do documento final N 006 - O
Observações:
Nível hierárquico: 2
Ocorrência - vários (por arquivo)
Campo 01 (REG) - Valor Válido: [C860]
Validação: não poderão existir dois ou mais registros para o conjunto COD_MOD, NR_SAT, DOC_INI e DOC_FIM
Campo 02 (COD_MOD) – Preenchimento: deve corresponder ao código CF-e-SAT (Valor Válido: 59). Ver tabela
reproduzida na subseção 1.4 deste Guia.
Campo 04 (DT_DOC) - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se
quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve estar compreendido dentro das datas informadas no registro 0000. Para data
inferior ao período de apuração informado no registro 0000, o valor do ICMS informado no registro C890 será adicionado no
campo Débitos Especiais do registro E110.
Campo 05 (DOC_INI) - Preenchimento: informar o número do primeiro CF-e-SAT emitido, mesmo que cancelado, no
período, pelo equipamento.
Validação: o valor informado deve ser menor ou igual ao valor informado no Campo 6.
Campo 06 (DOC_FIM) - Preenchimento: informar o número do último CF-e-SAT emitido, mesmo que cancelado, no período,
pelo equipamento.
Validação: o valor informado deve ser maior ou igual ao valor informado no Campo 5.
----
# REGISTRO C870: ITENS DO RESUMO DIÁRIO DOS DOCUMENTOS (CF-E-SAT) (CÓDIGO 59)
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C870” C 004 - Não O
02 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - apresentar O
03 QTD Quantidade do item N - 05 O
04 UNID Unidade do item (Campo 02 do registro 0190) C 006 - O
05 CST_ICMS Código da Situação Tributária referente ao ICMS N 003* - O
06 CFOP Código Fiscal de Operação e Prestação N 004* - O
Observação:
Nível hierárquico - 3
Ocorrência 1:N
Campo 01 (REG) - Valor Válido: [C870]
Campo 02 (COD_ITEM) - Validação: o valor informado neste campo deve existir no registro 0200 e constantes do documento
fiscal.
Campo 03 (QTD) - Preenchimento: informar a quantidade do item constante no documento fiscal expressa na unidade de
medida informada no campo UNID.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: informar a unidade de medida de comercialização do item utilizada no documento fiscal.
Caso a unidade de medida do documento fiscal seja diferente da unidade de medida de controle de estoque informada no
Registro 0200, deverá ser informado no Registro 0220 o fator de conversão entre as unidades de medida.
Validação: o valor informado neste campo deve existir no registro 0190.
Campo 05 (CST_ICMS) – Preenchimento: o campo deverá ser preenchido com o código da Situação Tributária
correspondente ao informado no documento fiscal.
Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referenciada no item 4.3.1, da Nota
Técnica, instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 06 (CFOP) - Preenchimento: informar o código de operação que consta no documento fiscal. O código CFOP deve
iniciar-se por “5”.
----
# REGISTRO C880: INFORMAÇÕES COMPLEMENTARES DAS OPERAÇÕES DE SAÍDA DE
MERCADORIAS SUJEITAS À SUBSTITUIÇÃO TRIBUTÁRIA (CF-E-SAT) (CÓDIGO 59)
A obrigatoriedade e a forma de escrituração deste registro serão definidas pela UF de domicílio do contribuinte.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C880” C 004 - Não O
02 COD_MOT_REST_COMPL Código do motivo da restituição ou C 005* - apresentar O
complementação conforme Tabela 5.7
03 QUANT_CONV Quantidade do item N - 06 O
04 UNID Unidade adotada para informar o campo C 006 - O
QUANT_CONV.
05 VL_UNIT_CONV Valor unitário da mercadoria, considerando a N - 03 O
unidade utilizada para informar o campo
“QUANT_CONV”.
06 VL_UNIT_ICMS_NA_OPE Valor unitário para o ICMS na operação, N - 03 OC
RACAO_CONV caso não houvesse a ST, considerando
unidade utilizada para informar o campo
“QUANT_CONV”, aplicando-se a mesma
redução da base de cálculo do ICMS ST na
tributação, se houver.
07 VL_UNIT_ICMS_OP_CON Valor unitário do ICMS OP calculado N - 03 OC
V conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”,
utilizado para cálculo de
ressarcimento/restituição de ST, no
desfazimento da substituição tributária,
quando se utiliza a fórmula descrita nas
instruções de preenchimento do campo 11,
no item a1).
08 VL_UNIT_ICMS_OP_EST Valor médio unitário do ICMS que o N - 03 OC
OQUE_CONV contribuinte teria se creditado referente à
operação de entrada das mercadorias em
estoque caso estivesse submetida ao regime
comum de tributação, calculado conforme a
legislação de cada UF, considerando a
unidade utilizada para informar o campo
“QUANT_CONV”
09 VL_UNIT_ICMS_ST_EST Valor médio unitário do ICMS ST, N - 03 OC
OQUE_CONV incluindo FCP ST, das mercadorias em
estoque, considerando unidade utilizada
para informar o campo “QUANT_CONV”.
10 VL_UNIT_FCP_ICMS_ST_ Valor médio unitário do FCP ST agregado N - 03 OC
ESTOQUE_CONV ao ICMS das mercadorias em estoque,
considerando unidade utilizada para
informar o campo “QUANT_CONV”.
11 VL_UNIT_ICMS_ST_CON Valor unitário do total do ICMS ST, N - 03 OC
V_REST incluindo FCP ST, a ser restituído/ressarcido,
calculado conforme a legislação de cada UF,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
12 VL_UNIT_FCP_ST_CONV Valor unitário correspondente à parcela de N - 03 OC
_REST ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_REST”,
considerando a unidade utilizada para
informar o campo “QUANT_CONV”.
13 VL_UNIT_ICMS_ST_CON Valor unitário do complemento do ICMS, N - 03 OC
V_COMPL incluindo FCP ST, considerando a unidade
utilizada para informar o campo
“QUANT_CONV”.
14 VL_UNIT_FCP_ST_CONV Valor unitário correspondente à parcela de N - 03 OC
_COMPL ICMS FCP ST que compõe o campo
“VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando unidade utilizada para
informar o campo “QUANT_CONV”.
Observação:
Nível hierárquico - 4
Ocorrência 1:1
Campo 01 (REG) - Valor Válido: [C880]
Campo 02 (COD_MOT_REST_COMPL) - Validação: o valor informado deve estar de acordo com a tabela 5.7 publicada
pela UF do informante do arquivo com o terceiro caractere igual a 0, 1, 2 ou 3.
Se o terceiro caractere do código preenchido no campo “COD_MOT_REST_COMPL” for:
a) igual a 0, os campos 08, 09 e 10 devem ser preenchidos e os campos 06, 07, 11 a 14 não devem ser preenchidos.
b) igual a 1, os campos 06, 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 07, 13 e 14 não devem ser preenchidos.
c) igual a 2, os campos 08, 09, 10, 11 e 12 devem ser preenchidos e os campos 06, 13 e 14 não devem ser preenchidos. O campo
07 pode ser preenchido de acordo com a legislação de cada UF.
d) igual a 3, os campos 06, 08, 09, 10, 13 e 14 devem ser preenchidos e os campos 07, 11 e 12 não devem ser preenchidos.
Campo 03 (QUANT_CONV) – Preenchimento: Quantidade do item convertida na unidade de controle de estoque informada
no registro 0200 ou na unidade de comercialização, a critério de cada UF.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (UNID) - Preenchimento: O campo UNID do registro pai não é necessariamente igual ao campo UNID deste
registro. No registro C870, deve corresponder à unidade de medida de comercialização do item utilizada no documento fiscal,
que pode não ser a unidade adotada para o cálculo do ressarcimento/restituição de ICMS ST.
Validação: o valor informado neste campo deve existir no registro 0190. Caso a unidade de medida informada seja diferente
da unidade de medida de controle de estoque informada no Registro 0200, deverá ser informado no Registro 0220 o fator de
conversão entre as unidades de medida.
Campo 05 (VL_UNIT_CONV) - Preenchimento: informar o valor unitário líquido do item/produto (considerando descontos e
acréscimos incondicionais aplicados sobre o valor bruto) na unidade utilizada para informar o campo “QUANT_CONV”.
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV) – Preenchimento: Valor correspondente à multiplicação da
alíquota interna (incluindo FCP) (informado no registro 0200) da mercadoria pelo valor correspondente à operação de saída
que seria tributada se não houvesse ST, considerando a unidade utilizada para informar o campo “QUANT_CONV”, aplicando-
se a mesma redução da base de cálculo do ICMS ST na tributação, se houver.
Campo 07 (VL_UNIT_ICMS_OP_CONV) – Preenchimento: Nos casos de direito a crédito do imposto pela não ocorrência
do fato gerador presumido e desfazimento da ST, corresponde ao valor do ICMS da operação própria do sujeito passivo por
substituição do qual a mercadoria tenha sido recebida diretamente ou o valor do ICMS que seria atribuído à operação própria
do contribuinte substituído do qual a mercadoria tenha sido recebida, caso estivesse submetida ao regime comum de tributação,
calculado conforme a legislação de cada UF, considerando unidade utilizada para informar o campo “QUANT_CONV”.
Para as UFs em que a legislação estabelecer que o valor desse campo corresponderá ao mesmo valor expresso no campo 12
(VL_UNIT_ICMS_OP_ESTOQUE_CONV), seu preenchimento será facultativo. O valor deste campo, quando obrigatório na
UF, será utilizado para o cálculo do valor do ressarcimento/restituição do Campo 15 (VL_UNIT_ICMS_ST_CONV_REST),
conforme fórmula abaixo:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV): Preenchimento: Informar o valor médio unitário de ICMS OP, das
mercadorias em estoque.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV) - Preenchimento: Informar o valor médio unitário do ICMS ST,
incluindo FCP ST, pago ou retido, das mercadorias em estoque. Quando a mercadoria estiver sujeita ao FCP adicionado ao
ICMS ST, neste campo deve ser informado o valor médio unitário da parcela do ICMS ST + a parcela do FCP.
O período para o cálculo do valor médio deve atender à legislação de cada UF. Exemplo: diário, mensal etc.
Campo 10 (VL_UNIT_FCP_ CONV) -: Preenchimento: Informar o valor médio unitário da parcela do FCP adicionado ao
ICMS que tenha sido informado no campo “VL_UNIT_ICMS_ST_ESTOQUE_CONV”.
Campo 11 (VL_UNIT_ICMS_ST_CONV_REST) – Validação: O valor a ser ressarcido / restituído é calculado conforme as
orientações a seguir:
a) Nos casos de direito ao crédito do imposto, por não ocorrência do fato gerador presumido:
a.1) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) for obrigatório, de acordo com a legislação da UF, correspondente
ao seguinte cálculo, considerando a unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 07 (VL_UNIT_ICMS_OP_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
a.2) Quando o campo 07 (VL_UNIT_ICMS_OP_CONV) não for obrigatório, de acordo com a legislação da UF,
corresponde ao valor no campo 13 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
b) Nos casos de direito ao crédito do imposto, calculada com base no valor de saída da mercadoria inferior ao
valor da BC ICMS ST, informar o valor unitário de ICMS correspondente ao seguinte cálculo, considerando a
unidade utilizada para informar o campo “QUANT_CONV”:
Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
+ Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
- Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
= Campo 11 (VL_UNIT_ICMS_ST_CONV_REST)
Campo 12 (VL_UNIT_FCP_ST_CONV_REST) – Preenchimento: Informar o valor unitário do Fundo de Combate à Pobreza
(FCP) vinculado à substituição tributária que compõe o campo “ VL_UNIT_ICMS_ST_CONV_REST”, considerando a
unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL) – Validação: Nos casos de complemento, informar o valor unitário de
ICMS correspondente ao cálculo a seguir. O valor a ser ressarcido / restituído é calculado conforme as orientações a seguir:
Campo 06 (VL_UNIT_ICMS_NA_OPERACAO_CONV)
- Campo 08 (VL_UNIT_ICMS_OP_ESTOQUE_CONV)
- Campo 09 (VL_UNIT_ICMS_ST_ESTOQUE_CONV)
= Campo 13 (VL_UNIT_ICMS_ST_CONV_COMPL)
Campo 14 (VL_UNIT_FCP_ST_CONV_COMPL) – Preenchimento: Informar o valor unitário do Fundo de Combate à
Pobreza (FCP) vinculado à substituição tributária que compõe o campo “VL_UNIT_ICMS_ST_CONV_COMPL”,
considerando a unidade utilizada para informar o campo “QUANT_CONV”, conforme previsão das legislações das UF.
----
# REGISTRO C890: RESUMO DIÁRIO DO CF-E-SAT (CÓDIGO 59) POR EQUIPAMENTO SAT-
CF-E
Este registro tem por objetivo promover a consolidação dos CF-e-SAT emitidos no período, por equipamento SAT-
CF-e.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C890" C 004 - O
02 CST_ICMS Código da Situação Tributária, conforme a Tabela N 003 - O
indicada no item 4.3.1 Não
03 CFOP Código Fiscal de Operação e Prestação do agrupamento N 004 - apresentar O
de itens
04 ALIQ_ICMS Alíquota do ICMS N 006 02 OC
05 VL_OPR “Valor total do CF-e” na combinação de CST_ICMS, N - 02 O
CFOP e ALÍQUOTA DO ICMS, correspondente ao
somatório do valor líquido dos itens.
06 VL_BC_ICMS Valor acumulado da base de cálculo do ICMS, referente N - 02 O
à combinação de CST_ICMS, CFOP e ALÍQUOTA
DO ICMS.
07 VL_ICMS Parcela correspondente ao "Valor do ICMS" referente à N - 02 O
combinação de CST_ICMS, CFOP e alíquota do ICMS.
08 COD_OBS Código da observação do lançamento fiscal (campo 02 C 006 - OC
do registro 0460)
Observações:
Nível hierárquico: 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C890]
Validação: não poderão existir dois ou mais registros para o conjunto DT_DOC, NR_SAT, CST_ICMS, CFOP e ALIQ_ICMS.
Campo 02 (CST_ICMS) - Validação: o valor informado no campo deve existir na Tabela da Situação Tributária referente ao
ICMS, constante do Artigo 5º do Convênio SN/70.
Campo 03 (CFOP) - Preenchimento: pelo fato de o CF-e-SAT referir-se apenas a operações de saídas internas, deve ser
preenchido com CFOP iniciado por 5 (ex: 5102, 5405, etc.).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme Ajuste
SINIEF 07/01 e iniciar com dígito “5”.
Campo 05 (VL_OPR) - Preenchimento: O valor deste campo deve corresponder ao somatório do Valor da Operação de todos
os registros informados no reg. C860, respeitando-se o agrupamento por DT_DOC, NR_SAT, CST_ICMS, CFOP e
ALIQ_ICMS.
Campo 06 (VL_BC_ICMS) - Preenchimento: O valor deste campo deve corresponder ao somatório do valor total da Base de
Cálculo do ICMS de todos os registros informados no reg. C860, respeitando-se o agrupamento por DT_DOC, NR_SAT,
CST_ICMS, CFOP e ALIQ_ICMS.
Campo 07 (VL_ICMS) - Preenchimento: O valor deste campo deve corresponder ao somatório do Valor Total do ICMS de
todos os registros informados no reg. C860, respeitando-se o agrupamento por DT_DOC, NR_SAT, CST_ICMS, CFOP e
ALIQ_ICMS.
Campo 08 (COD_OBS) - Preenchimento: este campo só deve ser informado pelos contribuintes localizados em UF que
determine em sua legislação o seu preenchimento.
Validação: o código informado deve constar do registro 0460.
----
# REGISTRO C895: OBSERVAÇÕES DO LANÇAMENTO FISCAL (CÓDIGO 59)
Este registro deve ser informado quando, em decorrência da legislação estadual, houver ajustes nos documentos fiscais,
informações sobre diferencial de alíquota, antecipação de imposto e outras situações. Estas informações equivalem às
observações que são lançadas na coluna “Observações” dos Livros Fiscais previstos no Convênio SN/70 – SINIEF, art. 63, I a
IV.
Sempre que existir um ajuste (lançamentos referentes aos impostos que têm o cálculo detalhado em Informações
Complementares da NF; ou aos impostos que estão definidos na legislação e não constam na NF; ou aos recolhimentos
antecipados dos impostos), deve, conforme dispuser a legislação estadual, ocorrer uma observação.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C895" C 004 - O O
02 COD_OBS Código da observação do lançamento fiscal (campo 02 do C 006 - O O
Registro 0460)
03 TXT_COMPL Descrição complementar do código de observação. C - - OC OC
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C895]
Campo 02 (COD_OBS) – Preenchimento: as observações de lançamento devem ser informadas neste campo, exceto
quando a legislação estadual prever o preenchimento do campo COD_OBS do registro C890.
Validação: o código informado deve constar do registro 0460.
Campo 03 (TXT_COMPL) - Preenchimento: utilizado para complementar observação, cujo código é de informação genérica.
----
# REGISTRO C897: OUTRAS OBRIGAÇÕES TRIBUTÁRIAS, AJUSTES E INFORMAÇÕES DE
VALORES PROVENIENTES DE DOCUMENTO FISCAL.
Este registro tem por objetivo detalhar outras obrigações tributárias, ajustes e informações de valores do documento
fiscal do registro C895, que podem ou não alterar o cálculo do valor do imposto.
Os valores de ICMS ou ICMS ST (campo 07-VL_ICMS) serão somados diretamente na apuração, no registro E110 –
Apuração do ICMS – Operações Próprias, campo VL_AJ_DEBITOS ou campo VL_AJ_CREDITOS, e no registro E210 –
Apuração do ICMS – Substituição Tributária, campo VL_AJ_CREDITOS_ST e campo VL_AJ_DEBITOS_ST, de acordo com
a especificação do TERCEIRO CARACTERE do Código do Ajuste (Tabela 5.3 -Tabela de Ajustes e Valores provenientes do
Documento Fiscal).
Este registro será utilizado também por contribuinte para o qual a Administração Tributária Estadual exija, por meio
de legislação específica, apuração em separado (sub-apuração). Neste caso o Estado publicará a Tabela 5.3 com códigos que
contenham os dígitos “3”, “4”, “5”, “6”, “7” e “8” no quarto caractere (“Tipos de Apuração de ICMS”), sendo que cada um
dos dígitos possibilitará a escrituração de uma apuração em separado (sub-apuração) no registro 1900 e filhos. Para que haja a
apuração em separado do ICMS de determinadas operações ou itens de mercadorias, estes valores terão de ser estornados da
Apuração Normal (E110) e transferidos para as sub-apurações constantes do registro 1900 e filhos por meio de lançamentos de
ajustes neste registro. Isto ocorrerá quando:
1. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C897 for igual a “2 – Estorno de Débito” e
o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no campo
07 - VL_ICMS gerará um ajuste a crédito (campo 07- VL_AJ_CREDITOS) no registro E110 e também um
outro lançamento a débito no registro 1920 (campo 02 - VL_TOT_TRANSF_DEBITOS_OA) da apuração
em separado (sub-apuração) definida no campo 02- IND_APUR_ICMS do registro 1900 por meio dos
códigos “3”, “4”, “5”, “6”, “7” e “8”, que deverá coincidir com o quarto caractere do COD_AJ; e
2. o terceiro caractere do código de ajuste (tabela 5.3) do reg. C897 for igual a “5 – Estorno de Crédito”
e o dígito do quarto caractere for igual a “3”; “4”, “5”, “6”, “7” e “8”. Neste caso o valor informado no
campo 07 - VL_ICMS gerará um ajuste a débito (campo 03- VL_AJ_DEBITOS) no registro E110 e
também um outro lançamento a crédito no registro 1920 (campo 05 -
VL_TOT_TRANSF_CRÉDITOS_OA) da apuração em separado (sub-apuração) que for definida no
campo 02 - IND_APUR_ICMS do registro 1900 por meio dos códigos “3”, “4” “5”, “6”, “7” e “8”, que
deverá coincidir com o quarto caractere do COD_AJ.
Os valores que gerarem crédito ou débito de ICMS (ou seja, aqueles que não são simplesmente informativos) serão
somados na apuração, assim como os registros C890.
Este registro somente deve ser informado para as UF que publicarem a tabela constante no item 5.3 da Nota Técnica,
instituída pelo Ato COTEPE/ICMS nº 44/2018 e alterações.
Nº Campo Descrição Tipo Tam Dec Entr Saída
01 REG Texto fixo contendo "C897" C 004 - O O
02 COD_AJ Código do ajustes/benefício/incentivo, conforme C 010* - O O
tabela indicada no item 5.3.
03 DESCR_COMPL_AJ Descrição complementar do ajuste do documento C - - OC OC
fiscal
04 COD_ITEM Código do item (campo 02 do Registro 0200) C 060 - OC OC
05 VL_BC_ICMS Base de cálculo do ICMS ou do ICMS ST N - 02 OC OC
06 ALIQ_ICMS Alíquota do ICMS N 006 02 OC OC
07 VL_ICMS Valor do ICMS ou do ICMS ST N - 02 OC OC
08 VL_OUTROS Outros valores N - 02 OC OC
Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [C897]
Campo 02 (COD_AJ) - Validação: verifica se o COD_AJ está de acordo com a Tabela da UF do informante do arquivo.
Campo 03 (DESCR_COMPL_AJ): Preenchimento: O contribuinte deverá fazer a descrição complementar de ajustes (tabela
5.3) sempre que informar códigos genéricos.
Campo 04 (COD_ITEM) - Preenchimento: deve ser informado se o ajuste/benefício for relacionado ao produto. O
COD_ITEM deverá ser informado no registro 0200.
Campo 07 (VL_ICMS) - Preenchimento: valor do montante do ajuste do imposto. Para ajustes referentes a ICMS ST, o campo
VL_ICMS deve conter o valor do ICMS ST. Os dados que gerarem crédito ou débito (ou seja, aqueles que não são simplesmente
informativos) serão somados na apuração, assim como os registros C850.
Campo 08 (VL_OUTROS) - Preenchimento: preencher com outros valores, quando o código do ajuste for informativo,
conforme Tabela 5.3.
----
# REGISTRO C990: ENCERRAMENTO DO BLOCO C
Este registro destina-se a identificar o encerramento do bloco C e informar a quantidade de linhas (registros)
existentes no bloco.
Validação do Registro: registro único e obrigatório para todos os informantes da EFD-ICMS/IPI.
Nº Campo Descrição Tipo Tam Dec Entr Saida
01 REG Texto fixo contendo "C990" C 004 - O O
02 QTD_LIN_C Quantidade total de linhas do Bloco C N - - O O
Observações: Registro obrigatório
Nível hierárquico - 1
Ocorrência – um por arquivo
Campo 01 (REG) - Valor Válido: [C990]
Campo 02 (QTD_LIN_C) - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios
registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco C é igual ao valor informado no campo QTD_LIN_C (registro
C990).
BLOCO D: DOCUMENTOS FISCAIS II - SERVIÇOS (ICMS)
Bloco de registros dos dados relativos à emissão ou ao recebimento de documentos fiscais que acobertam as prestações
de serviços de comunicação, transporte intermunicipal e interestadual.
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
Preenchimento: quando houver aquisições ou prestações de serviços de comunicação, transporte interestadual e intermunicipal,
deve-se gerar esse bloco utilizando a opção 0. Quando não houver aquisições ou prestações de serviços de comunicação,
transporte interestadual e intermunicipal, deve-se gerar esse bloco com a opção 1.
REGISTRO D100: NOTA FISCAL DE SERVIÇO DE TRANSPORTE (CÓDIGO 07) E
CONHECIMENTOS DE TRANSPORTE RODOVIÁRIO DE CARGAS (CÓDIGO 08),
CONHECIMENTOS DE TRANSPORTE DE CARGAS AVULSO (CÓDIGO 8B), AQUAVIÁRIO
DE CARGAS (CÓDIGO 09), AÉREO (CÓDIGO 10), FERROVIÁRIO DE CARGAS (CÓDIGO
11), MULTIMODAL DE CARGAS (CÓDIGO 26), NOTA FISCAL DE TRANSPORTE
FERROVIÁRIO DE CARGA (CÓDIGO 27), CONHECIMENTO DE TRANSPORTE
ELETRÔNICO – CT-e (CÓDIGO 57), CONHECIMENTO DE TRANSPORTE ELETRÔNICO
PARA OUTROS SERVIÇOS - CT-e OS (CÓDIGO 67) E BILHETE DE PASSAGEM
ELETRÔNICO – BP-e (CÓDIGO 63)
Este registro deve ser apresentado por todos os contribuintes adquirentes ou prestadores dos serviços que utilizem os
documentos especificados.
O campo CHV_CTE passa a ser de preenchimento obrigatório a partir de abril de 2012 em todas as situações, exceto para COD_SIT
= 5 (numeração inutilizada).
A partir da vigência do Ajuste SINIEF 28/2021 e 39/2021 (01/12/2021) deixa de ser obrigatória a informação referente
aos documentos fiscais eletrônicos denegados ou com numeração inutilizada.
A partir de janeiro de 2023, os códigos de situação de documento 04 (NF-e ou CT-e denegado) e 05 (NF-e ou CT-e
Numeração inutilizada) da tabela 4.1.2 - Tabela Situação do Documento serão descontinuados.
Página 171 de 361
