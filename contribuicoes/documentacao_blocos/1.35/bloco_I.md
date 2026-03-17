# Bloco I - Versão 1.35

BLOCO I: Operações das Instituições Financeiras, Seguradoras, Entidades de Previdencia Privada, Operadoras de Planos de Assistência à Saúde e Demais Pessoas Jurídicas Referidas nos §§ 6º, 8º e 9º do art. 3º da lei nº 9.718/98.
Neste bloco serão informadas pelas pessoas jurídicas referidas, as operações geradoras da contribuição para o PIS/Pasep e da Cofins, de conformidade com a legislação específica a elas aplicáveis e com a Instrução Normativa RFB nº 1.285, de 2012.
A escrituração do Bloco I só é de natureza obrigatória em relação aos fatos geradores a ocorrer a partir de 01 de janeiro de 2014, conforme disposto na IN RFB nº 1.387, de 2013.
Em relação ao primeiro mês de obrigatoriedade, correspondente ao período de apuração de janeiro de 2014, a transmitir até o dia 17/03/2014, a pessoa jurídica poderá utilizar tanto a versão 2.05 como a versão 2.06 do PVA, conforme quadro abaixo. A escrituração utilizando a versão 2.05 referente ao mês de janeiro de 2014, dispensa a escrituração analítica das receitas e deduções, no registro I300:

| VERSÃO PVA | DISPONIBILIZAÇÃO | BLOCO I - REGISTROS A ESCRITURAR |
| --- | --- | --- |
| 2.05 | Agosto / 2013 | Registro I100 |
| 2.05 | Agosto / 2013 | Registro I200 |
| 2.06 | Fevereiro / 2014 | Registro I100 |
| 2.06 | Fevereiro / 2014 | Registro I200 |
| 2.06 | Fevereiro / 2014 | Registro I300 (a partir de 01.01.2014) |

Para a adequada escrituração das operações no Bloco I, e corresponde validação da escrituração pelo PVA, deve na escrituração do Registro “0000 – Abertura do Arquivo Digital e Identificação da Pessoa Jurídica” ser informado no Campo 14 (IND_ATIV), o indicador “3 – Pessoas jurídicas referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998”.
Uma vez informado o indicador "3" no campo acima referido, o PVA irá desabilitar os registros dos Blocos A, C, D e F, específicos para a escrituração das receitas pelas PJ em geral, e habilitar tão somente o Bloco I, para o registro de todas as operações geradoras de receitas, tributáveis ou não.
<!-- Start Registro I001 -->
Registro I001: Abertura do Bloco I

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I001" | C | 004* | - |
| 02 | IND_MOV | Indicador de movimento: 0 - Bloco com dados informados 1 - Bloco sem dados informados | C | 001 | - |

