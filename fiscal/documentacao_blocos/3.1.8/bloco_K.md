# Bloco K - Versão 3.1.8

 
BLOCO K: CONTROLE DA PRODUÇÃO E DO ESTOQUE  
 
 Este bloco se destina a prestar informações mensais da produção e respectivo consumo de insumos, bem como do 
estoque escriturado, relativos aos estabelecimentos industriais ou a eles equiparados pela legislação federal e pelos atacadi stas, 
podendo, a crit ério do Fisco, ser exigido de estabelecimento de contribuintes de outros setores (conforme § 4º do art. 63 do 
Convênio s/número, de 1970). O bloco K entrará em vigor na EFD a partir 2016.  
  
 Os contribuintes optantes pelo Simples Nacional estão dispensados de apresentarem este bloco, em virtude da 
Resolução Comitê Gestor do Simples Nacional nº 94, de 29 de novembro de 2011 e alterações, que lista os livros obrigatórios 
do Regime Especial Unif icado de Arrecadação de Tributos e Contribuições devidos pelas Microempresas e Empresas de 
Pequeno Porte – Simples Nacional.  
----
REGISTRO K001: ABERTURA DO BLOCO K  
 
Este registro deve ser gerado para abertura do bloco K, indicando se há registros de informações no bloco.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig  
01 REG Texto fixo contendo "K001"  C 004 - O 
02 IND_MOV  Indicador de movimento:  
0- Bloco com dados informados;  
1- Bloco sem dados informados  C 001* - O 
Observações:  obrigatoriedade a partir de 2016  
Nível hierárquico - 1 
Ocorrência – um por Arquivo  
Campo 01  (REG)  - Valor Válido: [K001]  
 
Campo 02  (IND_MOV)  - Valores Válidos: [0,1] 
Validação: se preenchido com ”1” (um), devem ser informados os registros K001 e K990 (encerramento do bloco), significando 
que não há informação do controle da produção e do estoque. Se preenchido com ”0” (zero), então deve ser informado pelo 
menos um registro K100 e seus respectivos registros filhos, além do registro K990 (encerramento do  bloco).  
----
REGISTRO K010: INFORMAÇÃO SOBRE O TIPO DE LEIAUTE (SIMPLIFICADO / 
COMPLETO)  
 
Este registro indica o tipo de leiaute que o contribuinte adotou na informação do bloco K.  
Nº Campo  Descrição  Tipo Tam Dec Obrig  
01 REG Texto fixo contendo "K010"  C 004 - O 
02 IND_TP_LEIAUTE  Indicador de tipo de leiaute adotado:  
0 – Leiaute simplificado  
1 - Leiaute completo  
2 – Leiaute restrito aos saldos de estoque  C 001* - O 
Observações: obrigatoriedade a partir de 2023  
 Nível hierárquico - 2 
Ocorrência – um por Arquivo  
 
Campo 01  (REG) - Valor Válido: [K010]  
Validação:  registro obrigatório se o campo 02 (IND_MOV) do registro K001 estiver informado com “0 - Bloco com dados 
informados”  
A partir de 01/01/2023, os contribuintes poderão entregar o bloco K com a opção de um leiaute simplificado, de acordo 
com as condições estabelecidas no Ajuste Sinief 02/09. O leiaute simplificado desobriga a informação de alguns registros. A 
tabela a segui r indica a obrigatoriedade de informação dos registros de acordo com o leiaute adotado, completo ou simplificado.  
Registro  Descrição  Nível Ocorrência  Leiaute 
Completo  Leiaute  
Simplificado  
K100 Período de Apuração do ICMS/IPI  2 V sim sim 
K200 Estoque Escriturado  3 1:N sim sim 
K210 Desmontagem de mercadorias – Item de Origem  3 1:N sim não 
K215 Desmontagem de mercadorias – Item de Destino  4 1:N sim não 
K220 Outras Movimentações Internas entre Mercadorias  3 1:N sim sim 
K230 Itens Produzidos  3 1:N sim sim 
K235 Insumos Consumidos  4 1:N sim não 
K250 Industrialização Efetuada por Terceiros – Itens 
Produzidos  3 1:N sim sim 
K255 Industrialização em Terceiros – Insumos 
Consumidos  4 1:N sim não 
K260 Reprocessamento/Reparo de Produto/Insumo  3 1:N sim não 
K265 Reprocessamento/Reparo – Mercadorias 
Consumidas e/ou Retornadas  4 1:N sim não 
K270 Correção de Apontamento dos Registros K210, 
K220, K230, K250, K260, K291, K292, K301 e 
K302 3 1:N sim sim 
K275 Correção de Apontamento e Retorno de Insumos 
dos Registros K215, K220, K235, K255 e K265  4 1:N sim não 
K280 Correção de Apontamento – Estoque Escriturado  3 1:N sim sim 
K290 Produção Conjunta – Ordem de Produção  3 1:N sim sim 
K291 Produção Conjunta – Itens Produzidos  4 1:N sim sim 
K292 Produção Conjunta – Insumos Consumidos  4 1:N sim não 
K300 Produção Conjunta – Industrialização Efetuada por 
Terceiros  3 1:N sim sim 
K301 Produção Conjunta – Industrialização Efetuada por 
Terceiros – Itens Produzidos  4 1:N sim sim  
 K302 Produção Conjunta – Industrialização Efetuada por 
Terceiros – Insumos Consumidos  4 1:N sim não 
 
----
REGISTRO K100: PERÍODO DE APURAÇÃO DO ICMS/IPI  
 
Este registro tem o objetivo de informar o período de apuração do ICMS ou do IPI, prevalecendo os períodos mais 
curtos. Contribuintes com mais de um período de apuração no mês declaram um registro K100 para cada período no mesmo 
arquivo. Não podem ser informados dois ou mais registros com os mesmos campos DT_INI e DT_FIN.  
Os períodos informados neste registro deverão abranger todo o per íodo da escrituração, conforme informado no 
Registro 0000.  
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K100"  C 4 - O 
02 DT_INI  Data inicial a que a apuração se refere  N 8 - O 
03 DT_FIN  Data final a que a apuração se refere  N 8 - O 
Observações:  
Nível hierárquico - 2 
Ocorrência – Vários  
 
Campo 01  (REG)  - Valor Válido: [K100 ] 
 
Campo 02  (DT_INI)  – Validação : a data inicial deve estar compreendida no período informado nos campos DT_INI e DT_FIN 
do Registro 0000.  
 
Campo 03  (DT_FIN)  – Validação : a data final deve estar compreendida no período informado nos campos DT_INI e DT_FIN 
do Registro 0000.  
----
REGISTRO K200: ESTOQUE ESCRITURADO  
 
Este registro tem o objetivo de informar o estoque final escriturado do período de apuração informado no Registro 
K100, por tipo de estoque e por participante, nos casos em que couber, das mercadorias de tipos 00 – Mercadoria para revenda, 
01 – Matéria -Prima, 02 - Embalagem, 03 – Produtos em Processo, 04 – Produto Acabado, 05 – Subproduto, 06 – Produto 
Intermediário e 10 – Outros Insumos – campo TIPO_ITEM do Registro 0200.  
A informação de estoque zero (quantidade = 0) não deixa de ser uma informação e o PV A não a impede. Entretanto, 
caso não seja prestada essa informação, será considerado que o estoque é igual a zero. Portanto, é desnecessária a informação  
de estoque zero ca so não exista quantidade em estoque, independentemente de ter havido movimentação.  
A quantidade em estoque deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante 
no campo 06 do registro 0200 –UNID_INV .  
A chave deste registro são os campos: DT_EST, COD_ITEM, IND_EST e COD_PART (este, quando houver).  
O estoque escriturado informado no Registro K200 deve refletir a quantidade existente na data final do período de 
apuração informado no Registro K100, estoque este derivado dos apontamentos de estoque inicial / entrada / produção 
/consumo / saída / movimen tação interna. Considerando isso, o estoque escriturado informado no K200 é resultante da seguinte 
fórmula:  
Estoque final = estoque inicial + entradas/produção/movimentação interna – Saída / consumo /movimentação interna.  
Os estabelecimentos equiparados a industriais e atacadistas devem informar o estoque escriturado – K200 - e, caso 
ocorram movimentações internas, o K220.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K200"  C 4 - O 
02 DT_EST  Data do estoque final  N 8 - O 
03 COD_ITEM  Código do item (campo 02 do Registro 0200)  C 60 - O 
04 QTD Quantidade em estoque  N - 3 O 
05 IND_EST  Indicador do tipo de estoque:  
 0 - Estoque de propriedade do informante e em seu poder;  C 1 - O  
  1 - Estoque de propriedade do informante e em posse de 
