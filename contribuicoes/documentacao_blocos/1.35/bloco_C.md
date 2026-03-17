# Bloco C - Versão 1.35

BLOCO C: Documentos Fiscais – I - Mercadorias (ICMS/IPI)
<!-- Start Registro C001 -->
Registro C001: Abertura do Bloco C

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C001" | C | 004* | - | S |
| 02 | IND_MOV | Indicador de movimento: 0 - Bloco com dados informados; 1 - Bloco sem dados informados | C | 001* | - | S |

Observações:
Nível hierárquico - 1
Ocorrência – um por arquivo
Campo 01 - Valor Válido: [C001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro C001 -->
<!-- Start Registro C010 -->
Registro C010: Identificação do Estabelecimento
Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica a que se referem as operações e documentos fiscais informados neste bloco. Só devem ser escriturados no Registro C010 os estabelecimentos que efetivamente tenham realizado aquisição, venda ou devolução de mercadorias, bens e produtos, mediante emissão de documento fiscal definido pela legislação do ICMS e do IPI, que devam ser escrituradas no Bloco C.
O estabelecimento que não realizou operações passíveis de registro nesse bloco, no período da escrituração, não deve ser identificado no Registro C010.
Para cada estabelecimento cadastrado em “C010”, deve ser informado nos registros de nível inferior (Registros Filho) as operações próprias de prestação ou de contratação de serviços, mediante emissão de documento fiscal, no mercado interno ou externo.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “C010”. | C | 004* | - | S |
| 02 | CNPJ | Número de inscrição do estabelecimento no CNPJ. | N | 014* | - | S |
| 03 | IND_ESCRI | Indicador da apuração das contribuições e créditos, na escrituração das operações por NF-e e ECF, no período: 1 – Apuração com base nos registros de consolidação das operações por NF-e (C180 e C190) e por ECF (C490); 2 – Apuração com base no registro individualizado de NF-e (C100 e C170) e de ECF (C400) | C | 001* | - | N |

Observações: Registro de preenchimento obrigatório, se IND_MOV igual a “0” no Registro C001
Nível hierárquico - 2
Ocorrência – vários por arquivo
Campo 01 - Valor Válido: [C010];
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações passíveis de escrituração neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deve está cadastrado no Registro 0140.
Campo 03 - Preenchimento: este campo deve ser preenchido se no arquivo de registros da escrituração importado pelo PVA, constar em relação às operações documentadas por Nota Fiscal Eletrônica – NF-e, código 55, tanto registros individualizados por documento fiscal (C100) como registros consolidados dos documentos fiscais (C180 e/ou C190).
Deve igualmente ser preenchido se no arquivo da escrituração constar, em relação às operações emitidas por equipamento Emissor de Cupom Fiscal – ECF, tanto registros individualizados por ECF (C400) como registros consolidados de documentos fiscais emitidos por ECF (C490).
<!-- End Registro C010 -->
<!-- Start Registro C100 -->
Registro C100: Documento - Nota Fiscal (Código 01), Nota Fiscal Avulsa (Código 1B), Nota Fiscal de Produtor (Código 04), NF-e (Código 55) e NFC-e (Código 65).
Registro com estrutura, campos e conteúdo definidos e constantes no Leiaute da Escrituração Fiscal Digital – EFD (ICMS e IPI), instituído pelo Ato COTEPE/ICMS nº 9, de 12 de abril de 2008, disponível no portal de serviços (SPED) da página da Secretaria da Receita Federal do Brasil na Internet, no endereço <sped.rfb.gov.br>.
Este registro deve ser gerado para cada documento fiscal código 01, 1B, 04, 55 e 65 (NFC-e), registrando a entrada ou saída de produtos ou outras situações que envolvam a emissão dos documentos fiscais mencionados, representativos de receitas auferidas, tributadas ou não pelo PIS/Pasep ou pela Cofins, bem como de operações de aquisições e/ou devoluções com direito a crédito da não cumulatividade.
Não devem ser informados documentos fiscais que não se refiram a operações geradoras de receitas ou de créditos de PIS/Pasep e de Cofins.
Para cada registro C100, obrigatoriamente deve ser apresentado, pelo menos, um registro C170, exceto em relação aos documentos fiscais referentes à nota fiscal cancelada (código “02” ou “03”), Nota Fiscal Eletrônica (NF-e) denegada (código “04”) ou numeração inutilizada (código “05”), os quais não devem ser escriturados os registros filhos de C100.
Não podem ser informados, para um mesmo documento fiscal, dois ou mais registros com a mesma combinação de valores dos campos formadores da chave do registro. A chave deste registro é:
• para documentos com campo “IND_EMIT” igual a “1” (um) – emissão por terceiros: campo IND_OPER, campo IND_EMIT, campo COD_PART, campo COD_MOD, campo COD_SIT, campo SER e campo NUM_DOC;
• para documentos com campo “IND_EMIT” igual “0” (zero) – emissão própria: campo IND_OPER, campo IND_EMIT, campo COD_MOD, campo COD_SIT, campo SER e campo NUM_DOC.
Em ambos os casos, para os fatos geradores ocorridos a partir de abril de 2021, fica incluído o campo CHV_NFE na chave do registro.
ATENÇÃO:
1. Na escrituração das receitas lastreadas por notas fiscais eletrônicas ao consumidor final (NFC-e), modelo 65, deve a pessoa jurídica apresentar somente os registros C100 e C175 (visão analítica, por CST). Na escrituração das NFC-e no registro C100, não precisam ser informados os campos COD_PART, VL_BC_ICMS_ST, VL_ICMS_ST, VL_IPI, VL_PIS, VL_COFINS, VL_PIS_ST e VL_COFINS_ST. Os demais campos seguirão a obrigatoriedade definida pelo registro.
2. Na escrituração das receitas de vendas por NF-e neste registro, para os fatos geradores ocorridos a partir de 1º de maio de 2015, referente às bebidas frias de que trata os art. 14 a 34 da Lei nº 13.097/2015, deve a pessoa jurídica observar as orientações constantes na Nota Técnica nº 005, de 07 de maio de 2015, publicada no Portal do Sped (área da EFD-Contribuições), no sitio da Secretaria da Receita Federal do Brasil.
3. As notas fiscais avulsas eletrônicas emitidas pelas UF (séries 890 a 899) serão recuperadas e visualizadas no PGE na aba “C100 - Notas Fiscais Eletrônicas”. A aba “C100 - Notas Fiscais Avulsas” é exclusiva para documentos em papel, modelo 1B.
OPERAÇÕES COM SUBSTITUIÇÃO TRIBUTÁRIA DO PIS/PASEP E DA COFINS - ORIENTAÇÕES DE ESCRITURAÇÃO PELA PESSOA JURÍDICA FABRICANTE:
1. Procedimento de escrituração da substituição tributária de cigarros e cigarrilhas:
Tributação definida em recolhimento único, tendo por alíquota aplicável a alíquota básica definida para o regime cumulativo (0,65% e 3%). Desta forma, a pessoa jurídica fabricante, responsável pelo recolhimento como contribuinte e como substituto tributário, poderá registrar as vendas correspondentes, considerando o CST 01 (Operação tributável com alíquota básica) ou CST 05 (Operação tributável por substituição tributária). Independente do CST informado, a Receita Federal identificará a natureza da operação, em função da NCM e CFOP informados nos registros representativos das correspondentes operações;
2. Procedimento de escrituração da substituição tributária de motocicletas e máquinas agrícolas - Art. 43 da MP nº 2.158-31/2001:
Tributação definida em recolhimentos separados (dois recolhimentos) por parte do fabricante, como contribuinte e como substituto tributário, tendo por alíquota aplicável a alíquota básica definida para o regime cumulativo. Desta forma, a pessoa jurídica fabricante, responsável pelos dois recolhimentos, como contribuinte e como substituto tributário, poderá registrar as vendas correspondentes, no registro C170 ou C180 (e registros filhos) utilizando registros diferentes para cada recolhimento:
- No caso de escrituração por documento fiscal (C100): deverá ser escriturado 01 (um) registro C170 específico para informar a tributação como contribuinte (CST 01) e 01 (um) registro C170 específico para informar a tributação do outro recolhimento, como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração do registro C170 representativo da ST, informar valor zero no campo 07 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição;
- No caso de escrituração consolidada das receitas (C180): deverá ser escriturado 01 (um) registro C181/C185 específico para informar a tributação como contribuinte (CST 01) e 01 (um) registro C181/C185 específico para informar a tributação do outro recolhimento, como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração dos registros representativos da ST, informar valor zero no campo 04 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição.
3. Procedimento de escrituração da substituição tributária da venda de produtos monofásicos à ZFM - Arts. 64 e 65 da Lei nº 11.196/2005:
Tributação definida em recolhimento único, tendo por alíquota monofásicas, relacionadas nas tabelas 4.3.10 e 4.3.11, conforme o produto. Nesse regime de tributação por ST, aplicável a esses produtos, a tributação da operação no fabricante, como contribuinte está tributada com alíquota zero (CST 06) e, na condição de substituto, tributada com CST 05. Desta forma, a pessoa jurídica fabricante, responsável pelo recolhimento como substituto tributário, poderá registrar as vendas correspondentes, no registro C170 ou C180 (e registros filhos) utilizando registros diferentes para cada situação:
- No caso de escrituração por documento fiscal (C100): deverá ser escriturado 01 (um) registro C170 específico para informar a tributação à alíquota zero como contribuinte (CST 06) e 01 (um) registro C170 específico para informar a tributação do recolhimento como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração do registro C170 representativo da ST, informar valor zero no campo 07 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição;
- No caso de escrituração consolidada das receitas (C180): deverá ser escriturado 01 (um) registro C181/C185 específico para informar a tributação à alíquota zero como contribuinte (CST 06) e 01 (um) registro C181/C185 específico para informar a tributação do recolhimento como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração dos registros representativos da ST, informar valor zero no campo 04 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição.
4. Procedimentos de escrituração na revenda de bens sujeitos à substituição tributária de PIS/COFINS:
Conforme disposto no Decreto nº 4.524, de 2002, art. 37, os comerciantes varejistas de cigarros, em decorrência da substituição a que estão sujeitos na forma do caput do art. 4º, para efeito da apuração da base de cálculo das contribuições, podem excluir da receita bruta o valor das vendas desse produto, desde que a substituição tenha sido efetuada na aquisição.
Dessa forma, ao relacionar as receitas decorrentes das revendas destes produtos sujeitos ao regime da substituição tributária, devem escriturar:
- No campo destinado à receita ou valor dos itens: registrar o valor da receita ou do item sendo revendido
- No campo CST PIS ou CST COFINS: informar o valor 05
- No campo de Base de Cálculo: informar o valor zero (0,00)
- No campo de Alíquota: 0,65 para o PIS e 3,00 para a COFINS
- No campo de Valor PIS ou Valor COFINS: informar o valor zero (0,00)
Um exemplo de como informar essa operação para os contribuintes do lucro presumido, que optam pela escrituração consolidada pode ser obtida no Manual de Escrituração da EFD-Contribuições - PJ do Lucro Presumido, disponível para download em http://sped.rfb.gov.br/arquivo/show/3016.
Ressalte-se que até a versão 2.05 do PVA o procedimento de gerar estes registros utilizando alíquota zero era decorrente da solução de TI adotada pelo PVA. A partir da versão 2.0.5 este procedimento foi ajustado de acordo com o comando normativo acima mencionado. Cabe informar que a utilização de alíquota zero no registro destas vendas no PVA versão 2.0.5 não gera um respectivo registro M400 ou M800, como ocorria no PVA 2.0.4a e anteriores. A possibilidade de utilização da alíquota zero nestes casos será descontinuada nas próximas versões do PVA (2.0.6).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C100" | C | 004 | - | S |
| 02 | IND_OPER | Indicador do tipo de operação: 0- Entrada; 1- Saída | C | 001* | - | S |
| 03 | IND_EMIT | Indicador do emitente do documento fiscal: 0- Emissão própria; 1- Terceiros | C | 001* | - | S |
| 04 | COD_PART | Código do participante (campo 02 do Registro 0150): - do emitente do documento ou do remetente das mercadorias, no caso de entradas; - do adquirente, no caso de saídas | C | 060 | - | S |
| 05 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 06 | COD_SIT; | Código da situação do documento fiscal, conforme a Tabela 4.1.2 | N | 002* | - | S |
| 07 | SER | Série do documento fiscal | C | 003 | - | N |
| 08 | NUM_DOC | Número do documento fiscal | N | 009 | - | S |
| 09 | CHV_NFE | Chave da Nota Fiscal Eletrônica ou da NFC-e | N | 044* | - | N |
| 10 | DT_DOC | Data da emissão do documento fiscal | N | 008* | - | S |
| 11 | DT_E_S | Data da entrada ou da saída | N | 008* | - | N |
| 12 | VL_DOC | Valor total do documento fiscal | N | - | 02 | S |
| 13 | IND_PGTO | Indicador do tipo de pagamento: 0- À vista; 1- A prazo; 9- Sem pagamento. | C | 001* | - | S |
| 13 | IND_PGTO | Obs.: A partir de 01/07/2012 passará a ser: Indicador do tipo de pagamento: 0- À vista; 1- A prazo; 2 – Outros | C | 001* | - | S |
| 14 | VL_DESC | Valor total do desconto | N | - | 02 | N |
| 15 | VL_ABAT_NT | Abatimento não tributado e não comercial Ex. desconto ICMS nas remessas para ZFM. | N | - | 02 | N |
| 16 | VL_MERC | Valor total das mercadorias e serviços | N | - | 02 | N |
| 17 | IND_FRT | Indicador do tipo do frete: 0- Por conta de terceiros; 1- Por conta do emitente; 2- Por conta do destinatário; 9- Sem cobrança de frete. | C | 001* | - | S |
| 17 | IND_FRT | Obs.: A partir de 01/01/2012 passará a ser: Indicador do tipo do frete: 0- Por conta do emitente; 1- Por conta do destinatário/remetente; 2- Por conta de terceiros; 9- Sem cobrança de frete. | C | 001* | - | S |
| 17 | IND_FRT | Obs.: A partir de 01/10/2017 passará a ser: Indicador do tipo de frete/transporte: 0 - Frete por conta do remetente (CIF); 1 - Frete por conta do destinatário (FOB); 2 - Frete por conta de terceiros; 3 – Transporte próprio por conta do remetente; 4 – Transporte próprio por conta do destinatário; 9 - Sem ocorrência de transporte. | C | 001* | - | S |
| 18 | VL_FRT | Valor do frete indicado no documento fiscal | N | - | 02 | N |
| 19 | VL_SEG | Valor do seguro indicado no documento fiscal | N | - | 02 | N |
| 20 | VL_OUT_DA | Valor de outras despesas acessórias | N | - | 02 | N |
| 21 | VL_BC_ICMS | Valor da base de cálculo do ICMS | N | - | 02 | N |
| 22 | VL_ICMS | Valor do ICMS | N | - | 02 | N |
| 23 | VL_BC_ICMS_ST | Valor da base de cálculo do ICMS substituição tributária | N | - | 02 | N |
| 24 | VL_ICMS_ST | Valor do ICMS retido por substituição tributária | N | - | 02 | N |
| 25 | VL_IPI | Valor total do IPI | N | - | 02 | N |
| 26 | VL_PIS | Valor total do PIS | N | - | 02 | N |
| 27 | VL_COFINS | Valor total da COFINS | N | - | 02 | N |
| 28 | VL_PIS_ST | Valor total do PIS retido por substituição tributária | N | - | 02 | N |
| 29 | VL_COFINS_ST | Valor total da COFINS retido por substituição tributária | N | - | 02 | N |

Observações:
1. Tendo em vista que as operações de vendas e de aquisições e/ou devoluções, documentadas por Nota Fiscal Eletrônica – NF-e (código 55), serem escrituradas de forma consolidada nos registros C180 (vendas) e C190 (compras e/ou devoluções) da EFD-Contribuições, o registro C100 (e filhos) não é de preenchimento obrigatório na EFD-Contribuições em relação às referidas operações com NF-e (código 55) ;
2. Todavia, a EFD-Contribuições permite a escrituração alternativa, por opção da pessoa jurídica, das operações de vendas, compras e/ou devoluções por Nota Fiscal Eletrônica – NF-e, com base nos registros C100, C110, C120 e C170. Neste caso, a empresa optante por escriturar a EFD-Contribuições, na visão de documento, deve utilizar o leiaute destes registros constante nas especificações técnicas de geração da Escrituração Fiscal Digital – EFD (ICMS e IPI);
3. O leiaute, as especificações técnicas e o Programa Validador e Assinador da Escrituração Fiscal Digital – EFD (ICMS e IPI) encontram-se disponibilizados no portal de serviços (SPED) da página da Receita Federal do Brasil na Internet, no endereço <sped.rfb.gov.br>;
4. Para as operações documentadas por Nota Fiscal (Código 01), Nota Fiscal Avulsa (código 1B) e Nota Fiscal de Produtor (código 04), o registro C100 (e filhos) é de preenchimento obrigatório na EFD-Contribuições, em relação às operações de vendas e de aquisições e/ou devoluções (com direito a crédito) realizadas no período.
5. O detalhamento das informações dos itens dos documentos escriturados em “C100”, que repercutam na apuração das contribuições sociais (operações de vendas) e dos créditos (operações de compras) deve ser informado, em relação a cada item relacionado no documento, no registro Filho “C170”;
6. Caso o arquivo gerado pela pessoa jurídica contenha, em relação às operações documentadas por Nota Fiscal Eletrônica (NF-e) registros individualizados por documentos (C100 e filhos) e registros de consolidação (C180 e C190, e filhos), deverá informar no registro C010, no campo “IND_ESCRI”, se a escrituração está considerando as informações individualizadas ou as informações consolidadas.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [C100]
Campo 02 - Valores válidos: [0, 1]
Preenchimento: indicar a operação, conforme os códigos. Podem ser informados como documentos de entrada os documentos emitidos por terceiros e os documentos emitidos pelo próprio informante da EFD-Contribuições.
Campo 03 - Valores válidos: [0, 1]
Preenchimento: consideram-se de emissão própria somente os documentos fiscais emitidos pelo estabelecimento informante (campo CNPJ do registro C010) da EFD.
Se a legislação estadual a que estiver submetido o contribuinte obrigá-lo a escriturar notas fiscais avulsas em operação de saída, este campo deve ser informado com valor igual a “0” (zero).
Validação: se este campo tiver valor igual a “1” (um), o campo IND_OPER deve ser igual a “0” (zero).
Campo 04 - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 05 - Valores válidos: [01, 1B, 04, 55, 65]
Preenchimento: o valor informado deve constar na tabela 4.1.1 do Manual do Leiaute da EFD-Contribuições. O “código” a ser informado não é exatamente o “modelo” do documento, devendo ser consultada a tabela 4.1.1. Exemplo: o código “01” deve ser utilizado para os modelos “1” ou “1A".
Campo 06 - Valores válidos: [00, 01, 02, 03, 04, 05, 06, 07, 08]
Preenchimento e Validação: verificar a descrição da situação do documento na tabela 4.1.2. Os valores “04” e “05” só são possíveis para NF-e de emissão própria. NF-e “avulsas” emitidas pelas UF (séries 890 a 899) devem ser informados como emissão de terceiros, com o código de situação do documento igual a “08 - Documento Fiscal emitido com base em Regime Especial ou Norma Específica”.
Campo 07 – Preenchimento: informar neste campo a série do documento fiscal, se existir. Campo de preenchimento obrigatório com três posições para NF-e, COD_MOD igual a “55”, de emissão própria ou de terceiros e para NFC-e, COD_MOD igual a “65” de emissão própria. Se não existir Série para NF-e ou NFC-e, informar 000.
Campo 08 – Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 09 - Preenchimento: campo a ser preenchido quando o documento escriturado for NF-e, COD_MOD igual a “55”, com base nas seguintes definições:
1. Escrituração referente a período anterior ou igual a março de 2012:
Se IND_EMIT = 0 (Emissão própria): Preenchimento obrigatório (sujeito à validação)
Se IND_EMIT = 1 (Emissão de terceiros): Preenchimento opcional (sujeito à validação)
2. Escrituração referente a período igual ou posterior a abril de 2012:
Se IND_EMIT = 0 (Emissão própria): Preenchimento obrigatório (sujeito à validação)
Se IND_EMIT = 1 (Emissão de terceiros): Preenchimento obrigatório (sujeito à validação)
OBS: Tendo em vista que o preenchimento desse campo não é obrigatório, em relação aos períodos de apuração ocorridos até 31 de março de 2012, caso a versão utilizada do PVA da EFD-Contribuições, neste período, não valide a informação da chave da NF-e, no caso de emissão de terceiros, deve a pessoa jurídica deixar o campo em branco, sem a informação da Chave, para a validação e transmissão da escrituração
Validação: É conferido o dígito verificador (DV) da chave da NF-e. Este campo é de preenchimento obrigatório para COD_MOD igual a “55” e “65”, quando o campo IND_EMIT for igual a “0” (Emissão Própria). Para confirmação inequívoca de que a chave da NF-e corresponde aos dados informados do documento, será comparado o CNPJ existente na CHV_NFE com o campo CNPJ do registro C010, que corresponde ao CNPJ do informante do arquivo. Serão verificados a consistência da informação do campo NUM_DOC e o número do documento contido na chave da NF-e. Será também comparada a UF codificada na chave da NF-e com o campo UF informado no registro 0000.
No caso de operações de entradas por NF-e de emissão de terceiros, a informação da chave é facultativa e quando preenchida serão conferidos: 1) o dígito verificador; 2) o número do documento existente na chave comparado com o informado no campo anterior (NUM_DOC).
Campo 10 - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data de entrada/saída (campo 11) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 11 - Preenchimento: informar a data de entrada ou saída, conforme a operação, no formato ddmmaaaa; excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”. Quando o campo IND_OPER indicar operação de “saída”, este campo será informado apenas se o contribuinte possuir este dado em seus sistemas.
Validação: a data informada neste campo ou a data de emissão do documento fiscal (campo 10) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Para operações de entrada ou saída este valor deve ser maior ou igual à data de emissão (campo DT_DOC).
Nas operações de entradas de produtos este campo é sempre de preenchimento obrigatório.
Campo 12 – Preenchimento: informar o valor total do documento fiscal.
Campo 13 - Valores válidos: [0, 1, 9]
Preenchimento: informar o tipo de pagamento pactuado, independente do pagamento ocorrer em período anterior, no próprio período ou em período posterior ao de referência da escrituração. A partir de 01/07/2012 passará a ser:
Indicador do tipo de pagamento:
0- À vista;
1- A prazo;
2 - Outros
Campo 14 - Preenchimento: informar o valor do desconto incondicional discriminado na nota fiscal.
Campo 16 -  Preenchimento: informar o valor total das mercadorias e serviços.
Validação: O valor informado no campo deve ser igual à soma do campo VL_ITEM dos registros C170 (“filhos” deste registro C100), conforme regra definida também para a EFD (ICMS/IPI).
Campo 17 - Valores válidos: [0, 1, 2, 3, 4, 9]
Preenchimento: Em operações tais como: remessas simbólicas, faturamento simbólico, transporte próprio, venda balcão, informar o código “9 - sem frete”, ou seja, operações sem cobrança de frete.
Quando houver transporte com mais de um responsável pelo seu pagamento, deve ser informado o indicador do frete relativo ao responsável pelo primeiro percurso.
No sentido de harmonizar o conteúdo dos campos de registros comuns à EFD-Contribuições e à EFD (ICMS/IPI), bem como ao leiaute da NFe 4.1, em produção a partir de 1º de outubro de 2017 os indicadores do Campo 17 passam a ter a seguinte descrição:

