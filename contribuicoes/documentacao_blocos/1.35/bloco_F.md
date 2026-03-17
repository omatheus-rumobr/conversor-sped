# Bloco F - Versão 1.35

BLOCO F: Demais Documentos e Operações
Neste bloco serão informadas pela pessoa jurídica, as demais operações geradoras de contribuição ou de crédito, não informadas nos Blocos A, C e D, conforme tabela abaixo:

| Bloco | Registro | Operações a Escriturar |
| --- | --- | --- |
| A | - | Serviços prestados ou contratados, com emissão de nota fiscal |
| C | - | Venda e aquisição de mercadorias e produtos, com emissão de nota fiscal |
| D | - | Venda e aquisição de serviços de transportes e de comunicação/telecomunicação |
|   |   |   |
| F | F100 | 1. Demais receitas auferidas, da atividade ou não, tais como: receitas financeiras juros sobre o capital próprio aluguéis de bens móveis e imóveis receitas não operacionais (venda de bens do ativo não circulante) demais receitas não escrituradas nos Blocos A, C e D 2. Outras operações com direito a crédito, tais como: contraprestação de arrendamento mercantil aluguéis de prédios, máquinas e equipamentos despesas de armazenagem de mercadorias aquisição de bens e serviços a serem utilizados como insumos, com documentação que não deva ser informada nos Blocos A, C e D |
| F | F120 | Créditos com base nos encargos de depreciação/amortização, de bens incorporados ao ativo imobilizado. |
| F | F130 | Créditos com base no valor de aquisição de bens incorporados ao ativo imobilizado. |
| F | F150 | Crédito Presumido sobre o estoque de abertura |
| F | F200 | Receitas decorrentes da atividade imobiliária |
| F | F205 | Crédito apurado com base no custo incorrido da atividade imobiliária |
| F | F210 | Crédito apurado com base no custo orçado da atividade imobiliária |
| F | F600 | Demonstração dos valores retidos na fonte |
| F | F700 | Demonstração de outras deduções |
| F | F800 | Demonstração dos créditos decorrentes de eventos de incorporação, fusão e cisão |

No caso das informações serem escrituradas de forma centralizada pelo estabelecimento sede da pessoa jurídica, todas as operações serão registradas a partir do registro F010 do estabelecimento sede.
No caso das informações serem escrituradas por estabelecimentos, as operações devem ser registradas, de forma segregada, a partir dos diversos registros filhos de F010, de cada estabelecimento.
<!-- Start Registro F001 -->
Registro F001: Abertura do Bloco F
Registro obrigatório, indicador da existência ou não de informações no Bloco F.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F001" | C | 004* | - | S |
| 02 | IND_MOV | Indicador de movimento: 0- Bloco com dados informados; 1- Bloco sem dados informados | C | 001 | - | S |

