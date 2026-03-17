# Bloco M - Versão 1.35

BLOCO M – Apuração da Contribuição e Crédito do PIS/Pasep e da Cofins
Os registros componentes dos Blocos "M" são escriturados na visão da empresa, diferentemente dos registros informados nos Blocos "A", "C", "D" e "F" que são informados na visão de cada estabelecimento da pessoa jurídica que realizou as operações gerados de contribuições sociais ou de créditos.
<!-- Start Registro M001 -->
Registro M001: Abertura do Bloco M

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M001" | C | 004* | - | S |
| 02 | IND_MOV | Indicador de movimento: 0- Bloco com dados informados; 1- Bloco sem dados informados | C | 001* | - | S |

Observações: Registro obrigatório
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Campo 01 - Valor Válido: [M001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro M001 -->
<!-- Start Registro M100 -->
Registro M100: Crédito de PIS/Pasep Relativo ao Período
Este registro tem por finalidade realizar a consolidação do crédito relativo à contribuição para o PIS/PASEP apurado no período. Deve ser gerado um registro M100 especifico para cada tipo de crédito apurado (vinculados à receita tributada, vinculados à receita não tributada e vinculados à exportação), conforme a Tabela de tipos de créditos “Tabela 4.3.6”, bem como para créditos de operações próprias e créditos transferidos por eventos de sucessão.
ATENÇÃO: Os valores escriturados nos registros M100 (Crédito de PIS/Pasep do Período) e M105 (Detalhamento da Base de Cálculo do Crédito de PIS/Pasep do Período) serão determinados com base:
Nos valores informados no arquivo elaborado pela própria pessoa jurídica e importado pelo Programa Validador e Assinador da EFD-Contribuições – PVA, os quais serão objeto de validação; ou
Nos valores calculados pelo PVA para os registros M100 e M105, através da funcionalidade “Gerar Apurações”, disponibilizada no PVA, com base nos registros da escrituração constantes nos Blocos “A”, “C”, “D” e “F”.
No caso de operações e documentos informados nos referidos blocos em que os campos “CST_PIS” se refiram a créditos comuns a mais de um tipo de receitas (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA procederá o cálculo automático do crédito (funcionalidade “Gerar Apurações”) caso a pessoa jurídica tenha optado pelo método de apropriação com base no Rateio Proporcional com base na Receita Bruta (indicador “2” no Campo 03 do Registro 0110), considerando para fins de rateio, no Registro M105, os valores de Receita Bruta informados no Registro 0111.
Desta forma, caso a pessoa jurídica tenha optado pelo método do Rateio Proporcional com base na Receita Bruta Bruta (indicador “2” no Campo 03 do Registro 0110), o PVA procederá ao cálculo automático do crédito em relação a todos os Códigos de Situação Tributária (CST 50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65 e 66).
Caso a pessoa jurídica tenha optado pelo método de Apropriação Direta (indicador “1” no Campo 03 do Registro 0110) para a determinação dos créditos comuns a mais de um tipo de receita (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA não procederá ao cálculo dos créditos (funcionalidade “Gerar Apurações”) relacionados a estes CST, no Registro M105, gerando o cálculo dos créditos apenas em relação aos CST 50, 51, 52, 60, 61 e 62.
Neste caso, deve a pessoa jurídica editar os registros M105 correspondentes ao CST representativos de créditos comuns (CST 53, 54, 55, 56, 63, 64, 65 e 66), com base na apropriação direta, inclusive em relação aos custos, por meio de sistema de contabilidade de custos integrada e coordenada com a escrituração, conforme definido no § 8º do art. 3º, da Lei nº 10.637, de 2002.
A geração automática de apuração (funcionalidade “Gerar Apurações”) o PVA apura, em relação ao Registro M100, apenas os valores dos campos 02 (COD_CRED), 03 (IND_CRED_ORI), 04 (VC_BC_PIS), 05 (ALIQ_PIS), 06 (QUANT_BC_PIS), 07 (ALIQ_PIS_QUANT) e 08 (VL_CRED). Os campos de ajustes (Campos 09 e 10) e de diferimento (Campos 11 e 12) não serão recuperados na geração automática de apuração, devendo sempre serem informados pela própria pessoa jurídica no arquivo importado pelo PVA ou complementado pela edição do registro M100.
Na funcionalidade de geração automática de apuração, os valores apurados e preenchidos pelo PVA irão sobrepor (substituir) os valores eventualmente existentes nos referidos campos, constantes na escrituração.
As pessoas jurídicas sujeitas exclusivamente ao regime cumulativo das contribuições não devem preencher este registro, devendo eventuais créditos admitidos no regime cumulativo serem informados no registro F700 e consolidados em M200 (Campo 11 - VL_OUT_DED_CUM). Para as demais pessoas jurídicas (exceto atividade imobiliária), deverá existir um registro M100 para cada tipo de crédito e alíquota informados nos documentos que constam dos registros A100/A170, C100/C170, C190/C191, C395/C396, C500/C501, D100/D101, D500/D501, F100, F120, F130 e F150.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M100" | C | 004* | - | S |
| 02 | COD_CRED | Código de Tipo de Crédito apurado no período, conforme a Tabela 4.3.6. | C | 003* | - | S |
| 03 | IND_CRED_ORI | Indicador de Crédito Oriundo de: 0 – Operações próprias 1 – Evento de incorporação, cisão ou fusão | N | 001* | - | S |
| 04 | VL_BC_PIS | Valor da Base de Cálculo do Crédito | N | - | 02 | N |
| 05 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 06 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS | N | - | 03 | N |
| 07 | ALIQ_PIS_QUANT | Alíquota do PIS (em reais) | N | - | 04 | N |
| 08 | VL_CRED | Valor total do crédito apurado no período | N | - | 02 | S |
| 09 | VL_AJUS_ACRES | Valor total dos ajustes de acréscimo | N | - | 02 | S |
| 10 | VL_AJUS_REDUC | Valor total dos ajustes de redução | N | - | 02 | S |
| 11 | VL_CRED_DIF | Valor total do crédito diferido no período | N | - | 02 | S |
| 12 | VL_CRED_DISP | Valor Total do Crédito Disponível relativo ao Período (08 + 09 – 10 – 11) | N | - | 02 | S |
| 13 | IND_DESC_CRED | Indicador de opção de utilização do crédito disponível no período: 0 – Utilização do valor total para desconto da contribuição apurada no período, no Registro M200; 1 – Utilização de valor parcial para desconto da contribuição apurada no período, no Registro M200. | C | 001* | - | S |
| 14 | VL_CRED_DESC | Valor do Crédito disponível, descontado  da contribuição apurada no próprio período. Se IND_DESC_CRED=0, informar o valor total do Campo 12; Se IND_DESC_CRED=1, informar o valor parcial do Campo 12. | N | - | 02 | N |
| 15 | SLD_CRED | Saldo de créditos a utilizar em períodos futuros (12 – 14) | N | - | 02 | S |

Observações:
1. Deve ser gerado um registro M100 especifico para cada tipo de crédito apurado (vinculados a receita tributada, vinculados a receita não tributada e vinculados a exportação), conforme a Tabela de tipos de créditos “Tabela 4.3.6”.
2. A base de cálculo do crédito, determinada no Campo “VL_BC_PIS” deste registro, deve ser recuperada e corresponder ao somatório dos Campos “VL_BC_PIS”  de todos os registros Filho “M105”, que detalham a composição da base de cálculo do crédito.
3. No caso do crédito ser determinado com base em Unidade de Medida de Produto (crédito código 103, 203 e 303 da Tabela 4.3.6), a base de cálculo a ser determinada no Campo “QUANT_BC_PIS” deste registro, deve ser recuperada e corresponder ao somatório dos Campos “QUANT_BC_PIS” de todos os registros Filho “M105”, que detalham a composição da base de cálculo do crédito em quantidade.
Nível hierárquico – 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [M100]
Campo 02 - Preenchimento: informe o código do tipo do crédito cujo crédito está sendo totalizado no registro, conforme a Tabela “4.3.6 – Tabela Código de Tipo de Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Os códigos dos tipos de créditos são definidos a partir das informações de CST e Alíquota constantes nos documentos e operações registrados nos blocos A, C, D e F.
O CST 50 é mapeado para o grupo 100 (crédito vinculado exclusivamente a receita tributada no mercado interno), o CST 51 para o grupo 200 (crédito vinculado exclusivamente a receita não tributada no mercado interno) e o CST 52 para o grupo 300 (crédito vinculado exclusivamente a receita de exportação).
Os CST 53 a 56 se referem a créditos vinculados a mais de um tipo de receita. Assim, por exemplo, o CST 56 está relacionado a créditos aos 03 tipos de receitas (grupos 100, 200 e 300), conforme rateio proporcional da receita bruta (com base nos valores informados no registro 0111) ou com base no método da apropriação direta, e assim sucessivamente.
Caso o CST se refira a crédito presumido (60 a 66) o crédito será identificado com os códigos 106, 206 ou 306, quando se tratar de crédito presumido da agroindústria, ou os códigos 107, 207 ou 307, quando se tratar de outras hipóteses de crédito presumido (como no caso da subcontratação de transporte de cargas, pelas empresas de transporte de cargas), conforme o caso.
Dentro dos grupos, a alíquota informada determina se o código será o 101 (alíquotas básicas), 102 (alíquotas diferenciadas), 103 (alíquotas em reais) ou 105 (embalagens para revenda).
Os códigos vinculados à importação (108, 208 e 308) são obtidos através da informação de CFOP iniciado em 3 (quando existente) ou pelo campo IND_ORIG_CRED nos demais casos.
O código 109 (atividade imobiliária) é obtido diretamente dos registros F205 e F210, bem como os códigos relativos ao estoque de abertura (104, 204 e 304), os quais são obtidos diretamente do registro F150 (NAT_BC_CRED = 18).
Campo 03 - Valores válidos: [0, 1]
Campo 04 - Preenchimento: informe o somatório dos Campos “VL_BC_PIS” de todos os registros Filho “M105”, que detalham a composição da base de cálculo do respectivo crédito.  No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800. Para créditos da atividade imobiliária (COD_CRED = 109), este campo também não deverá ser preenchido, visto que o crédito é recuperado diretamente dos registros F205 e F210 para o campo 08 - VL_CRED. No caso de crédito apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 06 - QUANT_BC_PIS.
Campo 05 - Preenchimento: informe a alíquota aplicável à base de crédito informada no registro. No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800.
Para créditos da atividade imobiliária (COD_CRED = 109), este campo também não deverá ser preenchido, visto que o crédito é recuperado diretamente dos registros F205 e F210 para o campo 08 - VL_CRED.
No caso de crédito apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 07 - ALIQ_PIS_QUANT.
Campo 06 - Preenchimento: informe o somatório dos Campos “QUANT_BC_PIS”  de todos os registros Filho “M105”, que detalham a composição da base de cálculo do respectivo crédito.  No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800. No caso de crédito não apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 04 - VL_BC_PIS. O preenchimento deste campo só é admitido nos casos de COD_CRED ser 103, 203, 303, 105, 205, 305, 108, 208 e 308.
Campo 07 - Preenchimento: informe a alíquota em reais aplicável à base de crédito informada no registro. No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800. No caso de crédito não apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 05 - ALIQ_PIS. O preenchimento deste campo só é admitido nos casos de COD_CRED ser 103, 203, 303, 105, 205, 305, 108, 208 e 308.
Campo 08 - Preenchimento: informe o valor total do respectivo crédito apurado no período. No caso de crédito apurado pela própria pessoa jurídica, por unidade de medida de produto, o valor deste campo corresponderá à multiplicação dos campos 06 (QUANT_BC_PIS) e 07 (ALIQ_PIS_QUANT). Caso contrário deverá ser igual à multiplicação dos campos 04 (VL_BC_CRED) e 05 (ALIQ_PIS), dividido por 100 (cem).
No caso de crédito da atividade imobiliária (COD_CRED = 109) este campo será recuperado pela soma dos campos VL_CRED_PIS_DESC do registro F205 e VL_CRED_PIS_UTIL do registro F210. Nos casos de créditos transferidos por operação de sucessão, este campo será recuperado pelo somatório do campo VL_CRED_PIS dos registros F800 de mesmo COD_CRED.
Campo 09 - Preenchimento: informar o valor a ser adicionado por ajuste ao crédito do período. O preenchimento deste campo obriga o preenchimento do registro M110, sendo que o valor deve corresponder à soma do campo VL_AJ dos registros M110 onde o campo IND_AJ for igual a 1.
Campo 10 - Preenchimento: informar o valor a ser subtraído por ajuste ao crédito do período. O preenchimento deste campo obriga o preenchimento do registro M110, sendo que o valor deve corresponder à soma do campo VL_AJ dos registros M110 onde o campo IND_AJ for igual a 0.
Campo 11 - Preenchimento: informar o valor dos créditos da não-cumulatividade vinculados às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998). O preenchimento deste campo obriga o preenchimento do registro M230, devendo o somatório dos respectivos campos dos registros M100 ser igual ao somatório dos campos VL_CRED_DIF dos registros M230, para o mesmo COD_CRED.
Validação: O valor deste campo não pode ser maior que VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC.
Campo 12 - Preenchimento: informar o valor total do respectivo crédito disponível relativo ao período, correspondendo à VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC - VL_CRED_DIF.
Campo 13 - Valores válidos: [0, 1]
Preenchimento: Preencher com o valor 0, se a totalidade do valor do respectivo crédito disponível no período deve ser utilizada para desconto da contribuição apurada. No caso da apuração ser gerada automaticamente pelo PVA, o aproveitamento do crédito ocorrerá com o da a menor disponibilidade (vinculado à receita tributada no mercado interno) para o de maior (vinculado à receita de exportação). No caso de opção de aproveitamento parcial, o valor parcial do crédito a ser aproveitado para desconto da contribuição apurada deverá ser informado no campo 14 - VL_CRED_DESC. Quando o PVA gera automaticamente a apuração este campo é preenchido automaticamente, com base no valor aproveitado para desconto da contribuição apurada no registro M200.
Campo 14 - Preenchimento: informar o valor do crédito disponível, descontado da contribuição apurada no próprio período, no registro M200. Caso o campo 13 (IND_DESC_CRED) seja preenchido com o valor 0, informar o valor total do Campo 12, caso contrário informar o valor parcial do Campo 12.
Quando o PVA gera automaticamente a apuração este campo é preenchido automaticamente, com base no valor aproveitado para desconto da contribuição apurada no registro M200. A informação preenchida pela PJ neste campo será sobrescrita pelo PVA quando da geração automática da apuração. Caso necessário, faça os devidos ajustes neste campo (e no campo 13, se for o caso), bem como no respectivo campo do registro M200 (VL_TOT_CRED_DESC).
Campo 15 - Preenchimento: informar o valor do saldo credor para aproveitamento futuro. O valor informado deverá corresponder a "VL_CRED_DISP" – "VL_CRED_DESC".
<!-- End Registro M100 -->
<!-- Start Registro M105 -->
Registro M105: Detalhamento da Base de Calculo do Crédito Apurado no Período – PISPasep
Neste registro será informada a composição da base de cálculo de cada tipo de crédito (M100), conforme as informações constantes nos documentos e operações com CST geradores de créditos, escriturados nos Blocos “A”, “C”, “D” e “F”.
Os valores representativos de Bases de Cálculo  escriturados nestes registros serão transferidos para o Registro PAI M100 (Campos 04 e 06), que especifica e escritura os diversos tipos de créditos da escrituração.
Deve ser escriturado um registro M105 para cada CST recuperado dos registros dos Blocos “A”, “C”, “D” e “F”, vinculado ao tipo de crédito informado no Registro M100.
ATENÇÃO: Os valores escriturados nos registros M100 (Crédito de PIS/Pasep do Período) e M105 (Detalhamento da Base de Cálculo do Crédito de PIS/Pasep do Período) serão determinados com base:
Nos valores informados no arquivo elaborado pela própria pessoa jurídica e importado pelo Programa Validador e Assinador da EFD-Contribuições – PVA, os quais serão objeto de validação; ou
Nos valores calculados pelo PVA para os registros M100 e M105, através da funcionalidade “Gerar Apurações”, disponibilizada no PVA, com base nos registros da escrituração constantes nos Blocos “A”, “C”, “D” e “F”.
No caso de operações e documentos informados nos referidos blocos em que os campos “CST_PIS” se refiram a créditos comuns a mais de um tipo de receitas (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA procederá o cálculo automático do crédito (funcionalidade “Gerar Apurações”) caso a pessoa jurídica tenha optado pelo método de apropriação com base no Rateio Proporcional com base na Receita Bruta (indicador “2” no Campo 03 do Registro 0110), considerando para fins de rateio, no Registro M105, os valores de Receita Bruta informados no Registro 0111.
Desta forma, caso a pessoa jurídica tenha optado pelo método do Rateio Proporcional com base na Receita Bruta (Bruta (indicador “2” no Campo 03 do Registro 0110), o PVA procederá ao cálculo automático do crédito em relação a todos os Códigos de Situação Tributária (CST 50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65 e 66)
Caso a pessoa jurídica tenha optado pelo método de Apropriação Direta (indicador “1” no Campo 03 do Registro 0110) para a determinação dos créditos comuns a mais de um tipo de receita (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA não procederá ao cálculo do crédito (funcionalidade “Gerar Apurações”) relacionados a estes CST, no Registro M105, gerando o cálculo dos créditos apenas em relação aos CST 50, 51, 52, 60, 61 e 62. Neste caso, deve a pessoa jurídica editar os registros M105 correspondentes ao CST representativos de créditos comuns (CST 53, 54, 55, 56, 63, 64, 65 e 66), com base na apropriação direta, inclusive em relação aos custos, por meio de sistema de contabilidade de custos integrada e coordenada com a escrituração, conforme definido no § 8º do art. 3º, da Lei nº 10.637, de 2002.
Na funcionalidade de geração automática de apuração, os valores apurados e preenchidos pelo PVA irão sobrepor (substituir) os valores eventualmente existentes nos referidos campos, constantes na escrituração.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M105" | C | 004* | - | S |
| 02 | NAT_BC_CRED | Código da Base de Cálculo do Crédito apurado no período, conforme a Tabela 4.3.7. | C | 002* | - | S |
| 03 | CST_PIS | Código da Situação Tributária referente ao crédito de PIS/Pasep (Tabela 4.3.3) vinculado ao tipo de crédito escriturado em M100. | N | 002* | - | S |
| 04 | VL_BC_PIS_TOT | Valor Total da Base de Cálculo escriturada nos documentos e operações (Blocos “A”, “C”, “D” e “F”), referente ao CST_PIS informado no Campo 03. | N | - | 02 | N |
| 05 | VL_BC_PIS_CUM | Parcela do Valor Total da Base de Cálculo informada no Campo 04, vinculada a receitas com incidência cumulativa. Campo de preenchimento específico para a pessoa jurídica sujeita ao regime cumulativo e não-cumulativo da contribuição (COD_INC_TRIB = 3 do Registro 0110) | N | - | 02 | N |
| 06 | VL_BC_PIS_NC | Valor Total da Base de Cálculo do Crédito, vinculada a receitas com incidência não-cumulativa (Campo 04 – Campo 05). | N | - | 02 | N |
| 07 | VL_BC_PIS | Valor da Base de Cálculo do Crédito, vinculada ao tipo de Crédito escriturado em M100. - Para os CST_PIS = “50”, “51”, “52”, “60”, “61” e “62”: Informar o valor do Campo 06 (VL_BC_PIS_NC); - Para os CST_PIS = “53”, “54”, “55”, “56”, “63”, “64” “65” e “66” (Crédito sobre operações vinculadas a mais de um tipo de receita): Informar a parcela do valor do Campo 06 (VL_BC_PIS_NC) vinculada especificamente ao tipo de crédito escriturado em M100.  O valor deste campo será transportado para o Campo 04 (VL_BC_PIS) do registro M100. | N | - | 02 | N |
| 08 | QUANT_BC_PIS_TOT | Quantidade Total da Base de Cálculo do Crédito apurado em Unidade de Medida de Produto, escriturada nos documentos e operações (Blocos “A”, “C”, “D” e “F”), referente ao CST_PIS informado no Campo 03 | N | - | 03 | N |
| 09 | QUANT_BC_PIS | Parcela da base de cálculo do crédito em quantidade (campo 08) vinculada ao tipo de crédito escriturado em M100. - Para os CST_PIS = “50”, “51” e “52”: Informar o valor do Campo 08 (QUANT_BC_PIS); - Para os CST_PIS = “53”, “54”, “55” e “56” (crédito vinculado a mais de um tipo de receita): Informar a parcela do valor do Campo 08 (QUANT_BC_PIS) vinculada ao tipo de crédito escriturado em M100.  O valor deste campo será transportado para o Campo 06 (QUANT_BC_PIS) do registro M100. | N | - | 03 | N |
| 10 | DESC_CRED | Descrição do crédito | C | 060 | - | N |

Observações:
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [M105]
Campo 02 - Preenchimento: Informar neste campo a Natureza da Base de Cálculo do crédito, conforme códigos constantes na Tabela de Base de Cálculo do Crédito (4.3.7), tais como: Aquisição de bens para revenda; aquisição de insumos para produção de bens ou prestação de serviços; despesas com energia elétrica; despesas com aluguéis, encargos de depreciação de bens incorporados ao ativo imobilizado, etc. Será gerado um Registro M105 para cada fato gerador de crédito constante na escrituração.
Campo 03 - Preenchimento: Deve ser informado neste campo 03 o Código da Situação Tributária (CST – conforme Tabela 4.3.3) referente ao crédito de PIS/Pasep vinculado ao tipo de crédito escriturado em M100, conforme relação abaixo:
- Crédito Vinculado à Receita Tributada (Grupo 100): CST 50, 53, 54, 56, 60, 63, 64 e 66.
- Crédito Vinculado à Receita Não Tributada (Grupo 200): CST 51, 53, 55, 56, 61, 63, 65 e 66.
- Crédito Vinculado à Receita de Exportação (Grupo 300): CST 52, 54, 55, 56, 62, 64, 65 e 66.
Campo 04 - Preenchimento: Será informado neste campo o valor das bases de cálculo do crédito informadas nos Blocos “A”, “C”, “D” e “F”, correspondente a cada CST recuperado, formando assim, a base de calculo total dos documentos e operações escrituradas no Período.
Campo 05 - Preenchimento: Informar neste campo a parcela da base de cálculo informada no Campo 04, vinculada a receitas de natureza cumulativa.
Este campo deve ser preenchido pela pessoa jurídica que se submeta, no período da escrituração, concomitantemente aos regimes não-cumulativo e cumulativo, ou seja, que no Registro “0110” tenha informado no Campo 02 (COD_INC_TRIB) o indicador “3”. No caso da pessoa jurídica adotar o método do Rateio Proporcional da Receita Bruta (Registro “0110”), determinar a parcela cumulativa com base na proporção da receita bruta (Receita Bruta Cumulativa / Receita Bruta Total), conforme valores informados no Registro “0111”.
Para a pessoa jurídica que apura a contribuição exclusivamente no regime não-cumulativo, deve informar no Campo 05 o valor “0,00”, ou deixá-lo em branco.
Campo 06 - Preenchimento: Deve ser informado o Valor Total da Base de Cálculo do Crédito, vinculada a receitas com incidência não-cumulativa (Campo 04 – Campo 05). No caso de contribuinte submetido exclusivamente ao regime não-cumulativo, o valor corresponde ao valor informado no campo 04.
Campo 07 - Preenchimento: Será informado neste campo o valor da base de cálculo específica do tipo de crédito escriturado em M100, conforme o CST informado, com base na seguinte regra:
a) Para os CST_PIS = “50”, “51”, “52”, “60”, “61” e “62”, representativos de operações de créditos vinculados a um único tipo de receita: Informar no Campo 07 o valor do Campo 06 (VL_BC_PIS_NC);
b) Para os CST_PIS = “53”, “54”, “55”, “56”, “63”, “64” “65” e “66” (Crédito sobre operações vinculadas a mais de um tipo de receita): Informar a parcela do valor do Campo 06 (VL_BC_PIS_NC) vinculada especificamente ao tipo de crédito escriturado em M100.
Regras de Apuração das Bases de Cálculo para os CST = 53, 54, 55, 56, 63, 64, 65 e 66:
1. Caso a pessoa jurídica determine o crédito, sobre operações comuns a mais de um tipo de receita, pelo método da Apropriação Direta (conforme indicado no Registro “0110”), informar neste campo 07 o valor da base de cálculo do crédito correspondente, a que se refere o Registro PAI M100;
2. Caso a pessoa jurídica determine o crédito, sobre operações comuns a mais de um tipo de receita, pelo método do Rateio Proporcional da Receita Bruta (conforme indicado no Registro “0110”), informar neste campo 07 o valor da base de cálculo do crédito a que se refere o Registro PAI M100, conforme abaixo, considerando as Receitas Brutas informadas no Registro “0111”:
2.1) No caso de CST 53 e 63 (crédito vinculado a Receitas Tributadas e a Receitas Não Tributadas no Mercado Interno):
- M100 Correspondente a Crédito vinculado à Receita Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada);
- M100 Correspondente a Crédito vinculado à Receita Não Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Não Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada).
2.2) No caso de CST 54 e 64 (crédito vinculado a Receitas Tributadas no Mercado Interno e a Receitas de Exportação):
- M100 Correspondente a Crédito vinculado à Receita Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Tributada / (Receita Bruta Tributada + Receita de Exportação);
- M100 Correspondente a Crédito vinculado à Receita de Exportação: Campo 07 = Valor do Campo 06 x Receita Bruta de Exportação / (Receita Bruta Tributada + Receita Bruta de Exportação).
2.3) No caso de CST 55 e 65 (crédito vinculado a Receitas Não Tributadas e a Receitas de Exportação):
- M100 Correspondente a Crédito vinculado à Receita Não Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Não Tributada / (Receita Bruta Não Tributada + Receita Bruta de Exportação);
- M100 Correspondente a Crédito vinculado à Receita de Exportação: Campo 07 = Valor do Campo 06 x Receita Bruta de Exportação / (Receita Bruta Não Tributada + Receita Bruta de Exportação).
2.4) No caso de CST 56 e 66 (crédito vinculado a Receitas Tributadas, Receitas Não Tributadas no Mercado Interno e de Exportação):
- M100 Correspondente a Crédito vinculado à Receita Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada + Receita Bruta de Exportação);
- M100 Correspondente a Crédito vinculado à Receita Não Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Não Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada + Receita Bruta de Exportação).
- M100 Correspondente a Crédito vinculado à Receita de Exportação: Campo 07 = Valor do Campo 06 x Receita Bruta de Exportação / (Receita Bruta Tributada + Receita Bruta Não Tributada + Receita Bruta de Exportação).
Exemplo:
Considerando que a pessoa jurídica tenha escriturado em registros do Bloco C (C170 ou C191) insumos para industrialização (CFOP 1101) com direito a crédito, vinculados a receitas tributadas, não tributadas e da exportação (CST 56), nos valores de R$ R$ 350.800,00 (insumo A), R$ 210.000,00 (insumo B) e R$ 439.200,00 (insumo C);
Considerando que a pessoa jurídica tenha optado pelo método do Rateio Proporcional com base na Receita Bruta para a determinação do crédito (Registro 0110, Campo 03, indicador “2”) e informado os valores abaixo de Receita Bruta no Registro 0111:

| Valor da Receita Bruta | Natureza da Receita Bruta | Percentual |
| --- | --- | --- |
| 1.250.000,00 | Não Cumulativa – Tributada no MI | 50% |
| 500.000,00 | Não Cumulativa – Não Tributada no MI | 20% |
| 250.000,00 | Não Cumulativa – Exportação | 10% |
| 500.000,00 | Cumulativa | 20% |
| 2.500.000,00 | T O T A L | 100% |

Os valores a serem escriturados nos registros filhos M105, vinculados a cada código de crédito (COD_CRED)  relacionados nos registros pais M100, com base nas informações escrituradas nos Blocos “0” e “C”, corresponderão:
I – Registro M105 (registro filho de M100, com Campo “COD_CRED” = 101)

| Campo 01 REG | Campo 02 NAT_BC _CRED | Campo 03 CST PIS | Campo 04 VL_BC_ PIS_TOT | Campo 05 VL_BC_ PIS_CUM | Campo 06 VL_BC_ PIS_NC | Campo 07 VL_BC_PIS |
| --- | --- | --- | --- | --- | --- | --- |
| M105 | 02 | 56 | 1.000.000,00 | 200.000,00 | 800.000,00 | 500.000,00 |

Representação Gráfica dos registros M105 (base de cálculo do crédito) e M100 (crédito apurado – COD_CRED 101):
|M100|101|0|500000|1,65|0||8250|0|0|0|8250|0|8250|8250|
|M105|02|56|1000000|200000|800000|500000||0||
II – Registro M105 (registro filho de M100, com Campo “COD_CRED” = 201)

| Campo 01 REG | Campo 02 NAT_BC _CRED | Campo 03 CST PIS | Campo 04 VL_BC_ PIS_TOT | Campo 05 VL_BC_ PIS_CUM | Campo 06 VL_BC_ PIS_NC | Campo 07 VL_BC_PIS |
| --- | --- | --- | --- | --- | --- | --- |
| M105 | 02 | 56 | 1.000.000,00 | 200.000,00 | 800.000,00 | 200.000,00 |

Representação Gráfica dos registros M105 (base de cálculo do crédito) e M100 (crédito apurado – COD_CRED 201):
|M100|201|0|200000|1,65|0||3300|0|0|0|3300|1|0|3300|
|M105|02|56|1000000|200000|800000|200000||0||
III – Registro M105 (registro filho de M100, com Campo “COD_CRED” = 301)

| Campo 01 REG | Campo 02 NAT_BC _CRED | Campo 03 CST PIS | Campo 04 VL_BC_ PIS_TOT | Campo 05 VL_BC_ PIS_CUM | Campo 06 VL_BC_ PIS_NC | Campo 07 VL_BC_PIS |
| --- | --- | --- | --- | --- | --- | --- |
| M105 | 02 | 56 | 1.000.000,00 | 200.000,00 | 800.000,00 | 100.000,00 |

Representação Gráfica dos registros M105 (base de cálculo do crédito) e M100 (crédito apurado – COD_CRED 301):
|M100|301|0|100000|1,65|0||1650|0|0|0|1650|1|0|1650|
|M105|02|56|1000000|200000|800000|100000||0||
Campos 08 e 09 - Preenchimento: Campos específicos para as pessoas jurídicas que apuram crédito por Unidade de Medida de Produto (fabricantes/importadores de Combustíveis, Bebidas Frias ou Embalagens para Bebidas).
O crédito será determinado em quantidade quando o tipo de crédito do registro M100 corresponder a 103, 203 ou 303. O preenchimento destes campos também poderá ocorrer nos tipos de crédito 105, 205, 305 e 108, 208 e 308.
No caso de operações geradoras de créditos vinculados a mais de um tipo de receita (CST 53 a 56 e 63 a 66) deve a pessoa jurídica preencher 2 registros M105 (no caso de CST 53, 54, 55, 63, 64 e 65) ou 3 registros M105 (no caso de CST 56 e 66), um para cada tipo de receita a qual o crédito está vinculado.
Campo 10 - Preenchimento: Neste campo poderá a pessoa jurídica proceder à descrição do crédito, para fins de detalhamento ou esclarecimento da natureza da base de cálculo do crédito escriturado.
Validação: Quando o Campo NAT_BC_CRED = 13, este campo é de preenchimento obrigatório.
<!-- End Registro M105 -->
<!-- Start Registro M110 -->
Registro M110: Ajustes do Crédito de PIS/Pasep Apurado
Registro a ser preenchido caso a pessoa jurídica tenha de proceder a ajustes de créditos escriturados no período, decorrentes de ação judicial, de processo de consulta, da legislação tributária das contribuições sociais, de estorno ou de outras situações.
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas nos campos 09 e 10 do registro pai M100.
Deve ser informado neste registro, como ajuste de redução (Indicador “0”) o valor referente às devoluções de compras ocorridas no período, de bens e mercadorias sujeitas à incidência não cumulativa da Contribuição que, quando da aquisição gerou a apuração de créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M110" | C | 004* | - | S |
| 02 | IND_AJ | Indicador do tipo de ajuste: 0- Ajuste de redução; 1- Ajuste de acréscimo. | C | 001* | - | S |
| 03 | VL_AJ | Valor do ajuste | N | - | 02 | S |
| 04 | COD_AJ | Código do ajuste, conforme a Tabela indicada no item 4.3.8. | C | 002* |   | S |
| 05 | NUM_DOC | Número do processo, documento ou ato concessório ao qual o ajuste está vinculado, se houver. | C | - | - | N |
| 06 | DESCR_AJ | Descrição resumida do ajuste. | C | - | - | N |
| 07 | DT_REF | Data de referência do ajuste (ddmmaaaa) | N | 008* | - | N |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [M110]
Campo 02 - Valores válidos: [0, 1]
Campo 03 - Preenchimento: informar o valor do ajuste de redução ou de acréscimo. A soma de todos os valores deste campo, representando ajustes de acréscimo (IND_AJ = 1) deverá ser transportada para o campo 09 (VL_AJUS_ACRES) do registro M100. Por sua vez, a soma de todos os valores deste campo, representando ajustes de redução (IND_AJ = 0) deverá ser transportada para o campo 10 (VL_AJUS_REDUC) do registro M100.
Campo 04 - Preenchimento: informar o código do ajuste, conforme Tabela 4.3.8 - “Tabela Código de Ajustes de Contribuição ou Créditos”, referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informar, se for o caso, o número do processo, documento ou ato concessório ao qual o ajuste está vinculado.
No caso de ajuste que envolva grande quantidade de documentos, pode o registro ser escriturado consolidando as informações dos documentos, descrevendo no campo 06 (tipo de documento fiscal consolidado, quantidades de documentos, emitente/beneficiário, por exemplo).
Campo 06 - Preenchimento: informar a descrição resumida do ajuste que está sendo lançada no respectivo registro.
Campo 07 - Preenchimento: informar, se for o caso, a data de referência do ajuste, no formato "ddmmaaaa", excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
<!-- End Registro M110 -->
<!-- Start Registro M115 -->
Registro M115: Detalhamento dos Ajustes do Crédito de PIS/Pasep Apurado
Registro a ser preenchido para a pessoa jurídica detalhar a operação e valor a que se refere o ajuste de crédito informado no registro pai – M110.
Registro não disponível para os fatos geradores até 30/09/2015. Para os fatos geradores a partir de 01/10/2015 a versão 2.12 do Programa da EFD-Contribuições (PVA) disponibiliza este registro de detalhamento dos ajustes de crédito, o qual deve ser preenchido, para que seja demonstrado e detalhado à Receita Federal quais as operações realizadas que ensejaram os ajustes informados no registro M110.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M115” | C | 004* | - | S |
| 02 | DET_VALOR_AJ | Detalhamento do valor do crédito reduzido ou acrescido, informado no Campo 03 (VL_AJ) do registro M110. | N | - | 02 | S |
| 03 | CST_PIS | Código de Situação Tributária referente à operação detalhada neste registro. | N | 002* | - | N |
| 04 | DET_BC_CRED | Detalhamento da base de cálculo geradora de ajuste de crédito | N | - | 03 | N |
| 05 | DET_ALIQ | Detalhamento da alíquota a que se refere o ajuste de crédito | N | 08 | 04 | N |
| 06 | DT_OPER_AJ | Data da operação a que se refere o ajuste informado neste registro. | N | 008* | - | S |
| 07 | DESC_AJ | Descrição da(s) operação(ões) a que se refere o valor informado no Campo 02 (DET_VALOR_AJ) | C | - | - | N |
| 08 | COD_CTA | Código da conta contábil debitada/creditada | C | 255 | - | N |
| 09 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
Nível hierárquico – 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [M115]
Campo 02 - Preenchimento: Informar o detalhamento do valor da operação a que se refere o ajuste de crédito informado no Campo 03 (VL_AJ) do registro M110.
Caso o ajuste em M110 se refira a várias operações ou situações, devem ser gerados os registros de detalhamento M115 que se mostrem necessários e suficientes, para demonstrar o valor total do ajuste escriturado em M110.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao ajuste de crédito de PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 04 - Preenchimento: Informar a base de cálculo do ajuste de crédito a que se refere este registro.
Campo 05 - Preenchimento: Informar a alíquota a que se refere o ajuste de crédito informado neste registro.
Campo 06 - Preenchimento: Informar a data da operação a que se refere o ajuste de crédito detalhado neste registro.
Campo 07 - Preenchimento: Informar a descrição da(s) operação(ões) a que se refere o ajuste detalhado neste registro.
Campo 08 - Preenchimento: Informar, sendo o caso, o código da conta contábil a que se refere o ajuste detalhado neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 09 - Preenchimento: Campo para prestação de outras informações que se mostrem necessárias ou adequadas, para esclarecer ou justificar o ajuste.
<!-- End Registro M115 -->
<!-- Start Registro M200 -->
Registro M200: Consolidação da Contribuição para o PIS/Pasep do Período
Neste registro serão consolidadas as contribuições sociais apuradas no período da escrituração, nos regimes não-cumulativo e cumulativo, bem como procedido ao desconto dos créditos não cumulativos apurados no próprio período, dos créditos apurados em períodos anteriores, dos valores retidos na fonte e de outras deduções previstas em Lei, demonstrando em seu final os valores devidos a recolher.
ATENÇÃO: Os valores referentes às contribuições sociais escriturados nos Campos 02 e 09 do Registro M200 serão gerados com base:
Nos valores informados no arquivo elaborado pela própria pessoa jurídica e importado pelo Programa Validador e Assinador da EFD-Contribuições – PVA, os quais serão objeto de validação; ou
Nos valores das contribuições calculados pelo PVA no Registro M210 (Detalhamento da Contribuição para o PIS/Pasep no Período), no Campo 13 (VL_CONT_PER), através da funcionalidade “Gerar Apurações”, disponibilizada no PVA, com base nos registros de escrituração de receitas constantes nos Blocos “A”, “C”, “D” e “F”.
A geração automática de apuração (funcionalidade “Gerar Apurações” (Ctrl+M)) o PVA apura, em relação ao Registro M200, apenas os valores dos campos de contribuições (Campos 02 e 09) e de créditos a descontar (Campos 03 e 04). Os campos representativos de retenções na fonte (Campos 06 e 10) e de outras deduções (07 e 11) não são recuperados na geração automática de apuração, devendo sempre ser informados pela própria pessoa jurídica no arquivo importado pelo PVA ou complementado pela edição (digitação no próprio PVA) do registro M200, dos respectivos valores de retenção na fonte escriturados nos registros F600, 1300 (PIS) ou 1700 (Cofins), e de deduções, escriturados no registro F700.
Na funcionalidade de geração automática de apuração, os valores apurados e preenchidos pelo PVA para os Campos 02 e 09 (contribuições apuradas) e para os Campos 03 e 04 (créditos descontados) irão sobrepor (substituir) os valores eventualmente existentes nos referidos campos, constantes na escrituração.
No caso de totalização de contribuição não cumulativa do período no campo 02, mas que a legislação não permita o desconto de créditos, aproveitamento de retenções na fonte e de outras deduções, deverá a pessoa jurídica realizar os devidos ajustes nos registros de apuração de crédito (campo 14 do registro M100 ou campo 13 do registro 1100) e dos respectivos aproveitamentos neste registro (campos 03, 04, 06 e 07).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M200" | C | 004* | - | S |
| 02 | VL_TOT_CONT_NC_PER | Valor Total da Contribuição Não Cumulativa do Período (recuperado do campo 13 do Registro M210, quando o campo “COD_CONT” = 01, 02, 03, 04, 32 e 71) | N | - | 02 | S |
| 03 | VL_TOT_CRED_DESC | Valor do Crédito Descontado, Apurado no Próprio Período da Escrituração (recuperado do campo 14 do Registro M100) | N | - | 02 | S |
| 04 | VL_TOT_CRED_DESC_ANT | Valor do Crédito Descontado, Apurado em Período de Apuração Anterior (recuperado do campo 13 do Registro 1100) | N | - | 02 | S |
| 05 | VL_TOT_CONT_NC_DEV | Valor Total da Contribuição Não Cumulativa Devida (02 – 03 - 04) | N | - | 02 | S |
| 06 | VL_RET_NC | Valor Retido na Fonte Deduzido no Período | N | - | 02 | S |
| 07 | VL_OUT_DED_NC | Outras Deduções no Período | N | - | 02 | S |
| 08 | VL_CONT_NC_REC | Valor da Contribuição Não Cumulativa a Recolher/Pagar (05 – 06 - 07) | N | - | 02 | S |
| 09 | VL_TOT_CONT_CUM_PER | Valor Total da Contribuição Cumulativa do Período  (recuperado do campo 13 do Registro M210, quando o campo “COD_CONT” = 31, 32, 51, 52, 53, 54 e 72) | N | - | 02 | S |
| 10 | VL_RET_CUM | Valor Retido na Fonte Deduzido no Período | N | - | 02 | S |
| 11 | VL_OUT_DED_CUM | Outras Deduções no Período | N | - | 02 | S |
| 12 | VL_CONT_CUM_REC | Valor da Contribuição Cumulativa a Recolher/Pagar (09 - 10 – 11) | N | - | 02 | S |
| 13 | VL_TOT_CONT_REC | Valor Total da Contribuição a Recolher/Pagar no Período (08 + 12) | N | - | 02 | S |

Observações:
1. Os valores referentes às contribuições sociais não-cumulativas, informados no campo 02  “VL_TOT_CONT_NC_PER”, serão determinados e recuperados do Campo 13  “VL_CONT_PER” dos Registros Filho “M210”.
2. Os valores referentes aos créditos a descontar informados no campo 03  “VL_TOT_CRED_DESC”, serão determinados e recuperados do Campo 14 “VL_CRED_DESC” dos Registros Filho “M100”.
3. Os valores referentes às contribuições sociais cumulativas, informados no campo 09  “VL_TOT_CONT_CUM_PER”, serão determinados e recuperados do Campo 13  “VL_CONT_PER” dos Registros Filho “M210”.
4. Os valores retidos na fonte no período da escrituração, relacionados nos Campos 06 e 10, devem guardar correlação com os valores informados no Campo 09 “VL_RET_PIS” do Registro “F600”.
Nível hierárquico – 2
Ocorrência – Um (por arquivo)
Campo 01 - Valor Válido: [M200]
Campo 02 - Preenchimento: informar o valor total da contribuição não cumulativa do período, correspondendo à soma do campo 13 (VL_CONT_PER) do registro M210, quando o valor do campo “COD_CONT” for igual a 01, 02, 03, 04, 32 (neste caso quando a pessoa jurídica estiver sujeita a não cumulatividade, exclusivamente ou não) ou 71.  No caso da pessoa jurídica sujeitar-se exclusivamente ao regime cumulativo da contribuição, o valor do campo deverá ser igual a 0.
Campo 03 - Preenchimento: informar o valor do crédito descontado, apurado no próprio período da escrituração, correspondendo ao somatório do campo 14 (VL_CRED_DESC) dos diversos registros M100. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Validação: O somatório dos campos VL_TOT_CRED_DESC e VL_TOT_CRED_DESC_ANT deve ser menor ou igual ao valor do campo VL_TOT_CONT_NC_PER.
Campo 04 - Preenchimento: informar o valor do crédito descontado, apurado em período de apuração anterior, correspondendo ao somatório do campo 13 (VL_CRED_DESC_EFD), dos diversos registros 1100. Na geração automática da apuração pela PVA, este campo será preenchido automaticamente com o somatório do campo 13 dos registros 1100. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Validação: O somatório dos campos VL_TOT_CRED_DESC e VL_TOT_CRED_DESC_ANT deve ser menor ou igual ao valor do campo VL_TOT_CONT_NC_PER.
OBS: Tendo a pessoa jurídica apurado em um determinado mês um débito de R$ 500,00 e um crédito de R$ 400,00, não querendo utilizar como desconto os próprios R$ 400,00 apurados no período mas sim, R$ 400,00 de créditos de períodos anteriores, deve assim proceder na EFD-Contribuições:
Registro M100:
Campo 08 ==> 400,00
Campo 12 ==> 400,00
Campo 13 ==> "1"
Campo 14 ==> 100,00
Campo 15 ==> 300,00
Registro M200:
Campo 02 ==> 500,00
Campo 03 ==> 100,00
Campo 04 ==> 400,00
Campo 05 ==> 0
Registro 1100:
Campo 02 ==> xx/yyyy (período anterior ao da escrituração)
Campo 06 ==> 2.000,00
Campo 08 ==> 2.000,00
Campo 13 ==> 400,00
Campo 18 ==> 1.600,00
Campo 05 - Preenchimento: informar o valor total da contribuição não cumulativa devida, correspondendo a VL_TOT_CONT_NC_PER - VL_TOT_CRED_DESC - VL_TOT_CRED_DESC_ANT.
Campo 06 - Preenchimento: informar o valor na fonte deduzido do valor da contribuição não cumulativa devida no período. Caso a retenção na fonte tenha ocorrido no próprio período da escrituração, ela deverá estar detalhada no registro F600 e também no registro 1300, caso exista valor a utilizar em períodos futuros. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
O valor a ser informado no Campo 06 deve ser igual ou menor que o valor constante no campo 05.
Campo 07 - Preenchimento: informar o valor de outras deduções do valor da contribuição não cumulativa devida no período, correspondendo ao somatório do campo VL_DED_PIS dos registros F700 quando IND_NAT_DED = 0 (dedução de natureza não cumulativa). No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 08 - Preenchimento: informar o valor da contribuição não cumulativa a recolher/pagar no período da escrituração, correspondendo a VL_TOT_CONT_NC_DEV - VL_RET_NC - VL_OUT_DED_NC. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 09 - Preenchimento: informar o valor total da contribuição cumulativa do período, correspondendo à soma do campo 13 (VL_CONT_PER) do registro M210, quando o valor do campo “COD_CONT” for igual a 31, 32 (neste caso quando a pessoa jurídica estiver sujeita exclusivamente ao regime cumulativo),  51, 52, 53, 54 ou 72.  No caso da pessoa jurídica estar sujeita exclusivamente ao regime não cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 10 - Preenchimento: informar o valor na fonte deduzido do valor da contribuição cumulativa devida no período. Caso a retenção na fonte tenha ocorrido no próprio período da escrituração, ela deverá estar detalhada no registro F600 e também no registro 1300, caso exista valor a utilizar em períodos futuros. No caso da pessoa jurídica estar sujeita exclusivamente ao regime não cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
O valor a ser informado no Campo 10 deve ser igual ou menor que o valor constante no campo 09.
Campo 11 - Preenchimento: informar o valor de outras deduções do valor da contribuição cumulativa devida no período, correspondendo, no máximo, ao somatório do campo VL_DED_PIS dos registros F700 quando IND_NAT_DED = 1 (dedução de natureza cumulativa). No caso da pessoa jurídica estar sujeita exclusivamente ao regime não cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 12 - Preenchimento: informar o valor da contribuição cumulativa a recolher/pagar no período da escrituração, correspondendo a VL_TOT_CONT_CUM_PER - VL_RET_CUM - VL_OUT_DED_CUM.
Campo 13 - Preenchimento: informar o valor total da contribuição a recolher/pagar no período da escrituração, correspondendo a "VL_CONT_NC_REC" + "VL_CONT_CUM_REC".
<!-- End Registro M200 -->
<!-- Start Registro M205 -->
Registro M205: Contribuição para o PIS/Pasep a Recolher–Detalhamento por Código de Receita
Neste registro será informado, por código de receita (conforme códigos de débitos informados em DCTF), o detalhamento da contribuição a recolher informada nos campos 08 (regime não cumulativo) e 12 (regime cumulativo) do Registro Pai M200.
Atenção:
1. O código a ser informado no campo 03 (COD_REC) não é o código que consta no DARF (composto de quatro números), mas sim, o código identificador da contribuíção na Ficha “Débitos” da DCTF (composto de seis números).
2. O somatório dos valores informados no campo 04 (VL_DEBITO) informado neste registro, deve corresponder ao valor constante de contribuição a recolher, do Registro Pai M200.
Referido registro deverá ser preenchido a partir do período de apuração de janeiro de 2014, utilizando a versão 2.06 do Programa da EFD-Contribuições (PVA). De preenchimento opcional no período de janeiro a março de 2014, e de preenchimento obrigatório a partir do período de apuração abril de 2014.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M205" | C | 004* | - | S |
| 02 | NUM_CAMPO | Informar o número do campo do registro “M200” (Campo 08 (contribuição não cumulativa) ou Campo 12 (contribuição cumulativa)), objeto de detalhamento neste registro. | C | 002* | - | S |
| 03 | COD_REC | Informar o código da receita referente à contribuição a recolher, detalhada neste registro. | C | 006* | - | S |
| 04 | VL_DEBITO | Valor do Débito correspondente ao código do Campo 03, conforme informação na DCTF. | N | - | 02 | S |

Observações: Registro de preenchimento obrigatório a partir do período de apuração referente a abril de 2014.
Nível hierárquico – 3
Ocorrência – Vários por arquivo.
Campo 01 - Valor Válido: [M205]
Campo 02 - Preenchimento: Informar o número do campo do registro “M200” (Campo 08 (contribuição não cumulativa) ou Campo 12 (contribuição cumulativa)), objeto de detalhamento neste registro.
Campo 03 - Preenchimento: informar o código de débito referente ao PIS/Pasep, conforme os códigos de receitas informados na Ficha “Débitos” da DCTF, composto de 06 (seis) números, conforme referenciado no Ato Declaratório Executivo Codac/RFB nº 36, de 2014.

| Ato Declaratório Executivo Codac nº 36, de 22 de outubro de 2014 O COORDENADOR-GERAL DE ARRECADAÇÃO E COBRANÇA, no uso das atribuições que lhe confere o inciso III do art. 312 do Regimento Interno da Secretaria da Receita Federal do Brasil, aprovado pela Portaria MF nº 203, de 14 de maio de 2012, e tendo em vista o disposto na Instrução Normativa RFB nº 1.110, de 24 de dezembro de 2010, declara: Art. 1ºAs extensões dos códigos de receita a serem utilizadas na Declaração de Débitos e Créditos Tributários Federais (DCTF) serão divulgadas no sítio da Secretaria da Receita Federal do Brasil (RFB) na Internet, no endereço http://www.receita.fazenda.gov.br .  Parágrafo único. As extensões divulgadas na forma do caput e não relacionadas na tabela do programa gerador da DCTF deverão ser incluídas na referida tabela mediante a utilização da opção “Manutenção da Tabela de Códigos” do menu “Ferramentas” nos grupos respectivos. Art. 2º Este Ato Declaratório Executivo entra em vigor na data de sua publicação no Diário Oficial da União.  Art. 3º Fica revogado o Ato Declaratório Executivo Codac nº 99, de 29 de dezembro de 2011 JOÃO PAULO R. F. MARTINS DA SILVA |
| --- |

