# Bloco D - Versão 1.35

BLOCO D: Documentos Fiscais – II - Serviços (ICMS)
<!-- Start Registro D001 -->
Registro D001: Abertura do Bloco D
Este registro deve ser gerado para abertura do Bloco D e indica se há informações sobre prestações ou contratações de serviços de comunicação, transporte interestadual e intermunicipal, com o devido suporte do correspondente documento fiscal.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D001" | C | 004* | - | S |
| 02 | IND_MOV | Indicador de movimento: 0- Bloco com dados informados; 1- Bloco sem dados informados | C | 001 | - | S |

Observações:
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Campo 01 - Valor Válido: [D001]
Campo 02 - Valores válidos: [0, 1]
Validação: se o valor deste campo for igual a "1" (um), somente podem ser informados os registros de abertura e encerramento do bloco. Se o valor neste campo for igual a "0" (zero), deve ser informado pelo menos um registro além dos registros de abertura e encerramento do bloco.
<!-- End Registro D001 -->
<!-- Start Registro D010 -->
Registro D010: Identificação do Estabelecimento
Este registro tem o objetivo de identificar o estabelecimento da pessoa jurídica a que se referem as operações e documentos fiscais informados neste bloco. Só devem ser escriturados no Registro D010 os estabelecimentos que efetivamente tenham realizado as operações especificadas no Bloco D (prestação ou contratação), relativas a serviços de transporte de cargas e/ou de passageiros, serviços de comunicação e de telecomunicação, mediante emissão de documento fiscal definido pela legislação do ICMS e do IPI, que devam ser escrituradas no Bloco D.
O estabelecimento que não realizou operações passíveis de registro nesse bloco, no período da escrituração, não deve ser identificado no Registro D010.
Para cada estabelecimento cadastrado em “D010”, deve ser informado nos registros de nível inferior (Registros Filho) as operações próprias de prestação ou de contratação, mediante emissão de documento fiscal, no mercado interno ou externo

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo “D010”. | C | 004* | - | S |
| 02 | CNPJ | Número de inscrição do estabelecimento no CNPJ. | N | 014* | - | S |

Observações: Registro obrigatório.
Nível hierárquico - 2
Ocorrência – vários por arquivo
Campo 01 - Valor Válido: [D010];
Campo 02 - Preenchimento: informar o número do CNPJ do estabelecimento da pessoa jurídica a que se referem as operações passíveis de escrituração neste bloco.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. O estabelecimento informado neste registro deve está cadastrado no Registro 0140.
<!-- End Registro D010 -->
<!-- Start Registro D100 -->
Registro D100: Aquisição de Serviços de Transporte - Nota Fiscal de Serviço de Transporte (Código 07), Conhecimento de Transporte Rodoviário de Cargas (Código 08), Conhecimento de Transporte de Cargas Avulso (Código 8B), Conhecimento de Transporte Aquaviário de Cargas (Código 09), Conhecimento de Transporte Aéreo (Código 10), Conhecimento de Transporte Ferroviário de Cargas (Código 11), Conhecimento de Transporte Multimodal de Cargas (Código 26), Nota Fiscal de Transporte Ferroviário de Carga (Código 27), Conhecimento de Transporte Eletrônico – CT-E (Código 57), Bilhete de Passagem Eletrônico - BP-e (Código 63) e Conhecimento de Transporte Eletrônico para Outros Serviços – CT-e OS, modelo 67
Este registro deve ser apresentado por todos os contribuintes adquirentes dos serviços relacionados, que utilizem os documentos previstos para este registro, cuja operação dê direito à apuração de crédito à pessoa jurídica contratante, na forma da legislação tributária.
1. As seguintes operações de transportes dão direito a crédito, básicos ou presumidos, de acordo com a legislação e atos normativos aplicáveis ao PIS/Pasep e à Cofins:
- Fretes incorridos nas operações de revenda de mercadorias e produtos, quando o ônus for suportado pela pessoa jurídica comercial titular da escrituração (contratação de frete para a entrega da mercadoria revendida ao adquirente);
- Fretes incorridos nas operações de venda de bens e produtos fabricados a pessoa jurídica titular da escrituração, quando o ônus for suportado pela pessoa jurídica titular da escrituração (contratação de frete para a entrega de bens e produtos vendidos ao adquirente).
- Crédito presumido a ser apurado pelas empresas de serviço de transporte rodoviário de carga, decorrente de operação de subcontratação de serviço de transporte de carga prestado por pessoa física, transportador autônomo, ou por pessoa jurídica transportadora optante pelo Simples, conforme disposto nos §§ 19 e 20 do art. 3º da Lei nº 10.833, de 2003, calculado mediante a aplicação das alíquotas de 1,2375 % (PIS/Pasep) e de 5,7%, conforme Tabela 4.3.17.
IMPORTANTE:
1. Os gastos com transporte na aquisição das mercadorias podem compor a base de cálculo dos créditos não cumulativos, uma vez que consoante a boa técnica contábil e a legislação fiscal (art. 289, § 1º, do RIR/1999) integra o custo de aquisição das mercadorias adquiridas, o frete, quando pago pela pessoa jurídica adquirente.
2. O valor do frete pago pela pessoa jurídica na aquisição de mercadorias pode, assim, compor a base de cálculo do crédito referente às aquisições dos bens objeto de informação em C170 (escrituração por documento fiscal) ou em C191/C195 (escrituração consolidada), nos correspondentes campos de Base de Cálculo do crédito, reajustando o valor de aquisição dos bens, com o acréscimo do valor do frete.
3. Alternativamente á escrituração do crédito referente aos fretes pagos na aquisição de mercadorias, diretamente nos registros C170 ou C191/C195, poderá a pessoa jurídica proceder à escrituração dos créditos sobre os fretes na aquisição de mercadorias acima referido, no registro D100 e filhos. Neste caso, deve ser informado nos registros D101/D105, no campo 02 (IND_NAT_FRT), o indicador “2”.
4. As seguintes operações de transportes não estão relacionadas na legislação e atos normativos aplicáveis ao PIS/Pasep e à Cofins, como operações com direito à apuração de crédito:
- Os gastos com transporte do produto, acabado ou em elaboração, entre estabelecimentos industriais ou distribuidores da mesma pessoa jurídica (transferências de mercadorias e produtos);
- O transporte de bens recebidos em devolução, realizado do estabelecimento do comprador para o do vendedor.
Validação do Registro: não podem ser informados dois ou mais registros com a combinação de mesmos valores dos campos :
1. emissão de terceiros : IND_EMIT+NUM_DOC+COD_MOD+SER+SUB+COD_PART;
2. emissão própria: IND_EMIT+NUM_DOC+COD_MOD+SER+SUB.
Para cada documento informado e relacionado em cada registro D100, obrigatoriamente deve ser apresentado o detalhamento das informações, por item do documento, referentes ao PIS/Pasep (D101) e à Cofins (D105).

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D100" | C | 004* | - | S |
| 02 | IND_OPER | Indicador do tipo de operação: 0- Aquisição | C | 001* | - | S |
| 03 | IND_EMIT | Indicador do emitente do documento fiscal: 0- Emissão Própria; 1- Emissão por Terceiros | C | 001* | - | S |
| 04 | COD_PART | Código do participante (campo 02 do Registro 0150). | C | 060 | - | S |
| 05 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 06 | COD_SIT | Código da situação do documento fiscal, conforme a Tabela 4.1.2 | N | 002* | - | S |
| 07 | SER | Série do documento fiscal | C | 004 | - | N |
| 08 | SUB | Subsérie do documento fiscal | C | 003 | - | N |
| 09 | NUM_DOC | Número do documento fiscal | N | 009 | - | S |
| 10 | CHV_CTE | Chave do Conhecimento de Transporte Eletrônico | N | 044* | - | N |
| 11 | DT_DOC | Data de referência/emissão dos documentos fiscais | N | 008* | - | S |
| 12 | DT_A_P | Data da aquisição ou da prestação do serviço | N | 008* | - | N |
| 13 | TP_CT-e | Tipo de Conhecimento de Transporte Eletrônico conforme definido no Manual de Integração do CT-e | N | 001* | - | N |
| 14 | CHV_CTE_REF | Chave do CT-e de referência cujos valores foram complementados (opção “1” do campo anterior) ou cujo débito foi anulado (opção “2” do campo anterior). | N | 044* | - | N |
| 15 | VL_DOC | Valor total do documento fiscal | N | - | 02 | S |
| 16 | VL_DESC | Valor total do desconto | N | - | 02 | N |
| 17 | IND_FRT | Indicador do tipo do frete: 0- Por conta de terceiros; 1- Por conta do emitente; 2- Por conta do destinatário; 9- Sem cobrança de frete. | C | 001* | - | S |
| 17 | IND_FRT | Obs.: A partir de 01/07/2012 passará a ser: Indicador do tipo do frete: 0- Por conta do emitente; 1- Por conta do destinatário/remetente; 2- Por conta de terceiros; 9- Sem cobrança de frete. | C | 001* | - | S |
| 18 | VL_SERV | Valor total da prestação de serviço | N | - | 02 | S |
| 19 | VL_BC_ICMS | Valor da base de cálculo do ICMS | N | - | 02 | N |
| 20 | VL_ICMS | Valor do ICMS | N | - | 02 | N |
| 21 | VL_NT | Valor não-tributado do ICMS | N | - | 02 | N |
| 22 | COD_INF | Código da informação complementar do documento fiscal (campo 02 do Registro 0450) | C | 006 | - | N |
| 23 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Só devem ser relacionados neste registro as aquisições de serviços de transportes que, de acordo com a legislação tributária, confiram direito ao crédito do PIS/Pasep e da Cofins.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [D100]
Campo 02 - Valores válidos: [0]
Campo 03 - Valores válidos: [0, 1]
Preenchimento: informar o emitente do documento fiscal. Se o emitente for estabelecimento da própria pessoa jurídica titular da escrituração (emissão própria) informar o indicador “0”; se o emitente for terceiros informar o indicador “1”.
Campo 04 - Validação: o valor informado deve existir no campo COD_PART do registro 0150, correspondente à pessoa jurídica transportadora ou, no caso da escrituração pelas empresas de transporte de cargas, a pessoa física ou jurídica subcontratada, com direito à apuração do crédito presumido.
Campo 05 - Valores válidos: [07, 08, 8B, 09, 10, 11, 26, 27, 57, 63, 67]
Campo 06 (COD_SIT) - Valores válidos: [00, 02, 04, 05, 06, 08]
Preenchimento: verificar a descrição da situação do documento na Tabela “4.1.2 - Tabela Situação do Documento” integrante deste Guia Prático.
Campo 09 - Validação: o valor informado no campo deve ser maior que “0” (zero). Na impossibilidade de informar o número específico do documento fiscal, o campo deve ser preenchido com o conteúdo “000000000”.
Campo 10 - Preenchimento: informar a chave do conhecimento de transporte eletrônico, para documentos de COD_MOD igual a “57” de emissão própria ou de terceiros. O campo CHV_CTE, passa a ser de preenchimento obrigatório a partir de abril de 2012 em todas as situações.
OBS: Tendo em vista que o preenchimento desse campo não é obrigatório, em relação aos períodos de apuração ocorridos até 31 de março de 2012, caso a versão utilizada do PVA da EFD-Contribuições, neste período, não valide a informação da chave do CT-e, no caso de emissão de terceiros, deve a pessoa jurídica deixar o campo em branco, sem a informação da Chave, para a validação e transmissão da escrituração.
Validação: É conferido o dígito verificador (DV) da chave do documento eletrônico. Será verificada a consistência da raiz de CNPJ e UF do emissor com a raiz de CNPJ e UF contida na chave do documento eletrônico.  Será verificada a consistência da informação dos campos COD_MOD, NUM_DOC e SER com o número do documento e série contidos na chave do documento eletrônico.
Campo 11 - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”; excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data da aquisição do serviço (campo 12) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 12 - Preenchimento: informar a data de aquisição do serviço de transporte no formato “ddmmaaaa”,
excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data de emissão do documento fiscal (campo 11) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 13 - Preenchimento: informar o tipo de CT-e quando o modelo do documento for “57”.
Campo 14 - Preenchimento: Não preencher, informar campo “vazio”.
Campo 17 – Valores válidos: [0, 1, 2, 9]
Preenchimento: Para as escriturações referentes a períodos a partir de 01/07/2012, deve a pessoa jurídica usar o indicador “2 – Por conta de terceiros” para os casos em que o tomador do serviço de transporte é diferente do emitente ou do destinatário.
Tem-se por tomador quem efetuou o contrato junto à transportadora, arcando com o valor do serviço. Somente a este deve ser enviada a primeira via do conhecimento e só ele terá direito ao crédito, atendidas as condições da legislação quanto ao direito de crédito.
Quando o serviço de transporte ocorrer por conta da própria pessoa emissora do respectivo conhecimento/documento de transporte, deve ser informado neste campo o indicador “0 – Por conta do emitente”.
No sentido de harmonizar o conteúdo dos campos de registros comuns à EFD-Contribuições e à EFD (ICMS/IPI), a partir de 01/07/2012 os indicadores do Campo 17 passam a ter a seguinte descrição, conforme alteração promovida na EFD (ICMS/IPI):