| 17 | IND_FRT | Obs.: A partir de 01/01/2012 passará a ser: Indicador do tipo do frete: 0- Por conta do emitente; 1- Por conta do destinatário/remetente; 2- Por conta de terceiros; 9- Sem cobrança de frete. | C | 001* | - | S |
| --- | --- | --- | --- | --- | --- | --- |
| 17 | IND_FRT | Obs.: A partir de 01/10/2017 passará a ser: Indicador do tipo de frete/transporte: 0 - Frete por conta do remetente (CIF); 1 - Frete por conta do destinatário (FOB); 2 - Frete por conta de terceiros; 3 – Transporte próprio por conta do remetente; 4 – Transporte próprio por conta do destinatário; 9 - Sem ocorrência de transporte. | C | 001* | - | S |

Importante: No preenchimento/edição do registro C100, no próprio PVA, deve a empresa proceder à codificação (códigos “0”, “1”, “2”, “3”, “4” e “9”), de acordo com a descrição definida para cada período a que se refere a escrituração, para o campo 17, independente da descrição visualizada no respectivo campo de edição, no PVA.
Campo 18 - Preenchimento: informar o valor do frete pago/contratado, indicado no documento fiscal.
Importante registrar que vindo o valor do frete constante no documento fiscal a integrar a operação da venda, sendo o ônus for suportado pelo adquirente, o seu valor integra o produto da venda e, por conseguinte, compõe a receita bruta da pessoa jurídica vendedora, conforme disposições sobre a receita bruta na Lei nº 12.973/2014, a qual estabelece que "a receita bruta compreeende o produto da venda de bens nas operações em conta própria".
Neste sentido, considerando que o acessório (receita do frete) acompanha e tem a mesma natureza do principal (receita da produto/item vendido), a receita de frete deve seguir o tratamento tributário, o mesmo CST, aplicável ao(s) produtos objeto do transporte a que se refere o frete. Assim, temos o seguinte procedimento a adotar:
- se o produto/item é tributável à alíquota básica, o frete correspondente é tributável à alíquota básica;
- se o produto/item é tributável à alíquota zero, o frete correspondente é tributável à alíquota zero;
- se o produto/item é tributável à alíquota monofásica, o frete correspondente é tributável à alíquota monofásica;
- se o produto/item goza de suspensão, isenção ou não incidência, o frete correspondente goza de suspensão, isenção ou não incidência.
Observações:
1. Quando o frete nas operações de vendas não for suportado pelo vendedor, mas sim pelo adquirente, o seu valor deve integrar a base de cálculo do(s) produto(s) vendido(s), devendo assim ter o seu valor acrescido ao valor da base de cálculo do PIS/Pasep e da Cofins, nos correspondentes campos do Registro C170. No caso da pessoa jurídica vir a escriturar essa receita de frete no registro F100, deve observar as regras de tributação acima descritas.
2. Quando o frete nas operações de vendas for suportado pelo vendedor, o seu valor constituí hipótese de crédito no regime não cumulativo de apuração do PIS/pasep e da Cofins, conforme art. 3º das leis nº 10.637/2002 e 10.833/2003, respectivamente
Campo 22 – Preenchimento: informar o valor do ICMS creditado na operação de entrada ou o valor do ICMS debitado na operação de saída.
Campo 24 - Preenchimento: informar o valor do ICMS creditado/debitado por substituição tributária, nas operações de entrada ou saída, conforme legislação aplicada.
Campo 25 - Preenchimento: informar o valor total do IPI constante no documento fiscal.
Campo 26 - Preenchimento: informar o valor total do PIS/Pasep (débito ou crédito) referente ao documento fiscal.
Campo 27 - Preenchimento: informar o valor total da Cofins (débito ou crédito) referente ao documento fiscal.
Campo 28 - Preenchimento: informar o valor total do PIS/Pasep retido por substituição tributária, referente ao documento fiscal.
Campo 29 - Preenchimento: informar o valor total da Cofins retida por substituição tributária, referente ao documento fiscal.
Esclarecimentos adicionais quanto às operações tratadas neste registro:
I - De Vendas Canceladas, Retorno de Mercadorias e Devolução de Vendas.
Se a empresa está escriturando por documento, em C100, as vendas canceladas deve assim ser tratada:
1. Se o cancelamento se deu no próprio mês da emissão do documento, a empresa tem a opção de não relacionar na escrituração este documento ou, vindo a relacioná-lo, o fazer com as informações solicitadas para C100, mas sem gerar os registros filhos (C170);
2. Se o cancelamento se deu em período posterior ao de sua emissão, devendo assim ser considerado na redução da base de cálculo do período em que ocorreu o cancelamento, a empresa pode proceder à escrituração destes valores redutores da base de cálculo do mês do cancelamento, mediante a geração de registros de ajustes de débitos, em M220 (PIS) e M620 (Cofins), fazendo constar nestes registros de ajustes o montante da contribuição a ser reduzida, em decorrência do(s) cancelamentos em questão. Para os fatos geradores ocorridos a partir de janeiro/2019, os ajustes da base de cálculo do período em que ocorreu o cancelamento devem ser realizados, preferencialmente, nos campos próprios dos registros M210 (PIS - Campo 06 - VL_AJUS_REDUC_BC_PIS) e M610 (Cofins - Campo 06 - VL_AJUS_REDUC_BC_COFINS). Neste caso, o detalhamento do ajuste será informado nos registros M215 (PIS) e M615 (Cofins), respectivamente, preenchendo o campo COD_AJ_BC com o código 01 - Vendas canceladas de receitas tributadas em períodos anteriores - da tabela 4.3.18.
Já a operação de retorno de produtos ao estabelecimento emissor da nota fiscal, conforme previsão existente no RIPI/2010 (art. 234 do Decreto Nº 7.212, de 2010) e no Convênio SINIEF SN, de 1970 (Capítulo VI, Seção II – Da Nota Fiscal), para fins de escrituração de PIS/COFINS deve receber o tratamento de cancelamento de venda (não integrando a base de cálculo das contribuições nem dos créditos).
Registre-se que a venda cancelada é hipótese de exclusão da base de cálculo da contribuição (em C170, no caso de escrituração individualizada por documento fiscal ou em C181 (PIS/Pasep) e C185 (Cofins)), tanto no regime de incidência cumulativo como no não cumulativo.
A nota fiscal de entrada da mercadoria retornada, emitida pela própria pessoa jurídica, pode ser relacionada nos registros consolidados C190 e filhos (Operações de aquisição com direito a crédito, e operações de devolução de compras e vendas) ou nos registros individualizados C100 e filhos, somente para fins de maior transparência da apuração, visto não configurar hipótese legal de creditamento de PIS/COFINS. Neste caso, utilize o CST 98 ou 99.
Já as operações de Devolução de Vendas, no regime de incidência não cumulativo, correspondem a hipóteses de crédito, devendo ser escrituradas com os CFOP correspondentes em C170 (no caso de escrituração individualizada dos créditos por documento fiscal) ou nos registros C191/C195 (no caso de escrituração consolidada dos créditos), enquanto que, no regime cumulativo, tratam-se de hipótese de exclusão da base de cálculo da contribuição.
Dessa forma, no regime cumulativo, caso a operação de venda a que se refere o retorno tenha sido tributada para fins de PIS/COFINS, a receita da operação deverá ser excluída da apuração:
1. Caso a pessoa jurídica esteja utilizando os registros consolidados C180 e filhos (Operações de Vendas), não deverá incluir esta receita na base de cálculo das contribuições nos registros C181 e C185.
2. Caso a pessoa jurídica esteja utilizando os registros C100 e filhos, deverá incluir a nota fiscal de saída da mercadoria com a base de cálculo zerada, devendo constar no respectivo registro C110 a informação acerca do retorno da mercadoria, conforme consta no verso do documento fiscal ou do DANFE (NF-e).
Caso não seja possível proceder estes ajustes diretamente no bloco C, a pessoa jurídica deverá proceder aos ajustes diretamente no bloco M, nos respectivos campos e registros de ajustes de redução de contribuição (M220 e M620). Neste caso, deverá utilizar o campo “NUM_DOC” e “DESCR_AJ” para relacionar as notas fiscais de devolução de vendas, como ajuste de redução da contribuição cumulativa. Para os fatos geradores ocorridos a partir de janeiro/2019, caso não seja possível proceder estes ajustes de base de cálculo diretamente no bloco C, os mesmos devem ser realizados, preferencialmente, nos campos próprios dos registros M210 (PIS - Campo 06 - VL_AJUS_REDUC_BC_PIS) e M610 (Cofins - Campo 06 - VL_AJUS_REDUC_BC_COFINS). Neste caso, o detalhamento do ajuste será informado nos registros M215 (PIS) e M615 (Cofins), respectivamente, preenchendo o campo COD_AJ_BC com o código 02 - Devoluções de vendas tributadas em períodos anteriores - da tabela 4.3.18.
Mesmo não gerando direito a crédito no regime cumulativo, a nota fiscal de devolução de bens e mercadorias pode ser informada nos registros consolidados C190 e filhos, ou C100 e filhos, para fins de transparência na apuração. Nesse caso, deve ser informado o CST 98 ou 99, visto que a devolução de venda no regime cumulativo não gera crédito.
II – Devolução de Compras.
Os valores relativos às devoluções de compras, referentes a operações de aquisição com crédito da não cumulatividade, devem ser escriturados pela pessoa jurídica, no mês da devolução, e os valores dos créditos  correspondentes a serem anulados/estornados, devem ser informados preferencialmente mediante ajuste na base de cálculo da compra dos referidos bens, seja nos registros C100/C170 (informação individualizada), seja nos registros C190 e filhos (informação consolidada).
Caso não seja possível proceder estes ajustes diretamente no bloco C (como no caso da devolução ocorrer em período posterior ao da escrituração), a pessoa jurídica poderá proceder aos ajustes diretamente no bloco M, nos respectivos campos (campo 10 dos registros M100 e M500) e o detalhamento nos registros de ajustes de crédito (M110 e M510). Neste último caso, deverá utilizar o campo "NUM_DOC" e "DESCR_AJ"  para relacionar as notas fiscais de devolução, como ajuste de redução de crédito.
Por se referir a uma operação de saída, a devolução de compra deve ser escriturada com o CST 49. O valor da devolução deverá ser ajustado nas notas fiscais de compra ou, se não for possível, diretamente no bloco M. Neste último caso, deverá utilizar o campo de número do documento e descrição do ajuste para relacionar as notas fiscais de devolução.
<!-- End Registro C100 -->
<!-- Start Registro C110 -->
Registro C110: Complemento do Documento - Informação Complementar da Nota Fiscal (Códigos 01, 1B, 04 e 55)
Este registro tem por objetivo identificar os dados contidos no campo Informações Complementares da Nota Fiscal, que sejam de interesse do Fisco ou conforme disponha a legislação, e que estejam explicitamente citadas no documento Fiscal, tais como: forma de pagamento, local da prestação/execução do serviço, operação realizada com suspensão das contribuições sociais, etc.
Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo no campo COD_INF.
Registro com estrutura, campos e conteúdo definidos e constantes no Leiaute da Escrituração Fiscal Digital – EFD (ICMS e IPI), instituído pelo Ato COTEPE/ICMS nº 9, de 12 de abril de 2008, disponível no portal de serviços (SPED) da página da Secretaria da Receita Federal do Brasil na Internet, no endereço <sped.rfb.gov.br>.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C110" | C | 004 | - | S |
| 02 | COD_INF | Código da informação complementar do documento fiscal (campo 02 do Registro 0450) | C | 006 | - | S |
| 03 | TXT_COMPL | Descrição complementar do código de referência. | C | - | - | N |

Observações: Devem ser observadas para este registro as observações constantes no registro pai (C100).
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C110]
Campo 02 - Validação: o valor informado no campo deve existir no registro 0450 - Tabela de informação complementar.
<!-- End Registro C110 -->
<!-- Start Registro C111 -->
Registro C111: Processo Referenciado
Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos, pelo Programa Validador e Assinador da EFD-Contribuições.
Uma vez procedida à escrituração do Registro “C111”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C111" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - | S |

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
Campo 01 - Valor Válido: [C111]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C111 -->
<!-- Start Registro C120 -->
Registro C120: Complemento do Documento - Operações de Importação (Código 01)
Este registro tem por objetivo informar detalhes das operações de importação, que estejam sendo documentadas pela nota fiscal escriturada no registro C100 (registro individualizado de documentos códigos 1, 1B, 04 e 55 - NF-e), quando o campo IND_OPER for igual a “0” (zero), indicando operação de entrada e que no registro filho C170 conste CST_PIS ou CST_COFINS gerador de crédito (CST 50 a 56), bem como conste no registro C170 CFOP próprio de operações de importação (CFOP iniciado em 3).
Este registro deve ser utilizado mesmo que o documento escriturado em C100 e C170 refira-se a NFe (modelo 55). O registro C199 somente deve ser utilizado quando a PJ optou por relacionar suas operações com direito a crédito e documentadas por NFe nos registros consolidadores C190 e filhos.Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo no campo NUM_DOC_IMP e NUM_ACDRAW.
Registro com estrutura, campos e conteúdo definidos e constantes no Leiaute da Escrituração Fiscal Digital – EFD (ICMS e IPI), instituído pelo Ato COTEPE/ICMS nº 9, de 12 de abril de 2008, disponível no portal de serviços (SPED) da página da Secretaria da Receita Federal do Brasil na Internet, no endereço <sped.rfb.gov.br>.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C120" | C | 004 | - | S |
| 02 | COD_DOC_IMP | Documento de importação: 0 – Declaração de Importação; 1 – Declaração Simplificada de Importação;  A partir dos fatos geradores ocorridos em 01/2019: Documento de importação: 0 – Declaração de Importação; 1 – Declaração Simplificada de Importação; 2 – Declaração Única de Importação | C | 001* | - | S |
| 03 | NUM_DOC_IMP | Número do documento de Importação. | C | 015 | - | S |
| 04 | VL_PIS_IMP | Valor pago de PIS na importação | N | - | 02 | N |
| 05 | VL_COFINS_IMP | Valor pago de COFINS na importação | N | - | 02 | N |
| 06 | NUM_ACDRAW | Número do Ato Concessório do regime Drawback | C | 020 | - | N |