Observações:
Nível hierárquico - 1
Ocorrência – um por arquivo.
Campo 01 - Valor Válido: [F001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco F (F001 e F990). Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro F001 -->
<!-- Start Registro F010 -->
Registro F010: Identificação do Estabelecimento
Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica a que se referem as operações e documentos fiscais informados neste bloco. Só devem ser escriturados no Registro F010 os estabelecimentos da pessoa jurídica que efetivamente tenham realizado operações passíveis de escrituração neste bloco.
O estabelecimento que não realizou operações passíveis de registro no bloco F, no período da escrituração, não deve ser identificado no Registro F010.
Para cada estabelecimento cadastrado em “F010”, deve ser informado nos registros de nível inferior (Registros Filhos) as operações próprias do bloco, que tenham sido praticadas no período da escrituração.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “F010”. | C | 004* | - | S |
| 02 | CNPJ | Número de inscrição do estabelecimento no CNPJ. | N | 014* | - | S |

Observações: Registro obrigatório.
Nível hierárquico - 2
Ocorrência – vários por arquivo
Campo 01 - Valor Válido: [F010];
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações passíveis de escrituração neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deve está cadastrado no Registro 0140.
<!-- End Registro F010 -->
<!-- Start Registro F100 -->
Registro F100: Demais Documentos e Operações Geradoras de Contribuição e Créditos
Deverão ser informadas no Registro F100 as demais operações que, em função de sua natureza ou documentação, não sejam passíveis de serem escrituradas em registros próprios dos Blocos A, C, D e F.
Devem ser informadas no registro F100 as operações representativas das demais receitas auferidas, com incidência ou não das contribuições sociais, bem como das demais aquisições, despesas, custos e encargos com direito à apuração de créditos das contribuições sociais, que devam constar na escrituração do período, tais como:
- Receitas Financeiras auferidas no período;
- Receitas auferidas de Juros sobre o Capital Próprio;
- Receitas de Aluguéis auferidas no período;
- Montante do faturamento atribuído a pessoa jurídica associada/cooperada, decorrente da produção entregue a sociedade cooperativa para comercialização, conforme documento (extrato, demonstrativo, relatório, etc) emitido pela sociedade cooperativa;
- Outras receitas auferidas, operacionais ou não operacionais, não vinculadas à emissão de documento fiscal específico;
- Despesas de Aluguéis de prédios, máquinas e equipamentos utilizados nas atividades da empresa;
- Contraprestações de Arrendamento Mercantil;
- Despesa de armazenagem de mercadorias;
- Receitas e operações com direito a crédito, vinculadas a consórcio, contratos de longo prazo, etc., cujos documentos que a comprovem ou validem não sejam notas fiscais, objeto de relacionamento nos Blocos A, C ou D;
- aquisição de bens e serviços a serem utilizados como insumos, com documentação que não deva ser informada nos Blocos A, C e D;
- Operações de importação de mercadorias para revenda ou produtos a serem utilizados com insumos, quando a apropriação dos créditos ocorrer amparada pela DI (na competência do desembaraço aduaneiro) e não pela entrada da mercadoria com a nota fiscal correspondente;
- A escrituração de crédito presumido a ser apurado pelas empresas de serviço de transporte rodoviário de carga, decorrente de operação de subcontratação de serviço de transporte de carga prestado por pessoa física, transportador autônomo, ou por pessoa jurídica transportadora optante pelo Simples, conforme disposto nos §§ 19 e 20 do art. 3º da Lei nº 10.833, de 2003, calculado mediante a aplicação das alíquotas de 1,2375 % (PIS/Pasep) e de 5,7%, conforme Tabela 4.3.17. Na escrituração desses créditos presumidos no registro F100, devem ser observadas as orientações constantes do registro D100 e registros filhos, em relação às regras de preenchimento dos campos comuns.
ATENÇÃO:
Devem ser escriturados no Registro F100 os créditos presumidos incidentes sobre as receitas de venda de produtos específicos, como por exemplo, os incidentes sobre a receita de exportação de café (Lei nº 12.599/2012), sobre a receita decorrente da venda no mercado interno ou da exportação dos produtos derivados da soja, margarina e biodiesel (Lei nº 12.865/2013), bem como de quaisquer outros que venham a ser previstos na legislação tributária, conforme exemplo abaixo.
Considerando que a empresa tenha direito a crédito presumido relativo à receita de exportação dos produtos classificados no código 0901.1 da Tipi (café não torrado), no valor de R$ 1.000.000,00, a escrituração do crédito será efetuada, no registro “F100”, conforme abaixo:
- Campo IND_OPER: 0 (Operação sujeita a incidência de crédito)
- Campo VL_OPER: R$ 1.000.000,00 (receita de exportação de café)
- Campo CST PIS: 62
- Campo VL_BC_PIS: R$ 1.000.000,00
- Campo ALIQ_PIS: 0,1650% (Item 110 da Tabela 4.3.9)
- Campo VL_PIS: R$ 1.650,00
- Campo CST COFINS: 62
- Campo VL_BC_COFINS: R$ 1.000.000,00
- Campo ALIQ_COFINS: 0,76% (Item 110 da Tabela 4.3.9)
- Campo VL_COFINS: R$ 7.600,00
- Campo NAT_BC_CRED: 13 (*)
(*) Uma vez informado “NAT_BC_CRED” = 13 (outras operações com direito a crédito), deverá ser preenchido o campo “DESC_CRED”, nos registros M105 e M505, com a descrição do crédito, como por exemplo “Crédito Presumido da Exportação de café – Lei nº 12.599/2012”.
Caso ocorram devoluções de vendas, cujas receitas estejam sujeitas ao cálculo do crédito presumido, os correspondentes valores devem ser excluídos na base de cálculo do PIS/Pasep (campo "VL_BC_PIS") e da Cofins (campo "VL_BC_COFINS").
As operações relacionadas neste registro devem ser demonstradas de forma individualizada quando se referirem a operações com direito a crédito da não cumulatividade, como nos casos de contratos de locação de bens móveis e imoveis, das contraprestações de arrendamento mercantil, etc.
As operações referentes às demais receitas auferidas, tributadas ou não, devem ser individualizadas no registro F100 em função da sua natureza e tratamento tributário, tais como:
Rendimentos de aplicações financeiras;
Receitas de títulos vinculados ao mercado aberto;
Receitas decorrentes de consórcio constituído nos termos do disposto nos arts. 278 e 279 da Lei nº 6.404, de 1976;
Receitas de locação de bens móveis e imóveis;
Receita da venda de bens imóveis do ativo não-circulante;
Juros sobre o Capital Próprio recebidos;
Receitas decorrentes da execução por administração, empreitada ou subempreitada, de obras de construção civil;
Receita auferida com produtos e serviços, convencionada e estipulada mediante contrato;
Montante do faturamento atribuído a pessoa jurídica associada/cooperada;
Receitas da prestação de serviços de educação e da área de saúde, etc.
Podem ser demonstradas de forma consolidada as operações que, em função de sua natureza, volume ou detalhamento, dispensa a sua individualização, como por exemplo, na demonstração dos rendimentos de aplicações financeiras oriundos de investimentos diversos ou em contas diversas, consolidando as operações por instituição financeira:
Rendimentos de aplicação financeira – Banco X;
Rendimentos de aplicação financeira – Banco Y.
As operações que não se refiram a um estabelecimento específico da pessoa jurídica devem ser relacionadas nos registros filhos do Registro F010 do estabelecimento centralizador da escrituração (estabelecimento sede).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F100" | C | 004* | - | S |
| 02 | IND_OPER | Indicador do Tipo da Operação: 0 – Operação Representativa de Aquisição, Custos, Despesa ou Encargos, ou Receitas, Sujeita à Incidência de Crédito de PIS/Pasep ou Cofins (CST 50 a 66). 1 – Operação Representativa de Receita Auferida Sujeita ao Pagamento da Contribuição para o PIS/Pasep e da Cofins (CST 01, 02, 03 ou 05). 2 - Operação Representativa de Receita Auferida Não Sujeita ao Pagamento da Contribuição para o PIS/Pasep e da Cofins (CST 04, 06, 07, 08, 09, 49 ou 99). | C | 001* | - | S |
| 03 | COD_PART | Código do participante (Campo 02 do Registro 0150) | C | 060 | - | N |
| 04 | COD_ITEM | Código do item (campo 02 do Registro 0200) | C | 060 | - | N |
| 05 | DT_OPER | Data da Operação (ddmmaaaa) | N | 008* | - | S |
| 06 | VL_OPER | Valor da Operação/Item | N | - | 02 | S |
| 07 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 08 | VL_BC_PIS | Base de cálculo do PIS/PASEP | N | - | 04 | N |
| 09 | ALIQ_PIS | Alíquota do PIS/PASEP | N | 008 | 04 | N |
| 10 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 11 | CST_COFINS | Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 12 | VL_BC_COFINS | Base de cálculo da COFINS | N | - | 04 | N |
| 13 | ALIQ_COFINS | Alíquota da COFINS | N | 008 | 04 | N |
| 14 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 15 | NAT_BC_CRED | Código da Base de Cálculo dos Créditos, conforme a tabela indicada no item 4.3.7, caso seja informado código representativo de crédito nos Campos 07 (CST_PIS) e 11 (CST_COFINS). | C | 002* | - | N |
| 16 | IND_ORIG_CRED | Indicador da origem do crédito: 0 – Operação no Mercado Interno 1 – Operação de Importação | C | 001* | - | N |
| 17 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 18 | COD_CCUS | Código do Centro de Custos | C | 255 | - | N |
| 19 | DESC_DOC_OPER | Descrição do Documento/Operação | C | - | - | N |

Observações:
1. Os valores escriturados nos campos de bases de cálculo 08 (VL_BC_PIS) e 12 (VL_BC_COFINS), de itens com CST representativos de receitas tributadas (CST 01, 02, 03 e 05), serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210) e da Cofins (M610), nos Campos “VL_BC_CONT”, respectivamente.
2. Os valores escriturados nos campos de bases de cálculo 08 (VL_BC_PIS) e 12 (VL_BC_COFINS), de itens com CST representativos de operações com direito a crédito (CST 50 a 56; 60 a 67), serão recuperados no Bloco M, para a demonstração das bases de cálculo dos créditos de PIS/Pasep (M105) e dos créditos de Cofins (M505) nos Campos “VL_BC_PIS_TOT”, respectivamente.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [F100];
Campo 02 - Preenchimento: Informar neste campo o indicador do tipo ou natureza da operação.
Valores Válidos: [0, 1, 2]
Nas operações representativas de receitas, deve ser informado o indicador correspondente ao tratamento tributário (CST) da receita informada neste registro. Se referente a uma operação tributável (CST 01, 02, 03 ou 05) informar o indicador “1”; se referente a uma operação não tributável, ou tributável  à alíquota zero (CST 04, 05, 06, 07, 08, 09, 49 ou 99) informar o indicador “2”.
Nas operações representativas de aquisições, custos ou despesas com direito a crédito (CST 50 a 66), deve ser informado o indicador “0”, correspondente à operação com direito a crédito. As operações sem direito a crédito não precisam ser escrituradas em F100.
Campo 03 - Validação: o código informado neste campo deve está relacionado no registro 0150, no campo COD_PART.
No caso do registro se referir a uma operação representativa de receita (Campo IND_OPER = “1” e “2”) o Campo 03 não é de preenchimento obrigatório, como no caso de receitas financeiras auferidas em instituições financeiras diversas. Neste caso, a pessoa jurídica deve complementar o registro com informações complementares no Campo 19.
No caso do registro se referir a uma operação representativa de crédito (Campo IND_OPER = “0”) o Campo 03 é de preenchimento obrigatório, devendo ser informado o código de participante referente ao fornecedor/prestador de serviço, cadastrado no Registro 0150.
Campo 04 - Preenchimento: o código do item a que se refere a operação informado neste campo, quando existir, deve está relacionado no registro 0200, ressaltando-se que os códigos informados devem ser os definidos pelo pessoa jurídica titular da escrituração.
Campo 05 - Preenchimento: informar a data da operação escriturada neste registro, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
No caso da operação não se referir a um dia específico, ou se referir a mais de um dia, deve ser informado o dia final de referência ou o ultimo dia do período da escrituração, conforme o caso.
Campo 06 – Preenchimento: Informar o valor total da operação/item escriturado neste registro.
Campo 07 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 08 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à operação/item, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
ATENÇÃO: Como regra geral de tributação, a base de cálculo das contribuições é expressa em reais (receita ou faturamento), com duas casas decimais. No caso da tributação por unidade de medida de produto (fabricante de combustíveis e bebidas frias) a base de cálculo é expressa em quantidade vendida. Desta forma, os fabricantes de combustíveis e bebidas frias (cervejas, refrigerantes, etc) ao informarem este campo, com três ou quatro casas decimais, as mesmas serão automaticamente arredondadas, pelo PVA, na geração da apuração e na validação do registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “VL_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 09 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 10 – Preenchimento: informar o valor do PIS/Pasep (contribuição ou crédito) referente à operação/item escriturado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição e/ou do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500 e VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (VL_BC_PIS) multiplicado pela alíquota aplicável ao item (ALIQ_PIS). No caso de aplicação da alíquota do campo 09, em percentual, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500, então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 11 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 12 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à operação/item, para fins de apuração da contribuição social ou de apuração do crédito, conforme o caso.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
ATENÇÃO: Como regra geral de tributação, a base de cálculo das contribuições é expressa em reais (receita ou faturamento), com duas casas decimais. No caso da tributação por unidade de medida de produto (fabricante de combustíveis e bebidas frias) a base de cálculo é expressa em quantidade vendida. Desta forma, os fabricantes de combustíveis e bebidas frias (cervejas, refrigerantes, etc) ao informarem este campo, com três ou quatro casas decimais, as mesmas serão automaticamente arredondadas, pelo PVA, na geração da apuração e na validação do registro.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de item correspondente a fato gerador da contribuição social, ou para a demonstração das bases de cálculo do crédito de Cofins (M505, campo “VL_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 13 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição social ou do crédito, conforme o caso.
Campo 14 – Preenchimento: informar o valor da Cofins (contribuição ou crédito) referente à operação/item escriturado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição e/ou do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500 e VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (VL_BC_COFINS) multiplicado pela alíquota aplicável ao item (ALIQ_COFINS). No caso de aplicação da alíquota do campo 13, em percentual, o resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000, então o Campo “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 15 - Preenchimento: Caso seja informado código representativo de crédito no Campo 07 (CST_PIS) ou no Campo 11 (CST_COFINS) deste registro, informar neste campo o código da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 16 - Valores válidos: [0, 1]
Preenchimento: No caso de registro representativo de operação com direito a crédito, informar o código que indique se a operação tem por origem o mercado interno ou externo (importação de bens e serviços).
Campo 17 - Preenchimento: informar o Código da Conta Analítica. Exemplos: estoques, receitas da atividade, receitas não operacionais, custos, despesas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 18 - Preenchimento: Nos registros correspondentes às operações com direito a crédito, informar neste campo o Código do Centro de Custo relacionado à operação, se existir.
Campo 19 - Preenchimento: Neste campo pode ser informada a descrição complementar da operação ou do item, objeto de escrituração neste registro. Por exemplo, no caso de operações relativas a consórcios, pode ser informado neste campo o documento arquivado no órgão de registro, bem como a participação percentual da pessoa jurídica consorciada no empreendimento.
<!-- End Registro F100 -->
<!-- Start Registro F111 -->
Registro F111: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou de créditos.
2. Uma vez procedida à escrituração do Registro “F111”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | REG | Texto fixo contendo "F111" | C | 004* | - | S |
| 002 | NUM_PROC | Identificação do processo ou ato concessório. | C | 020 | - | S |
| 003 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - | S |

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
Campo 01 - Valor Válido: [F111]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F111 -->
<!-- Start Registro F120 -->
Registro F120: Bens Incorporados ao Ativo Imobilizado – Operações Geradoras de Créditos com Base nos Encargos de Depreciação e Amortização
Registro específico para a escrituração dos créditos determinados com base nos encargos de depreciação de bens incorporados ao Ativo Imobilizado da pessoa jurídica, adquirido para utilização na produção de bens destinados à venda, ou na prestação de serviços, bem como de encargos de amortização relativos a edificações e benfeitorias em imóveis próprios ou de terceiros.
As informações geradas neste registro referem-se aos bens incorporados ao Ativo Imobilizado ou às edificações e benfeitorias em imóveis próprios ou de terceiros que, em função de sua natureza, NCM, destinação ou data de aquisição, a legislação tributária permite o direito ao crédito de PIS/Pasep e de Cofins com base nos encargos de depreciação ou amortização incorridos no período da escrituração.
Os valores informados neste registro devem corresponder aos encargos de depreciação ou amortização incorridos em cada período, objeto de escrituração contábil pela pessoa jurídica, referente exclusivamente aos bens e edificações com direito a crédito, na forma da legislação tributária.
IMPORTANTE: Os bens incorporados ao Ativo Imobilizado da pessoa jurídica que foram considerados no computo do crédito determinado com base no valor de aquisição, escriturado no Registro F130, não devem ser relacionados e escriturados neste Registro F120.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F120" | C | 004* | - | S |
| 02 | NAT_BC_CRED | Código da Base de Cálculo do Crédito sobre Bens Incorporados ao Ativo Imobilizado, conforme a Tabela indicada no item 4.3.7: 09 = Crédito com Base nos Encargos de Depreciação; 11 = Crédito com Base nos Encargos de Amortização | C | 002* | - | S |
| 03 | IDENT_BEM_IMOB | Identificação dos Bens/Grupo de Bens Incorporados ao Ativo Imobilizado: 01 = Edificações e Benfeitorias em Imóveis Próprios; 02 = Edificações e Benfeitorias em Imóveis de Terceiros; 03 = Instalações; 04 = Máquinas; 05 = Equipamentos; 06 = Veículos; 99 = Outros . | N | 002* | - | S |
| 04 | IND_ORIG_CRED | Indicador da origem do bem incorporado ao ativo imobilizado, gerador de crédito: 0 – Aquisição no Mercado Interno 1 – Aquisição no Mercado Externo (Importação) | C | 001* | - | N |
| 05 | IND_UTIL_BEM_IMOB | Indicador da Utilização dos Bens Incorporados ao Ativo Imobilizado: 1 – Produção de Bens Destinados a Venda; 2 – Prestação de Serviços; 3 – Locação a Terceiros; 9 – Outros. | N | 001* | - | S |
| 06 | VL_OPER_DEP | Valor do Encargo de Depreciação/Amortização Incorrido no Período | N | - | 02 | S |
| 07 | PARC_OPER_NAO_BC_CRED | Parcela do Valor do Encargo de Depreciação/Amortização a excluir da base de cálculo de Crédito | N | - | 02 | N |
| 08 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 09 | VL_BC_PIS | Base de cálculo do Crédito de PIS/PASEP no período (06 – 07) | N | - | 02 | N |
| 10 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 11 | VL_PIS | Valor do Crédito de PIS/PASEP | N | - | 02 | N |
| 12 | CST_COFINS | Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 13 | VL_BC_COFINS | Base de Cálculo do Crédito da COFINS no período (06 – 07) | N | - | 02 | N |
| 14 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 15 | VL_COFINS | Valor do crédito da COFINS | N | - | 02 | N |
| 16 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 17 | COD_CCUS | Código do Centro de Custos | C | 255 | - | N |
| 18 | DESC_ BEM_IMOB | Descrição complementar do bem ou grupo de bens, com crédito apurado com base nos encargos de depreciação ou amortização. | C | - | - | N |

Observações: Em relação aos itens com CST representativos de operações geradoras de créditos, os valores dos Campos de base de cálculo “VL_BC_PIS” (Campo 09) e “VL_BC_COFINS” (Campo 13) serão recuperados no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105), no campo “VL_BC_PIS_TOT” e do crédito da Cofins (M505), no Campo “VL_BC_COFINS_TOT”.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [F120]
Campo 02 - Preenchimento: Informar neste registro o código correspondente à natureza da base de cálculo do crédito (Se Depreciação = 09 e se Amortização = 11), conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Valores Válidos: [09,11]
Campo 03 - Preenchimento: informar neste campo o código correspondente à identificação do bem ou grupo de bens (informação por gênero/grupo de bens) Incorporados ao Ativo Imobilizado, cujo encargo de depreciação ou amortização permite o direito ao crédito.
A identificação dos bens incorporados ao Ativo Imobilizado a ser informado no Campo 03 (IDENT_BEM_IMOB) pode ser realizada de forma individualizada ou por grupos de bens da mesma natureza ou destinação.
OBS: No caso do registro F120 se referir a grupo de bens correspondente a mais de um código de identificação como, por exemplo, “Maquinas e Equipamentos”, pode  a pessoa jurídica informar no Campo 03 quaisquer um dos códigos a que se refira o grupo de bens.
Valores Válidos: [01,02,03,04,05,06,99]
Campo 04 - Preenchimento: Informar neste campo o código que indique se a origem (País de aquisição) do bem incorporado ao ativo imobilizado, se no mercado interno ou externo (importação de bens e serviços). No caso do registro contábil do bem ou grupo de bens incorporados ao imobilizado, objeto de crédito com base nos encargos de depreciação, não identificar a origem do bem ou grupo de bens, o campo pode ser informado sem o indicador de origem. Nesse caso (campo em branco), em que o registro não identifica a aquisição como sendo no mercado externo (importação) – Indicador “1”, o PVA irá considerar o crédito como sendo de aquisição no mercado interno – Indicador “0”.
Campo 05 - Preenchimento: Informar neste campo o indicador correspondente à destinação ou utilização dos bens geradores de crédito neste registro. Caso o bem/grupo de bens relacionados aos créditos deste registro não estejam sendo utilizados entre as hipóteses previstas em lei para a apuração de créditos (Indicadores 1, 2 e 3), deve ser informado o indicador 9.
Registre-se que a legislação tributária não estabelece o direito ao crédito em relação aos bens incorporados ao ativo imobilizado:
- Cuja data de aquisição seja anterior a maio de 2004, conforme disposição do art. 31 da Lei nº 10.865/2004;
- que não seja utilizado na produção de bens, prestação de serviços e locação. Desta forma, as máquinas, equipamentos, instalações e outros bens móveis utilizados na área administrativa, comercial, gerencial, de processamento de dados, almoxarifado, etc., não tem previsão em lei para a apropriação de crédito.
Os encargos de depreciação e amortização referentes às edificações e benfeitorias em imóveis próprios ou de terceiros, utilizados nas atividades da pessoa jurídica dão direito a crédito.
Valores válidos: [1,2,3,9]
Campo 06 - Preenchimento: informar neste campo o valor do encargo de depreciação ou de amortização, incorrido no período, referente ao(s) bem(ns) objeto de escrituração neste registro.
Campo 07 - Preenchimento: informar neste campo a parcela do valor dos encargos de depreciação ou amortização informados no Campo 06, que a legislação não permite o direito à apuração de crédito, tais como os encargos de depreciação/amortização sobre bens incorporados ao imobilizado:
- adquiridos de pessoa física domiciliada no país;
- não sujeitos ao pagamento da contribuição social, quando de sua aquisição;
- de edificações e benfeitorias em imóveis próprios ou de terceiros, não utilizados nas atividades da empresa;
- de maquinas, equipamentos e outros bens, não utilizados na produção de bens destinados à venda, na locação a terceiros ou na prestação de serviços.
Os valores informados no campo 07 devem ser excluídos da base de cálculo dos créditos (Campo 09).
Campo 08 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 09 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à operação/item, para fins de apuração do crédito, conforme o caso.
Validação: [Campo 09 = Campo 06 – Campo 07]
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “VL_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 10 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito.
Campo 11 – Preenchimento: informar o valor do PIS/Pasep referente à operação/item escriturado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (VL_BC_PIS) multiplicado pela alíquota aplicável ao item (ALIQ_PIS), dividido pelo valor “100”
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500, então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 12 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 13 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à operação/item, para fins de apuração do crédito, conforme o caso.
Validação: [Campo 13 = Campo 06 – Campo 07]
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de Cofins (M505, campo “VL_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 14 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito.
Campo 15 – Preenchimento: informar o valor da Cofins referente à operação/item escriturado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (VL_BC_COFINS) multiplicado pela alíquota aplicável ao item (ALIQ_COFINS), dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000, então o Campo “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 16 - Preenchimento: informar o Código da Conta Analítica. Exemplos: encargos de depreciação do período, encargos de amortização do período, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 17 - Preenchimento: Nos registros correspondentes às operações com direito a crédito, informar neste campo o Código do Centro de Custo relacionado à operação, se existir.
Campo 18 - Preenchimento: Neste campo pode ser informada a descrição complementar do bem ou grupo de bens, com crédito apurado com base nos encargos de depreciação ou amortização, objeto de escrituração neste registro.
<!-- End Registro F120 -->
<!-- Start Registro F129 -->
Registro F129: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou de créditos.
2. Uma vez procedida à escrituração do Registro “F129”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | REG | Texto fixo contendo "F129" | C | 004* | - | S |
| 002 | NUM_PROC | Identificação do processo ou ato concessório. | C | 020 | - | S |
| 003 | IND_PROC | Indicador da origem do processo: 1 - Justiça Federal; 3 – Secretaria da Receita Federal do Brasil 9 – Outros. | C | 001* | - | S |

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
Campo 01 - Valor Válido: [F129]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F129 -->
<!-- Start Registro F130 -->
Registro F130: Bens Incorporados ao Ativo Imobilizado – Operações Geradoras de Créditos com Base no Valor de Aquisição/Contribuição
Registro específico para a escrituração dos créditos determinados com base no valor de aquisição de bens incorporados ao Ativo Imobilizado da pessoa jurídica, adquiridos para utilização na produção de bens destinados à venda, ou na prestação de serviços que, em função de sua natureza, NCM, destinação ou data de aquisição, a legislação tributária permite o direito ao crédito de PIS/Pasep e de Cofins com base no seu valor de aquisição.
A identificação dos bens incorporados ao Ativo Imobilizado a ser informado no Campo 03 (IDENT_BEM_IMOB) pode ser realizada de forma individualizada ou por gênero/grupo de bens da mesma natureza ou destinação.
IMPORTANTE: Os bens incorporados ao Ativo Imobilizado da pessoa jurídica que foram considerados no computo do crédito determinado com base nos encargos de depreciação/amortização, objeto de escrituração no Registro F120, não devem ser relacionados e escriturados neste Registro F130.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F130" | C | 004* | - | S |
| 02 | NAT_BC_CRED | Texto fixo contendo "10" (Código da Base de Cálculo do Crédito sobre Bens Incorporados ao Ativo Imobilizado, conforme a Tabela indicada no item 4.3.7) | C | 002* | - | S |
| 03 | IDENT_BEM_IMOB | Identificação dos bens ou grupo de bens incorporados ao Ativo Imobilizado: 01 = Edificações e Benfeitorias; 03 = Instalações; 04 = Máquinas; 05 = Equipamentos; 06 = Veículos; 99 = Outros bens incorporados ao Ativo Imobilizado. | N | 002* | - | S |
| 04 | IND_ORIG_CRED | Indicador da origem do bem incorporado ao ativo imobilizado, gerador de crédito: 0 – Aquisição no Mercado Interno 1 – Aquisição no Mercado Externo (Importação) | C | 001* | - | N |
| 05 | IND_UTIL_BEM_IMOB | Indicador da Utilização dos Bens Incorporados ao Ativo Imobilizado: 1 – Produção de Bens Destinados a Venda; 2 – Prestação de Serviços; 3 – Locação a Terceiros; 9 – Outros. | N | 001* | - | S |
| 06 | MES_OPER_AQUIS | Mês/Ano de Aquisição dos Bens Incorporados ao Ativo Imobilizado, com apuração de crédito com base no valor de aquisição. | N | 006* |   | N |
| 07 | VL_OPER_AQUIS | Valor de Aquisição dos Bens Incorporados ao Ativo Imobilizado – Crédito com base no valor de aquisição. | N | - | 02 | S |
| 08 | PARC_OPER_NAO_BC_CRED | Parcela do Valor de Aquisição a excluir da base de cálculo de Crédito | N | - | 02 | N |
| 09 | VL_BC_CRED | Valor da Base de Cálculo do Crédito sobre Bens Incorporados ao Ativo Imobilizado (07 – 08) | N | - | 02 | S |
| 10 | IND_NR_PARC | Indicador do Número de Parcelas a serem apropriadas (Crédito sobre Valor de Aquisição): 1 – Integral (Mês de Aquisição); 2 – 12 Meses; 3 – 24 Meses; 4 – 48 Meses; 5 – 6 Meses (Embalagens de bebidas frias) 9 – Outra periodicidade definida em Lei. | N | 001* | - | S |
| 11 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 12 | VL_BC_PIS | Base de cálculo Mensal do Crédito de PIS/PASEP, conforme indicador informado no campo 10. | N | - | 02 | N |
| 13 | ALIQ_PIS | Alíquota do PIS/PASEP | N | 008 | 04 | N |
| 14 | VL_PIS | Valor do Crédito de PIS/PASEP | N | - | 02 | N |
| 15 | CST_COFINS | Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 16 | VL_BC_COFINS | Base de Cálculo Mensal do Crédito da COFINS, conforme indicador informado no campo 10. | N | - | 02 | N |
| 17 | ALIQ_COFINS | Alíquota da COFINS | N | 008 | 04 | N |
| 18 | VL_COFINS | Valor do crédito da COFINS | N | - | 02 | N |
| 19 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 20 | COD_CCUS | Código do Centro de Custos | C | 255 | - | N |
| 21 | DESC_ BEM_IMOB | Descrição complementar do bem ou grupo de bens, com crédito apurado com base no valor de aquisição. | C | - | - | N |

Observações: Em relação aos itens com CST representativos de operações geradoras de créditos, os valores dos Campos de bases de cálculo “VL_BC_PIS” (Campo 12) e “VL_BC_COFINS” (Campo 16) serão recuperados no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105), no campo “VL_BC_PIS_TOT” e do crédito da Cofins (M505), no Campo “VL_BC_COFINS_TOT”.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [F130]
Campo 02 - Preenchimento: Informar neste registro o código correspondente à natureza da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Valor Válido: [10]
Campo 03 - Preenchimento: informar neste campo o código correspondente à identificação do bem ou grupo de bens (informação por gênero/grupo de bens) Incorporados ao Ativo Imobilizado, cujo crédito está sendo determinado com base no valor de aquisição.
A identificação dos bens incorporados ao Ativo Imobilizado a ser informado no Campo 03 (IDENT_BEM_IMOB) pode ser realizada de forma individualizada ou por grupos de bens da mesma natureza ou destinação.
OBS: No caso do registro F130 se referir a grupo de bens correspondente a mais de um código de identificação como, por exemplo, “Maquinas e Equipamentos”, pode a pessoa jurídica informar no Campo 03 quaisquer um dos códigos a que se refira o grupo de bens.
Valores Válidos: [01,02,03,04,05,06,99]
Campo 04 - Preenchimento: Informar neste campo o código que indique se a origem (País de aquisição) do bem incorporado ao ativo imobilizado, se no mercado interno ou externo (importação de bens e serviços).
Valores válidos: [0,1]
Campo 05 - Preenchimento: Informar neste campo o indicador correspondente à destinação ou utilização dos bens geradores de crédito neste registro. Caso o bem/grupo de bens relacionados aos créditos deste registro não estejam sendo utilizados entre as hipóteses previstas em lei para a apuração de créditos (Indicadores 1, 2 e 3), deve ser informado o indicador 9.
Registre-se que a legislação tributária não estabelece o direito ao crédito em relação aos bens incorporados ao ativo imobilizado:
- Cuja data de aquisição seja anterior a maio de 2004, conforme disposição do art. 31 da Lei nº 10.865/2004;
- Que não seja utilizado na produção de bens, prestação de serviços e locação. Desta forma, as máquinas, equipamentos, instalações e outros bens móveis utilizados na área administrativa, comercial, gerencial, de processamento de dados, almoxarifado, etc., não tem previsão em lei para a apropriação de crédito.
Valores válidos: [1,2,3,9]
Campo 06 - Preenchimento: informar neste campo o mês e ano de aquisição do bem ou grupo de bens incorporados ao ativo imobilizado, com apuração de crédito com base no valor de aquisição valor.  No caso da escrituração ser por grupo de bens, com datas de aquisição diversas, escriturar o registro com o campo em branco.
Campo 07 - Preenchimento: informar neste campo o valor de aquisição dos bens incorporados ao ativo imobilizado, cujo crédito for determinado com base no valor de aquisição, referente ao(s) bem(ns) objeto de escrituração neste registro.
Campo 08 - Preenchimento: informar neste campo a parcela do valor de aquisição a excluir da base de cálculo do crédito, em função de vedação na legislação quanto à apuração de crédito, tais as aquisições de bens incorporados ao imobilizado:
- adquiridos de pessoa física domiciliada no país;
- não sujeitos ao pagamento da contribuição social, quando de sua aquisição;
- de maquinas, equipamentos e outros bens, não utilizados na produção de bens destinados à venda, na locação a terceiros ou na prestação de serviços.
Os valores informados no campo 08 devem ser excluídos da base de cálculo dos créditos (Campo 09).
Campo 09 - Preenchimento: informar neste campo o valor total da base de cálculo do PIS/Pasep referente à operação/item, para fins de apuração do valor total do crédito.
Validação: [Campo 09 = Campo 07 – Campo 08]
Campo 10 - Preenchimento: informar neste campo o código correspondente ao número de parcelas a serem apropriadas, mensalmente, em relação ao valor total do crédito informado (Crédito sobre Valor de Aquisição):
1 – Integral (Mês de Aquisição);
2 – 12 Meses;
3 – 24 Meses;
4 – 48 Meses;
5 – 6 Meses (Embalagens de bebidas frias)
9 – Outra periodicidade definida em Lei.
OBS: Na hipótese de aquisição no mercado interno ou de importação de máquinas e equipamentos destinados à produção de bens e prestação de serviços, a partir de 03/08/2011, cujo crédito venha a ser apurado e descontado em prazo inferior a 12 meses, conforme previsto na Medida Provisória nº 540, de 2011, deve ser informado neste campo o indicador “09”. Neste caso, o período de aquisição informado no campo 06 “MES_OPER_AQUIS”, servirá como indicador e identificador do número de meses a apropriar o crédito em referência.
Valores Válidos: [1,2,3,4,5,9]
Campo 11 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 12 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep a ser apropriada no mês da escrituração, em função da quantidade de meses informada no Campo 10. O valor da base de cálculo do crédito do mês será determinado, sobre o valor total da base de cálculo informada no Campo 09, dividido pelo número de meses correspondente aos indicadores informados no Campo 10.
Validação: [Campo 12 = Campo 09 / Nº de Meses informados no Campo 10]
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “VL_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 13 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito.
Campo 14 – Preenchimento: informar o valor do PIS/Pasep referente à operação/item escriturado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento dos campos VL_CRED em M100/M500.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (VL_BC_PIS) multiplicado pela alíquota aplicável ao item (ALIQ_PIS), dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 15 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 16 - Preenchimento: informar neste campo o valor da base de cálculo de Cofins a ser apropriada no mês da escrituração, em função da quantidade de meses informada no Campo 10. O valor da base de cálculo do crédito do mês será determinado, sobre o valor total da base de cálculo informada no Campo 09, dividido pelo número de meses correspondente aos indicadores informados no Campo 10.
Validação: [Campo 16 = Campo 09 / Nº de Meses informados no Campo 10]
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de Cofins (M505, campo “VL_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 17 - Preenchimento: informar neste campo o valor da alíquota de Cofins aplicável para fins de apuração do crédito.
Campo 18 – Preenchimento: informar o valor da Cofins referente à operação/item escriturado neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (VL_BC_COFINS) multiplicado pela alíquota aplicável ao item (ALIQ_COFINS), dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000, então o Campo “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 19 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Maquinas e Equipamentos do Ativo Imobilizado, ativo fixo, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 20 - Preenchimento: Nos registros correspondentes às operações com direito a crédito, informar neste campo o Código do Centro de Custo relacionado à operação, se existir.
Campo 21 - Preenchimento:  Neste campo pode ser informada a descrição complementar do bem ou grupo de bens, com crédito apurado com base no valor de aquisição, objeto de escrituração neste registro.
<!-- End Registro F130 -->
<!-- Start Registro F139 -->
Registro F139: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “F139”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F139" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório. | C | 020 | - | S |
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
Ocorrência – 1:N
Campo 01 - Valor Válido: [F139]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F139 -->
<!-- Start Registro F150 -->
Registro F150: Crédito Presumido sobre Estoque de Abertura
Deve ser objeto de escrituração neste registro o crédito sobre o estoque de abertura de bens adquiridos para revenda (exceto os tributados no regime de substituição tributária e no regime monofásico) ou de bens a serem utilizados como insumo na prestação de serviços e na produção ou fabricação de bens ou produtos destinados à venda, adquiridos de pessoa jurídica domiciliada no País, existentes na data de início da incidência no regime não-cumulativo das contribuições sociais.
Os bens recebidos em devolução, tributados antes da mudança do regime de tributação para o lucro real, são considerados como integrantes do estoque de abertura, devendo ser os respectivos valores informados neste registro.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F150" | C | 004* | - | S |
| 02 | NAT_BC_CRED | Texto fixo contendo "18" Código da Base de Cálculo do Crédito sobre Estoque de Abertura, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | S |
| 03 | VL_TOT_EST | Valor Total do Estoque de Abertura | N | - | 002 | S |
| 04 | EST_IMP | Parcela do estoque de abertura referente a bens, produtos e mercadorias importados, ou adquiridas no mercado interno sem direito ao crédito | N | - | 002 | N |
| 05 | VL_BC_EST | Valor da Base de Cálculo do Crédito sobre o Estoque de Abertura (03 – 04) | N | - | 002 | S |
| 06 | VL_BC_MEN_EST | Valor da Base de Cálculo Mensal do Crédito sobre o Estoque de Abertura (1/12 avos do campo 05) | N | - | 2 | S |
| 07 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 08 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | S |
| 09 | VL_CRED_PIS | Valor Mensal do Crédito Presumido Apurado para o Período -  PIS/PASEP  (06 x 08) | N | - | 02 | S |
| 10 | CST_COFINS | Código da Situação Tributária referente ao COFINS, conforme a Tabela indicada no item 4.3.4 | N | 002* | - | S |
| 11 | ALIQ_COFINS | Alíquota do COFINS (em percentual) | N | 008 | 04 | S |
| 12 | VL_CRED_ COFINS | Valor Mensal do Crédito Presumido Apurado para o Período - COFINS (06 x 11) | N | - | 02 | S |
| 13 | DESC_EST | Descrição do estoque | C | 100 | - | N |
| 14 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Este registro só deve ser preenchido se o ingresso no regime não-cumulativo ocorreu em até 12 (doze) meses anteriores ao do período de apuração da escrituração.
2. O crédito presumido calculado neste registro será utilizado em doze parcelas mensais, iguais e sucessivas, a partir da data em que ocorrer o ingresso no regime não-cumulativo. Desta forma, será informada nos Campos 09 (VL_CRED_PIS) e 12 (VL_CRED_COFINS) a parcela mensal do crédito apurado, que será demonstrado nos Registros M100 (Créditos de PIS/Pasep) e M500 (Créditos de Cofins), bem como utilizado para desconto da contribuição em M200 (Contribuição de PIS/Pasep do Período) e M600 (Cofins do Período).
3. O campo 13 é de preenchimento optativo, caso a pessoa jurídica queira discriminar o seu estoque pela sua composição, tais como: por matéria prima, material de embalagem, produtos intermediários, produtos em processamento, produto acabado; por centro de custo; etc.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 – Valor Válido: [F150]
Campo 02 – Valor Válido: [18]
Campo 03 – Preenchimento: preencha com o valor total do estoque de abertura, conforme constantes nos livros fiscais da empresa.
Campo 04 – Preenchimento: informe o valor da parcela do estoque de abertura referente a bens, produtos e mercadorias importados, ou adquiridas no mercado interno sem direito ao crédito (como por exemplo, aquisições de pessoas físicas, aquisições de produtos sujeitos à alíquota zero, etc.)
Campo 05 – Preenchimento: informe a base de cálculo do crédito sobre o estoque de abertura, correspondendo ao campo 03 – campo 04.
Campo 06 – Validação: informe a base de cálculo mensal do crédito sobre o estoque de abertura, correspondendo a 1/12 avos do campo 05.
Campo 07 – Valores Válidos: [50, 51, 52, 53, 54, 55, 56]
Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 08 – Valor Válido: [0,65]
Campo 09 – Preenchimento: informar o valor do crédito de PIS/Pasep, resultante da multiplicação do campo 06 pelo campo 08, dividido pelo valor “100”. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Campo 10 – Valores Válidos: [50, 51, 52, 53, 54, 55, 56]
Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 11 – Valor Válido: [3,0]
Campo 12 – Preenchimento: informar o valor do crédito da Cofins, resultante da multiplicação do campo 06 pelo campo 11, dividido pelo valor “100”. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Campo 13 – Preenchimento: utilize este campo para discriminar o estoque pela sua composição, tais como: por matéria prima, material de embalagem, produtos intermediários, produtos em processamento, produto acabado; por centro de custo; etc.
Campo 14 – Preenchimento: informar o Código da Conta Analítica. Exemplos: matéria prima, material de embalagem, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro F150 -->
<!-- Start Registro F200 -->
Registro F200: Operações da Atividade Imobiliária - Unidade Imobiliária Vendida
Este registro deve ser preenchido apenas pela pessoa jurídica que auferiu receita da atividade imobiliária, decorrente da aquisição de imóvel para venda, promoção de empreendimento de desmembramento ou loteamento de terrenos, incorporação imobiliária ou construção de prédio destinado à venda.
Nos Registros F200 (receitas da atividade) e F205 e F210 (Operações da atividade com direito a créditos) devem ser informados apenas as operações que sejam próprias da atividade imobiliária. As demais receitas e operações geradoras de créditos, não próprias da atividade imobiliária, devem ser informadas nos registros específicos dos Blocos A, C, D e F, conforme cada caso.
Deve a pessoa jurídica que exerce a atividade imobiliária proceder à escrituração de cada imóvel vendido em registro individualizado, mesmo que a venda se refira a mais de uma unidade a um mesmo adquirente, pessoa física ou pessoa jurídica.
Conforme definido pela legislação tributária, a utilização dos créditos escriturados em F205 ou F210 referentes aos custos vinculados à unidade vendida, construída ou em construção, deve ser efetuada somente a partir da efetivação da venda e na proporção da receita relativa à venda da unidade imobiliária, à medida do recebimento.
No caso de unidades imobiliárias recebidas em devolução (Distrato), os créditos relacionados a estas unidades, apurados neste período ou em períodos anteriores, na EFD-Contribuições ou no DACON, deverão ser estornados na data do desfazimento do negócio (art. 4º da Lei n º 10.833, de 2003), mediante a escrituração dos Registros M110 – Ajustes do Crédito de PIS/Pasep (transferido para o campo 10 de M100) e M510 – Ajustes do Crédito de Cofins (transferido para o campo 10 de M500).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F200" | C | 004* | - | S |
| 02 | IND_OPER | Indicador do Tipo da Operação: 01 – Venda a Vista de Unidade Concluída; 02 – Venda a Prazo de Unidade Concluída; 03 – Venda a Vista de Unidade em Construção; 04 – Venda a Prazo de Unidade em Construção; 05 – Outras. | N | 002* | - | S |
| 03 | UNID_IMOB | Indicador do tipo de unidade imobiliária Vendida: 01 – Terreno adquirido para venda; 02 – Terreno decorrente de loteamento; 03 – Lote oriundo de desmembramento de terreno; 04 – Unidade resultante de incorporação imobiliária; 05 – Prédio construído/em construção para venda; 06 – Outras. | N | 002* | - | S |
| 04 | IDENT_EMP | Identificação/Nome do Empreendimento | C | - | - | S |
| 05 | DESC_UNID_IMOB | Descrição resumida da unidade imobiliária vendida | C | 090 | - | N |
| 06 | NUM_CONT | Número do Contrato/Documento que formaliza a Venda da Unidade Imobiliária | C | 090 | - | N |
| 07 | CPF_CNPJ_ADQU | Identificação da pessoa física (CPF) ou da pessoa jurídica (CNPJ) adquirente da unidade imobiliária | C | 014 | - | S |
| 08 | DT_OPER | Data da operação de venda da unidade imobiliária | N | 008* | - | S |
| 09 | VL_TOT_VEND | Valor total da unidade imobiliária vendida atualizado até o período da escrituração | N | - | 02 | S |
| 10 | VL_REC_ACUM | Valor recebido acumulado até o mês anterior ao da escrituração. | N | - | 02 | N |
| 11 | VL_TOT_REC | Valor total recebido no mês da escrituração | N | - | 02 | S |
| 12 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 13 | VL_BC_PIS | Base de Cálculo do PIS/PASEP | N | - | 02 | N |
| 14 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 15 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 16 | CST_COFINS | Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 17 | VL_BC_COFINS | Base de Cálculo da COFINS | N | - | 02 | N |
| 18 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 19 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 20 | PERC_REC_RECEB | Percentual da receita total recebida até o mês, da unidade imobiliária vendida ((Campo 10 + Campo 11) / Campo 09) | N | 006 | 02 | N |
| 21 | IND_NAT_EMP | Indicador da Natureza Específica do Empreendimento: 1 - Consórcio 2 - SCP 3 – Incorporação em Condomínio 4 - Outras | N | 001* | - | N |
| 22 | INF_COMP | Informações Complementares | C | 090 | - | N |

Observações: Em relação aos itens com CST representativos de receitas, os valores dos campos de bases de cálculo, VL_BC_PIS (Campo 13) e VL_BC_COFINS (Campo 17) serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210) e da Cofins (M610), no Campo “VL_BC_CONT”.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [F200]
Campo 02 - Valores válidos: [01,02,03,04,05]
Campo 03 - Valores válidos: [01,02,03,04,05,06]
Campo 04 - Preenchimento: deve ser informado neste campo a identificação ou nome do empreendimento a que se referem as operações relacionadas neste registro.
Campo 05 - Preenchimento: deve ser informado neste campo a descrição da unidade imobiliária a que se referem as operações relacionadas neste registro.
Campo 06 - Preenchimento: indicar neste campo o número do Contrato/Documento que formaliza a venda da unidade imobiliária relacionada neste registro.
Campo 07 - Preenchimento: deve ser informado neste campo o CPF da pessoa física ou o CNPJ da pessoa jurídica adquirente da unidade imobiliária. No caso de haver mais de um adquirente para a mesma unidade imobiliária vendida, objeto de escrituração no Registro F200, deve ser preenchido o Campo 07 informando o CPF ou o CNPJ de um dos adquirentes, sendo os demais CPF e/ou CNPJ informados no Campo 22 “INF_COMP”.
No caso da pessoa física adquirente da unidade imobiliária não estar cadastrada no CPF, deverá ser informado o CPF do procurador/representante legal.
Atenção: Neste campo deve ser informado o CPF/CNPJ do adquirente da unidade imobiliária e não, de quem está fazendo o pagamento. A finalidade deste campo é permitir à Receita Federal o controle e acompanhamento das partes envolvidas numa aquisição de imóvel, para ver a disponibilidade econômica de quem adquire o imóvel. Observem que idêntico tratamento é também efetuado na Dimob, onde se deve constar o adquirente e não, o financiador do imóvel informado na declaração.
Campo 08 – Preenchimento:  informar a data da operação de venda escriturada neste registro, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 09 - Preenchimento: Informar neste campo o valor total da unidade imobiliária vendida, atualizado até o término do período da escrituração. A informação constante neste campo é necessária e obrigatória na incidência não cumulativa das contribuições sociais, para fins de determinação do percentual da receita recebida até o mês da escrituração.
Campo 10 - Preenchimento: Informar neste campo o valor total da unidade imobiliária vendida, recebido até o mês anterior ao da escrituração. A informação constante neste campo é necessária e obrigatória na incidência não cumulativa das contribuições sociais, para fins de determinação do percentual da receita recebida até o mês da escrituração.
Campo 11 - Preenchimento: Informar no Campo 11 (VL_TOT_REC) o valor da receita recebida no mês da escrituração referente à unidade imobiliária objeto de escrituração. Caso a pessoa jurídica tenha recebido diversos valores no mês da escrituração, deverá informar neste campo o somatório dos valores recebidos no período.
Campo 12 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 13 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à receita tributável da atividade imobiliária.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Campo 14 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (0,65% ou 1,65%), conforme o caso.
Campo 15 – Preenchimento: informar o valor do PIS/Pasep apurado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Campo 16 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 17 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à receita tributável da atividade imobiliária.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Campo 18 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (3% ou 7,6%), conforme o caso.
Campo 19 – Preenchimento: informar o valor da Cofins apurada. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Campo 20 – Preenchimento: informar neste campo o percentual da receita total recebida até o mês, da unidade imobiliária vendida. . A informação constante neste campo é necessária e obrigatória na incidência não cumulativa das contribuições sociais, para fins de determinação do percentual da receita recebida até o mês da escrituração.
O Percentual da Receita da Unidade Vendida Recebida no Mês deve ser igual ao valor total recebido até o mês da escrituração (Campo 10 + Campo 11) dividido pelo Valor total de venda da Unidade Imobiliária (Campo 09).
Campo 21 – Preenchimento: informar neste campo o indicador da natureza do empreendimento cuja receita foi informada neste registro.
Valores válidos: [1, 2, 3, 4]
<!-- End Registro F200 -->
<!-- Start Registro F205 -->
Registro F205: Operações da Atividade Imobiliária – Custo Incorrido da Unidade Imobiliária
Neste registro a pessoa jurídica procederá à escrituração dos créditos referentes aos custos vinculados à unidade imobiliária vendida, construída ou em construção. De acordo com a regulamentação da atividade imobiliária referente ao PIS/Pasep e à Cofins (IN SRF nº 458/04), as despesas com vendas, as despesas financeiras, as despesas gerais e administrativas e quaisquer outras, operacionais e não operacionais, não integram o custo dos imóveis vendidos.
Os créditos referentes aos custos incorridos da unidade imobiliária vendida, conforme definido pela legislação tributária, deve ser objeto de utilização (desconto da contribuição apurada) pela pessoa jurídica somente a partir da efetivação da venda e na proporção da receita relativa à venda da unidade imobiliária, à medida do recebimento.
Atenção: Os créditos próprios da atividade imobiliária serão demonstrados nos registros F205 (crédito sobre o custo incorrido) e F210 (crédito presumido sobre o custo orçado). Os valores dos créditos apurados no período em F205 e F210 serão demonstrados no Registro M100 (Crédito de PIS/Pasep Relativo ao Período) e M500 (Crédito de Cofins Relativo ao Período) com base:
Nos valores informados nos registros M100 (e filhos) e M500 (e filhos), no arquivo elaborado pela própria pessoa jurídica e importado pelo Programa Validador e Assinador da EFD-Contribuições - PVA; ou
Nos valores calculados pelo PVA para os registros M100 e M500, através da funcionalidade “Gerar Apurações” disponibilizada no PVA.
No caso de unidades imobiliárias recebidas em devolução (Distrato), os créditos relacionados a estas unidades, apurados neste período ou em períodos anteriores, na EFD-Contribuições ou no DACON, deverão ser estornados na data do desfazimento do negócio (art. 4º da Lei n º 10.833, de 2003), mediante a escrituração dos Registros M110 – Ajustes do Crédito de PIS/Pasep (transferido para o campo 10 de M100) e M510 – Ajustes do Crédito de Cofins (transferido para o campo 10 de M500).
Caso a pessoa jurídica venha a apurar outros créditos, não próprios da atividade imobiliária (F205 e F210), deverá relacionar as operações e documentos não próprios da atividade imobiliária nos Blocos A, C, D ou F e proceder à apuração e alimentação desses créditos (não próprios da atividade) em registros específicos M100 e M500. Ou seja, o cálculo e demonstração do crédito não próprio da atividade deve ser sempre efetuado pela empresa, visto que a função “Gerar Apurações” só determina e demonstra em M100 e M500 os créditos informados em F205 e F210.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F205" | C | 004* | - | S |
| 02 | VL_CUS_INC_ACUM_ANT | Valor Total do Custo Incorrido da unidade imobiliária acumulado até o mês anterior ao da escrituração | N | - | 02 | S |
| 03 | VL_CUS_INC_PER_ESC | Valor Total do Custo Incorrido da unidade imobiliária no mês da escrituração | N | - | 02 | S |
| 04 | VL_CUS_INC_ACUM | Valor Total do Custo Incorrido da unidade imobiliária acumulado até o mês da escrituração (Campo 02 + 03) | N | - | 02 | S |
| 05 | VL_EXC_BC_CUS_INC_ACUM | Parcela do Custo Incorrido sem direito ao crédito da atividade imobiliária, acumulado até o período. | N | - | 02 | S |
| 06 | VL_BC_CUS_INC | Valor da Base de Cálculo do Crédito sobre o Custo Incorrido, acumulado até o período da escrituração (Campo 04 – 05) | N | - | 02 | S |
| 07 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 08 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | S |
| 09 | VL_CRED_PIS_ACUM | Valor Total do Crédito Acumulado sobre o custo incorrido – PIS/PASEP (Campo 06 x 08) | N | - | 02 | S |
| 10 | VL_CRED_PIS_DESC_ANT | Parcela do crédito descontada até o período anterior da escrituração – PIS/PASEP (proporcional à receita recebida até o mês anterior). | N | - | 02 | S |
| 11 | VL_CRED_PIS_DESC | Parcela a descontar no período da escrituração  – PIS/PASEP (proporcional à receita recebida no mês). | N | - | 02 | S |
| 12 | VL_CRED_PIS_DESC_FUT | Parcela a descontar em períodos futuros  – PIS/PASEP (Campo 09 – 10 – 11). | N | - | 02 | S |
| 13 | CST_COFINS | Código da Situação Tributária referente ao COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 14 | ALIQ_COFINS | Alíquota do COFINS (em percentual) | N | 008 | 04 | S |
| 15 | VL_CRED_COFINS_ACUM | Valor Total do Crédito Acumulado sobre o custo incorrido - COFINS (Campo 06 x 14) | N | - | 02 | S |
| 16 | VL_CRED_COFINS_DESC_ANT | Parcela do crédito descontada até o período anterior da escrituração – COFINS (proporcional à receita recebida até o mês anterior). | N | - | 02 | S |
| 17 | VL_CRED_COFINS_DESC | Parcela a descontar no período da escrituração  – COFINS (proporcional à receita recebida no mês). | N | - | 02 | S |
| 18 | VL_CRED_COFINS_DESC_FUT | Parcela a descontar em períodos futuros  – COFINS (Campo 15 – 16 – 17). | N | - | 02 | S |