terceiros;  
 2 - Estoque de propriedade de terceiros e em posse do 
informante  
06 COD_PART  Código do participante (campo 02 do Registro 0150):  
- proprietário/possuidor que não seja o informante do arquivo  C 60 - OC 
Observações:  
Nível hierárquico - 3 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido : [K200]  
 
Campo 02  (DT_EST)  – Validação : a data do estoque deve ser igual à data final do período de apuração – campo DT_FIN do 
Registro K100.  
 
Campo 03  (COD_ITEM)  – Validação : o código do item deverá existir no campo COD_ITEM do Registro 0200. Somente 
podem ser informados nesse campo os valores de COD_ITEM cujos tipos sejam iguais a 00, 01, 02, 03, 04, 05, 06 e 10 – campo 
TIPO_ITEM do Registro 0200.  
 
Campo 05  (IND_EST)  - Valores Válidos: [0, 1, 2]  
Validação:  se preenchido com valor ‘1’ (posse de terceiros) ou ‘2’ (propriedade de terceiros), o campo COD_PART será 
obrigatório . 
A quantidade em estoque existente no estabelecimento industrializador do produto industrializado para terceiro por encomenda 
deverá ser:  
a) quando o informante for o estabelecimento industrializador, do tipo 2 - estoque de propriedade de terceiros e em posse do 
informante;  
b) quando o informante for o estabelecimento encomendante, do tipo 1 - estoque de propriedade do informante e em posse de 
terceiros;  
A quantidade em estoque existente no estabelecimento industrializador de insumo recebido do encomendante para 
industrialização por encomenda deverá ser:  
a) quando o informante for o estabelecimento industrializador, do tipo 2 - estoque de propriedade de terceiros e em posse do 
informante;  
b) quando o informante for o estabelecimento encomendante, do tipo 1 - estoque de propriedade do informante e em posse de 
terceiros.  
 
Campo 06  (COD_PART)  – Preenchimento: obrigatório quando o IND_EST for “1” ou “2”.  
Validação: o valor fornecido deve constar no campo COD_PART do registro 0150.  
----
REGISTRO K210: DESMONTAGEM DE MERCADORIAS – ITEM DE ORIGEM  
 
 Este registro tem o objetivo de escriturar a desmontagem de mercadorias de tipos: 00 – Mercadoria para revenda; 01 
– Matéria -Prima; 02 – Embalagem; 03 – Produtos em Processo; 04 – Produto Acabado; 05 – Subproduto e 10 – Outros Insumos 
– campo TIPO_ITEM do Regi stro 0200, no que se refere à saída do estoque do item de origem . 
 
 A quantidade deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante no campo 
06 do registro 0200, UNID_INV .  
  
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
 Validação  do Registro : Quando  houver identificação da ordem de serviço, a chave deste registro são os campos: 
COD_DOC_OS e COD_ITEM_ORI. Nos casos em que a ordem de serviço não for identificada, o campo chave passa a ser 
COD_ITEM_ORI.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K210"  C 004 - O 
02 DT_INI_OS  Data de início da ordem de serviço  N 008* - OC  
 03 DT_FIN_OS  Data de conclusão da ordem de serviço  N 008* - OC 
04 COD_DOC_OS  Código de identificação da ordem de serviço  C 030 - OC 
05 COD_ITEM_ORI  Código do item de origem (campo 02 do Registro 
0200)  C 060 - O 
06 QTD_ORI  Quantidade de origem – saída do estoque  N - 6 O 
Observações:  
Nível  hierárquico - 3 
Ocorrência – 1:N 
 
Campo  01 (REG) - Valor  Válido:  [K210]  
 
Campo  02 (DT_INI_OS) - Preenchimento:  a data de início deverá ser informada se existir ordem de serviço, ainda que 
iniciada em período de apuração (K100) anterior.  
Validação:  obrigatório se informado o campo COD_DOC_OS ou o campo DT_FIN_OS. A data informada deve ser menor ou 
igual a DT_FIN do registro K100.  
 
Campo  03 (DT_FIN_OS) - Preenchimento:  informar a data de conclusão da ordem de serviço. Ficará em branco, caso a 
ordem de serviço não seja concluída até a data de encerramento do período de apuração.  
Validação:  se preenchido, DT_FIN_OS deve estar compreendida no período de apuração do K100 e ser maior ou igual a 
DT_INI_OS.  
 
Campo  04 (COD_DOC_OS) – Preenchimento:  informar o código da ordem de serviço, caso exista.  
Validação:  obrigatório se informado o campo DT_INI_OS.  
 
Campo  05 (COD_ITEM_ORI) - Validação:  o código do item de origem deverá existir no campo COD_ITEM do Registro 
0200.  
Campo  06 (QTD_ORI) – Preenchimento:  não é admitida quantidade negativa.  
----
REGISTRO K215: DESMONTAGEM DE MERCADORIAS – ITENS DE DESTINO  
 
 Este registro tem o objetivo de escriturar a desmontagem (com ou sem ordem de serviço) de mercadorias de tipos: 00 
– Mercadoria para revenda;  
01 – Matéria -Prima;  
02 – Embalagem;  
03 – Produtos em Processo;  
04 – Produto Acabado;  
05 – Subproduto;  
10 – Outros Insumos – 
*Campo TIPO_ITEM do Registro 0200, no que se refere à entrada em estoque do item de destino.  
 
 Este registro é obrigatório caso exista o registro -pai K210 e o controle da desmontagem não for por ordem de serviço 
(campos DT_INI_OS, DT_FIN_OS e COD_DOC_OS do Registro K210 em branco). Nesse caso, a saída do estoque do item 
de origem e a entrada em estoque do item de destino têm que ocorrer no período de apuração do Registro K100. Quando o 
controle da desmontagem for por ordem de serviç o, deverá existir o Registro K215 até o encerramento da ordem de serviço, 
que poderá ocorrer em outro período de apuração.  
 
 A quantidade deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante no campo 
06 do registro 0200, UNID_INV .  
 
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
 Validação  do Registro : A chave deste registro é o campo COD_ITEM_DES.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto  fixo contendo "K215"  C 004 - O 
02 COD_ITEM_DES  Código  do item de destino (campo 02 do Registro 0200)  C 060 - O 
03 QTD_DES  Quantidade  de destino – entrada em estoque  N - 6 O 
 Observações:  
Nível  hierárquico - 4 
Ocorrência – 1:N 
 
Campo  01 (REG) - Valor  Válido:  [K215]  
 
Campo  02 (COD_ITEM_DES) - Validação : 
a) o código informado deve ser diferente do campo COD_ITEM_ORI do Registro K210;  
b) o código do item de destino deverá existir no campo COD_ITEM do Registro 0200.  
 
Campo  03 (QTD_DES) – Preenchimento:  não é admitida quantidade negativa.  
 
----
REGISTRO K220: OUTRAS MOVIMENTAÇÕES INTERNAS ENTRE MERCADORIAS  
 
