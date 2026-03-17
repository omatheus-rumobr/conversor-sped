# Bloco 1 - Versão 1.35

BLOCO 1: Complemento da Escrituração – Controle de Saldos de Créditos e de Retenções, Operações Extemporâneas e Outras Informações
Os registros componentes dos Blocos "1"  são escriturados na visão da empresa, nos quais serão relacionadas informações referentes a processos administrativos e judiciais envolvendo o PIS/Pasep e a Cofins, o controle dos saldos de créditos da não cumulatividade, o controle dos saldos de retenções na fonte, as operações extemporâneas, bem como as contribuições devidas pelas empresa da atividade imobiliária pelo RET.
<!-- Start Registro 1001 -->
Registro 1001: Abertura do Bloco 1

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1001" | C | 004* | - | S |
| 02 | IND_MOV | Indicador de movimento: 0 - Bloco com dados informados; 1 - Bloco sem dados informados | N | 001* | - | S |

Observações:
Nível hierárquico – 1
Ocorrência - um (por arquivo)
Campo 01 - Valor Válido: [1001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro 1001 -->
<!-- Start Registro 1010 -->
Registro 1010: Processo Referenciado – Ação Judicial
Uma vez procedida à escrituração de Registros referentes à Processo Referenciado vinculado a uma ação judicial, deve a pessoa jurídica gerar tantos registros “1010” quantas ações judiciais forem utilizadas no período da escrituração, referentes ao detalhamento do(s) processo(s) judicial(is), que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1010" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do Número do Processo Judicial | C | 020 | - | S |
| 03 | ID_SEC_JUD | Identificação da Seção Judiciária | C | - | - | S |
| 04 | ID_VARA | Identificação da Vara | C | 002 | - | S |
| 05 | IND_NAT_ACAO | Indicador da Natureza da Ação Judicial, impetrada na Justiça Federal: 01 – Decisão judicial transitada em julgado, a favor da pessoa jurídica. 02 – Decisão judicial não transitada em julgado, a favor da pessoa jurídica. 03 – Decisão judicial oriunda de liminar em mandado de segurança. 04 – Decisão judicial oriunda de liminar em medida cautelar. 05 – Decisão judicial oriunda de antecipação de tutela. 06 - Decisão judicial vinculada a depósito administrativo ou judicial em montante integral. 07 – Medida judicial em que a pessoa jurídica não é o autor. 08 – Súmula vinculante aprovada pelo STF ou STJ. 09 – Decisão judicial oriunda de liminar em mandado de segurança coletivo. 12 – Decisão judicial não transitada em julgado, a favor da pessoa jurídica - Exigibilidade suspensa de contribuição.  13 – Decisão judicial oriunda de liminar em mandado de segurança - Exigibilidade suspensa de contribuição.  14 – Decisão judicial oriunda de liminar em medida cautelar - Exigibilidade suspensa de contribuição.  15 – Decisão judicial oriunda de antecipação de tutela - Exigibilidade suspensa de contribuição.  16 - Decisão judicial vinculada a depósito administrativo ou judicial em montante integral - Exigibilidade suspensa de contribuição.  17 – Medida judicial em que a pessoa jurídica não é o autor - Exigibilidade suspensa de contribuição.  19 – Decisão judicial oriunda de liminar em mandado de segurança coletivo - Exigibilidade suspensa de contribuição. 99 - Outros. | C | 002* | - | S |
| 06 | DESC_DEC_JUD | Descrição Resumida dos Efeitos Tributários abrangidos pela Decisão Judicial proferida. | C | 100 | - | N |
| 07 | DT_SENT_JUD | Data da Sentença/Decisão Judicial | N | 008* | - | N |

Observações:
1. A apuração da Contribuição para o PIS/Pasep e da Cofins mediante a escrituração dos valores componentes da base de cálculo mensal, da alíquota da contribuição ou de tratamento tributário (CST) diversos dos definidos pela legislação tributária, tendo por lastro e fundamento uma decisão judicial, só devem ser considerados na apuração e escrituração das referidas contribuições, caso a decisão judicial correspondente esteja com trânsito em julgado.
2. A apuração da Contribuição para o PIS/Pasep e da Cofins a recolher em cada período, demonstrada nos registros M200 (PIS/Pasep) e M600 (Cofins) deve corresponder e guardar uniformidade com os valores a serem declarados mensalmente na DCTF, segundo as normas disciplinadoras estabelecidas na Instrução Normativa RFB nº 1.599/2015.
3. Caso a pessoa jurídica seja titular ou beneficiária de decisão judicial que autoriza a suspensão da exigibilidade de parte do valor das contribuições, ou de seu valor integral, porém a decisão judicial não se encontra com o trânsito em julgado, deve a pessoa jurídica proceder à apuração das contribuições conforme a legislação aplicável, inclusive considerando a parcela que esteja com exigibilidade suspensa e, informar no Campo 06 (DESC_DEC_JUD) deste registro a parcela das contribuições com exigibilidade suspensa, a qual deve ser igualmente destacada e informada em DCTF. A partir do período de apuração Janeiro/2020, ao informar um dos códigos de 12 a 19 no campo 05 deste registro, deve a pessoa jurídica proceder à apuração das contribuições conforme a legislação aplicável, inclusive considerando a parcela que esteja com exigibilidade suspensa e, detalhar no registro filho “1011 - - Detalhamento das Contribuições com Exigibilidade Suspensa” a parcela das contribuições com exigibilidade suspensa, a qual deve ser igualmente destacada e informada em DCTF.
Exemplo: Caso a aplicação da decisão judicial sem trânsito em julgado resulte em valor da Contribuição para o PIS/Pasep e da Cofins com exigibilidade suspensa de R$ 10.000,00 e de R$ 18.000,00, respectivamente, o Registro 1010 será assim escriturado:
Campo 01: Identificação do registro
Campo 02: Identificação do processo judicial
Campo 03: Identificação da Seção Judiciária
Campo 04: Identificação da Vara
Campo 05: Identificação da natureza da ação judicial (Indicador 02 – Decisão judicial não transitada em julgado)
Campo 06: Valores com exigibilidade suspensa, conforme código de receita a informar nos registros M205/M605 e na DCTF
Campo 07: Data da decisão judicial
Representação gráfica do registro – Formato txt:
|1010|xxxxxxx-xx.2016.1.00.0000|TRF3|10|02|6912/01=R$10.000,00 e 5856/01=R$18.000,00|20032019|
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [1010]
Campo 02 - Preenchimento: informar o número do processo judicial que autoriza a adoção de procedimento específico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Preenchimento: informar a seção judiciária onde foi ajuizado processo judicial
Campo 04 - Preenchimento: informar a vara da seção judiciária onde foi ajuizado o processo judicial
Campo 05 - Valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 99]
Campo 06 - Preenchimento: utilizar este campo para descrever os efeitos tributários abrangidos pela decisão judicial proferida. Identificar, por exemplo, se os efeitos são em relação a alíquotas, CST, base de cálculo de operações sujeitas às contribuições ou com direito a crédito, bem como os demais efeitos da decisão proferida. Também deve ser aqui informada a parcela das contribuições com exigibilidade suspensa, a qual deve ser igualmente destacada e informada em DCTF.
Campo 07 - Preenchimento: informar a data da sentença/decisão judicial, no formato "ddmmaaaa", excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
Validação: a informação da data é essencial para a validação do processo judicial e de seus efeitos.
<!-- End Registro 1010 -->
<!-- Start Registro 1011 -->
Registro 1011: Detalhamento das Contribuições com Exigibilidade Suspensa
Deverá ser escriturado pelo menos um registro 1011 para cada uma das ações judiciais escrituradas no registro 1010 que se refira à decisão judicial que autoriza a suspensão da exigibilidade de parte do valor das contribuições, ou de seu valor integral, porém sem o trânsito em julgado.
Este registro está disponível apenas para as escriturações criadas a partir do leiaute VI da EFD-Contribuições, válido a partir de janeiro/2020.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1011" | C | 004* | - | S |
| 02 | REG_REF | Registro da escrituração que terá o detalhamento das contribuições sociais com exigibilidade suspensa (Blocos A, C, D, F e I, 1800) | C | 004* | - | N |
| 03 | CHAVE_DOC | Chave do documento eletrônico | C | 090 | - | N |
| 04 | COD_PART | Código do participante (Campo 02 do Registro 0150) | C | 060 | - | N |
| 05 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 06 | DT_OPER | Data da Operação (ddmmaaaa) | N | 008* | - | S |
| 07 | VL_OPER | Valor da Operação/Item | N | - | 02 | S |
| 08 | CST_PIS | Código da Situação Tributária conforme escrituração, referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 09 | VL_BC_PIS | Base de cálculo do PIS/PASEP, conforme escrituração | N | - | 04 | N |
| 10 | ALIQ_PIS | Alíquota do PIS/PASEP, conforme escrituração | N | 008 | 04 | N |
| 11 | VL_PIS | Valor do PIS/PASEP, conforme escrituração | N | - | 02 | N |
| 12 | CST_COFINS | Código da Situação Tributária conforme escrituração, referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 13 | VL_BC_COFINS | Base de cálculo da COFINS, conforme escrituração | N | - | 04 | N |
| 14 | ALIQ_COFINS | Alíquota da COFINS, conforme escrituração | N | 008 | 04 | N |
| 15 | VL_COFINS | Valor da COFINS, conforme escrituração | N | - | 02 | N |
| 16 | CST_PIS_SUSP | Código da Situação Tributária conforme decisão judicial, referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 17 | VL_BC_PIS_SUSP | Base de cálculo do PIS/PASEP, conforme decisão judicial | N | - | 04 | N |
| 18 | ALIQ_PIS_SUSP | Alíquota do PIS/PASEP, conforme decisão judicial | N | 008 | 04 | N |
| 19 | VL_PIS_SUSP | Valor do PIS/PASEP, conforme decisão judicial | N | - | 02 | N |
| 20 | CST_COFINS_SUSP | Código da Situação Tributária conforme decisão judicial, referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 21 | VL_BC_COFINS_SUSP | Base de cálculo da COFINS, conforme decisão judicial | N | - | 04 | N |
| 22 | ALIQ_COFINS_SUSP | Alíquota da COFINS, conforme decisão judicial | N | 008 | 04 | N |
| 23 | VL_COFINS_SUSP | Valor da COFINS, conforme decisão judicial | N | - | 02 | N |
| 24 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 25 | COD_CCUS | Código do Centro de Custos | C | 255 | - | N |
| 26 | DESC_DOC_OPER | Descrição do Documento/Operação | C | - | - | N |