Observações: Valor do crédito a descontar no período da escrituração, constante do Campo 11 (VL_CRED_PIS_DESC) e do Campo 17 (VL_CRED_COFINS_DESC) serão utilizados para desconto da contribuição apurada nos Registros M200 (PIS/Pasep) e M600 (Cofins), respectivamente, referente à atividade imobiliária.
Nível hierárquico - 4
Ocorrência – 1:1
Campo 01 - Valor Válido: [F205]
Campo 02 - Preenchimento: deve ser informado neste campo o valor total do custo incorrido da unidade imobiliária escriturada em cada registro F205, acumulado até o mês anterior ao da escrituração.
Campo 03 - Preenchimento: deve ser informado neste campo o valor do custo da unidade imobiliária escriturada em cada registro F205, incorrido no mês da escrituração.
Campo 04 - Preenchimento: deve ser informado neste campo o valor total do custo incorrido da unidade imobiliária escriturada em cada registro F205, acumulado até o mês da escrituração.
Validação: O valor informado neste campo deve corresponder ao somatório dos Campos 02 e 03.
Campo 05 - Preenchimento: neste registro deve a pessoa jurídica relacionar a parcela do custo incorrido da unidade imobiliária vendida que não deve compor a base de cálculo do crédito. De acordo com a legislação tributária, não dará direito a crédito o valor:
I - de mão-de-obra paga a pessoa física, bem assim dos encargos trabalhistas, sociais e previdenciários;
II - da aquisição de bens ou serviços não sujeitos ao pagamento das contribuições.
Campo 06 - Preenchimento: deve ser informado neste campo o valor da base de cálculo do crédito sobre o custo incorrido, acumulado até o período da escrituração, correspondente ao valor do campo 04 –  campo 05.
Campo 07 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. No caso de crédito vinculado à receita tributada no mercado interno, deve ser informado o CST 50.
Campo 08 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito da atividade imobiliária  que, em relação ao PIS/Pasep, correspondente ao percentual de 1,65%.
Campo 09 – Preenchimento: informar o valor total do crédito de PIS/Pasep incidente sobre o custo incorrido acumulado ajustado (Campo 06).
Validação: o valor do campo 09 deve corresponder ao valor da base de cálculo do custo incorrido total (Campo 06) multiplicado pela alíquota aplicável (Campo 08).
Campo 10 – Preenchimento: informar a parcela do crédito escriturada no campo 09, já utilizada mediante desconto da contribuição, até o período anterior da escrituração – PIS/PASEP (proporcional à receita acumulada recebida até o mês anterior).
Campo 11 – Preenchimento: informar a parcela do crédito escriturada no campo 09, a descontar da contribuição apurada neste período da escrituração – PIS/PASEP (proporcional à receita recebida no mês).
Campo 12 – Preenchimento: informar a parcela do crédito escriturada no campo 09, a descontar da contribuição para o PIS/Pasep em períodos futuros (Campo 09 – Campo 10 – Campo 11).
Campo 13 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 14 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito da atividade imobiliária que, em relação à Cofins, corresponde ao percentual de 7,6%.
Campo 15 – Preenchimento: informar o valor total do crédito de Cofins incidente sobre o custo incorrido acumulado ajustado (Campo 06).
Validação: o valor do campo 15 deve corresponder ao valor da base de cálculo do custo incorrido total (Campo 06) multiplicado pela alíquota aplicável (Campo 14).
Campo 16 – Preenchimento: informar a parcela do crédito escriturada no campo 15, já utilizada mediante desconto da contribuição, até o período anterior da escrituração – Cofins (proporcional à receita acumulada recebida até o mês anterior).
Campo 17 – Preenchimento: informar a parcela do crédito escriturada no campo 15, a descontar da Cofins apurada neste período da escrituração (proporcional à receita recebida no mês).
Campo 18 – Preenchimento: informar a parcela do crédito escriturada no campo 15, a descontar da Cofins em períodos futuros (Campo 15 – Campo 16 – Campo 17).
<!-- End Registro F205 -->
<!-- Start Registro F210 -->
Registro F210: Operações da Atividade Imobiliária - Custo Orçado da Unidade Imobiliária Vendida
Neste registro a pessoa jurídica procederá à escrituração dos créditos referentes ao custo orçado pra a conclusão da obra ou melhoramento, vinculado à unidade imobiliária vendida em construção. De acordo com a regulamentação da atividade imobiliária referente ao PIS/Pasep e à Cofins (IN SRF nº 458/04), as despesas com vendas, as despesas financeiras, as despesas gerais e administrativas e quaisquer outras, operacionais e não operacionais, não integram o custo dos imóveis vendidos.
Os créditos referentes ao custo orçado da unidade imobiliária vendida, conforme definido pela legislação tributária, deve ser objeto de utilização (desconto da contribuição apurada) pela pessoa jurídica somente a partir da efetivação da venda e na proporção da receita relativa à venda da unidade imobiliária, à medida do recebimento.
O Registro F210 é de preenchimento opcional. Será preenchido apenas quando o campo IND_OPER, do Registro F200, for igual a 03 ou 04, representativo de crédito vinculado a venda de unidade imobiliária não concluída, conforme definido no art. 4º da Lei nº 10.833, de 2003.
Atenção: Em relação à questão do custo orçado, a sua apuração é uma faculdade da pessoa jurídica, não se trata assim de um componente, um levantamento, que a empresa seja obrigado a fazer e considerar.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F210" | C | 004* | - | S |
| 02 | VL_CUS_ORC | Valor Total do Custo Orçado para Conclusão da Unidade Vendida | N | - | 02 | S |
| 03 | VL_EXC | Valores Referentes a Pagamentos a Pessoas Físicas, Encargos Trabalhistas, Sociais e Previdenciários e à aquisição de bens e serviços não sujeitos ao pagamento das contribuições | N | - | 02 | S |
| 04 | VL_CUS_ORC_AJU | Valor da Base de Calculo do Crédito sobre o Custo Orçado Ajustado (Campo 02 – 03). | N | - | 02 | S |
| 05 | VL_BC_CRED | Valor da Base de Cálculo do Crédito sobre o Custo Orçado referente ao mês da escrituração, proporcionalizada em função da receita recebida no mês. | N | - | 02 | S |
| 06 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP, conforme a Tabela indicada no item 4.3.3. | N | 002* | - | S |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 08 | VL_CRED_PIS_UTIL | Valor do Crédito sobre o custo orçado a ser utilizado no período da escrituração - PIS/PASEP (Campo 05 x 07) | N | - | 02 | N |
| 09 | CST_COFINS | Código da Situação Tributária referente a COFINS, conforme a Tabela indicada no item 4.3.4. | N | 002* | - | S |
| 10 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 11 | VL_CRED_COFINS_UTIL | Valor do Crédito sobre o custo orçado a ser utilizado no período da escrituração - COFINS (Campo 05 x 10) | N | - | 02 | N |