Este registro tem o objetivo de informar a movimentação interna entre mercadorias de tipos: 00 – Mercadoria para 
revenda; 01 – Matéria -Prima; 02 – Embalagem; 03 – Produtos em Processo; 04 – Produto Acabado; 05 – Subproduto e 10 – 
Outros Insumos – campo TIP O_ITEM do Registro 0200; que não se enquadre nas movimentações internas já informadas nos 
demais tipos de registros.  
Exemplos:  
1) Reclassificação de um produto em outro código em função do cliente a que se destina: o contribuinte aponta a 
quantidade produzida de determinado produto, por exemplo, código 1. Este produto, quando destinado a determinado 
cliente recebe uma outra codificaç ão, código 2. Neste caso há a necessidade de controle do estoque por cliente. Assim 
o contribuinte deverá fazer um registro K220 dando saída no estoque do produto 1 e entrada no estoque do produto 2.  
2) Reclassificação de um produto em função do controle de qualidade: quando o produto não conforme não permanecerá  
com o mesmo código, por exemplo: venda como produto com defeito ou subproduto; consumo em outra fase de 
produção. Caso o produto não conforme tiver como destino o reprocessamento, onde o produto reprocessado 
permanecerá com o mesmo código do produto a ser  reprocessado, deverá ser escriturado no Registro K260.  
A quantidade movimentada deve ser expressa, obrigatoriamente, na unidade de medida do item de origem e do item 
de destino constante no campo 06 do registro 0200(UNID_INV).  
 
Validação do Registro: A chave deste registro são os campos DT_MOV , COD_ITEM_ORI e COD_ITEM_DEST.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K220"  C 4 - O 
02 DT_MOV  Data da movimentação interna  N 8 - O 
03 COD_ITEM_ORI  Código do item de origem (campo 02 do Registro 
0200)  C 60 - O 
04 COD_ITEM_DEST  Código do item de destino (campo 02 do Registro 
0200)  C 60 - O 
05 QTD_ORI  Quantidade movimentada do item de origem  N - 6 O 
06 QTD_DEST  Quantidade movimentada do item de destino  N - 6 O 
Observações:  
Nível hierárquico - 3 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K220 ] 
 
Campo 02  (DT_MOV) - Validação : a data deve estar compreendida no período informado nos campos DT_INI e DT_FIN 
do Registro K100.  
 
Campo 03  (COD_ITEM_ORI) - Validação : o código do item de origem deverá existir no campo COD_ITEM do Registro 
0200.  
 
Campo 04  (COD_ITEM_DEST) - Validação : o código do item de destino deverá existir no campo COD_ITEM do Registro 
0200. O valor informado deve ser diferente do COD_ITEM_ORI.  
  
Campo 05  (QTD_ORI) - Preenchimento : informar a quantidade movimentada do item de origem codificado no campo  
COD_ITEM_ORI.  
Validação : este campo deve ser maior que zero.  
 
Campo 06  (QTD_DEST) - Preenchimento : informar a quantidade movimentada do item de destino codificado no campo 
COD_ITEM_DEST.  
Validação : este campo deve ser maior que zero.  
----
REGISTRO K230: ITENS PRODUZIDOS  
 
Este registro tem o objetivo de informar a produção acabada de produto em processo (tipo 03 – campo TIPO_ITEM 
do registro 0200) e produto acabado (tipo 04 – campo TIPO_ITEM do registro 0200), exceto produção conjunta, inclusive 
daquele industrializado para terceiro por encomenda. O produto resultante é clas sificado como tipo 03 – produto em processo, 
quando não estiver pronto para ser comercializado, mas estiver pronto para ser consumido em outra fase de produção. O produto  
resultante é classificado como tipo 04 – produto acabado, quando estiver pronto para ser comercializado.  
Deverá existir mesmo que a quantidade de produção acabada seja igual a zero, nas situações em que exista o consumo 
de item componente/insumo no registro filho K235. Nessa situação a produção ficou em elaboração. Essa produção em 
elaboração não é quantifica da, uma vez que a matéria não é mais um insumo e nem é ainda um produto resultante. O optante 
pelo tipo de leiaute simplificado é desobrigado de informar este registro quando a quantidade de produção acabada seja igual 
a zero.  
 
Devem ser informadas:  
a) as OP iniciadas e concluídas no período de apuração (K100);  
b) as OP iniciadas e não concluídas no período de apuração (OP em que a produção ficou em elaboração), em que haja 
informação de produção e/ou consumo de insumos (K235);  
c) as OP iniciadas em período anterior e concluídas no período de apuração;  
d) as OP iniciadas em período anterior e não concluídas no período de apuração, em que haja informação de produção 
e/ou consumo de insumos (K235).  
 
 Quando a informação for por período de apuração (K100), o K230 somente deve ser informado caso ocorra produção 
no período, com o respectivo consumo de insumos no K235 para se ter essa produção, uma vez que não se teria como vincular 
a quantidade consumida de insumos com a quantidade produzida do produto resultante envolvendo mais de um período de 
apuração. Somente podemos ter produção igual a zero no K230 quando a informação for por ordem de produção e quando essa 
OP não for concluída até a data final do p eríodo de apuração do K100 e quando houver o apontamento de consumo de insumos 
no K235.  
 
A ordem de produção que não for finalizada no período de apuração deve informar a data de conclusão da ordem de 
produção em branco, campo 03 – DT_FIN_OP. No período seguinte, e assim sucessivamente, a ordem de produção deve ser 
informada até que seja concl uída e caso exista apontamento de quantidade produzida e/ou quantidade consumida de insumo 
(K235).  
A quantidade de produção acabada deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque 
constante no campo 06 do registro 0200, UNID_INV .  
 
Validação do Registro: Quando houver identificação da ordem de produção, a chave deste registro são os campos: 
COD_DOC_OP e COD_ITEM. Nos casos em que a ordem de produção não for identificada, o campo chave passa a ser 
COD_ITEM.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K230"  C 4 - O 
02 DT_INI_OP  Data de início da ordem de produção  N 8 - OC 
03 DT_FIN_OP  Data de conclusão da ordem de produção  N 8 - OC 
04 COD_DOC_OP  Código de identificação da ordem de produção  C 30 - OC 
05 COD_ITEM  Código do item produzido (campo 02 do Registro 0200)  C 60 - O 
06 QTD_ENC  Quantidade de produção acabada  N - 6 O 
Observações:  
 Nível hierárquico - 3 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K230 ] 
 
Campo 02  (DT_INI_OP)  - Preenchimento : a data de início deverá ser informada se existir ordem de produção, ainda que 
iniciada em período de apuração cujo registro K100 correspondente esteja em um arquivo relativo a um mês anterior.  
Validação:  obrigatório se informado o campo COD_DOC_OP ou o campo DT_FIN_OP. O valor informado deve ser menor 
ou igual a DT_FIN do registro K100.  
 
Campo 03  (DT_FIN_OP)  - Preenchimento : informar a data de conclusão da ordem de produção. Ficará em branco, caso a 
ordem de produção não seja concluída até a data de encerramento do período de apuração. Nesta situação a produção ficou em 
elaboração.  
Validação:  se preenchido: a) DT_FIN_OP deve ser menor ou igual a DT_FIN do registro K100 e ser maior ou igual a 
DT_INI_OP;  
b) quando DT_FIN_OP for menor que o campo DT_INI do registro 0000, a mesma deve ser informada no primeiro período de 
apuração do K100.  
 
Campo 04  (COD_DOC_OP)  – Preenchimento : informar o código da ordem de produção.  
Validação : obrigatório se informado o campo DT_INI_OP.  
 
Campo 05  (COD_ITEM)  – Validação : o código do item produzido deverá existir no campo COD_ITEM do Registro 0200.  
 
Campo 06  (QTD_ENC) – Preenchimento : não é admitida quantidade negativa.  
Validação : a) deve ser maior que zero quando: os campos DT_INI_OP e DT_FIN_OP estiverem preenchidos e compreendidos 
no período do Registro K100 ou todos os três campos DT_FIN_OP, DT_INI_OP e COD_DOC_OP não estiverem preenchidos;  
b) deve ser igual a zero quando o campo DT_FIN_OP estiver preenchido e for menor que o campo DT_INI do Registro 0000.  
----
REGISTRO K235: INSUMOS CONSUMIDOS  
 