| 17 | IND_FRT | Indicador do tipo do frete: 0- Por conta do emitente; 1- Por conta do destinatário/remetente; 2- Por conta de terceiros; 9- Sem frete. | C | 001* | - | S |
| --- | --- | --- | --- | --- | --- | --- |

Campo 18 – Preenchimento: o valor informado, em havendo, deve englobar pedágio e demais despesas.
Campo 19 - Validação: este valor deve corresponder ao resultado da diferença entre o campo VL_SERV e o VL_NT.
Campo 22 - Validação: o valor informado no campo deve existir no registro 0450.
Campo 23 - Preenchimento: deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D100 -->
<!-- Start Registro D101 -->
Registro D101: Complemento do Documento de Transporte (Códigos 07, 08, 8B, 09, 10, 11, 26, 27, 57, 63 e 67) – PIS/Pasep
Serão escrituradas neste registro as informações referentes à incidência, base de cálculo, alíquota e valor do crédito de PIS/Pasep, básico ou presumido, referente às operações de transporte contratadas ou subcontratadas, conforme previsto na legislação.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D101” | C | 004* | - | S |
| 02 | IND_NAT_FRT | Indicador da Natureza do Frete Contratado, referente a: 0 – Operações de vendas, com ônus suportado pelo estabelecimento vendedor; 1 – Operações de vendas, com ônus suportado pelo adquirente; 2 – Operações de compras (bens para revenda, matérias-prima e outros produtos, geradores de crédito); 3 – Operações de compras (bens para revenda, matérias-prima e outros produtos, não geradores de crédito); 4 – Transferência de produtos acabados entre estabelecimentos da pessoa jurídica; 5 – Transferência de produtos em elaboração entre estabelecimentos da pessoa jurídica 9 – Outras. | C | 001* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 05 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | N |
| 06 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 08 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 09 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Deve ser informado um registro para cada indicador de natureza do frete.
2. No caso da base de cálculo do crédito não corresponder à totalidade do serviço de transporte contratado, por não previsão de crédito na legislação tributária, deve a pessoa jurídica informar no Campo “VL_BC_PIS” apenas o valor da operação com direito a crédito.
3. Os valores escriturados no campo de base de cálculo 06 (VL_BC_PIS), de itens com CST representativos de operações com direito a crédito, serão recuperados no Bloco M, para a demonstração das bases de cálculo dos créditos de PIS/Pasep (M105), nos Campos “VL_BC_PIS_TOT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [D101]
Campo 02 - Valor Válido: [0, 1, 2, 3, 4, 5, 9]
Preenchimento: Informar neste campo o Indicador da Natureza do Frete Contratado.
No caso de contratação de serviços de transporte cujo item se refira a transferência de mercadorias, produtos acabados ou em elaboração, entre estabelecimentos da pessoa jurídica (Indicador “4” e “5”), o Campo 04 (CST_PIS) será informado com o CST que reflita o tratamento tributário previsto na legislação que disciplina os créditos do regime não cumulativo. As operações que não tem previsão de apuração de crédito devem ser informadas com o CST “70” (operações de aquisição sem direito a crédito).
No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar o indicador “9- Outras”.
Campo 03 - Preenchimento: informar o valor do item constante no documento fiscal referenciado em D100.
Campo 04 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

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