Observações:
1. Devem ser observadas para este registro as observações constantes no registro pai (C100).
Caso a pessoa jurídica tenha importado mercadorias, bens e produtos de pessoa física ou jurídica domiciliada no exterior, com direito a crédito na forma prevista na Lei nº 10.865, de 2004, deve preencher o Registro “C120” para validar a apuração do crédito.
2. Deve ser informado neste registro os pagamentos de PIS/Pasep-Importação e de Cofins-Importação, referente ao serviço contratado com direito a crédito, uma vez que de acordo com a legislação em referência, o direito à apuração de crédito aplica-se apenas em relação às contribuições efetivamente pagas na importação de bens e serviços (art. 15 da Lei nº 10.865, de 2004).
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C120]
Campo 02 - Valores Válidos: [0,1,2]
Campo 03 - Preenchimento: informar o número do documento de importação
Campo 04 - Preenchimento: Informar o valor recolhido de PIS/Pasep – Importação, relacionado ao documento informado neste registro. No caso de haver mais de um recolhimento (PIS/Pasep – Importação) em relação ao mesmo documento, informar no campo o somatório dos valores pagos.
De acordo com a legislação, o direito ao crédito de PIS/Pasep aplica-se em relação às contribuições efetivamente pagas na importação de bens e serviços.
Campo 05 - Preenchimento: Informar o valor recolhido de Cofins – Importação, relacionado ao documento informado neste registro. No caso de haver mais de um recolhimento (Cofins – Importação) em relação ao mesmo documento, informar no campo o somatório dos valores pagos.
De acordo com a legislação, o direito ao crédito de Cofins aplica-se em relação às contribuições efetivamente pagas na importação de bens e serviços.
Campo 06 - Preenchimento: Informar neste campo o número do ato concessório habilitando o estabelecimento ao Regime Aduaneiro Especial de Drawback.
<!-- End Registro C120 -->
<!-- Start Registro C170 -->
Registro C170: Complemento do Documento - Itens do Documento (Códigos 01, 1B, 04 e 55)
Registro obrigatório para discriminar os itens da nota fiscal (mercadorias e/ou serviços constantes em notas conjugadas), inclusive em operações de entrada de mercadorias acompanhada de Nota Fiscal Eletrônica (NF-e) de emissão de terceiros.
Não podem ser informados para um mesmo documento fiscal, dois ou mais registros com o mesmo conteúdo no campo NUM_ITEM.
Registro com estrutura, campos e conteúdo definidos e constantes no Leiaute da Escrituração Fiscal Digital – EFD (ICMS e IPI), instituído pelo Ato COTEPE/ICMS nº 9, de 12 de abril de 2008, disponível no portal de serviços (SPED) da página da Secretaria da Receita Federal do Brasil na Internet, no endereço <sped.rfb.gov.br>.
IMPORTANTE: para documentos de entrada/aquisição, os campos de valor de imposto/contribuição, base de cálculo e alíquota só devem ser informados se o adquirente tiver direito à apropriação do crédito (enfoque do declarante). Não precisam ser relacionados documentos fiscais que não dão direito à apuração de créditos de PIS/Pasep e de Cofins. Caso o documento fiscal contenha tanto itens sem direito à apropriação de crédito quanto itens com direito, a nota fiscal deverá ser informada em sua integralidade.
Não precisam ser relacionados nesse registro os documentos fiscais representativos das operações geradoras de contribuição social ou de crédito, abaixo relacionadas, tendo em vista que as mesmas são informadas e consideradas em registros próprios da EFD-Contribuições:
Aquisição de bens a serem incorporados ao ativo imobilizado, cujo crédito for determinado com base no valor de aquisição e/ou com base nos encargos mensais de depreciação. O detalhamento do crédito com base nos encargos de depreciação deverá ser feito no registro F120. Caso o crédito seja apurado com base no valor de aquisição deverá ser informado no registro F130
-	Caso a pessoa jurídica venha a proceder neste registro à escrituração da aquisição de bens a serem incorporados ao ativo imobilizado, objeto de crédito mediante a escrituração do Registro F120 (com base no encargo de depreciação) ou do Registro F130 (com base no valor de aquisição), deverá informar no Campos 25 (CST_PIS) e 31 (CST_COFINS) o CST “98” ou “99”
Fornecimento e/ou Aquisição de Energia Elétrica (documento fiscal, códigos 06 ou 55). Os documentos fiscais relativos à energia elétrica devem ser escriturados nos registros C500 (Aquisição com crédito) e/ou C600 (Fornecimento de energia);
Prestação e/ou Aquisição de serviços de transportes (documentos fiscais códigos 07, 08, 8B, 09, 10, 11, 26, 27 e 57). Os referidos documentos fiscais relativos a serviços de transportes devem ser escriturados nos registros D100 (Aquisição com crédito) e/ou D200 (Prestação de serviço);
Prestação e/ou Aquisição de serviços de transporte de passageiros – Bilhetes de Passagem (documentos fiscais códigos 2E, 13, 14, 15, 16 e 18). Os referidos documentos fiscais relativos a serviços de transporte de passageiros devem ser escriturados nos registros D300 ou D350 (bilhete emitido por ECF);
Prestação e/ou Aquisição de serviços de comunicação e telecomunicação (documentos fiscais códigos 21 e 22). Os referidos documentos fiscais relativos a serviços de comunicação e telecomunicação devem ser escriturados nos registros D500 (Aquisição com crédito) e/ou D600 (Prestação de serviço);
Fornecimento e/ou Aquisição de água canalizada ou gás (documentos fiscais códigos 28 e 29). Os documentos fiscais relativos a água canalizada e gás devem ser escriturados nos registros C500 (Aquisição com crédito) e/ou C600 (Fornecimento d´água canalizada e gás);
Cupom Fiscal (documentos fiscais códigos 02, 2D e 59). Os documentos fiscais relativos Cupom Fiscal devem ser escriturados nos registros C400 (informação por ECF) ou C490 (informação consolidada).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C170" | C | 004 | - | S |
| 02 | NUM_ITEM | Número seqüencial do item no documento fiscal | N | 003 | - | S |
| 03 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | S |
| 04 | DESCR_COMPL | Descrição complementar do item como adotado no documento fiscal | C | - | - | N |
| 05 | QTD | Quantidade do item | N | - | 05 | N |
| 06 | UNID | Unidade do item (Campo 02 do registro 0190) | C | 006 | - | N |
| 07 | VL_ITEM | Valor total do item (mercadorias ou serviços) | N | - | 02 | S |
| 08 | VL_DESC | Valor do desconto comercial / exclusão da base de cálculo do PIS/PASEP e da COFINS | N | - | 02 | N |
| 09 | IND_MOV | Movimentação física do ITEM/PRODUTO: 0. SIM 1. NÃO | C | 001 | - | N |
| 10 | CST_ICMS | Código da Situação Tributária referente ao ICMS, conforme a Tabela indicada no item 4.3.1 | N | 003* | - | N |
| 11 | CFOP | Código Fiscal de Operação e Prestação | N | 004* | - | S |
| 12 | COD_NAT | Código da natureza da operação (campo 02 do Registro 0400) | C | 010 | - | N |
| 13 | VL_BC_ICMS | Valor da base de cálculo do ICMS | N | - | 02 | N |
| 14 | ALIQ_ICMS | Alíquota do ICMS | N | 006 | 02 | N |
| 15 | VL_ICMS | Valor do ICMS creditado/debitado | N | - | 02 | N |
| 16 | VL_BC_ICMS_ST | Valor da base de cálculo referente à substituição tributária | N | - | 02 | N |
| 17 | ALIQ_ST | Alíquota do ICMS da substituição tributária na unidade da federação de destino | N | 006 | 02 | N |
| 18 | VL_ICMS_ST | Valor do ICMS referente à substituição tributária | N | - | 02 | N |
| 19 | IND_APUR | Indicador de período de apuração do IPI: 0 - Mensal; 1  Decendial | C | 001* | - | N |
| 20 | CST_IPI | Código da Situação Tributária referente ao IPI, conforme a Tabela indicada no item 4.3.2. | C | 002* | - | N |
| 21 | COD_ENQ | Código de enquadramento legal do IPI, conforme tabela indicada no item 4.5.3. | C | 003* | - | N |
| 22 | VL_BC_IPI | Valor da base de cálculo do IPI | N | - | 02 | N |
| 23 | ALIQ_IPI | Alíquota do IPI | N | 006 | 02 | N |
| 24 | VL_IPI | Valor do IPI creditado/debitado | N | - | 02 | N |
| 25 | CST_PIS | Código da Situação Tributária referente ao PIS. | N | 002* | - | S |
| 26 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 27 | ALIQ_PIS | Alíquota do PIS (em percentual) | N | 008 | 04 | N |
| 28 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS/PASEP | N | - | 03 | N |
| 29 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 30 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 31 | CST_COFINS | Código da Situação Tributária referente ao COFINS. | N | 002* | - | S |
| 32 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 33 | ALIQ_COFINS | Alíquota do COFINS (em percentual) | N | 008 | 04 | N |
| 34 | QUANT_BC_COFINS | Quantidade – Base de cálculo COFINS | N | - | 03 | N |
| 35 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 36 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 37 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Devem ser observadas para este registro as observações constantes no registro pai (C100).
2. Este registro deve ser preenchido para detalhar, em relação a cada item constante no documento fiscal escriturado em C100, as informações referentes ao CST, bases de cálculo, alíquota e valor da contribuição ou do crédito.
3. Caso a pessoa jurídica apure a Contribuição Social por Unidade de Medida de Produto (Combustíveis, Bebidas Frias e Embalagem para Bebidas, etc), deve preencher os campos “QUANT_BC_PIS”, “QUANT_BC_COFINS”, “ALIQ_PIS_QUANT” e “ALIQ_COFINS_QUANT”. Neste caso (contribuição apurada por unidade de medida) os campos “VL_BC_PIS”, “VL_BC_COFINS”, “ALIQ_PIS” e “ALIQ_COFINS” não devem ser preenchidos.
4. Os valores escriturados nos campos de bases de cálculo de PIS/Pasep (Campos 26 e 28) e de Cofins (Campos 32 e 34), de itens com CST representativos de receitas tributadas ou de operações geradoras de créditos, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210) e da Cofins (M610) apuradas, bem como para a demonstração das bases de cálculo dos créditos de PIS/Pasep (M105) e da Cofins (M505) apurados, conforme o caso.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C170]
Campo 02 - Validação: deve ser maior que “0” (zero) e sequencial.
Campo 03 - Validação: o valor informado neste campo deve existir no registro 0200. Atentar para a premissa de que a informação deve ser prestada pela ótica da pessoa jurídica titular da escrituração, ou seja, nas operações de entradas de mercadorias, os códigos informados devem ser os definidos pelo próprio informante e não aqueles constantes do documento fiscal.
Campo 04 - Preenchimento: neste campo pode ser informada a descrição complementar do item, conforme adotado no documento fiscal.
Campo 05 - Preenchimento: informar a quantidade do item, expressa na unidade informada no campo UNID.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 06 - Preenchimento: informar a unidade de medida de comercialização do item utilizada no documento fiscal.
Validação: o valor informado neste campo deve existir no registro 0190.
Campo 07 - Preenchimento: informar o valor total do item/produto, somente o valor das mercadorias (equivalente à quantidade vezes preço unitário) ou do serviço.
Validação: a soma de valores dos registros C170 deve ser igual ao valor informado no campo VL_MERC do registro C100.
Campo 08 - Preenchimento: informar o valor do desconto comercial, ou seja, os descontos incondicionais constantes do próprio documento fiscal e das demais exclusões da base de cálculo do PIS/Pasep e da Cofins, aplicáveis ao ítem escriturado neste registro, desde que não exista campo específico neste mesmo registro para efetuar o detalhamento da exclusão. Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 09 - Valores válidos: [0, 1]
Preenchimento: indicar a movimentação física do item ou produto. Será informado o código “1” em todas as situações em que não houver movimentação de mercadorias, por exemplo: notas fiscais complementares, simples faturamento, remessas simbólicas, etc.
Campo 10 – Preenchimento: verificar orientações constantes do Guia Prático da Escrituração Fiscal Digital do ICMS/IPI (Sped Fiscal).
Campo 11 - Preenchimento: nas operações de entradas, devem ser registrados os códigos de operação que correspondem ao tratamento tributário relativo à destinação do item.
Deve ser ressaltado que na geração dos registros M105 (Base de Cálculo do crédito de PIS/Pasep) e M505 (Base de cálculo do crédito de Cofins) pelo PVA, serão consideradas apenas as operações de aquisição de bens, mercadorias e serviços (nota conjugada) e devoluções de vendas relacionadas neste registro, cujos CST sejam representativos de operações com direito a crédito (CST 50 a 66) e cujo conteúdo do campo CFOP seja referentes a:
Aquisição de bens para revenda;
Aquisição de bens utilizados como insumo;
Aquisição de serviços utilizados como insumo;
Devolução de vendas sujeitas ao regime não cumulativo;
Outras operações com direito a crédito.
OBS: A relação dos CFOP representativos dessas operações, que dão direito ao crédito, está disponibilizada na Tabela “CFOP – Operações Geradoras de Crédito” no Portal do Sped, no endereço eletrônico da Receita Federal do Brasil (http://www.receita.fazenda.gov.br).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Se o campo IND_OPER do registro C100 for igual a “0” (zero), então o primeiro caractere do CFOP deve ser igual a 1, 2 ou 3. Se campo IND_OPER do registro C100 for igual a “1” (um), então o primeiro caractere do CFOP deve ser igual a 5, 6 ou 7. O primeiro caractere deve ser o mesmo para todos os itens de um documento fiscal.
Campo 12 - Validação: o valor informado no campo deve existir no registro 0400 -Tabela de Natureza da Operação.
Campo 14 - Validação: nas operações de saídas, se os dois últimos caracteres do CST_ICMS forem 00, 10, 20 ou 70, o campo ALIQ_ICMS deve ser maior que “0” (zero).
Campo 19 - Valores válidos: [0, 1]
Campo 20 - Preenchimento: o campo deverá ser preenchido somente se o declarante for contribuinte do IPI. A tabela do CST_IPI consta publicada na Instrução Normativa RFB nº 1009, de 10 de fevereiro de 2010.
Campo 23 - Preenchimento: preencher com a alíquota do IPI estabelecida na TIPI e não preencher, quando a forma de tributação do IPI for fixada em reais e calculada por unidade ou por determinada quantidade de produto.
Campo 24 - Preenchimento: deverão ser destacados e informados neste campo todos os débitos e/ou créditos de IPI da operação. Esses valores serão totalizados para o registro C190, na combinação de CST_ICMS + CFOP + ALIQ_ICMS, bem como, comparados com o total informado no registro C100.
Campo 25 - Preenchimento: informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 26 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item documento fiscal, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
Atenção: No caso de escrituração de receitas decorrentes da venda de bebidas frias, nos termos do art. 14 a 34 da Lei nº 13.097/2015, pelos fabricantes e atacadistas, o valor do frete integrará a base de cálculo da Contribuição para o PIS/Pasep apurada pela pessoa jurídica vendedora dos citados produtos, para os fatos geradores a partir de 01.05.2015. Desta forma, a partir de 01.01.2015, deve a pessoa jurídica acrescer ao valor do Campo 26, o valor do frete correspondente à venda.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “VL_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 27 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 28 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social ou de crédito, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 28 (base de cálculo em quantidade) dispensa o preenchimento do campo 26 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “QUANT_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 29 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social ou do crédito, sobre a base de cálculo expressa em quantidade (campo 28).
Campo 30 – Preenchimento: informar o valor do PIS/Pasep (contribuição ou crédito) referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição e/ou do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500 e VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 26 ou campo 28) multiplicado pela alíquota aplicável ao item (campo 27 ou campo 29).
Campo 31 - Preenchimento: informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 32 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item documento fiscal, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
Atenção: No caso de escrituração de receitas decorrentes da venda de bebidas frias, nos termos do art. 14 a 34 da Lei nº 13.097/2015, pelos fabricantes e atacadistas, o valor do frete integrará a base de cálculo da Cofins apurada pela pessoa jurídica vendedora dos citados produtos, para os fatos geradores a partir de 01.05.2015. Desta forma, a partir de 01.01.2015, deve a pessoa jurídica acrescer ao valor do Campo 32, o valor do frete correspondente à venda.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de Cofins (M505, campo “VL_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 33 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 34 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social ou de crédito, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 34 (base de cálculo em quantidade) dispensa o preenchimento do campo 32 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de Cofins (M505, campo “QUANT_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 35 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social ou do crédito, sobre a base de cálculo expressa em quantidade (campo 34).
Campo 36 – Preenchimento: informar o valor da Cofins (contribuição ou crédito) referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição e/ou do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500 e VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 32 ou campo 34) multiplicado pela alíquota aplicável ao item (campo 33 ou campo 35).
Campo 37 - Preenchimento: informar o Código da Conta Analítica. Exemplos: estoques, receitas, despesas, ativos. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C170 -->
<!-- Start Registro C175 -->
Registro C175: Registro Analítico do Documento (Código 65)
Este registro tem por objetivo representar a escrituração da NFC-e, código 65, os documentos fiscais totalizados por CST PIS, CST Cofins, CFOP, alíquota de PIS e alíquota da Cofins. Trata-se de registro com procedimento de escrituração similar ao adotado para o registro C190 da EFD-ICMS/IPI.
Atenção:
1. Registro analítico das receitas decorrentes de emissão de NFC-e, disponível na versão 2.09 do PVA da EFD-Contribuições, para utilização na escrituração dos fatos geradores a partir de setembro de 2014.
2. As receitas eventualmente auferidas com a emissão de NFC-e, referentes aos períodos anteriores ao da disponibilidade da versão 2.09, devem ser escrituradas de forma consolidada no Registro C180, devendo observar as instruções de preenchimento do referido registro.
3. Apesar da escrituração do documento ser de forma individualizada por meio do registro C100, a escrituração da NFC-e referente ao seu conteúdo, seu item, não é feita de forma individualizada item a item (no registro C170, como é o procedimento para a NF-e, código 55), mas sim, de forma analítica, neste registro C175.
4. Para tanto, será gerado um registro C175, para consolidar todos os itens do documento que tenham o mesmo CST e Alíquota de PIS/Pasep e Cofins.
Exemplo: Considerando que determinada NFC-e emitida, contendo dezenas de itens/produtos diferentes em seu conteúdo apresente, por exemplo, 18 itens sujeitos à tributação às alíquotas básicas (CST 01) + 30 itens referentes a revenda de produtos sujeitos à alíquota zero (CST 06) + 05 cinco itens referentes a revenda de produtos sujeitos à substituição tributária de PIS/Pasep e Cofins (CST 05)  + 30 itens referentes a revenda de produtos sujeitos à tributação monofásica (CST 04), deve então a pessoa jurídica escriturar este documento em 01 (um) registro C100 e detalhar os valores dos itens contidos na NFC-e em 04 (quatro) registros C175, consolidando em cada registro C175 as receitas referentes ao cada CST.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos campos: CFOP, CST (PIS/Pasep e Cofins) e alíquotas (PIS/Pasep e Cofins).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C175” | C | 004* | - | S |
| 02 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 03 | VL_OPR | Valor da operação na combinação de CFOP, CST e alíquotas, correspondente ao somatório do valor das mercadorias e produtos constantes no documento. | N | - | 02 | S |
| 04 | VL_DESC | Valor do desconto comercial / exclusão da base de cálculo do PIS/PASEP e da COFINS | N | - | 02 | N |
| 05 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | N |
| 06 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP (em valor) | N | - | 02 | N |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 08 | QUANT_BC_PIS | Base de cálculo PIS/PASEP (em quantidade) | N | - | 03 | N |
| 09 | ALIQ_PIS_QUANT | Alíquota do PIS (em reais) | N | - | 04 | N |
| 10 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 11 | CST_COFINS | Código da Situação Tributária referente a Cofins, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 12 | VL_BC_COFINS | Valor da base de cálculo da Cofins | N | - | 02 | N |
| 13 | ALIQ_COFINS | Alíquota da Cofins (em percentual) | N | 008 | 04 | N |
| 14 | QUANT_BC_COFINS | Base de cálculo COFINS (em quantidade) | N | - | 03 | N |
| 15 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 16 | VL_COFINS | Valor da Cofins | N | - | 02 | N |
| 17 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 18 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações: Registro Filho de C100, para escrituração na visão analítica (similar ao registro C190, da EFD ICMS/IPI). A ser utilizado para a escrituração da NFC-e (código 65) segmentado por CST, CFOP e alíquotas do PIS/Pasep e da Cofins. Desta forma, para cada NFC-e escriturada no Registro C100, deve a pessoa jurídica proceder à escrituração analítica das receitas que a compõem, neste registro C175, conforme a classificação fiscal (Códigos de Situação Tributária – CST) destas receitas.
Nível hierárquico – 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C175]
Campo 02 - Preenchimento: informar neste campo o Código Fiscal de Operação – CFOP, relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01. Não devem ser relacionadas na consolidação operações que não se refiram a receitas auferidas de vendas, como no caso de transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica.
Na escrituração analítica das Notas Fiscais Eletrônicas ao Consumidor Final (NFC-e), só poderão ser informados CFOP iniciados com 5, conforme definido nas regras tanto da EFD-Contribuições como da EFD-ICMS/IPI.
Campo 03 - Preenchimento: informar o valor correspondente ao somatório do valor das mercadorias e produtos constantes na NFC-e, que correspondam à mesma combinação de CFOP, CST (PIS/Pasep e Cofins) e alíquotas (PIS/Pasep e Cofins).
Campo 04 - Preenchimento: informar o valor do desconto comercial / exclusões da base de cálculo das contribuições sociais, como por exemplo, os descontos incondicionais concedidos. Para mais informações sobre os efeitos das decisões judiciais e operacionalização de eventuais ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 05 - Preenchimento: informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. Os códigos são os constantes da Tabela 4.3.3 da escrituração.
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

Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à combinação de CFOP, CST e alíquotas, objeto de consolidação neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem (em percentual) aplicável para fins de apuração da contribuição para o PIS/Pasep, conforme o caso.
Campo 08 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de venda mediante emissão de NFC-e por fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 08 (base de cálculo em quantidade) dispensa o preenchimento do campo 06 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 09 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 08).
Campo 10 – Preenchimento: informar o valor do PIS/Pasep referente ao valor analítico consolidado/informado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610..
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 06 ou campo 08) multiplicado pela alíquota aplicável ao item (campo 07 ou campo 09). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 06 (VL_BC_PIS) = 1.000.000,00 e o Campo 07 (ALIQ_PIS) = 1,6500, então o Campo 10 (VL_PIS) será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 11 - Preenchimento: Informar neste campo o Código de Situação Tributária referente à Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. Os códigos são os constantes da Tabela 4.3.4 da escrituração.
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

Campo 12 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à combinação de CFOP, CST e alíquotas, objeto de consolidação neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 13 - Preenchimento: informar neste campo o valor da alíquota ad valorem (em percentual) aplicável para fins de apuração da Cofins, conforme o caso.
Campo 14 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de venda mediante emissão de NFC-e por fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 08 (base de cálculo em quantidade) dispensa o preenchimento do campo 06 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 15 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 14).
Campo 16 – Preenchimento: informar o valor da Cofins referente ao valor analítico consolidado/informado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição e/ou do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500 e VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 12 ou campo 14) multiplicado pela alíquota aplicável ao item (campo 13 ou campo 15). No caso de aplicação da alíquota do campo 13, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 12 (VL_BC_COFINS) = 1.000.000,00 e o Campo 13 (ALIQ_PIS) = 7,600, então o Campo 16 (VL_COFINS) será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 17 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas tributadas, receitas de vendas não tributadas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 19 - Preenchimento: Campo de preenchimento opcional, a ser utilizado para prestar informações complementares às operações relacionadas neste registro.
<!-- End Registro C175 -->
<!-- Start Registro C180 -->
Registro C180: Consolidação de Notas Fiscais Eletrônicas Emitidas Pela Pessoa Jurídica (Códigos 55 e 65) – Operações de Vendas
Este registro deve ser preenchido para consolidar as operações de vendas realizadas pela pessoa jurídica, por item vendido (Registro 0200), mediante emissão de NF-e (Modelo 55) e NFC-e (modelo 65). No caso das receitas auferidas por NFC-e, só podem ser consolidadas as operações no registro C180 se o arquivo txt ultrapassar o tamanho equivalente a 1GB caso a escrituração das vendas por NFC-e fosse realizada de forma individualizada em C100/C175. Além disso, todos estabelecimentos emissores de NFC-e devem estar obrigados à escrituração de suas operações de forma individualizada na EFD ICMS-IPI.
Excepcionalidade da escrituração da NFC-e (código 65): Para os fatos geradores ocorridos até agosto de 2014, a escrituração das receitas auferidas mediante a emissão de NFC-e se fará de forma consolidada no registro C180, identificando no Campo “COD_ITEM” do referido registro a codificação adotada no registro “0200” para a receita auferida com esses documentos. Como o campo 02 (COD_MOD) só valida o código “55”, a identificação das receitas decorrentes da emissão de NFC-e se fará na codificação do registro “0200”, assim, no registro C180, deve ser informado no campo 02 o código “55”, mesmo se tratando de receita decorrente de emissão de NFC-e.
IMPORTANTE:
A pessoa jurídica ao escriturar a consolidação de suas vendas no registro C180 deve atentar que:
1. A escrituração da consolidação de vendas por Nota Fiscal eletrônica (NF-e), no Registro C180 (Visão consolidada das vendas, por item vendido), dispensa a escrituração individualizada das vendas do período, por documento fiscal, no Registro C100 e registros filhos.
2. Não devem ser incluídos na consolidação do Registro C180 e registros filhos (C181 e C185) os documentos fiscais que não correspondam a receitas efetivamente auferidas, tais como as notas fiscais eletrônicas canceladas, as notas fiscais eletrônicas denegadas ou de numeração inutilizada e as notas fiscais referentes a transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica, etc.
Devem integrar o faturamento e ser relacionadas na consolidação as notas fiscais de venda de mercadorias, bens e produtos emitidos no período e que sejam objeto de devolução (devolução de vendas). Caso a receita da venda objeto de devolução seja tributada no regime não cumulativo, poderá a empresa apurar créditos em relação às devoluções nos termos do art. 3º, inciso VIII, das Leis nº 10.637/2002 (PIS/Pasep) e nº 10.833/2003 (Cofins). Caso a receita seja tributada no regime cumulativo, poderá a empresa excluir o seu valor da base de cálculo da contribuição cumulativa, nos termos da Lei nº 9.718/98.
3. Não devem ser relacionados nesse registro os documentos fiscais representativos das seguintes operações geradoras de receitas, com incidência ou não de contribuição social:
Fornecimento de Energia Elétrica (documento fiscal, códigos 06 ou 55). Os documentos fiscais relativos à energia elétrica devem ser escriturados no registro C600;
Prestação de serviços de transportes (documentos fiscais códigos 07, 08, 8B, 09, 10, 11, 26, 27 e 57). Os referidos documentos fiscais relativos a serviços de transportes devem ser escriturados no registro D200;
Prestação de serviços de transporte de passageiros – Bilhetes de Passagem (documentos fiscais códigos 2E, 13, 14, 15, 16 e 18). Os referidos documentos fiscais relativos a serviços de transporte de passageiros devem ser escriturados nos registros D300 ou D350 (bilhete emitido por ECF);
Prestação de serviços de comunicação e telecomunicação (documentos fiscais códigos 21 e 22). Os referidos documentos fiscais relativos a serviços de comunicação e telecomunicação devem ser escriturados no registro D600;
Fornecimento de água canalizada ou gás (documentos fiscais códigos 28 e 29). Os documentos fiscais relativos a água canalizada e gás devem ser escriturados no registro C600;
Cupom Fiscal (documentos fiscais códigos 02, 2D e 59). Os documentos fiscais relativos Cupom Fiscal devem ser escriturados nos registros C400 (informação por ECF) ou C490 (informação consolidada).
4. No caso de mudança de alíquota, CST ou CFOP no transcurso do período de apuração, resultando assim em mais de um tratamento tributário dentro do próprio mês, poderá a pessoa jurídica gerar um registro C180 para cada período objeto de tratamento tributário específico.
Exemplo: Considerando que o Decreto nº 7.455/2011 estabeleceu novas alíquotas para os fabricantes de cervejas e refrigerantes, com vigência a partir de 04 de abril de 2011, a empresa fabricante de cervejas ou refrigerantes procederá à escrituração de um Registro C180 para o período de 01 a 03 de abril de 2011 e outro registro C180 para o período de 04 a 30 de abril de 2011.
5. Na escrituração das receitas de vendas consolidadas (por item) neste registro, para os fatos geradores ocorridos a partir de 1º de maio de 2015, referente às bebidas frias de que trata os art. 14 a 34 da Lei nº 13.097/2015, deve a pessoa jurídica observar as orientações constantes na Nota Técnica nº 005, de 07 de maio de 2015, publicada no Portal do Sped (área da EFD-Contribuições), no sitio da Secretaria da Receita Federal do Brasil.
OPERAÇÕES COM SUBSTITUIÇÃO TRIBUTÁRIA DO PIS/PASEP E DA COFINS - ORIENTAÇÕES DE ESCRITURAÇÃO PELA PESSOA JURÍDICA FABRICANTE:
1. Procedimento de escrituração da substituição tributária de cigarros e cigarrilhas:
Tributação definida em recolhimento único, tendo por alíquota aplicável a alíquota básica definida para o regime cumulativo (0,65% e 3%). Desta forma, a pessoa jurídica fabricante, responsável pelo recolhimento como contribuinte e como substituto tributário, poderá registrar as vendas correspondentes, considerando o CST 01 (Operação tributável com alíquota básica) ou CST 05 (Operação tributável por substituição tributária). Independente do CST informado, a Receita Federal identificará a natureza da operação, em função da NCM e CFOP informados nos registros representativos das correspondentes operações;
2. Procedimento de escrituração da substituição tributária de motocicletas e máquinas agrícolas - Art. 43 da MP nº 2.158-31/2001:
Tributação definida em recolhimentos separados (dois recolhimentos) por parte do fabricante, como contribuinte e como substituto tributário, tendo por alíquota aplicável a alíquota básica definida para o regime cumulativo. Desta forma, a pessoa jurídica fabricante, responsável pelos dois recolhimentos, como contribuinte e como substituto tributário, poderá registrar as vendas correspondentes, no registro C170 ou C180 (e registros filhos) utilizando registros diferentes para cada recolhimento:
- No caso de escrituração por documento fiscal (C100), deverá ser escriturado 01 (um) registro C170 específico para informar a tributação como contribuinte (CST 01) e 01 (um) registro C170 específico para informar a tributação do outro recolhimento, como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração do registro C170 representativo da ST, informar valor zero no campo 07 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição;
- No caso de escrituração consolidada das receitas (C180), deverá ser escriturado 01 (um) registro C181/C185 específico para informar a tributação como contribuinte (CST 01) e 01 (um) registro C181/C185 específico para informar a tributação do outro recolhimento, como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração dos registros representativos da ST, informar valor zero no campo 04 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição.
3. Procedimento de escrituração da substituição tributária da venda de produtos monofásicos à ZFM - Arts. 64 e 65 da Lei nº 11.196/2005:
Tributação definida em recolhimento único, tendo por alíquota monofásicas, relacionadas nas tabelas 4.3.10 e 4.3.11, conforme o produto. Nesse regime de tributação por ST, aplicável a esses produtos, a tributação da operação no fabricante, como contribuinte está tributada com alíquota zero (CST 06) e, na condição de substituto, tributada com CST 05. Desta forma, a pessoa jurídica fabricante, responsável pelo recolhimento como substituto tributário, poderá registrar as vendas correspondentes, no registro C170 ou C180 (e registros filhos) utilizando registros diferentes para cada situação:
- No caso de escrituração por documento fiscal (C100), deverá ser escriturado 01 (um) registro C170 específico para informar a tributação à alíquota zero como contribuinte (CST 06) e 01 (um) registro C170 específico para informar a tributação do recolhimento como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração do registro C170 representativo da ST, informar valor zero no campo 07 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição;
- No caso de escrituração consolidada das receitas (C180), deverá ser escriturado 01 (um) registro C181/C185 específico para informar a tributação à alíquota zero como contribuinte (CST 06) e 01 (um) registro C181/C185 específico para informar a tributação do recolhimento como substituto tributário. Para tanto, deverá a empresa, em relação à escrituração dos registros representativos da ST, informar valor zero no campo 04 (VL_ITEM), no sentido de evitar que a receita fique duplicada na escrituração, informando assim os campos de base de cálculo, alíquota e valor da contribuição.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C180” | C | 004* | - | S |
| 02 | COD_MOD | Texto fixo contendo "55" ou “65”(Código da NF-e ou da NFC-e, conforme a Tabela 4.1.1) | C | 002* | - | S |
| 03 | DT_DOC_INI | Data de Emissão Inicial dos Documentos | N | 008* | - | S |
| 04 | DT_DOC_FIN | Data de Emissão Final dos Documentos | N | 008* | - | S |
| 05 | COD_ITEM | Código do Item (campo 02 do Registro 0200) | C | 060 | - | S |
| 06 | COD_NCM | Código da Nomenclatura Comum do Mercosul | C | 008* | - | N |
| 07 | EX_IPI | Código EX, conforme a TIPI | C | 003 | - | N |
| 08 | VL_TOT_ITEM | Valor Total do Item | N | - | 02 | S |