Este registro tem o objetivo de informar o consumo de mercadoria no processo produtivo, vinculado ao produto 
resultante informado no campo COD_ITEM do Registro K230 – Itens Produzidos.  
Na industrialização efetuada para terceiro por encomenda devem ser considerados os insumos recebidos do 
encomendante e os insumos próprios do industrializador.  
Este registro é obrigatório quando existir o registro pai K230 e:  
a) a informação da quantidade produzida (K230) for por período de apuração(K100); ou  
b) a ordem de produção (K230) se iniciar e concluir no período de apuração (K100); ou  
c) a ordem de produção (K230) se iniciar no período de apuração (K100) e não for concluída no mesmo período.  
O consumo de insumo componente cujo controle não permita um apontamento direto ao produto resultante não precisa 
ser escriturado neste Registro.  
A quantidade consumida deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante 
no campo 06 do registro 0200, UNID_INV .  
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
Validação do Registro:  
1. Até 31/12/2016, a chave deste registro são os campos DT_SAÍDA e COD_ITEM. A partir de 01/01/2017, 
a chave deste registro são os campos DT_SAÍDA, COD_ITEM e, quando existir, o COD_INS_SUBST. 
A partir de 01/01/2023, com a descontinuação do registro 0210, a chave deste registro são os campos 
DT_SAÍDA e COD_ITEM  
 
2. Se o indicador do tipo de leiaute corresponder ao valor “0 – simplificado” no registro K010, e os campos 
de DT_INI_OP e DT_FIN_OP do registro K230 estiverem contidos no período do K100, o registro K235 
não será obrigatório. Se o indicador do tipo de leiaut e corresponder ao valor “1 – completo” no registro 
K010, e os campos de DT_INI_OP e DT_FIN_OP do registro K230 estiverem contidos no período do 
K100, o registro K235 será obrigatório.  
 3. Se o indicador do tipo de leiaute corresponder ao valor “0 – simplificado” no registro K010, e os campos 
de DT_INI_OP, DT_FIN_OP e COD_DOC_OP do registro K230 não estiverem preenchidos, o registro 
K235 não será obrigatório. Se o indicador do tipo de leiaut e corresponder ao valor “1 – completo” no 
registro K010, e os campos de DT_INI_OP, DT_FIN_OP e COD_DOC_OP do registro K230 não 
estiverem preenchidos, o registro K235 será obrigatório.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K235"  C 4 - O 
02 DT_SAÍDA  Data de saída do estoque para alocação ao produto  N 8 - O 
03 COD_ITEM  Código do item componente/insumo (campo 02 do 
Registro 0200)  C 60 - O 
04 QTD Quantidade consumida do item  N - 6 O 
05 COD_INS_SUBS
T Código do insumo que foi substituído, caso ocorra a 
substituição (campo 02 do Registro 0210)  C 60 - OC 
Observações:  
Nível hierárquico - 4 
Ocorrência - 1:N 
 
Campo 01  (REG)  - Valor Válido: [K235 ] 
 
Campo 02  (DT_SAÍDA)  - Validação : a data deve estar compreendida no período da ordem de produção, se existente, campos 
DT_INI_OP e DT_FIN_OP do Registro K230. Se DT_FIN_OP do Registro K230 – Itens Produzidos estiver em branco, o 
campo  DT_SAÍDA deverá ser maior que o campo DT_INI_OP do Registro K230 e menor ou igual a DT_FIN do Registro 
K100. E em qualquer hipótese a data deve estar c ompreendida no período de apuração – K100.  
 
Campo 03  (COD_ITEM)  – Validações : 
a) o código do item componente/insumo deverá existir no campo COD_ITEM do Registro 0200;  
b) caso o campo COD_INS_SUBST esteja em branco, o código do item componente/insumo deve existir também no Registro 
0210 para o mesmo produto resultante – K230/0200 (validação aplicada apenas para as UFs que adotarem o registro 0210).  
c) o código do item componente/insumo deve ser diferente do código do produto resultante (COD_ITEM do Registro  K230);  
d) o tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.  
A quantidade consumida de produto intermediário – tipo 06 no processo produtivo não é escriturada na EFD ICMS/IPI, tanto 
no Bloco K quanto no Bloco C (NF -e). Se o Fisco quiser saber qual foi a quantidade consumida de produto intermediário no 
processo produ tivo basta aplicar a fórmula : Quantidade consumida = estoque inicial (K200) + entrada (C170) – saída 
(C100/NF -e - Devolução) – estoque final (K200).  
 
Campo 04  (QTD) – Preenchimento : não é admitida quantidade negativa.  
 
Campo 05  (COD_INS_SUBST)  – Preenchimento : informar  o código do item componente/insumo que estava previsto para 
ser consumido no Registro 0210 e que foi substituído pelo COD_ITEM  deste registro. A partir de 01/01/2022 não preencher.  
Validação : o código do insumo substituído deve existir no Registro 0210 para o mesmo produto resultante – K230/0200. O 
tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.  
----
REGISTRO K250: INDUSTRIALIZAÇÃO EFETUADA POR TERCEIROS – ITENS 
PRODUZIDOS  
 
Este registro tem o objetivo de informar os produtos que foram industrializados por terceiros por encomenda e sua 
quantidade, exceto produção conjunta  
 
A quantidade produzida deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante 
no campo 06 do registro 0200, UNID_INV .  
Validação do Registro: A chave deste registro são os campos DT_PROD e COD_ITEM.  
 
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K250"  C 4 - O 
 02 DT_PROD  Data do reconhecimento da produção ocorrida no terceiro  N 8 - O 
03 COD_ITEM  Código do item produzido (campo 02 do Registro 0200)  C 60 - O 
04 QTD Quantidade produzida  N - 6 O 
Observações:  
Nível hierárquico - 3 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K250 ] 
 
Campo 02  (DT_PROD)  - Validação : a data deve estar compreendida no período informado nos campos DT_INI e DT_FIN 
do Registro K100.  
 
Campo 03  (COD_ITEM)  – Validações : 
a) o código do item produzido deverá existir no campo COD_ITEM do Registro 0200;  
b) o TIPO_ITEM do Registro 0200 deve ser igual a 03 – Produto em Processo ou 04 – Produto Acabado.  
 
Campo 04  (QTD)  - Preenchimento : a quantidade produzida deve considerar a quantidade que foi recebida do terceiro e a 
variação de estoque ocorrida em terceiro. Cada legislação estadual prevê situações específicas. Consulte a Secretaria de 
Fazenda/Tributação de seu estado. Não é admitida  quantidade negativa.  
----
REGISTRO K255: INDUSTRIALIZAÇÃO EM TERCEIROS – INSUMOS CONSUMIDOS  
 
Este registro tem o objetivo de informar a quantidade de consumo do insumo que foi remetido para ser industrializado 
em terceiro, vinculado ao produto resultante informado no campo COD_ITEM do Registro K250. É obrigatório caso exista o 
registro pai K250.  
 
O consumo de insumo componente cujo controle não permita um apontamento direto ao produto resultante não precisa 
ser escriturado neste Registro.  
 
A quantidade consumida deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante 
no campo 06 do registro 0200, UNID_INV .  
 
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
Validação do Registro:  
1. Até 31/12/2016, a chave deste registro são os campos DT_CONS e COD_ITEM deste Registro. A 
partir de 01/01/2017, a chave deste registro são os campos DT_SAÍDA, COD_ITEM e, quando existir, 
o COD_INS_SUBST . A partir de 01/01/2023, com a descontinuação do registro 0210, a chave deste 
registro são os campos DT_CONS e COD_ITEM  
 
2. Se o indicador do tipo de leiaute corresponder ao valor “0 – simplificado” no registro K010, esse 
registro não será obrigatório.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K255"  C 4 - O 
02 DT_CONS  Data do reconhecimento do consumo do insumo 
referente ao produto informado no campo 04 do 
Registro K250  N 8 - O 
03 COD_ITEM  Código do insumo (campo 02 do Registro 0200)  C 60 - O 
04 QTD Quantidade de consumo do insumo.  N - 6 O 
05 COD_INS_SUBS
T Código do insumo que foi substituído, caso ocorra a 
substituição (campo 02 do Registro 0210)  C 60 - OC 
Observações:  
Nível hierárquico - 4 
Ocorrência - 1:N 
 Campo 01  (REG)  - Valor Válido: [K255 ] 
 
Campo 02  (DT_CONS)  - Validação : a data deve estar compreendida no período informado nos campos DT_INI e DT_FIN 
do Registro K100.  
 