Observações:
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [F210]
Campo 02 - Preenchimento: Informar neste campo o valor total do custo orçado, referente à unidade imobiliária não concluída vendida e objeto de escrituração neste registro.
Campo 03 - Preenchimento: neste registro deve a pessoa jurídica relacionar a parcela do custo orçado da unidade imobiliária vendida que não deve compor a base de cálculo do crédito. De acordo com a legislação tributária, não dará direito a crédito o valor:
I - de mão-de-obra paga a pessoa física, bem assim dos encargos trabalhistas, sociais e previdenciários;
II - da aquisição de bens ou serviços não sujeitos ao pagamento das contribuições.
Campo 04 - Preenchimento: Informar neste campo o valor da base de calculo do crédito sobre o custo orçado, ajustado pelas exclusões do valor informado no Campo 03 (Campo 04 – Campo 03).
Campo 05 - Preenchimento: o valor da base de cálculo do crédito do mês referente ao custo orçado, constante do Campo 05 (VL_BC_CRED) será determinado com base no valor do custo orçado ajustado (Campo 06), na proporção da receita recebida no mês, referente à unidade imobiliária vendida.
Campo 06 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. No caso de crédito vinculado à receita tributada no mercado interno, deve ser informado o CST 50.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito da atividade imobiliária que, em relação ao PIS/Pasep, correspondente ao percentual de 1,65%.
Campo 08 – Preenchimento:  informar o valor total do crédito de PIS/Pasep incidente sobre o custo orçado ajustado (Campo 05).
Validação: o valor do campo 08 deve corresponder ao valor da base de cálculo do custo orçado (Campo 05) multiplicado pela alíquota aplicável (Campo 07).
Campo 09 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições. No caso de crédito vinculado à receita tributada no mercado interno, deve ser informado o CST 50.
Campo 10 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito da atividade imobiliária que, em relação a Cofins, correspondente ao percentual de 7,6%.
Campo 11 – Preenchimento: informar o valor total do crédito de Cofins incidente sobre o custo orçado ajustado (Campo 05).
Validação: o valor do campo 11 deve corresponder ao valor da base de cálculo do custo orçado (Campo 05) multiplicado pela alíquota aplicável (Campo 10).
<!-- End Registro F210 -->
<!-- Start Registro F211 -->
Registro F211: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “F211”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F211" | C | 004* | - | S |
| 02 | NUM_PROC | Identificação do processo ou ato concessório. | C | 020 | - | S |
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
Campo 01 - Valor Válido: [F211]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F211 -->
<!-- Start Registro F500 -->
Registro F500: Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido  – Incidência do PIS/Pasep e da Cofins pelo Regime de Caixa
Registro especifico para a pessoa jurídica submetida ao regime de apuração com base no lucro presumido, optante pela apuração da contribuição para o PIS/Pasep e da Cofins pelo regime de caixa, conforme previsto no art. 20 da Medida Provisória nº 2.158-35, de 2001.
Este registro tem por objetivo representar a escrituração e tratamento fiscal das receitas recebidas no período, segmentado por Código de Situação Tributária - CST, do PIS/Pasep e da Cofins. O total das receitas consolidadas por CST nos registros F500, devem corresponder ao total das receitas relacionadas nos registros F525.
Os campos de CFOP, COD_CTA e INFO_COMPL podem ser utilizados pela pessoa jurídica para realizar o detalhamento da receita recebida por código de operação, documentos, contas contábeis, itens, clientes, etc.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F500" | C | 004* | - | S |
| 02 | VL_REC_CAIXA | Valor total da receita recebida, referente à combinação de CST e Alíquota. | N | - | 02 | S |
| 03 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 04 | VL_DESC_PIS | Valor do desconto / exclusão da base de cálculo | N | - | 02 | N |
| 05 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 06 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 07 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 08 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 09 | VL_DESC_COFINS | Valor do desconto / exclusão da base de cálculo | N | - | 02 | N |
| 10 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 11 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 12 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 13 | COD_MOD | Código do modelo do documento fiscal conforme a Tabela 4.1.1 | C | 002* | - | N |
| 14 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 15 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 16 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
1. Deve ser escriturado um registro para cada CST representativo das receitas recebidas no período, sujeitas ou não ao pagamento da contribuição social.
2. No caso de incidir mais de uma alíquota em relação a um mesmo CST, como no caso de produtos monofásicos, deve a pessoa jurídica escriturar um registro para cada combinação de CST e alíquota.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [F500]
Campo 02 – Preenchimento: Informar neste campo o valor total da receita recebida no período da escrituração, correspondente aos Códigos de Situação Tributária (CST-PIS e CST-Cofins) informados nos campos 03 e 08. Havendo receita recebida sujeita a alíquotas diversas, em relação ao mesmo CST, deve a pessoa jurídica gerar registros distintos, para cada combinação de CST e alíquota.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual de Orientação ao Leiaute da EFD-Contribuições.
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