Nível hierárquico - 3
Ocorrência – 1:N
Observações:
Os tratamentos tributários definidos na decisão judicial devem ser refletidos nos respectivos campos de “Código da Situação Tributária”, “Base de cálculo” e/ou “Alíquota”.  O registro disponibiliza dois grupos destes campos. O primeiro, nos campos 08-14, refere-se aos códigos e valores escriturados conforme a legislação vigente. O segundo, nos campos 16-22, é específico para escriturar os códigos e valores conforme a decisão judicial. Dessa forma, caso a decisão judicial não afete um determinado campo de “Código da Situação Tributária”, “Base de cálculo” e/ou “Alíquota” no segundo grupo, o mesmo deverá ser mantido em conformidade com os respectivos campos do primeiro grupo.
O detalhamento da contribuição suspensa poderá ser realizado por registro da escrituração (campo 02), pela chave do documento eletrônico (campo 03), pelo participante (campo 04), por produto/serviço (campo 05) ou por data da operação (campo 06), conforme decisão judicial. Caso necessário, o detalhamento também poderá ser realizado mediante combinação destes campos, como por exemplo, por data das operações (campo 06) e por produto/serviço (campo 05).
Por exemplo, no caso de decisão judicial permitir a utilização de alíquota zero para determinado bem tributado com alíquota básica conforme legislação vigente, deve a pessoa jurídica proceder da seguinte forma:
Campo 01: 1011
Campo 02: C170
Campo 03: xxxxxxxxxxxxxxxxxxxxxx
Campo 04: yyyyyyyy
Campo 05: zzzzzzzzz
Campo 06: 01/01/2020
Campo 07: 100,00
Campo 08: 01 (operação tributada)
Campo 09: 100,00
Campo 10: 1,65
Campo 11: 1,65
Campo 12: 01 (operação tributada)
Campo 13: 100,00
Campo 14: 7,6
Campo 15: 7,6
Campo 16: 06 (alíquota zero)
Campo 17: 100,00
Campo 18: 0
Campo 19: 0
Campo 20: 06 (alíquota zero)
Campo 21: 100,00
Campo 22: 0
Campo 23: 0
Campo 24: wwwwwww
Campo 25: yyyyyy
Campo 26: Tributação alíquota zero cfe. decisão judicial
Representação gráfica do registro – Formato txt:
1011|C170|xxxxxxxxxxxxxxxxxxxxxx|yyyyyyyy|zzzzzzzzz|01012020|100,00|01|100,00|1,65|1,65|01|100,00|7,6|7,6|06|100,00|0|0|06|100,00|0|0|wwwwwww|yyyyyy|Tributação alíquota zero cfe. decisão judicial|
Campo 01 (REG) – Valor Válido: [1011]
Campo 02 (REG_REF) – Preenchimento: Se o detalhamento da contribuição suspensa for realizado por registro da escrituração, deverá ser informado neste campo o seu respectivo nome.
Validação: O valor do campo deve ser igual a um nome de registro existente na escrituração, por exemplo, “C170”. Se houver letra no nome do registro ela deverá ser informada em maiúsculo.
Campo 03 (CHAVE_DOC) – Preenchimento: Se o detalhamento da contribuição suspensa for realizado por documento eletrônico, deverá ser informado a chave do mesmo.
Validação: Caso o registro informado no campo 02 (REG_REF) refira-se a C100, C180, C190, C500 ou D100 a chave do documento será validado de acordo com as regras aplicáveis à NFe/NF3e/CTe.
Campo 04 (COD_PART) – Preenchimento e validação: Se o detalhamento da contribuição suspensa for realizado por participante, informar o código do participante cadastrado no registro 0150.
Campo 05 (COD_ITEM) - Preenchimento e validação: Se o detalhamento da contribuição suspensa for realizado por produto/serviço, informar o código do item cadastrado no registro 0200.
Campo 06 (DT_OPER) – Preenchimento: Informar a data a que se referem as operações sendo detalhadas. Caso não seja aplicável, informar o último dia a que se refere a escrituração.
Campo 07 (VL_OPER) – Preenchimento: Informar o valor da operação ou do conjunto de operações sendo detalhadas no registro.
Validação: o valor informado deverá ser maior que zero.
Campo 08 (CST_PIS) – Preenchimento: informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. O CST informado é aquele que foi utilizado na escrituração da operação ou do grupo de operações sendo detalhadas neste registro.
Campo 09 (VL_BC_PIS) – Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à operação ou grupo de operações sendo detalhadas neste registro, conforme informado na escrituração, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso
Campo 10 (ALIQ_PIS) – Preenchimento: informar neste campo o valor da alíquota ad valorem ou expressa em reais aplicada na escrituração da operação ou do grupo de operações sendo detalhadas neste registro, para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 11 (VL_PIS) - Preenchimento: informar o valor do PIS/Pasep (contribuição ou crédito) referente à operação ou grupo de operações sendo detalhadas neste registro, conforme informado na escrituração.
Campo 12 (CST_COFINS) – Preenchimento: informar neste campo o Código de Situação Tributária referente a COFINS (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. O CST informado é aquele que foi utilizado na escrituração da operação ou do grupo de operações sendo detalhadas neste registro.
Campo 13 (VL_BC_COFINS) – Preenchimento: informar neste campo o valor da base de cálculo da COFINS referente à operação ou grupo de operações sendo detalhadas neste registro, conforme informado na escrituração, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso
Campo 14 (ALIQ_COFINS) – Preenchimento: informar neste campo o valor da alíquota ad valorem ou expressa em reais aplicada na escrituração da operação ou do grupo de operações sendo detalhadas neste registro, para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 15 (VL_COFINS) - Preenchimento: informar o valor da COFINS (contribuição ou crédito) referente à operação ou grupo de operações sendo detalhadas neste registro, conforme informado na escrituração.
Campo 16 (CST_PIS_SUSP) – Preenchimento: informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. O CST informado é aquele que foi determinado na decisão judicial para a escrituração da operação ou do grupo de operações sendo detalhadas neste registro.
Campo 17 (VL_BC_PIS_SUSP) – Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à operação ou grupo de operações sendo detalhadas neste registro, conforme determinado na decisão judicial, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
Campo 18 (ALIQ_PIS_SUSP) – Preenchimento: informar neste campo o valor da alíquota ad valorem ou expressa em reais determinada na decisão judicial para escrituração da operação ou do grupo de operações sendo detalhadas neste registro, para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 19 (VL_PIS_SUSP) - Preenchimento: informar o valor do PIS/Pasep (contribuição ou crédito) referente à operação ou grupo de operações sendo detalhadas neste registro, conforme decisão judicial.
Campo 20 (CST_COFINS_SUSP) – Preenchimento: informar neste campo o Código de Situação Tributária referente a COFINS (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. O CST informado é aquele que foi determinado na decisão judicial para a escrituração da operação ou do grupo de operações sendo detalhadas neste registro.
Campo 21 (VL_BC_COFINS_SUSP) – Preenchimento: informar neste campo o valor da base de cálculo da COFINS referente à operação ou grupo de operações sendo detalhadas neste registro, conforme determinado na decisão judicial, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
Campo 22 (ALIQ_COFINS_SUSP) – Preenchimento: informar neste campo o valor da alíquota ad valorem ou expressa em reais determinada na decisão judicial para a escrituração da operação ou do grupo de operações sendo detalhadas neste registro, para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 23 (VL_COFINS_SUSP) - Preenchimento: informar o valor da COFINS (contribuição ou crédito) referente à operação ou grupo de operações sendo detalhadas neste registro, conforme decisão judicial.
Campo 24 (COD_CTA) - Preenchimento: informar o Código da Conta Analítica. Exemplos: estoques, receitas da atividade, receitas não operacionais, custos, despesas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Validação: o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). O código deve existir no Registro 0500: Plano de Contas Contábeis.
Campo 25 (COD_CCUS) - Preenchimento: Nos registros correspondentes às operações com direito a crédito, informar neste campo o Código do Centro de Custo relacionado à operação, se existir.
Campo 26 (DESC_DOC_OPER) - Preenchimento: Neste campo pode ser informada a descrição complementar da operação ou do grupo de operações, objeto de detalhamento neste registro.
<!-- End Registro 1011 -->
<!-- Start Registro 1020 -->
Registro 1020: Processo Referenciado – Processo Administrativo
Uma vez procedida à escrituração de Registros referentes a Processo Referenciado vinculado a um processo administrativo, deve a pessoa jurídica gerar tantos registros “1020” quantos processos administrativos forem utilizadas no período da escrituração, referentes ao detalhamento do(s) mesmo(s) que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | *Texto fixo contendo "1020" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do Processo Administrativo ou da Decisão Administrativa | C | 020 | - | S |
| 03 | IND_NAT_ACAO | Indicador da Natureza da Ação, decorrente de Processo Administrativo na Secretaria da Receita Federal do Brasil: 01 – Processo Administrativo de Consulta 02 – Despacho Decisório 03 – Ato Declaratório Executivo 04 – Ato Declaratório Interpretativo 05 – Decisão Administrativa de DRJ ou do CARF 06 – Auto de Infração 99 – Outros | C | 002* | - | S |
| 04 | DT_DEC_ADM | Data do Despacho/Decisão Administrativa | N | 008* | - | S |

Observações:
Nível hierárquico - 2
Ocorrência - Vários (por arquivo)
Campo 01 - Valor Válido: [1020]
Campo 02 - Preenchimento: informar o número do processo administrativo onde consta o despacho/decisão que autoriza a adoção de procedimento específico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [01, 02, 03, 04, 05, 06, 99]
Campo 04 - Preenchimento: informar a data do despacho/decisão administrativa, no formato "ddmmaaaa", excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
<!-- End Registro 1020 -->
<!-- Start Registro 1050 -->
Registro 1050: Detalhamento de Ajustes de Base de Cálculo – Valores Extra Apuração
Este registro será utilizado pela pessoa jurídica para detalhar os totais de valores extra apuração, objeto de ajustes no Bloco M.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1050" | C | 004 | - | S |
| 02 | DT_REF | Data de referência do ajuste (ddmmaaaa) | N | 008* | - | S |
| 03 | IND_AJ_BC | Indicador da natureza do ajuste da base de cálculo, conforme Tabela Externa 4.3.18 | C | 002* | - | S |
| 04 | CNPJ | CNPJ do estabelecimento a que se refere o ajuste | N | 014* | - | S |
| 05 | VL_AJ_TOT | Valor total do ajuste | N | - | 02 | S |
| 06 | VL_AJ_CST01 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 01 | N | - | 02 | S |
| 07 | VL_AJ_CST02 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 02 | N | - | 02 | S |
| 08 | VL_AJ_CST03 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 03 | N | - | 02 | S |
| 09 | VL_AJ_CST04 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 04 | N | - | 02 | S |
| 10 | VL_AJ_CST05 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 05 | N | - | 02 | S |
| 11 | VL_AJ_CST06 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 06 | N | - | 02 | S |
| 12 | VL_AJ_CST07 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 07 | N | - | 02 | S |
| 13 | VL_AJ_CST08 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 08 | N | - | 02 | S |
| 14 | VL_AJ_CST09 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 09 | N | - | 02 | S |
| 15 | VL_AJ_CST49 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 49 | N | - | 02 | S |
| 16 | VL_AJ_CST99 | Parcela do ajuste a apropriar na base de cálculo referente ao CST 99 | N | - | 02 | S |
| 17 | IND_APROP | Indicador de apropriação do ajuste: 01 – Referente ao PIS/Pasep e a Cofins 02 – Referente unicamente ao PIS/Pasep 03 – Referente unicamente à Cofins | C | 002* | - | S |
| 18 | NUM_REC | Número do recibo da escrituração a que se refere o ajuste | C | 80 | - | N |
| 19 | INFO_COMPL | Informação complementar do registro | C | - | - | N |

Observações:
1. Este registro deve ser escriturado para a pessoa jurídica informar valores de ajustes de acréscimo ou de redução da base de cálculo mensal da contribuição, entre as diversas bases de cálculo da contribuição, especificadas pela legislação tributária de referência.
2. Para tanto, e considerando que as receitas auferidas no período da escrituração podem ser tributadas a alíquotas distintas (alíquota básica, alíquota monofásica, alíquota zero, alíquota específica)  ou não serem tributadas (operações com suspensão, isenção ou não incidência), faz-se necessário que a pessoa jurídica demonstre de forma segregada a parecela do ajuste de acréscimo ou de redução da base de cálculo, conforme o código de situação tributária (CST) aplicável às receitas mensais escrituradas.
3. Os valores de ajustes de base de cálculo segregados neste registro de controle, devem guardar correspondência com os valores escriturados nos registros M215 (PIS/Pasep) e M615 (Cofins) que demonstram a visão analítica dos ajustes, por CNPJ.
4. Este registro só é habilitado na versão 3.1.0 do leiaute do programa da EFD-Contribuições, a ser utilizado na escrituração dos fatos geradores ocorridos a partir de 01 de janeiro de 2019.
5. Desta forma, mesmo que a pessoa jurídica esteja utilizando a versão 3.1.0 e posteriores do programa da EFD-Contribuições para a escrituração de fatos geradores ocorridos até 31.12.2018, a versão em referência não disponibiliza este registro de controle.
6. Todavia, excepcionalmente na escrituração referente ao período de apuração de janeiro de 2019, poderá a pessoa jurídica demonstrar os valores de ajustes de redução (ou de acréscimo) da base de cálculo mensal da contribuição, entre as diversas bases de cálculo da contribuição, referentes aos períodos de apuração ocorridos até 31.12.2018, de forma a demonstrar à RFB, mês a mês, dos valores de ajustes a que tem direito, decorrente de processo judicial que autoriza e reconhece o direito de proceder a ajuste na base de cálculo mensal das contribuições, ou decorrente de disposição legal ou de ato administrativo específico.
Nível hierárquico - 2
Ocorrência – 1:N
Campo 01 - Valor Válido: [1050]
Campo 02 - Preenchimento: informar, se for o caso, a data de referência do ajuste, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
No caso de o ajuste informado no registro não ser específico de uma data do período, deve ser informado a data correspondente ao ultimo dia do mês a que se refere a escrituração, como por exemplo, “31012019”.
Campo 03 - Preenchimento: informar o código do ajuste da base de cálculo, conforme Tabela 4.3.18 - “Tabela Código de Ajustes da Base de Cálculo Mensal”, referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 04 - Preenchimento: informar o CNPJ do estabelecimento da pessoa jurídica a que se refere o ajuste escriturado neste registro.
Caso o ajuste não se refira a um estabelecimento especifico, deve ser informado o CNPJ correspondente ao estabelecimento matriz da pessoa jurídica, escriturado no Registro “0000”.
Campo 05 - Preenchimento: informar o valor total do ajuste de redução ou de acréscimo da base de cálculo mensal da contribuição que está sendo objeto de segregação, de escrituração analítica, neste registro de controle.
Campo 06 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas tributadas à alíquota básica, escrituradas com o CST 01.
Campo 07 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas tributadas à alíquota diferenciada, escrituradas com o CST 02.
Campo 08 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas tributadas à alíquota por unidade de medida de produto, escrituradas com o CST 03.
Campo 09 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas tributadas à alíquota zero, da revenda de produto sujeito à tributação monofásica, escrituradas com o CST 04.
Campo 10 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas tributadas no regime de substituição tributária, escrituradas com o CST 05.
Campo 11 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das demais receitas tributadas à alíquota zero, escrituradas com o CST 06.
Campo 12 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas isentas da contribuição, escrituradas com o CST 07.
Campo 13 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas sem incidência da contribuição, escrituradas com o CST 08.
Campo 14 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, referente à base de cálculo das receitas com suspensão da contribuição, escrituradas com o CST 09.
Campo 15 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, relacionadas a outras operações de saídas, caso escrituradas, com o CST 49.
Campo 16 - Preenchimento: informar a parcela do ajuste total informada no Campo 05, relacionadas a outras operações, caso escrituradas, com o CST 99.
Campo 17 - Preenchimento: informar a qual contribuição se refere o ajuste, conforme os indicadores informados no leiaute deste registro.
Campo 18 - Preenchimento: informar neste campo o número do recibo da escrituração a que se refere o ajuste. Caso o numero do recibo a ser informado neste camporefira-se a outra escrituração, como no caso da EFD-ICMS/IPI, ele deve conter 41 posições e ser informado somente com letras maiúsculas.
Campo 19 - Preenchimento: Campo para prestação de outras informações que se mostrem necessárias ou adequadas, para esclarecer ou justificar o ajuste da base de cálculo a que se refere este registro.
<!-- End Registro 1050 -->
<!-- Start Registro 1100 -->
Registro 1100: Controle de Créditos Fiscais – PIS/Pasep
Este registro tem por objetivo realizar o controle de saldos de créditos fiscais de períodos anteriores ao da atual escrituração, bem como eventual saldo credor apurado no próprio período da escrituração. Ou seja, este registro serve para escriturar as disponibilidades de créditos:
Apurados em períodos anteriores ao da escrituração, demonstrados mês a mês, com saldos a utilizar no atual período da escrituração ou em períodos posteriores, mediante desconto, compensação ou ressarcimento;
Apurados no próprio período da escrituração, mas que não foi totalmente utilizado neste período, restando saldos a utilizar em períodos posteriores, mediante desconto, compensação ou ressarcimento.
Atenção: Não precisam ser escriturados neste registro os créditos apurados no próprio período e que foram totalmente utilizados na atual escrituração, não restando assim saldos a utilizar em período posterior.
O saldo de créditos deverá ser segregado por período de apuração, devendo, ainda, levar em consideração a sua origem e, no caso de créditos transferidos por sucessão, o CNPJ da pessoa jurídica cedente do crédito. A chave deste registro é formada pelo campo PER_APU_CRED, campo ORIG_CRED, campo CNPJ_SUC e campo COD_CRED.
Conceitualmente, o crédito só se caracteriza como extemporâneo, quando se refere a período anterior ao da escrituração, e o mesmo não pode mais ser escriturado no correspondente período de apuração de sua constituição, via transmissão de Dacon retificador ou EFD-Contribuições retificadora.
Salienta-se que para correta forma de identificação dos saldos dos créditos de período(s) passados(s), a favor do contribuinte, seja observado o critério da clareza, expressando mês a mês a posição (tipo de crédito, constituição, utilização parcial ou total) do referido crédito de forma individualizada, ou seja, não agregando ou totalizando com quaisquer outros, ainda que de mesma natureza ou período. Deve-se respeitar e preservar o direito ao crédito pelo período decadencial, logo, não é procedimento regular de escrituração englobar ou relacionar em um mesmo registro, saldos de créditos referentes à meses distintos. Deve assim ser escriturado um registro para cada mês de períodos passados, que tenham saldos passíveis de utilização, no período a que se refere à escrituração atual.
Desta forma, eventual crédito extemporâneo informado no campo 07 tem, necessariamente, que se referir a período de apuração (campo 02) anterior ao da atual escrituração.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1100" | C | 004* | - | S |
| 02 | PER_APU_CRED | Período de Apuração do Crédito (MM/AAAA) | N | 006 | - | S |
| 03 | ORIG_CRED | Indicador da origem do crédito: 01 – Crédito decorrente de operações próprias; 02 – Crédito transferido por pessoa jurídica sucedida. | N | 002* | - | S |
| 04 | CNPJ_SUC | CNPJ da pessoa jurídica cedente do crédito (se ORIG_CRED = 02). | N | 014* | - | N |
| 05 | COD_CRED | Código do Tipo do Crédito, conforme Tabela 4.3.6. | N | 003* | - | S |
| 06 | VL_CRED_APU | Valor total do crédito apurado na Escrituração Fiscal Digital (Registro M100) ou em demonstrativo DACON (Fichas 06A e 06B) de período anterior. | N | - | 02 | S |
| 07 | VL_CRED_EXT_APU | Valor de Crédito Extemporâneo Apurado (Registro 1101), referente a Período Anterior, Informado no Campo 02 – PER_APU_CRED | N | - | 02 | N |
| 08 | VL_TOT_CRED_APU | Valor Total do Crédito Apurado (06 + 07) | N | - | 02 | S |
| 09 | VL_CRED_DESC_PA_ANT | Valor do Crédito utilizado mediante Desconto, em Período(s)  Anterior(es). | N | - | 02 | S |
| 10 | VL_CRED_PER_PA_ANT | Valor do Crédito utilizado mediante Pedido de Ressarcimento, em Período(s) Anterior(es). | N | - | 02 | N |
| 11 | VL_CRED_DCOMP_PA_ANT | Valor do Crédito utilizado mediante Declaração de Compensação Intermediária (Crédito de Exportação), em Período(s) Anterior(es). | N | - | 02 | N |
| 12 | SD_CRED_DISP_EFD | Saldo do Crédito Disponível para Utilização neste Período de Escrituração (08 – 09 – 10 - 11). | N | - | 02 | S |
| 13 | VL_CRED_DESC_EFD | Valor do Crédito descontado neste período de escrituração. | N | - | 02 | N |
| 14 | VL_CRED_PER_EFD | Valor do Crédito objeto de Pedido de Ressarcimento (PER) neste período de escrituração. | N | - | 02 | N |
| 15 | VL_CRED_DCOMP_EFD | Valor do Crédito utilizado mediante Declaração de Compensação Intermediária neste período de escrituração. | N | - | 02 | N |
| 16 | VL_CRED_TRANS | Valor do crédito transferido em evento de cisão, fusão ou incorporação. | N | - | 02 | N |
| 17 | VL_CRED_OUT | Valor do crédito utilizado por outras formas. | N | - | 02 | N |
| 18 | SLD_CRED_FIM | Saldo de créditos a utilizar em período de apuração futuro (12 – 13 – 14 – 15 – 16 - 17). | N | - | 02 | N |

Observações: Será preenchido um registro para cada período de apuração no qual exista saldo de créditos, utilizados neste período da escrituração ou a serem utilizados em períodos futuros.
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [1100]
Campo 02 - Preenchimento: informar o período em que o saldo credor foi apurado no formato “mmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o período informado deverá ser o mesmo ou anterior ao da atual escrituração
Campo 03 - Valores válidos: [01, 02]
Campo 04 - Preenchimento: caso o crédito sendo informado no registro refira-se a crédito transferido por pessoa jurídica sucedida (Campo ORIG_CRED preenchido com valor 02), informe neste campo o respectivo CNPJ. Caso contrário deve o campo ficar em branco.
Campo 05 - Preenchimento: informe o código do tipo do crédito cujo saldo credor está sendo informado no registro, conforme a Tabela “4.3.6 – Tabela Código de Tipo de Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 06 - Preenchimento: Informe neste campo o valor do crédito apurado no respectivo período de apuração. Para períodos em que não houve transmissão da escrituração (períodos anteriores ao início da obrigatoriedade de escrituração), este valor deve corresponder ao lançado no respectivo demonstrativo DACON.
Para períodos em que houve transmissão de escrituração o valor deste campo deverá corresponder ao valor do Campo 12 - VL_CRED_DISP, relativo ao mesmo COD_CRED do registro M100 do período de apuração do crédito, no caso de crédito apurado pela própria pessoa jurídica.
No caso de crédito oriundo de pessoa jurídica sucedida, o valor deste campo deverá corresponder ao valor da soma dos Campos 07 - VL_CRED_PIS, relativos ao mesmo COD_CRED e CNPJ_SUCED do registro F800 do mesmo período de transferência do crédito.
Campo 07 - Preenchimento: Crédito extemporâneo é aquele cujo período de apuração ou competência do crédito se refere a período anterior ao da escrituração atual, mas que somente agora está sendo registrado. Estes documentos deverão ser informados no registro 1101.
Validação: O valor deste campo deverá ser igual à soma do campo 17 (VL_PIS) dos Registros 1101 quando o respectivo campo 14 (CST_PIS) for  igual 50, 51, 52, 60, 61 e 62, adicionado à soma do campo 02 (VL_CRED_PIS_TRIB_MI), campo 03 (VL_CRED_PIS_NT_MI) e do campo 04 (VL_CRED_PIS_ EXP) dos Registros 1102 quando o respectivo campo 14 (CST_PIS) do registro 1101 for igual a 53, 54, 55, 56, 63, 64, 65 ou 66.
Campo 08 - Validação: Valor total do crédito apurado, correspondendo à soma dos campos 06 (VL_CRED_APU) e 07 (VL_CRED_EXT_APU)
Campo 09 - Preenchimento: Informar o valor do crédito utilizado mediante desconto no próprio período de apuração do crédito e em períodos subsequentes, anteriores ao da escrituração atual. No caso de períodos abrangidos pela entrega da escrituração o valor do crédito apurado pela própria pessoa jurídica, utilizado mediante desconto é obtido no campo 14 (VL_CRED_DESC) do registro M100.
Campo 10 - Preenchimento: Informar o valor do crédito utilizando mediante Pedido de Ressarcimento em períodos subsequentes ao de apuração do crédito, anteriores ao da escrituração atual.
Validação: O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 201, 202, 203, 204, 208, 301, 302, 303, 304, 307 ou 308.
Campo 11 - Preenchimento: Informar o valor do crédito utilizando mediante Declaração de Compensação Intermediária (compensação específica para créditos de exportação, objeto de Dcomp transmitida no próprio trimestre de apuração do crédito) em períodos subsequentes ao de apuração do crédito, anteriores ao da escrituração atual.
Validação: O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 301, 302, 303, 304 ou 308.
Campo 12 - Preenchimento: Preencher com o saldo do crédito disponível para utilização no período da atual escrituração, correspondendo a subtração do valor do campo 08 (VL_TOT_CRED_APU) pelos valores dos campos 09 (VL_CRED_DESC_PA_ANT), 10 (VL_CRED_PER_PA_ANT) e 11 (VL_CRED_DCOMP_PA_ANT).
Campo 13 - Preenchimento: Informar o valor do crédito disponível, conforme apurado no campo 12 (SD_CRED_DISP_EFD), utilizado mediante desconto neste período de escrituração. A soma dos valores lançados neste campo deverá corresponder àquele registrado no campo 04 (VL_TOT_CRED_DESC_ANT) do registro M200.
Campo 14 - Preenchimento: Informar o valor do crédito utilizando mediante Pedido de Ressarcimento no período da atual escrituração. O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 201, 202, 203, 204, 208, 301, 302, 303, 304, 307 ou 308.
Campo 15 - Preenchimento: Informar o valor do crédito utilizando mediante Declaração de Compensação Intermediária (compensação específica para créditos de exportação, objeto de Dcomp transmitida no próprio trimestre de apuração do crédito) no período da escrituração atual. O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 301, 302, 303, 304 ou 308.
Campo 16 - Preenchimento: Informar o valor do crédito transferido em evento de cisão, fusão ou incorporação. O valor deste campo deverá ser recuperado na escrituração da pessoa jurídica sucessora, no campo 07 (VL_CRED_PIS).
Campo 17 - Preenchimento: Informar o valor do crédito utilizado por outras formas, conforme previsão legal.
Campo 18 - Preenchimento: Informar o valor do saldo de crédito, se existente, para aproveitamento em períodos futuros, correspondendo à subtração do valor do campo 12 (SD_CRED_DISP_EFD) pelos valores dos campos 13 (VL_CRED_DESC_EFD), 14 (VL_CRED_PER_EFD), 15 (VL_CRED_DCOMP_EFD), 16 (VL_CRED_TRANS) e 17 (VL_CRED_OUT).
<!-- End Registro 1100 -->
<!-- Start Registro 1101 -->
Registro 1101: Apuração de Crédito Extemporâneo - Documentos e Operações de Períodos Anteriores – PIS/Pasep
Crédito extemporâneo é aquele cujo período de apuração ou competência do crédito se refere a período anterior ao da escrituração atual, mas que somente agora está sendo registrado. O crédito extemporâneo deverá ser informado, preferencialmente, mediante a retificação da escrituração cujo período se refere o crédito. No entanto, se a retificação não for possível, devido ao prazo previsto na Instrução Normativa RFB nº 1.052, de 2010, a PJ deverá detalhar suas operações através deste registro.
Este registro deverá ser utilizado para detalhar as informações prestadas no campo 07 do registro pai 1100.
Deve ser ressaltado que o crédito apurado no período da escrituração pelo método de apropriação direta (Art. 3º, § 8º, da Lei nº 10.637/02), referente a aquisições, custos e despesas incorridos em período anteriores ao da escrituração, não se trata de crédito extemporâneo, se a sua efetividade só vem a ser constituída no período atual da escrituração.

| ESCLARECIMENTOS IMPORTANTES QUANTO A NÃO VALIDAÇÃO DE REGISTROS DE CRÉDITOS EXTEMPORANEOS, A PARTIR DE AGOSTO DE 2013. |
| --- |
| 1. Os registros para informação extemporânea de créditos (registros 1101, 1102, 1501, 1502) e de contribuições (1200, 1210,1220 e 1600,1610,1620), passíveis de escrituração para os fatos geradores ocorridos até 31/07/2013, tanto na versão 2.04a como na nova versão 2.05, tinha a sua justificativa de escrituração apenas para os casos em que o período de apuração a que dissesse respeito a operação/documento fiscal, geradora de contribuição ou crédito, ainda não informada em escrituração já transmitida, não pudesse ser mais objeto de retificação, por ter expirado o prazo de retificação até então vigente na redação original da IN RFB 1.252/2012 (retificação até o término do ano calendário seguinte ao que se refere a escrituração original), conforme consta orientação no próprio Guia Prático da Escrituração, de que estes registros só deveriam ser utilizados, na impossibilidade de retificar as escriturações referentes às operações ainda não escrituradas. 2. Com o novo disciplinamento referente à retificação da EFD-Contribuições determinado pela IN RFB nº 1.387/2013, permitindo a escrituração e transmissão de arquivo retificador no prazo decadencial das contribuições, ou seja, em até cinco anos, a contar do período de apuração da EFD-Contribuições a ser retificada, deixa de ter qualquer fundamento de aplicabilidade e de validade os referidos registros, uma vez que todas as normas editadas pela Receita Federal quanto às obrigações acessórias, inclusive as do Sped, estabelece o instituto da retificação, para o contribuinte acrescentar, informar, registrar, sanear, qualquer fato que deveria ser incluído na declaração/escrituração original, conforme prazo e condições de retificação definidos para cada obrigação acessória. 3. No tocante à EFD-Contribuições, o prazo em vigor para retificação é agora de cinco anos, de forma que eventual documento ou operação que não tenha sido devidamente escriturado em qualquer escrituração dos anos de 2011, 2012 ou 2013, podem agora ser regularizados, mediante a retificação da escrituração original correspondente, nos Blocos A, C, de F.  4. Registre-se que, diferentemente da EFD-ICMS/IPI, a EFD-Contribuições não limita ou recusa na escrituração de documentos e operações nos Blocos A, C, D ou F, a escrituração de documentos cuja data de emissão seja diferente (meses anteriores ou posteriores) ao que se refere a escrituração.  Assim, na EFD-Contribuições do Período de Apuração referente a agosto de 2013, por exemplo, pode ser incluído documentos que, mesmo emitidos em meses anteriores a agosto/2013, ou emitidos em meses posteriores a agosto/2013, desde que o fato (receita ou operação geradora de crédito) tenha por período de competência, o mês da escrituração, ou seja, agosto de 2013. Em resumo, a EFD-Contribuições nunca validou como extemporâneo um documento, ou deixou de considerar como válido o documento/operação, em função de vir a ter data de emissão diferente ao do período de apuração a que se refere. O PVA nas versões disponibilizadas em ambiente de produção continua validando eventual registro extemporâneo, se o arquivo txt importado se referir a PA igual ou anterior a julho de 2013. Para as escriturações com período de apuração a partir de agosto de 2013, o PVA não valida nem permite a geração de registros de operação extemporânea, gerando ocorrência de erro de escrituração. |


| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1101" | C | 004* | - | S |
| 02 | COD_PART | Código do participante (Campo 02 do Registro 0150) | C | 060 | - | N |
| 03 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 04 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1. | C | 002* | - | N |
| 05 | SER | Série do documento fiscal | C | 004 | - | N |
| 06 | SUB_SER | Subsérie do documento fiscal | C | 003 | - | N |
| 07 | NUM_DOC | Número do documento fiscal | N | 009 | - | N |
| 08 | DT_OPER | Data da Operação (ddmmaaaa) | N | 008* | - | S |
| 09 | CHV_NFE | Chave da Nota Fiscal Eletrônica | N | 044* | - | N |
| 10 | VL_OPER | Valor da Operação | N | - | 02 | S |
| 11 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 12 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | S |
| 13 | IND_ORIG_CRED | Indicador da origem do crédito: 0 – Operação no Mercado Interno 1 – Operação de Importação | C | 001* | - | S |
| 14 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 15 | VL_BC_PIS | Base de Cálculo do Crédito de PIS/PASEP (em valor ou em quantidade). | N | - | 03 | S |
| 16 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual ou em reais). | N | - | 04 | S |
| 17 | VL_PIS | Valor do Crédito de PIS/PASEP. | N | - | 02 | S |
| 18 | COD_CTA | Código da conta analítica contábil debitada/creditada. | C | 255 | - | N |
| 19 | COD_CCUS | Código do Centro de Custos. | C | 255 | - | N |
| 20 | DESC_COMPL | Descrição complementar do Documento/Operação. | C | - | - | N |
| 21 | PER_ESCRIT | Mês/Ano da Escrituração em que foi registrado o documento/operação (Crédito pelo método da Apropriação Direta). | N | 006* | - | N |
| 22 | CNPJ | CNPJ do estabelecimento gerador do crédito extemporâneo (Campo 04  do Registro 0140) | N | 014* | - | S |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [1101];
Campo 02 - Validação: o código informado neste campo deve está relacionado no registro 0150, no campo COD_PART.
Campo 03 - Preenchimento: o código do item a que se refere a operação informado neste campo, quando existir, deve está relacionado no registro 0200, ressaltando-se que os códigos informados devem ser os definidos pelo pessoa jurídica titular da escrituração.
Campo 04 - Preenchimento: o valor informado deve constar na tabela 4.1.1 do Manual do Leiaute da EFD-Contribuições. O “código” a ser informado não é exatamente o “modelo” do documento, devendo ser consultada a tabela 4.1.1. Exemplo: o código “01” deve ser utilizado para os modelos “1” ou “1A".
Campo 05 - Preenchimento: informar a série do documento fiscal, se existir.
Campo 06 - Preenchimento: informar a subsérie do documento fiscal, se existir.
Campo 07 – Validação: Informar o número da nota fiscal ou documento internacional equivalente, se for o caso.
Campo 08 - Preenchimento: informar a data da operação escriturada neste registro, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
No caso da operação não se referir a um dia específico, ou se referir a mais de um dia, deve ser informado o dia final de referência ou o ultimo dia da escrituração, conforme o caso.
Campo 09 - Preenchimento: Neste campo deve ser informado a chave ou código de verificação, no caso de nota fiscal eletrônica.
Campo 10 – Preenchimento: Informar o valor total da operação/item escriturado neste registro.
Campo 11 - Preenchimento: Devem ser registrados os códigos de operação que correspondem ao tratamento tributário relativo à destinação do item, se for o caso de documento fiscal sujeito ao ICMS.
Campo 12 - Preenchimento: Informar neste campo o código da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 13 - Valores válidos: [0, 1]
Preenchimento: Informar o código que indique se a operação tem por origem o mercado interno ou externo (importação de bens e serviços).
Campo 14 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 15 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep referente à operação/item, para fins de apuração do crédito. Caso o crédito seja apurado por unidade de medida de produto, informe a quantidade da base de cálculo com três casas decimais. Caso contrário, utilize duas casas decimais.
Campo 16 - Preenchimento: informar neste campo a alíquota aplicável para fins de apuração do crédito. Caso o crédito seja apurado por unidade de medida de produto, utilize a alíquota em reais, caso contrário utilize a alíquota em percentual.
Campo 17 – Preenchimento: informar o valor do crédito do PIS/Pasep referente à operação/item escriturado neste registro, correspondendo a VL_BC_PIS x ALIQ_PIS, no caso de apuração por unidade de medida de produto ou VL_BC_PIS x ALIQ_PIS/100, caso contrário.
Validação: a soma dos valores deste campo deverá ser transportada para o campo 07 - VL_CRED_EXT_APU do registro pai 1100.
Campo 18 - Preenchimento: informar o Código da Conta Analítica. Exemplos: estoques, custos, despesas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo 19 - Preenchimento: Informar neste campo o Código do Centro de Custo relacionado à operação, se existir.
Campo 20 - Preenchimento: Neste campo pode ser informada a descrição complementar da operação ou do item, objeto de escrituração neste registro.
Campo 21 - Preenchimento:  No caso de apropriação direta de créditos comuns, informar o Mês/Ano da Escrituração em que foi registrado o documento/operação. Caso contrário deixar o campo em branco.
Validação: Devem ser informados conforme o padrão "mêsano" (mmaaaa), excluindo-se quaisquer caracteres de separação (tais como: ".", "/", "-", etc), sendo que o período deverá ser anterior ao da atual escrituração.
Campo 22 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações escrituradas neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deverá estar cadastrado no Registro 0140.
<!-- End Registro 1101 -->
<!-- Start Registro 1102 -->
Registro 1102: Detalhamento do Crédito Extemporaneo Vinculado a Mais de Um Tipo de Receita – PIS/Pasep
Este registro deverá ser preenchido quando CST_PIS do registro 1101 for referente a operações com direito a crédito (códigos 53, 54, 55, 56, 63, 64, 65 ou 66), independentemente do método de apropriação dos créditos comuns (apropriação direta ou rateio proporcional).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1102" | C | 004* | - | S |
| 02 | VL_CRED_PIS_TRIB_MI | Parcela do Crédito de PIS/PASEP, vinculada a Receita Tributada no Mercado Interno | N | - | 02 | N |
| 03 | VL_CRED_PIS_NT_MI | Parcela do Crédito de PIS/PASEP, vinculada a Receita Não Tributada no Mercado Interno | N | - | 02 | N |
| 04 | VL_CRED_PIS_ EXP | Parcela do Crédito de PIS/PASEP, vinculada a Receita de Exportação | N | - | 02 | N |