Observações: Registro de escrituração obrigatória.
Nível hierárquico - 1
Ocorrência – um por arquivo
Campo 01 - Valor Válido: [I001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro I001 -->
<!-- Start Registro I010 -->
Registro I010: Identificação da Pessoa Juridica/Estabelecimento
Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica a que se referem as operações informadas no Registro filho I100. Só devem ser escriturados no Registro I010 os estabelecimentos da pessoa jurídica que efetivamente tenham realizado operações passíveis de escrituração neste bloco.
No caso das operações a serem escrituradas estarem contabilizadas ou compostas de forma centralizada, pelo estabelecimento matriz da pessoa jurídica, deve ser informado neste registro o mesmo CNPJ constante no registro “0000”.
No caso de escrituração descentralizada, por estabelecimento, deve ser escriturado 01 (um) registro “I010” para cada estabelecimento que tenha realizado operações no período a que se refere a escrituração, identificando o mesmo no campo 02 deste registro. O estabelecimento que não realizou operações passíveis de registro no bloco I, no período da escrituração, não deve ser identificado no Registro I010.

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “I010” | C | 004* | - |
| 02 | CNPJ | Número de inscrição da pessoa jurídica no CNPJ. | N | 014* | - |
| 03 | IND_ATIV | Indicador de operações realizadas no período: 01 – Exclusivamente operações de Instituições Financeiras e Assemelhadas 02 – Exclusivamente operações de Seguros Privados 03 – Exclusivamente operações de Previdência Complementar 04 – Exclusivamente operações de Capitalização 05 – Exclusivamente operações de Planos de Assistência à Saúde 06 – Realizou operações referentes a mais de um dos indicadores acima | N | 002* | - |
| 04 | INFO_COMPL | Informação Complementar | C | - | - |

Observações: Registro obrigatório (se IND_MOV igual a 0, no Registro I001)
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Campo 01 - Valor Válido: [I010];
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações passíveis de escrituração neste grupo de registros.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deve está cadastrado no Registro 0140.
Campo 03 - Preenchimento: Informar neste campo o indicador do tipo ou natureza da operação.
A tabela abaixo relaciona a correlação entre o indicador de operações a ser informado no campo “IND_ATIV” e os correspondentes códigos de receitas ou deduções, objeto de validação nos registros “I200” e “I300”.
(*) O indicador “01 – Exclusivamente operações de instituições financeiras e Assemelhadas” correspondia e validava os códigos de receitas (Tabela 7.1.1) do Grupo 700, para os fatos geradores até 31.12.2013 (de transmissão opcional). Para os fatos geradores a partir de 01.01.2014, os códigos de receitas passam a ser codificados no Grupo 100, tanto para as receitas (Tabela 7.1.1) como para as deduções (Tabela 7.1.2).
Valores Válidos: [01, 02, 03, 04, 05, 06]
Campo 04 - Preenchimento: Escriturar neste campo informações complementares referente aos campos 02 ou 03, a critério e interesse da pessoa jurídica.
<!-- End Registro I010 -->
<!-- Start Registro I100 -->
Registro I100: Consolidação das Operações do Período
Registro específico para escrituração pelas pessoas jurídicas referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, sujeitas ao regime cumulativo de apuração das contribuições, conforme definido nas Leis nº 10.637/2002 (PIS/Pasep) e nº 10.833/2003 (Cofins).
Deve também ser objeto de escrituração as operações das agências de fomento referidas no art. 1º da MP nº 2.192-70, de 2001, tendo em vista o disposto no art. 70 da Lei nº 12.715, de 2012.
Deverá ser preenchido no mínimo 01 (um) registro para cada receita e CST correspondente.
O detalhamento das receitas e deduções/exclusões deve ser objeto de demonstração no registro filho “I200”, com base nos códigos e agrupamentos de receitas e deduções/exclusões especificados nas Tabelas 7.1.1 e 7.1.2, respectivamente.
Os valores informados nos campos 06 e 09 (Bases de cálculo) deste registro serão recuperados no campo 04 dos registros M210 (PIS/Pasep) e M610 (Cofins), respectivamente.
Chaves do registro: CST + ALIQ_PIS + ALIQ_COFINS + INFO_COMPL

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I100" | C | 004* | - |
| 02 | VL_REC | Valor Total do Faturamento/Receita Bruta no Período | N | - | 02 |
| 03 | CST_PIS_COFINS | Código de Situação Tributária referente à Receita informada no Campo 02 (Tabelas 4.3.3 e 4.3.4) | N | 002* | - |
| 04 | VL_TOT_DED_GER | Valor Total das Deduções e Exclusões de Caráter Geral | N | - | 02 |
| 05 | VL_TOT_DED_ESP | Valor Total das Deduções e Exclusões de Caráter Específico | N | - | 02 |
| 06 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 02 |
| 08 | VL_PIS | Valor do PIS/PASEP | N | - | 02 |
| 09 | VL_BC_COFINS | Valor da base de cálculo da Cofins | N | - | 02 |
| 10 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 02 |
| 11 | VL_COFINS | Valor da COFINS | N | - | 02 |
| 12 | INFO_COMPL | Informação Complementar dos dados informados no registro | C | - | - |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [I100]
Campo 02 – Preenchimento: Informar neste campo o valor total do faturamento, ou seja, o valor da receita bruta da pessoa jurídica no período, correspondente ao CST informado no Campo 03.
Atenção: O valor informado neste campo deve ser objeto de detalhamento, em registro(s) filho I200, conforme os códigos de detalhamento relacionados na Tabela “7.1.1 – Composição das Receitas - Pessoas Jurídicas Referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998”.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP e a Cofins (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 04 - Preenchimento: informar o valor das deduções e exclusões de caráter geral previstas na legislação de regência, conforme definidas na Instrução Normativa RFB nº 1.285, de 2012.
Atenção: O valor informado neste campo deve ser objeto de detalhamento, em registro(s) filho I200, conforme os códigos de detalhamento relacionados na Tabela “7.1.2 – Composição das Deduções e Exclusões - Pessoas Jurídicas Referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998”.
Campo 05 - Preenchimento: informar o valor das deduções e exclusões de caráter específicos previstas na legislação de regência, conforme definidas na Instrução Normativa RFB nº 1.285, de 2012.
Atenção: O valor informado neste campo deve ser objeto de detalhamento, em registro(s) filho I200, conforme os códigos de detalhamento relacionados na Tabela “7.1.2 – Composição das Deduções e Exclusões - Pessoas Jurídicas Referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998”.
Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente a receita informada no registro, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 08 – Preenchimento:  informar o valor do PIS/Pasep referente às operações consolidadas neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 06) multiplicado pela alíquota aplicável ao item (campo 07). O resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 06 (VL_BC_PIS) = 1.000.000,00 e o Campo 07 (ALIQ_PIS) = 0,6500, então o Campo 08 (VL_PIS) será igual a: 1.000.000,00 x 0,65 / 100 = 6.500,00.
Campo 09 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente a receita informada no registro, para fins de apuração da contribuição social, conforme o caso.
Atenção: No caso das instituições financeiras, o valor do campo de base de cálculo da Cofins pode ser diferente do valor da base de cálculo do PIS/Pasep, em decorrência de deduções específicas da Cofins, como a disposta na Lei nº 9.718/98, art. 3º, § 10, referente ao valor devido à instituição financeira em cada período de apuração, como remuneração pelos serviços de arrecadação de receitas federais, código “D0110” da Tabela 7.1.2 do Bloco I.
No registro analítico I200, deve a instituição financeira informar o código “D0110010 - Valor devido em cada período de apuração como remuneração pelos serviços de arrecadação de receitas federais” da Tabela 7.1.4.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 10 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, de 3% ou 4%, conforme o caso. Na edição da escrituração no próprio PVA, o programa recupera a alíquota de 4%, uma vez ser esta a alíquota aplicável em praticamente todas as operações tributadas pelo Bloco I. Todavia, o PVA valida a alíquota de 3%, determinada receita seja tributada a está alíquota. Para tanto, basta proceder a alteração da alíquota da Cofins, no campo correspondente.
Atenção: Para a validação da alíquota de 4% ou de 3%, deve a pessoa jurídica informar o CST “01 – Operação Tributável com Alíquota Básica”, no Campo 03.
Campo 11 – Preenchimento: informar o valor da Cofins referente às operações consolidadas neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 09) multiplicado pela alíquota aplicável ao item (campo 10). O resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 09 (VL_BC_COFINS) = 1.000.000,00 e o Campo 10 (ALIQ_COFINS) = 4,0000, então o Campo 11 (VL_COFINS) será igual a: 1.000.000,00 x 4,0000 / 100 = 40.000,00.
Campo 12 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
<!-- End Registro I100 -->
<!-- Start Registro I199 -->
Registro I199: Processo Referenciado
1. Registro filho de “I100 – Consolidação das Operações do período”, específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições apuradas no Registro I100.
2. Uma vez procedida à escrituração do Registro “I199”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições.

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I199" | C | 004* | - |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - |

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
Ocorrência - 1:N
Campo 01 - Valor Válido: [I199]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro I199 -->
<!-- Start Registro I200 -->
Registro I200: Composição das Receitas, Deduções e/ou Exclusões do Período
Registro específico para a identificação e o detalhamento dos valores informados nos campos 02, 04 e 05 do Registro I100.
Deve ser preenchido um registro para cada tipo de receita e/ou deduções e exclusões, codificadas nas Tabelas 7.1.1 e 7.1.2, conforme o caso.
Chaves do registro: NUM_CAMPO + COD_DET + COD_CTA + INFO_COMPL

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I200" | C | 004* | - |
| 02 | NUM_CAMPO | Informar o número do campo do registro “I100” (Campos 02, 04 ou 05), objeto de informação neste registro. | C | 002* | - |
| 03 | COD_DET | Código do tipo de detalhamento, conforme Tabelas 7.1.1 e/ou 7.1.2 | C | 005* | - |
| 04 | DET_VALOR | Valor detalhado referente ao campo 03 (COD_DET) deste registro | N | - | 02 |
| 05 | COD_CTA | Código da conta contábil referente ao valor informado no campo 04 (DET_VALOR) | C | 255 | - |
| 06 | INFO_COMPL | Informação Complementar dos dados informados no registro | C | - | - |

Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [I200]
Campo 02 – Preenchimento: Informar o campo do registro pai “I100”, objeto de demonstração de sua composição neste registro.
Campo 03 - Preenchimento: Informar o código de detalhamento correspondente a:
Tabela “7.1.1 – Composição das Receitas”, no caso de informações referentes ao campo 02 do registro pai;
Tabela “7.1.2 – Composição das Deduções e Exclusões”, no caso de informações referentes aos campos 04 ou 05 do registro pai.
OBS: As diversas tabelas sintéticas (registro I200) e analíticas (registro I300) utilizadas para a escrituração do Bloco I, estão disponibilizadas no portal do SPED, no sitio da Receita Federal na internet, no endereço http://sped.rfb.gov.br>.
Campo 04 – Preenchimento: Informar neste campo o valor da receita ou da dedução/exclusão, conforme o caso, referente ao código de detalhamento constante no Campo 03.
Atenção: O somatório dos valores informados no Registro I200 deve corresponder aos valores totais de receitas, deduções gerais ou deduções específicas, escriturados nos campos 02, 04 e 05, do registro I100, respectivamente.
Campo 05 - Preenchimento: informar o código da conta contábil correspondente aos valores informados neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 06 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
<!-- End Registro I200 -->
<!-- Start Registro I299 -->
Registro I299: Processo Referenciado
1. Registro filho de “I200 – Composição das Receitas e Deduções do período”, específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das operações informadas no Registro I200.
2. Uma vez procedida à escrituração do Registro “I299”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições.

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I299" | C | 004* | - |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - |

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
Nível hierárquico - 5
Ocorrência - 1:N
Campo 01 - Valor Válido: [I299]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro I299 -->
<!-- Start Registro I300 -->
Registro I300: Complemento das Operações – Detalhamento das Receitas, Deduções e/ou Exclusões Do Período
Esclarecimentos Importantes:
1. O registro analítico I300, de detalhamento das receitas e das deduções informadas de forma sintética no registro I200, só será objeto de escrituração a partir do período de apuração Janeiro de 2014, com a disponibilidade da versão 2.06 do PVA da EFD-Contribuições. Na versão 2.05, passível de escrituração em caráter facultativo do Bloco I, em relação aos fatos geradores a partir de agosto de 2013, a pessoa jurídica só procederá à escrituração dos registros I100 e I200. O PVA da versão 2.05 não valida ou permite a edição do registro I300.
2. A versão 2.05, disponível desde agosto de 2013, poderá ser utilizada regularmente para a escrituração referente ao mês de janeiro de 2014, mesmo que a referida escrituração, gerada nesta versão, não contemple os registros analíticos de receitas e deduções – I300. A escrituração referente ao mês de janeiro de 2014, validada e transmitida pela versão 2.05, não enseja qualquer irregularidade ou inconsistência, por ter sido prestada sem a escrituração analítica das operações do registro I300.
3. O valor da receita ou dedução, conforme o caso, informado no Campo 04 do registro pai I200, deve corresponder ao somatório dos valores informados no Campo 04 dos registros filhos I300, correspondentes. Ou seja, a escrituração dos valores informados no registro I300 vem a ser, tão somente, a demonstração num nível mais analítico, mais detalhado (conforme codificação constante nas diversas tabelas analíticas 7.1.3 e/ou 7.1.4), dos valores informados de forma sintética no registro I200.

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I300" | C | 004* | - |
| 02 | COD_COMP | Código das Tabelas 7.1.3 (Receitas – Visão Analítica/Referenciada) e/ou 7.1.4 (Deduções e exclusões – Visão Analítica/Referenciada), objeto de complemento neste registro | C | 060 | - |
| 03 | DET_VALOR | Valor da receita, dedução ou exclusão, objeto de complemento/detalhamento neste registro, conforme código informado no campo 02 (especificados nas tabelas analíticas 7.1.3 e 7.1.4) ou no campo 04 (código da conta contábil) | N | - | 02 |
| 04 | COD_CTA | Código da conta contábil referente ao valor informado no campo 03 | C | 255 | - |
| 05 | INFO_COMPL | Informação Complementar dos dados informados no registro | C | - | - |