Campo 03  (COD_ITEM)  – Validações : 
a) o código do insumo deverá existir no campo COD_ITEM do Registro 0200;  
b) caso o campo COD_INS_SUBST esteja em branco, o código do item componente/insumo deve existir também no Registro 
0210 para o mesmo produto resultante – K250/0200 (validação aplicada apenas para as UFs que adotarem o registro 0210).  
c) O código do insumo deve ser diferente do código do produto resultante (COD_ITEM do Registro K250 – Industrialização 
efetuada por terceiros – itens produzidos);  
d) o tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.  
 
Campo 04  (QTD)  - Preenchimento : a quantidade de consumo do insumo deve refletir a quantidade consumida para se ter a 
produção acabada informada no campo QTD do Registro K250. Não é admitida quantidade negativa.  
 
Campo 05  (COD_INS_SUBST)  – Preenchimento : informar o código do item componente/insumo que estava previsto para 
ser consumido no Registro 0210 e que foi substituído pelo COD_ITEM  deste registro. A partir de 01/01/2022 não preencher.  
Validação : o código do insumo substituído deve existir no Registro 0210 para o mesmo produto resultante – K250/0200. O 
tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.  
----
REGISTRO K260: REPROCESSAMENTO/REPARO DE PRODUTO/INSUMO  
 
 Este registro tem o objetivo de informar a saída do estoque de um produto/insumo para ser reprocessado no período 
de apuração do Registro K100,  em que o produto/insumo reprocessado/reparado permaneça com o mesmo código  após o 
reprocessamento no próprio estabelecimento do informante.  
 Não há previsão de um registro para informar o reprocessamento executado fora do estabelecimento informante. Não 
utilizar o K260 nessa situação.  
 Quando a informação for por período de apuração (K100), onde não existirá o controle por ordem de produção ou 
serviço, o registro K260 somente deve ser informado caso ocorra saída e respectivo retorno ao estoque de produto/insumo no 
período de apuração, c om o respectivo consumo de mercadorias no K265 para se ter esse reprocessamento/reparo, caso seja 
necessário, uma vez que não se teria como vincular a quantidade consumida de mercadorias com a quantidade que saiu do 
produto/insumo envolvendo mais de um per íodo de apuração.  
 
 As quantidades de saída ou retorno ao estoque devem ser expressas, obrigatoriamente, na unidade de medida de 
controle de estoque constante no campo 06 do registro 0200, UNID_INV .  
 
 O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
 Validação do Registro: Quando houver identificação da ordem de produção ou serviço, a chave deste registro são os 
campos: COD_OP_OS e COD_ITEM. No caso em que a ordem de produção ou serviço não for identificada, o campo chave 
passa a ser COD_ITEM. A partir de 01/01/2020, o campo DT_RET passa a integrar a chave do registro em ambos os casos.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K260"  C 004 - O 
02 COD_OP_OS  Código de identificação da ordem de produção, no 
reprocessamento, ou da ordem de serviço, no reparo  C 030 - OC 
03 COD_ITEM  Código do produto/insumo a ser reprocessado/reparado 
ou já reprocessado/reparado (campo 02 do Registro 
0200)  C 060 - O 
04 DT_SAÍDA  Data de saída do estoque  N 008* - O 
05 QTD_SAÍDA  Quantidade de saída do estoque  N - 6 O 
06 DT_RET  Data de retorno ao estoque (entrada)  N 008* - OC 
07 QTD_RET  Quantidade de retorno ao estoque (entrada)  N - 6 OC 
Observações:  
Nível hierárquico - 3  
 Ocorrência – 1:N 
 
Campo 01  (REG) - Valor Válido:  [K260]  
 
Campo 02  (COD_OP_OS) – Preenchimento:  informar o código de identificação da ordem de produção, no reprocessamento, 
ou da ordem de serviço, no reparo, caso exista.  
Validação:  obrigatório se o campo DT_RET não for preenchido e o campo DT_SAÍDA estiver no período de apuração do 
K100.  
 
Campo 03  (COD_ITEM) – Validação:  o código do produto/insumo a ser reprocessado ou já processado deverá existir no 
campo COD_ITEM do Registro 0200.  
 
Campo 04  (DT_SAÍDA) - Validação:  a data informada deve ser menor ou igual a DT_FIN do registro K100.  
 
Campo 05  (QTD_SAÍDA) – Preenchimento:  não é admitida quantidade negativa.  
 
Campo 06  (DT_RET) – Validação:  a data deve estar compreendida no período de apuração – K100 e ser maior ou igual que 
DT_SAÍDA.  
 
Campos 04 e 06  (DT_SAÍDA e DT_RET) – as datas de saída e retorno ao estoque do produto/insumo substituem, 
respectivamente, as datas de início e conclusão da ordem de produção/serviço.  
 
Campo 07  (QTD_RET) – Preenchimento:  não é admitida quantidade negativa.  
Validação:  este campo será obrigatório caso o campo DT_RET estiver preenchido.  
----
REGISTRO K265: REPROCESSAMENTO/REPARO – MERCADORIAS CONSUMIDAS E/OU 
RETORNADAS  
 
 Este registro tem o objetivo de informar o consumo de mercadoria e/ou o retorno de mercadoria ao estoque, ocorridos 
no reprocessamento/reparo de produto/insumo informado no Registro K260.  
  
A quantidade deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante no campo 
06 do registro 0200, UNID_INV .  
 
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
 Validação do Registro: A chave deste registro é o campo COD_ITEM.  
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K265"  C 004 - O 
02 COD_ITEM  Código da mercadoria (campo 02 do Registro 0200)  C 060 - O 
03 QTD_CONS  Quantidade consumida – saída do estoque  N - 6 OC 
04 QTD_RET  Quantidade retornada – entrada em estoque  N - 6 OC 
Observações:  
Nível hierárquico - 4 
Ocorrência - 1:N 
 
Campo 01  (REG) - Valor Válido:  [K265]  
 
