# Bloco A - Versão 1.35

BLOCO A: Documentos Fiscais - Serviços (Sujeitos ao ISS)
As operações a serem escrituradas nos registros do Bloco A correspondem às operações de prestação de serviços (Receitas) e/ou de contratação de serviços (custos e/ou despesas geradoras de créditos) que não estão escrituradas nos registros constantes nos Blocos C, D e F. As operações de serviços escrituradas nos Blocos C, D e F não devem ser informadas no Bloco A.
Na hipótese de dispensa da emissão de notas fiscais de serviços, em decorrência de legislação ou ato municipal, documentos equivalentes serão aceitos na escrituração, devendo ser informados no Bloco F (registro F100), independente da Lei impor ou não forma especial a esses documentos equivalentes. Para a adequada validade dos mesmos, esses documentos devem ser de idoneidade indiscutível e conter os elementos definidores da operação.
<!-- Start Registro A001 -->
Registro A001: Abertura do Bloco A

| Nº | Campo | Descrição | Tipo | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "A001" | Texto fixo contendo "A001" | C | 004* | - | S |
| 02 | IND_MOV | Indicador de movimento: 0 - Bloco com dados informados; 1 - Bloco sem dados informados | Indicador de movimento: 0 - Bloco com dados informados; 1 - Bloco sem dados informados | C | 001 | - | S |