Observações: Será preenchido quando CST_PIS do registro 1101 for referente a operações com direito a crédito (códigos 53, 54, 55, 56, 63, 64, 65 ou 66).
Nível hierárquico - 4
Ocorrência - 1:1
Campo 01 - Valor Válido: [1102]
Campo 02 - Preenchimento: informar o valor da parcela do crédito de PIS/Pasep, informado no campo 17 - VL_PIS, vinculada à receita tributada no mercado interno.
Validação: este campo só deverá ser preenchido se o campo 05 - COD_CRED do registro 1100 iniciar com “1” (crédito vinculado à receita tributada no mercado interno).
Campo 03 - Preenchimento: informar o valor da parcela do crédito de PIS/Pasep, informado no campo 17 - VL_PIS, vinculada à receita não tributada no mercado interno.
Validação: este campo só deverá ser preenchido se o campo 05 - COD_CRED do registro 1100 iniciar com “2” (crédito vinculado à receita não tributada no mercado interno).
Campo 04 - Preenchimento: informar o valor da parcela do crédito de PIS/Pasep, informado no campo 17 - VL_PIS, vinculada à receita de exportação.
Validação: este campo só deverá ser preenchido se o campo 05 - COD_CRED do registro 1100 iniciar com "3" (crédito vinculado à receita de exportação).
<!-- End Registro 1102 -->
<!-- Start Registro 1200 -->
Registro 1200: Contribuição Social Extemporânea – PIS/Pasep
Contribuição social extemporânea é aquela cujo documento/operação correspondente deveria ter sido escriturado e considerado na apuração da contribuição de período anterior, mas que somente agora está sendo registrado. A contribuição social extemporânea, por não ter sido escriturada no período correto, acarreta o respectivo recolhimento com pagamento de multa e juros de mora, caso não haja crédito/deduções válidas a serem descontadas.
Deverá ser gerado um registro para cada período de escrituração, natureza de contribuição a recolher, bem como data de recolhimento, se existir. Desta forma, a chave deste registro é formada pelos campos: PER_APUR_ANT + NAT_CONT_REC + DT_RECOL.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1200" | C | 004* | - | S |
| 02 | PER_APUR_ANT | Período de Apuração da Contribuição Social Extemporânea (MMAAAA). | N | 006* | - | S |
| 03 | NAT_CONT_REC | Natureza da Contribuição a Recolher, conforme Tabela 4.3.5. | C | 002 | - | S |
| 04 | VL_CONT_APUR | Valor da Contribuição Apurada. | N | - | 02 | S |
| 05 | VL_CRED_PIS_DESC | Valor do Crédito de PIS/PASEP a Descontar, da Contribuição Social Extemporânea. | N | - | 02 | S |
| 06 | VL_CONT_DEV | Valor da Contribuição Social Extemporânea Devida. | N | - | 02 | S |
| 07 | VL_OUT_DED | Valor de Outras Deduções. | N | - | 02 | S |
| 08 | VL_CONT_EXT | Valor da Contribuição Social Extemporânea a pagar. | N | - | 02 | S |
| 09 | VL_MUL | Valor da Multa. | N | - | 02 | N |
| 10 | VL_JUR | Valor dos Juros. | N | - | 02 | N |
| 11 | DT_RECOL | Data do Recolhimento. | N | 008* | - | N |