OBS: No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar CST de crédito presumido (CST 60 a 66).
Campo 05 - Preenchimento: Caso seja informado código representativo de crédito no Campo 04 (CST_PIS), informar neste campo o código da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
OBS: No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar código “14 – Atividade de Transporte de Cargas – Subcontratação”.
Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item, para fins de apuração do crédito, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, Campo “VL_BC_PIS_TOT”).
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem (em percentual) aplicável para fins de apuração do crédito de PIS/Pasep, conforme o caso.
OBS: No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar a alíquota de 1,2375%, conforme especificada na Tabela 4.3.17 de alíquotas diferenciadas.
Campo 08 – Preenchimento:  informar o valor do crédito de PIS/Pasep referente ao item. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (campo 06) multiplicado pela alíquota aplicável ao item (campo 07). O resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 09 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Custos com transportes, fretes contratados, despesas de comercialização, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D101 -->
<!-- Start Registro D105 -->
Registro D105: Complemento do Documento de Transporte (Códigos 07, 08, 8B, 09, 10, 11, 26, 27, 57, 63 e 67) – Cofins
Serão escrituradas neste registro as informações referentes à incidência, base de cálculo, alíquota e valor do crédito de Cofins, básicos ou presumidos, referente às operações de transporte contratadas ou subcontratadas, conforme previsto na legislação.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D105” | C | 004* | - | S |
| 02 | IND_NAT_FRT | Indicador da Natureza do Frete Contratado, referente a: 0 – Operações de vendas, com ônus suportado pelo estabelecimento vendedor; 1 – Operações de vendas, com ônus suportado pelo adquirente; 2 – Operações de compras (bens para revenda, matérias-prima e outros produtos, geradores de crédito); 3 – Operações de compras (bens para revenda, matérias-prima e outros produtos, não geradores de crédito); 4 – Transferência de produtos acabados entre estabelecimentos da pessoa jurídica 5 – Transferência de produtos em elaboração entre estabelecimentos da pessoa jurídica 9 – Outras. | C | 001* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 05 | NAT_BC_CRED | Código da base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7 | C | 002* | - | N |
| 06 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 07 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 08 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 09 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Deve ser informado um registro para cada indicador de natureza do frete.
2. No caso da base de cálculo do crédito não corresponder à totalidade do serviço de transporte contratado, por não previsão de crédito na legislação tributária, deve a pessoa jurídica informar no Campo “VL_BC_COFINS” apenas o valor da operação com direito a crédito.
3. Os valores escriturados no campo de base de cálculo 06 (VL_BC_COFINS), de itens com CST representativos de operações com direito a crédito, serão recuperados no Bloco M, para a demonstração das bases de cálculo dos créditos de Cofins (M505), nos Campos “VL_BC_COFINS_TOT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [D105]
Campo 02 - Valor Válido: [0, 1, 2, 3, 4, 5, 9]
Preenchimento: Informar neste campo o Indicador da Natureza do Frete Contratado.
No caso de contratação de serviços de transporte cujo item se refira a transferência de mercadorias, produtos acabados ou em elaboração, entre estabelecimentos da pessoa jurídica (Indicador “4” e “5”), o Campo 04 (CST_COFINS) será informado com o CST que reflita o tratamento tributário previsto na legislação que disciplina os créditos do regime não cumulativo. As operações que não tem previsão de apuração de crédito devem ser informadas com o CST “70” (operações de aquisição sem direito a crédito).
No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar o indicador “9- Outras”.
Campo 03 - Preenchimento: informar o valor do item constante no documento fiscal referenciado em D100.
Campo 04 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

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

OBS: No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar CST de crédito presumido (CST 60 a 66).
Campo 05 - Preenchimento: Caso seja informado código representativo de crédito no Campo 04 (CST_COFINS), informar neste campo o código da base de cálculo do crédito, conforme a Tabela “4.3.7 – Base de Cálculo do Crédito” referenciada no Manual do Leiaute da EFD-Contribuições e disponibilizada no Portal do SPED no sítio da RFB na Internet, no endereço <http://sped.rfb.gov.br>.
OBS: No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar código “14 – Atividade de Transporte de Cargas – Subcontratação”.
Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item, para fins de apuração do crédito, conforme o caso.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de Cofins (M505, Campo “VL_BC_COFINS_TOT”).
Campo 07 - Preenchimento: informar neste campo o valor da alíquota ad valorem (em percentual) aplicável para fins de apuração do crédito de Cofins, conforme o caso.
OBS: No caso da subcontratação de serviços de transporte, pelas pessoas jurídicas de transporte de cargas, informar a alíquota de 5,7%, conforme especificada na Tabela 4.3.17 de alíquotas diferenciadas.
Campo 08 – Preenchimento:  informar o valor do crédito de Cofins referente ao item. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (campo 06) multiplicado pela alíquota aplicável ao item (campo 07). O resultado deverá ser dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo 08 “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 09 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Custos com transportes, fretes contratados, despesas de comercialização, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D105 -->
<!-- Start Registro D111 -->
Registro D111: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro "D111", deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D111" | C | 004* | - | S |
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
Campo 01 - Valor Válido: [D111]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro D111 -->
<!-- Start Registro D200 -->
Registro D200: Resumo da Escrituração Diária – Prestação de Serviços de Transporte: Nota Fiscal de Serviço de Transporte (Código 07), Conhecimento de Transporte Rodoviário de Cargas (Código 08), Conhecimento de Transporte de Cargas Avulso (Código 8B), Conhecimento de Transporte Aquaviário de Cargas (Código 09), Conhecimento de Transporte Aéreo (Código 10), Conhecimento de Transporte Ferroviário de Cargas (Código 11), Conhecimento de Transporte Multimodal de Cargas (Código 26), Nota Fiscal de Transporte Ferroviário de Carga (Código 27), Conhecimento de Transporte Eletrônico – CT-E (Código 57), Bilhete de Passagem Eletrônico - BP-e (Código 63) e Conhecimento de Transporte Eletrônico para Outros Serviços – CT-e OS, modelo 67.
Escriturar neste registro a consolidação diária dos documentos fiscais válidos, referentes à prestação de serviços de transportes no período da escrituração.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D200" | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 03 | COD_SIT | Código da situação do documento fiscal, conforme a Tabela 4.1.2 | N | 002* | - | S |
| 04 | SER | Série do documento fiscal | C | 004 | - | N |
| 05 | SUB | Subsérie do documento fiscal | C | 003 | - | N |
| 06 | NUM_DOC_INI | Número do documento fiscal inicial emitido no período (mesmo modelo, série e subsérie). | N | 009 | - | S |
| 07 | NUM_DOC_FIN | Número do documento fiscal final emitido no período (mesmo modelo, série e subsérie). | N | 009 | - | S |
| 08 | CFOP | Código Fiscal de Operação e Prestação conforme tabela indicada no item 4.2.2 | N | 004* | - | S |
| 09 | DT_REF | Data do dia de referência do resumo diário | N | 008* | - | S |
| 10 | VL_DOC | Valor total dos documentos fiscais | N | - | 02 | S |
| 11 | VL_DESC | Valor total dos descontos | N | - | 02 | N |