Observações: Registro de escrituração obrigatória.
Nível hierárquico - 1
Ocorrência – um por arquivo
Campo 01 - Valor Válido: [A001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro A001 -->
<!-- Start Registro A010 -->
Registro A010: Identificação do Estabelecimento
Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica a que se referem as operações e documentos fiscais informados neste bloco. Só devem ser escriturados no Registro A010 os estabelecimentos que efetivamente tenham realizado operações de prestação ou de contratação de serviços, mediante emissão de documento fiscal, que devam ser escrituradas no Bloco A.
O estabelecimento que não realizou operações passíveis de registro nesse bloco, no período da escrituração, não deve ser identificado no Registro A010.
Para cada estabelecimento cadastrado em “A010”, deve ser informado nos registros de nível inferior (Registros Filho) as operações próprias de prestação ou de contratação de serviços, mediante emissão de documento fiscal, no mercado interno ou externo.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “A010” | C | 004* | - | S |
| 02 | CNPJ | Número de inscrição do estabelecimento no CNPJ. | N | 014* | - | S |

Observações: Registro obrigatório (se IND_MOV igual a 0, em A001)
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Campo 01 - Valor Válido: [A010];
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações passíveis de escrituração neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deve está cadastrado no Registro 0140.
<!-- End Registro A010 -->
<!-- Start Registro A100 -->
Registro A100: Documento - Nota Fiscal de Serviço
Deve ser gerado um Registro A100 para cada documento fiscal a ser relacionado na escrituração, referente à prestação ou à contratação de serviços, que envolvam a emissão de documentos fiscais estabelecidos pelos Municípios, eletrônicos ou em papel.
Para cada registro A100, obrigatoriamente deve ser apresentado, pelo menos, um registro A170.
Para documento fiscal de serviço cancelado (código da situação = 02), somente podem ser preenchidos os campos de código da situação, indicador de operação, emitente, número do documento, série, subsérie e código do participante. Os campos série e subsérie não são obrigatórios e o campo código do participante é obrigatório nas operações de contratação de serviços.
Observação: Não podem ser informados, para um mesmo documento fiscal, dois ou mais registros com a mesma combinação de valores dos campos formadores da chave do registro. A chave deste registro é:
• para documentos com campo IND_EMIT igual a “1” (um) – emissão por terceiros: campo IND_OPER, campo IND_EMIT, campo COD_PART, campo COD_SIT, campo SER e campo NUM_DOC;
• para documentos com campo (IND_EMIT igual “0” (zero) – emissão própria: campo IND_OPER, campo IND_EMIT, campo COD_SIT, campo SER e campo NUM_DOC.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "A100" | C | 004* | - | S |
| 02 | IND_OPER | Indicador do tipo de operação: 0 - Serviço Contratado pelo Estabelecimento; 1 - Serviço Prestado pelo Estabelecimento. | C | 001* | - | S |
| 03 | IND_EMIT | Indicador do emitente do documento fiscal: 0 - Emissão Própria; 1 - Emissão de Terceiros | C | 001* | - | S |
| 04 | COD_PART | Código do participante (campo 02 do Registro 0150): - do emitente do documento, no caso de emissão de terceiros; - do adquirente, no caso de serviços prestados. | C | 060 | - | N |
| 05 | COD_SIT | Código da situação do documento fiscal: 00 – Documento regular 02 – Documento cancelado | N | 002* | - | S |
| 06 | SER | Série do documento fiscal | C | 020 | - | N |
| 07 | SUB | Subsérie do documento fiscal | C | 020 | - | N |
| 08 | NUM_DOC | Número do documento fiscal ou documento internacional equivalente | C | 060 | - | S |
| 09 | CHV_NFSE | Chave/Código de Verificação da nota fiscal de serviço eletrônica | C | 060 | - | N |
| 10 | DT_DOC | Data da emissão do documento fiscal | N | 008* | - | S |
| 11 | DT_EXE_SERV | Data de Execução / Conclusão do Serviço | N | 008* | - | N |
| 12 | VL_DOC | Valor total do documento | N | - | 02 | S |
| 13 | IND_PGTO | Indicador do tipo de pagamento: 0- À vista; 1- A prazo; 9- Sem pagamento. | C | 001* | - | S |
| 14 | VL_DESC | Valor total do desconto | N | - | 02 | N |
| 15 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | S |
| 16 | VL_PIS | Valor total do PIS | N | - | 02 | S |
| 17 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | S |
| 18 | VL_COFINS | Valor total da COFINS | N | - | 02 | S |
| 19 | VL_PIS_RET | Valor total do PIS retido na fonte | N | - | 02 | N |
| 20 | VL_COFINS_RET | Valor total da COFINS retido na fonte. | N | - | 02 | N |
| 21 | VL_ISS | Valor do ISS | N | - | 02 | N |

Observações:
1. Devem ser informadas no Registro A100 as operações de serviços, prestados ou contratados, cujo documento fiscal não seja objeto de escrituração nos Blocos C, D e F.
2. O detalhamento das informações dos itens da Nota Fiscal de Serviço que repercute na apuração das contribuições sociais (serviços prestados) e dos créditos (serviços contratados) deve ser informado, em relação a cada item relacionado no documento, no Registro Filho “A170”.
3. Caso a pessoa jurídica tenha contratado serviços à pessoa física ou jurídica domiciliada no exterior, com direito a crédito nas formas previstas na Lei nº 10.865, de 2004, deve preencher o Registro “A120” para validar a apuração do crédito.
4. Caso a pessoa jurídica tenha realizado operações de prestação de serviço ou de contratação de serviços com direito a crédito, sem a emissão de Nota Fiscal de Serviço especifica ou documento internacional equivalente (no caso de serviços contratados com pessoa física ou jurídica domiciliada no exterior), deve proceder à escrituração das referidas operações no Registro “F100”, detalhando os campos necessários para a validação das contribuições sociais ou dos créditos.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [A100]
Campo 02 - Valores válidos: [0, 1]
Preenchimento: indicar o tipo da operação, conforme os códigos de preenchimento do campo. No caso de serviço contratado informar o valor “0” e no caso de prestação de serviços informar o valor “1”.
Campo 03 - Valores válidos: [0, 1]
Preenchimento: consideram-se de emissão própria somente os documentos fiscais emitidos pelo estabelecimento informado em A010. Documentos emitidos por outros estabelecimentos, ainda que da mesma empresa, devem ser considerados como documentos emitidos por terceiros.
Campo 04 - Validação: o valor informado deve existir no campo COD_PART do registro 0150. Campo obrigatório na escrituração das operações de contratação de serviços (operações geradoras de crédito). Caso o serviço seja prestado para consumidor final, não há obrigatoriedade de informação do código do participante.
Campo 05 - Valores válidos: [00, 02]
Campo 06 - Preenchimento: informar a série do documento fiscal a que se refere o item. Caso o documento fiscal não tenha série, o campo não é preenchido.
Campo 07 - Preenchimento: informar a subsérie do documento fiscal a que se refere o item, caso conste no documento.
Campo 08 – Validação: informar o número da nota fiscal ou documento internacional equivalente. Na impossibilidade de informar o número específico de documento fiscal, o campo deve ser preenchido com o conteúdo “SN”.
Campo 09 - Preenchimento: neste campo deve ser informado a chave ou código de verificação, no caso de nota fiscal de serviço eletrônica.
Campo 10 - Preenchimento: informar a data de emissão do documento fiscal, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data de execução/conclusão do serviço (campo 11) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 11 - Preenchimento: informar a data de execução ou da conclusão do serviço. No caso de não constar no documento fiscal a data da execução/conclusão do serviço contratado, ou esta não ser conhecida pela pessoa jurídica, informar a data de emissão do documento fiscal ou do último dia da escrituração, conforme o caso.
No caso de serviços contratados cuja execução total/conclusão venha a ocorrer em período posterior ao da escrituração, como nos contratos de longo prazo, pode ser informado neste campo a data correspondente à data de laudo técnico que certifique a porcentagem executada em função do progresso físico da empreitada ou produção.
Validação: a data informada neste campo ou a data de emissão do documento fiscal (campo 10) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 12 – Preenchimento: informar o valor total do documento fiscal.
Campo 13 – Preenchimento: informar o tipo de pagamento pactuado, independente do pagamento ocorrer em período anterior, no próprio período ou em período posterior ao de referência da escrituração.
Valores válidos: [0, 1, 9]
Campo 14 - Preenchimento: informar neste campo o valor do desconto discriminado no documento fiscal.
Campo 15 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao documento fiscal.
Campo 16 – Preenchimento: informar o valor total do PIS/Pasep (débito ou crédito) referente ao documento fiscal.
Validação: a soma dos valores do campo VL_PIS dos registros filhos A170 deve ser igual ao valor informado neste campo.
Campo 17 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao documento fiscal.
Campo 18 – Preenchimento: informar o valor total da Cofins (débito ou crédito) referente ao documento fiscal.
Validação: a soma dos valores do campo VL_COFINS dos registros filhos A170 deve ser igual ao valor informado neste campo.
Campo 19 - Preenchimento: informar o valor do PIS/Pasep retido na fonte correspondente aos serviços constantes no documento fiscal. A informação constante do documento não será utilizada na apuração das contribuições (vide registro F600), sendo de natureza meramente informativa.
Campo 20 - Preenchimento: informar o valor da Cofins retida na fonte correspondente aos serviços constantes no documento fiscal. A informação constante do documento não será utilizada na apuração das contribuições (vide registro F600), sendo de natureza meramente informativa.
Campo 21 - Preenchimento:  informar o valor do ISS referente aos serviços constantes no documento fiscal.
<!-- End Registro A100 -->
<!-- Start Registro A110 -->
Registro A110: Complemento do Documento - Informação Complementar da NF
Este registro tem por objetivo identificar os dados contidos no campo Informações Complementares da Nota Fiscal, que sejam de interesse do Fisco ou conforme disponha a legislação, e que estejam explicitamente citadas no documento Fiscal, tais como: forma de pagamento, local da prestação/execução do serviço, operação realizada com suspensão das contribuições sociais, etc.
Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo no campo COD_INF.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "A110" | C | 004* | - | S |
| 02 | COD_INF | Código da informação complementar do documento fiscal (Campo 02 do Registro 0450) | C | 006 | - | S |
| 03 | TXT_COMPL | Informação Complementar do Documento Fiscal | C | - | - | N |

Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [A110]
Campo 02 - Validação: o valor informado no campo deve existir no registro 0450 - Tabela de informação complementar.
<!-- End Registro A110 -->
<!-- Start Registro A111 -->
Registro A111: Processo Referenciado
Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), exclusões na base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos na escrituração fiscal digital do PIS/Pasep e da Cofins.
Uma vez procedida à escrituração do Registro “A111”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "A111" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 015 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 - Outros. | C | 001* | - | S |

Observações:
1. A apuração da Contribuição para o PIS/Pasep e da Cofins mediante a escrituração dos valores componentes da base de cálculo mensal, da alíquota da contribuição ou de tratamento tributário (CST) diversos dos definidos pela legislação tributária, tendo por lastro e fundamento uma decisão judicial, só devem ser considerados na apuração e escrituração das referidas contribuições, caso a decisão judicial correspondente esteja com trânsito em julgado.
2. A apuração da Contribuição para o PIS/Pasep e da Cofins a recolher em cada período, demonstrada nos registros M200 (PIS/Pasep) e M600 (Cofins) deve corresponder e guardar uniformidade com os valores a serem declarados mensalmente na DCTF, segundo as normas disciplinadoras estabelecidas na Instrução Normativa RFB nº 1.599/2015.
3. Caso a pessoa jurídica seja titular ou beneficiária de decisão judicial que autoriza a suspensão da exigibilidade de parte do valor das contribuições, ou de seu valor integral, porém a decisão judicial não se encontra com o transito em julgado, deve a pessoa jurídica proceder à apuração das contribuições conforme a legislação aplicável, inclusive considerando a parcela que esteja com exigibilidade suspensa e, no Registro “1010 – Processo Referenciado – Ação Judicial”, fazendo constar no Campo 06 (DESC_DEC_JUD) deste registro a parcela das contribuições com exigibilidade suspensa, a qual deve ser igualmente destacada e informada em DCTF. A partir do período de apuração Janeiro/2020, a parcela das contribuições com exigibilidade suspensa também deverá ser detalhada no registro filho 1011 - Detalhamento das Contribuições com Exigibilidade Suspensa.
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
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [A111]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro A111 -->
<!-- Start Registro A120 -->
Registro A120: Informação Complementar - Operações de Importação
Este registro tem por objetivo informar detalhes das operações de importação de serviços com direito a crédito, referentes a documento fiscal escriturado em A100 e que no registro filho A170 conste CST_PIS ou CST_COFINS gerador de crédito (CST 50 a 56), bem como conste ser o registro A170 originário de operação de importação (campo IND_ORIG_CRED = 1.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "A120” | C | 004 | - | S |
| 02 | VL_TOT_SERV | Valor total do serviço, prestado por pessoa física ou jurídica domiciliada no exterior. | N | - | 02 | S |
| 03 | VL_BC_PIS | Valor da base de cálculo da Operação – PIS/PASEP – Importação | N | - | 02 | S |
| 04 | VL_PIS_IMP | Valor pago/recolhido de PIS/PASEP – Importação | N | - | 02 | N |
| 05 | DT_PAG_PIS | Data de pagamento do PIS/PASEP – Importação | N | 008* | - | N |
| 06 | VL_BC_COFINS | Valor da base de cálculo da Operação – COFINS – Importação | N | - | 02 | S |
| 07 | VL_COFINS_IMP | Valor pago/recolhido de COFINS – Importação | N | - | 02 | N |
| 08 | DT_PAG_COFINS | Data de pagamento do COFINS – Importação | N | 008* | - | N |
| 09 | LOC_EXE_SERV | Local da execução do serviço: 0 – Executado no País; 1 – Executado no Exterior, cujo resultado se verifique no País. | C | 001* | - | S |

Observações: Deve ser informado neste registro os pagamentos de PIS/Pasep-Importação e de Cofins-Importação, referente ao serviço contratado com direito a crédito, uma vez que de acordo com a legislação em referência, o direito à apuração de crédito aplica-se apenas em relação às contribuições efetivamente pagas na importação de bens e serviços (art. 15 da Lei nº 10.865, de 2004).
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [A120]
Campos 03, 04 e 05 - Preenchimento: Informar o valor da base de cálculo, o valor recolhido e a data de pagamento do PIS/Pasep – Importação, respectivamente, decorrente do pagamento, crédito, entrega, emprego ou da remessa de valores a residentes ou domiciliados no exterior como contraprestação por serviço prestado. No caso de haver recolhimentos (PIS/Pasep – Importação) em mais de uma data, deve a pessoa jurídica proceder à escrituração de um registro para cada data de pagamento.
De acordo com a legislação, o direito ao crédito de PIS/Pasep aplica-se em relação às contribuições efetivamente pagas na importação de bens e serviços.
Campos 06, 07 e 08 - Preenchimento: Informar o valor da base de cálculo, o valor recolhido e a data de pagamento da Cofins – Importação, respectivamente, decorrente do pagamento, crédito, entrega, emprego ou da remessa de valores a residentes ou domiciliados no exterior como contraprestação por serviço prestado. No caso de haver recolhimentos (Cofins – Importação) em mais de uma data, deve a pessoa jurídica proceder à escrituração de um registro para cada data de pagamento.
De acordo com a legislação, o direito ao crédito de Cofins aplica-se em relação às contribuições efetivamente pagas na importação de bens e serviços.
<!-- End Registro A120 -->
<!-- Start Registro A170 -->
Registro A170: Complemento do Documento - Itens do Documento
Registro obrigatório para discriminar os itens da nota fiscal de serviço emitida pela pessoa jurídica ou por terceiros.
No Registro A170 serão informados os itens constantes nas Notas Fiscais de Serviços ou documento internacional equivalente (no caso de importações), especificando o tratamento tributável (CST) aplicável a cada item.
Em relação aos itens com CST representativos de receitas, os valores dos Campos de bases de cálculo, VL_BC_PIS (Campo 10) e VL_BC_COFINS (Campo 14) serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210) e da Cofins (M610), no Campo “VL_BC_CONT”.
Em relação aos itens com CST representativos de operações geradoras de créditos, os valores dos Campos de bases de cálculo, VL_BC_PIS (Campo 10) e VL_BC_COFINS (Campo 14) serão recuperados no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105), no campo “VL_BC_PIS_TOT” e do crédito da Cofins (M505), no Campo “VL_BC_COFINS_TOT”.
Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo no campo NUM_ITEM.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "A170" | C | 004* | - | S |
| 02 | NUM_ITEM | Número seqüencial do item no documento fiscal | N | 004 | - | S |
| 03 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | S |
| 04 | DESCR_COMPL | Descrição complementar do item como adotado no documento fiscal | C | - | - | N |
| 05 | VL_ITEM | Valor total do item (mercadorias ou serviços) | N | - | 02 | S |
| 06 | VL_DESC | Valor do desconto comercial  / exclusão da base de cálculo do PIS/PASEP e da COFINS | N | - | 02 | N |
| 07 | NAT_BC_CRED | Código da base de cálculo do crédito, conforme a Tabela indicada no item 4.3.7, caso seja informado código representativo de crédito no Campo 09 (CST_PIS) ou no Campo 13 (CST_COFINS). | C | 002* | - | N |
| 08 | IND_ORIG_CRED | Indicador da origem do crédito: 0 – Operação no Mercado Interno 1 – Operação de Importação | C | 001* | - | N |
| 09 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP – Tabela 4.3.3. | N | 002* | - | S |
| 10 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP. | N | - | 02 | N |
| 11 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | - | 02 | N |
| 12 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 13 | CST_COFINS | Código da Situação Tributária referente ao COFINS – Tabela 4.3.4. | N | 002* | - | S |
| 14 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N |   | 02 | N |
| 15 | ALIQ_COFINS | Alíquota do COFINS (em percentual) | N | 006 | 02 | N |
| 16 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 17 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 18 | COD_CCUS | Código do centro de custos | C | 255 | - | N |

Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [A170]
Campo 02 - Validação: deve ser maior que “0” (zero) e sequencial.
Campo 03 - Preenchimento: o valor informado neste campo deve existir no registro 0200, ressaltando-se que os códigos informados devem ser os definidos pela pessoa jurídica titular da escrituração.
Campo 04 - Preenchimento: neste campo pode ser informada a descrição complementar do item, conforme adotado no documento fiscal.
Campo 05 - Preenchimento: informar o valor total do item (serviços ou mercadorias) a que se refere o registro.
Campo 06 - Preenchimento: informar o valor do desconto comercial e/ou dos valores a excluir da base de cálculo da contribuição ou do crédito, conforme o caso.
Campo 07 - Preenchimento: caso seja informado código representativo de crédito no Campo 09 (CST_PIS) ou no Campo 13 (CST_COFINS) do Registro A170, informar neste campo o código da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Atenção: O campo somente deve ser preenchido nos casos de serviços contratados pelo estabelecimento.
Campo 08 - Valores válidos: [0, 1]
Preenchimento: informar neste campo o código indicador da origem do crédito, se referente à operação no mercado interno (código “0”) ou se referente a operação de importação (código “1”). No caso de se referir à operação de importação, deve ser escriturado o registro A120.
Atenção: O campo somente deve ser preenchido nos casos de serviços contratados pelo estabelecimento.
Campo 09 - Preenchimento: informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 10 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item do documento fiscal, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “VL_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 11 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 12 – Preenchimento: informar o valor do PIS/Pasep (contribuição ou crédito) referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição e/ou do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500 e VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (VL_BC_PIS) multiplicado pela alíquota aplicável ao item (ALIQ_PIS). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,65 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 13 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 14 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item do documento fiscal, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de Cofins (M505, campo “VL_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 15 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 16 – Preenchimento: informar o valor da Cofins (contribuição ou crédito) referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição e/ou do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500 e VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (VL_BC_COFINS) multiplicado pela alíquota aplicável ao item (ALIQ_COFINS). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,60 , então o Campo “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 17 - Preenchimento: informar o Código da Conta Analítica. Exemplos: custo de serviços prestados por pessoa jurídica, receita da prestação de serviços, receitas da atividade, serviços contratados, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 18 - Preenchimento: Nos registros correspondentes a operações com direito a crédito, informar neste campo o Código do Centro de Custo relacionado à operação, se existir.
<!-- End Registro A170 -->
<!-- Start Registro A990 -->
Registro A990: Encerramento do Bloco A
Este registro destina-se a identificar o encerramento do bloco A e informar a quantidade de linhas (registros) existentes no bloco.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "A990" | C | 004* | - | S |
| 02 | QTD_LIN_A | Quantidade total de linhas do Bloco A | N | - | - | S |

Observações: Registro obrigatório, no caso do arquivo conter o Registro A001
Nível hierárquico - 1
Ocorrência – um por arquivo
Validação do Registro: registro único e obrigatório para todos os informantes da EFD-Contribuições.
Campo 01 - Valor Válido: [A990]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros deabertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco A é igual ao valor informado no campo QTD_LIN_A
(registro C990).
<!-- End Registro A990 -->