Observações:
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [1200];
Campo 02 - Preenchimento: Preenchimento: informar o período em que a contribuição a recolher deveria ter sido apurada, no formato “mmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o período informado deverá ser anterior ao da atual escrituração.
Campo 03 - Preenchimento: informe o código da contribuição social que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 04 - Preenchimento: Informe o valor total da contribuição extemporânea apurada, referente ao código informado no campo 03 e data de recolhimento informada no campo 11, conforme detalhamento do registro filho 1210.
Campo 05 - Preenchimento: Informe o valor do crédito de PIS/Pasep a descontar, da contribuição social extemporânea, conforme detalhamento do registro filho 1220.
Campo 06 - Preenchimento: Informe o valor da contribuição social extemporânea devida, correspondendo à subtração do valor do campo 04 pelo valor do campo 05.
Campo 07 - Preenchimento: Informe o valor das demais deduções à contribuição social extemporânea devida.
Campo 08 - Preenchimento: Informe o valor da contribuição social extemporânea a pagar, correspondendo à subtração do valor do campo 06 pelo valor do campo 07.
Campo 09 - Preenchimento: Informe o valor da multa vinculado ao recolhimento da contribuição social extemporânea a pagar, no caso do valor informado no campo 08 ser maior do que zero.
Campo 10 - Preenchimento: Informe o valor dos juros vinculados ao recolhimento da contribuição social extemporânea a pagar, no caso do valor informado no campo 08 ser maior do que zero.
Campo 11 - Preenchimento: Informe a data do recolhimento da contribuição social extemporânea a pagar, no caso do valor informado no campo 08 ser maior do que zero.
Validação: Informar a data no padrão "diamêsano" (ddmmaaaa), excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
<!-- End Registro 1200 -->
<!-- Start Registro 1210 -->
Registro 1210: Detalhamento aa Contribuição Social Extemporânea – PIS/Pasep
Este registro deverá ser preenchido pela pessoa jurídica que apurou valores de contribuição social extemporânea no registro pai 1200, em relação a cada estabelecimento e participante, segregando as informações por data da operação, CST do PIS/Pasep, participante e conta contábil. Dessa forma, a chave deste registro é formada pelos campos: CNPJ + CST_PIS + COD_PART + DT_OPER + ALIQ_PIS + COD_CTA.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “1210” | C | 004* | - | S |
| 02 | CNPJ | Número de inscrição do estabelecimento no CNPJ (Campo 04 do Registro 0140). | N | 014* | - | S |
| 03 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 04 | COD_PART | Código do participante (Campo 02 do Registro 0150) | C | 060 | - | N |
| 05 | DT_OPER | Data da Operação (ddmmaaaa) | N | 008* | - | S |
| 06 | VL_OPER | Valor da Operação | N | - | 02 | S |
| 07 | VL_BC_PIS | Base de cálculo do PIS/PASEP (em valor ou em quantidade) | N | - | 03 | S |
| 08 | ALIQ_PIS | Alíquota da PIS (em percentual ou em reais) | N | - | 04 | S |
| 09 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | S |
| 10 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 11 | DESC_COMPL | Descrição complementar do Documento/Operação | C | - | - | N |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [1210];
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações escrituradas neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deverá estar cadastrado no Registro 0140.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 04 - Validação: o código informado neste campo, se for o caso, deve estar relacionado no registro 0150, no campo COD_PART.
Campo 05 - Preenchimento: informar a data da operação escriturada neste registro, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
No caso da operação não se referir a um dia específico, ou se referir a mais de um dia, deve ser informado o dia final de referência ou o ultimo dia da escrituração, conforme o caso.
Campo 06 – Preenchimento: Informar o valor total da operação/item escriturado neste registro.
Campo 07 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep referente à operação/item, para fins de apuração da contribuição social extemporânea. Caso a operação/item esteja sujeita à apuração por unidade de medida de produto, utilize três casas decimais, caso contrário, duas casas decimais.
Campo 08 - Preenchimento: informar neste campo a alíquota aplicável para fins de apuração da contribuição social extemporânea. Caso a operação/item esteja sujeita à apuração por unidade de medida de produto, utilize a respectiva alíquota em reais, caso contrário, utilize alíquota em percentual.
Campo 09 – Preenchimento: informar o valor da contribuição social extemporânea referente à operação/item escriturado neste registro, correspondendo a VL_BC_PIS x ALIQ_PIS, no caso de apuração por unidade de medida de produto ou VL_BC_PIS x ALIQ_PIS/100, caso contrário.
Validação: a soma dos valores deste campo deverá ser transportada para o campo 04 - VL_CONT_APUR do registro pai 1200.
Campo 10 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita da prestação de serviços, receitas da atividade, etc. deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo 11 - Preenchimento: Neste campo pode ser informada a descrição complementar da operação ou do item, objeto de escrituração neste registro.
<!-- End Registro 1210 -->
<!-- Start Registro 1220 -->
Registro 1220: Demonstração do Crédito a Descontar a Contribuição Extemporânea – PIS/Pasep
Este registro deverá ser preenchido pela pessoa jurídica que descontou créditos referentes aos valores de contribuição social extemporânea apurada no registro pai 1200. A informação deverá ser segregada em relação a cada código de crédito, período de apuração do respectivo crédito e sua origem. Dessa forma, a chave deste registro é formada pelos campos: PER_APUR_CRED + ORIG_CRED + COD_CRED.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1220" | C | 004* | - | S |
| 02 | PER_APU_CRED | Período de Apuração do Crédito (MM/AAAA) | N | 006 | - | S |
| 03 | ORIG_CRED | Indicador da origem do crédito: 01 – Crédito decorrente de operações próprias; 02 – Crédito transferido por pessoa jurídica sucedida. | N | 002* | - | S |
| 04 | COD_CRED | Código do Tipo do Crédito, conforme Tabela 4.3.6. | N | 003* | - | S |
| 05 | VL_CRED | Valor do Crédito a Descontar | N | - | 002 | S |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [1220]
Campo 02 - Preenchimento: Informe o período de apuração do crédito descontado da contribuição social extemporânea.
Validação: Devem ser informados conforme o padrão "mêsano" (mmaaaa), excluindo-se quaisquer caracteres de separação (tais como: ".", "/", "-", etc), sendo que o período informado no campo deve ser anterior ou igual ao período de apuração (PER_APUR_ANT) do registro pai 1200.
Campo 03 - Valores válidos: [01, 02]
Campo 04 - Preenchimento: informe o código do tipo do crédito cujo valor foi aproveitado para desconto da contribuição social extemporânea, conforme a Tabela “4.3.6 – Tabela Código de Tipo de Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informe o valor do crédito que foi aproveitado para desconto da contribuição social extemporânea. A soma dos valores deste campo deverá ser transportada para o campo 05 - VL_CRED_PIS_DESC do registro pai 1200.
<!-- End Registro 1220 -->
<!-- Start Registro 1300 -->
Registro 1300: Controle dos Valores Retidos na Fonte – PIS/Pasep
Este registro tem por objetivo realizar o controle dos saldos de valores retidos na fonte, de períodos anteriores e do período da atual escrituração. Estes valores, observada a legislação que regulamenta o assunto, poderão ser utilizados para dedução da contribuição cumulativa e/ou não cumulativa devida, conforme apuração constante dos registros M200.
As informações deverão estar consolidadas pela natureza da retenção na fonte e seu respectivo período de recebimento e retenção. Assim, a chave deste registro é formada pelos campos: IND_NAT_RET + PR_REC_RET.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1300" | C | 004* | - | S |
| 02 | IND_NAT_RET | Indicador de Natureza da Retenção na Fonte até 2013: 01 - Retenção por Órgãos, Autarquias e Fundações Federais 02 - Retenção por outras Entidades da Administração Pública Federal 03 - Retenção por Pessoas Jurídicas de Direito Privado 04 - Recolhimento por Sociedade Cooperativa 05 - Retenção por Fabricante de Máquinas e Veículos 99 - Outras Retenções | N | 002* | - | S |
| 02 | IND_NAT_RET | Indicador de Natureza da Retenção na Fonte, a partir de 2014:  Retenção Rendimentos sujeitos ao Regime Não Cumulativo (PJ Tributada pelo Lucro Real) e ao Regime Cumulativo (PJ Tributada pelo Lucro Presumido/Arbitrado): 01 - Retenção por Órgãos, Autarquias e Fundações Federais 02 - Retenção por outras Entidades da Administração Pública Federal 03 - Retenção por Pessoas Jurídicas de Direito Privado 04 - Recolhimento por Sociedade Cooperativa 05 - Retenção por Fabricante de Máquinas e Veículos 99 - Outras Retenções - Rendimentos sujeitos à regra geral de incidência (não cumulativa ou cumulativa)  Retenção Rendimentos sujeitos ao Regime Cumulativo, auferido por Pessoa Jurídica Tributada pelo Lucro Real: 51 - Retenção por Órgãos, Autarquias e Fundações Federais 52 - Retenção por outras Entidades da Administração Pública Federal 53 - Retenção por Pessoas Jurídicas de Direito Privado 54 - Recolhimento por Sociedade Cooperativa 55 - Retenção por Fabricante de Máquinas e Veículos 59 - Outras Retenções - Rendimentos sujeitos à regra específica de incidência cumulativa (art. 8º da Lei nº 10.637/2002 e art. 10 da Lei nº 10.833/2003) | N | 002* | - | S |
| 03 | PR_REC_RET | Período do Recebimento e da Retenção (MM/AAAA) | N | 006 | - | S |
| 04 | VL_RET_APU | Valor Total da Retenção | N | - | 02 | S |
| 05 | VL_RET_DED | Valor da Retenção deduzida da Contribuição devida no período da escrituração e em períodos anteriores. | N | - | 02 | S |
| 06 | VL_RET_PER | Valor da Retenção utilizada mediante Pedido de Restituição. | N | - | 02 | S |
| 07 | VL_RET_DCOMP | Valor da Retenção utilizada mediante Declaração de Compensação. | N | - | 02 | S |
| 08 | SLD_RET | Saldo de Retenção a utilizar em períodos de apuração futuros (04 – 05 - 06 - 07). | N | - | 02 | S |