Observações: Devem ser informados apenas os documentos fiscais válidos.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [D200]
Campo 02 - Valores válidos: [07, 08, 8B, 09, 10, 11, 26, 27, 57, 63 e 67]
Campo 03 - Valores válidos: [00, 01, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Tabela “4.1.2 - Tabela Situação do Documento” integrante deste Guia Prático. Não deve ser considerado no Resumo Diário (D200) os documentos fiscais cancelados, denegados ou de numeração inutilizada.
Campo 04 - Preenchimento: informar a série dos documentos fiscais consolidados, se houver.
Campo 05 - Preenchimento: informar a subsérie dos documentos fiscais consolidados, se houver.
Campo 06 - Preenchimento: informar o número do documento fiscal inicial a que se refere a consolidação diária.
Validação: valor informado deve ser maior que “0” (zero). O número do documento inicial deve ser menor ou igual ao número do documento final.
Campo 07 - Preenchimento: informar o número do documento fiscal final a que se refere a consolidação diária.
Validação: valor informado deve ser maior que “0” (zero). O número do documento final deve ser maior ou igual ao número do documento inicial.
Campo 08 – Preenchimento:  Informar o CFOP correspondente aos documentos fiscais consolidados no registro.
Campo 09 - Preenchimento: informar a data de referência da consolidação diária, no formato “ddmmaaaa”; excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 10 – Preenchimento: informar o valor total dos documentos fiscais consolidados neste registro.
Campo 11 – Preenchimento: informar o valor total dos descontos, constantes nos documentos fiscais consolidados neste registro.
<!-- End Registro D200 -->
<!-- Start Registro D201 -->
Registro D201: Totalização do Resumo Diário – PIS/Pasep
Serão escrituradas neste registro as informações referentes à incidência, base de cálculo, alíquota e valor do PIS/Pasep, referente às operações de transporte consolidadas em D200.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D201" | C | 004* | - | S |
| 02 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 05 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 06 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 07 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Em relação aos itens com CST representativos de receitas, os valores dos campos de bases de cálculo, VL_BC_PIS (Campo 04) serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), no Campo “VL_BC_CONT”.
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [D201]
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
Campo 04 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à consolidação diária. O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 05 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (0,65% ou 1,65%), conforme o caso.
Campo 06 – Preenchimento: informar o valor do PIS/Pasep apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 07 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Receita de Fretes, Receitas operacionais, receita de transportes rodoviário de cargas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D201 -->
<!-- Start Registro D205 -->
Registro D205: Totalização do Resumo Diário – Cofins
Serão escrituradas neste registro as informações referentes à incidência, base de cálculo, alíquota e valor da Cofins, referente às operações de transporte consolidadas em D200.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D205" | C | 004* | - | S |
| 02 | CST_COFINS | Código da Situação Tributária referente a COFINS. | N | 002* | - | S |
| 03 | VL_ITEM | Valor total dos itens | N | - | 02 | S |
| 04 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 05 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 06 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 07 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações: Em relação aos itens com CST representativos de receitas, os valores dos campos de bases de cálculo, VL_BC_COFINS (Campo 04) serão recuperados no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), no Campo “VL_BC_CONT”.
Nível hierárquico - 4
Ocorrência – 1:N
Campo 01 - Valor Válido: [D205]
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
Campo 04 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à consolidação diária. O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 05 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (3% ou 7,6%), conforme o caso.
Campo 06 – Preenchimento: informar o valor da Cofins apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo  “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 07 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Receita de Fretes, Receitas operacionais, receita de transportes rodoviário de cargas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D205 -->
<!-- Start Registro D209 -->
Registro D209: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “D209”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D209" | C | 004* | - | S |
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
Campo 01 - Valor Válido: [D209]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro D209 -->
<!-- Start Registro D300 -->
Registro D300: Resumo da Escrituração Diária - Bilhetes Consolidados de Passagem Rodoviário (Código 13), de Passagem Aquaviário (Código 14), de Passagem e Nota de Bagagem (Código 15), de Passagem Ferroviário (Código 16) e Resumo de Movimento Diário (Código 18)
Escriturar neste registro a consolidação diária dos documentos fiscais válidos, códigos 13, 14, 15, 16 e 18, referentes aos serviços de transportes no período da escrituração.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D300" | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1. | C | 002* | - | S |
| 03 | SER | Série do documento fiscal | C | 004 | - | N |
| 04 | SUB | Subsérie do documento fiscal | N | 003 | - | N |
| 05 | NUM_DOC_INI | Número do primeiro documento fiscal emitido no período (mesmo modelo, série e subsérie) | N | 006 | - | N |
| 06 | NUM_DOC_FIN | Número do último documento fiscal emitido no período (mesmo modelo, série e subsérie) | N | 006 | - | N |
| 07 | CFOP | Código Fiscal de Operação e Prestação conforme tabela indicada no item 4.2.2 | N | 004* | - | S |
| 08 | DT_REF | Data do dia de referência do resumo diário | N | 008* | - | S |
| 09 | VL_DOC | Valor total dos documentos fiscais emitidos | N | - | 02 | S |
| 10 | VL_DESC | Valor total dos descontos | N | - | 02 | N |
| 11 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 12 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 13 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 14 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 15 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 16 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 17 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 18 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 19 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
Em relação aos itens com CST representativos de receitas, os valores dos Campos de bases de cálculo, VL_BC_PIS (Campo 12) e VL_BC_COFINS (Campo 16) serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210) e da Cofins (M610), no Campo “VL_BC_CONT”.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [D300]
Campo 02 - Valores válidos: [13, 14, 15, 16, 18]
Campo 03 - Preenchimento: informar a série dos documentos fiscais consolidados, se houver.
Campo 04 - Preenchimento: informar a subsérie dos documentos fiscais consolidados, se houver.
Campo 05 - Preenchimento: informar o número do documento fiscal inicial a que se refere a consolidação diária.
Validação: valor informado deve ser maior que “0” (zero). O número do documento inicial deve ser menor ou igual ao número do documento final.
Campo 06 - Preenchimento: informar o número do documento fiscal final a que se refere a consolidação diária.
Validação: valor informado deve ser maior que “0” (zero). O número do documento final deve ser maior ou igual ao número do documento inicial.
Campo 07 – Preenchimento: Informar o CFOP correspondente aos documentos fiscais consolidados no registro.
Campo 08 - Preenchimento: informar a data de referência da consolidação diária, no formato “ddmmaaaa”; excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 09 – Preenchimento: informar o valor total dos documentos fiscais consolidados neste registro.
Campo 10 – Preenchimento: informar o valor total dos descontos, constantes nos documentos fiscais consolidados neste registro.
Campo 11 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 12 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à consolidação diária. O valor deste campo referente às receitas da consolidação diária será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 13 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (0,65% ou 1,65%), conforme o caso.
Campo 14 – Preenchimento: informar o valor do PIS/Pasep apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 15 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 16 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à consolidação diária. O valor deste campo referente às receitas da consolidação diária será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 17 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (3% ou 7,6%), conforme o caso.
Campo 18 – Preenchimento: informar o valor da Cofins apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo  “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 19 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Serviços de transportes, Receita de Fretes, Receitas operacionais, receita de transporte rodoviário de cargas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D300 -->
<!-- Start Registro D309 -->
Registro D309: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “D309”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referente ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D309" | C | 004* | - | S |
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
Campo 01 - Valor Válido: [D309]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro D309 -->
<!-- Start Registro D350 -->
Registro D350: Resumo Diário de Cupom Fiscal Emitido Por ECF - (Código: 2E, 13, 14, 15 e 16)
Deve ser escriturada neste registro a consolidação diária das operações referentes serviços de transportes, objeto de registro nos documentos fiscais códigos 2E, 13, 14, 15 e 16), emitidos por equipamentos de ECF.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D350" | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1 | C | 002* | - | S |
| 03 | ECF_MOD | Modelo do equipamento | C | 020 | - | S |
| 04 | ECF_FAB | Número de série de fabricação do ECF | C | 021 | - | S |
| 05 | DT_DOC | Data do movimento a que se refere a Redução Z | N | 008* | - | S |
| 06 | CRO | Posição do Contador de Reinício de Operação | N | 003 | - | S |
| 07 | CRZ | Posição do Contador de Redução Z | N | 006 | - | S |
| 08 | NUM_COO_FIN | Número do Contador de Ordem de Operação do último documento emitido no dia. (Número do COO na Redução Z) | N | 006 | - | S |
| 09 | GT_FIN | Valor do Grande Total final | N | - | 02 | S |
| 10 | VL_BRT | Valor da venda bruta | N | - | 02 | S |
| 11 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 12 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 13 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 14 | QUANT_BC_PIS | Quantidade – Base de cálculo PIS/PASEP | N | - | 03 | N |
| 15 | ALIQ_PIS_QUANT | Alíquota do PIS/PASEP (em reais) | N | - | 04 | N |
| 16 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 17 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 18 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 19 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 20 | QUANT_BC_COFINS | Quantidade – Base de cálculo da COFINS | N | - | 03 | N |
| 21 | ALIQ_COFINS_QUANT | Alíquota da COFINS (em reais) | N | - | 04 | N |
| 22 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 23 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
1. Os valores escriturados nos campos de bases de cálculo 12 (VL_BC_PIS) e 14 (QUANT_BC_PIS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT” e “QUANT_BC_PIS_TOT”, respectivamente.
2. Os valores escriturados nos campos de bases de cálculo 18 (VL_BC_COFINS) e 20 (QUANT_BC_COFINS), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT” e “QUANT_BC_COFINS_TOT”, respectivamente.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 - Valor Válido: [D350]
Campo 02 - Valores válidos: [2E, 13, 14, 15, 16]
Campo 05 - Preenchimento: considerar a data do movimento, que inclui as operações de venda realizadas durante operíodo de tolerância do Equipamento ECF, no formato “ddmmaaaa”, sem os caracteres de separação, tais como: ".", "/", "-".
Validação: o valor informado deve ser menor ou igual à DT_FIN deste arquivo.
Campo 06 – Preenchimento: Informar a posição do Contador de Reinício de Operação.
Validação: o valor informado deve ser maior que “0” (zero).
Campo 07 – Preenchimento: Informar a posição do Contador de Redução Z.
Validação: o valor informado deve ser maior que “0” (zero).
Campo 08 – Preenchimento:  Informar o número do Contador de Ordem de Operação do último documento emitido no dia.
Validação: o valor informado deve ser maior que “0” (zero).
Campo 09 - Preenchimento: informar o valor acumulado no totalizador de venda bruta.
Campo 10 - Preenchimento: informar o valor total da venda bruta, objeto da consolidação diária.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 11 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 12 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente à consolidação diária. O valor deste campo referente às receitas da consolidação diária será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 13 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (0,65% ou 1,65%), conforme o caso.
Campo 14 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep em quantidade, referente à consolidação diária, quando for o caso.
Campo 15 - Preenchimento: informar neste campo o valor da alíquota em reais, para fins de apuração da contribuição sobre a base de calculo informada no campo 14, conforme o caso.
Campo 16 – Preenchimento: informar o valor do PIS/Pasep apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Campo 17 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.
Campo 18 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente à consolidação diária. O valor deste campo referente às receitas da consolidação diária será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 19 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração da contribuição (3% ou 7,6%), conforme o caso.
Campo 20 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins em quantidade, referente à consolidação diária, quando for o caso.
Campo 21 - Preenchimento:  informar neste campo o valor da alíquota em reais, para fins de apuração da contribuição sobre a base de cálculo informada no campo 20, conforme o caso.
Campo 22 – Preenchimento: informar o valor da Cofins apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Campo 23 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Serviços de transportes, Receita de Fretes, Receitas operacionais, receita de transportes rodoviário de cargas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D350 -->
<!-- Start Registro D359 -->
Registro D359: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “D359”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D359" | C | 004* | - | S |
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
Campo 01 - Valor Válido: [D359]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro D359 -->
<!-- Start Registro D500 -->
Registro D500: Nota Fiscal de Serviço de Comunicação (Código 21) e Nota Fiscal de Serviço de Telecomunicação (Código 22) – Documentos de Aquisição com Direito a Crédito
Neste registro deverá a pessoa jurídica informar as operações referentes à contratação de serviços de comunicação ou de telecomunicação que, em função da natureza do serviço e da atividade econômica desenvolvida pela pessoa jurídica, permita a apuração de créditos de PIS/Pasep e de Cofins, na forma da legislação tributária.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D500" | C | 004* | - | S |
| 02 | IND_OPER | Indicador do tipo de operação: 0- Aquisição | C | 001* | - | S |
| 03 | IND_EMIT | Indicador do emitente do documento fiscal: 0- Emissão própria; 1- Terceiros | C | 001* | - | S |
| 04 | COD_PART | Código do participante prestador do serviço (campo 02 do Registro 0150). | C | 060 | - | S |
| 05 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1. | C | 002* | - | S |
| 06 | COD_SIT | Çódigo da situação do documento fiscal, conforme a Tabela 4.1.2. | N | 002* | - | S |
| 07 | SER | Série do documento fiscal | C | 004 | - | N |
| 08 | SUB | Subsérie do documento fiscal | N | 003 | - | N |
| 09 | NUM_DOC | Número do documento fiscal | N | 009 | - | S |
| 10 | DT_DOC | Data da emissão do documento fiscal | N | 008* | - | S |
| 11 | DT_A_P | Data da entrada (aquisição) | N | 008* | - | S |
| 12 | VL_DOC | Valor total do documento fiscal | N | - | 02 | S |
| 13 | VL_DESC | Valor total do desconto | N | - | 02 | N |
| 14 | VL_SERV | Valor da prestação de serviços | N | - | 02 | S |
| 15 | VL_SERV_NT | Valor total dos serviços não-tributados pelo ICMS | N | - | 02 | N |
| 16 | VL_TERC | Valores cobrados em nome de terceiros | N | - | 02 | N |
| 17 | VL_DA | Valor de outras despesas indicadas no documento fiscal | N | - | 02 | N |
| 18 | VL_BC_ICMS | Valor da base de cálculo do ICMS | N | - | 02 | N |
| 19 | VL_ICMS | Valor do ICMS | N | - | 02 | N |
| 20 | COD_INF | Código da informação complementar (campo 02 do Registro 0450) | C | 006 | - | N |
| 21 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 22 | VL_COFINS | Valor da COFINS | N | - | 02 | N |

Observações:
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [D500]
Campo 02 - Valores válidos: [0]
Campo 03 - Valores válidos: [0, 1]
Preenchimento: informar o emitente do documento fiscal. Se o emitente for estabelecimento da própria pessoa jurídica titular da escrituração (emissão própria) informar o indicador “0”; se o emitente for terceiros informar o indicador “1”.
Campo 04 - Validação: o valor informado deve existir no campo COD_PART do registro 0150.
Campo 05 - Valores válidos: [21, 22]
Campo 06 - Valores válidos: [00, 01, 02, 03, 06, 07, 08]
Preenchimento: verificar a descrição da situação do documento na Tabela Situação do Documento, integrante deste Guia Prático.
Campo 07 – Preenchimento: Informar neste campo a série do documento fiscal, se existir.
Campo 08 – Preenchimento:  Informar neste campo a subsérie do documento fiscal, se existir.
Campo 09 – Preenchimento: Informar neste campo o número do documento fiscal de aquisição de serviço de comunicação ou de telecomunicação com direito a crédito.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 10 - Preenchimento: informar a data de emissão do documento, no formato “ddmmaaaa”; excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data da aquisição do serviço (campo 11) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 11 - Preenchimento: informar a data de aquisição do serviço no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: a data informada neste campo ou a data de emissão do documento fiscal (campo 10) deve estar compreendida no período da escrituração (campos 06 e 07 do registro 0000). Regra aplicável na validação/edição de registros da escrituração, a ser gerada com a versão 1.0.2 do Programa Validador e Assinador da EFD-Contribuições.
Campo 12 - Preenchimento: Informar neste campo o valor do documento fiscal com direito à apuração de crédito.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 14 - Preenchimento: Informar neste campo o valor da prestação de serviço constante no documento fiscal.
Campo 17 - Preenchimento: Informar neste campo o valor de outras despesas/valores constantes no documento fiscal, que não sejam as informadas no campo 14.
Campo 19 - Preenchimento: Informar neste campo o valor do total do ICMS.
Campo 21 - Preenchimento:  Informar neste campo o valor do total do PIS/Pasep.
Campo 22 - Preenchimento: Informar neste campo o valor da Cofins.
<!-- End Registro D500 -->
<!-- Start Registro D501 -->
Registro D501: Complemento da Operação (Códigos 21 e 22) – PIS/Pasep
1. Deve ser escriturado um registro D501 para cada item (serviço de comunicação ou de telecomunicação) cuja operação dê direito a crédito, pelo seu valor total ou parcial;
2. Caso em relação a um mesmo item venha a ocorrer tratamentos tributários diversos (mais de um CST), deve a pessoa jurídica informar um registro D501 para cada CST;
3. Em relação aos itens com CST representativos de operações geradoras de créditos, os valores do campo de base de cálculo “VL_BC_PIS” (Campo 05) serão recuperados no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (Registro M105), no campo “VL_BC_PIS_TOT”.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D501” | C | 004* | - | S |
| 02 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 03 | VL_ITEM | Valor Total dos Itens (Serviços) | N | - | 02 | S |
| 04 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | N |
| 05 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 06 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 07 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 08 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [D501]
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
| 03 | Aquisição de serviços utilizados como insumo |
| 13 | Outras operações com direito a crédito |

Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item do documento fiscal.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito de PIS/Pasep (M105, campo “VL_BC_PIS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito do crédito (1,65%), conforme o caso.
Campo 07 – Preenchimento: informar o valor do crédito de PIS/Pasep referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_PIS” deve corresponder ao valor da base de cálculo (VL_BC_PIS) multiplicado pela alíquota aplicável ao item (ALIQ_PIS), dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 08 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Serviços prestados por pessoa jurídica, outros custos, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D501 -->
<!-- Start Registro D505 -->
Registro D505: Complemento da Operação (Códigos 21 e 22) – Cofins
1. Deve ser escriturado um registro D505 para cada item (serviço de comunicação ou de telecomunicação) cuja operação dê direito a crédito, pelo seu valor total ou parcial;
2. Caso em relação a um mesmo item venha a ocorrer tratamentos tributários diversos (mais de um CST), deve a pessoa jurídica informar um registro D505 para cada CST;
3. Em relação aos itens com CST representativos de operações geradoras de créditos, os valores do campo de base de cálculo “VL_BC_COFINS” (Campo 05) serão recuperados no Bloco M, para a demonstração das bases de cálculo do crédito da Cofins (Registro M505), no campo “VL_BC_PIS_TOT”.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D505” | C | 004* | - | S |
| 02 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 03 | VL_ITEM | Valor Total dos Itens | N | - | 02 | S |
| 04 | NAT_BC_CRED | Código da Base de Cálculo do Crédito, conforme a Tabela indicada no item 4.3.7. | C | 002* | - | N |
| 05 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 06 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008 | 04 | N |
| 07 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 08 | COD_CTA | Código da conta analítica contábil debitada/creditada | C | 255 | - | N |

Observações:
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [D505]
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
| 03 | Aquisição de serviços utilizados como insumo |
| 13 | Outras operações com direito a crédito |

Campo 05 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item do documento fiscal.
O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do crédito da Cofins (M505, campo “VL_BC_COFINS_TOT”) no caso de item correspondente a fato gerador de crédito.
Campo 06 - Preenchimento: informar neste campo o valor da alíquota aplicável para fins de apuração do crédito do crédito (7,6%), conforme o caso.
Campo 07 – Preenchimento: informar o valor do crédito de Cofins referente ao item do documento fiscal. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor do crédito apurado. O cálculo do valor do crédito no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CRED em M100/M500.
Validação: o valor do campo “VL_COFINS” deve corresponder ao valor da base de cálculo (VL_BC_COFINS) multiplicado pela alíquota aplicável ao item (ALIQ_COFINS), dividido pelo valor “100”.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 08 - Preenchimento: informar o Código da Conta Analítica. Exemplos: : Serviços prestados por pessoa jurídica, outros custos , etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D505 -->
<!-- Start Registro D509 -->
Registro D509: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “D509”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referentes ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D509" | C | 004* | - | S |
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
Campo 01 - Valor Válido: [D509]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro D509 -->
<!-- Start Registro D600 -->
Registro D600: Consolidação da Prestação de Serviços - Notas de Serviço de Comunicação (Código 21) e de Serviço de Telecomunicação (Código 22)
Neste registro será informada a consolidação das receitas auferidas pelas empresas de comunicação e de telecomunicação, de acordo com a natureza dos serviços prestados.
Devem ser objeto de escrituração as receitas efetivamente realizadas, mesmo que ainda a faturar, desde que os serviços já tenham sido prestados ao consumidor dos mesmos. Desta forma, as receitas de serviços de comunicação e de telecomunicação a faturar em período futuro (mês seguinte, por exemplo), devem ser escrituradas em D600 e não, em F100.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D600" | C | 004* | - | S |
| 02 | COD_MOD | Código do modelo do documento fiscal, conforme a Tabela 4.1.1. | C | 002* | - | S |
| 03 | COD_MUN | Código do município dos terminais faturados, conforme a tabela IBGE | N | 007* | - | N |
| 04 | SER | Série do documento fiscal | C | 004 | - | N |
| 05 | SUB | Subsérie do documento fiscal | N | 003 | - | N |
| 06 | IND_REC | Indicador do tipo de receita: 0- Receita própria - serviços prestados; 1- Receita própria - cobrança de débitos; 2- Receita própria - venda de serviço pré-pago – faturamento de períodos anteriores; 3- Receita própria - venda de serviço pré-pago – faturamento no período; 4- Outras receitas próprias de serviços de comunicação e telecomunicação; 5- Receita própria - co-faturamento; 6- Receita própria – serviços a faturar em período futuro; 7– Outras receitas próprias de natureza não-cumulativa; 8 - Outras receitas de terceiros 9 – Outras receitas | N | 001* | - | S |
| 07 | QTD_CONS | Quantidade de documentos consolidados neste registro | N | - | - | S |
| 08 | DT_DOC_INI | Data Inicial dos documentos consolidados no período | N | 008* | - | S |
| 09 | DT_DOC_FIN | Data Final dos documentos consolidados no período | N | 008* | - | S |
| 10 | VL_DOC | Valor total acumulado dos documentos fiscais | N | - | 02 | S |
| 11 | VL_DESC | Valor acumulado dos descontos | N | - | 02 | N |
| 12 | VL_SERV | Valor acumulado das prestações de serviços tributados pelo ICMS | N | - | 02 | S |
| 13 | VL_SERV_NT | Valor acumulado dos serviços não-tributados pelo ICMS | N | - | 02 | N |
| 14 | VL_TERC | Valores cobrados em nome de terceiros | N | - | 02 | N |
| 15 | VL_DA | Valor acumulado das despesas acessórias | N | - | 02 | N |
| 16 | VL_BC_ICMS | Valor acumulado da base de cálculo do ICMS | N | - | 02 | N |
| 17 | VL_ICMS | Valor acumulado do ICMS | N | - | 02 | N |
| 18 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 19 | VL_COFINS | Valor da COFINS | N | - | 02 | N |

Observações: Não precisam ser incluídos na consolidação do Registro D600 os documentos fiscais que não correspondam a receitas efetivamente auferidas, tais como os documentos cancelados.
Nível hierárquico - 3
Ocorrência – 1:N
Campo 01 - Valor Válido: [D600]
Campo 02 - Valores válidos: [21, 22]
Preenchimento: informar o Código do modelo do documento fiscal, conforme a Tabela 4.1.1
Campo 03 - Preenchimento: informar o código do município dos terminais faturados.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
Campo 04 – Preenchimento: informar a Série do documento fiscal objeto da consolidação, se houver.
Campo 05 – Preenchimento: informar a Subsérie do documento fiscal objeto da consolidação, se houver.
Campo 06 - Preenchimento: Informar neste campo o indicador da natureza da receita consolidada neste registro.
Valores Válidos: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
0 - RECEITA PRÓPRIA – SERVIÇOS PRESTADOS:
Indicar as receitas próprias auferidas e suportadas por NOTAS FISCAIS DE SERVIÇOS DE TELECOMUNICAÇÃOS/COMUNICAÇÃO no período tributados pela contribuição de PIS e COFINS pelo regime cumulativo.
Caso o registro seja consolidado pela contabilidade neste código deverá ser registrado a receita bruta de telecomunicação/ comunicação com incidência de PIS e COFINS pelo regime cumulativo.
1 - RECEITA PRÓPRIA – COBRANÇA DE DÉBITOS:
Este item será utilizado pela empresa que optar por consolidar as informações por documentos fiscais. Indicar valores cobrados em nota fiscal referente a cobrança de débitos anteriores, já tributados.
2 - RECEITA PRÓPRIA – VENDA DE SERVIÇO PRÉ-PAGO – FATURAMENTO DE PERÍODOS ANTERIORES
Este item será utilizado pela empresa que optar por consolidar as informações por documentos fiscais. No registro referente a este código indicador, deve a pessoa jurídica consolidar as receitas de serviços pré-pago prestadas no período da escrituração e que foram faturadas em períodos anteriores.
Este item será utilizado, por exemplo, quando o VALOR DO CONSUMO do crédito de pré-pago for maior que o total ativado no período (valor registrado no item 3).
3 – RECEITA PRÓPRIA – VENDA DE SERVIÇO PRÉ-PAGO – FATURAMENTO NO PERÍODO
Este item será utilizado pela empresa que optar por consolidar as informações por documentos fiscais.
Refere-se à ATIVAÇÃO DO CRÉDITO DO SERVIÇO PRÉ-PAGO na plataforma com emissão da NOTA FISCAL MODELO 22 de acordo com CONVÊNIO ICMS 55/2005.
Quando O VALOR DA ATIVAÇÃO do mês de referência do arquivo “FOR MAIOR” do que o VALOR CONSUMIDO no mesmo período, a diferença do valor ainda não consumido deverá ser informada no campo 04 do Registro D601 e D605 para exclusões na base de cálculo
4 – OUTRAS RECEITAS PRÓPRIAS DE SERVIÇOS DE COMUNICAÇÃO E TELECOMUNICAÇÃO
Representa outras receitas eventuais de serviços de telecomunicação/comunicação da companhia. Caso se refiram a receitas já oferecidas à tributação, em períodos de apuração anteriores, deve o seu valor ser excluído da base de cálculo nos registros filhos D601 e D605;
5 – RECEITA PRÓPRIA – CO-FATURAMENTO
Este item será utilizado pela empresa que optar por consolidar as informações por documentos fiscais.
A receita própria de co-faturamento é aquela em que outra empresa Operadora de TELECOM fatura para a empresa que está entregando o arquivo da EFD PIS/COFINS.
6 – RECEITA PRÓPRIA – SERVIÇOS A FATURAR EM PERÍODO FUTURO
Este item será utilizado pela empresa que optar por consolidar as informações por documentos fiscais.
Os serviços a faturar representam os valores dos “serviços prestados” e ainda não faturados no período (ainda sem emissão da NOTA FISCAL DE SERVIÇOS). Representam receitas já auferidas, mas ainda não faturadas em razão dos ciclos de faturamento existentes nas empresas de telecomunicação/comunicação.
Informações para a EFD:
- Fato gerador do PIS/COFINS sobre a receita “a faturar”: Deverá ser informado como Tipo de Receita 6 (Campo 06) para compor a base de cálculo do PIS/COFINS.
- Estorno da receita “a faturar” (Mês Seguinte): Com as respectivas emissões das Notas Fiscais e informadas como Tipo de Receita 0 (Campo 06) deverá ocorrer o estorno (exclusão da base de cálculo) do valor “a faturar”, demonstrado no arquivo do mês  corrente no Campo 04, nos registros D601 e D605, para exclusão da base de cálculo do PIS/COFINS.
7 – OUTRAS RECEITAS PRÓPRIAS DE NATUREZA NÃO CUMULATIVA
Informar neste item outras receitas próprias da pessoa jurídica, não referentes a serviços de telecomunicação ou comunicação, passíveis assim de tributação no regime não cumulativo.
8 – OUTRAS RECEITAS DE TERCEIROS
Este item será utilizado pela empresa que optar por consolidar as informações por documentos fiscais.
Indicar neste item os valores que não representam RECEITAS das Operadoras, mas que eventualmente estão inseridas na NOTA FISCAL DE PRESTAÇÃO DE SERVIÇOS DE TELECOMUNICAÇÃO/COMUNICAÇÃO. Esses valores não transitam pelas contas de resultado das operadoras e são contabilizados numa conta de ATIVO (a receber do cliente) contra um PASSIVO (a pagar para algum terceiro). Exemplo: assinaturas de jornais, telegramas fonados etc.
9 – OUTRAS RECEITAS
Outras receitas que não se enquadrarem nos conceitos anteriores e relacionadas com serviços de telecomunicação/comunicação.
Campo 07 - Preenchimento: Informar neste campo a quantidade de documentos consolidados.
Campo 08 - Preenchimento: informar a data de emissão inicial dos documentos consolidados no registro, representativos da prestação de serviços de comunicação e de telecomunicação, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 09 - Preenchimento: informar a data de emissão Final dos documentos consolidados no registro, representativos da prestação de serviços de comunicação e de telecomunicação, no formato “ddmmaaaa”, excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Campo 10 - Preenchimento: Informar neste campo o valor total da receita de serviços de comunicação ou de telecomunicação consolidada neste registro, correspondente ao tipo de receita informado no Campo 06 .
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 11 - Preenchimento: Informar neste campo o valor total dos descontos relacionados à receita consolidada no Campo 10.
Campo 12 - Preenchimento: Informar neste campo o valor total da receita da prestação de serviços tributados pelo ICMS, correspondente à receita consolidada no Campo 10.
Campo 13 - Preenchimento: Informar neste campo o valor total da receita da prestação de serviços não-tributados pelo ICMS, correspondente à receita consolidada no Campo 10.
Campo 14 - Preenchimento: Informar neste campo os valores totais cobrados em nome de terceiros, relacionadas às operações/documentos correspondentes à receita consolidada no Campo 10.
Campo 15 - Preenchimento: Informar neste campo o valor total das despesas acessórias relacionadas às operações/documentos correspondentes à receita consolidada no Campo 10.
Campo 16 - Preenchimento: Informar neste campo o valor acumulado da base de cálculo do ICMS.
Campo 17 - Preenchimento: Informar neste campo o valor do total do ICMS.
Campo 18 - Preenchimento: Informar neste campo o valor do total do PIS/Pasep.
Campo 19 - Preenchimento: Informar neste campo o valor da Cofins.
<!-- End Registro D600 -->
<!-- Start Registro D601 -->
Registro D601: Complemento da Consolidação da Prestação de Serviços (Códigos 21 e 22) - PIS/Pasep
Devem ser informadas neste registro as informações relacionadas à determinação da base de cálculo e do valor da Contribuição para o PIS/Pasep, dos valores consolidados no registro D600.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D601” | C | 004* | - | S |
| 02 | COD_CLASS | Código de classificação do item do serviço de comunicação ou de telecomunicação, conforme a Tabela 4.4.1 | N | 004* | - | S |
| 03 | VL_ITEM | Valor acumulado do item | N | - | 02 | S |
| 04 | VL_DESC | Valor acumulado dos descontos/exclusões da base de cálculo | N | - | 02 | N |
| 05 | CST_PIS | Código da Situação Tributária referente ao PIS/PASEP | N | 002* | - | S |
| 06 | VL_BC_PIS | Valor da base de cálculo do PIS/PASEP | N | - | 02 | N |
| 07 | ALIQ_PIS | Alíquota do PIS/PASEP (em percentual) | N | 008 | 04 | N |
| 08 | VL_PIS | Valor do PIS/PASEP | N | - | 02 | N |
| 09 | COD_CTA | Código da conta contábil debitada/creditada | C | 255 | - | N |

Observações: Os valores escriturados no campo 06 (base de cálculo), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [D601]
Campo 02 - Preenchimento: informar o código de classificação do item do serviço de comunicação ou de telecomunicação, conforme a Tabela 4.4.1 do Ato COTEPE/ICMS nº 09, de 18 de abril de 2008.
Campo 03 - Preenchimento: Informar neste campo o valor acumulado do item.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 - Preenchimento: informar o valor do desconto comercial ou dos valores a excluir da base de cálculo da contribuição, conforme o caso.
Campo 05 - Preenchimento: Informar neste campo o Código de Situação Tributária referente ao PIS/PASEP (CST), conforme a Tabela II constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

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

Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo do PIS/Pasep referente ao item consolidado. O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo do PIS/Pasep (M210), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota aplicável ao item, para fins de apuração da contribuição (0,65% ou 1,65%), conforme o caso.
Campo 08 – Preenchimento:  informar o valor do PIS/Pasep apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_PIS” = 1.000.000,00 e o Campo “ALIQ_PIS” = 1,6500 , então o Campo “VL_PIS” será igual a: 1.000.000,00 x 1,65 / 100 = 16.500,00.
Campo 09 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Receita da atividade, receita de telecomunicações, receitas de comunicações, outras receitas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D601 -->
<!-- Start Registro D605 -->
Registro D605: Complemento da Consolidação da Prestação de Serviços (Códigos 21 e 22) – Cofins
Devem ser informadas neste registro as informações relacionadas à determinação da base de cálculo e do valor da Cofins, dos valores consolidados no registro D600.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D605” | C | 004* | - | S |
| 02 | COD_CLASS | Código de classificação do item do serviço de comunicação ou de telecomunicação, conforme a Tabela 4.4.1 | N | 004* | - | S |
| 03 | VL_ITEM | Valor acumulado do item | N | - | 02 | S |
| 04 | VL_DESC | Valor acumulado dos descontos/exclusões da base de cálculo | N | - | 02 | N |
| 05 | CST_COFINS | Código da Situação Tributária referente a COFINS | N | 002* | - | S |
| 06 | VL_BC_COFINS | Valor da base de cálculo da COFINS | N | - | 02 | N |
| 07 | ALIQ_COFINS | Alíquota da COFINS (em percentual) | N | 008- | 04 | N |
| 08 | VL_COFINS | Valor da COFINS | N | - | 02 | N |
| 09 | COD_CTA | Código da conta contábil debitada/creditada | C | 255 | - | N |

Observações: Os valores escriturados no campo 06 (base de cálculo), de itens com CST representativos de receitas tributadas, serão recuperados no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Nível hierárquico - 4
Ocorrência - 1:N
Campo 01 - Valor Válido: [D605]
Campo 02 - Preenchimento: informar o código de classificação do item do serviço de comunicação ou de telecomunicação, conforme a Tabela 4.4.1 do Ato COTEPE/ICMS nº 09, de 18 de abril de 2008.
Campo 03 - Preenchimento: Informar neste campo o valor acumulado do item.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 - Preenchimento: informar o valor do desconto comercial ou dos valores a excluir da base de cálculo da contribuição, conforme o caso.
Campo 05 - Preenchimento: Informar neste campo o Código de Situação Tributária referente a Cofins (CST), conforme a Tabela III constante no Anexo Único da Instrução Normativa RFB nº 1.009, de 2010, referenciada no Manual do Leiaute da EFD-Contribuições.

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

Campo 06 - Preenchimento: informar neste campo o valor da base de cálculo da Cofins referente ao item consolidado. O valor deste campo será recuperado no Bloco M, para a demonstração das bases de cálculo da Cofins (M610), nos Campos “VL_BC_CONT”.
Para mais informações sobre os efeitos das decisões judiciais e operacionalização de ajustes de exclusão vide Seção 11 – Observações sobre os efeitos das decisões judiciais na escrituração da EFD-Contribuições e Seção 12 – Operacionalização dos ajustes de exclusão do ICMS da base de cálculo do PIS/Cofins.
Campo 07 - Preenchimento: informar neste campo o valor da alíquota aplicável ao item, para fins de apuração da contribuição (3% ou 7,6%), conforme o caso.
Campo 08 – Preenchimento:  informar o valor da Cofins apurado em relação ao item consolidado. O valor deste campo não será recuperado no Bloco M, para a demonstração do valor da contribuição devida e/ou do crédito apurado. O cálculo do valor da contribuição no bloco M é efetuado mediante a multiplicação dos campos de base de cálculo totalizados no bloco M e as respectivas alíquotas. Para maiores informações verifique as orientações de preenchimento do campo VL_CONT_APUR em M210/M610.
Exemplo: Sendo o Campo “VL_BC_COFINS” = 1.000.000,00 e o Campo “ALIQ_COFINS” = 7,6000 , então o Campo “VL_COFINS” será igual a: 1.000.000,00 x 7,6 / 100 = 76.000,00.
Campo 09 - Preenchimento: informar o Código da Conta Analítica. Exemplos: Receita da atividade, receita de telecomunicações, receitas de comunicações, outras receitas, etc. Deve ser a conta credora ou devedora principal, podendo ser informada a conta sintética (nível acima da conta analítica).
Campo de preenchimento opcional para os fatos geradores até outubro de 2017. Para os fatos geradores a partir de novembro de 2017 o campo "COD_CTA" é de preenchimento obrigatório, exceto se a pessoa jurídica estiver dispensada de escrituração contábil (ECD), como no caso da pessoa jurídica tributada pelo lucro presumido e que escritura o livro caixa (art. 45 da Lei nº 8.981/95). Vide Registro 0500: Plano de Contas Contábeis
<!-- End Registro D605 -->
<!-- Start Registro D609 -->
Registro D609: Processo Referenciado
1. Registro específico para a pessoa jurídica informar a existência de processo administrativo ou judicial que autoriza a adoção de tratamento tributário (CST), base de cálculo ou alíquota diversa da prevista na legislação. Trata-se de informação essencial a ser prestada na escrituração para a adequada validação das contribuições sociais ou dos créditos.
2. Uma vez procedida à escrituração do Registro “D609”, deve a pessoa jurídica gerar os registros “1010” ou “1020” referente ao detalhamento do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
3. Devem ser relacionados todos os processos judiciais ou administrativos que fundamente ou autorize a adoção de procedimento especifico na apuração das contribuições sociais e dos créditos.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D609" | C | 004* | - | S |
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
Campo 01 - Valor Válido: [D609]
Campo 02 - Preenchimento: informar o número do processo judicial ou do processo administrativo, conforme o caso, que autoriza a adoção de procedimento especifico de apuração das contribuições sociais ou dos créditos.
Campo 03 - Valores válidos: [1, 3, 9]
<!-- End Registro D609 -->
<!-- Start Registro D990 -->
Registro D990: Encerramento do Bloco D
Este registro destina-se a identificar o encerramento do bloco D e informar a quantidade de linhas (registros) existentes no bloco.

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | REG | Texto fixo contendo "D990" | C | 004* | - | S |
| 02 | QTD_LIN_D | Quantidade total de linhas do Bloco D | N | - | - | S |

Observações: Registro obrigatório, se existir o Registro D001
Nível hierárquico - 1
Ocorrência - um (por arquivo)
Validação do Registro: registro único e obrigatório para todos os informantes da EFD-Contribuições.
Campo 01 - Valor Válido: [D990]
Campo 02 - Preenchimento: a quantidade de linhas a ser informada deve considerar também os próprios registros de abertura e encerramento do bloco.
Validação: o número de linhas (registros) existentes no bloco D é igual ao valor informado no campo QTD_LIN_D (registro D990).
<!-- End Registro D990 -->