Observações:
Registro específico para o detalhamento do valor da receita, dedução ou exclusão, informada de forma consolidada no Registro Pai I200, de preenchimento a partir do período de apuração Janeiro de 2014.
Chaves do registro: COD_COMP + COD_CTA + INFO_COMPL
Nível hierárquico - 5
Ocorrência – 1:N
Campo 01 - Valor Válido: [I300]
Campo 02 - Preenchimento: Informar o código de detalhamento correspondente a:
Tabelas Analíticas 7.1.3 (Receitas – Visão Analítica/Referenciada), no caso de informações referentes a receitas, no registro pai I200;
Tabela 7.1.4 (Deduções e Exclusões – Visão Analítica/Referenciada), no caso de informações referentes a deduções ou exclusões, no registro pai I200.
OBS: As diversas tabelas sintéticas (registro I200) e analíticas (registro I300) utilizadas para a escrituração do Bloco I, estão disponibilizadas no portal do SPED, no sitio da Receita Federal na internet, no endereço http://sped.rfb.gov.br>.
Campo 03 – Preenchimento: Informar neste campo o valor da receita ou da dedução/exclusão, conforme o caso, referente ao código de detalhamento constante no Campo 02.
Campo 04 - Preenchimento: informar o código da conta contábil correspondente aos valores informados neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 05 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
<!-- End Registro I300 -->
<!-- Start Registro I399 -->
Registro I399: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário, base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições.
2. Uma vez procedida à escrituração do Registro “I399”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições.

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I399" | C | 004* | - |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - |

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
Nível hierárquico - 6
Ocorrência - 1:N
Campo 01 - Valor Válido: [I399]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro I399 -->
<!-- Start Registro I990 -->
Registro I990: Encerramento do Bloco I

| Nº | Campo | Descrição | Tipo | Tam | Dec |
| --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "I990" | C | 004* | - |
| 02 | QTD_LIN_I | Quantidade total de linhas do Bloco I | N | - | - |

Observações: Registro obrigatório
Nível hierárquico - 1
Ocorrência - um (por arquivo)
TABELAS PARA A ESCRITURAÇÃO DO BLOCO “I”:
7.1.1 – Composição das Receitas - Pessoas Jurídicas Referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998: Tabela externa a ser especificada pela RFB e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>>;
7.1.2 – Composição das Deduções e Exclusões - Pessoas Jurídicas Referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998: Tabela externa a ser especificada pela RFB e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>>;
7.1.3 – Receitas – Visão Analítica/Referenciada: Tabelas externas a serem especificadas pela RFB e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>>;
7.1.4 – Deduções e Exclusões – Visão Analítica/Referenciada - Pessoas Jurídicas Referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998: Tabelas externas a serem especificadas pela RFB e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>>.
<!-- End Registro I990 -->