Observações:
Conforme art. 9º da IN RFB 1.234, de 2012, com a redação dada pela IN RFB 1.540, de 2015, os valores retidos na fonte a título de Contribuição para o PIS/Pasep e Cofins nos pagamentos efetuados pelos órgãos da administração pública federal direta, autarquias e fundações federais, empresas públicas, sociedades de economia mista e demais PJs mencionadas na própria IN a outras PJs pelo fornecimento de bens e serviços, somente poderão ser deduzidos com o que for devido em relação à mesma espécie de contribuição e no mês de apuração a que se refere a retenção. Os valores retidos na fonte a título de Contribuição para o PIS/Pasep e Cofins que excederem ao valor da respectiva contribuição a pagar no mesmo mês de apuração poderão ser restituídos ou compensados com débitos relativos a outros tributos administrados pela RFB, mediante PER / DCOMP.
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [1300]
Campo 02 - Valores válidos: [01, 02, 03, 04, 05, 99]
A partir do período de apuração de janeiro de 2014, os valores válidos são: [01, 02, 03, 04, 05, 51, 52, 53, 54, 55 e 99], de acordo com a natureza da receita que sofreu retenção na fonte, conforme abaixo.
Campo 03 - Preenchimento: informe o período do recebimento e da retenção, conforme campo 02.
Validação: Devem ser informados conforme o padrão "mêsano" (mmaaaa), excluindo-se quaisquer caracteres de separação (tais como: ".", "/", "-", etc), sendo que o período deverá ser anterior ou o mesmo da atual escrituração.
Campo 04 - Preenchimento: Informe o valor total da retenção efetivamente sofrida referente à natureza informada no campo 02 e período informado no campo 03.
Campo 05 - Preenchimento: Informe o valor da retenção deduzida da contribuição devida no período da escrituração, se for o caso, e em períodos anteriores. O valor deverá ser informado de forma acumulada, ou seja, o valor descontado no atual período de apuração deverá ser somado àqueles deduzidos em períodos anteriores ao da atual escrituração (mesmo que a dedução tenha sido informada em DACON, anterior à entrega da EFD-Contribuições).
Os valores aqui relacionados devem guardar correlação com os valores informados nos Campos 06 (VL_RET_NC) e 10 (VL_RET_CUM) dos Registros “M200”.
Campo 06 - Preenchimento: Informe o valor da retenção utilizada mediante pedido de restituição. O valor deverá ser informado de forma acumulada, ou seja, o valor utilizado mediante pedido de restituição no atual período de apuração deverá ser somado àqueles transmitidos/pleiteados em períodos anteriores ao da atual escrituração.
Campo 07 - Preenchimento: Informe o valor da retenção utilizada mediante declaração de compensação. O valor deverá ser informado de forma acumulada, ou seja, o valor utilizado mediante declaração de compensação no atual período de apuração deverá ser somado àqueles transmitidos/pleiteados em períodos anteriores ao da atual escrituração.
Campo 08 - Preenchimento: Informe o saldo de retenção a utilizar em períodos de apuração futuros (04 – 05 - 06 - 07).
Validação: O valor do campo deverá ser igual a VL_RET_APU - VL_RET_DED - VL_RET_PER - VL_RET_DCOMP.
<!-- End Registro 1300 -->
<!-- Start Registro 1500 -->
Registro 1500: Controle de Créditos Fiscais – Cofins
Este registro tem por objetivo realizar o controle de saldos de créditos fiscais de períodos anteriores ao da atual escrituração, bem como eventual saldo credor apurado no próprio período da escrituração.
O saldo de créditos deverá ser segregado por período de apuração, devendo, ainda, levar em consideração a sua origem e, no caso de créditos transferidos por sucessão, o CNPJ da pessoa jurídica cedente do crédito. A chave deste registro é formada pelo campo PER_APU_CRED, campo ORIG_CRED, campo CNPJ_SUC e campo COD_CRED. Este registro tem por objetivo realizar o controle de saldos de créditos fiscais de períodos anteriores ao da atual escrituração, bem como eventual saldo credor apurado no próprio período da escrituração.
Salienta-se que para correta forma de identificação dos saldos dos créditos de período(s) passados(s), a favor do contribuinte, seja observado o critério da clareza, expressando mês a mês a posição (tipo de crédito, constituição, utilização parcial ou total) do referido crédito de forma individualizada, ou seja, não agregando ou totalizando com quaisquer outros, ainda que de mesma natureza ou período. Deve-se respeitar e preservar o direito ao crédito pelo período decadencial, logo, não é procedimento regular de escrituração englobar ou relacionar em um mesmo registro, saldos de créditos referentes à meses distintos. Deve assim ser escriturado um registro para cada mês de períodos passados, que tenham saldos passíveis de utilização, no período a que se refere à escrituração atual.
O saldo de créditos deverá ser segregado por período de apuração, devendo, ainda, levar em consideração a sua origem e, no caso de créditos transferidos por sucessão, o CNPJ da pessoa jurídica cedente do crédito. A chave deste registro é formada pelo campo PER_APU_CRED, campo ORIG_CRED, campo CNPJ_SUC e campo COD_CRED.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1500" | C | 004* | - | S |
| 02 | PER_APU_CRED | Período de Apuração do Crédito (MM/AAAA) | N | 006 | - | S |
| 03 | ORIG_CRED | Indicador da origem do crédito: 01 – Crédito decorrente de operações próprias; 02 – Crédito transferido por pessoa jurídica sucedida. | N | 002* | - | S |
| 04 | CNPJ_SUC | CNPJ da pessoa jurídica cedente do crédito (se ORIG_CRED = 02). | N | 014* | - | N |
| 05 | COD_CRED | Código do Tipo do Crédito, conforme Tabela 4.3.6. | N | 003* | - | S |
| 06 | VL_CRED_APU | Valor Total do crédito apurado na Escrituração Fiscal Digital (Registro M500) ou em demonstrativo DACON (Fichas 16A e 16B) de período anterior. | N | - | 02 | S |
| 07 | VL_CRED_EXT_APU | Valor de Crédito Extemporâneo Apurado (Registro 1501), referente a Período Anterior, Informado no Campo 02 – PER_APU_CRED | N | - | 02 | N |
| 08 | VL_TOT_CRED_APU | Valor Total do Crédito Apurado (06 + 07) | N | - | 02 | S |
| 09 | VL_CRED_DESC_PA_ANT | Valor do Crédito utilizado mediante Desconto, em Período(s)  Anterior(es) | N | - | 02 | S |
| 10 | VL_CRED_PER_PA_ANT | Valor do Crédito utilizado mediante Pedido de Ressarcimento, em Período(s) Anterior(es). | N | - | 02 | N |
| 11 | VL_CRED_DCOMP_PA_ANT | Valor do Crédito utilizado mediante Declaração de Compensação Intermediária (Crédito de Exportação), em Período(s) Anterior(es) | N | - | 02 | N |
| 12 | SD_CRED_DISP_EFD | Saldo do Crédito Disponível para Utilização neste Período de Escrituração (08-09-10-11) | N | - | 02 | S |
| 13 | VL_CRED_DESC_EFD | Valor do Crédito descontado neste período de escrituração | N | - | 02 | N |
| 14 | VL_CRED_PER_EFD | Valor do Crédito objeto de Pedido de Ressarcimento (PER) neste período de escrituração | N | - | 02 | N |
| 15 | VL_CRED_DCOMP_EFD | Valor do Crédito utilizado mediante Declaração de Compensação Intermediária neste período de escrituração | N | - | 02 | N |
| 16 | VL_CRED_TRANS | Valor do crédito transferido em evento de cisão, fusão ou incorporação | N | - | 02 | N |
| 17 | VL_CRED_OUT | Valor do crédito utilizado por outras formas | N | - | 02 | N |
| 18 | SLD_CRED_FIM | Saldo de créditos a utilizar em período de apuração futuro (12-13-14-15-16-17). | N | - | 02 | S |