Campo 02  (COD_ITEM) – Validações:  
a) o código da mercadoria deverá existir no campo COD_ITEM do Registro 0200;  
b) o código da mercadoria deve ser diferente do código do produto/insumo reprocessado/ reparado (COD_ITEM do Registro 
K260);  
c) o tipo da mercadoria (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.  
 
Campos 03  (QTD_CONS) e 04 (QTD_RET) – Preenchimento:  não é admitida quantidade negativa.  
 Validação:  pelo menos um dos campos é obrigatório.  
 
----
REGISTRO K270: CORREÇÃO DE APONTAMENTO DOS REGISTROS K210, K220, K230, 
K250, K260, K291, K292, K301 E K302  
 
 Este registro tem o objetivo de escriturar correção de apontamento de período de apuração anterior, relativo ao 
Registro -pai, por tipo de Registro e por período de apuração em que o apontamento será corrigido.  
 Caso ocorra correção de apontamento apenas do Registro -filho, este Registro deverá ser informado com os campos de 
quantidade vazios.  
 A correção de apontamento tem que ocorrer, obrigatoriamente, entre o levantamento de 02 inventários (Campo 02 do 
Registro H005) , uma vez que, com a contagem do estoque, se terá conhecimento de uma eventual necessidade de correção de 
apontamento.  
 As quantidades devem ser expressas, obrigatoriamente, na unidade de medida de controle de estoque constante no 
campo 06 do registro 0200, UNID_INV .  
 Validação do Registro: Quando houver identificação da ordem de produção ou da ordem de serviço e do período de 
apuração, a chave deste registro são os campos: DT_INI_AP, DT_FIN_AP, COD_OP_OS e COD_ITEM e ORIGEM. No caso 
em que a ordem de produção ou a ordem de serviço não forem identificadas, a chave deste registro passa a ser DT_INI_AP, 
DT_FIN_AP e COD_ITEM e ORIGEM. No caso em que a ordem de produção ou a ordem de serviço e o período de apuração 
não forem identificados, a chave deste registro passa a ser  COD_ITEM e ORIGEM.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K270"  C 004 - O 
02 DT_INI_AP  Data inicial do período de apuração em que ocorreu 
o apontamento que está sendo corrigido  N 008* - OC 
03 DT_FIN_AP  Data final do período de apuração em que ocorreu o 
apontamento que está sendo corrigido  N 008* - OC 
04 COD_OP_OS  Código de identificação da ordem de produção ou 
da ordem de serviço que está sendo corrigida  C 030 - OC 
05 COD_ITEM  Código da mercadoria que está sendo corrigido 
(campo 02 do Registro 0200)  C 060 - O 
06 QTD_COR_POS  Quantidade de correção positiva de apontamento 
ocorrido em período de apuração anterior  N - 6 OC 
07 QTD_COR_NEG  Quantidade de correção negativa de apontamento 
ocorrido em período de apuração anterior  N - 6 OC 
 08 ORIGEM  1 – correção de apontamento de produção e/ou 
consumo relativo aos Registros K230/K235;  
2 – correção de apontamento de produção e/ou 
consumo relativo aos Registros K250/K255;  
3 – correção de apontamento de desmontagem e/ou 
consumo relativo aos Registros K210/K215;  
4 – correção de apontamento de 
reprocessamento/reparo e/ou consumo relativo aos 
Registros K260/K265;  
5 – correção de apontamento de movimentação 
interna relativo ao Registro K220.  
6 – correção de apontamento de produção relativo 
ao Registro K291;  
7 – correção de apontamento de consumo relativo 
ao Registro K292;  
8 – correção de apontamento de produção relativo 
ao Registro K301;  
9 – correção de apontamento de consumo relativo 
ao Registro K302.  C 001 - O 
Observações:  
Nível hierárquico - 3 
Ocorrência – 1:N 
Campo 01  (REG) - Valor Válido:  [K270]  
 
Campos 02 e 03 (DT_INI_AP e  DT_FIN_AP) – Preenchimento:  estes campos poderão não ser preenchidos  somente na 
hipótese em que o campo 4 (COD_OP_OS), na correção de apontamento, se referir:  
a) a uma ordem de produção que esteja em aberto (DT_FIN_OP do Registro K230 em branco) com o campo 08 (ORIGEM) do 
registro K270 igual a 1, no presente período de apuração do K100 ou em período de apuração imediatamente anterior ao 
presente período de apura ção do K100;  
b) a uma ordem de serviço que esteja em aberto (DT_FIN_OS do Registro K210 em branco) com o campo 08 (ORIGEM) do 
registro K270 igual a 3, no presente período de apuração do K100 ou em período de apuração imediatamente anterior ao 
presente período de apuraç ão do K100;  
c) a uma ordem de produção ou ordem de serviço que esteja em aberto (COD_OP_OS do Registro K260 em branco) com o 
campo 08 (ORIGEM) do registro K270 igual a 4, no presente período de apuração do K100 ou em período de apuração 
imediatamente anterior ao prese nte período de apuração do K100.  
Validação:  a data inicial e a data final têm de ser anteriores à data inicial do período informado no Registro 0000.  
 
Campo 05  (COD_ITEM) – Validação:  o código do item produzido que está sendo corrigido deverá existir no campo 
COD_ITEM do Registro 0200.  
 
Campos 06 e 07  (QTD_COR_POS e QTD_COR_NEG) – Validação:  não é admitida quantidade negativa.  
Validação:  somente um dos campos pode ser preenchido.  
 
Campo 08  (ORIGEM) – Valores Válidos:  [1, 2, 3, 4, 5, 6, 7, 8, 9]  
Preenchimento:  quando a correção de apontamento se referir ao Registro K220 – origem 5: a correção deste Registro será 
relativa ao item de origem da movimentação interna; no Registro -filho K275 será apontada a correção do item de destino.  
----
REGISTRO K275: CORREÇÃO DE APONTAMENTO E RETORNO DE INSUMOS DOS 
REGISTROS K215, K220, K235, K255 E K265.  
 
 Este registro tem o objetivo de escriturar correção de apontamento de período de apuração anterior, relativo ao 
Registro -filho, por tipo de Registro e por período de apuração em que o apontamento será corrigido.  
 
 A correção de apontamento tem que ocorrer,  obrigatoriamente, entre o levantamento de 02 inventários (Campo 02 do 
Registro H005) , uma vez que, com a contagem do estoque, se terá conhecimento de uma eventual necessidade de correção de 
 apontamento.  
 
 Este registro poderá também ser escriturado para substituição ou retorno de insumo/componente que já tenha sido 
baixado do estoque por consumo efetivo em período de apuração de exercício anterior, desde que vinculado à Ordem de 
Produção não encerrada no p róprio exercício de abertura da OP.  
 
 Caso ocorra correção de apontamento apenas do Registro -pai (K270), este Registro não deverá ser escriturado, exceto 
quando a correção tiver como origem o Registro K220 (origem 5 do Registro K270), onde este Registro será obrigatório para 
identificação do item de destino, mesmo que não ocorra correção de quantidades.  
 
 As quantidades devem ser expressas, obrigatoriamente, na unidade de medida de controle de estoque constante no 
campo 06 do registro 0200, UNID_INV .  
 
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
 Validação do Registro: A chave deste registro é o campo COD_ITEM.  
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K275"  C 004 - O 
02 COD_ITEM  Código da mercadoria (campo 02 do Registro 
0200)  C 060 - O 
03 
QTD_COR_POS  Quantidade de correção positiva de apontamento 
ocorrido em período de apuração anterior  N - 6 OC 
04 
QTD_COR_NEG  Quantidade de correção negativa de apontamento 
ocorrido em período de apuração anterior  N - 6 OC 
05 COD_INS_SUBST  Código do insumo que foi substituído, caso ocorra 
a substituição, relativo aos Registros K235/K255.  C 060 - OC 
Observações:  
Nível hierárquico - 4 
Ocorrência - 1:N 
 
Campo 01  (REG) - Valor Válido:  [K275]  
 
Campo 02  (COD_ITEM) – Validação:  o código da mercadoria deverá existir no campo COD_ITEM do Registro 0200 e 
somente são admitidas mercadorias de tipos 00 a 05 e 10 – campo TIPO_ITEM do Registro 0200.  
 
Campos 03 e 04 (QTD_COR_POS e QTD_COR_NEG) – Validação:  não é admitida quantidade negativa.  
Validação:  somente um dos campos pode ser preenchido.  
 
Campo 05  (COD_INS_SUBST) – Preenchimento:  este campo deverá ser informado quando se estiver escriturando 
quantidade consumida não apontada em período anterior, e desde que exista a substituição.  
Validação:  este campo somente pode existir quando a origem da correção de apontamento for dos tipos 1 ou 2 (campo ORIGEM 
do Registro K270).  
----
REGISTRO K280: CORREÇÃO DE APONTAMENTO – ESTOQUE ESCRITURADO  
 
 Este registro tem o objetivo de escriturar correção de apontamento de estoque escriturado de período de apuração 
anterior, escriturado no Registro K200.  
 A correção de apontamento tem que ocorrer, obrigatoriamente, entre o levantamento de 02 inventários (Campo 02 do 
Registro H005) , uma vez que a contagem do estoque permite identificar eventual necessidade de correção de apontamento.  
 
 A correção do estoque escriturado de um período de apuração poderá influenciar estoques escriturados de períodos 
posteriores, até o período imediatamente anterior ao período de apuração em que se está fazendo a correção, uma vez que o 
estoque final de um período de apuração é o estoque inicial do período de apuração seguinte.   
  
 As quantidades devem ser expressas, obrigatoriamente, na unidade de medida de controle de estoque constante no 
campo 06 do registro 0200, UNID_INV .  
 
 Validação do Registro: A chave deste registro são os campos: DT_EST, COD_ITEM, IND_EST e COD_PART (este, 
quando houver).  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K280"  C 004 - O 
02 DT_EST  Data do estoque final escriturado que está sendo 
corrigido  N 008* - O 
03 COD_ITEM  Código do item (campo 02 do Registro 0200)  C 060 - O 
04 QTD_COR_POS  Quantidade de correção positiva de apontamento 
ocorrido em período de apuração anterior  N - 3 OC 
05 QTD_COR_NEG  Quantidade de correção negativa de apontamento 
ocorrido em período de apuração anterior  N - 3 OC 
06 IND_EST  Indicador do tipo de estoque:  
 0 = Estoque de propriedade do informante e em seu 
poder;  
 1 = Estoque de propriedade do informante e em posse 