Observações: Os valores consolidados por item vendido (bens ou serviços, no caso de nota conjugada) serão segregados e totalizados, nos registros filhos (C181 e C185), por CST-PIS (Tabela 4.3.3), CST-Cofins (Tabela 4.3.4), CFOP e alíquotas.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [C180]
Campo 02 - Valor Válido: [55,65]
Campo 03 - Preenchimento: informar a data de referência inicial dos documentos consolidados no registro, representativos de operações de vendas, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 04 - Preenchimento: informar a data de referência Final dos documentos consolidados no registro, representativos de operações de vendas, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 05 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 06 – Preenchimento: Informar neste campo o código NCM, conforme a Nomenclatura Comum do MERCOSUL, de acordo com o Decreto nº 6.006/06.
A identificação do NCM é determinante para validar a incidência ou não das contribuições sociais, confrontando e cruzando com as informações de CST, CFOP, base de cálculo e alíquotas informadas nos registros de detalhamento “C181” e “C185”
O campo NCM é de preenchimento obrigatório no registro C180, para as seguintes situações:
Empresas industriais e equiparadas a industrial, referente aos itens correspondentes às suas atividades fins;
Pessoas jurídicas, inclusive cooperativas, que produzam mercadorias de origem animal ou vegetal (agroindústria), referente aos itens correspondentes às atividades geradoras de crédito presumido;
Empresas que realizarem operações de exportação ou importação;
Empresas atacadistas ou industriais, referentes aos itens representativos de vendas no mercado interno com alíquota zero, suspensão, isenção ou não incidência, nas situações em que a legislação tributária atribua o benefício a um código NCM específico.
Atenção: A partir da versão 2.1.1 do PVA da EFD-Contribuições, disponibilizada em agosto de 2017, o campo de NCM passa a ser obrigatório e, no caso do item se referir a serviços, conforme cadastro em 0200, poderá ser utilizado o código "00".
Campo 07 - Preenchimento: informar com o Código de Exceção de NCM, de acordo com a Tabela de Incidência do Imposto sobre Produtos Industrializados (TIPI), quando existir.
Campo 08 – Preenchimento:  Informar neste campo o valor total dos documentos fiscais (NF-e) consolidados neste registro.
Esclarecimentos adicionais quanto às operações de Vendas Canceladas, Retorno de Mercadorias e Devolução de Vendas:
Se a empresa está escriturando por documento, em C100, as vendas canceladas deve assim ser tratada:
1. Se o cancelamento se deu no próprio mês da emissão do documento, a empresa tem a opção de não relacionar na escrituração este documento ou, vindo a relacioná-lo, o fazer com as informações solicitadas para C100, mas sem gerar os registros filhos (C170);
2. Se o cancelamento se deu em período posterior ao de sua emissão, devendo assim ser considerado na redução da base de cálculo do período em que ocorreu o cancelamento, a empresa pode proceder à escrituração destes valores redutores da base de cálculo do mês do cancelamento, mediante a geração de registros de ajustes de débitos, em M220 (PIS) e M620 (Cofins), fazendo constar nestes registros de ajustes o montante da contribuição a ser reduzida, em decorrência do(s) cancelamentos em questão. Para os fatos geradores ocorridos a partir de janeiro/2019, os ajustes da base de cálculo do período em que ocorreu o cancelamento devem ser realizados, preferencialmente, nos campos próprios dos registros M210 (PIS - Campo 06 - VL_AJUS_REDUC_BC_PIS) e M610 (Cofins - Campo 06 - VL_AJUS_REDUC_BC_COFINS). Neste caso, o detalhamento do ajuste será informado nos registros M215 (PIS) e M615 (Cofins), respectivamente, preenchendo o campo COD_AJ_BC com o código 01 - Vendas canceladas de receitas tributadas em períodos anteriores - da tabela 4.3.18.
A operação de retorno de produtos ao estabelecimento emissor da nota fiscal, conforme previsão existente no RIPI/2010 (art. 234 do Decreto Nº 7.212, de 2010) e no Convênio SINIEF SN, de 1970 (Capítulo VI, Seção II – Da Nota Fiscal), para fins de escrituração de PIS/COFINS deve receber o tratamento de cancelamento de venda (não integrando a base de cálculo das contribuições nem dos créditos).
Registre-se que a venda cancelada é hipótese de exclusão da base de cálculo da contribuição (em C170, no caso de escrituração individualizada por documento fiscal ou em C181 (PIS/Pasep) e C185 (Cofins)), tanto no regime de incidência cumulativo como no não cumulativo.
A nota fiscal de entrada da mercadoria retornada, emitida pela própria pessoa jurídica, pode ser relacionada nos registros consolidados C190 e filhos (Operações de aquisição com direito a crédito, e operações de devolução de compras e vendas) ou nos registros individualizados C100 e filhos, somente para fins de maior transparência da apuração, visto não configurar hipótese legal de creditamento de PIS/COFINS. Neste caso, utilize o CST 98 ou 99.
Já as operações de Devolução de Vendas, no regime de incidência não cumulativo, correspondem a hipóteses de crédito, devendo ser escrituradas com os CFOP correspondentes em C170 (no caso de escrituração individualizada dos créditos por documento fiscal) ou nos registros C191/C195 (no caso de escrituração consolidada dos créditos), enquanto que, no regime cumulativo, tratam-se de hipótese de exclusão da base de cálculo da contribuição.
Dessa forma, no regime cumulativo, caso a operação de venda a que se refere o retorno tenha sido tributada para fins de PIS/COFINS, a receita da operação deverá ser excluída da apuração:
1. Caso a pessoa jurídica esteja utilizando os registros consolidados C180 e filhos (Operações de Vendas), não deverá incluir esta receita na base de cálculo das contribuições nos registros C181 e C185.
2. Caso a pessoa jurídica esteja utilizando os registros C100 e filhos, deverá incluir a nota fiscal de saída da mercadoria com a base de cálculo zerada, devendo constar no respectivo registro C110 a informação acerca do retorno da mercadoria, conforme consta no verso do documento fiscal ou do DANFE (NF-e).
Caso não seja possível proceder estes ajustes diretamente no bloco C, a pessoa jurídica deverá proceder aos ajustes diretamente no bloco M, nos respectivos campos e registros de ajustes de redução de contribuição (M220 e M620). Neste caso, deverá utilizar o campo “NUM_DOC” e “DESCR_AJ” para relacionar as notas fiscais de devolução de vendas, como ajuste de redução da contribuição cumulativa. Para os fatos geradores ocorridos a partir de janeiro/2019, caso não seja possível proceder estes ajustes de base de cálculo diretamente no bloco C, os mesmos devem ser realizados, preferencialmente, nos campos próprios dos registros M210 (PIS - Campo 06 - VL_AJUS_REDUC_BC_PIS) e M610 (Cofins - Campo 06 - VL_AJUS_REDUC_BC_COFINS). Caso não seja possível proceder estes ajustes diretamente no bloco C, a pessoa jurídica deverá proceder aos ajustes diretamente no bloco M, nos respectivos campos e registros de ajustes de redução de contribuição (M220 e M620). Neste caso, deverá utilizar o campo “NUM_DOC” e “DESCR_AJ” para relacionar as notas fiscais de devolução de vendas, como ajuste de redução da contribuição cumulativa. Para os fatos geradores ocorridos a partir de janeiro/2019, caso não seja possível proceder estes ajustes de base de cálculo diretamente no bloco C, os mesmos devem ser realizados, preferencialmente, nos campos próprios dos registros M210 (PIS - Campo 06 - VL_AJUS_REDUC_BC_PIS) e M610 (Cofins - Campo 06 - VL_AJUS_REDUC_BC_COFINS). Neste caso, o detalhamento do ajuste será informado nos registros M215 (PIS) e M615 (Cofins), respectivamente, preenchendo o campo COD_AJ_BC com o código 02 - Devoluções de vendas tributadas em períodos anteriores - da tabela 4.3.18.
Mesmo não gerando direito a crédito no regime cumulativo, a nota fiscal de devolução de bens e mercadorias pode ser informada nos registros consolidados C190 e filhos, ou C100 e filhos, para fins de transparência na apuração. Nesse caso, deve ser informado o CST 98 ou 99, visto que a devolução de venda no regime cumulativo não gera crédito.
<!-- End Registro C180 -->
<!-- Start Registro C181 -->
Registro C181: Detalhamento da Consolidação – Operações de Vendas – PIS/Pasep
Registro obrigatório, para fins de detalhamento por CST, CFOP e Alíquotas, dos valores consolidados de PIS/Pasep referentes a cada item objeto de venda por Nota Fiscal Eletrônica – NF-e.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C181” | C | 004* | - | S |
| 02 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 03 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 04 | VL_ITEM | Valor do item | N | - | 02 | S |
| 05 | VL_DESC | Valor do desconto comercial / exclusão da base de cálculo | N | - | 02 | N |
| 06 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 08 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS/PASEP | N | - | 03 | N |
| 09 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 10 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 11 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Deve ser informado um registro C181 para cada CST, CFOP ou Alíquotas, referentes às vendas do item no período da escrituração.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C181]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 03 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01. Não devem ser relacionadas na consolidação operações que não se refiram a receitas auferidas de vendas, como no caso de transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica.
Campo 04 - Preenchimento: informar o valor do item/produto consolidado neste registro.
Campo 05 - Preenchimento: informar o valor do desconto comercial ou dos valores a excluir da base de cálculo da contribuição, conforme o caso. Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item, para fins de apuração da contribuição social, conforme o caso.
Atenção: No caso de escrituração de receitas decorrentes da venda de bebidas frias, nos termos do art. 14 a 34 da Lei nº 13.097/2015, pelos fabricantes e atacadistas, o valor do frete integrará a base de cálculo da Contribuição para o PIS/Pasep e da Cofins apurada pela pessoa jurídica vendedora dos citados produtos, para os fatos geradores a partir de 01.05.2015. Desta forma, a partir de 01.01.2015, deve a pessoa jurídica acrescer ao valor do Campo 06, o valor do frete correspondente à venda.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 08 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 08 (base de cálculo em quantidade) dispensa o preenchimento do campo 06 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 09 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 08).
Campo 10 – Preenchimento: informar o valor do PIS/Pasep referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 06 ou campo 08) multiplicado pela alíquota aplicável ao item (campo 07 ou campo 09). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 06 (VL_BC_PIS) = 1.000.000,00 e o Campo 07 (ALIQ_PIS) = 1,6500, então o Campo 10 (VL_PIS) será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 11 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas financeiras, receitas não operacionais, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C181 -->
<!-- Start Registro C185 -->
Registro C185: Detalhamento da Consolidação – Operações de Vendas – Cofins
Registro obrigatório, para fins de detalhamento por CST, CFOP e Alíquotas, dos valores consolidados da Cofins referentes a cada item objeto de venda por Nota Fiscal Eletrônica – NF-e.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C185” | C | 004* | - | S |
| 02 | CST_COFINS | Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 03 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 04 | VL_ITEM | Valor do item | N | - | 02 | S |
| 05 | VL_DESC | Valor do desconto comercial / exclusão da base de cálculo | N | - | 02 | N |
| 06 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 07 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 08 | QUANT_BC_COFINS | Quantidade – Base de cálculo da COFINS | N | - | 03 | N |
| 09 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 10 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 11 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Deve ser informado um registro C181 para cada CST, CFOP ou Alíquotas, referentes às vendas do item no período da escrituração.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C185]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 03 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01. Não devem ser relacionadas na consolidação operações que não se refiram a receitas auferidas de vendas, como no caso de transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica.
Campo 04 - Preenchimento: informar o valor do item/produto consolidado neste registro.
Campo 05 - Preenchimento: informar o valor do desconto comercial ou dos valores a excluir da base de cálculo da contribuição, conforme o caso. Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item, para fins de apuração da contribuição social, conforme o caso.
Atenção: No caso de escrituração de receitas decorrentes da venda de bebidas frias, nos termos do art. 14 a 34 da Lei nº 13.097/2015, pelos fabricantes e atacadistas, o valor do frete integrará a base de cálculo da Contribuição para o PIS/Pasep e da Cofins apurada pela pessoa jurídica vendedora dos citados produtos, para os fatos geradores a partir de 01.05.2015. Desta forma, a partir de 01.01.2015, deve a pessoa jurídica acrescer ao valor do Campo 06, o valor do frete correspondente à venda.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 08 - Preenchimento: informar neste campo a base de cálculo da cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 08 (base de cálculo em quantidade) dispensa o preenchimento do campo 06 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 09 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 08).
Campo 10 – Preenchimento: informar o valor da Cofins referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 06 ou campo 08) multiplicado pela alíquota aplicável ao item (campo 07 ou campo 09). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 06 (VL_BC_COFINS) = 1.000.000,00 e o Campo 07 (ALIQ_COFINS) = 7,6000, então o Campo 10 (VL_COFINS) será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 11 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas financeiras, receitas não operacionais, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C185 -->
<!-- Start Registro C188 -->
Registro C188: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a  existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “C188”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C188" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 - Secretaria da Receita Federal do Brasil; 9 – Outros. | C | 001* | - | S |

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
Campo 01 - Valor Válido: [C188]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C188 -->
<!-- Start Registro C190 -->
Registro C190: Consolidação de Notas Fiscais Eletrônicas (Código 55) – Operações de Aquisição com Direito a Crédito, e Operações de Devolução de Compras e Vendas.
Este registro deve ser preenchido para consolidar as operações de aquisições ou devoluções de vendas realizadas pela pessoa jurídica, por item vendido (Registro 0200), mediante emissão de NF-e (Modelo 55), no período da escrituração, com direito à apuração de crédito.
IMPORTANTE: A pessoa jurídica ao escriturar a consolidação de suas aquisições com crédito e/ou devoluções, no registro C190, deve atentar que:
1. A escrituração da consolidação de vendas por Nota Fiscal eletrônica (NF-e), no Registro C190 (Visão consolidada das aquisições e devoluções com direito a crédito, por item vendido), dispensa a escrituração individualizada das aquisições do período, por documento fiscal, no Registro C100 e registros filhos.
2. Não devem ser incluídos na consolidação do Registro C190 e registros filhos (C191 e C195) os documentos fiscais que não correspondam a aquisições com direito a crédito ou a devoluções (devoluções de vendas), bem como as notas fiscais eletrônicas canceladas, as notas fiscais eletrônicas denegadas ou de numeração inutilizada e as notas fiscais referentes a transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica, etc.
3. Não devem ser relacionados neste registro os documentos fiscais representativos das seguintes operações geradoras de crédito:
Aquisição de bens a serem incorporados ao ativo imobilizado, cujo crédito for determinado com base no valor de aquisição e/ou com base nos encargos mensais de depreciação. O detalhamento do crédito com base nos encargos de depreciação deverá ser feito no registro F120. Caso o crédito seja apurado com base no valor de aquisição deverá ser informado no registro F130.
Caso a pessoa jurídica venha a proceder neste registro à escrituração da aquisição de bens a serem incorporados ao ativo imobilizado, objeto de crédito mediante a escrituração do Registro F120 (com base no encargo de depreciação) ou  do Registro F130 (com base no valor de aquisição), deverá informar nos registros filhos C191 (PIS/Pasep) e C195 (Cofins) o CST “98” ou “99”;
Aquisição de Energia Elétrica (documento fiscal códigos 06 ou 55). Os documentos fiscais relativos à aquisição de energia elétrica devem ser escriturados nos registros C500;
Aquisição de serviços de transportes (documentos fiscais códigos 07, 08, 8B, 09, 10, 11, 26, 27 e 57). Os referidos documentos fiscais relativos à aquisição de serviços de transportes devem ser escriturados no registro D100;
Aquisição de serviços de transporte de passageiros – Bilhetes de Passagem (documentos fiscais códigos 2E, 13, 14, 15, 16 e 18). Os referidos documentos fiscais relativos à aquisição de serviços de transporte de passageiros devem ser escriturados nos registros D300 ou D350 (bilhete emitido por ECF);
Aquisição de serviços de comunicação e telecomunicação (documentos fiscais códigos 21 e 22). Os referidos documentos fiscais relativos a serviços de comunicação e telecomunicação devem ser escriturados nos registros D500;
Aquisição de água canalizada ou gás (documentos fiscais códigos 28 e 29). Os documentos fiscais relativos a água canalizada e gás devem ser escriturados no registro C500;
Cupom Fiscal (documentos fiscais códigos 02, 2D e 59). Os documentos fiscais relativos Cupom Fiscal devem ser escriturados nos registros C400 (informação por ECF) ou C490 (informação consolidada).
Devem também serem relacionadas neste registro as operações de devoluções de compras que, quando da aquisição, geraram créditos da não cumulatividade. Os valores relativos às devoluções de compras, com crédito apurado na aquisição, devem ser escriturados pela pessoa jurídica, no mês da devolução, e os valores dos créditos  correspondentes a serem anulados/estornados, devem ser informados como “Ajuste de Redução” no campo 10 dos registros M100 (PIS/Pasep) e M500 (Cofins), bem como nos registros filhos de detalhamento de ajustes (M110/M510).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C190” | C | 004* | - | S |
| 02 | COD_MOD | Texto fixo contendo "55" (Código da Nota Fiscal Eletrônica, modelo 55, conforme a Tabela 4.1.1) | C | 002* | - | S |
| 03 | DT_REF_INI | Data Inicial de Referência da Consolidação | N | 008* | - | S |
| 04 | DT_REF_FIN | Data Final de Referência da Consolidação | N | 008* | - | S |
| 05 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | S |
| 06 | COD_NCM | Código da Nomenclatura Comum do Mercosul | C | 008* | - | N |
| 07 | EX_IPI | Código EX, conforme a TIPI | C | 003 | - | N |
| 08 | VL_TOT_ITEM | Valor Total do Item | N | - | 02 | S |