Observações: Será preenchido um registro para cada período de apuração no qual exista saldo de créditos, utilizados neste período da escrituração ou a serem utilizados em períodos futuros.
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [1500]
Campo 02 - Preenchimento: informar o período em que o saldo credor foi apurado no formato “mmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o período informado deverá ser o mesmo ou anterior ao da atual escrituração
Campo 03 - Valores válidos: [01, 02]
Campo 04 - Preenchimento: caso o crédito sendo informado no registro refira-se a crédito transferido por pessoa jurídica sucedida (Campo ORIG_CRED preenchido com valor 02), informe neste campo o respectivo CNPJ. Caso contrário deve o campo ficar em branco.
Campo 05 - Preenchimento: informe o código do tipo do crédito cujo saldo credor está sendo informado no registro, conforme a Tabela “4.3.6 – Tabela Código de Tipo de Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 06 - Preenchimento: Informe neste campo o valor do crédito apurado no respectivo período de apuração. Para períodos em que não houve transmissão da escrituração (períodos anteriores ao início da obrigatoriedade de escrituração), este valor deve corresponder ao lançado no respectivo demonstrativo DACON.
Para períodos em que houve transmissão de escrituração o valor deste campo deverá corresponder ao valor do Campo 12 - VL_CRED_DISP, relativo ao mesmo COD_CRED do registro M500 do período de apuração do crédito, no caso de crédito apurado pela própria pessoa jurídica.
No caso de crédito oriundo de pessoa jurídica sucedida, o valor deste campo deverá corresponder ao valor da soma dos Campos 07 - VL_CRED_COFINS, relativos ao mesmo COD_CRED e CNPJ_SUCED do registro F800 do mesmo período de transferência do crédito.
Campo 07 - Preenchimento: Crédito extemporâneo é aquele cujo período de apuração ou competência do crédito se refere a período anterior ao da escrituração atual, mas que somente agora está sendo registrado. Estes documentos deverão ser informados no registro 1501.
Validação: O valor deste campo deverá ser igual à soma do campo 17 (VL_COFINS) dos Registros 1501 quando o respectivo campo 14 (CST_COFINS) for igual 50, 51, 52, 60, 61 e 62, adicionado à soma do campo 02 (VL_CRED_COFINS_TRIB_MI), campo 03 (VL_CRED_COFINS_NT_MI) e do campo 04 (VL_CRED_COFINS_ EXP) dos Registros 1502 quando o respectivo campo 14 (CST_COFINS) do registro 1501 for igual a 53, 54, 55, 56, 63, 64, 65 ou 66.
Campo 08 - Validação: Valor total do crédito apurado, correspondendo à soma dos campos 06 (VL_CRED_APU) e 07 (VL_CRED_EXT_APU)
Campo 09 - Preenchimento: Informar o valor do crédito utilizado mediante desconto no próprio período de apuração do crédito e em períodos subsequentes, anteriores ao da escrituração atual. No caso de períodos abrangidos pela entrega da escrituração o valor do crédito apurado pela própria pessoa jurídica, utilizado mediante desconto é obtido no campo 14 (VL_CRED_DESC) do registro M500.
Campo 10 - Preenchimento: Informar o valor do crédito utilizando mediante Pedido de Ressarcimento em períodos subsequentes ao de apuração do crédito, anteriores ao da escrituração atual.
Validação: O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 201, 202, 203, 204, 208, 301, 302, 303, 304, 307 ou 308.
Campo 11 - Preenchimento: Informar o valor do crédito utilizando mediante Declaração de Compensação Intermediária (compensação específica para créditos de exportação, objeto de Dcomp transmitida no próprio trimestre de apuração do crédito) em períodos subsequentes ao de apuração do crédito, anteriores ao da escrituração atual.
Validação: O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 301, 302, 303, 304 ou 308.
Campo 12 - Preenchimento: Preencher com o saldo do crédito disponível para utilização no período da atual escrituração, correspondendo à subtração do valor do campo 08 (VL_TOT_CRED_APU) pelos valores dos campos 09 (VL_CRED_DESC_PA_ANT), 10 (VL_CRED_PER_PA_ANT) e 11 (VL_CRED_DCOMP_PA_ANT).
Campo 13 - Preenchimento: Informar o valor do crédito disponível, conforme apurado no campo 12 (SD_CRED_DISP_EFD), utilizado mediante desconto no atual período de escrituração. A soma dos valores lançados neste campo deverá corresponder àquele registrado no campo 04 (VL_TOT_CRED_DESC_ANT) do registro M200.
Campo 14 - Preenchimento: Informar o valor do crédito utilizando mediante Pedido de Ressarcimento no período da atual escrituração. O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 201, 202, 203, 204, 208, 301, 302, 303, 304, 307 ou 308.
Campo 15 - Preenchimento: Informar o valor do crédito utilizando mediante Declaração de Compensação Intermediária (compensação específica para créditos de exportação, objeto de Dcomp transmitida no próprio trimestre de apuração do crédito) no período da escrituração atual. O campo deve ser informado apenas se os valores do campo 05 (COD_CRED) forem iguais a 301, 302, 303, 304 ou 308.
Campo 16 - Preenchimento: Informar o valor do crédito transferido em evento de cisão, fusão ou incorporação. O valor deste campo deverá ser recuperado na escrituração da pessoa jurídica sucessora, no campo 07 (VL_CRED_COFINS).
Campo 17 - Preenchimento: Informar o valor do crédito utilizado por outras formas, conforme previsão legal.
Campo 18 - Preenchimento: Informar o valor do saldo de crédito, se existente, para aproveitamento em períodos futuros, correspondendo à subtração do valor do campo 12 (SD_CRED_DISP_EFD) pelos valores dos campos 13 (VL_CRED_DESC_EFD), 14 (VL_CRED_PER_EFD), 15 (VL_CRED_DCOMP_EFD), 16 (VL_CRED_TRANS) e 17 (VL_CRED_OUT).
<!-- End Registro 1500 -->
<!-- Start Registro 1501 -->
Registro 1501: Apuração de Crédito Extemporâneo - Documentos e Operações de Períodos Anteriores – Cofins
Crédito extemporâneo é aquele cujo período de apuração ou competência do crédito se refere a período anterior ao da escrituração atual, mas que somente agora está sendo registrado. O crédito extemporâneo deverá ser informado, preferencialmente, mediante a retificação da escrituração cujo período se refere o crédito. No entanto, se a retificação não for possível, devido ao prazo previsto na Instrução Normativa RFB nº 1.052, de 2010, a PJ deverá detalhar suas operações através deste registro.
Este registro deverá ser utilizado para detalhar as informações prestadas no campo 07 do registro pai 1500.
Deve ser ressaltado que o crédito apurado no período da escrituração pelo método de apropriação direta (Art. 3º, § 8º, da Lei nº 10.833/04), referente a aquisições, custos e despesas incorridos em período anteriores ao da escrituração, não se trata de crédito extemporâneo, se a sua efetividade só vem a ser constituída no período atual da escrituração.

| ESCLARECIMENTOS IMPORTANTES QUANTO A NÃO VALIDAÇÃO DE REGISTROS DE CRÉDITOS EXTEMPORANEOS, A PARTIR DE AGOSTO DE 2013. |
| --- |
| 1. Os registros para informação extemporânea de créditos (registros 1101, 1102, 1501, 1502) e de contribuições (1200, 1210,1220 e 1600,1610,1620), passíveis de escrituração para os fatos geradores ocorridos até 31/07/2013, tanto na versão 2.04a como na nova versão 2.05, tinha a sua justificativa de escrituração apenas para os casos em que o período de apuração a que dissesse respeito a operação/documento fiscal, geradora de contribuição ou crédito, ainda não informada em escrituração já transmitida, não pudesse ser mais objeto de retificação, por ter expirado o prazo de retificação até então vigente na redação original da IN RFB 1.252/2012 (retificação até o término do ano calendário seguinte ao que se refere a escrituração original), conforme consta orientação no próprio Guia Prático da Escrituração, de que estes registros só deveriam ser utilizados, na impossibilidade de retificar as escriturações referentes às operações ainda não escrituradas. 2. Com o novo disciplinamento referente à retificação da EFD-Contribuições determinado pela IN RFB nº 1.387/2013, permitindo a escrituração e transmissão de arquivo retificador no prazo decadencial das contribuições, ou seja, em até cinco anos, a contar do período de apuração da EFD-Contribuições a ser retificada, deixa de ter qualquer fundamento de aplicabilidade e de validade os referidos registros, uma vez que todas as normas editadas pela Receita Federal quanto às obrigações acessórias, inclusive as do Sped, estabelece o instituto da retificação, para o contribuinte acrescentar, informar, registrar, sanear, qualquer fato que deveria ser incluído na declaração/escrituração original, conforme prazo e condições de retificação definidos para cada obrigação acessória. 3. No tocante à EFD-Contribuições, o prazo em vigor para retificação é agora de cinco anos, de forma que eventual documento ou operação que não tenha sido devidamente escriturado em qualquer escrituração dos anos de 2011, 2012 ou 2013, podem agora ser regularizados, mediante a retificação da escrituração original correspondente, nos Blocos A, C, de F.  4. Registre-se que, diferentemente da EFD-ICMS/IPI, a EFD-Contribuições não limita ou recusa na escrituração de documentos e operações nos Blocos A, C, D ou F, a escrituração de documentos cuja data de emissão seja diferente (meses anteriores ou posteriores) ao que se refere a escrituração.  Assim, na EFD-Contribuições do Período de Apuração referente a agosto de 2013, por exemplo, pode ser incluído documentos que, mesmo emitidos em meses anteriores a agosto/2013, ou emitidos em meses posteriores a agosto/2013, desde que o fato (receita ou operação geradora de crédito) tenha por período de competência, o mês da escrituração, ou seja, agosto de 2013. Em resumo, a EFD-Contribuições nunca validou como extemporâneo um documento, ou deixou de considerar como válido o documento/operação, em função deste vir a ter data de emissão diferente ao do período de apuração a que se refere. O PVA nas versões disponibilizadas em ambiente de produção continua validando eventual registro extemporâneo, se o arquivo txt importado se referir a PA igual ou anterior a julho de 2013. Para as escriturações com período de apuração a partir de agosto de 2013, o PVA não valida nem permite a geração de registros de operação extemporânea, gerando ocorrência de erro de escrituração. |


| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1501" | C | 004* | - | S |
| 02 | COD_PART | Código do participante (Campo 02 do Registro 0150) | C | 060 | - | N |
| 03 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 04 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1. | C | 002* | - | N |
| 05 | SER | Série do documento fiscal | C | 004 | - | N |
| 06 | SUB_SER | Subsérie do documento fiscal | C | 003 | - | N |
| 07 | NUM_DOC | Número do documento fiscal | N | 009 | - | N |
| 08 | DT_OPER | Data da Operação (ddmmaaaa) | N | 008* | - | S |
| 09 | CHV_NFE | Chave da Nota Fiscal Eletrônica | N | 044* | - | N |
| 10 | VL_OPER | Valor da Operação | N | - | 02 | S |
| 11 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 12 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | S |
| 13 | IND_ORIG_CRED | Indicador da origem do crédito: 0 – Operação no Mercado Interno 1 – Operação de Importação | C | 001* | - | S |
| 14 | CST_COFINS | Código da Situação Tributária referente ao COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 15 | VL_BC_COFINS | Base de Cálculo do Crédito de COFINS (em valor ou em quantidade) | N | - | 03 | S |
| 16 | ALIQ_COFINS | Alíquota do COFINS (em percentual ou em reais) | N | - | 04 | S |
| 17 | VL_COFINS | Valor do Crédito de COFINS | N | - | 02 | S |
| 18 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 19 | COD_CCUS | Código do Centro de Custos | C | 255 | - | N |
| 20 | DESC_COMPL | Descrição complementar do Documento/Operação | C | - | - | N |
| 21 | PER_ESCRIT | Mês/Ano da Escrituração em que foi registrado o documento/operação (Crédito pelo método da Apropriação Direta). | N | 006* | - | N |
| 22 | CNPJ | CNPJ do estabelecimento gerador do crédito extemporâneo (Campo 04  do Registro 0140) | N | 014* | - | S |

Observações:.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [1501];
Campo 02 - Validação: o código informado neste campo deve está relacionado no registro 0150, no campo COD_PART.
Campo 03 - Preenchimento: o código do item a que se refere a operação informado neste campo, quando existir, deve está relacionado no registro 0200, ressaltando-se que os códigos informados devem ser os definidos pelo pessoa jurídica titular da escrituração.
Campo 04 - Preenchimento: o valor informado deve constar na tabela 4.1.1 do Manual do Leiaute da EFD-Contribuições. O “código” a ser informado não é exatamente o “modelo” do documento, devendo ser consultada a tabela 4.1.1. Exemplo: o código “01” deve ser utilizado para os modelos “1” ou “1A".
Campo 05 - Preenchimento: informar a série do documento fiscal, se existir.
Campo 06 - Preenchimento: informar a subsérie do documento fiscal, se existir.
Campo 07 – Validação: Informar o número da nota fiscal ou documento internacional equivalente, se for o caso.
Campo 08 - Preenchimento: informar a data da operação escriturada neste registro, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
No caso da operação não se referir a um dia específico, ou se referir a mais de um dia, deve ser informado o dia final de referência ou o ultimo dia da escrituração, conforme o caso.
Campo 09 - Preenchimento: Neste campo deve ser informado a chave ou código de verificação, no caso de nota fiscal eletrônica.
Campo 10 – Preenchimento: Informar o valor total da operação/item escriturado neste registro.
Campo 11 - Preenchimento: Devem ser registrados os códigos de operação que correspondem ao tratamento tributário relativo à destinação do item, se for o caso de documento fiscal sujeito ao ICMS.
Campo 12 - Preenchimento: Informar neste campo o código da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 13 - Valores válidos: [0, 1]
Preenchimento: Informar o código que indique se a operação tem por origem o mercado interno ou externo (importação de bens e serviços).
Campo 14 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a COFINS (CST), conforme a Tabela I constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 15 - Preenchimento: informar neste campo a base de cálculo da COFINS referente à operação/item, para fins de apuração do crédito. Caso o crédito seja apurado por unidade de medida de produto, informe a quantidade da base de cálculo com três casas decimais. Caso contrário, utilize duas casas decimais.
Campo 16 - Preenchimento: informar neste campo a alíquota aplicável para fins de apuração do crédito. Caso o crédito seja apurado por unidade de medida de produto, utilize a alíquota em reais, caso contrário utilize a alíquota em percentual.
Campo 17 – Preenchimento: informar o valor do crédito da COFINS referente à operação/item escriturado neste registro, correspondendo a VL_BC_COFINS x ALIQ_COFINS, no caso de apuração por unidade de medida de produto ou VL_BC_COFINS x ALIQ_COFINS/100, caso contrário.
Validação: a soma dos valores deste campo deverá ser transportada para o campo 07 - VL_CRED_EXT_APU do registro pai 1500.
Campo 18 - Preenchimento: informar o Código da Conta Analítica. Exemplos: estoques, custos, despesas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo 19 - Preenchimento: Informar neste campo o Código do Centro de Custo relacionado à operação, se existir.
Campo 20 - Preenchimento: Neste campo pode ser informada a descrição complementar da operação ou do item, objeto de escrituração neste registro.
Campo 21 - Preenchimento:  No caso de apropriação direta de créditos comuns, informar o Mês/Ano da Escrituração em que foi registrado o documento/operação. Caso contrário deixar o campo em branco.
Validação: Devem ser informados conforme o padrão "mêsano" (mmaaaa), excluindo-se quaisquer caracteres de separação (tais como: ".", "/", "-", etc), sendo que o período deverá ser anterior ao da atual escrituração.
Campo 22 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações escrituradas neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deverá estar cadastrado no Registro 0140.
<!-- End Registro 1501 -->
<!-- Start Registro 1502 -->
Registro 1502: Detalhamento do Crédito Extemporâneo Vinculado a Mais de Um Tipo de Receita – Cofins
Este registro deverá ser preenchido quando CST_COFINS do registro 1101 for referente a operações com direito a crédito (códigos 53, 54, 55, 56, 63, 64, 65 ou 66), independentemente do método de apropriação dos créditos comuns (apropriação direta ou rateio proporcional).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1502" | C | 004* | - | S |
| 02 | VL_CRED_COFINS_TRIB_MI | Parcela do Crédito de COFINS, vinculada a Receita Tributada no Mercado Interno | N | - | 02 | N |
| 03 | VL_CRED_COFINS_NT_MI | Parcela do Crédito de COFINS, vinculada a Receita Não Tributada no Mercado Interno | N | - | 02 | N |
| 04 | VL_CRED_COFINS_ EXP | Parcela do Crédito de COFINS, vinculada a Receita de Exportação | N | - | 02 | N |