de terceiros;  
 2 = Estoque de propriedade de terceiros e em posse 
do informante  C 001 - O 
07 COD_PART  Código do participante (campo 02 do Registro 0150):  
- proprietário/possuidor que não seja o informante do 
arquivo  C 060 - OC 
Observações:  
Nível hierárquico - 3 
Ocorrência – 1:N 
Campo 01  (REG) - Valor Válido:  [K280]  
 
Campo 02  (DT_EST) – Validação:  a data do estoque deve ser anterior à data inicial do período de apuração – campo DT_INI 
do Registro 0000.  
Campo 03  (COD_ITEM) – Validação:  o código do item deverá existir no campo COD_ITEM do Registro 0200. Somente 
podem ser informados nesse campo, valores de COD_ITEM cujos tipos sejam iguais a 00, 01, 02, 03, 04, 05, 06 e 10 – campo 
TIPO_ITEM do Registro 0200.  
Campos 04 e 05  (QTD_COR_POS e QTD_COR_NEG) – Validação:  não é admitida quantidade negativa.  
Validação:  somente um dos campos pode ser preenchido.  
 
Campo 06  (IND_EST) - Valores Válidos:  [0, 1, 2]  
Validação:  se preenchido com valor “1” (posse de terceiros) ou “2” (propriedade de terceiros), o campo COD_PART será 
obrigatório.  
A quantidade em estoque existente no estabelecimento industrializador do produto industrializado para terceiro por encomenda 
deverá ser:  
a) quando o informante for o estabelecimento industrializador, do tipo 2 - estoque de propriedade de terceiros e em posse do 
informante;  
b) quando o informante for o estabelecimento encomendante, do tipo 1 - estoque de propriedade do informante e em posse de 
terceiros.  
A quantidade em estoque existente no estabelecimento industrializador de insumo recebido do encomendante para 
industrialização por encomenda deverá ser:  
a) quando o informante for o estabelecimento industrializador, do tipo 2 - estoque de propriedade de terceiros e em posse do 
informante;  
b) quando o informante for o estabelecimento encomendante, do tipo 1 - estoque de propriedade do informante e em posse de 
 terceiros.  
 
Campo 07  (COD_PART) – Preenchimento:  obrigatório quando o IND_EST for “1” ou “2”.  
Validação:  o valor fornecido deve constar no campo COD_PART do registro 0150.  
----
REGISTRO K290: PRODUÇÃO CONJUNTA – ORDEM DE PRODUÇÃO  
 
Este registro tem o objetivo de informar a ordem de produção relativa à produção conjunta.  
 
Entenda -se por produção conjunta a produção de mais de um produto resultante a partir do consumo de um ou mais 
insumos em um fluxo produtivo comum, onde não seja possível apontar o consumo de insumos diretos aos produtos resultantes, 
que podem ser classifi cados, conforme a relevância nas vendas do contribuinte, como coprodutos ou subprodutos.  
 
No Bloco K, devem ser considerados para a classificação de produção conjunta apenas os produtos resultantes 
classificados como co -produtos (produto principal). Não se deve informar a produção de subprodutos. Exemplo: processo 
produtivo que resulta em dois subprodutos e um coproduto: declarar nos registros K230/K250. Processo produtivo que resulta 
em dois coprodutos e um subproduto: declarar nos registros K290/K300.  
 
Devem ser informadas:  
a) as OP iniciadas e concluídas no período de apuração (K100);  
b) as OP iniciadas e não concluídas no período de apuração (OP em que a produção ficou em elaboração), em que haja 
informação de produção e/ou consumo de insumos (K292);  
c) as OP iniciadas em período anterior e concluídas no período de apuração;  
d) as OP iniciadas em período anterior e não concluídas no período de apuração, em que haja informação de produção 
e/ou consumo de insumos (K292).  
A ordem de produção que não for finalizada no período de apuração deve informar a data de conclusão da ordem de 
produção em branco, campo 03 – DT_FIN_OP. No período seguinte, e assim sucessivamente, a ordem de produção deve ser 
informada até que seja concl uída e caso exista apontamento de quantidade produzida e/ou quantidade consumida de insumo 
(K292).  
Quando o processo não for controlado por ordem de produção, os campos DT_INI_OP, DT_FIN_OP e COD_DOC_OP 
não devem ser preenchidos.  
Quando DT_FIN_OP for menor que o campo DT_INI do registro 0000, não devem ser escriturados os registros K291 
e K292.  
 
Validação do Registro: Quando houver identificação da ordem de produção, a chave deste registro é o campo 
COD_DOC_OP.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K290"  C 4 - O 
02 DT_INI_OP  Data de início da ordem de produção  N 8 - OC 
03 DT_FIN_OP  Data de conclusão da ordem de produção  N 8 - OC 
04 COD_DOC_OP  Código de identificação da ordem de produção  C 30 - OC 
Observações:  
Nível hierárquico - 3 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K290 ] 
 
Campo 02  (DT_INI_OP)  - Preenchimento : a data de início deverá ser informada se existir ordem de produção, ainda que 
iniciada em período de apuração cujo registro K100 correspondente esteja em um arquivo relativo a um mês anterior.  
Validação:  obrigatório se informado o campo COD_DOC_OP ou o campo DT_FIN_OP. O valor informado deve ser menor 
ou igual a DT_FIN do registro K100.  
 
Campo 03  (DT_FIN_OP)  - Preenchimento : informar a data de conclusão da ordem de produção. Ficará em branco, caso a 
ordem de produção não seja concluída até a data de encerramento do período de apuração. Nesta situação a produção ficou em 
elaboração.  
 Validação:  se preenchido:  
a) DT_FIN_OP deve ser menor ou igual a DT_FIN do registro K100 e ser maior ou igual a DT_INI_OP;  
b) quando DT_FIN_OP for menor que o campo DT_INI do registro 0000, a mesma deve ser informada no primeiro período de 
apuração do K100;  
c)quando DT_FIN_OP for menor que o campo DT_INI do registro 0000, é obrigatório existir pelo menos um Registro K291 e 
não devem existir Registros K292.  
 
Campo 04  (COD_DOC_OP)  – Preenchimento : informar o código da ordem de produção.  
Validação : obrigatório se informado o campo DT_INI_OP.  
----
REGISTRO K291: PRODUÇÃO CONJUNTA – ITENS PRODUZIDOS  
 
Este registro tem o objetivo de informar a produção acabada de produto em processo (tipo 03 – campo TIPO_ITEM 
do registro 0200) e produto acabado (tipo 04 – campo TIPO_ITEM do registro 0200), originados de produção conjunta, 
inclusive daquele industrializa do para terceiro por encomenda. O produto resultante é classificado como tipo 03 – produto em 
processo, quando não estiver pronto para ser comercializado, mas estiver pronto para ser consumido em outra fase de produção.  
O produto resultante é classificado como tipo 04 – produto acabado, quando estiver pronto para ser comercializado.  
A quantidade de produção acabada deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque 
constante no campo 06 do registro 0200, UNID_INV .  
 
Este registro não deve ser escriturado quando DT_FIN_OP do registro K290 for menor que o campo DT_INI do 
registro 0000.  
 
Validação do Registro: A chave deste registro é o campo COD_ITEM.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K291"  C 4 - O 
02 COD_ITEM  Código do item produzido (campo 02 do Registro 0200)  C 60 - O 
03 QTD Quantidade de produção acabada  N - 6 O 
 
Observações:  
Nível hierárquico - 4 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K291 ] 
 
Campo 02  (COD_ITEM)  – Validação : a) o código do item produzido deverá existir no campo COD_ITEM do Registro 0200; 
b) o tipo do produto resultante (campo TIPO_ITEM do Registro 0200) deve ser igual a 03 ou 04.  
 
Campo 03  (QTD) – Preenchimento : não é admitida quantidade negativa.  
Validação : deve ser maior que zero.  
----
REGISTRO K292: PRODUÇÃO CONJUNTA – INSUMOS CONSUMIDOS  
 