Campo 04 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da contribuição.
Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente aos valores de receita recebida, consolidados nesse registro por CST e alíquota, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de corresponder a fato gerador tributado da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota em percentual (aplicável sobre a base cálculo correspondente à receita recebida, informada em reais no campo “05”).
Campo 07 – Preenchimento: informar o valor do PIS/Pasep referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: No caso de alíquotas ad valorem (alíquota básica de 0,65%, por exemplo) o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo “05”) multiplicado pela alíquota aplicável em percentual (campo “06”).
Exemplo: Sendo o Campo 05 (VL_BC_PIS) = 1.000.000,00 e o Campo 06 (ALIQ_PIS) = 0,6500, então o Campo 07 (VL_PIS) será igual a: 1.000.000,00 x 0,65 / 100 = 6.500,00.
Campo 08 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 09 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da Cofins.
Campo 10 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente aos valores de receita recebida, consolidados nesse registro por CST e alíquota, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de corresponder a fato gerador tributado da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 11 - Preenchimento: informar neste campo o valor da alíquota em percentual (aplicável sobre a base cálculo correspondente à receita recebida, informada em reais no campo “10”).
Campo 12 – Preenchimento: informar o valor da Cofins referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: No caso de alíquotas ad valorem (alíquota básica de 3,0%, por exemplo) o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo “10”) multiplicado pela alíquota aplicável em percentual (campo “11”).
Exemplo: Sendo o Campo 10 (VL_BC_COFINS) = 1.000.000,00 e o Campo 11 (ALIQ_COFINS) = 3,0000, então o Campo 12 (VL_COFINS) será igual a: 1.000.000,00 x 3,0000 / 100 = 30.000,00.
Campo 13 - Preenchimento: Informar neste campo o Código do modelo do documento fiscal, conforme a Tabela 4.1.1. Referida segregação do registro, por código de modelo do documento fiscal, apesar de não ser obrigatória na escrituração digital, quando efetuada torna a mesma mais completa e transparente.
No caso de escrituração de vendas mediante emissão de NFC-e, deve ser informado o registro com o código “65”, neste campo.
No caso de não constar na relação de códigos da Tabela 4.1.1 no documentro, deve ser informado o código “99”. Especificadamente em relação aos documentos fiscais representativos da prestação de serviços, definidos pela legislação municipal do I.S.S., deve ser informado o código “98”.
Campo 14 - Preenchimento: Informar neste campo o Código Fiscal de Operação (CFOP) correspondente às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 15 - Preenchimento: informar o Código da Conta Analítica representativa da receita informada neste registro. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, receita recebida no período, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 16 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
<!-- End Registro F500 -->
<!-- Start Registro F509 -->
Registro F509: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “F509”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F509” | C | 004 | - | S |
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
Campo 01 - Valor Válido: [F509]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F509 -->
<!-- Start Registro F510 -->
Registro F510: Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação Com Base no Lucro Presumido – Incidência do PIS/Pasep e da Cofins pelo Regime de Caixa (Apuração da Contribuição por Unidade de Medida de Produto – Alíquota em Reais)

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F510" | C | 004* | - | S |
| 02 | VL_REC_CAIXA | Valor total da receita recebida, referente à combinação de CST e Alíquota. | N | - | 02 | S |
| 03 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 04 | VL_DESC_PIS | Valor do desconto / exclusão | N | - | 02 | N |
| 05 | QUANT_BC_PIS | Base de cálculo em quantidade - PIS/PASEP | N | - | 03 | N |
| 06 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | 008 | 04 | N |
| 07 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 08 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 09 | VL_DESC_COFINS | Valor do desconto / exclusão | N | - | 02 | N |
| 10 | QUANT_BC_COFINS | Base de cálculo em quantidade - COFINS | N | - | 03 | N |
| 11 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | 008 | 04 | N |
| 12 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 13 | COD_MOD | Código do modelo do documento fiscal conforme a Tabela 4.1.1 | C | 002* | - | N |
| 14 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 15 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 16 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
1. Registro específico para a pessoa jurídica submetida ao regime de apuração com base no lucro presumido, optante pela apuração da contribuição para o PIS/Pasep e da Cofins pelo regime de caixa, conforme previsto no art. 20 da Medida Provisória nº 2.158-35, de 2001, que apure as contribuições por unidade de medida de produto, conforme as hipóteses abaixo:
- Pessoa jurídica industrial ou importadora optante pelo regime especial de tributação de bebidas frias (cervejas, refrigerantes, águas, etc), conforme previsto no art. 58-J da Lei nº 10.833/2003;
- Pessoa jurídica fabricante ou importadora de combustíveis, optante pelo regime especial de tributação, conforme previsto no art. 23 da Lei nº 10.865/2004;
- Pessoa jurídica produtora, importadora ou distribuidora de álcool, optante pelo regime especial de tributação, conforme previsto no art. 5º da Lei nº 9.718/98;
- Pessoa jurídica industrial, comercial ou importadora de embalagens para bebidas frias, sujeitas ao regime de tributação previsto no art. 51 da Lei nº 10.833/2003;
- Outras hipóteses de tributação por unidade de medida de produto, especificadas na legislação tributária.
2. No caso de incidir mais de uma alíquota em relação a um mesmo CST, como no caso de produtos monofásicos, deve a pessoa jurídica escriturar um registro para cada combinação de CST e alíquota.
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [F510]
Campo 02 – Preenchimento: Informar neste campo o valor total da receita recebida no período da escrituração, correspondente aos Códigos de Situação Tributária (CST-PIS e CST-Cofins) informados nos campos 03 e 08. Havendo receita recebida sujeita a alíquotas diversas, em relação ao mesmo CST, deve a pessoa jurídica gerar registros distintos, para cada combinação de CST e alíquota .
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 04 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da contribuição.
Campo 05 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 05).
Campo 07 – Preenchimento: informar o valor do PIS/Pasep referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 05) multiplicado pela alíquota aplicável ao item (campo 06).
Campo 08 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 09 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da contribuição.
Campo 10 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 11 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 10).
Campo 12 – Preenchimento: informar o valor da Cofins referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 10) multiplicado pela alíquota aplicável ao item (campo 11).
Campo 13 - Preenchimento: Informar neste campo o Código indicador do modelo de documento fiscal a que se refere a receita demonstrada neste registro, conforme a Tabela 4.1.1.
No caso de escrituração de vendas mediante emissão de NFC-e, deve ser informado o registro com o código “65”, neste campo.
Campo 14 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 15 - Preenchimento: informar o Código da Conta Analítica representativa da receita informada neste registro. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, receita recebida no período, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
Campo 16 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
<!-- End Registro F510 -->
<!-- Start Registro F519 -->
Registro F519: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “F519”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F519” | C | 004 | - | S |
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
Campo 01 - Valor Válido: [F519]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F519 -->
<!-- Start Registro F525 -->
Registro F525: Composição da Receita Escriturada no Período – Detalhamento da Receita Recebida pelo Regime de Caixa
Registro obrigatório para a pessoa jurídica submetida ao regime de tributação com base no lucro presumido, optante pela apuração das contribuições sociais pelo regime de caixa. Tem por objetivo relacionar a composição de todas as receitas recebidas pela pessoa jurídica no período da escrituração, sujeitas ou não ao pagamento da contribuição social.
O total das receitas relacionadas nos registros F525 deve corresponder ao total das receitas recebidas, relacionadas nos registros F500.
Atenção: Este registro é de escrituração opcional até o período de apuração referente a março de 2013. A partir de abril de 2013 o registro “F525” passa a ser de escrituração obrigatória.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F525" | C | 004* | - | S |
| 02 | VL_REC | Valor total da receita recebida, correspondente ao indicador informado no campo 03 (IND_REC) | N | - | 02 | S |
| 03 | IND_REC | Indicador da composição da receita recebida no período (Campo 02), por: 01- Clientes 02- Administradora de cartão de débito/crédito 03- Título de crédito - Duplicata, nota promissória, cheque, etc. 04- Documento fiscal 05- Item vendido (produtos e serviços) 99- Outros (Detalhar no campo 10 – Informação Complementar) | C | 002* | - | S |
| 04 | CNPJ_CPF | CNPJ/CPF do participante (cliente/pessoa física ou jurídica pagadora) ou da administradora de cartões (vendas por cartão de débito ou de crédito), no caso de detalhamento da receita recebida conforme os indicadores “01” ou “02”, respectivamente. | C | 014 | - | N |
| 05 | NUM_DOC | Número do título de crédito ou do documento fiscal, no caso de detalhamento da receita recebida conforme os indicadores “03” ou “04”, respectivamente. | C | 060 | - | N |
| 06 | COD_ITEM | Código do item (campo 02 do Registro 0200), no caso de detalhamento da receita recebida por item vendido, conforme o indicador “05”. | C | 060 | - | N |
| 07 | VL_REC_DET | Valor da receita detalhada, correspondente ao conteúdo informado no campo 04, 05, 06 ou 10. | N | - | 02 | S |
| 08 | CST_PIS | Código da Situação Tributária do PIS/Pasep | N | 002* | - | N |
| 09 | CST_COFINS | Código da Situação Tributária da Cofins | N | 002* | - | N |
| 10 | INFO_COMPL | Informação complementar | C | - | - | N |
| 11 | COD_CTA | Código da conta analítica contábil representativa da receita recebida | C | 255 | - | N |

Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [F525]
Campo 02 – Preenchimento: Informar neste campo o valor total da receita recebida no período da escrituração, de acordo com as informações e controles internos da pessoa jurídica, considerados na formação da base de cálculo mensal do PIS/Pasep e da Cofins. A segregação ou demonstração das receitas recebidas deve ser efetuada, com base nos códigos indicadores de receita recebidas constante do Campo “03”. No caso da pessoa jurídica utilizar outro critério de demonstração das receitas recebidas, deve identificá-lo informando o indicador “99” no campo “03”.
Campo 03 - Preenchimento: Informar neste campo o código indicador do critério de demonstração da receita recebida pela pessoa jurídica no período da escrituração. No caso da pessoa jurídica segregar e demonstrar as receitas recebidas no período por critério não relacionado em um dos indicadores específicos deste campo, deve então informar o indicador “99”, detalhando o outro critério no campo “10”, referente a informações complementares.
Atenção: Somente deverá ser utilizado o indicador “99” quando nenhum dos outros indicadores for aplicável.
Por exemplo, no caso de receitas de aplicações financeiras recebidas, decorrentes de aplicações em instituições financeiras, informar o código “99”, uma vez que estas receitas, pela sua natureza e origem, não se classificam nos códigos “1”, “2”, “3”, “4” ou “5”.
Campo 04 – Preenchimento: Informar neste campo o CNPJ ou o CPF do cliente, no caso de detalhamento da receita recebida de conformidade com o indicador “01”, no campo “03”. No caso da pessoa jurídica demonstrar as receitas recebidas, por administradoras de cartão de débito ou de crédito, conforme indicador “02” do campo “03”, informar neste  campo o CNPJ da administradora de cartões.
Campo 05 - Preenchimento: Informar neste campo o título ou número do documento fiscal, no caso de detalhamento da receita recebida por título de crédito ou por documento fiscal, conforme indicadores “03” ou “04” do campo “03”, respectivamente.
Campo 06 - Preenchimento: No caso da pessoa jurídica demonstrar as receitas recebidas com base nos produtos vendidos (bens e serviços), informar neste campo o código do item, conforme informado e cadastrado no campo “02” do registro “0200”.
Campo 07 – Preenchimento: Informar neste campo o valor da receita recebida, correspondente ao detalhamento informado no campo “04”, “05”, “06” ou “10”.
Campo 08 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), correspondente à receita informada no campo “07”.
Os códigos CST-PIS encontram-se demonstrados na Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições (Tabela 4.3.3).
Campo 09 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), correspondente à receita informada no campo “07”.
Os códigos CST-COFINS encontram-se demonstrados na Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições (Tabela 4.3.4).
Campo 10 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
Campo 11 - Preenchimento: informar o Código da Conta Analítica representativa da receita detalhada neste registro. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, receita recebida no período, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro F525 -->
<!-- Start Registro F550 -->
Registro F550: Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido – Incidência do PIS/Pasep e da Cofins pelo Regime de Competência
Registro específico para a pessoa jurídica submetida ao regime de apuração com base no lucro presumido, optante pela apuração da contribuição para o PIS/Pasep e da Cofins pelo regime de competência, conforme previsto na Lei nº 9.718, de 1998.
Este registro tem por objetivo representar a escrituração e tratamento fiscal das receitas auferidas no período, independente de seu recebimento ou não, segmentado por Código de Situação Tributária - CST, do PIS/Pasep e da Cofins.
As receitas consolidadas por CST no registro “F550”, devem estar relacionadas no registro “L900” (demonstração consolidada das receitas auferidas no período, por tipo/natureza do documento de registro da receita).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F550" | C | 004* | - | S |
| 02 | VL_REC_COMP | Valor total da receita auferida, referente à combinação de CST e Alíquota. | N | - | 02 | S |
| 03 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 04 | VL_DESC_PIS | Valor do desconto / exclusão da base de cálculo | N | - | 02 | N |
| 05 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 06 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 07 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 08 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 09 | VL_DESC_COFINS | Valor do desconto / exclusão da base de cálculo | N | - | 02 | N |
| 10 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 11 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 12 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 13 | COD_MOD | Código do modelo do documento fiscal conforme a Tabela 4.1.1 | C | 002* | - | N |
| 14 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 15 | COD_CTA | Código da conta analítica contábil debitada / creditada | C | 255 | - | N |
| 16 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
Deve ser escriturado um registro para cada CST representativo das receitas auferidas no período, sujeitas ou não ao pagamento da contribuição social.
No caso de incidir mais de uma alíquota em relação a um mesmo CST, como no caso de produtos monofásicos, deve a pessoa jurídica escriturar um registro para cada combinação de CST e alíquota.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [F550]
Campo 02 – Preenchimento: Informar neste campo o valor total da receita auferida no período da escrituração, pelo regime de competência, correspondente aos Códigos de Situação Tributária (CST-PIS e CST-Cofins) informados nos campos 03 e 08. Havendo receita auferida sujeita a alíquotas diversas, em relação ao mesmo CST, deve a pessoa jurídica gerar registros distintos, para cada combinação de CST e alíquota.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 04 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da contribuição.
Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente aos valores de receita auferida, consolidados nesse registro por CST e alíquota, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “VL_BC_CONT”) no caso de corresponder a fato gerador tributado da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota em percentual (aplicável sobre a base cálculo correspondente à receita auferida, informada em reais no campo “05”), ou o valor da alíquota em reais  (para os produtores e importadores de produtos monofásicos, aplicável sobre a base cálculo determinada por quantidade de produtos vendidos, informada no campo “05”), conforme o caso.
Campo 07 – Preenchimento: informar o valor do PIS/Pasep referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: No caso de alíquotas ad valorem (alíquota básica de 0,65%, por exemplo) o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 05) multiplicado pela alíquota aplicável em percentual (campo 06).
Exemplo: Sendo o Campo 05 (VL_BC_PIS) = 1.000.000,00 e o Campo 06 (ALIQ_PIS) = 0,6500, então o Campo 07 (VL_PIS) será igual a: 1.000.000,00 x 0,65 / 100 = 6.500,00.
Campo 08 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 09 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da Cofins.
Campo 10 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente aos valores de receita auferida, consolidados nesse registro por CST e alíquota, para fins de apuração da contribuição social, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “VL_BC_CONT”) no caso de corresponder a fato gerador tributado da contribuição social.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 11 - Preenchimento: informar neste campo o valor da alíquota em percentual (aplicável sobre a base cálculo correspondente à receita auferida, informada em reais no campo “10”), ou o valor da alíquota em reais  (para os produtores e importadores de produtos monofásicos, aplicável sobre a base cálculo determinada por quantidade de produtos vendidos, informada no campo “10”), conforme o caso.
Campo 12 – Preenchimento: informar o valor da Cofins referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: No caso de alíquotas ad valorem (alíquota básica de 3,0%, por exemplo) o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 10) multiplicado pela alíquota aplicável em percentual (campo 11).
Exemplo: Sendo o Campo 10 (VL_BC_COFINS) = 1.000.000,00 e o Campo 11 (ALIQ_COFINS) = 3,0000, então o Campo 12 (VL_COFINS) será igual a: 1.000.000,00 x 3,0000 / 100 = 30.000,00.
Campo 13 - Preenchimento: Informar neste campo o Código do modelo do documento fiscal, conforme a Tabela 4.1.1. Referida segregação do registro, por código de modelo do documento fiscal, apesar de não ser obrigatória na escrituração digital, quando efetuada torna a mesma mais completa e transparente.
No caso de escrituração de vendas mediante emissão de NFC-e, deve ser informado o registro com o código “65”, neste campo.
Campo 14 - Preenchimento: Informar neste campo o Código Fiscal de Operação – CFOP,  relativo às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 15 - Preenchimento: informar o Código da Conta Analítica representativa da receita informada neste registro. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, receita auferida no período, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Atenção:
Para as pessoas jurídicas que adotam o regime de competência para apuração do IR, da CSLL, do PIS/Pasep e da Cofins, devem informar no Campo 15 deste registro o código da conta contábil, representativa das receitas auferidas.
A não informação da conta contábil correspondente às operações, nos registros representativos de receitas e/ou de créditos acarretará:
- Para os fatos geradores até 31 de outubro de 2017, ocorrência de aviso/advertência (não impedindo a validação do registro);
- Para os fatos geradores a partir de 01 de novembro de 2017, ocorrência de erro (impedindo a validação do registro).
Informação de preenchimento – PJ tributadas com base no lucro presumido:
Considerando que o atual programa da EFD-Contribuições (versão 2.1.4) estabelece a obrigatoriedade de se informar nos registros da escrituração, das operações geradoras de receitas e/ou de créditos, a conta contábil (Campo COD_CTA), a partir do período de apuração de novembro de 2017;
Considerando que Instrução Normativa RFB nº 1.774, de 22.12.2017, dispensou da obrigatoriedade da escrituração contábil digital (ECD) as pessoas jurídicas tributadas com base no lucro presumido que não distribuíram, a título de lucro, sem incidência do Imposto sobre a Renda Retido na Fonte (IRRF), parcela de lucros ou dividendos, superior ao valor da base de cálculo do Imposto sobre a Renda diminuída dos impostos e contribuições a que estiver sujeita;
As pessoas jurídicas tributadas com base no lucro presumido não sujeitas à obrigatoriedade da ECD, nos termos da IN RFB nº 1.774/2017, poderão, opcionalmente, informar nos campos "COD_CTA" dos registros da EFD-Contribuições, para os fatos geradores a partir de novembro/2017, inclusive, a informação "Dispensa de ECD - IN RFB nº 1.774/2017".
Campo 16 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
<!-- End Registro F550 -->
<!-- Start Registro F559 -->
Registro F559: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “F559”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F559” | C | 004 | - | S |
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
Campo 01 - Valor Válido: [F559]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F559 -->
<!-- Start Registro F560 -->
Registro F560: Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido – Incidência do PIS/Pasep e da Cofins pelo Regime de Competência (Apuração da Contribuição por Unidade de Medida de Produto – Alíquota em Reais)

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F560" | C | 004* | - | S |
| 02 | VL_REC_COMP | Valor total da receita auferida, referente à combinação de CST e Alíquota. | N | - | 02 | S |
| 03 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 04 | VL_DESC_PIS | Valor do desconto / exclusão | N | - | 02 | N |
| 05 | QUANT_BC_PIS | Base de cálculo em quantidade - PIS/PASEP | N | - | 03 | N |
| 06 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | 008 | 04 | N |
| 07 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 08 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 09 | VL_DESC_COFINS | Valor do desconto / exclusão | N | - | 02 | N |
| 10 | QUANT_BC_COFINS | Base de cálculo em quantidade – COFINS | N | - | 03 | N |
| 11 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | 008 | 04 | N |
| 12 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 13 | COD_MOD | Código do modelo do documento fiscal conforme a Tabela 4.1.1 | C | 002* | - | N |
| 14 | CFOP | Código fiscal de operação e prestação | N | 004* | - | N |
| 15 | COD_CTA | Código da conta analítica contábil debitada / creditada | C | 255 | - | N |
| 16 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
1. Registro específico para a pessoa jurídica submetida ao regime de apuração com base no lucro presumido, optante pela apuração da contribuição para o PIS/Pasep e da Cofins pelo regime de competência, conforme previsto na Lei nº 9.718, de 1998, que apure as contribuições por unidade de medida de produto, conforme as hipóteses abaixo:
- Pessoa jurídica industrial ou importadora optante pelo regime especial de tributação de bebidas frias, conforme previsto no art. 58-J da Lei nº 10.833/2003 (para fatos geradores até 30.04.2015);
- Pessoa jurídica fabricante ou importadora de combustíveis, optante pelo regime especial de tributação, conforme previsto no art. 23 da Lei nº 10.865/2004;
- Pessoa jurídica produtora, importadora ou distribuidora de álcool, optante pelo regime especial de tributação, conforme previsto no art. 5º da Lei nº 9.718/98;
- Pessoa jurídica industrial, comercial ou importadora de embalagens para bebidas frias, sujeitas ao regime de tributação previsto no art. 51 da Lei nº 10.833/2003 (para fatos geradores até 30.04.2015);
2. No caso de incidir mais de uma alíquota em relação a um mesmo CST, como no caso de produtos monofásicos, deve a pessoa jurídica escriturar um registro para cada combinação de CST e alíquota.
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [F560]
Campo 02 – Preenchimento: Informar neste campo o valor total da receita recebida no período da escrituração, correspondente aos Códigos de Situação Tributária (CST-PIS e CST-Cofins) informados nos campos 03 e 08. Havendo receita recebida sujeita a alíquotas diversas, em relação ao mesmo CST, deve a pessoa jurídica gerar registros distintos, para cada combinação de CST e alíquota.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST-PIS), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 04 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da contribuição.
Campo 05 - Preenchimento: informar neste campo a base de cálculo do PIS/Pasep expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210, Campo “QUANT_BC_PIS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 05).
Campo 07 – Preenchimento: informar o valor do PIS/Pasep referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 05) multiplicado pela alíquota aplicável ao item (campo 06).
Campo 08 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST-COFINS), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
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