Observações: Os valores consolidados por item adquirido (bens ou serviços, no caso de nota conjugada), ou devoluções, serão segregados e totalizados, nos registros filhos (C191 e C195), por CST-PIS (Tabela 4.3.3), CST-Cofins (Tabela 4.3.4), CFOP e alíquotas.
Nível hierárquico - 3
Ocorrência –1:N
Campo 01 - Valor Válido: [C190]
Campo 02 - Valor Válido: [55]
Campo 03 - Preenchimento: informar a data de referência inicial dos documentos consolidados no registro, ou seja, a data do documento com emissão mais antiga, representativos de operações de aquisição ou devolução, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 04 - Preenchimento: informar a data de referência final dos documentos consolidados no registro, ou seja, a data do documento com emissão mais atual, representativos de operações de aquisição ou devolução, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 05 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200. Atentar para a premissa de que a informação deve ser prestada pela ótica da pessoa jurídica titular da escrituração, ou seja, nas operações de entradas de mercadorias, os códigos informados devem ser os definidos pelo próprio informante e não aqueles constantes do documento fiscal.
Campo 06 – Preenchimento: Informar neste campo o código NCM, conforme a Nomenclatura Comum do MERCOSUL, de acordo com o Decreto nº 6.006/06.
A identificação do NCM é determinante para validar a incidência ou não das contribuições sociais, confrontando e cruzando com as informações de CST, CFOP, base de cálculo e alíquotas informadas nos registros de detalhamento “C191” e “C195”
O campo NCM é de preenchimento obrigatório no registro C190, para as seguintes situações:
as empresas industriais e equiparadas a industrial, referente aos itens correspondentes às suas atividades fins;
as pessoas jurídicas, inclusive cooperativas, que produzam mercadorias de origem animal ou vegetal (agroindústria), referente aos itens correspondentes às atividades geradoras de crédito presumido;
as empresas que realizarem operações de exportação ou importação;
as empresas atacadistas ou industriais, referentes aos itens representativos de vendas no mercado interno com alíquota zero, suspensão, isenção ou não incidência, nas situações em que a legislação tributária atribua o benefício a um código NCM específico.
Atenção: A partir da versão 2.1.1 do PVA da EFD-Contribuições, disponibilizada em agosto de 2017, o campo de NCM passa a ser obrigatório e, no caso do item se referir a serviços, conforme cadastro em 0200, poderá ser utilizado o código "00".
Campo 07 - Preenchimento: informar com o Código de Exceção de NCM, de acordo com a Tabela de Incidência do Imposto sobre Produtos Industrializados (TIPI), quando existir.
Campo 08 – Preenchimento:  Informar neste campo o valor total dos documentos fiscais (NF-e) consolidados neste registro.
Esclarecimentos adicionais quanto às operações a serem escrituradas nesse registro:
I – Vendas Canceladas, Retorno de Mercadorias e Devolução de Vendas.
A operação de retorno de produtos ao estabelecimento emissor da nota fiscal, conforme previsão existente no RIPI/2010 (art. 234 do Decreto Nº 7.212, de 2010), para fins de escrituração de PIS/COFINS deve receber o tratamento de cancelamento de venda (não integrando a base de cálculo das contribuições).
Registre-se que a venda cancelada é hipótese de exclusão da base de cálculo da contribuição (em C170, no caso de escrituração individualizada por documento fiscal ou em C181 (PIS/Pasep) e C185 (Cofins)), tanto no regime de incidência cumulativo como no não cumulativo.
Já as operações de Devolução de Vendas, no regime de incidência não cumulativo, correspondem a hipóteses de crédito, devendo ser escrituradas com os CFOP correspondentes em C170 (no caso de escrituração individualizada dos créditos por documento fiscal) ou nos registros C191/C195 (no caso de escrituração consolidada dos créditos), enquanto que, no regime cumulativo, tratam-se de  hipótese de exclusão da base de cálculo da contribuição.
Dessa forma, caso a operação de venda a que se refere o retorno tenha sido tributada para fins de PIS/COFINS, a receita da operação deverá ser excluída da apuração:
1. Caso a pessoa jurídica esteja utilizando os registros consolidados C180 e filhos (Operações de Vendas), não deve incluir esta receita na base de cálculo das contribuições nos registros C181 e C185.
2. Caso a pessoa jurídica esteja utilizando os registros C100 e filhos, deverá incluir a nota fiscal de saída da mercadoria com a base de cálculo zerada, devendo constar no respectivo registro C110 a informação acerca do retorno da mercadoria, conforme consta no verso do documento fiscal ou do DANFE (NFe).
No caso de devolução de venda no regime cumulativo, hipótese de exclusão de base de cálculo da contribuição, caso não seja possível proceder estes ajustes diretamente no bloco C (no caso da devolução ocorrer em período posterior ao da escrituração), a pessoa jurídica deverá proceder aos ajustes diretamente no bloco M, nos respectivos campos e registros de ajustes de redução de contribuição (M220 e M620). Neste caso, deverá utilizar o campo “NUM_DOC” e “DESCR_AJ” para relacionar as notas fiscais de devolução de vendas, como ajuste de redução da contribuição cumulativa. Para os fatos geradores ocorridos a partir de janeiro/2019, caso não seja possível proceder estes ajustes de base de cálculo diretamente no bloco C, os mesmos devem ser realizados, preferencialmente, nos campos próprios dos registros M210 (PIS - Campo 06 - VL_AJUS_REDUC_BC_PIS) e M610 (Cofins - Campo 06 - VL_AJUS_REDUC_BC_COFINS). Caso não seja possível proceder estes ajustes diretamente no bloco C, a pessoa jurídica deverá proceder aos ajustes diretamente no bloco M, nos respectivos campos e registros de ajustes de redução de contribuição (M220 e M620). Neste caso, deverá utilizar o campo “NUM_DOC” e “DESCR_AJ” para relacionar as notas fiscais de devolução de vendas, como ajuste de redução da contribuição cumulativa. Para os fatos geradores ocorridos a partir de janeiro/2019, caso não seja possível proceder estes ajustes de base de cálculo diretamente no bloco C, os mesmos devem ser realizados, preferencialmente, nos campos próprios dos registros M210 (PIS - Campo 06 - VL_AJUS_REDUC_BC_PIS) e M610 (Cofins - Campo 06 - VL_AJUS_REDUC_BC_COFINS). Neste caso, o detalhamento do ajuste será informado nos registros M215 (PIS) e M615 (Cofins), respectivamente, preenchendo o campo COD_AJ_BC com o código 02 - Devoluções de vendas tributadas em períodos anteriores - da tabela 4.3.18.
A nota fiscal de entrada da mercadoria retornada, emitida pela própria pessoa jurídica, não deverá ser relacionada nos registros consolidados C190 e filhos (Operações de aquisição com direito a crédito, e operações de devolução de compras e vendas) ou nos registros individualizados C100 e filhos, visto não configurar hipótese legal de creditamento de PIS/COFINS.
A devolução de venda tributada, por pessoa jurídica sujeita ao regime cumulativo deverá obedecer aos mesmos critérios, ou seja, de exclusão da base de cálculo, devendo proceder aos ajustes diretamente nos registros consolidados C180 e filhos ou no registro C100 e filhos. Mesmo não gerando direito a crédito, a nota fiscal de devolução pode ser informada nos registros consolidados C190 e filhos, ou C100 e filhos, para fins de transparência na apuração. Nesse caso, deve ser informado o CST 99, visto que a devolução de venda no regime cumulativo não gera crédito.
II – Devolução de Compras.
Os valores relativos às devoluções de compras, referentes a operações de aquisição com crédito da não cumulatividade, devem ser escriturados pela pessoa jurídica, no mês da devolução, e os valores dos créditos correspondentes a serem anulados/estornados, devem ser informados preferencialmente mediante ajuste na base de cálculo da compra dos referidos bens, seja nos registros C100/C170 (informação individualizada), seja nos registros C190 e filhos (informação consolidada).
Caso não seja possível proceder estes ajustes diretamente no bloco C (como no caso da devolução ocorrer em período posterior ao da escrituração), a pessoa jurídica poderá proceder aos ajustes diretamente no bloco M, nos respectivos campos (campo 10 dos registros M100 e M500) e o detalhamento nos registros de ajustes de crédito (M110 e M510). Neste caso, deverá utilizar o campo “NUM_DOC” e “DESCR_AJ” para relacionar as notas fiscais de devolução, como ajuste de redução de crédito.
Por se referir a uma operação de saída, a escrituração do documento fiscal referente à operação de devolução de compra deve ser informada com o CST 49.
<!-- End Registro C190 -->
<!-- Start Registro C191 -->
Registro C191: Detalhamento da Consolidação – Operações de Aquisição Com Direito a Crédito, e Operações de Devolução de Compras e Vendas – PIS/Pasep
Registro obrigatório, para fins de detalhamento por fornecedor, CST, CFOP e Alíquotas, dos valores consolidados de PIS/Pasep referentes a cada item objeto de aquisição e/ou devolução, por Nota Fiscal Eletrônica – NF-e.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C191” | C | 004* | - | S |
| 02 | CNPJ_CPF_PART | CNPJ/CPF do Participante a que se referem as operações consolidadas neste registro (pessoa jurídica ou pessoa física vendedora/remetente) | C | 014 | - | N |
| 03 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 04 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 05 | VL_ITEM | Valor do item | N | - | 02 | S |
| 06 | VL_DESC | Valor do desconto comercial / Exclusão | N | - | 02 | N |
| 07 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 08 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 09 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS/PASEP | N | - | 03 | N |
| 10 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 11 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 12 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Deve ser informado um registro C191 para cada CST, CFOP ou Alíquotas, referentes às aquisições e devoluções do item no período da escrituração.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C191]
Campo 02 - Preenchimento: Informar neste campo o CNPJ/CPF do Participante (Fornecedor) a que se referem as operações consolidadas neste registro (pessoa jurídica ou pessoa física vendedora/remetente). No caso de participante estrangeiro não ter cadastro no CNPJ/CPF, deixar o campo em branco.
Validação: O campo é de preenchimento obrigatório, exceto em operações com participantes estrangeiros (importação) não cadastrados no CNPJ/CPF, quando deverá estar em branco.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

| Código | Descrição |
| --- | --- |
| 50 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 51 | Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno |
| 52 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação |
| 53 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 54 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 55 | Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 56 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 60 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 61 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno |
| 62 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação |
| 63 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 64 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 65 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 66 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 70 | Operação de Aquisição sem Direito a Crédito |
| 71 | Operação de Aquisição com Isenção |
| 72 | Operação de Aquisição com Suspensão |
| 73 | Operação de Aquisição a Alíquota Zero |
| 73 | Operação de Aquisição a Alíquota Zero |
| 74 | Operação de Aquisição sem Incidência da Contribuição |
| 75 | Operação de Aquisição por Substituição Tributária |
| 98 | Outras Operações de Entrada |
| 99 | Outras Operações |

No caso de devolução de compras de mercadorias, serviços e produtos, cujas operações geraram créditos quando da aquisição, deve ser informado o CST “49 – Outras Operações de Saída”.
Campo 04 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP, relativo às operações de aquisição e/ou devolução consolidadas neste registro.
Deve ser ressaltado que na geração do registro M105 (Base de Cálculo do crédito de PIS/Pasep) pelo PVA, serão consideradas apenas as operações de aquisição de bens, mercadorias e serviços (nota conjugada, por exemplo) e devoluções de vendas relacionadas neste registro, cujos CST sejam representativos de operações com direito a crédito (CST 50 a 66) e cujo conteúdo do campo CFOP seja referentes a:
- Aquisição de bens para revenda: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Aquisição de bens utilizados como insumo: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Aquisição de serviços utilizados como insumo: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Devolução de vendas tributadas no regime não cumulativo: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Outras Operações com direito a créditos: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”.
OBS: A tabela “CFOP – Operações Geradoras de Crédito” está disponibilizada no Portal do Sped, no endereço eletrônico da Receita Federal do Brasil (http://www.receita.fazenda.gov.br).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01. Não devem ser relacionadas na consolidação operações que não se refiram a aquisições ou a devoluções de vendas, como no caso de transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica.
A informação do CFOP refere-se à operação do ponto de vista do contribuinte informante da escrituração, ou seja, nas suas aquisições/entradas de mercadorias ou serviços, o contribuinte deve indicar, neste campo, o CFOP de entrada (iniciado por 1, 2 ou 3), e não o CFOP (iniciado por 5, 6 ou 7) constante no documento fiscal que acobertou a operação a que se refere.
Os seguintes CFOP não devem ser utilizados na EFD, visto serem considerados títulos: 1000, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1900, 2000, 2100, 2150, 2200, 2250, 2300, 2350, 2400, 2500, 2550, 2600, 2900, 3000, 3100, 3200, 3250, 3300, 3350, 3500, 3550, 3650, 3900, 5000, 5100, 5150, 5200, 5250, 5300, 5350, 5400, 5450, 5500, 5550, 5600, 5650, 5900, 6000, 6100, 6150, 6200, 6250, 6300, 6350, 6400, 6500, 6550, 6600, 6650, 6900, 7000, 7100, 7200, 7250, 7300, 7350, 7500, 7550, 7650, 7900.
No tocante às operações de devolução de compras, com crédito apropriado na aquisição, deve a pessoa jurídica observar os esclarecimentos adicionais constantes no Campo 08 do Registro Pai C190.
Campo 05 - Preenchimento: informar o valor do item/produto consolidado neste registro.
Campo 06 - Preenchimento: informar o valor do desconto comercial ou dos valores a excluir da base de cálculo do crédito, conforme o caso, como por exemplo, o valor referente as devoluções de compras ocorridas no mês do respectivo item.
Campo 07 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item, para fins de apuração do crédito, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, Campo “VL_BC_PIS_TOT”).
Campo 08 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração do crédito de PIS/Pasep, conforme o caso.
Campo 09 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração de crédito, conforme as hipóteses previstas em lei, como por exemplo, no caso de importação de combustíveis e de bebidas frias (água, cerveja, refrigerantes) e de devolução de vendas dos referidos produtos quanto tributados por unidade de medida de produto.
O preenchimento do campo 09 (base de cálculo em quantidade) dispensa o preenchimento do campo 07 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, Campo “QUANT_BC_PIS_TOT”).
Campo 10 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração do crédito, sobre a base de cálculo expressa em quantidade (campo 09).
Campo 11 – Preenchimento: informar o valor do crédito de PIS/Pasep referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 07 ou campo 09) multiplicado pela alíquota aplicável ao item (campo 08 ou campo 10). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 07 (VL_BC_PIS) = 1.000.000,00 e o Campo 08 (ALIQ_PIS) = 1,6500, então o Campo 11 (VL_PIS) será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 12 - Preenchimento: informar o Código da Conta Analítica. Exemplos: aquisições de bens para revenda, aquisições de insumos para industrialização, devoluções de vendas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C191 -->
<!-- Start Registro C195 -->
Registro C195: Detalhamento da Consolidação - Operações de Aquisição Com Direito a Crédito, e Operações de Devolução de Compras e Vendas – Cofins
Registro obrigatório, para fins de detalhamento por fornecedor, CST, CFOP e Alíquotas, dos valores consolidados de Cofins referentes a cada item objeto de aquisição e/ou devolução, por Nota Fiscal Eletrônica – NF-e.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C195” | C | 004* | - | S |
| 02 | CNPJ_CPF_PART | CNPJ/CPF do Participante a que se referem as operações consolidadas neste registro (pessoa jurídica ou pessoa física vendedora/remetente) | C | 014 | - | N |
| 03 | CST_COFINS | Código da Situação Tributária referente a COFINS. | N | 002* | - | S |
| 04 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 05 | VL_ITEM | Valor do item | N | - | 02 | S |
| 06 | VL_DESC | Valor do desconto comercial / Exclusão | N | - | 02 | N |
| 07 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 08 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 09 | QUANT_BC_COFINS | Quantidade – Base de cálculo da COFINS | N | - | 03 | N |
| 10 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 11 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 12 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Deve ser informado um registro C195 para cada CST, CFOP ou Alíquotas, referentes às aquisições e devoluções do item no período da escrituração.
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [C195]
Campo 02 - Preenchimento: Informar neste campo o CNPJ/CPF do Participante (Fornecedor) a que se referem as operações consolidadas neste registro (pessoa jurídica ou pessoa física vendedora/remetente). No caso de participante estrangeiro não ter cadastro no CNPJ/CPF, deixar o campo em branco.
Validação: O campo é de preenchimento obrigatório, exceto em operações com participantes estrangeiros (importação) não cadastrados no CNPJ/CPF, quando deverá estar em branco.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

| Código | Descrição |
| --- | --- |
| 50 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 51 | Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno |
| 52 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação |
| 53 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 54 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 55 | Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 56 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 60 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 61 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno |
| 62 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação |
| 63 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 64 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 65 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 66 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 70 | Operação de Aquisição sem Direito a Crédito |
| 71 | Operação de Aquisição com Isenção |
| 72 | Operação de Aquisição com Suspensão |
| 73 | Operação de Aquisição a Alíquota Zero |
| 73 | Operação de Aquisição a Alíquota Zero |
| 74 | Operação de Aquisição sem Incidência da Contribuição |
| 75 | Operação de Aquisição por Substituição Tributária |
| 98 | Outras Operações de Entrada |
| 99 | Outras Operações |

Campo 04 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações de aquisição e/ou devolução consolidadas neste registro.
Deve ser ressaltado que na geração do registro M505 (Base de cálculo do crédito de Cofins) pelo PVA, serão consideradas apenas as operações de aquisição de bens, mercadorias e serviços (nota conjugada, por exemplo) e devoluções de vendas relacionadas neste registro, cujos CST sejam representativos de operações com direito a crédito (CST 50 a 66) e cujo conteúdo do campo CFOP seja referentes a:
- Aquisição de bens para revenda: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Aquisição de bens utilizados como insumo: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Aquisição de serviços utilizados como insumo: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Devolução de vendas tributadas no regime não cumulativo: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”;
- Outras Operações com direito a créditos: conforme CFOP relacionados na Tabela “CFOP – Operações Geradoras de Créditos”.
OBS: A tabela “CFOP – Operações Geradoras de Crédito” está disponibilizada no Portal do Sped, no endereço eletrônico da Receita Federal do Brasil (http://www.receita.fazenda.gov.br).
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01. Não devem ser relacionadas na consolidação operações que não se refiram a aquisições ou a devoluções de vendas, como no caso de transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica.
A informação do CFOP refere-se à operação do ponto de vista do contribuinte informante da escrituração, ou seja, nas suas aquisições/entradas de mercadorias ou serviços, o contribuinte deve indicar, neste campo, o CFOP de entrada (iniciado por 1, 2 ou 3), e não o CFOP (iniciado por 5, 6 ou 7) constante no documento fiscal que acobertou a operação a que se refere.
Os seguintes CFOP não devem ser utilizados na EFD, visto serem considerados títulos: 1000, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1900, 2000, 2100, 2150, 2200, 2250, 2300, 2350, 2400, 2500, 2550, 2600, 2900, 3000, 3100, 3200, 3250, 3300, 3350, 3500, 3550, 3650, 3900, 5000, 5100, 5150, 5200, 5250, 5300, 5350, 5400, 5450, 5500, 5550, 5600, 5650, 5900, 6000, 6100, 6150, 6200, 6250, 6300, 6350, 6400, 6500, 6550, 6600, 6650, 6900, 7000, 7100, 7200, 7250, 7300, 7350, 7500, 7550, 7650, 7900.
No tocante às operações de devolução de compras, com crédito apropriado na aquisição, deve a pessoa jurídica observar os esclarecimentos adicionais constantes no Campo 08 do Registro Pai C190.
Campo 05 - Preenchimento: informar o valor do item/produto consolidado neste registro.
Campo 06 - Preenchimento: informar o valor do desconto comercial ou dos valores a excluir da base de cálculo do crédito, conforme o caso, como por exemplo o valor referente as devoluções de compras ocorridas no mês do respectivo item.
Campo 07 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item, para fins de apuração do crédito, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de Cofins (M505, Campo “VL_BC_COFINS_TOT”).
Campo 08 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração do crédito de Cofins, conforme o caso.
Campo 09 - Preenchimento: informar neste campo a base de cálculo de Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração de crédito, conforme as hipóteses previstas em lei, como por exemplo, no caso de importação de combustíveis e de bebidas frias (água, cerveja, refrigerantes) e de devolução de vendas dos referidos produtos quanto tributados por unidade de medida de produto.
O preenchimento do campo 09 (base de cálculo em quantidade) dispensa o preenchimento do campo 07 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de Cofins (M505, Campo “QUANT_BC_COFINS_TOT”).
Campo 10 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração do crédito, sobre a base de cálculo expressa em quantidade (campo 09).
Campo 11 – Preenchimento: informar o valor do crédito de Cofins referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 07 ou campo 09) multiplicado pela alíquota aplicável ao item (campo 08 ou campo 10). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 07 (VL_BC_COFINS) = 1.000.000,00 e o Campo 08 (ALIQ_COFINS) = 7,6000, então o Campo 11 (VL_COFINS) será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 12 - Preenchimento: informar o Código da Conta Analítica. Exemplos: aquisições de bens para revenda, aquisições de insumos para industrialização, devoluções de vendas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C195 -->
<!-- Start Registro C198 -->
Registro C198: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “C198”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referente ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C198" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - | S |

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
Campo 01 - Valor Válido: [C198]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C198 -->
<!-- Start Registro C199 -->
Registro C199: Complemento do Documento - Operações de Importação (Código 55)
Este registro tem por objetivo informar detalhes das operações de importação, que estejam sendo documentadas de forma consolidada no registro C190 (registro consolidado das aquisições por NF-e, código 55), quando no Campo 03 dos registros C191 e C195 conste CST_PIS ou CST_COFINS gerador de crédito (CST 50 a 56) e, no Campo 04, conste CFOP próprio de operações de importação (CFOP iniciado em 3).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C199" | C | 004* | - | S |
| 02 | COD_DOC_IMP | Documento de importação: 0 – Declaração de Importação; 1 – Declaração Simplificada de Importação;  A partir dos fatos geradores ocorridos em 01/2019: Documento de importação: 0 – Declaração de Importação; 1 – Declaração Simplificada de Importação; 2 – Declaração Única de Importação | C | 001* | - | S |
| 03 | NUM_DOC__IMP | Número do documento de Importação. | C | 015 | - | S |
| 04 | VL_PIS_IMP | Valor pago de PIS na importação | N | - | 02 | N |
| 05 | VL_COFINS_IMP | Valor pago de COFINS na importação | N | - | 02 | N |
| 06 | NUM_ACDRAW | Número do Ato Concessório do regime Drawback | C | 020 | - | N |