Este registro tem o objetivo de informar o consumo de insumo/componente no processo produtivo, relativo à produção 
conjunta.  
Na industrialização efetuada para terceiro por encomenda devem ser considerados os insumos recebidos do 
encomendante e os insumos próprios do industrializador.  
O consumo de insumo componente cujo controle não permita um apontamento direto não precisa ser escriturado neste 
Registro.  
A quantidade consumida deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante 
no campo 06 do registro 0200 - UNID_INV .  
Este registro não deve ser escriturado quando DT_FIN_OP do registro K290 for menor que o campo DT_INI do 
registro 0000.  
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro  
  
Validação do Registro:  
1. A chave deste registro é o campo COD_ITEM.  
2. Se o indicador do tipo de leiaute corresponder ao valor “0 – simplificado” no registro K010, e os 
campos de DT_INI_OP e DT_FIN_OP do registro K290 estiverem contidos no período  do K100, o 
registro K292 não será obrigatório . Se o indicador do tipo de leiaute corresponder ao valor “1 – 
completo”no registro K010, e os campos de DT_INI_OP e DT_FIN_OP do registro K290 estiverem 
contidos no período  do K100, o registro K292 será obrigatório . 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K292"  C 4 - O 
02 COD_ITEM  Código do insumo/componente consumido (campo 02 do 
Registro 0200)  C 60 - O 
03 QTD Quantidade consumida  N - 6 O 
Observações:  
Nível hierárquico - 4 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K292 ] 
 
Campo 02  (COD_ITEM)  – Validações : 
a) o código do item componente/insumo deverá existir no campo COD_ITEM do Registro 0200;  
b) o código do item componente/insumo deve ser diferente do código do produto resultante (COD_ITEM do Registro K291);  
c) o tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.  
 
Campo 03  (QTD) – Preenchimento : não é admitida quantidade negativa.  
Validação : deve ser maior que zero.  
----
REGISTRO K300: PRODUÇÃO CONJUNTA – INDUSTRIALIZAÇÃO EFETUADA POR 
TERCEIROS  
 
Este registro tem o objetivo de informar a data de reconhecimento da produção ocorrida em terceiro, relativa à 
produção conjunta. Entenda -se por produção conjunta a produção de mais de um produto resultante a partir do consumo de um 
ou mais insumos em um m esmo processo.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K300"  C 4 - O 
02 DT_PROD  Data do reconhecimento da produção ocorrida no terceiro  N 8 - O 
Observações:  
Nível hierárquico - 3 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K300 ] 
 
Campo 02  (DT_PROD)  - Validação : a data chave deve estar compreendida no período informado nos campos DT_INI e 
DT_FIN do Registro K100.  
----
REGISTRO K301: PRODUÇÃO CONJUNTA – INDUSTRIALIZAÇÃO EFETUADA POR 
TERCEIROS – ITENS PRODUZIDOS  
 
Este registro tem o objetivo de informar os produtos que foram industrializados por terceiros por encomenda e sua 
quantidade, originados de produção conjunta.  
A quantidade produzida deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante 
no campo 06 do registro 0200, UNID_INV .   
 Validação do Registro: A chave deste registro é o campo COD_ITEM.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K301"  C 4 - O 
02 COD_ITEM  Código do item produzido (campo 02 do Registro 0200)  C 60 - O 
03 QTD Quantidade produzida  N - 6 O 
Observações:  
Nível hierárquico - 4 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K301 ] 
 
Campo 02  (COD_ITEM)  – Validações : 
a) o código do item produzido deverá existir no campo COD_ITEM do Registro 0200;  
b) o TIPO_ITEM do Registro 0200 deve ser igual a 03 – Produto em Processo ou 04 – Produto Acabado.  
 
Campo 03  (QTD)  - Preenchimento : a quantidade produzida deve considerar a quantidade que foi recebida do terceiro e a 
variação de estoque ocorrida em terceiro. Cada legislação estadual prevê situações específicas. Consulte a Secretaria de 
Fazenda/Tributação de seu estado. Não é admitida  quantidade negativa.  
Validação : deve ser maior que zero.  
----
REGISTRO K302: PRODUÇÃO CONJUNTA – INDUSTRIALIZAÇÃO EFETUADA POR 
TERCEIROS – INSUMOS CONSUMIDOS  
 
Este registro tem o objetivo de informar a quantidade de consumo do insumo que foi remetido para ser industrializado 
em terceiro, relativo a produção conjunta.  
O consumo de insumo componente cujo controle não permita um apontamento direto não precisa ser escriturado neste 
Registro.  
A quantidade consumida deve ser expressa, obrigatoriamente, na unidade de medida de controle de estoque constante 
no campo 06 do registro 0200 - UNID_INV .  
O optante pelo tipo de leiaute simplificado é desobrigado de informar este registro.  
 
Validação do Registro:  
1. A chave deste registro é o campo COD_ITEM.  
 
2. Se o indicador do tipo de leiaute corresponder ao valor “0 – simplificado ” no registro K010, o registro 
K302 não será obrigatório . Se o indicador do tipo de leiaute corresponder ao valor “1 – completo” 
no registro K010, o registro K302 será obrigatório . 
Nº Campo  Descrição  Tipo Tam Dec Obrig.  
01 REG Texto fixo contendo "K302"  C 4 - O 
02 COD_ITEM  Código do insumo (campo 02 do Registro 0200)  C 60 - O 
03 QTD Quantidade consumida  N - 6 O 
Observações:  
Nível hierárquico - 4 
Ocorrência – 1:N 
 
Campo 01  (REG)  - Valor Válido: [K302 ] 
 
Campo 02  (COD_ITEM)  – Validações : 
a) o código do insumo deverá existir no campo COD_ITEM do Registro 0200;  
b) o código do insumo deve ser diferente do código do produto resultante (COD_ITEM do Registro K301);  
c) o tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.  
 
Campo 03  (QTD)  - Preenchimento : a quantidade de consumo do insumo deve refletir a quantidade consumida para se ter a  
 produção acabada informada nos Registros K301. Não é admitida quantidade negativa.  
Validação : deve ser maior que zero.  
----
REGISTRO K990: ENCERRAMENTO DO BLOCO K  
 
Este registro destina -se a identificar o encerramento do bloco K e a informar a quantidade de linhas (registros) 
existentes no bloco.  
Nº Campo  Descrição  Tipo Tam Dec Obrig  
01 REG Texto fixo contendo "K990"  C 004 - O 
02 QTD_LIN_K  Quantidade total de linhas do Bloco K  N - - O 
Observações:    
Nível hierárquico - 1 
Ocorrência –um por arquivo  
Campo 01  (REG)  - Valor Válido: [K990]  
 
Campo 02  (QTD_LIN_K)  - Preenchimento : a quantidade de linhas a ser informada deve considerar também os próprios 
registros de abertura e encerramento do bloco.  
Validação:  o número de linhas (registros) existentes no bloco K é igual ao valor informado no campo QTD_LIN_K.  
 
 
 
 
 
 
BLOCO 1: OUTRAS INFORMAÇÕES  
  
 Este bloco destina -se à prestação de outras informações exigidas pelo fisco.  
 
REGISTRO 1001: ABERTURA DO BLOCO 1  
 
Este registro deverá ser gerado para abertura do bloco 1 e indicará se há informações no bloco.  
 
Nº Campo  Descrição  Tipo Tam Dec Obrig  
01 REG Texto fixo contendo "1001"  C 004 - O 
02 IND_MOV  Indicador de movimento:  
0- Bloco com dados informados;  
1- Bloco sem dados informados  N 001* - O 
Observações :  
Nível hierárquico – 1 
Ocorrência - um por arquivo  
 
Campo 01  (REG)  - Valor Válido: [ 1001]  
 
Campo 02  (IND_MOV)  - Valores Válidos: [0, 1] 
Validação: além dos registros de abertura e encerramento, sempre deve ser informado o registro 1010 (Obrigatoriedade de 
Registros do Bloco 1).  
  
REGISTRO 1010: OBRIGATORIEDADE DE REGISTROS DO BLOCO 1  
 
Este registro deverá ser apresentado por todos os contribuintes. Caso a resposta seja “S”, o contribuinte está obrigado 
à apresentação do registro respectivo. Se houver dispensa de apresentação do registro pela unidade federada, a resposta para o 
campo esp ecífico do registro deverá ser “N”.  
 