Campo 04 - Preenchimento: informar o valor do débito correspondente ao código de receita constante no Campo 03.
<!-- End Registro M205 -->
<!-- Start Registro M210 -->
Registro M210: Detalhamento da Contribuição para o PIS/Pasep do Período
Será gerado um Registro “M210” para cada situação geradora contribuição social, especificada na Tabela “4.3.5 – Código de Contribuição Social Apurada”, recuperando os valores referentes às diversas bases de cálculo escriturados nos registros dos Blocos “A”, “C”, “D” e “F”.
Caso sejam recuperados registros dos Blocos “A”, “C”, “D” ou “F” referentes a uma mesma situação com incidência de contribuição social (conforme Tabela 4.3.5), mas sujeitas a mais de uma alíquota de apuração, deve ser escriturado um Registro “M210” em relação a cada alíquota existente na escrituração. Dessa forma a chave do registro é formada pelos campos COD_CONT + ALIQ_PIS_QUANT + ALIQ_PIS.
Conforme item “4. Procedimentos de escrituração na revenda de bens sujeitos à substituição tributária de PIS/COFINS”, até a versão 2.0.4a e anteriores do PGE, documentos escriturados com CST 05 e alíquota zero eram totalizados nos registros M400 e M800. A partir da versão 2.0.5 do PGE, todas as operações com CST 05 devem ser totalizadas nos registros M210 e M610.
Para os períodos de apuração até dezembro de 2013, no caso de apuração da contribuição para o PIS/Pasep (cumulativa ou não cumulativa) incidente sobre receitas específicas de sociedade em conta de participação (SCP), da qual a pessoa jurídica titular da escrituração seja sócia ostensiva,  deve ser escriturada em registro M210 específico e separado da contribuição incidente sobre as demais receitas, informando no Campo 02 o código de tipo de contribuição “71” ou “72”, conforme o regime de tributação a que está submetida a SCP.
A funcionalidade de apuração automática de contribuição e crédito pelo próprio PVA da EFD-Contribuições (opção “Gerar Apurações” (Ctrl+M), do PVA), não apura contribuições específica de SCP, face a impossibilidade de sua identificação em cada documento/operação escriturados nos Blocos A, C, D ou F. Assim, a demonstração da contribuição vinculada a SCP, em M210, deverá sempre ser efetuada pela própria pessoa jurídica, conforme procedimentos abaixo:
Procedimento 1 – Destaque dos valores referentes à(s) SCP:
Primeiramente, deve ser reduzido dos valores totais de débitos (M210) e créditos (M100) apurados de forma consolidada na empresa, sócia ostensiva, os valores referentes a cada SCP. Para tanto, informar o valor do crédito (em M100, campo 10 e gerando um registro de ajuste de redução em M110 para cada SCP) e o valor do débito (em M210, campo 10 e gerando um registro de ajuste de redução em M220 para cada SCP), segregando assim os valores referentes à sócia ostensiva, dos valores referentes à(s) SCP.
Procedimento 2 – Registros dos valores referentes à(s) SCP:
Em seguida, gerar novos registros M210 (Contribuições) para a demonstração dos créditos e débitos apurados no período, de cada SCP da qual seja sócia ostensiva, com os códigos específicos de contribuição de SCP (71 ou 72), gerando também os correspondentes registros de ajuste de acréscimo de contribuições, em M220.
Para identificação das SCPs poderão ser utilizados os registros de conta contábil informados em 0500.
Para os períodos de apuração a partir de janeiro de 2014, no caso de apuração da contribuição para o PIS/Pasep (cumulativa ou não cumulativa) incidente sobre receitas específicas de sociedade em conta de participação (SCP), da qual a pessoa jurídica titular da escrituração seja sócia ostensiva, deve ser escriturada uma EFD-Contribuições para cada SCP, sendo cada SCP identificada na EFD-Contribuições da pessoa jurídica sócia ostensiva no Registro "0035 - Identificação das SCP".
Leiaute do Registro M210 aplicável aos Fatos Geradores ocorridos até 31 de dezembro de 2018:

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M210" | C | 004* | - | S |
| 02 | COD_CONT | Código da contribuição social apurada no período, conforme a Tabela 4.3.5. | C | 002* | - | S |
| 03 | VL_REC_BRT | Valor da Receita Bruta | N | - | 02 | S |
| 04 | VL_BC_CONT | Valor da Base de Cálculo da Contribuição | N | - | 02 | S |
| 05 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 06 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS | N | - | 03 | N |
| 07 | ALIQ_PIS_QUANT | Alíquota do PIS (em reais) | N | - | 04 | N |
| 08 | VL_CONT_APUR | Valor total da contribuição social apurada | N | - | 02 | S |
| 09 | VL_AJUS_ACRES | Valor total dos ajustes de acréscimo | N | - | 02 | S |
| 10 | VL_AJUS_REDUC | Valor total dos ajustes de redução | N | - | 02 | S |
| 11 | VL_CONT_DIFER | Valor da contribuição a diferir no período | N | - | 02 | N |
| 12 | VL_CONT_DIFER_ANT | Valor da contribuição diferida em períodos anteriores | N | - | 02 | N |
| 13 | VL_CONT_PER | Valor Total da Contribuição do Período (08 + 09 – 10 – 11+12) | N | - | 02 | S |

Observações:
1. Os valores representativos de Bases de Cálculo da contribuição, demonstrados no Campo 04 “VL_BC_CONT” (base de cálculo referente a receitas auferidas) do Registro “M210”, são recuperados do Campo “VL_BC_PIS” dos diversos registros dos Blocos “A”, “C”, “D” ou “F” que contenham o mesmo CST.
2. Os valores representativos de Bases de Cálculo da contribuição em quantidade, demonstrados no Campo 06 “QUANT_BC_PIS” (base de cálculo referente a quantidades vendidas) do Registro “M210”, são recuperados do Campo “QUANT_BC_PIS” dos registros do Bloco “C” que contenham o mesmo CST.
3. Deve existir ao menos um registro M210 de apuração de contribuição a alíquotas específicas (diferenciadas ou por unidade de medida de produto), com o Campo “COD_CONT” igual a 02 ou 03 (regime não-cumulativo) ou 52 ou 53 (regime cumulativo) se o Campo “COD_TIPO_CONT” do Registro 0110 for igual a 2.
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [M210]
Campo 02 - Preenchimento: informe o código da contribuição social que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>. Quando a apuração é gerada automaticamente pelo PVA, o campo é obtido através das seguintes combinações:

| Campo COD_CONT do Registro M210 | Descrição do COD_CONT | CST_PIS | Campo COD_INC_TRIB do Registro 0110 | Alíquota do PIS (em percentual) (ALIQ_PIS) | Alíquota do PIS (em reais) (ALIQ_PIS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 1 | 1,65(PIS) | - |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 3 | 1,65(PIS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 2 | 0,65(PIS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 3 | 0,65(PIS) | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 1 | - | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 3 | - | - |
| 52 | Contribuição cumulativa apurada a alíquotas diferenciadas | 02 | 2 | - | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 1 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 1 | > 0 | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 3 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 3 | > 0 | - |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03 | 2 | - | > 0 |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03* | 2 | > 0 | - |
| 31 | Contribuição apurada por substituição tributária | 05 | - | 0,65(PIS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | Diferente de 0, 0,65(PIS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | - | >0 |

Tabela para apuração dos registros M210 – F200 (Item exclusivo para informações obtidas dos registros F200)

| Campo COD_CONT do Registro M210 | Descrição do COD_CONT | CST_PIS | Campo COD_INC_TRIB do Registro 0110 | Alíquota do PIS (em percentual) (ALIQ_PIS) | Alíquota do PIS (em reais) (ALIQ_PIS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 1 | 1,65 | - |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 1,65 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 2 | 0,65 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 0,65 | - |

O PVA não validará e não gerará automaticamente registros M210 com COD_CONT igual a 71 (Contribuição apurada de SCP – Incidência Não Cumulativa), 72 (Contribuição apurada de SCP – Incidência Cumulativa) e 99 (Contribuição para o PIS/Pasep – Folha de Salários – Vide registro M350).
Campo 03 - Preenchimento: informar o valor da receita bruta auferida no período, vinculada ao respectivo COD_CONT.
Validação: Quando o valor do campo 02 (COD_CONT) for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual à soma dos seguintes campos (quando o CST da operação vinculada for 01, 02, 03, 04, 05 com alíquota diferente de zero e 49):
VL_ITEM dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_ITEM dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_ITEM dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_ITEM dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_ITEM dos registros C381, C601, C870, C880, D201, D601
VL_DOC dos registros D300,
VL_BRT do registro D350,
VL_OPR do registro C175,
VL_OPER do registro F100, cujo valor do campo IND_OPER seja igual a “1” ou “2”,
VL_TOT_REC do registro F200,
VL_REC_CAIXA do registro F500 e F510,
VL_REC_COMP do registro F550 e F560,
VL_REC do registro I100.
Campo 04 - Preenchimento: informar o valor da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro.
Validação: Quando a natureza da pessoa jurídica (IND_NAT_PJ do registro “0000” igual a 00, 02, 03 ou 05) não for sociedade cooperativa e o valor do campo COD_CONT for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual a:
VL_BC_PIS dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_BC_PIS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_BC_PIS dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_BC_PIS dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_BC_PIS dos registros C175, C381, C601, C870, D201, D300, D350, D601, F200, F500, F550,
VL_BC_PIS do registro F100, quando o valor do campo ALIQ_PIS não conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”,
VL_BC_PIS dos registros I100
Quando o COD_CONT for igual a 03 ou 53, o valor deste campo será igual a zero.
Caso contrário (sociedade cooperativa), o valor deste campo será igual ao valor do campo VL_BC_CONT do registro M211.
Campo 05 - Preenchimento: informar a alíquota do PIS/PASEP (em percentual) aplicável. Quando o COD_CONT for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 06 - Preenchimento: informar a quantidade da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro.
Validação: Quando o valor do campo COD_CONT for igual a 03, 53 ou 32, o valor do campo será igual a:
QUANT_BC_PIS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
QUANT_BC_PIS dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
QUANT_BC_PIS dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
QUANT_BC_PIS dos registros C381, C880, D350, F510, F560,
VL_BC_PIS do registro F100, quando o valor do campo ALIQ_PIS conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”
Quando valor do campo COD_CONT for igual a 01, 51, 02, 52 ou 31 o campo deverá ser deixado em branco.
Campo 07 - Preenchimento: informar a alíquota do PIS (em reais) aplicável. Quando o COD_CONT não for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 08 - Preenchimento: informar o valor total da contribuição social apurada, vinculada ao COD_CONT do registro, correspondendo a QUANT_BC_PIS x ALIQ_PIS_QUANT, quando a contribuição for calculada por unidade de medida de produto ou VL_BC_CONT x ALIQ_PIS/100, caso contrário.
Campo 09 - Preenchimento: informar o valor dos ajustes de acréscimo à contribuição social apurada no campo 08. O preenchimento deste campo obriga o respectivo detalhamento no registro M220, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M220 quando IND_AJ = 1.
Campo 10 - Preenchimento: informar o valor dos ajustes de redução à contribuição social apurada no campo 08. O preenchimento deste campo obriga o respectivo detalhamento no registro M220, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M220 quando IND_AJ = 0.
Campo 11 - Preenchimento: informar o valor da contribuição a diferir no período, referente às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998).
O preenchimento deste campo obriga o preenchimento do registro M230, devendo ser igual ao somatório do campo VL_CONT_DIF dos registros M230.
Campo 12 - Preenchimento: informar o valor da contribuição diferida em períodos anteriores, adicionada a este período de escrituração, referente às receitas diferidas recebidas no mês da escrituração.
O preenchimento deste campo obriga o preenchimento do registro M300, sendo que a soma dos valores deste campo de todos os registros M210 deverá ser igual a soma dos campos VL_CONT_DIFER_ANT dos registros M300, para um mesmo COD_CONT.
Campo 13 - Preenchimento: informar o valor total da contribuição do período da escrituração, para o respectivo COD_CONT, devendo ser igual a VL_CONT_APUR + VL_AJUS_ACRES - VL_AJUS_REDUC – VL_CONT_DIFER + VL_CONT_DIFER_ANT.
Leiaute do Registro M210 aplicável aos Fatos Geradores ocorridos a partir de 01 de janeiro de 2019:
A chave do registro é formada pelos campos: COD_CONT;  ALIQ_PIS_QUANT e ALIQ_PIS

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M210" | C | 004* | - | S |
| 02 | COD_CONT | Código da contribuição social apurada no período, conforme a Tabela 4.3.5. | C | 002* | - | S |
| 03 | VL_REC_BRT | Valor da Receita Bruta | N | - | 02 | S |
| 04 | VL_BC_CONT | Valor da Base de Cálculo da Contribuição, antes de ajustes | N | - | 02 | S |
| 05 | VL_AJUS_ACRES_BC_PIS | Valor do total dos ajustes de acréscimo da base de cálculo da contribuição a que se refere o Campo 04 | N | - | 02 | S |
| 06 | VL_AJUS_REDUC_BC_PIS | Valor do total dos ajustes de redução da base de cálculo da contribuição a que se refere o Campo 04 | N | - | 02 | S |
| 07 | VL_BC_CONT_AJUS | Valor da Base de Cálculo da Contribuição, após os ajustes. (Campo 07 = Campo 04 + Campo 05 - Campo 06) | N | - | 02 | S |
| 08 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 09 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS | N | - | 03 | N |
| 10 | ALIQ_PIS_QUANT | Alíquota do PIS (em reais) | N | - | 04 | N |
| 11 | VL_CONT_APUR | Valor total da contribuição social apurada | N | - | 02 | S |
| 12 | VL_AJUS_ACRES | Valor total dos ajustes de acréscimo da contribuição social apurada | N | - | 02 | S |
| 13 | VL_AJUS_REDUC | Valor total dos ajustes de redução da contribuição social apurada | N | - | 02 | S |
| 14 | VL_CONT_DIFER | Valor da contribuição a diferir no período | N | - | 02 | N |
| 15 | VL_CONT_DIFER_ANT | Valor da contribuição diferida em períodos anteriores | N | - | 02 | N |
| 16 | VL_CONT_PER | Valor Total da Contribuição do Período (11 + 12 – 13 – 14+15) | N | - | 02 | S |

Observações:
1. Os valores representativos de Bases de Cálculo da contribuição, demonstrados no Campo 04 “VL_BC_CONT” (base de cálculo referente a receitas auferidas) do Registro “M210”, são recuperados do Campo “VL_BC_PIS” dos diversos registros dos Blocos “A”, “C”, “D”, “I” ou “F” que contenham o mesmo CST.
2. Os valores representativos de Bases de Cálculo da contribuição em quantidade, demonstrados no Campo 09 “QUANT_BC_PIS” (base de cálculo referente a quantidades vendidas) do Registro “M210”, são recuperados do Campo “QUANT_BC_PIS” dos registros do Bloco “C” que contenham o mesmo CST.
3. Deve existir ao menos um registro M210 de apuração de contribuição a alíquotas específicas (diferenciadas ou por unidade de medida de produto), com o Campo “COD_CONT” igual a 02 ou 03 (regime não-cumulativo) ou 52 ou 53 (regime cumulativo) se o Campo “COD_TIPO_CONT” do Registro 0110 for igual a 2.
4. Considerando que este novo leiaute do Registro M210 só pode ser utilizado na escrituração dos fatos geradores a partir de 01.01.2019, eventuais ajustes referentes aos fatos geradores ocorridos até 31.12.2018 devem ser informados, nas EFD-Contribuições correspondentes a estes períodos anteriores a 2019, originais ou retificadoras, nos campos 09 (VL_AJUS_ACRES) e 10 (VL_AJUS_REDUC).
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [M210]
Campo 02 - Preenchimento: informe o código da contribuição social que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>. Quando a apuração é gerada automaticamente pelo PVA, o campo é obtido através das seguintes combinações:

| Campo COD_CONT do Registro M210 | Descrição do COD_CONT | CST_PIS | Campo COD_INC_TRIB do Registro 0110 | Alíquota do PIS (em percentual) (ALIQ_PIS) | Alíquota do PIS (em reais) (ALIQ_PIS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 1 | 1,65(PIS) | - |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 3 | 1,65(PIS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 2 | 0,65(PIS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 3 | 0,65(PIS) | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 1 | - | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 3 | - | - |
| 52 | Contribuição cumulativa apurada a alíquotas diferenciadas | 02 | 2 | - | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 1 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 1 | > 0 | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 3 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 3 | > 0 | - |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03 | 2 | - | > 0 |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03* | 2 | > 0 | - |
| 31 | Contribuição apurada por substituição tributária | 05 | - | 0,65(PIS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | Diferente de 0, 0,65(PIS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | - | >0 |

Tabela para apuração dos registros M210 – F200 (Item exclusivo para informações obtidas dos registros F200)

| Campo COD_CONT do Registro M210 | Descrição do COD_CONT | CST_PIS | Campo COD_INC_TRIB do Registro 0110 | Alíquota do PIS (em percentual) (ALIQ_PIS) | Alíquota do PIS (em reais) (ALIQ_PIS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 1 | 1,65 | - |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 1,65 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 2 | 0,65 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 0,65 | - |

O PVA não validará e não gerará automaticamente registros M210 com COD_CONT igual a 71 (Contribuição apurada de SCP – Incidência Não Cumulativa), 72 (Contribuição apurada de SCP – Incidência Cumulativa) e 99 (Contribuição para o PIS/Pasep – Folha de Salários – Vide registro M350).
Campo 03 - Preenchimento: informar o valor da receita bruta auferida no período, vinculada ao respectivo COD_CONT.
Validação: Quando o valor do campo 02 (COD_CONT) for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual à soma dos seguintes campos (quando o CST da operação vinculada for 01, 02, 03, 04, 05 com alíquota diferente de zero e 49):
VL_ITEM dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_ITEM dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_ITEM dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_ITEM dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_ITEM dos registros C381, C601, C870, C880, D201, D601
VL_DOC dos registros D300,
VL_BRT do registro D350,
VL_OPR do registro C175,
VL_OPER do registro F100, cujo valor do campo IND_OPER seja igual a “1” ou “2”,
VL_TOT_REC do registro F200,
VL_REC_CAIXA do registro F500 e F510,
VL_REC_COMP do registro F550 e F560,
VL_REC do registro I100.
Campo 04 - Preenchimento: informar o valor da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro, antes dos ajustes dos campos 05 e 06.
Validação: Quando a natureza da pessoa jurídica (IND_NAT_PJ do registro “0000” igual a 00, 02, 03 ou 05) não for sociedade cooperativa e o valor do campo COD_CONT for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual a:
VL_BC_PIS dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_BC_PIS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_BC_PIS dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_BC_PIS dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_BC_PIS dos registros C175, C381, C601, C870, D201, D300, D350, D601, F200, F500, F550,
VL_BC_PIS do registro F100, quando o valor do campo ALIQ_PIS não conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”,
VL_BC_PIS dos registros I100.
Quando o COD_CONT for igual a 03 ou 53, o valor deste campo será igual a zero.
Caso contrário (sociedade cooperativa), o valor deste campo será igual ao valor do campo VL_BC_CONT do registro M211.
Campo 05 - Preenchimento: informar neste campo o valor do total dos ajustes de acréscimo da base de cálculo mensal da contribuição a que se refere o Campo 04.
O valor mensal dos ajustes de acréscimo informado neste campo deve ser detalhado no Registro Filho M215, de acordo com as informações especificadas no leiaute deste registro, inclusive, devendo ser segregado e referenciado ao estabelecimento (CNPJ) a que se refere o ajuste.
Campo 06 - Preenchimento: informar neste campo o valor do total dos ajustes de redução da base de cálculo mensal da contribuição a que se refere o Campo 04.
O valor mensal dos ajustes de redução informado neste campo deve ser detalhado no Registro Filho M215, de acordo com as informações especificadas no leiaute deste registro, inclusive, devendo ser segregado e referenciado ao estabelecimento (CNPJ) a que se refere o ajuste.
Campo 07 – Preenchimento: informar o valor da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro, após os ajustes dos campos 05 e 06.
Campo 08 - Preenchimento: informar a alíquota do PIS/PASEP (em percentual) aplicável. Quando o COD_CONT for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 09 - Preenchimento: informar a quantidade da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro.
Validação: Quando o valor do campo COD_CONT for igual a 03, 53 ou 32, o valor do campo será igual a:
QUANT_BC_PIS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
QUANT_BC_PIS dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
QUANT_BC_PIS dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
QUANT_BC_PIS dos registros C381, C880, D350, F510 e F560,
VL_BC_PIS do registro F100, quando o valor do campo ALIQ_PIS conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”
Quando valor do campo COD_CONT for igual a 01, 51, 02, 52 ou 31 o campo deverá ser deixado em branco.
Campo 10 - Preenchimento: informar a alíquota do PIS (em reais) aplicável. Quando o COD_CONT não for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 11 - Preenchimento: informar o valor total da contribuição social apurada, vinculada ao COD_CONT do registro, correspondendo a QUANT_BC_PIS x ALIQ_PIS_QUANT, quando a contribuição for calculada por unidade de medida de produto ou VL_BC_CONT_AJUS x ALIQ_PIS/100, caso contrário.
Campo 12 - Preenchimento: informar o valor dos ajustes de acréscimo à contribuição social apurada no campo 11. O preenchimento deste campo obriga o respectivo detalhamento no registro M220, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M220 quando IND_AJ = 1.
Campo 13 - Preenchimento: informar o valor dos ajustes de redução à contribuição social apurada no campo 11. O preenchimento deste campo obriga o respectivo detalhamento no registro M220, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M220 quando IND_AJ = 0.
Campo 14 - Preenchimento: informar o valor da contribuição a diferir no período, referente às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998).
O preenchimento deste campo obriga o preenchimento do registro M230, devendo ser igual ao somatório do campo VL_CONT_DIF dos registros M230.
Campo 15 - Preenchimento: informar o valor da contribuição diferida em períodos anteriores, adicionada a este período de escrituração, referente às receitas diferidas recebidas no mês da escrituração.
O preenchimento deste campo obriga o preenchimento do registro M300, sendo que a soma dos valores deste campo de todos os registros M210 deverá ser igual a soma dos campos VL_CONT_DIFER_ANT dos registros M300, para um mesmo COD_CONT.
Campo 16 - Preenchimento: informar o valor total da contribuição do período da escrituração, para o respectivo COD_CONT, devendo ser igual a VL_CONT_APUR (campo 11) + VL_AJUS_ACRES (campo 12) - VL_AJUS_REDUC (campo 13) – VL_CONT_DIFER (campo 14) + VL_CONT_DIFER_ANT (campo 15).
<!-- End Registro M210 -->
<!-- Start Registro M211 -->
Registro M211: Sociedades Cooperativas – Composição da Base de Calculo – PIS/Pasep
Este registro deve ser preenchido quando o Campo “IND_NAT_PJ” do registro “0000” for igual a “01” ou “04”, tratando-se de registro obrigatório para a determinação das bases de cálculo das sociedades cooperativas. No caso da cooperativa se enquadrar em mais de um dos tipos abaixo indicados, informar o tipo preponderante.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M211" | C | 004* | - | S |
| 02 | IND_TIP_COOP | Indicador do Tipo de Sociedade Cooperativa: 01 – Cooperativa de Produção Agropecuária; 02 – Cooperativa de Consumo; 03 – Cooperativa de Crédito; 04 – Cooperativa de Eletrificação Rural; 05 – Cooperativa de Transporte Rodoviário de Cargas; 06 – Cooperativa de Médicos; 99 – Outras. | N | 002* | - | S |
| 03 | VL_BC_CONT_ANT_EXC_COOP | Valor da Base de Cálculo da Contribuição, conforme Registros escriturados nos Blocos A, C, D e F, antes das Exclusões das Cooperativas. | N | - | 02 | S |
| 04 | VL_EXC_COOP_GER | Valor de Exclusão Especifica das Cooperativas em Geral, decorrente das Sobras Apuradas na DRE, destinadas a constituição do Fundo de Reserva e do FATES. | N | - | 02 | N |
| 05 | VL_EXC_ESP_COOP | Valor das Exclusões da Base de Cálculo Especifica do Tipo da Sociedade Cooperativa, conforme Campo 02 (IND_TIP_COOP). | N | - | 02 | N |
| 06 | VL_BC_CONT | Valor da Base de Cálculo, Após as Exclusões Especificas da Sociedade Cooperativa (04 – 05 – 06) – Transportar para M210. | N | - | 02 | S |

Observações:
Nível hierárquico - 4
Ocorrência – 1:1
Campo 01 - Valor Válido: [M211]
Campo 02 - Valores válidos: [01, 02, 03, 04, 05, 06, 99]
Preenchimento: informar o tipo de sociedade cooperativa. Caso a cooperativa se enquadre em mais de um tipo, informe o fim preponderante.
Campo 03 - Preenchimento: informar o valor da base de cálculo da contribuição, vinculada ao COD_CONT do registro M210, conforme registros escriturados nos Blocos A, C, D e F, antes das exclusões das cooperativas.
Validação: Quando o valor do campo COD_CONT for igual a 01, 51, 02, 52, 31 ou 32 (no caso de apuração da contribuição com base em alíquotas da tabela 4.3.10), o valor do campo será igual a:
· VL_BC_PIS dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
· VL_BC_PIS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
· VL_BC_PIS dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
· VL_BC_PIS dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
· VL_BC_PIS dos registros C175, C381, C601, C870, D201, D300, D350, D601, F200, F500, F550, I100
· VL_BC_PIS do registro F100, quando o valor do campo ALIQ_PIS não conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”
Nos demais casos, o valor deste e dos demais campos será igual a zero.
Campo 04 - Preenchimento: informar o valor exclusão especifica das cooperativas em geral, decorrente das sobras apuradas na DRE, destinadas a constituição do fundo de reserva e do FATES.
Campo 05 - Preenchimento: informar o valor das exclusões da base de cálculo especifica do tipo da sociedade cooperativa, conforme campo 02 (IND_TIP_COOP).
Campo 06 - Preenchimento: informar o valor da base de cálculo, após as exclusões especificas da sociedade cooperativa, correspondendo a VL_BC_CONT_ANT_EXC_COOP - VL_EXC_COOP_GER - VL_EXC_ESP_COOP. O valor apurado neste campo deverá ser transportado para o campo 04 (VL_BC_CONT), do registro pai M210.
<!-- End Registro M211 -->
<!-- Start Registro M215 -->
Registro M215: Ajustes da Base de Cálculo da Contribuição para o PIS/Pasep Apurada
Este registro será utilizado pela pessoa jurídica para detalhar os totais de ajustes da base de cálculo, informados nos campos 05 e 06 do registro pai M210.
A chave do registro é formada pelos campos: IND_AJ_BC; COD_AJ_BC; NUM_DOC; COD_CTA; DT_REF; CNPJ e INFO_COMPL

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M215" | C | 004 | - | S |
| 02 | IND_AJ_BC | Indicador do tipo de ajuste da base de cálculo: 0 - Ajuste de redução; 1 - Ajuste de acréscimo. | C | 001* | - | S |
| 03 | VL_AJ_BC | Valor do ajuste de base de cálculo | N | - | 02 | S |
| 04 | COD_AJ_BC | Código do ajuste, conforme a Tabela indicada no item 4.3.18 | C | 002* | - | S |
| 05 | NUM_DOC | Número do processo, documento ou ato concessório ao qual o ajuste está vinculado, se houver. | C | - | - | N |
| 06 | DESCR_AJ_BC | Descrição resumida do ajuste na base de cálculo. | C | - | - | N |
| 07 | DT_REF | Data de referência do ajuste (ddmmaaaa) | N | 008* | - | N |
| 08 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 09 | CNPJ | CNPJ do estabelecimento a que se refere o ajuste | N | 014* | - | S |
| 10 | INFO_COMPL | Informação complementar do registro | C | - | - | N |

Observações:
1. Este registro deve ser escriturado, obrigatoriamente, quando a pessoa jurídica informar valores de ajustes de acréscimo ou de redução da base de cálculo mensal da contribuição, no Registro Pai M210, objetivando demonstrar, de forma analítica e segregada, os totais dos ajustes na base de cálculo da contribuição correspondente ao período a que se refere a escrituração.
2. Como já informado neste Guia Prático da Escrituração, os ajustes da base de cálculo mensal das contribuições, objeto de escrituração consolidada (nos campos 05 e 06 do Registro Pai M210) e analítica (no Registro Filho M215), só são habilitados na escrituração das contribuições referentes aos períodos de apuração correspondentes aos fatos geradores a ocorrer a partir de 01 de janeiro de 2019.
3. Desta forma, mesmo que a pessoa jurídica esteja utilizando a versão 3.1.0 e posteriores da versão do programa da EFD-Contribuições para a escrituração de fatos geradores ocorridos até 31.12.2018, a versão em referência não disponibiliza estes campos de ajustes de base de cálculo, especificados nos Registros M210 e M215.
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [M215]
Campo 02 - Valores válidos: [0, 1]
Campo 03 - Preenchimento: informar o valor do ajuste de redução ou de acréscimo da base de cálculo mensal da contribuição que está sendo objeto de segregação, de escrituração analítica, neste registro filho.
A soma de todos os valores analíticos representativos de ajustes de acréscimo de base de cálculo (IND_AJ_BC = 1) e de ajustes de redução de base de cálculo (IND_AJ_BC = 0) dos diversos registros M215 escriturados e relativos ao período da escrituração, deverá corresponder aos valores totais escriturados nos campos 05 (VL_AJUS_ACRES_BC_PIS) e 06 (VL_AJUS_REDUC_BC_PIS) do Registro Pai M210, respectivamente.
Campo 04 - Preenchimento: informar o código do ajuste da base de cálculo, conforme Tabela 4.3.18 - “Tabela Código de Ajustes da Base de Cálculo Mensal”, referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informar, se for o caso, o número do processo, documento ou ato concessório ao qual o ajuste está vinculado, como por exemplo, o número do processo judicial que autoriza a pessoa jurídica a proceder a ajustes na base de cálculo mensal da contribuição.
Campo 06 - Preenchimento: informar a descrição resumida do ajuste da base de cálculo mensal que está sendo escriturado no respectivo registro.
Campo 07 - Preenchimento: informar, se for o caso, a data de referência do ajuste, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
No caso de o ajuste informado no registro não ser específico de uma data do período, deve ser informado a data correspondente ao ultimo dia do mês a que se refere a escrituração, como por exemplo, “31012019”.
Campo 08 - Preenchimento: Informar, sendo o caso, o código da conta contábil a que se refere o ajuste detalhado neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 09 - Preenchimento: informar o CNPJ do estabelecimento da pessoa jurídica a que se refere o ajuste escriturado neste registro.
Caso o ajuste não se refira a um estabelecimento especifico, deve ser informado o CNPJ correspondente ao estabelecimento matriz da pessoa jurídica, escriturado no Registro “0000”.
Campo 10 - Preenchimento: Campo para prestação de outras informações que se mostrem necessárias ou adequadas, para esclarecer ou justificar o ajuste na base de cálculo a que se refere este registro.
<!-- End Registro M215 -->
<!-- Start Registro M220 -->
Registro M220: Ajustes da Contribuição para o PIS/Pasep Apurada
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas nos campos 09 e 10 do registro pai M210.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M220" | C | 004 | - | S |
| 02 | IND_AJ | Indicador do tipo de ajuste: 0- Ajuste de redução; 1- Ajuste de acréscimo. | C | 001* | - | S |
| 03 | VL_AJ | Valor do ajuste | N | - | 02 | S |
| 04 | COD_AJ | Código do ajuste, conforme a Tabela indicada no item 4.3.8. | C | 002* |   | S |
| 05 | NUM_DOC | Número do processo, documento ou ato concessório ao qual o ajuste está vinculado, se houver. | C | - | - | N |
| 06 | DESCR_AJ | Descrição resumida do ajuste. | C | - | - | N |
| 07 | DT_REF | Data de referência do ajuste (ddmmaaaa) | N | 008* | - | N |

Observações:
Nível hierárquico - 4
Ocorrência – 1:N (por tipo de contribuição M200)
Campo 01 - Valor Válido: [M220]
Campo 02 - Valores Válidos: [0, 1]
Campo 03 - Preenchimento: informar o valor do ajuste de redução ou de acréscimo. A soma de todos os valores deste campo, representando ajustes de acréscimo (IND_AJ = 1) deverá ser transportada para o campo 09 (VL_AJUS_ACRES) do registro M210. Por sua vez, a soma de todos os valores deste campo, representando ajustes de redução (IND_AJ = 0) deverá ser transportada para o campo 10 (VL_AJUS_REDUC) do registro M210
Campo 04 - Preenchimento: informar o código do ajuste, conforme Tabela 4.3.8 - “Tabela Código de Ajustes de Contribuição ou Créditos”, referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informar, se for o caso, o número do processo, documento ou ato concessório ao qual o ajuste está vinculado, como por exemplo, o documento fiscal referenciado na devolução de venda.
No caso de ajuste que envolva grande quantidade de documentos, pode o registro ser escriturado consolidando as informações dos documentos, descrevendo no campo 06 (tipo de documento fiscal consolidado, quantidades de documentos, emitente/beneficiário, por exemplo).
Campo 06 - Preenchimento: informar a descrição resumida do ajuste que está sendo lançada no respectivo registro.
Campo 07 - Preenchimento: informar, se for o caso, a data de referência do ajuste, no formato "ddmmaaaa", excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
<!-- End Registro M220 -->
<!-- Start Registro M225 -->
Registro M225: Detalhamento dos Ajustes da Contribuição Para o Pis/Pasep Apurada
Registro a ser preenchido para a pessoa jurídica detalhar a operação e valor a que se refere o ajuste da contribuição informado no registro pai – M220.
Registro não disponível para os fatos geradores até 30/09/2015.
Para os fatos geradores a partir de 01/10/2015 a versão 2.12 do Programa da EFD-Contribuições (PVA) disponibiliza este registro de detalhamento dos ajustes de PIS/Pasep, o qual deve ser preenchido, para que seja demonstrado e detalhado à Receita Federal quais as operações realizadas que ensejaram os ajustes informados no registro M220, quando a informação prestada no Registro M220 não seja suficientemente analítica, de forma a detalhar a(s) operação(ões) ensejadora(s) do ajuste.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M225” | C | 004* | - | S |
| 02 | DET_VALOR_AJ | Detalhamento do valor da contribuição reduzida ou acrescida, informado no Campo 03 (VL_AJ) do registro M220. | N | - | 02 | S |
| 03 | CST_PIS | Código de Situação Tributária referente à operação detalhada neste registro. | N | 002* | - | N |
| 04 | DET_BC_CRED | Detalhamento da base de cálculo geradora de ajuste de contribuição | N | - | 03 | N |
| 05 | DET_ALIQ | Detalhamento da alíquota a que se refere o ajuste de contribuição | N | 08 | 04 | N |
| 06 | DT_OPER_AJ | Data da operação a que se refere o ajuste informado neste registro. | N | 008* | - | S |
| 07 | DESC_AJ | Descrição da(s) operação(ões) a que se refere o valor informado no Campo 02 (DET_VALOR_AJ) | C | - | - | N |
| 08 | COD_CTA | Código da conta contábil debitada/creditada | C | 255 | - | N |
| 09 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
Nível hierárquico – 5
Ocorrência - 1:N
Campo 01 - Valor Válido: [M225]
Campo 02 - Preenchimento: Informar o detalhamento do valor da operação a que se refere o ajuste da contribuição informado no Campo 03 (VL_AJ) do registro M220.
Caso o ajuste em M220 se refira a várias operações ou situações, devem ser gerados os registros de detalhamento M225 que se mostrem necessários e suficientes, para demonstrar o valor total do ajuste escriturado em M220.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao ajuste de contribuição de PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 04 - Preenchimento: Informar a base de cálculo do ajuste de contribuição a que se refere este registro.
Campo 05 - Preenchimento: Informar a alíquota a que se refere o ajuste de contribuição informado neste registro.
Campo 06 - Preenchimento: Informar a data da operação a que se refere o ajuste de contribuição detalhado neste registro.
Campo 07 - Preenchimento: Informar a descrição da(s) operação(ões) a que se refere o ajuste detalhado neste registro.
Campo 08 - Preenchimento: Informar, sendo o caso, o código da conta contábil a que se refere o ajuste detalhado neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 09 - Preenchimento: Campo para prestação de outras informações que se mostrem necessárias ou adequadas, para esclarecer ou justificar o ajuste.
<!-- End Registro M225 -->
<!-- Start Registro M230 -->
Registro M230: Informações Adicionais de Diferimento
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas no campo 11 (VL_CONT_DIFER) do registro pai M210, referente às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998).
Os créditos da não-cumulatividade vinculados a estas receitas ainda não recebidas também deverão ser detalhados neste registro, sendo que o somatório dos campos 11 (VL_CRED_DIF) do registro M100 deverá ser igual ao somatório dos campos VL_CRED_DIF dos registros M230, para o mesmo COD_CRED.
O somatório do campo 05 (VL_CONT_DIF) destes registros deverá ser igual ao valor lançado no respectivo campo 11 do registro pai M210.
Deverá existir um registro M230 para cada CNPJ em que houve contribuição diferida no período e para cada código de tipo de crédito diferido no período. Assim, a chave do registro é formada pelos campos CNPJ + COD_CRED.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M230" | C | 004* | - | S |
| 02 | CNPJ | CNPJ da pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias. | N | 014* | - | S |
| 03 | VL_VEND | Valor Total das vendas no período | N | - | 02 | S |
| 04 | VL_NAO_RECEB | Valor Total não recebido no período | N | - | 02 | S |
| 05 | VL_CONT_DIF | Valor da Contribuição diferida no período | N | - | 02 | S |
| 06 | VL_CRED_DIF | Valor do Crédito diferido no período | N | - | 02 | N |
| 07 | COD_CRED | Código de Tipo de Crédito diferido no período, conforme a Tabela 4.3.6. | C | 003* | - | N |

Observações:
Nível hierárquico – 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [M230]
Campo 02 - Preenchimento: informar o CNPJ da pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias para a qual foi realizada a construção por empreitada ou o fornecimento a preço predeterminado de bens ou serviços.
Campo 03 - Preenchimento: informar o valor total das vendas no período da escrituração para o CNPJ informado no campo 02.
Campo 04 - Preenchimento: informar o valor total não recebido no período da escrituração, referente ao CNPJ informado no campo 02.
Campo 05 - Preenchimento: informar a contribuição diferida no período, referente ao não recebimento de valores do CNPJ informado no campo 02.
Campo 06 - Preenchimento: informar o valor dos créditos da não-cumulatividade vinculados às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços, conforme o tipo de crédito diferido, informado no campo 07 (COD_CRED) deste registro.
Campo 07 - Preenchimento: informar o código de tipo de crédito diferido no período, informado no campo 06, conforme tabela 4.3.6 - "Tabela Código de Tipo de Crédito" referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
<!-- End Registro M230 -->
<!-- Start Registro M300 -->
Registro M300: Contribuição de PIS/pasep Diferida em Períodos Anteriores – Valores a Pagar no Período.
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas no campo 12 (VL_CONT_DIFER_ANT) dos diversos registros M210 existentes na escrituração.
Os valores da contribuição diferida em períodos anteriores, que deverão ser pagos no atual período da escrituração, face aos recebimentos ocorridos no mês, descontados dos respectivos créditos diferidos, serão adicionados à respectiva contribuição calculada (COD_CONT) no registro M210, sendo que a soma dos valores do campo 12 de todos os registros M210 deverá ser igual a soma dos campos VL_CONT_DIFER_ANT dos registros M300, para um mesmo COD_CONT.
Deverá existir um registro M300 para cada data em que houve recebimento de receita objeto de diferimento, de maneira combinada com o período da escrituração em que o diferimento ocorreu e para cada tipo de contribuição diferida e natureza do crédito diferido a descontar no período. Assim, a chave deste registro é formada pelos campos COD_CONT + NAT_CRED_DESC + PER_APUR + DT_RECEB.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M300" | C | 004* | - | S |
| 02 | COD_CONT | Código da contribuição social diferida em períodos anteriores, conforme a Tabela 4.3.5. | C | 002 | - | S |
| 03 | VL_CONT_APUR_DIFER | Valor da Contribuição Apurada, diferida em períodos anteriores. | N | - | 02 | S |
| 04 | NAT_CRED_DESC | Natureza do Crédito Diferido, vinculado à receita tributada no mercado interno, a descontar: 01 – Crédito a Alíquota Básica; 02 – Crédito a Alíquota Diferenciada; 03 – Crédito a Alíquota por Unidade de Produto; 04 – Crédito Presumido da Agroindústria. | C | 002 | - | N |
| 05 | VL_CRED_DESC_DIFER | Valor do Crédito a Descontar vinculado à contribuição diferida. | N | - | 02 | N |
| 06 | VL_CONT_DIFER_ANT | Valor da Contribuição a Recolher, diferida em períodos anteriores (Campo 03 – Campo 05) | N | - | 02 | S |
| 07 | PER_APUR | Período de apuração da contribuição social e dos créditos diferidos (MMAAAA) | N | 006* | - | S |
| 08 | DT_RECEB | Data de recebimento da receita, objeto de diferimento | N | 008* | - | N |

Observações: O valor do Campo 06 (VL_CONT_DIFER_ANT) será recuperado no registro M210, Campo 12, que detalha a contribuição devida no período da escrituração.
Nível hierárquico – 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [M300]
Campo 02 - Preenchimento: informe o código da contribuição social diferida em períodos anteriores que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>
Campo 03 - Preenchimento: informar o valor da contribuição apurada, diferida em períodos anteriores e que deverá ser paga no período da escrituração, após o desconto de eventuais créditos informados no campo 05.
Campo 04 - Valores válidos: [01, 02, 03, 04]
Campo 05 - Preenchimento: informar o valor do crédito a descontar vinculado à contribuição diferida
Campo 06 - Preenchimento: informar o valor da contribuição a recolher, diferida em períodos anteriores, após o desconto de eventuais créditos informados no campo 05, correspondendo, então, a VL_CONT_APUR_DIFER - VL_CRED_DESC_DIFER.
Campo 07 - Preenchimento: informar o período de apuração da contribuição social e dos créditos diferidos, conforme informado anteriormente no registro M230 (no caso do respectivo período ter sido objeto de transmissão da EFD PIS/COFINS). Utilize o formato “mmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.  O período informado não pode ser o mesmo da atual escrituração.
Campo 08 - Preenchimento: informar a data de recebimento da receita, objeto de diferimento.
Validação: A data deverá estar compreendida no período da atual escrituração.
<!-- End Registro M300 -->
<!-- Start Registro M350 -->
Registro M350: PIS/Pasep – Folha de Salários
Este registro deverá ser informado caso a pessoa jurídica também ser contribuinte do PIS/Pasep sobre a Folha de Salários, bem como no caso das sociedades cooperativas, na hipótese destas procederem a quaisquer das exclusões previstas no art. 15 da MP nº 2.158, de 2001 e no art. 1º da Lei nº 10.676, de 2003.
O registro também deve ser utilizado (IND_NAT_PJ do registro 0000 igual a 02) pelos templos de qualquer culto, partidos políticos, as instituições de educação e de assistência social a que se refere o art. 12 da Lei no 9.532, de 10 de dezembro de 1997, as instituições de caráter filantrópico, recreativo, cultural, científico e as associações, a que se refere o art. 15 da Lei no 9.532, de 1997, os sindicatos, as federações e as confederações, os serviços sociais autônomos, criados ou autorizados por lei, os conselhos de fiscalização de profissões regulamentadas, as fundações de direito privado e as fundações públicas instituídas ou mantidas pelo Poder Público e os condomínios de proprietários de imóveis residenciais ou comerciais.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M350" | C | 004* | - | S |
| 02 | VL_TOT_FOL | Valor Total da Folha de Salários | N | - | 02 | S |
| 03 | VL_EXC_BC | Valor Total das Exclusões à Base de Cálculo | N | - | 02 | S |
| 04 | VL_TOT_BC | Valor Total da Base de Cálculo | N | - | 02 | S |
| 05 | ALIQ_PIS_FOL | Alíquota do PIS/PASEP – Folha de Salários | N | 006 | 02 | S |
| 06 | VL_TOT_CONT_FOL | Valor Total da Contribuição Social sobre a Folha de Salários | N | - | 02 | S |

Observações: No caso da pessoa jurídica também ser contribuinte do PIS/Pasep sobre a Folha de Salários, como no caso das sociedades cooperativas, na hipótese prevista no art. 15 da MP nº 2.158 de 2001, deve escriturar este registro a informar a contribuição devida com base na folha de salários do mês da escrituração.
Nível hierárquico – 2
Ocorrência – Um (por arquivo)
Campo 01 - Valor Válido: [M350]
Campo 02 - Preenchimento: informe o valor total da folha de salários
Campo 03 - Preenchimento: informe o valor total das exclusões à base de cálculo, como por exemplo, o salário família, o aviso prévio indenizado, o Fundo de Garantia por Tempo de Serviço (FGTS) pago diretamente ao empregado na rescisão contratual e a indenização por dispensa, desde que dentro dos limites legais.
Campo 04 - Preenchimento: informar o valor da base de cálculo do PIS/Pasep incidente sobre a folha de salários, apurado conforme campos 03 e 04.
Campo 05 - Valor Válido: [1]
Campo 06 - Preenchimento: informar o valor total da contribuição social sobre a folha de salários, correspondendo a "VL_TOT_BC" x "ALIQ_PIS_FOL".
<!-- End Registro M350 -->
<!-- Start Registro M400 -->
Registro M400: Receitas Isentas, não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas com Suspensão – PIS/Pasep
Este registro será utilizado pela pessoa jurídica para consolidar as receitas não sujeitas ao pagamento da contribuição social, com base nos CST específicos (04, 06, 07, 08 e 09) informados nas receitas relacionadas nos Blocos A, C, D e F.
Conforme item “4. Procedimentos de escrituração na revenda de bens sujeitos à substituição tributária de PIS/COFINS”, até a versão 2.0.4a e anteriores do PGE, documentos escriturados com CST 05 e alíquota zero eram totalizados nos registros M400 e M800. A partir da versão 2.0.5 do PGE, todas as operações com CST 05 devem ser totalizadas nos registros M210 e M610. Dessa forma, as menções ao CST 05 nas orientações deste registro e respectivo registro filho aplicam-se apenas aos fatos geradores escriturados nas versões 2.0.4a e anteriores do PGE.
Quando utilizada a funcionalidade de “Gerar Apuração” do PVA EFD PIS/COFINS este registro será gerado automaticamente pelo PVA. Contudo, o registro filho M410, de natureza obrigatória neste caso, deverá ser preenchido pela própria pessoa jurídica.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M400” | C | 004* | - | S |
| 02 | CST_PIS | Código de Situação Tributária – CST das demais receitas auferidas no período, sem incidência da contribuição, ou sem contribuição apurada a pagar, conforme a Tabela 4.3.3. | C | 002* | - | S |
| 03 | VL_TOT_REC | Valor total da receita bruta no período. | N | - | 02 | S |
| 04 | COD_CTA | Código da conta analítica contábil debitada/creditada. | C | 255 | - | N |
| 05 | DESC_COMPL | Descrição Complementar da Natureza da Receita. | C | - | - | N |

Observações:
1. Neste registro serão escrituradas as receitas não sujeitas ao pagamento da contribuição social, com base nos CST específicos informados nas receitas relacionadas nos Blocos A, C, D e F.
2. O campo VL_TOT_REC sera recuperado do somatório dos campos VL_REC dos registros M410.
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [M400]
Campo 02 - Valores válidos: [04, 05, 06, 07, 08, 09]
Preenchimento: informar o CST relativo às demais receitas auferidas no período, sem incidência da contribuição, ou sem contribuição apurada a pagar.
Campo 03 - Preenchimento: informar o valor total da receita bruta no período, referente ao CST informado no campo 02, correspondendo à soma dos seguintes campos:
VL_ITEM dos registros A170, cujo valor do campo IND_OPER do respectivo registro A100, seja igual a “1”,
VL_ITEM dos registros C170, cujo valor do campo COD_MOD do registro C100 seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_ITEM dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_ITEM dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_ITEM dos registros C381, C601, D201, D601,
VL_DOC dos registros D300,
VL_BRT do registro D350,
VL_OPR do registro C175,
VL_OPER do registro F100, cujo valor do campo IND_OPER seja igual a “1” ou “2”,
VL_TOT_REC do registro F200,
VL_REC_CAIXA dos registros F500 e F510,
VL_REC_COMP dos registros F550 e F560,
VL_REC do registro I100.
No caso de ser informado o CST 05 - Operação Tributável por Substituição Tributária, o preenchimento deste campo deverá ser feito apenas quando a alíquota aplicável for igual a zero (casos de revenda de produtos sujeitos à substituição tributária).
Campo 04 - Preenchimento: informar o código da conta contábil representativa da receita desonerada da contribuição a que se refere este registro. Exemplos: Receitas tributadas à alíquota zero, com suspensão, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta informada no registro de detalhamento M410). No caso de ser informado neste campo a conta sintética de receita, deve então ser informado no Campo 04 (COD_CTA) do(s) registro(s) filho M410, a conta de nível inferior (analítica ou sintética, conforme o plano de contas da empresa).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 05 - Preenchimento: informar a descrição complementar da natureza da receita.
<!-- End Registro M400 -->
<!-- Start Registro M410 -->
Registro M410: Detalhamento das Receitas Isentas, não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas com Suspensão – Cofins
Neste registro a pessoa jurídica deverá detalhar as receitas isentas, não alcançadas pela incidência da contribuição, sujeitas à alíquota zero ou de vendas com suspensão, totalizadas no registro pai M400, conforme relação de códigos constantes das tabelas relacionadas no campo 02 (NAT_REC) e respectivas descrições complementares de cada uma das receitas sendo detalhadas. Desta forma, a chave deste registro é composta pelos campos NAT_REC + COD_CTA + DESC_COMPL.
Este registro não será gerado automaticamente pelo PVA EFD PIS/COFINS, sendo necessário a pessoa jurídica preencher manualmente mesmo quando utilizada a opção de “Gerar Apuração”.
A soma dos campos VL_REC dos registros M410 deverá corresponder ao valor informado/calculado no campo VL_TOT_REC do registro pai M400.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M410” | C | 004* | - | S |
| 02 | NAT_REC | Natureza da Receita, conforme relação constante nas Tabelas de Detalhamento da Natureza da Receita por Situação Tributária abaixo: - Tabela 4.3.10: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas Diferenciadas (CST 04 - Revenda); - Tabela 4.3.11: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda); - Tabela 4.3.12: Produtos Sujeitos à Substituição Tributária da Contribuição Social (CST 05 - Revenda); - Tabela 4.3.13: Produtos Sujeitos à Alíquota Zero da Contribuição Social (CST 06); - Tabela 4.3.14: Operações com Isenção da Contribuição Social (CST 07); - Tabela 4.3.15: Operações sem Incidência da Contribuição Social (CST 08); - Tabela 4.3.16: Operações com Suspensão da Contribuição Social (CST 09). | C | 003* | - | S |
| 03 | VL_REC | Valor da receita bruta no período, relativo a natureza da receita (NAT_REC) | N | - | 02 | S |
| 04 | COD_CTA | Código da conta analítica contábil debitada/creditada. | C | 255 | - | N |
| 05 | DESC_COMPL | Descrição Complementar da Natureza da Receita. | C | - | - | N |

Observações:
1. As receitas componentes deste registro (receitas não tributadas ou não sujeitas ao pagamento da contribuição) devem ser informadas nos respectivos registros dos blocos A, C, D e F.
2. Deve ser informado no Campo 02 o detalhamento da natureza da receita não tributada ou não sujeita ao pagamento da contribuição, conforme as tabelas externas disponibilizadas pela RFB.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [M410]
Campo 02 - Preenchimento: informar a natureza da receita sendo detalhada no registro, conforme códigos existentes nas tabelas abaixo indicadas, obedecendo ao respectivo CST orientador:
Para o CST 04 - Operação Tributável Monofásica - Revenda a Alíquota Zero, utilize os códigos constantes nas tabelas 4.3.10: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas Diferenciadas e 4.3.11: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto.
Para o CST 05 (e alíquota zero) - Operação Tributável por Substituição Tributária, utilize os códigos da Tabela 4.3.12: Produtos Sujeitos à Substituição Tributária da Contribuição Social.
Para o CST 06 - Operação Tributável a Alíquota Zero, utilize os códigos da Tabela 4.3.13: Produtos Sujeitos à Alíquota Zero da Contribuição Social.
Para o CST 07 - Operação Isenta da Contribuição, utilize os códigos da Tabela 4.3.14: Operações com Isenção da Contribuição Social.
Para o CST 08 - Operação sem Incidência da Contribuição, utilize os códigos da Tabela 4.3.15: Operações sem Incidência da Contribuição Social.
Para o CST 09 - Operação com Suspensão da Contribuição, utilize os códigos da Tabela 4.3.16: Operações com Suspensão da Contribuição Social.
Campo 03 - Preenchimento: informar o valor da receita bruta no período, relativo a natureza da receita informada no campo 02.
Campo 04 - Preenchimento: informar o código da conta analítica ou sintética referente à receita relativa à respectiva natureza informada no campo 02. Deve ser a conta contábil de nível inferior à informada no Registro M400.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 05 - Preenchimento: informar a descrição complementar da natureza da receita, relativa a natureza da receita informada no campo 02.
<!-- End Registro M410 -->
<!-- Start Registro M500 -->
Registro M500: Crédito de Cofins Relativo Ao Período
Este registro tem por finalidade realizar a consolidação do crédito relativo à Cofins apurado no período. Deve ser gerado um registro M500 especifico para cada tipo de crédito apurado (vinculados à receita tributada, vinculados à receita não tributada e vinculados à exportação), conforme a Tabela de tipos de créditos “Tabela 4.3.6”, bem como para créditos de operações próprias e créditos transferidos por eventos de sucessão.
ATENÇÃO: Os valores escriturados nos registros M500 (Crédito de Cofins do Período) e M505 (Detalhamento da Base de Cálculo do Crédito de Cofins do Período) serão determinados com base:
Nos valores informados no arquivo elaborado pela própria pessoa jurídica e importado pelo Programa Validador e Assinador da EFD-Contribuições – PVA, os quais serão objeto de validação; ou
Nos valores calculados pelo PVA para os registros M500 e M505, através da funcionalidade “Gerar Apurações”, disponibilizada no PVA, com base nos registros da escrituração constantes nos Blocos “A”, “C”, “D” e “F”.
No caso de operações e documentos informados nos referidos blocos em que os campos “CST_COFINS” se refiram a créditos comuns a mais de um tipo de receitas (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA procederá o cálculo automático do crédito (funcionalidade “Gerar Apurações”) caso a pessoa jurídica tenha optado pelo método de apropriação com base no Rateio Proporcional com base na Receita Bruta (indicador “2” no Campo 03 do Registro 0110), considerando para fins de rateio, no Registro M505, os valores de Receita Bruta informados no Registro 0111.
Desta forma, caso a pessoa jurídica tenha optado pelo método do Rateio Proporcional com base na Receita Bruta (Bruta (indicador “2” no Campo 03 do Registro 0110), o PVA procederá ao cálculo automático do crédito em relação a todos os Códigos de Situação Tributária (CST 50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65 e 66).
Caso a pessoa jurídica tenha optado pelo método de Apropriação Direta (indicador “1” no Campo 03 do Registro 0110) para a determinação dos créditos comuns a mais de um tipo de receita (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA não procederá ao cálculo dos créditos (funcionalidade “Gerar Apurações”) relacionados a estes CST, no Registro M505, gerando o cálculo dos créditos apenas em relação aos CST 50, 51, 52, 60, 61 e 62. Neste caso, deve a pessoa jurídica editar os registros M505 correspondentes ao CST representativos de créditos comuns (CST 53, 54, 55, 56, 63, 64, 65 e 66), com base na apropriação direta, inclusive em relação aos custos, por meio de sistema de contabilidade de custos integrada e coordenada com a escrituração, conforme definido no § 8º do art. 3º, da Lei nº 10.833, de 2003.
A geração automática de apuração (funcionalidade “Gerar Apurações”) o PVA apura, em relação ao Registro M500,  apenas os valores dos campos 02 (COD_CRED), 03 (IND_CRED_ORI), 04 (VC_BC_COFINS), 05 (ALIQ_COFINS), 06 (QUANT_BC_COFINS), 07 (ALIQ_COFINS_QUANT) e 08 (VL_CRED).
Os campos de ajustes (Campos 09 e 10) e de diferimento (Campos 11 e 12) não serão recuperados na geração automática de apuração,  devendo sempre serem informados pela própria pessoa jurídica no arquivo importado pelo PVA ou complementado pela edição do registro M500.
Na funcionalidade de geração automática de apuração, os valores apurados e preenchidos pelo PVA irão sobrepor (substituir) os valores eventualmente existentes nos referidos campos, constantes na escrituração.
As pessoas jurídicas sujeitas exclusivamente ao regime cumulativo das contribuições não devem preencher este registro, devendo eventuais créditos admitidos no regime cumulativo serem informados no registro F700 e consolidados em M600 (Campo 11 - VL_OUT_DED_CUM). Para as demais pessoas jurídicas (exceto atividade imobiliária), deverá existir um registro M500 para cada tipo de crédito e alíquota informados nos documentos que constam dos registros A100/A170, C100/C170, C190/C195, C395/C395, C500/C505, D100/D105, D500/D505, F100, F120, F130 e F150.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M500" | C | 004* | - | S |
| 02 | COD_CRED | Código de Tipo de Crédito apurado no período, conforme a Tabela 4.3.6. | C | 003* | - | S |
| 03 | IND_CRED_ORI | Indicador de Crédito Oriundo de: 0 – Operações próprias 1 – Evento de incorporação, cisão ou fusão | N | 001* | - | S |
| 04 | VL_BC_COFINS | Valor da Base de Cálculo do Crédito | N | - | 02 | N |
| 05 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 06 | QUANT_BC_COFINS | Quantidade – Base de cálculo COFINS | N | - | 03 | N |
| 07 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 08 | VL_CRED | Valor total do crédito apurado no período | N | - | 02 | S |
| 09 | VL_AJUS_ACRES | Valor total dos ajustes de acréscimo | N | - | 02 | S |
| 10 | VL_AJUS_REDUC | Valor total dos ajustes de redução | N | - | 02 | S |
| 11 | VL_CRED_DIFER | Valor total do crédito diferido no período | N | - | 02 | S |
| 12 | VL_CRED_DISP | Valor Total do Crédito Disponível relativo ao Período (08 + 09 – 10 – 11) | N | - | 02 | S |
| 13 | IND_DESC_CRED | Indicador de utilização do crédito disponível no período: 0 – Utilização do valor total para desconto da contribuição apurada no período, no Registro M600; 1 – Utilização de valor parcial para desconto da contribuição apurada no período, no Registro M600. | C | 001* | - | S |
| 14 | VL_CRED_DESC | Valor do Crédito disponível, descontado da contribuição apurada no próprio período. Se IND_DESC_CRED=0, informar o valor total do Campo 12; Se IND_DESC_CRED=1, informar o valor parcial do Campo 12. | N | - | 02 | N |
| 15 | SLD_CRED | Saldo de créditos a utilizar em períodos futuros (12 – 14) | N | - | 02 | S |

Observações:
1. Deve ser gerado um registro M500 especifico para cada tipo de crédito apurado (vinculados a receita tributada, vinculados a receita não tributada e vinculados a exportação), conforme a Tabela de tipos de créditos “Tabela 4.3.6”.
2. A base de cálculo do crédito, determinada no Campo “VL_BC_COFINS” deste registro, deve ser recuperada e corresponder ao somatório dos Campos “VL_BC_COFINS” de todos os registros Filho “M505”, que detalham a composição da base de cálculo do crédito.
3. No caso do crédito ser determinado com base em Unidade de Medida de Produto (crédito código 103, 203 e 303 da Tabela 4.3.6), a base de cálculo a ser determinada no Campo “QUANT_BC_COFINS” deste registro, deve ser recuperada e corresponder ao somatório dos Campos “QUANT_BC_COFINS” de todos os registros Filho “M505”, que detalham a composição da base de cálculo do crédito em quantidade.
Nível hierárquico – 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [M500]
Campo 02 - Preenchimento: informe o código do tipo do crédito cujo crédito está sendo totalizado no registro, conforme a Tabela “4.3.6 – Tabela Código de Tipo de Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Os códigos dos tipos de créditos são definidos a partir das informações de CST e Alíquota constantes nos documentos e operações registrados nos blocos A, C, D e F.
O CST 50 é mapeado para o grupo 100 (crédito vinculado exclusivamente a receita tributada no mercado interno), o CST 51 para o grupo 200 (crédito vinculado exclusivamente a receita não tributada no mercado interno) e o CST 52 para o grupo 300 (crédito vinculado exclusivamente a receita de exportação).
Os CST 53 a 56 se referem a créditos vinculados a mais de um tipo de receita. Assim, por exemplo, o CST 56 está relacionado a créditos aos 03 tipos de receitas (grupos 100, 200 e 300), conforme rateio proporcional da receita bruta (com base nos valores informados no registro 0111) ou com base no método da apropriação direta, e assim sucessivamente.
Caso o CST se refira a crédito presumido (60 a 66) o crédito será identificado com os códigos 106, 206 ou 306, quando se tratar de crédito presumido da agroindústria, ou os códigos 107, 207 ou 307, quando se tratar de outras hipóteses de crédito presumido (como no caso da subcontratação de transporte de cargas, pelas empresas de transporte de cargas), conforme o caso.
Dentro dos grupos, a alíquota informada determina se o código será o 101 (alíquotas básicas), 102 (alíquotas diferenciadas), 103 (alíquotas em reais) ou 105 (embalagens para revenda).
Os códigos vinculados à importação (108, 208 e 308) são obtidos através da informação de CFOP iniciado em 3 (quando existente) ou pelo campo IND_ORIG_CRED nos demais casos.
O código 109 (atividade imobiliária) é obtido diretamente dos registros F205 e F210, bem como os códigos relativos ao estoque de abertura (104, 204 e 304), os quais são obtidos diretamente do registro F150 (NAT_BC_CRED = 18).
Campo 03 - Valores válidos: [0, 1]
Campo 04 - Preenchimento: informe o somatório dos Campos “VL_BC_COFINS” de todos os registros Filho “M505”, que detalham a composição da base de cálculo do respectivo crédito.  No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800. Para créditos da atividade imobiliária (COD_CRED = 109), este campo também não deverá ser preenchido, visto que o crédito é recuperado diretamente dos registros F205 e F210 para o campo 08 - VL_CRED. No caso de crédito apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 06 - QUANT_BC_COFINS.
Campo 05 - Preenchimento: informe a alíquota aplicável à base de crédito informada no registro. No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800. Para créditos da atividade imobiliária (COD_CRED = 109), este campo também não deverá ser preenchido, visto que o crédito é recuperado diretamente dos registros F205 e F210 para o campo 08 - VL_CRED. No caso de crédito apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 07 - ALIQ_COFINS_QUANT.
Campo 06 - Preenchimento: informe o somatório dos Campos “QUANT_BC_COFINS” de todos os registros Filho “M505”, que detalham a composição da base de cálculo do respectivo crédito.  No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800. No caso de crédito não apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 04 - VL_BC_COFINS. O preenchimento deste campo só é admitido nos casos de COD_CRED ser 103, 203, 303, 105, 205, 305, 108, 208 e 308.
Campo 07 - Preenchimento: informe a alíquota em reais aplicável à base de crédito informada no registro. No caso de crédito originado em operação de sucessão este campo não deverá ser preenchido, conforme preenchimento do registro F800. No caso de crédito não apurado por unidade de medida de produto, deixe este campo em branco, preenchendo apenas o campo 05 - ALIQ_COFINS. O preenchimento deste campo só é admitido nos casos de COD_CRED ser 103, 203, 303, 105, 205, 305, 108, 208 e 308.
Campo 08 - Preenchimento: informe o valor total do respectivo crédito apurado no período. No caso de crédito apurado pela própria pessoa jurídica, por unidade de medida de produto, o valor deste campo corresponderá à multiplicação dos campos 06 (QUANT_BC_COFINS) e 07 (ALIQ_COFINS_QUANT). Caso contrário deverá ser igual à multiplicação dos campos 04 (VL_BC_CRED) e 05 (ALIQ_COFINS), dividido por 100 (cem).
No caso de crédito da atividade imobiliária (COD_CRED = 109) este campo será recuperado pela soma dos campos VL_CRED_COFINS_DESC do registro F205 e VL_CRED_COFINS_UTIL do registro F210. Nos casos de créditos transferidos por operação de sucessão, este campo será recuperado pelo somatório do campo VL_CRED_COFINS dos registros F800 de mesmo COD_CRED.
Campo 09 - Preenchimento: informar o valor a ser adicionado por ajuste ao crédito do período. O preenchimento deste campo obriga o preenchimento do registro M510, sendo que o valor deve corresponder à soma do campo VL_AJ dos registros M510 onde o campo IND_AJ for igual a 1.
Campo 10 - Preenchimento: informar o valor a ser subtraído por ajuste ao crédito do período. O preenchimento deste campo obriga o preenchimento do registro M510, sendo que o valor deve corresponder à soma do campo VL_AJ dos registros M510 onde o campo IND_AJ for igual a 0.
Campo 11 - Preenchimento: informar o valor dos créditos da não cumulatividade vinculados às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998).
O preenchimento deste campo obriga o preenchimento do registro M630, devendo o somatório dos respectivos campos dos registros M500 ser igual ao somatório dos campos VL_CRED_DIF dos registros M630, para o mesmo COD_CRED.
Validação: O valor deste campo não pode ser maior que VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC.
Campo 12 - Preenchimento: informar o valor total do respectivo crédito disponível relativo ao período, correspondendo à VL_CRED + VL_AJUS_ACRES - VL_AJUS_REDUC - VL_CRED_DIF.
Campo 13 - Valores válidos: [0, 1]
Preenchimento: Preencher com o valor 0, se a totalidade do valor do respectivo crédito disponível no período deve ser utilizada para desconto da contribuição apurada. No caso da apuração ser gerada automaticamente pelo PVA, o aproveitamento do crédito ocorrerá com o da menor disponibilidade (vinculado à receita tributada no mercado interno) para o de maior (vinculado à receita de exportação).
No caso de opção de aproveitamento parcial, o valor parcial do crédito a ser aproveitado para desconto da contribuição apurada deverá ser informado no campo 14 - VL_CRED_DESC. Quando o PVA gera automaticamente a apuração este campo é preenchido automaticamente, com base no valor aproveitado para desconto da contribuição apurada no registro M600.
Campo 14 - Preenchimento: informar o valor do crédito disponível, descontado da contribuição apurada no próprio período, no registro M600. Caso o campo 13 (IND_DESC_CRED) seja preenchido com o valor 0, informar o valor total do Campo 12, caso contrário informar o valor parcial do Campo 12.
Quando o PVA gera automaticamente a apuração este campo é preenchido automaticamente, com base no valor aproveitado para desconto da contribuição apurada no registro M600.
A informação preenchida pela PJ neste campo será sobrescrita pelo PVA quando da geração automática da apuração. Caso necessário, faça os devidos ajustes neste campo (e no campo 13, se for o caso), bem como no respectivo campo do registro M600 (VL_TOT_CRED_DESC).
Campo 15 - Preenchimento: informar o valor do saldo credor para aproveitamento futuro. O valor informado deverá corresponder a  "VL_CRED_DISP" – "VL_CRED_DESC".
<!-- End Registro M500 -->
<!-- Start Registro M505 -->
Registro M505: Detalhamento da Base de Calculo do Crédito Apurado no Período – Cofins
Neste registro será informada a composição da base de cálculo de cada tipo de crédito (M500), conforme as informações constantes nos documentos e operações com CST geradores de créditos, escriturados nos Blocos “A”, “C”, “D” e “F”. Os valores representativos de Bases de Cálculo  escriturados nestes registros serão transferidos para o Registro PAI M500 (Campos 04 e 06), que especifica e escritura os diversos tipos de créditos da escrituração.
ATENÇÃO: Os valores escriturados nos registros M500 (Crédito de Cofins do Período) e M505 (Detalhamento da Base de Cálculo do Crédito de Cofins do Período) serão determinados com base:
Nos valores informados no arquivo elaborado pela própria pessoa jurídica e importado pelo Programa Validador e Assinador da EFD-Contribuições – PVA, os quais serão objeto de validação; ou
Nos valores calculados pelo PVA para os registros M500 e M505, através da funcionalidade “Gerar Apurações”, disponibilizada no PVA, com base nos registros da escrituração constantes nos Blocos “A”, “C”, “D” e “F”.
No caso de operações e documentos informados nos referidos blocos em que os campos “CST_COFINS” se refiram a créditos comuns a mais de um tipo de receitas (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA procederá o cálculo automático do crédito (funcionalidade “Gerar Apurações”) caso a pessoa jurídica tenha optado pelo método de apropriação com base no Rateio Proporcional com base na Receita Bruta (indicador “2” no Campo 03 do Registro 0110), considerando para fins de rateio, no Registro M505, os valores de Receita Bruta informados no Registro 0111.
Desta forma, caso a pessoa jurídica tenha optado pelo método do Rateio Proporcional com base na Receita Bruta (Bruta (indicador “2” no Campo 03 do Registro 0110), o PVA procederá ao cálculo automático do crédito em relação a todos os Códigos de Situação Tributária (CST 50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65 e 66).
Caso a pessoa jurídica tenha optado pelo método de Apropriação Direta (indicador “1” no Campo 03 do Registro 0110) para a determinação dos créditos comuns a mais de um tipo de receita (CST 53, 54, 55, 56, 63, 64, 65 e 66), o PVA não procederá ao cálculo dos créditos (funcionalidade “Gerar Apurações”) relacionados a estes CST, no Registro M505, gerando o cálculo dos créditos apenas em relação aos CST 50, 51, 52, 60, 61 e 62. Neste caso, deve a pessoa jurídica editar os registros M505 correspondentes ao CST representativos de créditos comuns (CST 53, 54, 55, 56, 63, 64, 65 e 66), com base na apropriação direta, inclusive em relação aos custos, por meio de sistema de contabilidade de custos integrada e coordenada com a escrituração, conforme definido no § 8º do art. 3º, da Lei nº 10.833, de 2003.
Na funcionalidade de geração automática de apuração, os valores apurados e preenchidos pelo PVA irão sobrepor (substituir) os valores eventualmente existentes nos referidos campos, constantes na escrituração.
Deve ser escriturado um registro M505 para cada CST recuperado dos registros dos Blocos “A”, “C”, “D” e “F”, vinculado ao tipo de crédito informado no Registro M500.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M505" | C | 004* | - | S |
| 02 | NAT_BC_CRED | Código da Base de Cálculo do Crédito apurado no período, conforme a Tabela 4.3.7. | C | 002* | - | S |
| 03 | CST_COFINS | Código da Situação Tributária referente ao crédito de COFINS (Tabela 4.3.4) vinculado ao tipo de crédito escriturado em M500. | N | 002* | - | S |
| 04 | VL_BC_COFINS_TOT | Valor Total da Base de Cálculo escriturada nos documentos e operações (Blocos “A”, “C”, “D” e “F”), referente ao CST_COFINS informado no Campo 03. | N | - | 02 | N |
| 05 | VL_BC_COFINS_CUM | Parcela do Valor Total da Base de Cálculo informada no Campo 04, vinculada a receitas com incidência cumulativa. Campo de preenchimento específico para a pessoa jurídica sujeita ao regime cumulativo e não-cumulativo da contribuição (COD_INC_TRIB = 3 do Registro 0110) | N | - | 02 | N |
| 06 | VL_BC_COFINS_NC | Valor Total da Base de Cálculo do Crédito, vinculada a receitas com incidência não-cumulativa (Campo 04 – Campo 05). | N | - | 02 | N |
| 07 | VL_BC_COFINS | Valor da Base de Cálculo do Crédito, vinculada ao tipo de Crédito escriturado em M500. - Para os CST_COFINS = “50”, “51”, “52”, “60”, “61” e “62”: Informar o valor do Campo 06 (VL_BC_COFINS_NC); - Para os CST_COFINS = “53”, “54”, “55”, “56”, “63”, “64” “65” e “66” (Crédito sobre operações vinculadas a mais de um tipo de receita): Informar a parcela do valor do Campo 06 (VL_BC_COFINS_NC) vinculada especificamente ao tipo de crédito escriturado em M500.  O valor deste campo será transportado para o Campo 04 (VL_BC_COFINS) do registro M500. | N | - | 02 | N |
| 08 | QUANT_BC_COFINS_TOT | Quantidade Total da Base de Cálculo do Crédito apurado em Unidade de Medida de Produto, escriturada nos documentos e operações (Blocos “A”, “C”, “D” e “F”), referente ao CST_COFINS informado no Campo 03 | N | - | 03 | N |
| 09 | QUANT_BC_COFINS | Parcela da base de cálculo do crédito em quantidade (campo 08) vinculada ao tipo de crédito escriturado em M500. - Para os CST_COFINS = “50”, “51” e “52”: Informar o valor do Campo 08 (QUANT_BC_COFINS); - Para os CST_COFINS = “53”, “54”, “55” e “56” (crédito vinculado a mais de um tipo de receita): Informar a parcela do valor do Campo 08 (QUANT_BC_COFINS) vinculada ao tipo de crédito escriturado em M500.  O valor deste campo será transportado para o Campo 06 (QUANT_BC_COFINS) do registro M500. | N | - | 03 | N |
| 10 | DESC_CRED | Descrição do crédito | C | 060 | - | N |

Observações:
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [M505]
Campo 02 - Preenchimento: Informar neste campo a Natureza da Base de Cálculo do crédito, conforme códigos constantes na Tabela de Base de Cálculo do Crédito (4.3.7), tais como: Aquisição de bens para revenda; aquisição de insumos para produção de bens ou prestação de serviços; despesas com energia elétrica; despesas com aluguéis, encargos de depreciação de bens incorporados ao ativo imobilizado, etc. Será gerado um Registro M505 para cada fato gerador de crédito constante na escrituração.
Campo 03 - Preenchimento: Deve ser informado neste campo 03 o Código da Situação Tributária (CST – conforme Tabela 4.3.4) referente ao crédito de Cofins vinculado ao tipo de crédito escriturado em M500, conforme relação abaixo:
- Crédito Vinculado à Receita Tributada (Grupo 100): CST 50, 53, 54, 56, 60, 63, 64 e 66.
- Crédito Vinculado à Receita Não Tributada (Grupo 200): CST 51, 53, 55, 56, 61, 63, 65 e 66.
- Crédito Vinculado à Receita de Exportação (Grupo 300): CST 52, 54, 55, 56, 62, 64, 65 e 66.
Campo 04 - Preenchimento: Será informado neste campo o valor das bases de cálculo do crédito informadas nos Blocos “A”, “C”, “D” e “F”, correspondente a cada CST recuperado, formando assim, a base de calculo total dos documentos e operações escrituradas no Período.
Campo 05 - Preenchimento: Informar neste campo a parcela da base de cálculo informada no Campo 04, vinculada a receitas de natureza cumulativa.
Este campo deve ser preenchido pela pessoa jurídica que se submeta, no período da escrituração, concomitantemente aos regimes não-cumulativo e cumulativo, ou seja, que no Registro “0110” tenha informado no Campo 02 (COD_INC_TRIB) o indicador “3”.
No caso da pessoa jurídica adotar o método do Rateio Proporcional da Receita Bruta (Registro “0110”), determinar a parcela cumulativa com base na proporção da receita bruta (Receita Bruta Cumulativa / Receita Bruta Total), conforme valores informados no Registro “0111”.
Para a pessoa jurídica que apura a contribuição exclusivamente no regime não-cumulativo, deve informar no Campo 05 o valor “0,00”, ou deixá-lo em branco.
Campo 06 - Preenchimento: Deve ser informado o Valor Total da Base de Cálculo do Crédito, vinculada a receitas com incidência não-cumulativa (Campo 04 – Campo 05). No caso de contribuinte submetido exclusivamente ao regime não-cumulativo, o valor corresponde ao valor informado no campo 04.
Campo 07 - Preenchimento: Será informado neste campo o valor da base de cálculo específica do tipo de crédito escriturado em M500, conforme o CST informado, com base na seguinte regra:
a) Para os CST_COFINS = “50”, “51”, “52”, “60”, “61” e “62”, representativos de operações de créditos vinculados a um único tipo de receita: Informar no Campo 07 o valor do Campo 06 (VL_BC_COFINS_NC);
b) Para os CST_COFINS = “53”, “54”, “55”, “56”, “63”, “64” “65” e “66” (Crédito sobre operações vinculadas a mais de um tipo de receita): Informar a parcela do valor do Campo 06 (VL_BC_COFINS_NC) vinculada especificamente ao tipo de crédito escriturado em M500.
Regras de Apuração das Bases de Cálculo para os CST = 53, 54, 55, 56, 63, 64, 65 e 66:
1. Caso a pessoa jurídica determine o crédito, sobre operações comuns a mais de um tipo de receita, pelo método da Apropriação Direta (conforme indicado no Registro “0110”), informar neste campo 07 o valor da base de cálculo do crédito a que se refere o Registro PAI M500;
2. Caso a pessoa jurídica determine o crédito, sobre operações comuns a mais de um tipo de receita, pelo método do Rateio Proporcional da Receita Bruta (conforme indicado no Registro “0110”), informar neste campo 07 o valor da base de cálculo do crédito a que se refere o Registro PAI M500, conforme abaixo, considerando as Receitas Brutas informadas no Registro “0111”:
2.1) No caso de CST 53 e 63 (crédito vinculado a Receitas Tributadas e a Receitas Não Tributadas no Mercado Interno):
- M500 Correspondente a Crédito vinculado à Receita Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada);
- M500 Correspondente a Crédito vinculado à Receita Não Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Não Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada).
2.2) No caso de CST 54 e 64 (crédito vinculado a Receitas Tributadas no Mercado Interno e a Receitas de Exportação):
- M500 Correspondente a Crédito vinculado à Receita Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Tributada / (Receita Bruta Tributada + Receita de Exportação);
- M500 Correspondente a Crédito vinculado à Receita de Exportação: Campo 07 = Valor do Campo 06 x Receita Bruta de Exportação / (Receita Bruta Tributada + Receita Bruta de Exportação).
2.3) No caso de CST 55 e 65 (crédito vinculado a Receitas Não Tributadas e a Receitas de Exportação):
- M500 Correspondente a Crédito vinculado à Receita Não Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Não Tributada / (Receita Bruta Não Tributada + Receita Bruta de Exportação);
- M500 Correspondente a Crédito vinculado à Receita de Exportação: Campo 07 = Valor do Campo 06 x Receita Bruta de Exportação / (Receita Bruta Não Tributada + Receita Bruta de Exportação).
2.4) No caso de CST 56 e 66 (crédito vinculado a Receitas Tributadas, Receitas Não Tributadas no Mercado Interno e de Exportação):
- M500 Correspondente a Crédito vinculado à Receita Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada + Receita Bruta de Exportação);
- M500 Correspondente a Crédito vinculado à Receita Não Tributada no Mercado Interno: Campo 07 = Valor do Campo 06 x Receita Bruta Não Tributada / (Receita Bruta Tributada + Receita Bruta Não Tributada + Receita Bruta de Exportação).
- M500 Correspondente a Crédito vinculado à Receita de Exportação: Campo 07 = Valor do Campo 06 x Receita Bruta de Exportação / (Receita Bruta Tributada + Receita Bruta Não Tributada + Receita Bruta de Exportação).
Exemplo:
Considerando que a pessoa jurídica tenha escriturado em registros do Bloco C (C170 ou C191) insumos para industrialização (CFOP 1101) com direito a crédito, vinculados a receitas tributadas, não tributadas e da exportação (CST 56), nos valores de R$ R$ 350.800,00 (insumo A), R$ 210.000,00 (insumo B) e R$ 439.200,00 (insumo C);
Considerando que a pessoa jurídica tenha optado pelo método do Rateio Proporcional com base na Receita Bruta para a determinação do crédito (Registro 0110, Campo 03, indicador “2”) e informado os valores abaixo de Receita Bruta no Registro 0111:

| Valor da Receita Bruta | Natureza da Receita Bruta | Percentual |
| --- | --- | --- |
| 1.250.000,00 | Não Cumulativa – Tributada no MI | 50% |
| 500.000,00 | Não Cumulativa – Não Tributada no MI | 20% |
| 250.000,00 | Não Cumulativa – Exportação | 10% |
| 500.000,00 | Cumulativa | 20% |
| 2.500.000,00 | T O T A L | 100% |

Os valores a serem escriturados nos registros filhos M505, vinculados a cada código de crédito (COD_CRED)  relacionados nos registros pais M500, com base nas informações escrituradas nos Blocos “0” e “C”, corresponderão:
I – Registro M505 (registro filho de M500, com Campo “COD_CRED” = 101)

| Campo 01 REG | Campo 02 NAT_BC_CRED | Campo 03 CST_COFINS | Campo 04 VL_BC_COFINS_TOT | Campo 05 VL_BC_COFINS_CUM | Campo 06 VL_BC_COFINS_NC | Campo 07 VL_BC_COFINS |
| --- | --- | --- | --- | --- | --- | --- |
| M505 | 02 | 56 | 1.000.000,00 | 200.000,00 | 800.000,00 | 500.000,00 |

Representação Gráfica dos registros M505 (base de cálculo do crédito) e M500 (crédito apurado – COD_CRED 101):
|M500|101|0|500000|7,6|0||38000|0|0|0|38000|1|22834,2|15165,8|
|M505|02|56|1000000|200000|800000|500000||0||
II – Registro M505 (registro filho de M500, com Campo “COD_CRED” = 201)

| Campo 01 REG | Campo 02 NAT_BC_CRED | Campo 03 CST_COFINS | Campo 04 VL_BC_COFINS_TOT | Campo 05 VL_BC_COFINS_CUM | Campo 06 VL_BC_COFINS_NC | Campo 07 VL_BC_COFINS |
| --- | --- | --- | --- | --- | --- | --- |
| M505 | 02 | 56 | 1.000.000,00 | 200.000,00 | 800.000,00 | 200.000,00 |

Representação Gráfica dos registros M505 (base de cálculo do crédito) e M500 (crédito apurado – COD_CRED 201):
|M500|201|0|200000|7,6|0||15200|0|0|0|15200|1|0|15200|
|M505|02|56|1000000|200000|800000|200000||0||
III – Registro M505 (registro filho de 500, com Campo “COD_CRED” = 301)

| Campo 01 REG | Campo 02 NAT_BC_CRED | Campo 03 CST_COFINS | Campo 04 VL_BC_COFINS_TOT | Campo 05 VL_BC_COFINS_CUM | Campo 06 VL_BC_COFINS_NC | Campo 07 VL_BC_COFINS |
| --- | --- | --- | --- | --- | --- | --- |
| M505 | 02 | 56 | 1.000.000,00 | 200.000,00 | 800.000,00 | 100.000,00 |

Representação Gráfica dos registros M505 (base de cálculo do crédito) e M500 (crédito apurado – COD_CRED 301):
|M500|301|0|100000|7,6|0||7600|0|0|0|7600|1|0|7600|
|M505|02|56|1000000|200000|800000|100000||0||
Campos 08 e 09 - Preenchimento: Campos específicos para as pessoas jurídicas que apuram crédito por Unidade de Medida de Produto (fabricantes/importadores de Combustíveis, Bebidas Frias ou Embalagens para Bebidas).
O crédito será determinado em quantidade quando o tipo de crédito do registro M500 corresponder a 103, 203 ou 303. . O preenchimento destes campos também poderá ocorrer nos tipos de crédito 105, 205, 305 e 108, 208 e 308.
No caso de operações geradoras de créditos vinculados a mais de um tipo de receita (CST 53 a 56 e 63 a 66) deve a pessoa jurídica preencher 2 registros M505 (no caso de CST 53, 54, 55, 63, 64 e 65) ou 3 registros M505 ( no caso de CST 56 e 66), um para cada tipo de receita a qual o crédito está vinculado.
Campo 10 - Preenchimento: Neste campo poderá a pessoa jurídica proceder à descrição do crédito, para fins de detalhamento ou esclarecimento da natureza da base de cálculo do crédito escriturado.
Validação: Quando o Campo NAT_BC_CRED = 13, este campo é de preenchimento obrigatório.
<!-- End Registro M505 -->
<!-- Start Registro M510 -->
Registro M510: Ajustes do Crédito de Cofins Apurado
Registro a ser preenchido caso a pessoa jurídica tenha de proceder a ajustes de créditos escriturados no período, decorrentes de ação judicial, de processo de consulta, da legislação tributária das contribuições sociais, de estorno ou de outras situações.
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas nos campos 09 e 10 do registro pai M500.
Deve ser informado neste registro, como ajuste de redução (Indicador “0”) o valor referente às devoluções de compras ocorridas no período, de bens e mercadorias sujeitas à incidência não cumulativa da Contribuição que, quando da aquisição gerou a apuração de créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M510" | C | 004* | - | S |
| 02 | IND_AJ | Indicador do tipo de ajuste: 0- Ajuste de redução; 1- Ajuste de acréscimo. | C | 001* | - | S |
| 03 | VL_AJ | Valor do ajuste | N | - | 02 | S |
| 04 | COD_AJ | Código do ajuste, conforme a Tabela indicada no item 4.3.8. | C | 002* |   | S |
| 05 | NUM_DOC | Número do processo, documento ou ato concessório ao qual o ajuste está vinculado, se houver. | C | - | - | N |
| 06 | DESCR_AJ | Descrição resumida do ajuste. | C | - | - | N |
| 07 | DT_REF | Data de referência do ajuste (ddmmaaaa) | N | 008* | - | N |

Observações: Registro a ser preenchido caso a pessoa jurídica tenha de proceder a ajustes de créditos escriturados no período, decorrentes de ação judicial, de processo de consulta, da legislação tributária das contribuições sociais, de estorno ou de outras situações, deverá proceder à escrituração deste registro
Nível hierárquico - 3
Ocorrência – 1:N (por tipo de crédito – M500)
Campo 01 - Valor Válido: [M510]
Campo 02 - Valores Válidos: [0, 1]
Campo 03 - Preenchimento: informar o valor do ajuste de redução ou de acréscimo. A soma de todos os valores deste campo, representando ajustes de acréscimo (IND_AJ = 1) deverá ser transportada para o campo 09 (VL_AJUS_ACRES) do registro M500. Por sua vez, a soma de todos os valores deste campo, representando ajustes de redução (IND_AJ = 0) deverá ser transportada para o campo 10 (VL_AJUS_REDUC) do registro M500.
Campo 04 - Preenchimento: informar o código do ajuste, conforme Tabela 4.3.8 - “Tabela Código de Ajustes de Contribuição ou Créditos”, referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informar, se for o caso, o número do processo, documento ou ato concessório ao qual o ajuste está vinculado.
No caso de ajuste que envolva grande quantidade de documentos, pode o registro ser escriturado consolidando as informações dos documentos, descrevendo no campo 06 (tipo de documento fiscal consolidado, quantidades de documentos, emitente/beneficiário, por exemplo).
Campo 06 - Preenchimento: informar a descrição resumida do ajuste que está sendo lançada no respectivo registro.
Campo 07 - Preenchimento: informar, se for o caso, a data de referência do ajuste, no formato "ddmmaaaa", excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
<!-- End Registro M510 -->
<!-- Start Registro M515 -->
Registro M515: Detalhamento dos Ajustes do Crédito de Cofins Apurado
Registro a ser preenchido para a pessoa jurídica detalhar a operação e valor a que se refere o ajuste de crédito informado no registro pai – M510.
Registro não disponível para os fatos geradores até 30/09/2015. Para os fatos geradores a partir de 01/10/2015 a versão 2.12 do Programa da EFD-Contribuições (PVA) disponibiliza este registro de detalhamento dos ajustes de créditos da Cofins, o qual deve ser preenchido, para que seja demonstrado e detalhado à Receita Federal quais as operações realizadas que ensejaram os ajustes informados no registro M510.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M515” | C | 004* | - | S |
| 02 | DET_VALOR_AJ | Detalhamento do valor do crédito reduzido ou acrescido, informado no Campo 03 (VL_AJ) do registro M510. | N | - | 02 | S |
| 03 | CST_COFINS | Código de Situação Tributária referente à operação detalhada neste registro. | N | 002* | - | N |
| 04 | DET_BC_CRED | Detalhamento da base de cálculo geradora de ajuste de crédito | N | - | 03 | N |
| 05 | DET_ALIQ | Detalhamento da alíquota a que se refere o ajuste de crédito | N | 08 | 04 | N |
| 06 | DT_OPER_AJ | Data da operação a que se refere o ajuste informado neste registro. | N | 008* | - | S |
| 07 | DESC_AJ | Descrição da(s) operação(ões) a que se refere o valor informado no Campo 02 (DET_VALOR_AJ) | C | - | - | N |
| 08 | COD_CTA | Código da conta contábil debitada/creditada | C | 255 | - | N |
| 09 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
Nível hierárquico – 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [M515]
Campo 02 - Preenchimento: Informar o detalhamento do valor da operação a que se refere o ajuste de crédito informado no Campo 03 (VL_AJ) do registro M510.
Caso o ajuste em M510 se refira a várias operações ou situações, devem ser gerados os registros de detalhamento M515 que se mostrem necessários e suficientes, para demonstrar o valor total do ajuste escriturado em M510.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao ajuste de crédito de PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 04 - Preenchimento: Informar a base de cálculo do ajuste de crédito a que se refere este registro.
Campo 05 - Preenchimento: Informar a alíquota a que se refere o ajuste de crédito informado neste registro.
Campo 06 - Preenchimento: Informar a data da operação a que se refere o ajuste de crédito detalhado neste registro.
Campo 07 - Preenchimento: Informar a descrição da(s) operação(ões) a que se refere o ajuste detalhado neste registro.
Campo 08 - Preenchimento: Informar, sendo o caso, o código da conta contábil a que se refere o ajuste detalhado neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 09 - Preenchimento: Campo para prestação de outras informações que se mostrem necessárias ou adequadas, para esclarecer ou justificar o ajuste.
<!-- End Registro M515 -->
<!-- Start Registro M600 -->
Registro M600:  Consolidação da Contribuição para a Seguridade Social - Cofins do Período
Neste registro serão consolidadas as contribuições sociais apuradas no período da escrituração, nos regimes não-cumulativo e cumulativo, bem como procedido ao desconto dos créditos não cumulativos apurados no próprio período, dos créditos apurados em períodos anteriores, dos valores retidos na fonte e de outras deduções previstas em lei, demonstrando em seu final os valores devidos a recolher.
ATENÇÃO: Os valores referentes às contribuições sociais escriturados nos Campos 02 e 09 do Registro M600 serão gerados com base:
Nos valores informados no arquivo elaborado pela própria pessoa jurídica e importado pelo Programa Validador e Assinador da EFD-Contribuições – PVA, os quais serão objeto de validação; ou
Nos valores das contribuições calculados pelo PVA no Registro M610 (Detalhamento da Cofins no Período), no Campo 13 (VL_CONT_PER), através da funcionalidade “Gerar Apurações”, disponibilizada no PVA, com base nos registros de escrituração de receitas constantes nos Blocos “A”, “C”, “D” e “F”.
A geração automática de apuração (funcionalidade “Gerar Apurações” (Ctrl+M)) o PVA apura, em relação ao Registro M600, apenas os valores dos campos de contribuições (Campos 02 e 09) e de créditos a descontar (Campos 03 e 04). Os campos representativos de retenções na fonte (Campos 06 e 10) e de outras deduções (07 e 11) não serão recuperados na geração automática de apuração, devendo sempre ser informados pela própria pessoa jurídica no arquivo importado pelo PVA ou complementado pela edição (digitação no próprio PVA) no registro M600, dos respectivos valores de retenção na fonte escriturados nos registros F600, 1300 (PIS) ou 1700 (Cofins), e de deduções, escriturados no registro F700.
Na funcionalidade de geração automática de apuração, os valores apurados e preenchidos pelo PVA para os Campos 02 e 09 (contribuições apuradas) e para os Campos 03 e 04 (créditos descontados) irão sobrepor (substituir) os valores eventualmente existentes nos referidos campos, constantes na escrituração.
No caso de totalização de contribuição não cumulativa do período no campo 02, mas que a legislação não permita o desconto de créditos, aproveitamento de retenções na fonte e de outras deduções, deverá a pessoa jurídica realizar os devidos ajustes nos registros de apuração de crédito (campo 14 do registro M100 ou campo 13 do registro 1100) e dos respectivos aproveitamentos neste registro (campos 03, 04, 06 e 07).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M600" | C | 004* | - | S |
| 02 | VL_TOT_CONT_NC_PER | Valor Total da Contribuição Não Cumulativa do Período (recuperado do campo 13 do Registro M610, quando o campo “COD_CONT” = 01, 02, 03, 04, 32 e 71) | N | - | 02 | S |
| 03 | VL_TOT_CRED_DESC | Valor do Crédito Descontado, Apurado no Próprio Período da Escrituração (recuperado do campo 14 do Registro M500) | N | - | 02 | S |
| 04 | VL_TOT_CRED_DESC_ANT | Valor do Crédito Descontado, Apurado em Período de Apuração Anterior (recuperado do campo 13 do Registro 1500) | N | - | 02 | S |
| 05 | VL_TOT_CONT_NC_DEV | Valor Total da Contribuição Não Cumulativa Devida (02 - 03 - 04) | N | - | 02 | S |
| 06 | VL_RET_NC | Valor Retido na Fonte Deduzido no Período | N | - | 02 | S |
| 07 | VL_OUT_DED_NC | Outras Deduções no Período | N | - | 02 | S |
| 08 | VL_CONT_NC_REC | Valor da Contribuição Não Cumulativa a Recolher/Pagar (05 - 06 - 07) | N | - | 02 | S |
| 09 | VL_TOT_CONT_CUM_PER | Valor Total da Contribuição Cumulativa do Período (recuperado do campo 13 do Registro M610, quando o campo “COD_CONT” = 31, 32, 51, 52, 53, 54 e 72) | N | - | 02 | S |
| 10 | VL_RET_CUM | Valor Retido na Fonte Deduzido no Período | N | - | 02 | S |
| 11 | VL_OUT_DED_CUM | Outras Deduções no Período | N | - | 02 | S |
| 12 | VL_CONT_CUM_REC | Valor da Contribuição Cumulativa a Recolher/Pagar (09 - 10 - 11) | N | - | 02 | S |
| 13 | VL_TOT_CONT_REC | Valor Total da Contribuição a Recolher/Pagar no Período (08 + 12) | N | - | 02 | S |

Observações:
1. Os valores referentes às contribuições sociais não-cumulativas, informados no campo 02  “VL_TOT_CONT_NC_PER”, serão determinados e recuperados do Campo 13  “VL_CONT_PER” dos Registros Filho “M610”.
2. Os valores referentes aos créditos a descontar informados no campo 03  “VL_TOT_CRED_DESC”, serão determinados e recuperados do Campo 14 “VL_CRED_DESC” dos Registros Filho “M500”.
3. Os valores referentes às contribuições sociais cumulativas, informados no campo 09  “VL_TOT_CONT_CUM_PER”, serão determinados e recuperados do Campo 13  “VL_CONT_PER” dos Registros Filho “M610”.
4. Os valores retidos na fonte no período da escrituração, relacionados nos Campos 06 e 10, devem guardar correlação com os valores informados no Campo 10 “VL_RET_COFINS” do Registro “F600”.
Nível hierárquico – 2
Ocorrência – Um (por arquivo)
Campo 01 - Valor Válido: [M600]
Campo 02 - Preenchimento: informar o valor total da contribuição não cumulativa do período, correspondendo à soma do campo 13 (VL_CONT_PER) do registro M610, quando o valor do campo “COD_CONT” for igual a 01, 02, 03, 04, 32 (neste caso quando a pessoa jurídica estiver sujeita a não cumulatividade, exclusivamente ou não) ou 71.  No caso da pessoa jurídica sujeitar-se exclusivamente ao regime cumulativo da contribuição, o valor do campo deverá ser igual a 0.
Campo 03 - Preenchimento: informar o valor do crédito descontado, apurado no próprio período da escrituração, correspondendo ao somatório do campo 14 (VL_CRED_DESC) dos diversos registros M500. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Validação: O somatório dos campos VL_TOT_CRED_DESC e VL_TOT_CRED_DESC_ANT deve ser menor ou igual ao valor do campo VL_TOT_CONT_NC_PER.
Campo 04 - Preenchimento: informar o valor do crédito descontado, apurado em período de apuração anterior, correspondendo ao somatório do campo 13 (VL_CRED_DESC_EFD), dos diversos registros 1500.
Na geração automática da apuração pela PVA, este campo será preenchido automaticamente com o somatório do campo 13 dos registros 1500. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Validação: O somatório dos campos VL_TOT_CRED_DESC e VL_TOT_CRED_DESC_ANT deve ser menor ou igual ao valor do campo VL_TOT_CONT_NC_PER.
OBS: Tendo a pessoa jurídica apurado em um determinado mês um débito de R$ 500,00 e um crédito de R$ 400,00, não querendo utilizar como desconto os próprios R$ 400,00 apurados no período mas sim, R$ 400,00 de créditos de períodos anteriores, deve assim proceder na EFD-Contribuições:
Registro M500:
Campo 08 ==> 400,00
Campo 12 ==> 400,00
Campo 13 ==> "1"
Campo 14 ==> 100,00
Campo 15 ==> 300,00
Registro M600:
Campo 02 ==> 500,00
Campo 03 ==> 100,00
Campo 04 ==> 400,00
Campo 05 ==> 0
Registro 1500:
Campo 02 ==> xx/yyyy (período anterior ao da escrituração)
Campo 06 ==> 2.000,00
Campo 08 ==> 2.000,00
Campo 13 ==> 400,00
Campo 18 ==> 1.600,00
Campo 05 - Preenchimento: informar o valor total da contribuição não cumulativa devida, correspondendo a VL_TOT_CONT_NC_PER - VL_TOT_CRED_DESC - VL_TOT_CRED_DESC_ANT.
Campo 06 - Preenchimento: informar o valor na fonte deduzido do valor da contribuição não cumulativa devida no período. Caso a retenção na fonte tenha ocorrido no próprio período da escrituração, ela deverá estar detalhada no registro F600 e também no registro 1700, caso exista valor a utilizar em períodos futuros. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
O valor a ser informado no Campo 06 deve ser igual ou menor que o valor constante no campo 05.
Campo 07 - Preenchimento: informar o valor de outras deduções do valor da contribuição não cumulativa devida no período, correspondendo ao somatório do campo VL_DED_COFINS dos registros F700 quando IND_NAT_DED = 0 (dedução de natureza não cumulativa). No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 08 - Preenchimento: informar o valor da contribuição não cumulativa a recolher/pagar no período da escrituração, correspondendo a VL_TOT_CONT_NC_DEV - VL_RET_NC - VL_OUT_DED_NC. No caso da pessoa jurídica estar sujeita exclusivamente ao regime cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 09 - Preenchimento: informar o valor total da contribuição cumulativa do período, correspondendo à soma do campo 13 (VL_CONT_PER) do registro M610, quando o valor do campo “COD_CONT” for igual a 31, 32 (neste caso quando a pessoa jurídica estiver sujeita exclusivamente ao regime cumulativo),  51, 52, 53, 54 ou 72.  No caso da pessoa jurídica estar sujeita exclusivamente ao regime não cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 10 - Preenchimento: informar o valor na fonte deduzido do valor da contribuição cumulativa devida no período. Caso a retenção na fonte tenha ocorrido no próprio período da escrituração, ela deverá estar detalhada no registro F600 e também no registro 1700, caso exista valor a utilizar em períodos futuros. No caso da pessoa jurídica estar sujeita exclusivamente ao regime não cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
O valor a ser informado no Campo 10 deve ser igual ou menor que o valor constante no campo 09.
Campo 11 - Preenchimento: informar o valor de outras deduções do valor da contribuição cumulativa devida no período, correspondendo, no máximo, ao somatório do campo VL_DED_COFINS dos registros F700 quando IND_NAT_DED = 1 (dedução de natureza cumulativa). No caso da pessoa jurídica estar sujeita exclusivamente ao regime não cumulativo da contribuição, o valor deste campo deverá ser igual a 0.
Campo 12 - Preenchimento: informar o valor da contribuição cumulativa a recolher/pagar no período da escrituração, correspondendo a VL_TOT_CONT_CUM_PER - VL_RET_CUM - VL_OUT_DED_CUM.
Campo 13 - Preenchimento: informar o valor total da contribuição a recolher/pagar no período da escrituração, correspondendo a "VL_CONT_NC_REC" + "VL_CONT_CUM_REC".
<!-- End Registro M600 -->
<!-- Start Registro M605 -->
Registro M605: Cofins a Recolher – Detalhamento por Código de Receita
Neste registro será informado, por código de receita (conforme códigos de débitos informados em DCTF), o detalhamento da contribuição a recolher informada nos campos 08 (regime não cumulativo) e 12 (regime cumulativo) do Registro Pai M600.
Atenção:
1. O código a ser informado no campo 03 (COD_REC) não é o código que consta no DARF (composto de quatro números), mas sim, o código identificador da contribuição na Ficha “Débitos” da DCTF (composto de seis números).
2. O somatório dos valores informados no campo 04 (VL_DEBITO) informado neste registro, deve corresponder ao valor constante de contribuição a recolher, do Registro Pai M600.
Referido registro deverá ser preenchido a partir do período de apuração de janeiro de 2014, utilizando a versão 2.06 do Programa da EFD-Contribuições (PVA). De preenchimento opcional no período de janeiro a março de 2014, e de preenchimento obrigatório a partir do período de apuração abril de 2014.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M605" | C | 004* | - | S |
| 02 | NUM_CAMPO | Informar o número do campo do registro “M600” (Campo 08 (contribuição não cumulativa) ou Campo 12 (contribuição cumulativa)), objeto de detalhamento neste registro. | C | 002* | - | S |
| 03 | COD_REC | Informar o código da receita referente à contribuição a recolher, detalhada neste registro. | C | 006* | - | S |
| 04 | VL_DEBITO | Valor do Débito correspondente ao código do Campo 03, conforme informação na DCTF. | N | - | 02 | S |

Observações: Registro de preenchimento obrigatório a partir do período de apuração referente a abril de 2014
Nível hierárquico – 3
Ocorrência – Vários por arquivo.
Campo 01 - Valor Válido: [M605]
Campo 02 - Preenchimento: Informar o número do campo do registro “M600” (Campo 08 (contribuição não cumulativa) ou Campo 12 (contribuição cumulativa)), objeto de detalhamento neste registro.
Campo 03 - Preenchimento: informar o código de débito referente a Cofins, conforme os códigos de receitas informados na Ficha “Débitos” da DCTF, composto de 06 (seis) números, conforme referenciado no Ato Declaratório Executivo Codac/RFB nº 36, de 2014.

| Ato Declaratório Executivo Codac nº 36, de 22 de outubro de 2014 O COORDENADOR-GERAL DE ARRECADAÇÃO E COBRANÇA, no uso das atribuições que lhe confere o inciso III do art. 312 do Regimento Interno da Secretaria da Receita Federal do Brasil, aprovado pela Portaria MF nº 203, de 14 de maio de 2012, e tendo em vista o disposto na Instrução Normativa RFB nº 1.110, de 24 de dezembro de 2010, declara: Art. 1ºAs extensões dos códigos de receita a serem utilizadas na Declaração de Débitos e Créditos Tributários Federais (DCTF) serão divulgadas no sítio da Secretaria da Receita Federal do Brasil (RFB) na Internet, no endereço http://www.receita.fazenda.gov.br . Parágrafo único. As extensões divulgadas na forma do caput e não relacionadas na tabela do programa gerador da DCTF deverão ser incluídas na referida tabela mediante a utilização da opção “Manutenção da Tabela de Códigos” do menu “Ferramentas” nos grupos respectivos. Art. 2ºEste Ato Declaratório Executivo entra em vigor na data de sua publicação no Diário Oficial da União. Art. 3ºFica revogado o Ato Declaratório Executivo Codac nº 99, de 29 de dezembro de 2011 JOÃO PAULO R. F. MARTINS DA SILVA |
| --- |

Campo 04 - Preenchimento: informar o valor do débito correspondente ao código de receita constante no Campo 03.
<!-- End Registro M605 -->
<!-- Start Registro M610 -->
Registro M610: Detalhamento da Contribuição para a Seguridade Social - Cofins do Período
Será gerado um Registro “M610” para cada situação geradora contribuição social, especificada na Tabela “4.3.5 – Código de Contribuição Social Apurada”, recuperando os valores referentes às diversas bases de cálculo escriturados nos registros dos Blocos “A”, “C”, “D” e “F”.
Caso sejam recuperados registros dos Blocos “A”, “C”, “D” ou “F” referentes a uma mesma situação com incidência de contribuição social (conforme Tabela 4.3.5), mas sujeitas a mais de uma alíquota de apuração, deve ser escriturado um Registro “M610” em relação a cada alíquota existente na escrituração. Dessa forma a chave do registro é formada pelos campos “COD_CONT” + “ALIQ_COFINS_QUANT” + “ALIQ_COFINS”.
Conforme item “4. Procedimentos de escrituração na revenda de bens sujeitos à substituição tributária de PIS/COFINS”, até a versão 2.0.4a e anteriores do PGE, documentos escriturados com CST 05 e alíquota zero eram totalizados nos registros M400 e M800. A partir da versão 2.0.5 do PGE, todas as operações com CST 05 devem ser totalizadas nos registros M210 e M610.
Para os períodos de apuração até dezembro de 2013, no caso de apuração da Cofins (cumulativa ou não cumulativa) incidente sobre receitas específicas de sociedade em conta de participação (SCP), da qual a pessoa jurídica titular da escrituração seja sócia ostensiva,  deve ser escriturada em registro M610 específico e separado da contribuição incidente sobre as demais receitas, informando no Campo 02 o código de tipo de contribuição “71” ou “72”, conforme o regime de tributação a que está submetida a SCP.
A funcionalidade de apuração automática de contribuição e crédito pelo próprio PVA da EFD-Contribuições (opção “Gerar Apurações” (Ctrl+M), do PVA), não apura contribuições específica de SCP, face a impossibilidade de sua identificação em cada documento/operação escriturados nos Blocos A, C, D ou F. Assim, a demonstração da contribuição vinculada a SCP, em M610, deverá sempre ser efetuada pela própria pessoa jurídica, conforme procedimentos abaixo:
Procedimento 1 – Destaque dos valores referentes à(s) SCP:
Primeiramente, deve ser reduzido dos valores totais de débitos (M610) e créditos (M500) apurados de forma consolidada na empresa, sócia ostensiva, os valores referentes a cada SCP. Para tanto, informar o valor do crédito (em M500, campo 10 e gerando um registro de ajuste de redução em M510 para cada SCP) e o valor do débito (em M610, campo 10 e gerando um registro de ajuste de redução em M620 para cada SCP), segregando assim os valores referentes à sócia ostensiva, dos valores referentes à(s) SCP.
Procedimento 2 – Registros dos valores referentes à(s) SCP:
Em seguida, gerar novos registros M610 (Contribuições) para a demonstração dos créditos e débitos apurados no período, de cada SCP da qual seja sócia ostensiva, com os códigos específicos de contribuição de SCP (71 ou 72),  gerando também os correspondentes registros de ajuste de acréscimo de contribuições, em M620.
Para identificação das SCPs poderão ser utilizados os registros de conta contábil informados em 0500.
Para os períodos de apuração a partir de janeiro de 2014, no caso de apuração da contribuição para o PIS/Pasep (cumulativa ou não cumulativa) incidente sobre receitas específicas de sociedade em conta de participação (SCP), da qual a pessoa jurídica titular da escrituração seja sócia ostensiva, deve ser escriturada uma EFD-Contribuições para cada SCP, sendo cada SCP identificada na EFD-Contribuições da pessoa jurídica sócia ostensiva no Registro "0035 - Identificação das SCP".
Leiaute do Registro M610 aplicável aos Fatos Geradores ocorridos até 31 de dezembro de 2018:

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M610" | C | 004* | - | S |
| 02 | COD_CONT | Código da contribuição social apurada no período, conforme a Tabela 4.3.5. | C | 002 | - | S |
| 03 | VL_REC_BRT | Valor da Receita Bruta | N | - | 02 | S |
| 04 | VL_BC_CONT | Valor da Base de Cálculo da Contribuição | N | - | 02 | S |
| 05 | ALIQ_COFINS | Alíquota do COFINS (em percentual) | N | 008 | 04 | N |
| 06 | QUANT_BC_COFINS | Quantidade – Base de cálculo COFINS | N | - | 03 | N |
| 07 | ALIQ_COFINS_QUANT | Alíquota do COFINS (em reais) | N | - | 04 | N |
| 08 | VL_CONT_APUR | Valor total da contribuição social apurada | N | - | 02 | S |
| 09 | VL_AJUS_ACRES | Valor total dos ajustes de acréscimo | N | - | 02 | S |
| 10 | VL_AJUS_REDUC | Valor total dos ajustes de redução | N | - | 02 | S |
| 11 | VL_CONT_DIFER | Valor da contribuição a diferir no período | N | - | 02 | N |
| 12 | VL_CONT_DIFER_ANT | Valor da contribuição diferida em períodos anteriores | N | - | 02 | N |
| 13 | VL_CONT_PER | Valor Total da Contribuição do Período (08 + 09 – 10 – 11 +12) | N | - | 02 | S |

Observações:
1. Os valores representativos de Bases de Cálculo da contribuição, demonstrados no Campo 04 “VL_BC_CONT” (base de cálculo referente a receitas auferidas) do Registro “M610”, são recuperados do Campo “VL_BC_PIS” dos diversos registros dos Blocos “A”, “C”, “D” ou “F” que contenham o mesmo CST.
2. Os valores representativos de Bases de Cálculo da contribuição em quantidade, demonstrados no Campo 06 “QUANT_BC_PIS” (base de cálculo referente a quantidades vendidas) do Registro “M610”, são recuperados do Campo “QUANT_BC_PIS” dos registros do Bloco “C” que contenham o mesmo CST.
3. Deve existir ao menos um registro M610 de apuração de contribuição a alíquotas específicas (diferenciadas ou por unidade de medida de produto), com o Campo “COD_CONT” igual a 02 ou 03 (regime não-cumulativo) ou 52 ou 53 (regime cumulativo) se o Campo “COD_TIPO_CONT” do Registro 0110 for igual a 2.
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [M610]
Campo 02 - Preenchimento: informe o código da contribuição social que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>. Quando a apuração é gerada automaticamente pelo PVA, o campo é obtido através das seguintes combinações:

| Campo COD_CONT do Registro M610 | Descrição do COD_CONT | CST_COFINS | Campo COD_INC_TRIB do Registro 0110 | Alíquota da COFINS (em percentual) (ALIQ_COFINS) | Alíquota da COFINS (em reais) (ALIQ_COFINS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 1 | 7,6(COFINS) | - |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 3 | 7,6(COFINS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 2 | 3,0(COFINS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 3 | 3,0(COFINS) | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 1 | - | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 3 | - | - |
| 52 | Contribuição cumulativa apurada a alíquotas diferenciadas | 02 | 2 | - | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 1 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 1 | > 0 | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 3 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 3 | > 0 | - |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03 | 2 | - | > 0 |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03* | 2 | > 0 | - |
| 31 | Contribuição apurada por substituição tributária | 05 | - | 3,0(COFINS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | Diferente de 0, 3,0(COFINS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | - | >0 |

Tabela para apuração dos registros M610 – F200 (Item exclusivo para informações obtidas dos registros F200)

| Campo COD_CONT do Registro M610 | Descrição do COD_CONT | CST_COFINS | Campo COD_INC_TRIB do Registro 0110 | Alíquota do COFINS (em percentual) (ALIQ_COFINS) | Alíquota do COFINS (em reais) (ALIQ_COFINS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 1 | 7,6 | - |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 7,6 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 2 | 3,0 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 3,0 | - |

O PVA não validará e não gerará automaticamente registros M610 com COD_CONT igual a 71 (Contribuição apurada de SCP – Incidência Não Cumulativa), 72 (Contribuição apurada de SCP – Incidência Cumulativa) e 99 (Contribuição para o PIS/Pasep – Folha de Salários – Vide registro M350).
Campo 03 - Preenchimento: informar o valor da receita bruta auferida no período, vinculada ao respectivo COD_CONT.
Validação: Quando o valor do campo 02 (COD_CONT) for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual à soma dos seguintes campos (quando o CST da operação vinculada for 01, 02, 03, 04, 05 com alíquota diferente de zero):
VL_ITEM dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_ITEM dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_ITEM dos registros C185 e C495, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_ITEM dos registros C485, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_ITEM dos registros C385, C605, C870, C880, D205, D605
VL_DOC dos registros D300,
VL_BRT do registro D350,
VL_OPR do registro C175,
VL_OPER do registro F100, cujo valor do campo IND_OPER seja igual a “1” ou “2”,
VL_TOT_REC do registro F200,
VL_REC_CAIXA do registro F500 e F510,
VL_REC_COMP do registro F550 e F560,
VL_REC do registro I100.
Campo 04 - Preenchimento: informar o valor da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro.
Validação: Quando a natureza da pessoa jurídica (IND_NAT_PJ do registro “0000” igual a 00, 02, 03 ou 05) não for sociedade cooperativa e o valor do campo COD_CONT for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual a:
VL_BC_COFINS dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_BC_COFINS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_BC_COFINS dos registros C185 e C495, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_BC_COFINS dos registros C485, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_BC_COFINS dos registros C175, C385, C605, C870, D205, D300, D350, D605, F200, F500, F550,
VL_BC_COFINS do registro F100, quando o valor do campo ALIQ_COFINS não conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”,
VL_BC_COFINS dos registros I100.
Quando o COD_CONT for igual a 03 ou 53, o valor deste campo será igual a zero.
Caso contrário (sociedade cooperativa), o valor deste campo será igual ao valor do campo VL_BC_CONT do registro M611.
Campo 05 - Preenchimento: informar a alíquota da COFINS (em percentual) aplicável. Quando o COD_CONT for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 06 - Preenchimento: informar a quantidade da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro.
Validação: Quando o valor do campo COD_CONT for igual a 03, 53 ou 32, o valor do campo será igual a:
QUANT_BC_COFINS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
QUANT_BC_COFINS dos registros C185 e C495, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
QUANT_BC_COFINS dos registros C485, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
QUANT_BC_COFINS dos registros C385, C880, D350, F510, F560,
VL_BC_COFINS do registro F100, quando o valor do campo ALIQ_COFINS conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”
Quando valor do campo COD_CONT for igual a 01, 51, 02, 52 ou 31 o campo deverá ser deixado em branco.
Campo 07 - Preenchimento: informar a alíquota da COFINS (em reais) aplicável. Quando o COD_CONT não for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 08 - Preenchimento: informar o valor total da contribuição social apurada, vinculada ao COD_CONT do registro, correspondendo a QUANT_BC_COFINS x ALIQ_COFINS_QUANT, quando a contribuição for calculada por unidade de medida de produto ou VL_BC_CONT x ALIQ_COFINS/100, caso contrário.
Campo 09 - Preenchimento: informar o valor dos ajustes de acréscimo à contribuição social apurada no campo 08. O preenchimento deste campo obriga o respectivo detalhamento no registro M620, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M620 quando IND_AJ = 1.
Campo 10 - Preenchimento: informar o valor dos ajustes de redução à contribuição social apurada no campo 08. O preenchimento deste campo obriga o respectivo detalhamento no registro M620, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M620 quando IND_AJ = 0.
Campo 11 - Preenchimento: informar o valor da contribuição a diferir no período, referente às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998). O preenchimento deste campo obriga o preenchimento do registro M630, devendo ser igual ao somatório do campo VL_CONT_DIF dos registros M630.
Campo 12 - Preenchimento: informar o valor da contribuição diferida em períodos anteriores, adicionada a este período de escrituração, referente às receitas diferidas recebidas no mês da escrituração.  O preenchimento deste campo obriga o preenchimento do registro M300, sendo que a soma dos valores deste campo de todos os registros M610 deverá ser igual a soma dos campos VL_CONT_DIFER_ANT dos registros M300, para um mesmo COD_CONT.
Campo 13 - Preenchimento: informar o valor total da contribuição do período da escrituração, para o respectivo COD_CONT, devendo ser igual a VL_CONT_APUR + VL_AJUS_ACRES - VL_AJUS_REDUC – VL_CONT_DIFER + VL_CONT_DIFER_ANT.
Leiaute do Registro M610 aplicável aos Fatos Geradores ocorridos a partir de 01 de janeiro de 2019:
A chave do registro é formada pelos campos COD_CONT + ALIQ_COFINS_QUANT + ALIQ_COFINS

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M610" | C | 004* | - | S |
| 02 | COD_CONT | Código da contribuição social apurada no período, conforme a Tabela 4.3.5. | C | 002* | - | S |
| 03 | VL_REC_BRT | Valor da Receita Bruta | N | - | 02 | S |
| 04 | VL_BC_CONT | Valor da Base de Cálculo da Contribuição, antes de ajustes | N | - | 02 | S |
| 05 | VL_AJUS_ACRES_BC_COFINS | Valor do total dos ajustes de acréscimo da base de cálculo da contribuição a que se refere o Campo 04 | N | - | 02 | S |
| 06 | VL_AJUS_REDUC_BC_COFINS | Valor do total dos ajustes de redução da base de cálculo da contribuição a que se refere o Campo 04 | N | - | 02 | S |
| 07 | VL_BC_CONT_AJUS | Valor da Base de Cálculo da Contribuição, após os ajustes. (Campo 07 = Campo 04 + Campo 05 - Campo 06) | N | - | 02 | S |
| 08 | ALIQ_COFINS | Alíquota da Cofins (em percentual) | N | 008 | 04 | N |
| 09 | QUANT_BC_COFINS | Quantidade – Base de cálculo Cofins | N | - | 03 | N |
| 10 | ALIQ_COFINS_QUANT | Alíquota da Cofins (em reais) | N | - | 04 | N |
| 11 | VL_CONT_APUR | Valor total da contribuição social apurada | N | - | 02 | S |
| 12 | VL_AJUS_ACRES | Valor total dos ajustes de acréscimo da contribuição social apurada | N | - | 02 | S |
| 13 | VL_AJUS_REDUC | Valor total dos ajustes de redução da contribuição social apurada | N | - | 02 | S |
| 14 | VL_CONT_DIFER | Valor da contribuição a diferir no período | N | - | 02 | N |
| 15 | VL_CONT_DIFER_ANT | Valor da contribuição diferida em períodos anteriores | N | - | 02 | N |
| 16 | VL_CONT_PER | Valor Total da Contribuição do Período (11 + 12 – 13 – 14+15) | N | - | 02 | S |

Observações:
1. Os valores representativos de Bases de Cálculo da contribuição, demonstrados no Campo 04 “VL_BC_CONT” (base de cálculo referente a receitas auferidas) do Registro “M610”, são recuperados do Campo “VL_BC_COFINS” dos diversos registros dos Blocos “A”, “C”, “D” ou “F” que contenham o mesmo CST.
2. Os valores representativos de Bases de Cálculo da contribuição em quantidade, demonstrados no Campo 06 “QUANT_BC_COFINS” (base de cálculo referente a quantidades vendidas) do Registro “M610”, são recuperados do Campo “QUANT_BC_COFINS” dos registros do Bloco “C” que contenham o mesmo CST.
3. Deve existir ao menos um registro M610 de apuração de contribuição a alíquotas específicas (diferenciadas ou por unidade de medida de produto), com o Campo “COD_CONT” igual a 02 ou 03 (regime não-cumulativo) ou 52 ou 53 (regime cumulativo) se o Campo “COD_TIPO_CONT” do Registro 0110 for igual a 2.
4. Considerando que este novo leiaute do Registro M610 só pode ser utilizado na escrituração dos fatos geradores a partir de 01.01.2019, eventuais ajustes referentes aos fatos geradores ocorridos até 31.12.2018 devem ser informados, nas EFD-Contribuições correspondentes a estes períodos anteriores a 2019, originais ou retificadoras, nos campos 09 (VL_AJUS_ACRES) e 10 (VL_AJUS_REDUC).
Nível hierárquico – 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [M610]
Campo 02 - Preenchimento: informe o código da contribuição social que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>. Quando a apuração é gerada automaticamente pelo PVA, o campo é obtido através das seguintes combinações:

| Campo COD_CONT do Registro M610 | Descrição do COD_CONT | CST_COFINS | Campo COD_INC_TRIB do Registro 0110 | Alíquota da COFINS (em percentual) (ALIQ_COFINS) | Alíquota da COFINS (em reais) (ALIQ_COFINS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 1 | 7,6(COFINS) | - |
| 01 | Contribuição não-cumulativa apurada a alíquota básica | 01 | 3 | 7,6(COFINS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 2 | 3,0(COFINS) | - |
| 51 | Contribuição cumulativa apurada a alíquota básica | 01 | 3 | 3,0(COFINS) | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 1 | - | - |
| 02 | Contribuição não-cumulativa apurada a alíquotas diferenciadas | 02 | 3 | - | - |
| 52 | Contribuição cumulativa apurada a alíquotas diferenciadas | 02 | 2 | - | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 1 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 1 | > 0 | - |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03 | 3 | - | > 0 |
| 03 | Contribuição não-cumulativa apurada a alíquota por unidade de medida de produto | 03* | 3 | > 0 | - |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03 | 2 | - | > 0 |
| 53 | Contribuição cumulativa apurada a alíquota por unidade de medida de produto | 03* | 2 | > 0 | - |
| 31 | Contribuição apurada por substituição tributária | 05 | - | 3,0(COFINS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | Diferente de 0, 3,0(COFINS) | - |
| 32 | Contribuição apurada por substituição tributária – Vendas à Zona Franca de Manaus | 05 | - | - | >0 |

Tabela para apuração dos registros M610 – F200 (Item exclusivo para informações obtidas dos registros F200)

| Campo COD_CONT do Registro M610 | Descrição do COD_CONT | CST_COFINS | Campo COD_INC_TRIB do Registro 0110 | Alíquota do COFINS (em percentual) (ALIQ_COFINS) | Alíquota do COFINS (em reais) (ALIQ_COFINS_QUANT) |
| --- | --- | --- | --- | --- | --- |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 1 | 7,6 | - |
| 04 | Contribuição não-cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 7,6 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 2 | 3,0 | - |
| 54 | Contribuição cumulativa apurada a alíquota básica - Atividade Imobiliária | 01 | 3 | 3,0 | - |

O PVA não validará e não gerará automaticamente registros M610 com COD_CONT igual a 71 (Contribuição apurada de SCP – Incidência Não Cumulativa), 72 (Contribuição apurada de SCP – Incidência Cumulativa) e 99 (Contribuição para o PIS/Pasep – Folha de Salários – Vide registro M350).
Campo 03 - Preenchimento: informar o valor da receita bruta auferida no período, vinculada ao respectivo COD_CONT.
Validação: Quando o valor do campo 02 (COD_CONT) for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual à soma dos seguintes campos (quando o CST da operação vinculada for 01, 02, 03, 04, 05 com alíquota diferente de zero):
VL_ITEM dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_ITEM dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_ITEM dos registros C185 e C495, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_ITEM dos registros C485, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_ITEM dos registros C385, C601, C870, C880, D205, D605
VL_DOC dos registros D300,
VL_BRT do registro D350,
VL_OPR do registro C175,
VL_OPER do registro F100, cujo valor do campo IND_OPER seja igual a “1” ou “2”,
VL_TOT_REC do registro F200,
VL_REC_CAIXA do registro F500 e F510,
VL_REC_COMP do registro F550 e F560,
VL_REC do registro I100.
Campo 04 - Preenchimento: informar o valor da base de cálculo da contribuição antes dos ajustes dos campos 05 e 06, vinculada ao valor de COD_CONT do respectivo registro.
Validação: Quando a natureza da pessoa jurídica (IND_NAT_PJ do registro “0000” igual a 00, 02, 03 ou 05) não for sociedade cooperativa e o valor do campo COD_CONT for igual a 01, 51, 02, 52, 31 ou 32, o valor do campo será igual a:
VL_BC_COFINS dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_BC_COFINS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_BC_COFINS dos registros C185 e C495, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_BC_COFINS dos registros C485, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_BC_COFINS dos registros C175, C385, C605, C870, D205, D300, D350, D605, F200, F500, F550,
VL_BC_COFINS do registro F100, quando o valor do campo ALIQ_COFINS não conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”,
VL_BC_COFINS dos registros I100.
Quando o COD_CONT for igual a 03 ou 53, o valor deste campo será igual a zero.
Caso contrário (sociedade cooperativa), o valor deste campo será igual ao valor do campo VL_BC_CONT do registro M611.
Campo 05 - Preenchimento: informar neste campo o valor do total dos ajustes de acréscimo da base de cálculo mensal da contribuição a que se refere o Campo 04.
O valor mensal dos ajustes de acréscimo informado neste campo deve ser detalhado no Registro Filho M615, de acordo com as informações especificadas no leiaute deste registro, inclusive, devendo ser segregado e referenciado ao estabelecimento (CNPJ) a que se refere o ajuste.
Campo 06 - Preenchimento: informar neste campo o valor do total dos ajustes de redução da base de cálculo mensal da contribuição a que se refere o Campo 04.
O valor mensal dos ajustes de redução informado neste campo deve ser detalhado no Registro Filho M615, de acordo com as informações especificadas no leiaute deste registro, inclusive, devendo ser segregado e referenciado ao estabelecimento (CNPJ) a que se refere o ajuste.
Campo 07 – Preenchimento: informar o valor da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro, após os ajustes dos campos 05 e 06.
Campo 08 - Preenchimento: informar a alíquota da COFINS (em percentual) aplicável. Quando o COD_CONT for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 09 - Preenchimento: informar a quantidade da base de cálculo da contribuição, vinculada ao valor de COD_CONT do respectivo registro.
Validação: Quando o valor do campo COD_CONT for igual a 03, 53 ou 32, o valor do campo será igual a:
QUANT_BC_COFINS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
QUANT_BC_COFINS dos registros C185 e C495, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
QUANT_BC_COFINS dos registros C485, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
QUANT_BC_COFINS dos registros C385, C880, D350, F510 e F560
VL_BC_COFINS do registro F100, quando o valor do campo ALIQ_COFINS conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”
Quando valor do campo COD_CONT for igual a 01, 51, 02, 52 ou 31 o campo deverá ser deixado em branco.
Campo 10 - Preenchimento: informar a alíquota da COFINS (em reais) aplicável. Quando o COD_CONT não for apurado por unidade de medida de produto, este campo deverá ser deixado em branco.
Campo 11 - Preenchimento: informar o valor total da contribuição social apurada, vinculada ao COD_CONT do registro, correspondendo a QUANT_BC_COFINS x ALIQ_COFINS_QUANT, quando a contribuição for calculada por unidade de medida de produto ou VL_BC_CONT_AJUS x ALIQ_COFINS/100, caso contrário.
Campo 12 - Preenchimento: informar o valor dos ajustes de acréscimo à contribuição social apurada no campo 11. O preenchimento deste campo obriga o respectivo detalhamento no registro M620, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M620 quando IND_AJ = 1.
Campo 13 - Preenchimento: informar o valor dos ajustes de redução à contribuição social apurada no campo 11. O preenchimento deste campo obriga o respectivo detalhamento no registro M620, sendo que o valor deste campo deverá ser igual ao somatório do campo VL_AJ dos registros M620 quando IND_AJ = 0.
Campo 14 - Preenchimento: informar o valor da contribuição a diferir no período, referente às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998). O preenchimento deste campo obriga o preenchimento do registro M630, devendo ser igual ao somatório do campo VL_CONT_DIF dos registros M630.
Campo 15 - Preenchimento: informar o valor da contribuição diferida em períodos anteriores, adicionada a este período de escrituração, referente às receitas diferidas recebidas no mês da escrituração.  O preenchimento deste campo obriga o preenchimento do registro M300, sendo que a soma dos valores deste campo de todos os registros M610 deverá ser igual a soma dos campos VL_CONT_DIFER_ANT dos registros M300, para um mesmo COD_CONT.
Campo 16 - Preenchimento: informar o valor total da contribuição do período da escrituração, para o respectivo COD_CONT, devendo ser igual a VL_CONT_APUR (campo 11) + VL_AJUS_ACRES (campo 12) - VL_AJUS_REDUC (campo 13) – VL_CONT_DIFER (campo 14) + VL_CONT_DIFER_ANT (campo 15).
Registro M611: Sociedades Cooperativas – Composição da Base de Calculo – Cofins
Este registro deve ser preenchido quando o Campo “IND_NAT_PJ” do registro 0000 for igual a “01” ou “04”, tratando-se de registro obrigatório para a determinação das bases de cálculo das sociedades cooperativas. No caso da cooperativa se enquadrar em mais de um dos tipos abaixo indicados, informar o tipo preponderante.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M611" | C | 004* | - | S |
| 02 | IND_TIP_COOP | Indicador do Tipo de Sociedade Cooperativa: 01 – Cooperativa de Produção Agropecuária; 02 – Cooperativa de Consumo; 03 – Cooperativa de Crédito; 04 – Cooperativa de Eletrificação Rural; 05 – Cooperativa de Transporte Rodoviário de Cargas; 06 – Cooperativa de Médicos; 99 – Outras. | N | 002* | - | S |
| 03 | VL_BC_CONT_ANT_EXC_COOP | Valor da Base de Cálculo da Contribuição, conforme Registros escriturados nos Blocos A, C, D e F, antes das Exclusões das Sociedades Cooperativas. | N | - | 02 | S |
| 04 | VL_EXC_COOP_GER | Valor de Exclusão Especifica das Cooperativas em Geral, decorrente das Sobras Apuradas na DRE, destinadas a constituição do Fundo de Reserva e do FATES. | N | - | 02 | N |
| 05 | VL_EXC_ESP_COOP | Valor das Exclusões da Base de Cálculo Especifica do Tipo da Sociedade Cooperativa, conforme Campo 02 (IND_TIP_COOP). | N | - | 02 | N |
| 06 | VL_BC_CONT | Valor da Base de Cálculo, Após as Exclusões Especificas da Sociedade Cooperativa (04 – 05 – 06) – Transportar para M610. | N | - | 02 | S |

Observações:
Nível hierárquico – 4
Ocorrência - 1:1
Campo 01 - Valor Válido: [M611]
Campo 02 - Valores válidos: [01, 02, 03, 04, 05, 06, 99]
Preenchimento: informar o tipo de sociedade cooperativa. Caso a cooperativa se enquadre em mais de um tipo, informe o fim preponderante.
Campo 03 - Preenchimento: informar o valor da base de cálculo da contribuição, vinculada ao COD_CONT do registro M610, conforme registros escriturados nos Blocos A, C, D e F, antes das exclusões das cooperativas.
Validação: Quando o valor do campo COD_CONT for igual a 01, 51, 02, 52, 31 ou 32 (no caso de apuração da contribuição com base em alíquotas da tabela 4.3.10), o valor do campo será igual a:
·	VL_BC_COFINS dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
·	VL_BC_COFINS dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
·	VL_BC_COFINS dos registros C185 e C495, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
·	VL_BC_COFINS dos registros C485, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
·	VL_BC_COFINS dos registros C175, C385, C605, C870, D205, D300, D350, D605, F200, F500, F550,
-	VL_BC_COFINS do registro F100, quando o valor do campo ALIQ_COFINS não conste nas alíquotas da tabela 4.3.11 - “Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda)”
Nos demais casos, o valor deste e dos demais campos será igual a zero.
Campo 04 - Preenchimento: informar o valor exclusão especifica das cooperativas em geral, decorrente das sobras apuradas na DRE, destinadas a constituição do fundo de reserva e do FATES.
Campo 05 - Preenchimento: informar o valor das exclusões da base de cálculo especifica do tipo da sociedade cooperativa, conforme campo 02 (IND_TIP_COOP).
Campo 06 - Preenchimento: informar o valor da base de cálculo, após as exclusões especificas da sociedade cooperativa, correspondendo a VL_BC_CONT_ANT_EXC_COOP - VL_EXC_COOP_GER - VL_EXC_ESP_COOP. O valor apurado neste campo deverá ser transportado para o campo 04 (VL_BC_CONT), do registro pai M610.
<!-- End Registro M611 -->
<!-- Start Registro M615 -->
Registro M615: Ajustes da Base de Cálculo da COFINS Apurada
Este registro será utilizado pela pessoa jurídica para detalhar os totais de ajustes da base de cálculo, informados nos campos 05 e 06 do registro pai M610.
A chave do registro é formada pelos campos: IND_AJ_BC; COD_AJ_BC; NUM_DOC; COD_CTA; DT_REF; CNPJ e INFO_COMPL.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M615" | C | 004 | - | S |
| 02 | IND_AJ_BC | Indicador do tipo de ajuste da base de cálculo: 0 - Ajuste de redução; 1 - Ajuste de acréscimo. | C | 001* | - | S |
| 03 | VL_AJ_BC | Valor do ajuste de base de cálculo | N | - | 02 | S |
| 04 | COD_AJ_BC | Código do ajuste, conforme a Tabela indicada no item 4.3.18 | C | 002* | - | S |
| 05 | NUM_DOC | Número do processo, documento ou ato concessório ao qual o ajuste está vinculado, se houver. | C | - | - | N |
| 06 | DESCR_AJ_BC | Descrição resumida do ajuste na base de cálculo. | C | - | - | N |
| 07 | DT_REF | Data de referência do ajuste (ddmmaaaa) | N | 008* | - | N |
| 08 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |
| 09 | CNPJ | CNPJ do estabelecimento a que se refere o ajuste | N | 014* | - | S |
| 10 | INFO_COMPL | Informação complementar do registro | C | - | - | N |

Observações:
1. Este registro deve ser escriturado, obrigatoriamente, quando a pessoa jurídica informar valores de ajustes de acréscimo ou de redução da base de cálculo mensal da contribuição, no Registro Pai M610, objetivando demonstrar, de forma analítica e segregada, os totais dos ajustes na base de cálculo da contribuição correspondente ao período a que se refere a escrituração.
2. Como já informado neste Guia Prático da Escrituração, os ajustes da base de cálculo mensal das contribuições, objeto de escrituração consolidada (nos campos 05 e 06 do Registro Pai M610) e analítica (no Registro Filho M615), só são habilitados na escrituração das contribuições referentes aos períodos de apuração correspondentes aos fatos geradores a ocorrer a partir de 01 de janeiro de 2019.
3. Desta forma, mesmo que a pessoa jurídica esteja utilizando a versão 3.1.0 e posteriores da versão do programa da EFD-Contribuições para a escrituração de fatos geradores ocorridos até 31.12.2018, a versão em referência não disponibiliza estes campos de ajustes de base de cálculo, especificados nos Registros M610 e M615.
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [M615]
Campo 02 - Valores válidos: [0, 1]
Campo 03 - Preenchimento: informar o valor do ajuste de redução ou de acréscimo da base de cálculo mensal da contribuição que está sendo objeto de segregação, de escrituração analítica, neste registro filho.
A soma de todos os valores analíticos representativos de ajustes de acréscimo de base de cálculo (IND_AJ_BC = 1) e de ajustes de redução de base de cálculo (IND_AJ_BC = 0) dos diversos registros M615 escriturados e relativos ao período da escrituração, deverá corresponder aos valores totais escriturados nos campos 05 (VL_AJUS_ACRES_BC_COFINS) e 06 (VL_AJUS_REDUC_BC_COFINS) do Registro Pai M610, respectivamente.
Campo 04 - Preenchimento: informar o código do ajuste da base de cálculo, conforme Tabela 4.3.18 - “Tabela Código de Ajustes da Base de Cálculo Mensal”, referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informar, se for o caso, o número do processo, documento ou ato concessório ao qual o ajuste está vinculado, como por exemplo, o número do processo judicial que autoriza a pessoa jurídica a proceder a ajustes na base de cálculo mensal da contribuição.
Campo 06 - Preenchimento: informar a descrição resumida do ajuste da base de cálculo mensal que está sendo escriturado no respectivo registro.
Campo 07 - Preenchimento: informar, se for o caso, a data de referência do ajuste, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
No caso de o ajuste informado no registro não ser específico de uma data do período, deve ser informado a data correspondente ao ultimo dia do mês a que se refere a escrituração, como por exemplo, “31012019”.
Campo 08 - Preenchimento: Informar, sendo o caso, o código da conta contábil a que se refere o ajuste detalhado neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 09 - Preenchimento: informar o CNPJ do estabelecimento da pessoa jurídica a que se refere o ajuste escriturado neste registro.
Caso o ajuste não se refira a um estabelecimento especifico, deve ser informado o CNPJ correspondente ao estabelecimento matriz da pessoa jurídica, escriturado no Registro “0000”.
Campo 10 - Preenchimento: Campo para prestação de outras informações que se mostrem necessárias ou adequadas, para esclarecer ou justificar o ajuste na base de cálculo a que se refere este registro.
<!-- End Registro M615 -->
<!-- Start Registro M620 -->
Registro M620: Ajustes da Cofins Apurada
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas nos campos 09 e 10 do registro pai M610.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M620" | C | 004* | - | S |
| 02 | IND_AJ | Indicador do tipo de ajuste: 0- Ajuste de redução; 1- Ajuste de acréscimo. | C | 001* | - | S |
| 03 | VL_AJ | Valor do ajuste | N | - | 02 | S |
| 04 | COD_AJ | Código do ajuste, conforme a Tabela indicada no item 4.3.8. | C | 002* |   | S |
| 05 | NUM_DOC | Número do processo, documento ou ato concessório ao qual o ajuste está vinculado, se houver. | C | - | - | N |
| 06 | DESCR_AJ | Descrição resumida do ajuste. | C | - | - | N |
| 07 | DT_REF | Data de referência do ajuste (ddmmaaaa) | N | 008* | - | N |

Ocorrências:
Nível hierárquico - 4
Ocorrência – 1:N (por tipo de contribuição M600)
Campo 01 - Valor Válido: [M620]
Campo 02 - Valores válidos: [0, 1]
Campo 03 - Preenchimento: informar o valor do ajuste de redução ou de acréscimo. A soma de todos os valores deste campo, representando ajustes de acréscimo (IND_AJ = 1) deverá ser transportada para o campo 09 (VL_AJUS_ACRES) do registro M610. Por sua vez, a soma de todos os valores deste campo, representando ajustes de redução (IND_AJ = 0) deverá ser transportada para o campo 10 (VL_AJUS_REDUC) do registro M610.
Campo 04 - Preenchimento: informar o código do ajuste, conforme Tabela 4.3.8 - “Tabela Código de Ajustes de Contribuição ou Créditos”, referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
Campo 05 - Preenchimento: informar, se for o caso, o número do processo, documento ou ato concessório ao qual o ajuste está vinculado, como por exemplo, o documento fiscal referenciado na devolução de venda.
No caso de ajuste que envolva grande quantidade de documentos, pode o registro ser escriturado consolidando as informações dos documentos, descrevendo no campo 06 (tipo de documento fiscal consolidado, quantidades de documentos, emitente/beneficiário, por exemplo).
Campo 06 - Preenchimento: informar a descrição resumida do ajuste que está sendo lançada no respectivo registro.
Campo 07 - Preenchimento: informar, se for o caso, a data de referência do ajuste, no formato "ddmmaaaa", excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
<!-- End Registro M620 -->
<!-- Start Registro M625 -->
Registro M625: Detalhamento dos Ajustes da Cofins Apurada
Registro a ser preenchido para a pessoa jurídica detalhar a operação e valor a que se refere o ajuste da contribuição informado no registro pai M620.
Registro não disponível para os fatos geradores até 30/09/2015.
Para os fatos geradores a partir de 01/10/2015 a versão 2.12 do Programa da EFD-Contribuições (PVA) disponibiliza este registro de detalhamento de ajustes da Cofins, o qual deve ser preenchido, para que seja demonstrado e detalhado à Receita Federal quais as operações realizadas que ensejaram os ajustes informados no registro M620, quando a informação prestada no Registro M620 não seja suficientemente analítica, de forma a detalhar a(s) operação(ões) ensejadora(s) do ajuste.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M625” | C | 004* | - | S |
| 02 | DET_VALOR_AJ | Detalhamento do valor da contribuição reduzida ou acrescida, informado no Campo 03 (VL_AJ) do registro M620. | N | - | 02 | S |
| 03 | CST_COFINS | Código de Situação Tributária referente à operação detalhada neste registro. | N | 002* | - | N |
| 04 | DET_BC_CRED | Detalhamento da base de cálculo geradora de ajuste de contribuição | N | - | 03 | N |
| 05 | DET_ALIQ | Detalhamento da alíquota a que se refere o ajuste de contribuição | N | 08 | 04 | N |
| 06 | DT_OPER_AJ | Data da operação a que se refere o ajuste informado neste registro. | N | 008* | - | S |
| 07 | DESC_AJ | Descrição da(s) operação(ões) a que se refere o valor informado no Campo 02 (DET_VALOR_AJ) | C | - | - | N |
| 08 | COD_CTA | Código da conta contábil debitada/creditada | C | 255 | - | N |
| 09 | INFO_COMPL | Informação complementar | C | - | - | N |

Observações:
Nível hierárquico – 5
Ocorrência - 1:N
Campo 01 - Valor Válido: [M625]
Campo 02 - Preenchimento: Informar o detalhamento do valor da operação a que se refere o ajuste da contribuição informado no Campo 03 (VL_AJ) do registro M620.
Caso o ajuste em M620 se refira a várias operações ou situações, devem ser gerados os registros de detalhamento M625 que se mostrem necessários e suficientes, para demonstrar o valor total do ajuste escriturado em M620.
Campo 03 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao ajuste de contribuição de PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 04 - Preenchimento: Informar a base de cálculo do ajuste de contribuição a que se refere este registro.
Campo 05 - Preenchimento: Informar a alíquota a que se refere o ajuste de contribuição informado neste registro.
Campo 06 - Preenchimento: Informar a data da operação a que se refere o ajuste de contribuição detalhado neste registro.
Campo 07 - Preenchimento: Informar a descrição da(s) operação(ões) a que se refere o ajuste detalhado neste registro.
Campo 08 - Preenchimento: Informar, sendo o caso, o código da conta contábil a que se refere o ajuste detalhado neste registro.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 09 - Preenchimento: Campo para prestação de outras informações que se mostrem necessárias ou adequadas, para esclarecer ou justificar o ajuste.
<!-- End Registro M625 -->
<!-- Start Registro M630 -->
Registro M630: Informações Adicionais de Diferimento
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas no campo 11 (VL_CONT_DIFER) do registro pai M610, referente às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços (parágrafo único e no caput do art. 7º da Lei nº 9.718, de 1998).
Os créditos da não-cumulatividade vinculados a estas receitas ainda não recebidas também deverão ser detalhados neste registro, sendo que o somatório dos campos 11 (VL_CRED_DIF) do registro M500 deverá ser igual ao somatório dos campos VL_CRED_DIF dos registros M630, para o mesmo COD_CRED.
O somatório do campo 05 (VL_CONT_DIF) destes registros deverá ser igual ao valor lançado no respectivo campo 11 do registro pai M610.
Deverá existir um registro M630 para cada CNPJ em que houve contribuição diferida no período e para cada código de tipo de crédito diferido no período. Assim, a chave do registro é formada pelos campos CNPJ + COD_CRED.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M630" | C | 004* | - | S |
| 02 | CNPJ | CNPJ da pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias. | N | 014* | - | S |
| 03 | VL_VEND | Valor Total das vendas no período | N | - | 02 | S |
| 04 | VL_NAO_RECEB | Valor Total não recebido no período | N | - | 02 | S |
| 05 | VL_CONT_DIF | Valor da Contribuição diferida no período | N | - | 02 | S |
| 06 | VL_CRED_DIF | Valor do Crédito diferido no período | N | - | 02 | N |
| 07 | COD_CRED | Código de Tipo de Crédito diferido no período, conforme a Tabela 4.3.6. | C | 003* | - | N |

Observações:
Nível hierárquico – 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [M630]
Campo 02 - Preenchimento: informar o CNPJ da pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias para a qual foi realizada a construção por empreitada ou o fornecimento a preço predeterminado de bens ou serviços.
Campo 03 - Preenchimento: informar o valor total das vendas no período da escrituração para o CNPJ informado no campo 02.
Campo 04 - Preenchimento: informar o valor total não recebido no período da escrituração, referente ao CNPJ informado no campo 02.
Campo 05 - Preenchimento: informar a contribuição diferida no período, referente ao não recebimento de valores do CNPJ informado no campo 02.
Campo 06 - Preenchimento: informar o valor dos créditos da não cumulatividade vinculados às receitas ainda não recebidas decorrentes da celebração de contratos com pessoa jurídica de direito público, empresa pública, sociedade de economia mista ou suas subsidiárias, relativos à construção por empreitada ou a fornecimento a preço predeterminado de bens ou serviços, conforme o tipo de crédito diferido, informado no campo 07 (COD_CRED) deste registro.
Campo 07 - Preenchimento: informar o código de tipo de crédito diferido no período, informado no campo 06, conforme tabela 4.3.6 - "Tabela Código de Tipo de Crédito" referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
<!-- End Registro M630 -->
<!-- Start Registro M700 -->
Registro M700: Cofins Diferida em Períodos Anteriores – Valores a Pagar no Período
Este registro será utilizado pela pessoa jurídica para detalhar as informações prestadas no campo 12 (VL_CONT_DIFER_ANT) dos diversos registros M610 existentes na escrituração.
Os valores da contribuição diferida em períodos anteriores, que deverão ser pagos no atual período da escrituração, face aos recebimentos ocorridos no mês, descontados dos respectivos créditos diferidos, serão adicionados à respectiva contribuição calculada (COD_CONT) no registro M610, sendo que a soma dos valores do campo 12 de todos os registros M610 deverá ser igual a soma dos campos VL_CONT_DIFER_ANT dos registros M700, para um mesmo COD_CONT.
Deverá existir um registro M700 para cada data em que houve recebimento de receita objeto de diferimento, de maneira combinada com o período da escrituração em que o diferimento ocorreu e para cada tipo de contribuição diferida e natureza do crédito diferido a descontar no período. Assim, a chave deste registro é formada pelos campos COD_CONT + NAT_CRED_DESC + PER_APUR + DT_RECEB.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M700" | C | 004* | - | S |
| 02 | COD_CONT | Código da contribuição social diferida em períodos anteriores, conforme a Tabela 4.3.5. | C | 002 | - | S |
| 03 | VL_CONT_APUR_DIFER | Valor da Contribuição Apurada, diferida em períodos anteriores. | N | - | 02 | S |
| 04 | NAT_CRED_DESC | Natureza do Crédito Diferido, vinculado à receita tributada no mercado interno, a descontar: 01 – Crédito a Alíquota Básica; 02 – Crédito a Alíquota Diferenciada; 03 – Crédito a Alíquota por Unidade de Produto; 04 – Crédito Presumido da Agroindústria. | C | 002 | - | N |
| 05 | VL_CRED_DESC_DIFER | Valor do Crédito a Descontar vinculado à contribuição diferida. | N | - | 02 | N |
| 06 | VL_CONT_DIFER_ANT | Valor da Contribuição a Recolher, diferida em períodos anteriores (Campo 03 – Campo 05) | N | - | 02 | S |
| 07 | PER_APUR | Período de apuração da contribuição social e dos créditos diferidos (MMAAAA). | N | 006* | - | S |
| 08 | DT_RECEB | Data de recebimento da receita, objeto de diferimento. | N | 008* | - | N |

Observações: O valor do Campo 06 (VL_CONT_DIFER_ANT) será recuperado no registro M610, Campo 12, que detalha a contribuição devida no período da escrituração.
Nível hierárquico – 2
Ocorrência – vários por arquivo
Campo 01 - Valor Válido: [M700]
Campo 02 - Preenchimento: informe o código da contribuição social diferida em períodos anteriores que está sendo informado no registro, conforme a Tabela “4.3.5 – Código de Contribuição Social Apurada” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>
Campo 03 - Preenchimento: informar o valor da contribuição apurada, diferida em períodos anteriores e que deverá ser paga no período da escrituração, após o desconto de eventuais créditos informados no campo 05.
Campo 04 - Valores válidos: [01, 02, 03, 04]
Campo 05 - Preenchimento: informar o valor do crédito a descontar vinculado à contribuição diferida.
Campo 06 - Preenchimento: informar o valor da contribuição a recolher, diferida em períodos anteriores, após o desconto de eventuais créditos informados no campo 05, correspondendo, então, a VL_CONT_APUR_DIFER - VL_CRED_DESC_DIFER.
Campo 07 - Preenchimento: informar o período de apuração da contribuição social e dos créditos diferidos, conforme informado anteriormente no registro M630 (no caso do respectivo período ter sido objeto de transmissão da EFD PIS/COFINS). Utilize o formato “mmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.  O período informado não pode ser o mesmo da atual escrituração.
Campo 08 - Preenchimento: informar a data de recebimento da receita, objeto de diferimento. A data deverá estar compreendida no período da atual escrituração.
<!-- End Registro M700 -->
<!-- Start Registro M800 -->
Registro M800: Receitas Isentas, Não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas Com Suspensão – Cofins
Este registro será utilizado pela pessoa jurídica para consolidar as receitas não sujeitas ao pagamento da contribuição social, com base nos CST específicos (04, 06, 07, 08 e 09) informados nas receitas relacionadas nos Blocos A, C, D e F.
Conforme item “4. Procedimentos de escrituração na revenda de bens sujeitos à substituição tributária de PIS/COFINS”, até a versão 2.0.4a e anteriores do PGE, documentos escriturados com CST 05 e alíquota zero eram totalizados nos registros M400 e M800. A partir da versão 2.0.5 do PGE, todas as operações com CST 05 devem ser totalizadas nos registros M210 e M610. Dessa forma, as menções ao CST 05 nas orientações deste registro e respectivo registro filho aplicam-se apenas aos fatos geradores escriturados nas versões 2.0.4a e anteriores do PGE.
Quando utilizada a funcionalidade de “Gerar Apuração” do PVA EFD PIS/COFINS este registro será gerado automaticamente pelo PVA. Contudo, o registro filho M810, de natureza obrigatória neste caso, deverá ser preenchido pela própria pessoa jurídica.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M800” | C | 004* | - | S |
| 02 | CST_COFINS | Código de Situação Tributária – CST das demais receitas auferidas no período, sem incidência da contribuição, ou sem contribuição apurada a pagar, conforme a Tabela 4.3.4. | C | 002* | - | S |
| 03 | VL_TOT_REC | Valor total da receita bruta no período. | N | - | 02 | S |
| 04 | COD_CTA | Código da conta analítica contábil debitada/creditada. | C | 255 | - | N |
| 05 | DESC_COMPL | Descrição Complementar da Natureza da Receita. | C | - | - | N |

Observações:
1. Neste registro serão escrituradas as receitas não sujeitas ao pagamento da contribuição social, com base nos CST específicos informados nas receitas relacionadas nos Blocos A, C, D e F.
2. O campo VL_TOT_REC será correspondente ao somatório dos campos VL_REC dos registros M810.
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 - Valor Válido: [M800]
Campo 02 - Valores válidos: [04, 05, 06, 07, 08, 09]
Preenchimento: informar o CST relativo às demais receitas auferidas no período, sem incidência da contribuição, ou sem contribuição apurada a pagar.
Campo 03 - Preenchimento: informar o valor total da receita bruta no período, referente ao CST informado no campo 02, correspondendo à soma dos seguintes campos:
VL_ITEM dos registros A170, cujo valor do campo IND_OPER do registro A100 seja igual a “1”,
VL_ITEM dos registros C170, cujo valor do campo COD_MOD seja diferente de 55 (NFe) ou quando o valor do campo COD_MOD seja igual a 55 e o valor do campo IND_ESCRI do registro C010 seja igual a 2. Em ambos casos o valor do campo IND_OPER do registro C100 deve ser igual a “1”,
VL_ITEM dos registros C181 e C491, quando o valor do campo IND_ESCRI do registro C010 seja igual a 1
VL_ITEM dos registros C481, quando o valor do campo do campo IND_ESCRI do registro C010 seja igual a 2
VL_ITEM dos registros C381, C601, D201, D601,
VL_DOC dos registros D300,
VL_BRT do registro D350,
VL_OPR do registro C175,
VL_OPER do registro F100, cujo valor do campo IND_OPER seja igual a “1” ou “2”,
VL_TOT_REC do registro F200,
VL_REC_CAIXA dos registros F500 e F510,
VL_REC_COMP dos registros F550 e F560,
VL_REC do registro I100.
No caso de ser informado o CST 05 - Operação Tributável por Substituição Tributária, o preenchimento deste campo deverá ser feito apenas quando a alíquota aplicável for igual a zero (casos de revenda de produtos sujeitos à substituição tributária).
Campo 04 - Preenchimento: informar o código da conta contábil representativa da receita desonerada da contribuição a que se refere este registro. Exemplos: Receitas tributadas à alíquota zero, com suspensão, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta informada no registro de detalhamento M810). No caso de ser informado neste campo a conta sintética de receita, deve então ser informado no Campo 04 (COD_CTA) do(s) registro(s) filho M810, a conta de nível inferior (analítica ou sintética, conforme o plano de contas da empresa).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 05 - Preenchimento: informar a descrição complementar da natureza da receita.
<!-- End Registro M800 -->
<!-- Start Registro M810 -->
Registro M810: Detalhamento das Receitas Isentas, Não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas com Suspensão – Cofins
Neste registro a pessoa jurídica deverá detalhar as receitas isentas, não alcançadas pela incidência da contribuição, sujeitas à alíquota zero ou de vendas com suspensão, totalizadas no registro pai M800, conforme relação de códigos constantes das tabelas relacionadas no campo 02 (NAT_REC) e respectivas descrições complementares de cada uma das receitas sendo detalhadas. Desta forma, a chave deste registro é composta pelos campos NAT_REC + COD_CTA + DESC_COMPL.
Este registro não será gerado automaticamente pelo PVA EFD PIS/COFINS, sendo necessário a pessoa jurídica preencher manualmente mesmo quando utilizada a opção de “Gerar Apuração”.
A soma dos campos VL_REC dos registros M810 deverá corresponder ao valor informado/calculado no campo VL_TOT_REC do registro pai M800.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M810” | C | 004* | - | S |
| 02 | NAT_REC | Natureza da Receita, conforme relação constante nas Tabelas de Detalhamento da Natureza da Receita por Situação Tributária abaixo: - Tabela 4.3.10: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas Diferenciadas (CST 04 - Revenda); - Tabela 4.3.11: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto (CST 04 - Revenda); - Tabela 4.3.12: Produtos Sujeitos à Substituição Tributária da Contribuição Social (CST 05 - Revenda); - Tabela 4.3.13: Produtos Sujeitos à Alíquota Zero da Contribuição Social (CST 06); - Tabela 4.3.14: Operações com Isenção da Contribuição Social (CST 07); - Tabela 4.3.15: Operações sem Incidência da Contribuição Social (CST 08); - Tabela 4.3.16: Operações com Suspensão da Contribuição Social (CST 09). | C | 003* | - | S |
| 03 | VL_REC | Valor da receita bruta no período, relativo a natureza da receita (NAT_REC) | N | - | 02 | S |
| 04 | COD_CTA | Código da conta analítica contábil debitada/creditada. | C | 255 | - | N |
| 05 | DESC_COMPL | Descrição Complementar da Natureza da Receita. | C | - | - | N |

Observações:
As receitas componentes deste registro (receitas não tributadas ou não sujeitas ao pagamento da contribuição) devem ser informadas nos respectivos registros dos blocos A, C, D e F.
Deve ser informado no Campo 02 o detalhamento da natureza da receita não tributada ou não sujeita ao pagamento da contribuição, conforme as tabelas externas disponibilizadas pela RFB.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [M810]
Campo 02 - Preenchimento: informar a natureza da receita sendo detalhada no registro, conforme códigos existentes nas tabelas abaixo indicadas, obedecendo ao respectivo CST orientador:
Para o CST 04 - Operação Tributável Monofásica - Revenda a Alíquota Zero, utilize os códigos constantes nas tabelas 4.3.10: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas Diferenciadas e 4.3.11: Produtos Sujeitos à Incidência Monofásica da Contribuição Social – Alíquotas por Unidade de Medida de Produto.
Para o CST 05 (e alíquota zero) - Operação Tributável por Substituição Tributária, utilize os códigos da Tabela 4.3.12: Produtos Sujeitos à Substituição Tributária da Contribuição Social.
Para o CST 06 - Operação Tributável a Alíquota Zero, utilize os códigos da Tabela 4.3.13: Produtos Sujeitos à Alíquota Zero da Contribuição Social.
Para o CST 07 - Operação Isenta da Contribuição, utilize os códigos da Tabela 4.3.14: Operações com Isenção da Contribuição Social.
Para o CST 08 - Operação sem Incidência da Contribuição, utilize os códigos da Tabela 4.3.15: Operações sem Incidência da Contribuição Social.
Para o CST 09 - Operação com Suspensão da Contribuição, utilize os códigos da Tabela 4.3.16: Operações com Suspensão da Contribuição Social.
Campo 03 - Preenchimento: informar o valor da receita bruta no período, relativo a natureza da receita informada no campo 02.
Campo 04 - Preenchimento: informar o Código da Conta Analítica referente à receita relativa à respectiva natureza informada no campo 02. Deve ser a conta contábil de nível inferior à informada no Registro M800.
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo “COD_CTA” é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide
Campo 05 - Preenchimento: informar a descrição complementar da natureza da receita, relativa a natureza da receita informada no campo 02.
<!-- End Registro M810 -->
<!-- Start Registro M990 -->
Registro M990: Encerramento do Bloco M

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "M990" | C | 004* | - | S |
| 02 | QTD_LIN_M | Quantidade total de linhas do Bloco M | N | - | - | S |

Observações: Registro obrigatório
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Validação do Registro: registro único e obrigatório para todos os informantes da EFD-Contribuições.
Campo 01 - Valor Válido: [M990]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco M é igual ao valor informado no campo QTD_LIN_M (registro M990).
<!-- End Registro M990 -->