Observações:
1. Caso a pessoa jurídica tenha importado mercadorias, bens e produtos de pessoa física ou jurídica domiciliada no exterior, com direito a crédito na forma prevista na Lei nº 10.865, de 2004, deve preencher o Registro “C199” para validar a apuração do crédito. De acordo com a legislação em referência, o direito à apuração de crédito aplica-se apenas em relação às contribuições efetivamente pagas na importação de bens e serviços.
2. Devem ser informados neste registro os pagamentos de PIS/Pasep-Importação e de Cofins-Importação, referente ao serviço contratado com direito a crédito, uma vez que de acordo com a legislação em referência, o direito à apuração de crédito aplica-se apenas em relação às contribuições efetivamente pagas na importação de bens e serviços (art. 15 da Lei nº 10.865, de 2004).
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C199]
Campo 02 - Valor Válido: [0,1,2]
Campo 03 - Preenchimento: informar o número do documento de importação
Campo 04 - Preenchimento: Informar o valor recolhido de PIS/Pasep – Importação, relacionado ao documento informado neste registro. No caso de haver mais de um recolhimento (PIS/Pasep – Importação) em relação ao mesmo documento, informar no campo o somatório dos valores pagos.
De acordo com a legislação, o direito ao crédito de PIS/Pasep aplica-se em relação às contribuições efetivamente pagas na importação de bens e serviços.
Campo 05 - Preenchimento: Informar o valor recolhido de Cofins – Importação, relacionado ao documento informado neste registro. No caso de haver mais de um recolhimento (Cofins – Importação) em relação ao mesmo documento, informar no campo o somatório dos valores pagos.
De acordo com a legislação, o direito ao crédito de Cofins aplica-se em relação às contribuições efetivamente pagas na importação de bens e serviços.
Campo 06 - Preenchimento: Informar neste campo o número do ato concessório habilitando o estabelecimento ao Regime Aduaneiro Especial de Drawback.
<!-- End Registro C199 -->
<!-- Start Registro C380 -->
Registro C380: Nota Fiscal de Venda a Consumidor (Código 02) - Consolidação de Documentos Emitidos.
No registro C380 e filhos deve a pessoa jurídica escriturar as notas fiscais de venda ao consumidor não emitidas por ECF (código 02), consolidando os valores dos documentos emitidos no período da escrituração.
Nos registros filhos C381 (PIS/Pasep) e C385 (Cofins) devem ser detalhados os valores por CST, por item vendido e por alíquota, conforme o caso.
Os valores de documentos fiscais cancelados não devem ser computados no valor total dos documentos (campo VL_DOC), nem nos registros filhos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C380” | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 (Código 02 – Nota Fiscal de Venda a Consumidor) | C | 002* | - | S |
| 03 | DT_DOC_INI | Data de Emissão Inicial dos Documentos | N | 008* | - | S |
| 04 | DT_DOC_FIN | Data de Emissão Final dos Documentos | N | 008* | - | S |
| 05 | NUM_DOC_INI | Número do documento fiscal inicial | N | 006 | - | N |
| 06 | NUM_DOC_FIN | Número do documento fiscal final | N | 006 | - | N |
| 07 | VL_DOC | Valor total dos documentos emitidos | N | - | 02 | S |
| 08 | VL_DOC_CANC | Valor total dos documentos cancelados | N | - | 02 | S |

Observações: Nos Registros filhos C381 (PIS/Pasep) e C385 (Cofins) devem ser detalhados os valores por CST, por item vendido e por alíquota, conforme o caso.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [C380]
Campo 02 - Valor Válido: [02]
Campo 03 - Preenchimento: informar a data de emissão inicial dos documentos consolidados no registro, representativos de operações de vendas a consumidor, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 04 - Preenchimento: informar a data de emissão Final dos documentos consolidados no registro, representativos de operações de vendas a consumidor, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 05 - Preenchimento: informar o número do documento fiscal inicial a que se refere a consolidação.
Validação: valor informado deve ser maior que “0” (zero). O número do documento inicial deve ser menor ou igual ao número do documento final.
Campo 06 - Preenchimento: informar o número do documento fiscal final a que se refere a consolidação.
Validação: valor informado deve ser maior que “0” (zero). O número do documento final deve ser maior ou igual ao número do documento inicial.
Campo 07 – Preenchimento: Informar o valor total dos documentos fiscais consolidados no registro.
Campo 08 – Preenchimento:  Informar o valor total dos documentos fiscais de venda a consumidor – código 02, cancelados no período da escrituração. Os valores referentes aos documentos cancelados não devem ser incluídos no detalhamento dos registros filhos (C381 e C385).
<!-- End Registro C380 -->
<!-- Start Registro C381 -->
Registro C381: Detalhamento da Consolidação – PIS/Pasep
Neste registro serão informados os valores consolidados de cada item constante nas notas fiscais de venda a consumidor – código 02, objeto de consolidação no Registro Pai C380. Deve ser gerado um registro para cada combinação de CST e alíquotas.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C381” | C | 004* | - | S |
| 02 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 03 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | S |
| 04 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 05 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 06 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 07 | QUANT_BC_PIS | Quantidade – Base de cálculo do PIS/PASEP | N |   | 03 | N |
| 08 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 09 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | S |
| 10 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Deve ser gerado um registro para cada item vendido, conforme o cadastramento efetuado em 0200.
2. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST.
3. Os valores escriturados nos campos de bases de cálculo 05 (VL_BC_PIS) e 07 (QUANT_BC_PIS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT” e “QUANT_BC_PIS”, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C381]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 03 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 04 - Preenchimento: informar o valor total do item/produto consolidado neste registro.
Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 07 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 07 (base de cálculo em quantidade) dispensa o preenchimento do campo 05 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 08 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 07).
Campo 09 – Preenchimento: informar o valor do PIS/Pasep referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 05 ou campo 07) multiplicado pela alíquota aplicável ao item (campo 06 ou campo 08). No caso de aplicação da alíquota do campo 06, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 05 (VL_BC_PIS) = 1.000.000,00 e o Campo 06 (ALIQ_PIS) = 1,6500, então o Campo 09 (VL_PIS) será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 10 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas financeiras, receitas não operacionais, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C381 -->
<!-- Start Registro C385 -->
Registro C385: Detalhamento da Consolidação – Cofins
Neste registro serão informados os valores consolidados de cada item constante nas notas fiscais de venda a consumidor – código 02, objeto de consolidação no Registro Pai C380. Deve ser gerado um registro para cada combinação de CST e alíquotas.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C385” | C | 004* | - | S |
| 02 | CST_COFINS | Código da Situação Tributária referente a COFINS. | N | 002* | - | S |
| 03 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | S |
| 04 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 05 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N |   | 02 | N |
| 06 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 07 | QUANT_BC_COFINS | Quantidade – Base de cálculo da COFINS | N |   | 03 | N |
| 08 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N |   | 04 | N |
| 09 | VL_COFINS | Valor da COFINS | N | - | 02 | S |
| 10 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Deve ser gerado um registro para cada item vendido, conforme o cadastramento efetuado em 0200.
2. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST.
3. Os valores escriturados nos campos de bases de cálculo 05 (VL_BC_COFINS) e 07 (QUANT_BC_COFINS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT” e “QUANT_BC_COFINS_TOT”, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C381]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 03 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 04 - Preenchimento: informar o valor total do item/produto consolidado neste registro.
Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 07 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 07 (base de cálculo em quantidade) dispensa o preenchimento do campo 06 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 08 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 07).
Campo 09 – Preenchimento: informar o valor da Cofins referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 05 ou campo 07) multiplicado pela alíquota aplicável ao item (campo 06 ou campo 08). No caso de aplicação da alíquota do campo 06, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo 05 (VL_BC_COFINS) = 1.000.000,00 e o Campo 06 (ALIQ_COFINS) = 7,6000, então o Campo 09 (VL_COFINS) será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 10 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas financeiras, receitas não operacionais, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C385 -->
<!-- Start Registro C395 -->
Registro C395: Notas Fiscais de Venda a Consumidor (Códigos 02, 2D, 2E, 59, 60 e 65) – Aquisições/Entradas com Crédito.
No Registro C395 a pessoa jurídica poderá escriturar eventuais aquisições com direito a crédito (aquisição de bens a serem utilizados como insumos, por exemplo) cuja operação esteja documentada por nota fiscal de venda a consumidor.
No Registro filho C396 deve ser detalhado os dados fiscais necessários para a apuração dos créditos de PIS/Pasep e de Cofins.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C395" | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 03 | COD_PART | Código do participante emitente do documento (campo 02 do Registro 0150). | C | 060 | - | N |
| 04 | SER | Série do documento fiscal | C | 003 | - | S |
| 05 | SUB_SER | Subsérie do documento fiscal | C | 003 | - | N |
| 06 | NUM_DOC | Número do documento fiscal | C | 006 | - | S |
| 07 | DT_DOC | Data da emissão do documento fiscal | N | 008* | - | S |
| 08 | VL_DOC | Valor total do documento fiscal | N | - | 02 | S |

Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [C395]
Campo 02 - Valores válidos: [02, 2D, 2E, 59, 60 e 65]
Campo 03 - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 04 – Preenchimento: Informar neste campo a série do documento fiscal, se existir. Se no documento fiscal escriturado não constar série, informar o campo com “000”.
Campo 05 – Preenchimento: Informar neste campo a subsérie do documento fiscal, se existir.
Campo 06 – Preenchimento: informe apenas caracteres numéricos (0 a 9).
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 07 - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 08 – Preenchimento:  Informar o valor total do documento fiscal.
<!-- End Registro C395 -->
<!-- Start Registro C396 -->
Registro C396: Itens do Documento (Códigos 02, 2D, 2E, 59, 60 e 65) – Aquisições/Entradas com Crédito
Deve ser informado neste registro as informações referentes aos itens das notas fiscais de vendas a consumidor relacionadas no Registro Pai C395, necessárias para a apuração, por item do documento fiscal, dos créditos de PIS/Pasep e de Cofins.
Deve ser gerado um registro para cada item constante na nota fiscal de venda a consumidor relacionada em C395.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C396" | C | 004* | - | S |
| 02 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | S |
| 03 | VL_ITEM | Valor total do item (mercadorias ou serviços) | N | - | 02 | S |
| 04 | VL_DESC | Valor do desconto comercial do item | N | - | 02 | N |
| 05 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | S |
| 06 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 07 | VL_BC_PIS | Valor da base de cálculo do crédito de PIS/PASEP | N |   | 02 | N |
| 08 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 09 | VL_PIS | Valor do crédito de PIS/PASEP | N | - | 02 | N |
| 10 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 11 | VL_BC_COFINS | Valor da base de cálculo do crédito de COFINS | N |   | 02 | N |
| 12 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 13 | VL_COFINS | Valor do crédito de COFINS | N | - | 02 | N |
| 14 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Em relação aos itens com CST representativos de operações geradoras de créditos, os valores dos campos de bases de cálculo, VL_BC_PIS (Campo 07) e VL_BC_COFINS (Campo 11) serão recuperados no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105), no campo “VL_BC_PIS_TOT” e do crédito da Cofins (M505), no Campo “VL_BC_COFINS_TOT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C396]
Campo 02 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 03 - Preenchimento: informar o valor total do item/produto consolidado neste registro.
Campo 04 - Preenchimento: informar o valor do desconto comercial ou dos valores a excluir da base de cálculo da contribuição, conforme o caso.
Campo 05 - Preenchimento: informar a natureza da base de cálculo do crédito, conforme Tabela indicada no item 4.3.7 do Leiaute
Campo 06 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST.
Campo 07 - Preenchimento: informar neste campo o valor da base de cálculo do crédito de PIS/Pasep referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo de PIS/Pasep, no registro M105.
Campo 08 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 09 - Preenchimento: informar neste campo o valor do crédito de PIS/Pasep. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Campo 10 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST.
Campo 11 - Preenchimento: informar neste campo o valor da base de cálculo do crédito de Cofins referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo de Cofins no registro M505.
Campo 12 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 13 - Preenchimento: informar neste campo o valor do crédito de Cofins. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Campo 14 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas financeiras, receitas não operacionais, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C396 -->
<!-- Start Registro C400 -->
Registro C400: Equipamento ECF (Códigos 02 e 2D)
Este registro tem por objetivo identificar os equipamentos de ECF e deve ser informado por todos os contribuintes que utilizem tais equipamentos na emissão de documentos fiscais.
As operações de vendas com emissão de documento fiscal (códigos 02 e 2D) por ECF podem ser escrituradas na EFD-Contribuições, de forma consolidada (Registro C490) ou por ECF (C400), a critério da pessoa jurídica.
Caso a pessoa jurídica opte por escriturar as operações de vendas por ECF, de forma consolidada, no Registro C490, não precisa proceder à escrituração do Registro C400 (e registros filhos).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C400" | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 03 | ECF_MOD | Modelo do equipamento | C | 020 | - | S |
| 04 | ECF_FAB | Número de série de fabricação do ECF | C | 021 | - | S |
| 05 | ECF_CX | Número do caixa atribuído ao ECF | N | 003 | - | S |

Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [C400]
Campo 02 - Valores válidos: [02, 2D].
Campo 05 - Preenchimento: informar o número do caixa atribuído, pelo estabelecimento, ao equipamento emissor de documento fiscal. Um mesmo valor do campo ECF_CX não pode ser usado por dois equipamentos ECF ao mesmo tempo. Contudo, se o uso de um número for cessado, este mesmo número pode ser atribuído a outro equipamento de ECF, no período.
Validação do Registro: não podem ser informados dois ou mais registros C400 com a mesma combinação de valores dos campos COD_MOD, ECF_MOD e ECF_FAB.
<!-- End Registro C400 -->
<!-- Start Registro C405 -->
Registro C405: Redução Z (Códigos 02 e 2D)
Este registro deve ser apresentado com as informações da Redução Z de cada equipamento em funcionamento na data das operações de venda à qual se refere a redução. Inclui todos os documentos fiscais totalizados na Redução Z, inclusive as operações de venda realizadas durante o período de tolerância do Equipamento ECF.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C405" | C | 004* | - | S |
| 02 | DT_DOC | Data do movimento a que se refere a Redução Z | N | 008* | - | S |
| 03 | CRO | Posição do Contador de Reinício de Operação | N | 003 | - | S |
| 04 | CRZ | Posição do Contador de Redução Z | N | 006 | - | S |
| 05 | NUM_COO_FIN | Número do Contador de Ordem de Operação do último documento emitido no dia (Número do COO na Redução Z) | N | 006 | - | S |
| 06 | GT_FIN | Valor do Grande Total final | N | - | 02 | S |
| 07 | VL_BRT | Valor da venda bruta | N | - | 02 | S |

Observações: Registro obrigatório, se existir C400.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C405]
Campo 02 - Preenchimento: considerar a data do movimento, que inclui as operações de vendas realizadas durante o período de tolerância do equipamento ECF. Informar a data do movimento, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado deve ser menor ou igual à DT_FIN deste arquivo.
Campo 03 - Validação: o valor informado deve ser maior que “0” (zero).
Campo 04 - Validação: o valor informado deve ser maior que “0” (zero).
Campo 05 - Validação: o valor informado deve ser maior que “0” (zero).
Campo 06 - Preenchimento: valor acumulado no totalizador geral final.
Validação: o campo GT_FIN deve ser maior ou igual ao campo VL_BRT, exceto se houver reinício de operação.
Campo 07 - Preenchimento: valor acumulado no totalizador de venda bruta.
<!-- End Registro C405 -->
<!-- Start Registro C481 -->
Registro C481: Resumo Diário de Documentos Emitidos por ECF–PIS/Pasep (Código 02 e 2D).
Neste registro serão informados os valores consolidados por resumo diário, das informações relativas ao PIS/Pasep incidente sobre as vendas por ECF, por item vendido no período.
Deve ser gerado um registro para cada item vendido, conforme o cadastramento efetuado em 0200. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C481” | C | 004* | - | S |
| 02 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 05 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 06 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS/PASEP | N | - | 03 | N |
| 07 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 08 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 09 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 10 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Os valores escriturados nos campos de bases de cálculo 04 (VL_BC_PIS) e 06 (QUANT_BC_PIS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT” e “QUANT_BC_PIS_TOT”, respectivamente.
Nível hierárquico - 5
Ocorrência - 1:N
Campo 01 - Valor Válido: [C481]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 03 - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 05 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 06 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 06 (base de cálculo em quantidade) dispensa o preenchimento do campo 04 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 06).
Campo 08 – Preenchimento:  informar o valor do PIS/Pasep referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 04 ou campo 06) multiplicado pela alíquota aplicável ao item (campo 05 ou campo 07). No caso de aplicação da alíquota do campo 05, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 09 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 10 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas financeiras, receitas não operacionais, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C481 -->
<!-- Start Registro C485 -->
Registro C485: Resumo Diário de Documentos Emitidos por ECF – Cofins (Códigos 02 e 2D)
Neste registro serão informados os valores consolidados por resumo diário, das informações relativas a Cofins incidente sobre as vendas por ECF, por item vendido no período.
Deve ser gerado um registro para cada item vendido, conforme o cadastramento efetuado em 0200. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C485” | C | 004* | - | S |
| 02 | CST_COFINS | Código da Situação Tributária referente a COFINS. | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 05 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 06 | QUANT_BC_COFINS | Quantidade – Base de cálculo da COFINS | N | - | 03 | N |
| 07 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 08 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 09 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 10 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Os valores escriturados nos campos de bases de cálculo 04 (VL_BC_COFINS) e 06 (QUANT_BC_COFINS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT” e “QUANT_BC_COFINS_TOT”, respectivamente.
Nível hierárquico - 5
Ocorrência - 1:N
Campo 01 - Valor Válido: [C485]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 03 - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 05 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 06 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 06 (base de cálculo em quantidade) dispensa o preenchimento do campo 04 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 06).
Campo 08 – Preenchimento:  informar o valor da Cofins referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 04 ou campo 06) multiplicado pela alíquota aplicável ao item (campo 05 ou campo 07). No caso de aplicação da alíquota do campo 05, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo 08 “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 09 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 10 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas de comercialização, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C485 -->
<!-- Start Registro C489 -->
Registro C489: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “C489”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referente ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C489" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
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
Ocorrência - 1:N
Campo 01 - Valor Válido: [C489]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C489 -->
<!-- Start Registro C490 -->
Registro C490: Consolidação de Documentos Emitidos por ECF (Códigos 02, 2D, 59 e 60)
Registro para a escrituração consolidada das vendas do período, mediante a emissão de cupom fiscal por ECF, relacionando as operações por item de produto. A escrituração de forma consolidada das operações de vendas mediante cupom fiscal neste registro substitui a escrituração das vendas por ECF constante do registro C400.Nos registros filhos C491 (PIS/Pasep) e C495 (Cofins) devem ser detalhados os valores por CST, por item vendido e por alíquota, conforme o caso.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C490” | C | 004* | - | S |
| 02 | DT_DOC_INI | Data de Emissão Inicial dos Documentos | N | 008* | - | S |
| 03 | DT_DOC_FIN | Data de Emissão Final dos Documentos | N | 008* | - | S |
| 04 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |

Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [C490]
Campo 02 - Preenchimento: informar a data de emissão inicial dos documentos consolidados no registro, representativos de operações de vendas mediante emissão de cupom fiscal, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 03 - Preenchimento: informar a data de emissão Final dos documentos consolidados no registro, representativos de operações de vendas mediante emissão de cupom fiscal, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 04 - Valor Válido: [02, 2D, 59, 60]
<!-- End Registro C490 -->
<!-- Start Registro C491 -->
Registro C491: Detalhamento da Consolidação de Documentos Emitidos por ECF (Códigos 02, 2D, 59 e 60) – PIS/Pasep

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C491” | C | 004* | - | S |
| 02 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 03 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 04 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 05 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 06 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 08 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS/PASEP | N | - | 03 | N |
| 09 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 10 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 11 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Deve ser gerado um registro para cada item vendido, conforme o cadastramento efetuado em 0200.
2. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST.
3. Os valores escriturados nos campos de bases de cálculo 06 (VL_BC_PIS) e 08 (QUANT_BC_PIS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT” e “QUANT_BC_PIS_TOT”, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C491]
Campo 02 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 04 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01. Não devem ser relacionadas na consolidação operações que não se refiram a receitas auferidas de vendas, como no caso de transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica.
Campo 05 - Preenchimento: Informar neste campo o valor consolidado das vendas do item no período.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 08 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 08 (base de cálculo em quantidade) dispensa o preenchimento do campo 06 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 09 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 08).
Campo 10 – Preenchimento: informar o valor do PIS/Pasep referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 06 ou campo 08) multiplicado pela alíquota aplicável ao item (campo 07 ou campo 09). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 11 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas de comercialização, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C491 -->
<!-- Start Registro C495 -->
Registro C495: Detalhamento da Consolidação de Documentos Emitidos por ECF (Códigos 02, 2D, 59 e 60) – Cofins

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C495” | C | 004* | - | S |
| 02 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 03 | CST_COFINS | Código da Situação Tributária referente a COFINS. | N | 002* | - | S |
| 04 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 05 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 06 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 07 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 08 | QUANT_BC_COFINS | Quantidade – Base de cálculo da COFINS | N | - | 03 | N |
| 09 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 10 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 11 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Deve ser gerado um registro para cada item vendido, conforme o cadastramento efetuado em 0200.
2. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST.
3. Os valores escriturados nos campos de bases de cálculo 06 (VL_BC_COFINS) e 08 (QUANT_BC_COFINS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT” e “QUANT_BC_COFINS_TOT”, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C495]
Campo 02 – Preenchimento: informar neste campo o código do item (produtos e/ou serviços) a que se refere a consolidação.
Validação: o valor informado neste campo deve existir no registro 0200.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 04 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP, relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01. Não devem ser relacionadas na consolidação operações que não se refiram a receitas auferidas de vendas, como no caso de transferência de mercadorias e produtos entre estabelecimentos da pessoa jurídica.
Campo 05 - Preenchimento: Informar neste campo o valor consolidado das vendas do item no período.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 08 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O preenchimento do campo 08 (base de cálculo em quantidade) dispensa o preenchimento do campo 06 (base de cálculo em valor), em relação ao item informado neste registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 09 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 08).
Campo 10 – Preenchimento: informar o valor da Cofins referente ao item consolidado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 06 ou campo 08) multiplicado pela alíquota aplicável ao item (campo 07 ou campo 09). No caso de aplicação da alíquota do campo 07, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo 10 “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 11 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receitas de vendas, receitas de comercialização, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C495 -->
<!-- Start Registro C499 -->
Registro C499: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “C499”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C499" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
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
Ocorrência - 1:N
Campo 01 - Valor Válido: [C499]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C499 -->
<!-- Start Registro C500 -->
Registro C500: Nota Fiscal/Conta de Energia Elétrica (Código 06), Nota Fiscal de Energia Elétrica Eletrônica – NF3e (Código 66), Nota Fiscal/Conta de fornecimento D'água Canalizada (Código 29), Nota Fiscal/Consumo Fornecimento de Gás (Código 28) e NF-e (Código 55) – Documentos de Entrada / Aquisição com Crédito
Neste registro serão informadas pela pessoa jurídica as operações sujeitas à apuração de créditos de PIS/Pasep e de Cofins, na forma da legislação tributária, referentes a:
- energia elétrica, consumida nos estabelecimentos da pessoa jurídica (art. 3º, III, das Leis nº 10.637/02 e nº 10.833/03);
- água canalizada ou gás, utilizados como insumo na fabricação de produtos destinados à venda ou na prestação de serviços (art. 3º, II, das Leis nº 10.637/02 e nº 10.833/03).
A partir de 01/01/2020, se o campo COD_MOD for igual a ”66” ou “55” o campo CHV_DOCe é obrigatório.
Validação do Registro: não podem ser informados dois ou mais registros com a mesma combinação de valores dos campos COD_PART, COD_MOD, COD_SIT, SER, SUB, NUM_DOC e DT_DOC. A partir de 01/01/2020 fica incluído o campo CHV_DOCe.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C500" | C | 004* | - | S |
| 02 | COD_PART | Código do participante do fornecedor (campo 02 do Registro 0150). | C | 060 | - | S |
| 03 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 04 | COD_SIT | Código da situação do documento fiscal, conforme a Tabela 4.1.2 | N | 002* | - | S |
| 05 | SER | Série do documento fiscal | C | 004 | - | N |
| 06 | SUB | Subsérie do documento fiscal | N | 003 | - | N |
| 07 | NUM_DOC | Número do documento fiscal | N | 009 | - | S |
| 08 | DT_DOC | Data da emissão do documento fiscal | N | 008* | - | S |
| 09 | DT_ENT | Data da entrada | N | 008* | - | N |
| 10 | VL_DOC | Valor total do documento fiscal | N | - | 02 | S |
| 11 | VL_ICMS | Valor acumulado do ICMS | N | - | 02 | N |
| 12 | COD_INF | Código da informação complementar do documento fiscal (campo 02 do Registro 0450) | C | 006 | - | N |
| 13 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 14 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 15 | CHV_DOCe | Chave do Documento Fiscal Eletrônico | N | 044* | - | N |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [C500]
Campo 02 - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 03 - Valores válidos: [06, 28, 29,55, 66]
A versão 1.03 do Programa Validador e Assinador (PVA) da EFD-Contribuições passa a aceitar a Nota Fiscal Eletrônica, código 55, referente a aquisição de energia elétrica, como documento válido a ser escriturado nesse registro.
Campo 04 - Valores válidos: [00, 01, 02, 03, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Tabela Situação do Documento, integrante deste Guia Prático.
Campo 05 – Preenchimento: Informar neste campo a série do documento fiscal, se existir.
Campo 06 – Preenchimento: Informar neste campo a subsérie do documento fiscal, se existir.
Campo 07 – Preenchimento: Informar neste campo o número do documento fiscal de aquisição de energia elétrica, água canalizada ou gás, com direito a crédito.
Validação: o valor informado no campo deve ser maior que “0” (zero). Na impossibilidade de informar o número específico de documento fiscal, o campo deve ser preenchido com o conteúdo “000000000”.
Campo 08 - Preenchimento: data de emissão da nota fiscal no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data de entrada (campo 09) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 09 - Preenchimento: data de entrada da nota fiscal no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data de emissão do documento fiscal (campo 08) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). O valor deve ser maior ou igual à data de emissão. Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 10 - Preenchimento: Informar neste campo o valor do documento fiscal com direito à apuração de crédito.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 11 - Preenchimento: Informar neste campo o valor do ICMS constante no documento fiscal.
Campo 12 - Preenchimento: Informar neste campo o código da informação complementar do documento fiscal, se houver.
Campo 13 - Preenchimento: Informar neste campo o valor do total do PIS/Pasep.
Campo 14 - Preenchimento: Informar neste campo o valor da Cofins.
Campo 15 (CHV_DOCe) - Preenchimento: Informar a chave do documento eletrônico. A partir de 01/01/2020, o campo é obrigatório quando COD_MOD for igual a “66” ou “55”.
Validação: será conferido o dígito verificador (DV) da chave do documento eletrônico. Será verificada a consistência da raiz de CNPJ e UF do participante com a raiz de CNPJ e UF contida na chave do documento eletrônico.  Será verificada a consistência da informação dos campos COD_MOD, NUM_DOC e SER com o número do documento e série contidos na chave do documento eletrônico.
<!-- End Registro C500 -->
<!-- Start Registro C501 -->
Registro C501: Complemento da Operação (Códigos 06, 28 e 29) – PIS/Pasep
Neste registro devem ser detalhadas as informações relativas à apuração do crédito de PIS/Pasep, referentes ao documento fiscal escriturado no Registro Pai C500. Deve ser escriturado um registro C501 para cada item (fornecimento d´água canalizada, de energia elétrica ou de gás) cuja operação dê direito a crédito, pelo seu valor total ou parcial.
Caso em relação a um mesmo item venha a ocorrer tratamentos tributários diversos (mais de um CST), deve a pessoa jurídica informar um registro C501 para cada CST.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C501” | C | 004* | - | S |
| 02 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | N |
| 05 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | S |
| 06 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | S |
| 07 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | S |
| 08 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Em relação aos itens com CST representativos de operações geradoras de créditos, os valores dos campos de bases de cálculo escriturados no campo “VL_BC_PIS” (Campo 05) serão recuperados no Bloco M, para a demonstração da base de cálculo do crédito de PIS/Pasep (M105), no campo “VL_BC_PIS_TOT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C501]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