Observações: Será preenchido quando CST_ COFINS do registro 1501 for referente a operações com direito a crédito (códigos 53, 54, 55, 56, 63, 64, 65 ou 66).
Nível hierárquico - 4
Ocorrência - 1:1
Campo 01 - Valor Válido: [1502]
Campo 02 - Preenchimento: informar o valor da parcela do crédito de COFINS, informado no campo 17 - VL_COFINS, vinculada à receita tributada no mercado interno.
Validação: este campo só deverá ser preenchido se o campo 05 - COD_CRED do registro 1500 iniciar com “1” (crédito vinculado à receita tributada no mercado interno).
Campo 03 - Preenchimento: informar o valor da parcela do crédito de COFINS, informado no campo 17 - VL_COFINS, vinculada à receita não tributada no mercado interno.
Validação: este campo só deverá ser preenchido se o campo 05 - COD_CRED do registro 1500 iniciar com “2” (crédito vinculado à receita não tributada no mercado interno).
Campo 04 - Preenchimento: informar o valor da parcela do crédito de COFINS, informado no campo 17 - VL_COFINS, vinculada à receita de exportação.
Validação: este campo só deverá ser preenchido se o campo 05 - COD_CRED do registro 1500 iniciar com "3" (crédito vinculado à receita de exportação).
<!-- End Registro 1502 -->
<!-- Start Registro 1600 -->
Registro 1600: Contribuição Social Extemporânea – Cofins
Contribuição social extemporânea é aquela cujo documento/operação correspondente deveria ter sido escriturado e considerado na apuração da contribuição de período anterior, mas que somente agora está sendo registrado. A contribuição social extemporânea, por não ter sido escriturada no período correto, acarreta o respectivo recolhimento com pagamento de multa e juros de mora, caso não haja crédito/deduções válidas a serem descontadas.
Deverá ser gerado um registro para cada período de escrituração, natureza de contribuição a recolher, bem como data de recolhimento, se existir. Desta forma, a chave deste registro é formada pelos campos: PER_APUR_ANT + NAT_CONT_REC + DT_RECOL.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1600" | C | 004* | - | S |
| 02 | PER_APUR_ANT | Período de Apuração da Contribuição Social Extemporânea (MMAAAA) | N | 006* | - | S |
| 03 | NAT_CONT_REC | Natureza da Contribuição a Recolher, conforme Tabela 4.3.5. | C | 002 | - | S |
| 04 | VL_CONT_APUR | Valor da Contribuição Apurada | N | - | 02 | S |
| 05 | VL_CRED_COFINS_DESC | Valor do Crédito de COFINS a Descontar, da Contribuição Social Extemporânea. | N | - | 02 | S |
| 06 | VL_CONT_DEV | Valor da Contribuição Social Extemporânea Devida. | N | - | 02 | S |
| 07 | VL_OUT_DED | Valor de Outras Deduções. | N | - | 02 | S |
| 08 | VL_CONT_EXT | Valor da Contribuição Social Extemporânea a pagar. | N | - | 02 | S |
| 09 | VL_MUL | Valor da Multa. | N | - | 02 | N |
| 10 | VL_JUR | Valor dos Juros. | N | - | 02 | N |
| 11 | DT_RECOL | Data do Recolhimento. | N | 008* | - | N |

Observações:
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [1600];
Campo 02 - Preenchimento: Preenchimento: informar o período em que a contribuição a recolher deveria ter sido apurada, no formato “mmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o período informado deverá ser anterior ao da atual escrituração.
Campo 03 - Preenchimento: informe o código da contribuição social que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 04 - Preenchimento: Informe o valor total da contribuição extemporânea apurada, referente ao código informado no campo 03 e data de recolhimento informada no campo 11, conforme detalhamento do registro filho 1610.
Campo 05 - Preenchimento: Informe o valor do crédito de COFINS a descontar, da contribuição social extemporânea, conforme detalhamento do registro filho 1620.
Campo 06 - Preenchimento: Informe o valor da contribuição social extemporânea devida, correspondendo à subtração do valor do campo 04 pelo valor do campo 05.
Campo 07 - Preenchimento: Informe o valor das demais deduções à contribuição social extemporânea devida.
Campo 08 - Preenchimento: Informe o valor da contribuição social extemporânea a pagar, correspondendo à subtração do valor do campo 06 pelo valor do campo 07.
Campo 09 - Preenchimento: Informe o valor da multa vinculado ao recolhimento da contribuição social extemporânea a pagar, no caso do valor informado no campo 08 ser maior do que zero.
Campo 10 - Preenchimento: Informe o valor dos juros vinculados ao recolhimento da contribuição social extemporânea a pagar, no caso do valor informado no campo 08 ser maior do que zero.
Campo 11 - Preenchimento: Informe a data do recolhimento da contribuição social extemporânea a pagar, no caso do valor informado no campo 08 ser maior do que zero. A data do recolhimento deverá estar compreendida no período da atual escrituração.
Validação: Informar a data no padrão "diamêsano" (ddmmaaaa), excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
<!-- End Registro 1600 -->
<!-- Start Registro 1610 -->
Registro 1610: Detalhamento da Contribuição Social Extemporânea – Cofins
Este registro deverá ser preenchido pela pessoa jurídica que apurou valores de contribuição social extemporânea no registro pai 1600, em relação a cada estabelecimento e participante, segregando as informações por data da operação, CST da COFINS, participante e conta contábil. Dessa forma, a chave deste registro é formada pelos campos: CNPJ + CST_COFINS + COD_PART + DT_OPER + ALIQ_COFINS + COD_CTA.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “1610” | C | 004* | - | S |
| 02 | CNPJ | Número de inscrição do estabelecimento no CNPJ (Campo 04 do Registro 0140). | N | 014* | - | S |
| 03 | CST_COFINS | Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 04 | COD_PART | Código do participante (Campo 02 do Registro 0150) | C | 060 | - | N |
| 05 | DT_OPER | Data da Operação (ddmmaaaa) | N | 008* | - | S |
| 06 | VL_OPER | Valor da Operação | N | - | 02 | S |
| 07 | VL_BC_COFINS | Base de cálculo da COFINS (em valor ou em quantidade) | N | - | 03 | S |
| 08 | ALIQ_COFINS | Alíquota da COFINS (em percentual ou em reais) | N | - | 04 | S |
| 09 | VL_COFINS | Valor da COFINS | N | - | 02 | S |
| 10 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 11 | DESC_COMPL | Descrição complementar do Documento/Operação | C | - | - | N |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [1610];
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações escrituradas neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deverá estar cadastrado no Registro 0140.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a COFINS (CST), conforme a Tabela I constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 04 - Validação: o código informado neste campo, se for o caso, deve estar relacionado no registro 0150, no campo COD_PART.
Campo 05 - Preenchimento: informar a data da operação escriturada neste registro, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”. No caso da operação não se referir a um dia específico, ou se referir a mais de um dia, deve ser informado o dia final de referência ou o ultimo dia da escrituração, conforme o caso.
Campo 06 – Preenchimento: Informar o valor total da operação/item escriturado neste registro.
Campo 07 - Preenchimento: informar neste campo a base de cálculo da COFINS referente à operação/item, para fins de apuração da contribuição social extemporânea. Caso a operação/item esteja sujeita à apuração por unidade de medida de produto, utilize três casas decimais, caso contrário, duas casas decimais.
Campo 08 - Preenchimento: informar neste campo a alíquota aplicável para fins de apuração da contribuição social extemporânea. Caso a operação/item esteja sujeita à apuração por unidade de medida de produto, utilize a respectiva alíquota em reais, caso contrário, utilize alíquota em percentual.
Campo 09 – Preenchimento: informar o valor da contribuição social extemporânea referente à operação/item escriturado neste registro, correspondendo a VL_BC_COFINS x ALIQ_COFINS, no caso de apuração por unidade de medida de produto ou VL_BC_COFINS x ALIQ_COFINS/100, caso contrário.
Validação: a soma dos valores deste campo deverá ser transportada para o campo 04 - VL_CONT_APUR do registro pai 1600.
Campo 10 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita da prestação de serviços, receitas da atividade, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo 11 - Preenchimento: Neste campo pode ser informada a descrição complementar da operação ou do item, objeto de escrituração neste registro.
<!-- End Registro 1610 -->
<!-- Start Registro 1620 -->
Registro 1620: Demonstração do Crédito a Descontar da Contribuição Extemporânea – Cofins
Este registro deverá ser preenchido pela pessoa jurídica que descontou créditos referentes aos valores de contribuição social extemporânea apurada no registro pai 1600. A informação deverá ser segregada em relação a cada código de crédito, período de apuração do respectivo crédito e sua origem. Dessa forma, a chave deste registro é formada pelos campos: PER_APUR_CRED + ORIG_CRED + COD_CRED.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1620" | C | 004* | - | S |
| 02 | PER_APU_CRED | Período de Apuração do Crédito (MM/AAAA) | N | 006 | - | S |
| 03 | ORIG_CRED | Indicador da origem do crédito: 01 – Crédito decorrente de operações próprias; 02 – Crédito transferido por pessoa jurídica sucedida. | N | 002* | - | S |
| 04 | COD_CRED | Código do Tipo do Crédito, conforme Tabela 4.3.6. | N | 003* | - | S |
| 05 | VL_CRED | Valor do Crédito a Descontar | N | - | 002 | S |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [1620]
Campo 02 - Preenchimento: Informe o período de apuração do crédito descontado da contribuição social extemporânea.
Validação: Devem ser informados conforme o padrão "mêsano" (mmaaaa), excluindo-se quaisquer caracteres de separação (tais como: ".", "/", "-", etc), sendo que o período informado no campo deve ser anterior ou igual ao período de apuração (PER_APUR_ANT) do registro pai 1600.
Campo 03 - Valores válidos: [01, 02]
Campo 04 - Preenchimento: informe o código do tipo do crédito cujo valor foi aproveitado para desconto da contribuição social extemporânea, conforme a Tabela “4.3.6 – Tabela Código de Tipo de Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informe o valor do crédito que foi aproveitado para desconto da contribuição social extemporânea. A soma dos valores deste campo deverá ser transportada para o campo 05 - VL_CRED_PIS_DESC do registro pai 1600.
<!-- End Registro 1620 -->
<!-- Start Registro 1700 -->
Registro 1700: Controle dos Valores Retidos na Fonte – Cofins
Este registro tem por objetivo realizar o controle dos saldos de valores retidos na fonte, de períodos anteriores e do período da atual escrituração. Estes valores, observada a legislação que regulamenta o assunto, poderão ser utilizados para dedução da contribuição cumulativa e/ou não cumulativa devida, conforme apuração constante dos registros M600.
As informações deverão estar consolidadas pela natureza da retenção na fonte e seu respectivo período de recebimento e retenção. Assim, a chave deste registro é formada pelos campos: IND_NAT_RET + PR_REC_RET.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1700" | C | 004* | - | S |
| 02 | IND_NAT_RET | Indicador de Natureza da Retenção na Fonte até 2013: 01 - Retenção por Órgãos, Autarquias e Fundações Federais 02 - Retenção por outras Entidades da Administração Pública Federal 03 - Retenção por Pessoas Jurídicas de Direito Privado 04 - Recolhimento por Sociedade Cooperativa 05 - Retenção por Fabricante de Máquinas e Veículos 99 - Outras Retenções | N | 002* | - | S |
| 02 | IND_NAT_RET | Indicador de Natureza da Retenção na Fonte, a partir de 2014:  Retenção Rendimentos sujeitos ao Regime Não Cumulativo (PJ Tributada pelo Lucro Real) e ao Regime Cumulativo (PJ Tributada pelo Lucro Presumido/Arbitrado): 01 - Retenção por Órgãos, Autarquias e Fundações Federais 02 - Retenção por outras Entidades da Administração Pública Federal 03 - Retenção por Pessoas Jurídicas de Direito Privado 04 - Recolhimento por Sociedade Cooperativa 05 - Retenção por Fabricante de Máquinas e Veículos 99 - Outras Retenções - Rendimentos sujeitos à regra geral de incidência (não cumulativa ou cumulativa)  Retenção Rendimentos sujeitos ao Regime Cumulativo, auferido por Pessoa Jurídica Tributada pelo Lucro Real: 51 - Retenção por Órgãos, Autarquias e Fundações Federais 52 - Retenção por outras Entidades da Administração Pública Federal 53 - Retenção por Pessoas Jurídicas de Direito Privado 54 - Recolhimento por Sociedade Cooperativa 55 - Retenção por Fabricante de Máquinas e Veículos 59 - Outras Retenções - Rendimentos sujeitos à regra específica de incidência cumulativa (art. 8º da Lei nº 10.637/2002 e art. 10 da Lei nº 10.833/2003) | N | 002* | - | S |
| 03 | PR_REC_RET | Período do Recebimento e da Retenção (MM/AAAA) | N | 006* | - | S |
| 04 | VL_RET_APU | Valor Total da Retenção | N | - | 02 | S |
| 05 | VL_RET_DED | Valor da Retenção deduzida da Contribuição devida no período da escrituração e em períodos anteriores | N | - | 02 | S |
| 06 | VL_RET_PER | Valor da Retenção utilizada mediante Pedido de Restituição. | N | - | 02 | S |
| 07 | VL_RET_DCOMP | Valor da Retenção utilizada mediante Declaração de Compensação. | N | - | 02 | S |
| 08 | SLD_RET | Saldo de Retenção a utilizar em períodos de apuração futuros (04 - 05 - 06 - 07). | N | - | 02 | S |

Observações:
Conforme art. 9º da IN RFB 1.234, de 2012, com a redação dada pela IN RFB 1.540, de 2015, os valores retidos na fonte a título de Contribuição para o PIS/Pasep e Cofins nos pagamentos efetuados pelos órgãos da administração pública federal direta, autarquias e fundações federais, empresas públicas, sociedades de economia mista e demais PJs mencionadas na própria IN a outras PJs pelo fornecimento de bens e serviços, somente poderão ser deduzidos com o que for devido em relação à mesma espécie de contribuição e no mês de apuração a que se refere a retenção. Os valores retidos na fonte a título de Contribuição para o PIS/Pasep e Cofins que excederem ao valor da respectiva contribuição a pagar no mesmo mês de apuração poderão ser restituídos ou compensados com débitos relativos a outros tributos administrados pela RFB, mediante PER / DCOMP.
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [1700]
Campo 02 - Valores válidos: [01, 02, 03, 04, 05, 99]
A partir do período de apuração de janeiro de 2014, os valores válidos são: [01, 02, 03, 04, 05, 51, 52, 53, 54, 55 e 99], de acordo com a natureza da receita que sofreu retenção na fonte, conforme abaixo.

| Código Natureza Retenção | Receitas / Rendimentos Correspondentes |
| --- | --- |
| 01, 02, 03, 04, 05, 99 | Receita Não Cumulativa: Art. 1º da Lei nº 10.833/03 |
| 01, 02, 03, 04, 05, 99 | Receita Cumulativa - PJ Lucro Presumido/Arbitrado: Art. 10 da Lei nº 10.833/03 |
|   |   |
| 51, 52, 53, 54, 55, 59 | Receita Cumulativa - PJ Lucro Real (Bloco I): Art. 10, inciso I da Lei nº 10.833/03 |
| 51, 52, 53, 54, 55, 59 | Receita Cumulativa - PJ Lucro Real: Art. 10, incisos VII a XXIX da Lei nº 10.833/03 |