Campo 09 – Preenchimento: Informar neste campo o valor dos descontos/exclusões da base de cálculo da contribuição.
Campo 10 - Preenchimento: informar neste campo a base de cálculo da Cofins expressa em quantidade (Unidade de Medida de Produto), para fins de apuração da contribuição social, conforme as hipóteses previstas em lei, como por exemplo, no caso de fabricantes e importadores de combustíveis e de bebidas frias (água, cerveja, refrigerantes) que tenham optado por apurar as contribuições sociais com base na quantidade de produto vendida.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610, Campo “QUANT_BC_COFINS”) no caso de item correspondente a fato gerador da contribuição social.
Campo 11 - Preenchimento: informar neste campo o valor da alíquota expressa em reais, aplicável para fins de apuração da contribuição social, sobre a base de cálculo expressa em quantidade (campo 10).
Campo 12 – Preenchimento: informar o valor da Cofins referente aos valores consolidados neste registro. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 10) multiplicado pela alíquota aplicável ao item (campo 11).
Campo 13 - Preenchimento: Informar neste campo o Código indicador do modelo de documento fiscal a que se refere a receita demonstrada neste registro, conforme a Tabela 4.1.1.
No caso de escrituração de vendas mediante emissão de NFC-e, deve ser informado o registro com o código “65”, neste campo.
Campo 14 - Preenchimento: Informar neste campo o Código Fiscal de Operação (CFOP) correspondente às operações consolidadas neste registro.
Validação: o valor informado no campo deve existir na Tabela de Código Fiscal de Operação e Prestação, conforme ajuste SINIEF 07/01.
Campo 15 - Preenchimento: informar o Código da Conta Analítica representativa da receita informada neste registro. Exemplos: receita de venda de produtos de fabricação própria, receita de comercialização, receita de revenda de produtos importados, receita de vendas a consumidor final, receita auferida no período, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Atenção:
Para as pessoas jurídicas que adotam o regime de competência para apuração do IR, da CSLL, do PIS/Pasep e da Cofins, devem informar no Campo 15 deste registro o código da conta contábil, representativa das receitas auferidas.
A não informação da conta contábil correspondente às operações, nos registros representativos de receitas e/ou de créditos acarretará:
- Para os fatos geradores até 31 de outubro de 2017, ocorrência de aviso/advertência (não impedindo a validação do registro);
- Para os fatos geradores a partir de 01 de novembro de 2017, ocorrência de erro (impedindo a validação do registro).
Informação de preenchimento – PJ tributadas com base no lucro presumido:
Considerando que o atual programa da EFD-Contribuições (versão 2.1.4) estabelece a obrigatoriedade de se informar nos registros da escrituração, das operações geradoras de receitas e/ou de créditos, a conta contábil (Campo COD_CTA), a partir do período de apuração de novembro de 2017;
Considerando que Instrução Normativa RFB nº 1.774, de 22.12.2017, dispensou da obrigatoriedade da escrituração contábil digital (ECD) as pessoas jurídicas tributadas com base no lucro presumido que não distribuíram, a título de lucro, sem incidência do Imposto sobre a Renda Retido na Fonte (IRRF), parcela de lucros ou dividendos, superior ao valor da base de cálculo do Imposto sobre a Renda diminuída dos impostos e contribuições a que estiver sujeita;
As pessoas jurídicas tributadas com base no lucro presumido não sujeitas à obrigatoriedade da ECD, nos termos da IN RFB nº 1.774/2017, poderão, opcionalmente, informar nos campos "COD_CTAT" dos registros da EFD-Contribuições, para os fatos geradores a partir de novembro/2017, inclusive, a informação "Dispensa de ECD - IN RFB nº 1.774/2017".
Campo 16 - Preenchimento: Informar neste campo as informações complementares relacionadas ao registro, necessárias ou adequadas para tornar a escrituração mais completa e transparente.
<!-- End Registro F560 -->
<!-- Start Registro F569 -->
Registro F569: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “F569”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F569” | C | 004 | - | S |
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
Campo 01 - Valor Válido: [F569]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro F569 -->
<!-- Start Registro F600 -->
Registro F600: Contribuição Retida na Fonte
Neste registro devem ser informados pela pessoa jurídica beneficiária da retenção/recolhimento os valores da contribuição para o PIS/pasep e da Cofins retidos na Fonte, decorrentes de:
1. Pagamentos efetuados por órgãos, autarquias e fundações da administração pública federal à pessoa jurídica titular da escrituração (art. 64 da Lei nº 9.430/96);
2. Pagamentos efetuados por empresas públicas, sociedades de economia mista e demais entidades sob o controle direto ou indireto da União, à pessoa jurídica titular da escrituração (art. 34 da Lei nº 10.833/03);
3. Pagamentos efetuados por outras pessoas jurídicas de direito privado, pela prestação de serviços de limpeza, conservação, manutenção, segurança, vigilância, transporte de valores e locação de mão-de-obra, pela prestação de serviços de assessoria creditícia, mercadológica, gestão de crédito, seleção e riscos, administração de contas a pagar e a receber, bem como pela remuneração de serviços profissionais, prestados pela à pessoa jurídica titular da escrituração (art. 30 da Lei nº 10.833/03);
4. Pagamentos efetuados por associações, inclusive entidades sindicais, federações, confederações, centrais sindicais e serviços sociais autônomos, sociedades simples, inclusive sociedades cooperativas, fundações de direito privado ou condomínios edilícios, pela prestação de serviços de limpeza, conservação, manutenção, segurança, vigilância, transporte de valores e locação de mão-de-obra, pela prestação de serviços de assessoria creditícia, mercadológica, gestão de crédito, seleção e riscos, administração de contas a pagar e a receber, bem como pela remuneração de serviços profissionais, prestados pela à pessoa jurídica titular da escrituração (art. 30 da Lei nº 10.833/03);
5. Pagamentos efetuados por órgãos, autarquias e fundações da administração pública estadual, distrital ou municipal, à pessoa jurídica titular da escrituração (art. 33 da Lei nº 9.430/96);
6. Pagamentos efetuados por pessoa jurídica fabricante de veículos e peças, referentes à aquisição de autopeças junto à pessoa jurídica titular da escrituração (art. 3º da Lei nº 10.485/02);
7. Outras hipóteses de retenção na fonte das referidas contribuições sociais, previstas na legislação tributária.
Além das hipóteses de retenção na fonte acima especificadas, devem também ser escriturados neste registro os valores recolhidos de PIS/Pasep e de Cofins, pelas sociedades cooperativas que se dedicam a vendas em comum, referidas no art. 82 da Lei nº 5.764/71, que recebam para comercialização a produção de suas associadas, conforme disposto no art. 66 da Lei nº 9.430/96.
A escrituração no registro F600 dos recolhimentos de PIS/Pasep e de Cofins, efetuados pelas sociedades cooperativas nos termos do art. 66 da Lei nº 9.430/96, deve ser efetuada:
- Pela pessoa jurídica benefíciária do recolhimento (pessoa jurídica associada/cooperada), com base nos valores informados pela cooperativa quanto aos valores de PIS/Pasep e Cofins pagos. Neste caso, deve ser informado no Campo 11 (IND_DEC) o indicador “0”;
- Pela sociedade cooperativa responsável pelo recolhimento, decorrente da comercialização ou da entrega para  revenda à central de cooperativas. Neste caso, deve ser informado no Campo 11 (IND_DEC) o indicador “1”
Os valores efetivamente retidos na fonte de PIS/Pasep e de Cofins, escriturados neste registro, são passíveis de dedução da contribuição apurada nos Registros M200 (PIS/Pasep) e M600 (Cofins), respectivamente.
Atenção: As retenções efetivamente sofridas pela PJ no mês da escrituração, informadas neste registro, nos campos 09 (PIS/Pasep) e 10 (Cofins), não são recuperadas de forma automática nos respectivos registros apuração das contribuições M200 (PIS/Pasep) e M600 (Cofins), devendo ser sempre informados pela própria pessoa jurídica no arquivo importado pelo PVA ou complementado pela edição, no próprio PVA, dos registros M200 e M600.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F600" | C | 004* | - | S |
| 02 | IND_NAT_RET | Indicador de Natureza da Retenção na Fonte: 01 - Retenção por Órgãos, Autarquias e Fundações Federais 02 - Retenção por outras Entidades da Administração Pública Federal 03 - Retenção por Pessoas Jurídicas de Direito Privado 04 - Recolhimento por Sociedade Cooperativa 05 - Retenção por Fabricante de Máquinas e Veículos 99 - Outras Retenções | N | 002* | - | S |
| 03 | DT_RET | Data da Retenção | N | 008* | - | S |
| 04 | VL_BC_RET | Base de calculo da retenção ou do recolhimento (sociedade cooperativa) | N | - | 04 | S |
| 05 | VL_RET | Valor Total Retido na Fonte / Recolhido (sociedade cooperativa) | N | - | 02 | S |
| 06 | COD_REC | Código da Receita | C | 004 | - | N |
| 07 | IND_NAT_REC | Indicador da Natureza da Receita: 0 – Receita de Natureza Não Cumulativa 1 – Receita de Natureza Cumulativa | N | 001* | - | N |
| 08 | CNPJ | CNPJ referente a: - Fonte Pagadora Responsável pela Retenção / Recolhimento (no caso de o registro ser escriturado pela pessoa jurídica beneficiária da retenção); ou - Pessoa Jurídica Beneficiária da Retenção / Recolhimento (no caso de o registro ser escriturado pela pessoa jurídica responsável pela retenção). | N | 014* | - | S |
| 09 | VL_RET_PIS | Valor Retido na Fonte – Parcela Referente ao PIS/Pasep | N | - | 02 | S |
| 10 | VL_RET_COFINS | Valor Retido na Fonte – Parcela Referente a COFINS | N | - | 02 | S |
| 11 | IND_DEC | Indicador da condição da pessoa jurídica declarante: 0 – Beneficiária da Retenção / Recolhimento 1- Responsável pelo Recolhimento | N | 001* | - | S |