| Código | Descrição |
| --- | --- |
| 50 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 51 | Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno |
| 52 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação |
| 53 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 54 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 55 | Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 56 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 60 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 61 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno |
| 62 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação |
| 63 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 64 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 65 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 66 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 70 | Operação de Aquisição sem Direito a Crédito |
| 71 | Operação de Aquisição com Isenção |
| 72 | Operação de Aquisição com Suspensão |
| 73 | Operação de Aquisição a Alíquota Zero |
| 73 | Operação de Aquisição a Alíquota Zero |
| 74 | Operação de Aquisição sem Incidência da Contribuição |
| 75 | Operação de Aquisição por Substituição Tributária |
| 98 | Outras Operações de Entrada |
| 99 | Outras Operações |

Campo 03 - Preenchimento: informar o valor total do item, constante no documento fiscal a que se refere o registro.
Campo 04 - Preenchimento: Informar o código correspondente à natureza da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.

| Código | Descrição |
| --- | --- |
| 01 | Aquisição de bens para revenda |
| 02 | Aquisição de bens utilizados como insumo |
| 04 | Energia elétrica utilizada nos estabelecimentos da pessoa jurídica |
| 13 | Outras operações com direito a crédito |

Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item do documento fiscal.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “VL_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito do crédito (1,65%), conforme o caso.
Campo 07 – Preenchimento: informar o valor do crédito de PIS/Pasep referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (VL_BC_PIS) multiplicado pela alíquota aplicável ao item (ALIQ_PIS), dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 08 - Preenchimento: informar o Código da Conta Analítica. Exemplos: custos de fabricação, despesas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C501 -->
<!-- Start Registro C505 -->
Registro C505: Complemento da Operação (Códigos 06, 28 e 29) – Cofins
Neste registro devem ser detalhadas as informações relativas à apuração do crédito de COFINS, referentes ao documento fiscal escriturado no Registro Pai C500. Deve ser escriturado um registro C505 para cada item (fornecimento d´água canalizada, de energia elétrica ou de gás) cuja operação dê direito a crédito, pelo seu valor total ou parcial.
Caso em relação a um mesmo item venha a ocorrer tratamentos tributários diversos (mais de um CST), deve a pessoa jurídica informar um registro C505 para cada CST.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C505” | C | 004* | - | S |
| 02 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7 | C | 002* | - | N |
| 05 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | S |
| 06 | ALIQ_COFINS | Alíquota da COFINS  (em percentual) | N | 008 | 04 | S |
| 07 | VL_COFINS | Valor da COFINS | N | - | 02 | S |
| 08 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Em relação aos itens com CST representativos de operações geradoras de créditos, os valores dos campos de bases de cálculo escriturados no campo “VL_BC_COFINS” (Campo 05) serão recuperados no Bloco M, para a demonstração da base de cálculo do crédito da Cofins (M505), no Campo “VL_BC_COFINS_TOT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C505]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

| Código | Descrição |
| --- | --- |
| 50 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 51 | Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno |
| 52 | Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação |
| 53 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 54 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 55 | Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 56 | Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 60 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno |
| 61 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno |
| 62 | Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação |
| 63 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno |
| 64 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação |
| 65 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação |
| 66 | Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação |
| 70 | Operação de Aquisição sem Direito a Crédito |
| 71 | Operação de Aquisição com Isenção |
| 72 | Operação de Aquisição com Suspensão |
| 73 | Operação de Aquisição a Alíquota Zero |
| 73 | Operação de Aquisição a Alíquota Zero |
| 74 | Operação de Aquisição sem Incidência da Contribuição |
| 75 | Operação de Aquisição por Substituição Tributária |
| 98 | Outras Operações de Entrada |
| 99 | Outras Operações |

Campo 03 - Preenchimento: informar o valor total do item, constante no documento fiscal a que se refere o registro.
Campo 04 - Preenchimento: Informar o código correspondente à natureza da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.

| Código | Descrição |
| --- | --- |
| 01 | Aquisição de bens para revenda |
| 02 | Aquisição de bens utilizados como insumo |
| 04 | Energia elétrica utilizada nos estabelecimentos da pessoa jurídica |
| 13 | Outras operações com direito a crédito |

Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item do documento fiscal.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito da Cofins (M505, campo “VL_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito do crédito (7,6%), conforme o caso.
Campo 07 – Preenchimento: informar o valor do crédito de Cofins referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (VL_BC_COFINS) multiplicado pela alíquota aplicável ao item (ALIQ_COFINS), dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo 07 “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 08 - Preenchimento: informar o Código da Conta Analítica. Exemplos: custos de fabricação, despesas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C505 -->
<!-- Start Registro C509 -->
Registro C509: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “C509”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C509" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - | S |

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
Campo 01 - Valor Válido: [C509]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C509 -->
<!-- Start Registro C600 -->
Registro C600: Consolidação Diária de Notas Fiscais/Contas Emitidas de Energia Elétrica (Código 06), Nota Fiscal de Energia Elétrica Eletrônica – NF3e (Código 66), Nota Fiscal/Conta de Fornecimento D'água Canalizada (Código 29) e Nota Fiscal/Conta de Fornecimento de Gás (Código 28) (Empresas Obrigadas ou não Obrigadas ao Convenio ICMS 115/03) – Documentos de Saída
Este registro deve ser apresentado pelas pessoas jurídicas que auferem receita da venda de energia elétrica, água canalizada e gás, informando a consolidação diária de Notas Fiscais/Conta de Energia Elétrica (código 06 da Tabela Documentos Fiscais do ICMS), Nota Fiscal de Energia Elétrica Eletrônica – NF3e (código 66 da Tabela de Documentos Fiscais do ICMS – a partir das escriturações de janeiro/2020), Notas Fiscais de Fornecimento D’Água (código 29 da Tabela Documentos Fiscais do ICMS) e Notas Fiscais/Conta de Fornecimento de Gás (código 28 da Tabela Documentos Fiscais do ICMS), independente se a pessoa jurídica está ou não obrigada ao Convênio ICMS 115/2003. Notas fiscais eletrônicas, modelo 55, referentes à fornecimento de energia elétrica também devem ser consolidadas neste registro.
OBS: Caso a pessoa jurídica queira demonstrar na escrituração os registros representativos das receitas de suas atividades, de acordo com cada natureza, tipo ou forma de reconhecimento, poderá segregar os diversos tipos de receitas, nos registros C601 (PIS/Pasep) e C605 (Cofins), segregando as receitas em contas contábeis específicas, gerando registros C601 e C605 específicos para cada conta contábil correspondente.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C600" | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 03 | COD_MUN | Código do município dos pontos de consumo, conforme a tabela IBGE | N | 007* | - | N |
| 04 | SER | Série do documento fiscal | C | 004 | - | N |
| 05 | SUB | Subsérie do documento fiscal | N | 003 | - | N |
| 06 | COD_CONS | Código de classe de consumo de energia elétrica, conforme a Tabela 4.4.5, ou Código de Consumo de Fornecimento D´água – Tabela 4.4.2 ou Código da classe de consumo de gás canalizado   conforme Tabela 4.4.3. | N | 002* | - | N |
| 07 | QTD_CONS | Quantidade de documentos consolidados neste registro | N | - | - | S |
| 08 | QTD_CANC | Quantidade de documentos cancelados | N | - | - | N |
| 09 | DT_DOC | Data dos documentos consolidados | N | 008* | - | S |
| 10 | VL_DOC | Valor total dos documentos | N | - | 02 | S |
| 11 | VL_DESC | Valor acumulado dos descontos | N | - | 02 | N |
| 12 | CONS | Consumo total acumulado, em kWh (Código 06) | N | - | - | N |
| 13 | VL_FORN | Valor acumulado do fornecimento | N | - | 02 | N |
| 14 | VL_SERV_NT | Valor acumulado dos serviços não-tributados pelo ICMS | N | - | 02 | N |
| 15 | VL_TERC | Valores cobrados em nome de terceiros | N | - | 02 | N |
| 16 | VL_DA | Valor acumulado das despesas acessórias | N | - | 02 | N |
| 17 | VL_BC_ICMS | Valor acumulado da base de cálculo do ICMS | N | - | 02 | N |
| 18 | VL_ICMS | Valor acumulado do ICMS | N | - | 02 | N |
| 19 | VL_BC_ICMS_ST | Valor acumulado da base de cálculo do ICMS substituição tributária | N | - | 02 | N |
| 20 | VL_ICMS_ST | Valor acumulado do ICMS retido por substituição tributária | N | - | 02 | N |
| 21 | VL_PIS | Valor acumulado do PIS/PASEP | N | - | 02 | S |
| 22 | VL_COFINS | Valor acumulado da COFINS | N | - | 02 | S |

Observações: Não devem ser considerados os documentos fiscais denegados ou de numeração inutilizada.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [C600]
Campo 02 - Valores válidos: [01, 06, 28, 29, 55, 66]
Campo 03 - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
Campo 04 – Preenchimento: informar a série do documento fiscal objeto da consolidação diária, se houver.
Campo 05– Preenchimento: informar a subsérie do documento fiscal objeto da consolidação diária, se houver.
Campo 06 - Preenchimento: informe, caso existente, a classe de consumo de energia elétrica conforme Tabela  4.4.5, ou Código de Consumo de Fornecimento D´água – Tabela 4.4.2 ou Código da  classe de consumo de gás canalizado   conforme Tabela 4.4.3. Estas tabelas estão disponibilizadas no Portal do SPED no sítio da RFB na Internet, no endereço http://sped.rfb.gov.br>.
Campo 07 - Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 08 - Validação: o valor deve ser menor ou igual ao valor do campo QTD_CONS, pois a quantidade de documentos cancelados não pode ser maior que a quantidade de documentos consolidados. Não devem ser considerados os documentos fiscais denegados ou de numeração inutilizada.
Campo 09 - Preenchimento: Utilizar o formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 10 – Preenchimento: informar o valor total dos documentos objeto da consolidação diária.
Campo 18 - Validação: informar o valor acumulado do ICMS referente aos documentos consolidados.
Campo 21 - Validação: informar o valor acumulado do PIS/Pasep referente aos documentos consolidados.
Campo 22 - Validação: informar o valor acumulado da Cofins referente aos documentos consolidados.
<!-- End Registro C600 -->
<!-- Start Registro C601 -->
Registro C601: Complemento da Consolidação Diária (Códigos 06, 28 e 29) – Documentos de Saídas - PIS/Pasep
Registro de detalhamento das informações referentes ao PIS/Pasep, consolidadas no registro C600.
No caso de a pessoa jurídica auferir receitas com regimes tributários (CST-PIS) distintos, deve a pessoa jurídica gerar um registro para cada CST, conforme a natureza da receita (tributada, não-tributada, de exportação).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C601” | C | 004* | - | S |
| 02 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | S |
| 05 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | S |
| 06 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | S |
| 07 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Os valores escriturados nos campos de bases de cálculo 04 (VL_BC_PIS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C601]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 03 - Preenchimento: informar o valor total do item objeto da consolidação diária a que se refere o registro.
Campo 04 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à consolidação diária.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 05 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (0,65% ou 1,65%), conforme o caso.
Campo 06 – Preenchimento: informar o valor do PIS/Pasep apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 07 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita de comercialização, receita da venda de produtos de fabricação própria, receita da distribuição de energia elétrica, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C601 -->
<!-- Start Registro C605 -->
Registro C605: Complemento da Consolidação Diária (Códigos 06, 28 e 29) – Documentos de Saídas – Cofins
Registro de detalhamento das informações referentes a COFINS, consolidadas no registro C600.
No caso de a pessoa jurídica auferir receitas com regimes tributários (CST-COFINS) distintos, deve a pessoa jurídica gerar um registro para cada CST, conforme a natureza da receita (tributada, não-tributada, de exportação).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C605” | C | 004* | - | S |
| 02 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N |   | 02 | S |
| 05 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | S |
| 06 | VL_COFINS | Valor da COFINS | N | - | 02 | S |
| 07 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Os valores escriturados nos campos de bases de cálculo 04 (VL_BC_COFINS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C605]
Campo 02 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 03 - Preenchimento: informar o valor total do item objeto da consolidação diária a que se refere o registro.
Campo 04 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à consolidação diária.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 05 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (3% ou 7,6%), conforme o caso.
Campo 06 – Preenchimento: informar o valor da Cofins apurada em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo 06 “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 07 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita de comercialização, receita da venda de produtos de fabricação própria, receita da distribuição de energia elétrica, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C605 -->
<!-- Start Registro C609 -->
Registro C609: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou de créditos.
2. Uma vez procedida à escrituração do Registro “C609”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C609" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - | S |

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
Campo 01 - Valor Válido: [C609]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C609 -->
<!-- Start Registro C800 -->
Registro C800: Cupom Fiscal Eletrônico (Código 59)
Registro para informação por documento fiscal emitido – não disponível para escrituração no PVA
Registro para escrituração pela pessoa jurídica, da receita da venda de bens e serviços mediante a emissão de cupom fiscal eletrônico – CF-e (código 59), conforme Ajuste SINIEF nº 11, de 24 de setembro de 2010, ou outro documento representativo de nota fiscal de venda a consumidor (NFC-e), porventura instituído.
As operações de vendas com emissão de cupom fiscal eletrônico - CF-e poderão, a critério da pessoa jurídica, ser escrituradas na EFD-Contribuições, por documento fiscal individualizado (registro C800) ou de forma consolidada por equipamento SAT-CF-e (C860).
Caso a pessoa jurídica opte por escriturar as operações de vendas por documento fiscal (CF-e) neste registro C800, não deve proceder à escrituração consolidada por equipamento SAT-CF-e, em C860.
Deve a pessoa jurídica gerar um registro para cada CF-e (Código 59) emitido por equipamento SAT-CF-e. Não poderão ser informados dois ou mais registros com a mesma combinação de COD_SIT + NUM_CFE + NUM_SAT.
Para cupom fiscal eletrônico cancelado, informar somente os campos REG, COD_MOD, COD_SIT, NUM_CFE, NR_SAT e CHV_CFE.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C800" | C | 004 | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002 | - | S |
| 03 | COD_SIT | Código da situação do documento fiscal, conforme a Tabela 4.1.2 | N | 002 | - | S |
| 04 | NUM_CFE | Número do Cupom Fiscal Eletrônico | N | 009 | - | S |
| 05 | DT_DOC | Data da emissão do Cupom Fiscal Eletrônico | N | 008 | - | S |
| 06 | VL_CFE | Valor total do Cupom Fiscal Eletrônico | N | - | 02 | S |
| 07 | VL_PIS | Valor total do PIS | N | - | 02 | N |
| 08 | VL_COFINS | Valor total da COFINS | N | - | 02 | N |
| 09 | CNPJ_CPF | CNPJ ou CPF do destinatário | N | 14 | - | N |
| 10 | NR_SAT | Número de Série do equipamento SAT | N | 009 | - | N |
| 11 | CHV_CFE | Chave do Cupom Fiscal Eletrônico | N | 044 | - | N |
| 12 | VL_DESC | Valor total do desconto/exclusão sobre item | N | - | 02 | N |
| 13 | VL_MERC | Valor total das mercadorias e serviços | N | - | 02 | N |
| 14 | VL_OUT_DA | Valor de outras desp. Acessórias (acréscimo) | N | - | 02 | N |
| 15 | VL_ICMS | Valor do ICMS | N | - | 02 | N |
| 16 | VL_PIS_ST | Valor total do PIS retido por subst. trib. | N | - | 02 | N |
| 17 | VL_COFINS_ST | Valor total da COFINS retido por subst. trib. | N | - | 02 | N |

Observações:
1. As operações de vendas com emissão de cupom fiscal eletrônico (código 59) podem ser escrituradas na EFD-Contribuições, de forma individualizada por documento fiscal (Registro C800) ou de forma consolidada (resumos diários) por equipamentos SAT-CF-e (C860), a critério da pessoa jurídica;
2. Caso a pessoa jurídica opte por escriturar as operações de vendas por CF-e, no Registro C800, não precisa proceder à escrituração do Registro C860 (e registros filhos).
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 – Valor Válido: [C800]
Campo 02 – Preenchimento: deve corresponder ao código do Cupom Fiscal Eletrônico (Valor Válido: [59])
Campo 03 – Valores válidos: [00, 01, 02, 03]
Campo 04 – Preenchimento: informar o número do cupom fiscal eletrônico
Campo 05 – Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve ser menor ou igual ao valor do campo DT_FIN do registro 0000.
Campo 06 – Preenchimento: corresponde ao campo Valor total do CF-e, constante do leiaute do CF-e.
Validação: o valor informado neste campo deve ser igual à soma do campo VL_OPR dos registros C850 (“filhos” deste registro C800).
Campo 07 – Preenchimento: corresponde ao campo Valor Total do PIS, constante do leiaute do CF-e.
Campo 08 – Preenchimento:  corresponde ao campo Valor Total do COFINS, constante do leiaute do CF-e.
Campo 09 – Preenchimento: informar o CNPJ, com 14 dígitos, ou o CPF, com 11 dígitos, do adquirente.
Validação: se forem informados 14 caracteres, o campo será validado como CNPJ. Se forem informados 11 caracteres, o campo será validado como CPF. O preenchimento com outra quantidade de caracteres será considerado inválido.
Campo 10 – Preenchimento: informar o número de série do equipamento SAT.
Campo 11 – Validação: é conferido o dígito verificador (DV) da chave do CF-e. Para confirmação inequívoca de que a chave da NF-e corresponde aos dados informados no documento, será comparado o CNPJ existente na CHV_CFE com o campo CNPJ do registro 0000, que corresponde ao CNPJ do informante do arquivo. Serão verificados a consistência da informação do campo NUM_CFE e o número do documento contido na chave do CF-e, bem como comparado se a informação do AAMM de emissão contido na chave do CFE corresponde ao ano e mês da data de emissão do CF-e. Será também comparada a UF codificada na chave do CF-e com o campo UF informado no registro 0000.
Formação da chave:

| Campo | Tamanho | Observação: |
| --- | --- | --- |
| Código da UF | 2 |   |
| AAMM da emissão | 4 |   |
| CNPJ do emitente | 14 |   |
| Modelo do documento fiscal | 2 | Código para o CF-e |
| Número de série do SAT | 9 | Número sequencial atribuído pela SEFAZ, iniciando em 000000001 |
| Número do CF-e | 6 | Numeração sequencial para cada equipamento |
| Código numérico | 6 | Número aleatório gerado pelo SAT para cada CF-e |
| DV | 1 | Módulo 11 |
| Total | 44 |   |

Campo 12 – Preenchimento: corresponde ao campo Valor Total dos Descontos sobre item, constante do leiaute do CF-e.
Campo 13 – Preenchimento: corresponde ao campo Valor Total dos Produtos e Serviços, constante do leiaute do CF-e.
Campo 14 – Preenchimento: corresponde ao campo Valor Total de Outras Despesas Acessórias sobre item, constante do leiaute do CF-e.
Campo 15 – Preenchimento: corresponde ao campo Valor Total do ICMS, constante do leiaute do CF-e.
Campo 16 – Preenchimento: corresponde ao campo Valor Total do PIS retido por substituição tributária, constante do leiaute do CF-e.
Campo 17 – Preenchimento: corresponde ao campo Valor Total do COFINS retido por substituição tributária, constante do leiaute do CF-e.
<!-- End Registro C800 -->
<!-- Start Registro C810 -->
Registro C810: Detalhamento do Cupom Fiscal Eletrônico (Código 59) – PIS/Pasep e Cofins
Registro para informação por documento fiscal emitido – não disponível para escrituração no PVA
Registro de preenchimento obrigatório para fins de detalhamento, por item constante no documento fiscal ou por CST, dos valores constantes no cupom fiscal eletrônico, escriturado no registro C800.
No caso de detalhamento do registro C810 por item do documento fiscal, havendo em relação a um mesmo item mais de um CST, CFOP ou Alíquotas (do PIS/Pasep e da Cofins), deve ser informado pela pessoa jurídica um registro C810 para cada CST, CFOP ou alíquota existente.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C810" | C | 004* | - | S |
| 02 | CFOP | Código fiscal de operação e prestação | N | 004 | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 05 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 06 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N |   | 02 | N |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 08 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 09 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 10 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N |   | 02 | N |
| 11 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 12 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 13 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Este registro tem por objetivo representar a escrituração do CF-e (código 59) segmentado por item do documento ou por CST (CST PIS/Pasep e CST Cofins);
2. No caso do detalhamento do CF-e ser efetuado por item do documento, deve ser gerado um registro para cada item vendido, conforme o código de item cadastrado no Registro 0200;
3. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST. Como também, no caso de a operação tributável incidir a alíquotas distintas;
4. Os valores escriturados nos campos de bases de cálculo 06 (VL_BC_PIS) e 10 (VL_BC_COFINS) correspondentes a itens vendidos com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep e da Cofins, nos Campos “VL_BC_CONT” dos registros M210 e M610, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C810]
Campo 02 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações informadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 03 - Preenchimento: informar o valor do(s) item(ns) (produto e/ou serviço) constante(s) no documento fiscal.
Campo 04 – Preenchimento: informar neste campo o código do(s) item(ns), referente(s) ao produto e/ou serviço objeto de escrituração neste registro.
Validação: o valor informado neste campo (código do item) deve está informado e cadastrado no registro 0200 (Tabela de Identificação do Item).
Campo 05 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 04 | Operação Tributável Monofásica - Revenda a Alíquota Zero |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 08 – Preenchimento:  informar o valor do PIS/Pasep referente ao item consolidado neste registro.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 06) multiplicado pela alíquota aplicável ao item (campo 07).
Exemplo: Sendo o Campo 06 (VL_BC_PIS) = 1.000.000,00 e o Campo 07 (ALIQ_PIS) = 1,6500, então o Campo 08 (VL_PIS) será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 09 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 04 | Operação Tributável Monofásica - Revenda a Alíquota Zero |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 10 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social.
Campo 11 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 12 – Preenchimento: informar o valor da Cofins referente ao item consolidado neste registro.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 10) multiplicado pela alíquota aplicável ao item (campo 11).
Exemplo: Sendo o Campo 10 (VL_BC_COFINS) = 1.000.000,00 e o Campo 11 (ALIQ_COFINS) = 7,6000, então o Campo 12 (VL_COFINS) será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 13 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
<!-- End Registro C810 -->
<!-- Start Registro C820 -->
Registro C820: Detalhamento do Cupom Fiscal Eletrônico (Código 59) – PIS/Pasep e Cofins Apurado por Unidade de Medida de Produto
Registro para informação por documento fiscal emitido – não disponível para escrituração no PVA
Registro de preenchimento específico para fins de detalhamento das contribuições apuradas por unidade de medida de produto, pela pessoa jurídica produtora/fabricante e importadora dos produtos sujeitos a esse regime tributário (combustíveis, álcool, bebidas frias e embalagens para bebidas frias), e pessoa jurídica comercial de embalagem para bebidas frias. A escrituração da receita da revenda de produtos monofásicos, sujeitas a alíquota zero das contribuições, devem ser informadas no registro C810.
No caso de detalhamento do registro C820 por item do documento fiscal, havendo em relação a um mesmo item mais de um CST, CFOP ou Alíquotas (do PIS/Pasep e da Cofins), deve ser informado pela pessoa jurídica um registro C820 para cada CST, CFOP ou alíquota existente.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C820" | C | 004* | - | S |
| 02 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 05 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 06 | QUANT_BC_PIS | Base de cálculo em quantidade - PIS/PASEP | N | - | 03 | N |
| 07 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 08 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 09 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 10 | QUANT_BC_COFINS | Base de cálculo em quantidade – COFINS | N | - | 03 | N |
| 11 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 12 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 13 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Este registro tem por objetivo representar a escrituração do CF-e (código 59) segmentado por item  ou por CST (CST PIS/Pasep e CST Cofins), correspondente a receitas tributadas por quantidade de produtos vendidos;
2. No caso do detalhamento do CF-e ser efetuado por item do documento, deve ser gerado um registro para cada item vendido, conforme o código de item cadastrado no Registro 0200;
3. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST. Como também, no caso de a operação tributável incidir a alíquotas distintas.
4. Os valores escriturados nos campos de bases de cálculo 06 (QUANT_BC_PIS) e 10 (QUANT_BC_COFINS) correspondentes a itens vendidos com CST representativos de receitas tributadas por quantidade de produto vendido, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep e da Cofins, no Campo “QUANT_BC_PIS” do registro M210 e no Campo “QUANT_BC_PIS” do registro M610, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C820]
Campo 02 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações informadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 03 - Preenchimento: informar o valor do(s) item(ns) (produto e/ou serviço) constante(s) no documento fiscal.
Campo 04 – Preenchimento: informar neste campo o código do item, referente ao produto e/ou serviço objeto de individualização neste registro.
Validação: o valor informado neste campo (código do item) deve está informado e cadastrado no registro 0200 (Tabela de Identificação do Item).
Campo 05 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 03 | Operação Tributável com Alíquota por Unidade de Medida de Produto |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 06 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 06).
Campo 08 – Preenchimento:  informar o valor do PIS/Pasep referente ao item consolidado neste registro.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 06) multiplicado pela alíquota aplicável ao item (campo 07).
Campo 09 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 03 | Operação Tributável com Alíquota por Unidade de Medida de Produto |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 10 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 11 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 10).
Campo 12 – Preenchimento: informar o valor da Cofins referente ao item consolidado neste registro.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 10) multiplicado pela alíquota aplicável ao item (campo 11).
Campo 13 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de venda a consumidor final, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
<!-- End Registro C820 -->
<!-- Start Registro C830 -->
Registro C830: Processo Referenciado
Registro para complementação de informação por documento fiscal emitido – não disponível para escrituração no PVA

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C830” | C | 004 | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
| 03 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 - Outros. | C | 001* | - | S |