Campo 03 - Preenchimento: informe o período do recebimento e da retenção, conforme campo 02.
Validação: Devem ser informados conforme o padrão "mêsano" (mmaaaa), excluindo-se quaisquer caracteres de separação (tais como: ".", "/", "-", etc), sendo que o período deverá ser anterior ou o mesmo da atual escrituração.
Campo 04 - Preenchimento: Informe o valor total da retenção efetivamente sofrida referente à natureza informada no campo 02 e período informado no campo 03.
Campo 05 - Preenchimento: Informe o valor da retenção deduzida da contribuição devida no período da escrituração, se for o caso, e em períodos anteriores. O valor deverá ser informado de forma acumulada, ou seja, o valor descontado no atual período de apuração deverá ser somado àqueles deduzidos em períodos anteriores ao da atual escrituração (mesmo que a dedução tenha sido informada em DACON, anterior à entrega da EFD-Contribuições).
Os valores aqui relacionados devem guardar correlação com os valores informados nos Campos 06 (VL_RET_NC) e 10 (VL_RET_CUM) dos Registros “M600”.
Campo 06 - Preenchimento: Informe o valor da retenção utilizada mediante pedido de restituição. O valor deverá ser informado de forma acumulada, ou seja, o valor utilizado mediante pedido de restituição no atual período de apuração deverá ser somado àqueles transmitidos/pleiteados em períodos anteriores ao da atual escrituração.
Campo 07 - Preenchimento: Informe o valor da retenção utilizada mediante declaração de compensação. O valor deverá ser informado de forma acumulada, ou seja, o valor utilizado mediante declaração de compensação no atual período de apuração deverá ser somado àqueles transmitidos/pleiteados em períodos anteriores ao da atual escrituração.
Campo 08 - Preenchimento: Informe o saldo de retenção a utilizar em períodos de apuração futuros (04 – 05 - 06 - 07).
Validação: O valor do campo deverá ser igual a VL_RET_APU - VL_RET_DED - VL_RET_PER - VL_RET_DCOMP.
<!-- End Registro 1700 -->
<!-- Start Registro 1800 -->
Registro 1800: Incorporação Imobiliária – RET
Este registro deve ser preenchido pela pessoa jurídica que executa empreendimentos objeto de incorporação imobiliária e que apuram contribuição social com base em Regimes Especiais de Tributação – RET. As normas relativas ao RET, nas modalidades previstas na legislação tributária, encontram-se dispostas na Instrução Normativa RFB nº 1.435/2013.
Devem ser escriturados registros específicos para cada incorporação imobiliária, bem para cada Regime Especial estabelecido na legislação tributária, sujeitos ao pagamento mensal unificado a alíquotas diversas.
A receita da incorporação sujeita a tributação pelo RET não deve ser computada nos demais registros da escrituração, relativos a suas outras atividades empresariais, inclusive incorporações não optantes pelo RET.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1800" | C | 004* | - | S |
| 02 | INC_IMOB | Empreendimento objeto de Incorporação Imobiliária, optante pelo RET. | C | 090 | - | S |
| 03 | REC_RECEB_RET | Receitas recebidas pela incorporadora na venda das unidades imobiliárias que compõem a incorporação. | N | - | 02 | S |
| 04 | REC_FIN_RET | Receitas Financeiras e Variações Monetárias decorrentes das vendas submetidas ao RET. | N | - | 02 | N |
| 05 | BC_RET | Base de Cálculo do Recolhimento Unificado | N | - | 02 | S |
| 06 | ALIQ_RET | Alíquota do Recolhimento Unificado. | N | 006 | 02 | S |
| 07 | VL_REC_UNI | Valor do Recolhimento Unificado. | N | - | 02 | S |
| 08 | DT_REC_UNI | Data do recolhimento unificado | N | 008* | - | N |
| 09 | COD_REC | Código da Receita | C | 004 | - | N |

Observações:
Nível hierárquico - 2
Ocorrência - Vários (por arquivo)
Campo 01 - Valor Válido: [1800]
Campo 02 - Preenchimento: identifique o empreendimento objeto de incorporação imobiliária, optante pelo RET, informando o respectivo CNPJ do empreendimento, de acordo com o inciso XIII do art. 4º da IN RFB nº 1.634, de 2016, no formato “XXXXXXXXYYYYZZ” (14 caracteres, sem pontuação ou separadores).
Campo 03 - Preenchimento: informe o valor das receitas recebidas pela incorporadora na venda das unidades imobiliárias que compõem a incorporação.
Campo 04 - Preenchimento: informe o valor das receitas financeiras e variações monetárias decorrentes das vendas submetidas ao RET.
Campo 05 - Preenchimento: informe a base de cálculo do recolhimento unificado, correspondendo à soma dos campos 03 e 04, podendo ser deduzidas as vendas canceladas, as devoluções de vendas e os descontos incondicionais concedidos no período.
Campo 06 - Preenchimento: informe a alíquota aplicável ao recolhimento unificado. No caso da pessoa jurídica executar incorporações submetidas a alíquotas diversas, deverá ser gerado um registro para demonstrar as contribuições devidas de acordo com cada alíquota de incidência.
No caso de projetos de incorporação de imóveis residenciais considerados de interesse social (Lei nº 12.024/2009), bem como de construção ou reforma de estabelecimentos de educação infantil (Lei nº 12.715/2012), deve ser informada a alíquota de 1% (um por cento).
Em relação aos demais projetos submetidos ao RET, nos termos da Lei nº 10.931, de 2004, a alíquota a ser informada deve ser de 6% (seis por cento) ou de 4% (quatro por cento), conforme o período da escrituração e as disposições da Lei nº 10.931/2004.
Campo 07 - Preenchimento: informe o valor do recolhimento unificado, efetuado na data e código de receita, informados nos campos 08 e 09, respectivamente.
Campo 08 - Preenchimento: informe a data do recolhimento unificado, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 09 - Preenchimento: informe o código da receita, conforme consta no DARF ou DCOMP.
<!-- End Registro 1800 -->
<!-- Start Registro 1809 -->
Registro 1809: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “1809”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1809" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - | S |

Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [1809]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro 1809 -->
<!-- Start Registro 1900 -->
Registro 1900: Consolidação dos Documentos Emitidos no Período por Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido–Regime de Caixa ou de Competência
Registro para a pessoa jurídica sujeita à tributação com base no lucro presumido, que procedeu à escrituração de suas receitas de forma consolidada, pelo regime de caixa (registro “F500” ou “F510”) ou de competência (registro “F550” ou “F560”), informar o valor consolidado dos documentos fiscais e demais documentos, emitidos no período da escrituração, representativos de receitas da venda de bens e serviços efetuada no período, independente de sua realização (recebimento) ou não.
Atenção: Este registro é de escrituração opcional até o período de apuração referente a março de 2013. A partir de abril de 2013 o registro “1900” passa a ser de escrituração obrigatória. Mesmo na inexistência de receita de vendas no período da escrituração, o registro 1900 deve ser informado.
Neste sentido, a empresa não auferindo receita nova no mês a que se refere a escrituração, deve gerar o registro 1900 (especificado por documento fiscal usualmente utilizado para o registro das receitas, no Campo 03) informando no campo 07 o valor R$ 0,00 e no campo 08 a quantidade 0 (zero).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1900” | C | 004* | - | S |
| 02 | CNPJ | CNPJ do estabelecimento da pessoa jurídica, emitente dos documentos geradores de receita | N | 014* | - | S |
| 03 | COD_MOD | Código do modelo do documento fiscal conforme a Tabela 4.1.1, ou: 98 – Nota Fiscal de Prestação de Serviços (ISSQN) 99 – Outros Documentos | C | 002* | - | S |
| 04 | SER | Série do documento fiscal | C | 004 | - | N |
| 05 | SUB_SER | Subserie do documento fiscal | N | 020 | - | N |
| 06 | COD_SIT | Código da situação do documento fiscal: 00 – Documento regular 02 – Documento cancelado 99 – Outros | N | 02* | - | N |
| 07 | VL_TOT_REC | Valor total da receita, conforme os documentos emitidos no período, representativos da venda de bens e serviços | N | - | 02 | S |
| 08 | QUANT_DOC | Quantidade total de documentos emitidos no período | N | - | - | N |
| 09 | CST_PIS | Código da Situação Tributária do PIS/Pasep | N | 002* | - | N |
| 10 | CST_COFINS | Código da Situação Tributária da Cofins | N | 002* | - | N |
| 11 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 12 | INF_COMPL | Informações complementares | C | - | - | N |
| 13 | COD_CTA | Código da conta analítica contábil representativa da receita | C | 255 | - | N |

Observações: Neste registro, a pessoa jurídica irá informar, por estabelecimento, os valores totais consolidados representativos das receitas auferidas decorrentes da venda de bens, serviços ou de outras receitas, de acordo com cada modelo/tipo de documento, de natureza fiscal (notas fiscais) ou não (contratos, recibos, etc). Pode também a pessoa jurídica realizar a consolidação dos documentos levanto em conta demais informações dos documentos sendo consolidados, como: CFOP, CST, Série/Subsérie, Situação, Informações complementares e conta contábil.
Nível hierárquico - 2
Ocorrência -  Vários (por arquivo)
Campo 01 - Valor Válido: [1900]
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações passíveis de escrituração neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deve está cadastrado no Registro 0140.
Campo 03 - Preenchimento: Informar neste campo o Código indicador do modelo de documento fiscal a que se refere a receita consolidada e demonstrada neste registro.
Validação: deverá ser gerado um registro para segregar as receitas, no campo “03”, de conformidade com cada código de modelo de documento fiscal relacionado na Tabela 4.1.1 do leiaute da EFD-Contribuições (operações sujeitas ao ICMS).
No caso da receita escriturada se referir a documento fiscal de serviço (sujeito ao ISSQN), em modelo definido pelo Fisco Municipal, deve ser  informado no campo “03” o indicador “98”. E no caso de outros tipos de documentos representativos da receita auferida, deve ser informado o indicador “99”, detalhando a sua natureza ou histórico (contratos, recibos, etc) no campo “12”, de informações complementares.
Campo 04 - Preenchimento: informar, caso exista, a série do documento fiscal a que se refere o indicador informado no campo “03”.
Campo 05 - Preenchimento: informar, caso exista, a subsérie do documento fiscal a que se refere o indicador informado no campo “03”.
Campo 06 - Valores válidos: [00, 02, 99]
Campo 07 – Preenchimento: Informar neste campo o valor total da receita auferida no período da escrituração,  correspondente ao modelo de documento fiscal informado no campo “03”, independente de seu recebimento ou não.
Caso a pessoa jurídica realize a consolidação de documentos utilizando os demais campos não obrigatórios do registro (CFOP, CST, Série/Subsérie, Situação, Informações complementares e conta contábil) o valor total da receita a ser informado neste campo deve levar em conta também os correspondentes campos utilizados.
No caso de no mês da escrituração a pessoa jurídica não ter emitido documento fiscal algum, de modelo que usualmente ou regularmente é emitido e informado no registro 1900, pode a pessoa jurídica gerar o registro 1900, no mês sem emissão, informando nos campos 07 e 08 o valor zero.
Campo 08 – Preenchimento:  Informar neste campo a quantidade de documentos emitidos, correspondente ao modelo informado no campo “03”. Não precisa ser informado casas decimais, na escrituração deste campo.
Caso a pessoa jurídica realize a consolidação de documentos utilizando os demais campos não obrigatórios do registro (CFOP, CST, Série/Subsérie, Situação, Informações complementares e conta contábil) a quantidade de documentos a ser informada neste campo deve levar em conta também os correspondentes campos utilizados.
Campo 09 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 03 | Operação Tributável com Alíquota por Unidade de Medida de Produto |
| 04 | Operação Tributável Monofásica - Revenda a Alíquota Zero |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

OBS: Existindo mais de um CST para o modelo de documento consolidado no registro, sem que a pessoa jurídica tenha como decompor por cada CST, o campo 09 será escriturado em branco.
Campo 10 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 03 | Operação Tributável com Alíquota por Unidade de Medida de Produto |
| 04 | Operação Tributável Monofásica - Revenda a Alíquota Zero |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |
| 99 | Outras Operações |

OBS: Existindo mais de um CST para o modelo de documento consolidado no registro, sem que a pessoa jurídica tenha como decompor por cada CST, o campo 10 será escriturado em branco.
Campo 11 - Preenchimento: Informar neste campo o Código Fiscal de Operação (CFOP) correspondente às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 12 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
Campo 13 - Preenchimento: informar o Código da Conta Analítica representativa da receita informada neste registro. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, receita auferida no período, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Atenção:
Para as pessoas jurídicas que adotam o regime de competência para apuração do IR, da CSLL, do PIS/Pasep e da Cofins, devem informar no Campo 15 deste registro o código da conta contábil, representativa das receitas auferidas.
A não informação da conta contábil correspondente às operações, nos registros representativos de receitas e/ou de créditos acarretará:
- Para os fatos geradores até 31 de outubro de 2017, ocorrência de aviso/advertência (não impedindo a validação do registro);
- Para os fatos geradores a partir de 01 de novembro de 2017, ocorrência de erro (impedindo a validação do registro).
Informação de preenchimento – PJ tributadas com base no lucro presumido:
Considerando que o atual programa da EFD-Contribuições (versão 2.1.4) estabelece a obrigatoriedade de se informar nos registros da escrituração, das operações geradoras de receitas e/ou de créditos, a conta contábil (Campo COD_CONT), a partir do período de apuração de novembro de 2017;
Considerando que Instrução Normativa RFB nº 1.774, de 22.12.2017, dispensou da obrigatoriedade da escrituração contábil digital (ECD) as pessoas jurídicas tributadas com base no lucro presumido que não distribuíram, a título de lucro, sem incidência do Imposto sobre a Renda Retido na Fonte (IRRF), parcela de lucros ou dividendos, superior ao valor da base de cálculo do Imposto sobre a Renda diminuída dos impostos e contribuições a que estiver sujeita;
As pessoas jurídicas tributadas com base no lucro presumido não sujeitas à obrigatoriedade da ECD, nos termos da IN RFB nº 1.774/2017, poderão, opcionalmente, informar nos campos "COD_CTA" dos registros da EFD-Contribuições, para os fatos geradores a partir de novembro/2017, inclusive, a informação "Dispensa de ECD - IN RFB nº 1.774/2017".
<!-- End Registro 1900 -->
<!-- Start Registro 1990 -->
Registro 1990: Encerramento do Bloco 1

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "1990" | C | 004* | - | S |
| 02 | QTD_LIN_1 | Quantidade total de linhas do Bloco 1 | N | - | - | S |

Observações: Registro obrigatório
Nível hierárquico - 1
Ocorrência - Um (por arquivo)
Validação do Registro: registro único e obrigatório para todos os informantes da EFD-Contribuições.
Campo 01 - Valor Válido: [1990]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco 1 é igual ao valor informado no campo QTD_LIN_1 (registro 1990).
<!-- End Registro 1990 -->