Observações: A escrituração do Registro F600 corresponde tão somente à informação dos valores efetivamente retidos na fonte, a título de PIS/Pasep e de Cofins, quando do pagamento pelas fontes pagadoras. Desta forma, este registro não deve ser preenchido com base nos valores destacados em notas fiscais de vendas (visão documental) e sim, com base nos valores efetivamente retidos pelas fontes pagadoras (visão financeira).
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [F600]
Campo 02 - Preenchimento: Informar neste campo o indicador da natureza da retenção na fonte objeto de escrituração neste registro.
Valores Válidos: [01,02,03,04,05,99]
Campo 03 - Preenchimento: informar neste campo a data de retenção. No caso de haver mais de retenção/recolhimento no período, ou no caso da data ser desconhecida pela pessoa jurídica beneficiária da retenção/recolhimento, informar a data final da escrituração (Campo 07 do Registro “0000”).
Validação: o valor informado deve ser menor ou igual à DT_FIN deste arquivo.
Campo 04 - Preenchimento: informar neste campo o valor da base de cálculo referente à retenção sofrida. No caso da pessoa jurídica beneficiária da retenção não conhecer a base de cálculo (valor da base de cálculo das retenções na fonte efetuada pela fonte pagadora), informar neste campo o valor líquido recebido da fonte pagadora, acrescido dos valores retidos na fonte, a título de IR, CSLL, PIS e Cofins.
Exemplo: Considerando que a fonte pagadora ao pagar uma fatura no valor de R$ 1.000,00, tenha efetuado a retenção de R$ 45,00 (1% a título de CSLL; 0,65% a título de PIS e 3% a título de Cofins), efetuando assim o pagamento líquido de R$ 955,00, o valor a ser informado no Campo 04 será:
Valor líquido recebido da fonte pagadora: R$ 955,00;
Valor total das contribuições retidas na fonte (CSLL, PIS/Pasep e Cofins): R$ 45,00
Valor a ser informado no Campo 04: R$ 955,00 + R$ 45,00 = R$ 1.000,00
No caso de sociedades cooperativas, para informar a base de cálculo do(s) recolhimento(s) por ela efetuado(s), decorrentes da receita de venda de produtos entregues por suas associadas pessoas jurídicas. No caso do recolhimento incidir sobre bases de cálculos diversas (com base na receita bruta ou com base em unidade de medida de produto), deve escriturar um registro para cada base de cálculo sujeita ao recolhimento, mesmo que este seja efetuado em um único DARF.
Campo 05 - Preenchimento: informar neste campo o valor da retenção na fonte ou do recolhimento (sociedade cooperativa), conforme o caso. No caso da pessoa jurídica não conhecer o valor total retido na fonte pela fonte pagadora (valores constantes no(s) DARF(s)) como, por exemplo, em função do recolhimento total também contar outros tributos (IR e CSLL), deve informar neste campo o valor correspondente ao somatório dos valores retidos a título de PIS/Pasep (campo 09) e de Cofins (campo 10).
Campo 06 - Preenchimento: informar neste campo o código de receita referente à retenção ou ao recolhimento. No caso da pessoa jurídica beneficiária da retenção desconhecer o código de receita, o campo deve ser informado em branco.
Campo 07 - Preenchimento: informar neste campo o indicador da natureza da receita que sofreu retenção na fonte ou recolhimento. No caso do valor retido/recolhido ser referente a receita não cumulativa e cumulativa, informar o indicador “0”.
Valores válidos: [0,1]
Campo 08 - Preenchimento: deve ser informado neste campo:
- No caso de escrituração pela pessoa jurídica beneficiária da retenção ou do recolhimento (PJ cooperada), informar o CNPJ da pessoa jurídica que efetuou a retenção;
- No caso de escrituração pela sociedade cooperativa que efetuou o recolhimento, informar o CNPJ da pessoa jurídica associada.
Campo 09 - Preenchimento: informar neste campo a parcela da retenção na fonte referente ao PIS/Pasep ou, no caso da sociedade cooperativa, o valor recolhido referente ao PIS/Pasep.
Campo 10 - Preenchimento: informar neste campo a parcela da retenção na fonte referente à Cofins ou, no caso da sociedade cooperativa, o valor recolhido referente a Cofins.
Campo 11 - Preenchimento: Informar neste campo se as informações constantes no registro estão sendo prestadas:
- pela pessoa jurídica beneficiária da retenção ou do recolhimento (PJ cooperada), neste caso deve ser informado o indicador "0"; ou
- pela sociedade cooperativa responsável pelo recolhimento, neste caso deve ser informado o indicador "1".
Valores Válidos: [0,1]
<!-- End Registro F600 -->
<!-- Start Registro F700 -->
Registro F700: Deduções Diversas
Neste registro devem ser informadas as deduções diversas previstas na legislação tributária, inclusive os créditos que não sejam específicos do regime não-cumulativo, passiveis de dedução na determinação da contribuição social a recolher, nos registros M200 (PIS/Pasep) e M600 (Cofins). A chave deste registro é composta pelos campos IND_ORI_DED + IND_NAT_DED + CNPJ, ou seja, não poderá existir dois ou mais registros F700 com os mesmos valores nestes campos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F700" | C | 004* | - | S |
| 02 | IND_ORI_DED | Indicador de Origem de Deduções Diversas: 01 – Créditos Presumidos - Medicamentos 02 – Créditos Admitidos no Regime Cumulativo – Bebidas Frias 03 – Contribuição Paga pelo Substituto Tributário - ZFM 04 – Substituição Tributária – Não Ocorrência do Fato Gerador Presumido 99 - Outras Deduções | N | 002* | - | S |
| 03 | IND_NAT_DED | Indicador da Natureza da Dedução: 0 – Dedução de Natureza Não Cumulativa 1 – Dedução de Natureza Cumulativa | N | 001* | - | S |
| 04 | VL_DED_PIS | Valor a Deduzir - PIS/PASEP | N | - | 02 | S |
| 05 | VL_DED_COFINS | Valor a Deduzir – Cofins | N | - | 02 | S |
| 06 | VL_BC_OPER | Valor da Base de Cálculo da Operação que ensejou o Valor a Deduzir informado nos Campos 04 e 05 | N | - | 02 | N |
| 07 | CNPJ | CNPJ da Pessoa Jurídica relacionada à Operação que ensejou o Valor a Deduzir informado nos Campos 04 e 05. | N | 014* | - | N |
| 08 | INF_COMP | Informações Complementares do Documento/Operação que ensejou o Valor a Deduzir informado nos Campos 04 e 05. | C | 090 | - | N |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [F700]
Campo 02 - Preenchimento: Informar neste campo o indicador referente à origem ou natureza da operação a ser escriturada como dedução.
Valores Válidos: [01,02,03,04,99]
Campo 03 - Preenchimento: informar neste campo o indicador da natureza da dedução. No caso da dedução estar relacionada a uma operação de natureza não cumulativa, informar o indicador “0”. No caso da dedução estar relacionada a uma operação de natureza cumulativa, informar o indicador “1”.
Valores válidos: [0,1]
Campo 04 - Preenchimento: informar neste campo a parcela da dedução referente ao PIS/Pasep.
Campo 05 - Preenchimento: informar neste campo a parcela da dedução referente à Cofins.
Campo 06 - Preenchimento: informar neste campo a base de cálculo da operação que ensejou o valor a deduzir informado nos Campos 04 e 05.
Campo 07 - Preenchimento: informar neste campo o CNPJ da pessoa jurídica relacionada à operação que ensejou o Valor a Deduzir informado nos Campos 04 e 05.
O Campo 07 (CNPJ) não é de preenchimento obrigatório, quando o indicador de origem da operação informado no Campo 02 (IND_ORI_DED) for igual a “01 – Créditos Presumidos – Medicamentos”. No caso de créditos presumidos do setor de bebidas frias, referentes ao ressarcimento à CMB, recolhidos mediante DARF, informar o CNPJ do estabelecimento industrial envasador das bebidas.
Campo 08 - Preenchimento: Neste campo devem constar as informações complementares do documento ou da operação que ensejou a determinação do valor a deduzir informado nos campos 04 e 05.
<!-- End Registro F700 -->
<!-- Start Registro F800 -->
Registro F800: Créditos Decorrentes de Eventos de Incorporação, Fusão e Cisão
Devem ser escriturados neste registro os créditos oriundos da versão de bens e direitos referidos no art. 3º das Leis nº 10.637/2002 e nº 10.833/2003, bem como os créditos referentes à importação referidos na Lei nº 10.865/2004, transferidos em decorrência de eventos de fusão, incorporação e cisão de pessoa jurídica domiciliada no País, relacionando-os por cada tipo, conforme Tabela 4.3.6. da EFD-Contribuições.
A pessoa jurídica sucessora titular da escrituração, deve informar o CNPJ da sucedida, a natureza e a data do evento, origem e tipo de crédito, mês e ano em que foi apurado o crédito e o valor do crédito disponível (Valor do crédito transferido).
Estes créditos são vertidos para a pessoa jurídica sucessora sob as mesmas condições em que foram apurados na pessoa jurídica sucedida, passíveis de utilização para desconto da contribuição devida no período, se decorrentes de operações no mercado interno ou, ainda, de compensação e ressarcimento, se decorrentes de operações de exportação ou não tributadas no mercado interno.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F800" | C | 004* | - | S |
| 02 | IND_NAT_EVEN | Indicador da Natureza do Evento de Sucessão: 01 – Incorporação 02 – Fusão 03 – Cisão Total 04 – Cisão Parcial 99 – Outros | N | 002* | - | S |
| 03 | DT_EVEN | Data do Evento | N | 008* | - | S |
| 04 | CNPJ_SUCED | CNPJ da Pessoa Jurídica Sucedida | N | 014* | - | S |
| 05 | PA_CONT_CRED | Período de Apuração do Crédito – Mês/Ano (MM/AAAA) | N | 006* | - | S |
| 06 | COD_CRED | Código do crédito transferido, conforme Tabela 4.3.6 | N | 003* | - | S |
| 07 | VL_CRED_PIS | Valor do Crédito Transferido de PIS/Pasep | N | - | 02 | S |
| 08 | VL_CRED_COFINS | Valor do Crédito Transferido de Cofins | N | - | 02 | S |
| 09 | PER_CRED_CIS | Percentual do crédito original transferido, no caso de evento de Cisão. | N | 006 | 02 | N |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [F800]
Campo 02 - Preenchimento: Informar neste campo a natureza do evento de sucessão, que resultou na apropriação/ recebimento de créditos..
Valores Válidos: [01,02,03,04,99]
Campo 03 - Preenchimento: informar neste campo a data do evento de sucessão a que se refere o crédito escriturado neste registro.
Validação: o valor informado deve ser menor ou igual à DT_FIN deste arquivo.
Campo 04 - Preenchimento: informar neste campo o CNPJ da pessoa jurídica sucedida, que apurou o crédito em período anterior ao do evento.
Campo 05 - Preenchimento: informar neste campo o período de apuração do crédito, apurado pela pessoa jurídica sucedida.
Campo 06 - Preenchimento: informar neste campo o código do tipo de crédito transferido e relacionado neste registro, conforme a Tabela 4.3.6 do Leiaute da EFD-Contribuições (Tabela Código de Tipo de Crédito).
Campo 07- Preenchimento: informar neste campo o valor do crédito de PIS/Pasep adquirido em decorrência do evento de sucessão.
Campo 08- Preenchimento: informar neste campo o valor do crédito de Cofins adquirido em decorrência do evento de sucessão
Campo 09 - Preenchimento: informar neste campo o percentual do crédito original transferido, no caso de evento de Cisão.
<!-- End Registro F800 -->
<!-- Start Registro F990 -->
Registro F990: Encerramento do Bloco F
Este registro destina-se a identificar o encerramento do bloco F e informar a quantidade de linhas (registros) existentes no bloco.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "F990" | C | 004 | - | S |
| 02 | QTD_LIN_F | Quantidade total de linhas do Bloco F | N | - | - | S |

Observações: Registro obrigatório, se existir o Registro F001 no arquivo.
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Validação do Registro: registro único e obrigatório para todos os informantes da EFD-Contribuições.
Campo 01 - Valor Válido: [F990]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco F é igual ao valor informado no campo QTD_LIN_F (registro F990).
<!-- End Registro F990 -->