Observações:
1. registro é específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “C830”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referente ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C830]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C830 -->
<!-- Start Registro C860 -->
Registro C860: Identificação do Equipamento SAT-CF-e
Registro para escrituração pela pessoa jurídica, da receita da venda de bens e serviços mediante a emissão de cupom fiscal eletrônico – CF-e-SAT (código 59), conforme Ajuste SINIEF no 11, de 24 de setembro de 2010.
As operações de vendas com emissão de cupom fiscal eletrônico - CF-e-SAT devem ser escrituradas de forma consolidada por equipamento SAT-CF-e (no registro C860), com base nos totais de vendas diárias de cada equipamento, sendo as receitas demonstradas e segregadas no registro filho C870, para cada item vendido no dia.
Este registro tem por objetivo identificar os equipamentos SAT-CF-e.Não poderão ser informados dois ou mais registros com a mesma combinação COD_MOD, NR_SAT, DOC_INI e DOC_FIM.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C860" | C | 004 | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002 | - | S |
| 03 | NR_SAT | Número de Série do equipamento SAT | N | 009 | - | S |
| 04 | DT_DOC | Data de emissão dos documentos fiscais | N | 008 | - | N |
| 05 | DOC_INI | Número do documento inicial | N | 009 | - | N |
| 06 | DOC_FIM | Número do documento final | N | 009 | - | N |

Observações: Os registros referentes à escrituração do Cupom Fiscal Eletrônico – CF-e, código 59, estão disponíveis na versão 2.11 do Programa Validador e Assinador (PVA) da EFD-Contribuições, para a escrituração dos períodos de apuração a partir de 01 de maio de 2015. Para os períodos anteriores a maio de 2015, a escrituração do CF-e, deve ser efetuada no registro C400 ou C490.
Nível hierárquico: 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [C860]
Validação: não poderão existir dois ou mais registros para o conjunto COD_MOD e NR_SAT
Campo 02 – Preenchimento: deve corresponder ao código Cupom Fiscal Eletrônico (Valor Válido: 59).
Campo 03 - Preenchimento: informar o número de série do equipamento SAT .
Campo 04 - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: o valor informado no campo deve estar compreendido dentro das datas informadas no registro 0000, correspondendo assim a operações relacionadas ao período de apuração da escrituração das contribuições sociais.
Campo 05 - Preenchimento: informar o número do primeiro CF-e emitido, mesmo que cancelado, no período, pelo equipamento.
Validação: o valor informado deve ser menor ou igual ao valor informado no Campo 6.
Campo 06 - Preenchimento: informar o número do último CF-e emitido, mesmo que cancelado, no período, pelo
equipamento.
Validação: o valor informado deve ser maior ou igual ao valor informado no Campo 5.
<!-- End Registro C860 -->
<!-- Start Registro C870 -->
Registro C870: Resumo Diário de Documentos Emitidos por Equipamento SAT-Cf-e (Código 59) – PIS/Pasep e Cofins
Registro para demonstração da receita consolidada e apuração das contribuições sociais, por equipamento SAT-CF-e, referente aos documentos fiscais emitidos no período.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C870" | C | 004* | - | S |
| 02 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 03 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 04 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 05 | VL_DESC | Valor da exclusão/desconto comercial dos itens | N | - | 02 | N |
| 06 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 07 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N |   | 02 | N |
| 08 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 09 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 10 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 11 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N |   | 02 | N |
| 12 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 13 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 14 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Este registro tem por objetivo representar a escrituração consolidada das vendas diárias por equipamento SAT-CF-e, segmentado por CST (CST PIS/Pasep e CST Cofins) ou por item;
2. Na escrituração de suas operações diárias de cada equipamento SAT-CF-e, por item vendido, deve ser gerado um registro para cada item, conforme o código de item cadastrado no Registro 0200;
3. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST. Como também, no caso de a operação tributável incidir a alíquotas distintas;
4. Os valores escriturados nos campos de bases de cálculo 07 (VL_BC_PIS) e 11 (VL_BC_COFINS) correspondentes a itens vendidos com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep e da Cofins, nos Campos “VL_BC_CONT” dos registros M210 e M610, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C870]
Campo 02 – Preenchimento: informar neste campo o código do(s) item(ns), referente(s) ao produto e/ou serviço objeto de consolidação neste registro.
Validação: Quando informado este campo (código do item) deve o referido código cadastrado no registro 0200 (Tabela de Identificação do Item).
Campo 03 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP, relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 04 - Preenchimento: informar o valor do(s) item(ns) (produto e/ou serviço) constante(s) objeto de consolidação neste registro.
Campo 05 - Preenchimento: informar neste campo o valor das exclusões da base de cálculo do PIS/Pasep e da Cofins referente aos valores consolidados neste registro, no campo 04, para fins de apuração da contribuição social, conforme o caso. No caso de não ter exclusões em relação aos valores informados no campo 04, informar o valor "0,00" ou deixar em branco.
Campo 06 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 04 | Operação Tributável Monofásica - Revenda a Alíquota Zero |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 07 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente valores consolidados nesse registro, para fins de apuração da contribuição social, conforme o caso.
O valor a ser informado neste campo deve corresponder ao valor informado no Campo 04 (VL_ITEM) menos as exclusões de base de cálculo (vendas canceladas, descontos incondicionais, etc.) informadas no Campo 05, ocorridas no período.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de corresponder a fato gerador tributado da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 08 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 09 – Preenchimento: informar o valor do PIS/Pasep referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 07) multiplicado pela alíquota aplicável ao item (campo 08).
Exemplo: Sendo o Campo 07 (VL_BC_PIS) = 1.000.000,00 e o Campo 08 (ALIQ_PIS) = 1,6500, então o Campo 09 (VL_PIS) será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 10 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 01 | Operação Tributável com Alíquota Básica |
| 02 | Operação Tributável com Alíquota Diferenciada |
| 04 | Operação Tributável Monofásica - Revenda a Alíquota Zero |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 11 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referentes aos valores consolidados nesse registro, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de corresponder a fato gerador tributado da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 12 - Preenchimento: informar neste campo o valor da alíquota ad valorem aplicável para fins de apuração da contribuição social, conforme o caso.
Campo 13 – Preenchimento: informar o valor da Cofins referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 11) multiplicado pela alíquota aplicável ao item (campo 12).
Exemplo: Sendo o Campo 11 (VL_BC_COFINS) = 1.000.000,00 e o Campo 12 (ALIQ_COFINS) = 7,6000, então o Campo 13 (VL_COFINS) será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 14 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta analítica ou sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C870 -->
<!-- Start Registro C880 -->
Registro C880: Resumo Diário de Documentos Emitidos por Equipamento SAT-Cf-e (Código 59) – PIS/Pasep e Cofins Apurado por Unidade de Medida de Produto
Registro para demonstração por equipamento SAT-CF-e, da receita consolidada e da apuração das contribuições sociais por unidade de medida de produto, referente aos documentos fiscais CF-e emitidos pela pessoa jurídica produtora/fabricante e importadora dos produtos sujeitos a esse regime tributário (combustíveis, álcool, bebidas frias e embalagens para bebidas frias), e pessoa jurídica comercial de embalagem para bebidas frias.
A escrituração da receita da revenda de produtos monofásicos, pelas pessoas jurídicas comerciais, sujeitas a alíquota zero das contribuições, devem ser informadas no registro C870.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C880" | C | 004* | - | S |
| 02 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 03 | CFOP | Código fiscal de operação e prestação | N | 004* | - | S |
| 04 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 05 | VL_DESC | Valor da exclusão/desconto comercial dos itens | N | - | 02 | N |
| 06 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 07 | QUANT_BC_PIS | Base de cálculo em quantidade - PIS/PASEP | N | - | 03 | N |
| 08 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 09 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 10 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 11 | QUANT_BC_COFINS | Base de cálculo em quantidade – COFINS | N | - | 03 | N |
| 12 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 13 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 14 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Este registro tem por objetivo representar a escrituração consolidada das vendas diárias por equipamento SAT-DF-E, segmentado por CST (CST PIS/Pasep e CST Cofins) ou por item, correspondente a receitas tributadas por quantidade de produtos vendidos;
2. Na escrituração de suas operações diárias de cada equipamento SAT-CF-E, por item vendido, deve ser gerado um registro para cada item, conforme o código de item cadastrado no Registro 0200;
3. No caso de ocorrência de venda com CST distintos, deve ser gerado um registro para cada CST. Como também, no caso de a operação tributável incidir a alíquotas distintas;
4. Os valores escriturados nos campos de bases de cálculo 07 (QUANT_BC_PIS) e 11 (QUANT_BC_COFINS) correspondentes a itens vendidos com CST representativos de receitas tributadas por quantidade de produto vendido, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep e da Cofins, no Campo “QUANT_BC_PIS” do registro M210 e no Campo “QUANT_BC_PIS” do registro M610, respectivamente.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [C880]
Campo 02 – Preenchimento: informar neste campo o código do item, referente ao produto e/ou serviço objeto de escrituração neste registro.
Validação: o valor informado neste campo (código do item) deve está informado e cadastrado no registro 0200 (Tabela de Identificação do Item).
Campo 03 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações informadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 04 - Preenchimento: informar o valor do(s) item(ns) (produto e/ou serviço) constante(s) no documento fiscal.
Campo 05 - Preenchimento: informar neste campo o valor das exclusões da base de cálculo do PIS/Pasep e da Cofins referente aos valores consolidados neste registro, no campo 04, para fins de apuração da contribuição social, conforme o caso.
Deve ser ressaltado que, apesar de informar as exclusões neste campo, em moeda (reais), as exclusões a serem objeto de redução da base de cálculo do registro C880, nos campos 07 e 11, são em quantidades.
Campo 06 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 03 | Operação Tributável com Alíquota por Unidade de Medida de Produto |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 07 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 08 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 07).
Campo 09 – Preenchimento: informar o valor do PIS/Pasep referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo em quantidade (campo 07) multiplicado pela alíquota aplicável ao item (campo 08).
Campo 10 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Validação: o valor informado no campo deve constar na Tabela de Código de Situação Tributária – CST, abaixo:

| Código | Descrição |
| --- | --- |
| 03 | Operação Tributável com Alíquota por Unidade de Medida de Produto |
| 05 | Operação Tributável por Substituição Tributária |
| 06 | Operação Tributável a Alíquota Zero |
| 07 | Operação Isenta da Contribuição |
| 08 | Operação sem Incidência da Contribuição |
| 09 | Operação com Suspensão da Contribuição |
| 49 | Outras Operações de Saída |
| 99 | Outras Operações |

Campo 11 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 12 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 11).
Campo 13 – Preenchimento: informar o valor da Cofins referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo em quantidade (campo 11) multiplicado pela alíquota aplicável ao item (campo 12).
Campo 14 - Preenchimento: informar o Código da Conta Analítica. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de venda a consumidor final, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta analítica ou sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro C880 -->
<!-- Start Registro C890 -->
Registro C890: Processo Referenciado
1. registro é específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “C890”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referente ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C890” | C | 004 | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório | C | 020 | - | S |
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
Ocorrência - 1:N
Campo 01 - Valor Válido: [C890]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro C890 -->
<!-- Start Registro C990 -->
Registro C990: Encerramento do Bloco C
Este registro destina-se a identificar o encerramento do bloco C e informar a quantidade de linhas (registros) existentes no bloco.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "C990" | C | 004* | - | S |
| 02 | QTD_LIN_C | Quantidade total de linhas do Bloco C | N | - | - | S |

Observações: Registro obrigatório, se existir o Registro C001
Nível hierárquico - 1
Ocorrência – um por arquivo
Validação do Registro: registro único e obrigatório para todos os informantes da EFD-Contribuições.
Campo 01 - Valor Válido: [C990]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco C é igual ao valor informado no campo QTD_LIN_C (registro C990).
<!-- End Registro C990 -->