# Bloco 0 - Versão 3.1.8

---
BLOCO 0: ABERTURA, IDENTIFICAÇÃO E REFERÊNCIAS
REGISTRO 0000: ABERTURA DO ARQUIVO DIGITAL E IDENTIFICAÇÃO DA ENTIDADE
Este Registro é obrigatório e corresponde ao primeiro registro do arquivo.
Nos casos de EFD-ICMS/IPI apresentadas por estabelecimentos situados em outra UF e que possuam Inscrição
Estadual nos termos do Convênio ICMS nº 113/04 (serviços de comunicação definidos pela Anatel), bem como as distribuidoras que forneçam energia elétrica a consumidor localizado em UF diversa da sede do estabelecimento deverão observar o seguinte procedimento para preenchimento do registro 0000:
1) Informar o campo UF da unidade federada do tomador de serviços/consumidor de energia elétrica;
2) Informar no campo IE a inscrição estadual na unidade federada do tomador de serviços/consumidor de energia elétrica;
3) Informar no campo COD_MUN o código de município correspondente à capital do estado do tomador de serviços/consumidor de energia elétrica.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0000”. C 004 - O
02 COD_VER Código da versão do leiaute conforme a tabela indicada no N 003* - O
Ato COTEPE.
03 COD_FIN Código da finalidade do arquivo: N 001 - O
0 - Remessa do arquivo original;
1 - Remessa do arquivo substituto.
04 DT_INI Data inicial das informações contidas no arquivo. N 008* - O
05 DT_FIN Data final das informações contidas no arquivo. N 008* - O
06 NOME Nome empresarial da entidade. C 100 - O
07 CNPJ Número de inscrição da entidade no CNPJ. N 014* - OC
08 CPF Número de inscrição da entidade no CPF. N 011* OC
09 UF Sigla da unidade da federação da entidade. C 002* - O
10 IE Inscrição Estadual da entidade. C 014 - O
11 COD_MUN Código do município do N 007* - O
domicílio fiscal da entidade,
conforme a tabela IBGE
12 IM Inscrição Municipal da entidade. C - - OC
13 SUFRAMA Inscrição da entidade na SUFRAMA C 009* - OC
14 IND_PERFIL Perfil de apresentação do arquivo fiscal; C 001 - O
A – Perfil A;
B – Perfil B.;
C – Perfil C.
15 IND_ATIV Indicador de tipo de atividade: N 001 - O
0 – Industrial ou equiparado a industrial;
1 – Outros.
Observações:
Nível hierárquico - 0
Ocorrência - um por arquivo.
Campo 01 (REG) - Valor Válido: [0000]
Campo 02 (COD_VER) - Preenchimento: o código da versão do leiaute informado é validado conforme a data referenciada no campo DT_FIN. Verificar na Tabela Versão do Leiaute (item 3.1.1 da Nota Técnica, conforme Ato COTEPE/ICMS nº44/2018 e alterações).
Validação: Válido para o período informado. A versão do leiaute informada no arquivo deverá ser válida na data final da escrituração (campo DT_FIN do registro 0000).
Campo 03 (COD_FIN) - Valores Válidos: [0, 1]
Preenchimento: dentro do prazo normal de entrega o arquivo pode ser substituído.
Após o vencimento do prazo de entrega, com a publicação do Ajuste Sinief 11/2012, que define regras padronizadas em todo o território nacional para a RETIFICAÇÃO DA EFD-ICMS/IPI, a partir de janeiro de 2013, o procedimento deve ser o seguinte:
1. EFD-ICMS/IPI de mês de referência janeiro de 2009 a dezembro de 2012 pode ser retificada, sem autorização, até 30 de abril de 2013;
2. EFD-ICMS/IPI de mês de referência janeiro de 2013 em diante, pode ser retificada, sem autorização, até o último dia do terceiro mês subsequente ao encerramento do mês da apuração (exemplo: Janeiro de 2013 pode ser retificado até 30 de abril de 2013);
3. Cumpridos estes prazos, retificações somente serão possíveis com autorização, de acordo com o que determina o referido Ajuste, exceto, a partir de 03.09.20, se a autorização para retificação da EFD for dispensada a critério da Secretaria de Fazenda, Receita, Finanças, Economia ou Tributação do domicílio fiscal do contribuinte, quando se tratar de ICMS, conforme Ajuste SINIEF 27/20.
Para a entrega da EFD-ICMS/IPI deverá ser utilizado o leiaute vigente à época do período de apuração e, para validação e transmissão, a versão do Programa de Validação e Assinatura - PVA atualizada.
Obs.: Para as SEFAZ que exigem a informação do hash do arquivo, esse refere-se ao hash do arquivo RETIFICADOR assinado.
Para obtê-lo utilizar a opção “Dados da Escrituração” da aba Relatórios, o hash está identificado com o nome “ID do Arquivo Assinado (hash)”, contendo 32 caracteres. Para os arquivos retificadores que afetam o IPI, verificar as regras da Seção 7 – Outras Informações, do Capítulo I.
Campo 04 (DT_INI) - Preenchimento: informar o período de validade das informações contidas neste registro, no padrão
“diamêsano” (ddmmaaaa), excluindo-se quaisquer caracteres de separação, tais como: ".", "/", "-".
O valor informado deve ser o primeiro dia do mês, exceto no caso de início de atividades ou de qualquer outro evento que altere
a forma e o período de escrituração fiscal do estabelecimento.
Campo 05 (DT_FIN) - Preenchimento: informar a última data do período da escrituração, no padrão “ddmmaaa”, excluindo-
se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
Validação: Verifica se a data informada neste campo pertence ao mesmo mês/ano da data informada no campo DT_INI.
O valor informado deve ser o último dia do mesmo mês da data inicial, exceto no caso de encerramento de atividades ou de
qualquer outro fato determinante para paralisação das atividades do estabelecimento.
Campo 07 (CNPJ) - Preenchimento: informar o número do CNPJ do contribuinte. Se o contribuinte for pessoa física (por
exemplo: produtor rural), deixar o campo em branco.
Validação: será conferido o dígito verificador (DV) do CNPJ informado.
Campo 08 (CPF) - Preenchimento: informar o número de inscrição do contribuinte no cadastro do CPF. Obrigatório, se o
informante do arquivo for pessoa física e não obrigado à inscrição no CNPJ.
Validação: será conferido o dígito verificador (DV) do CPF informado.
Os campos CNPJ e CPF são mutuamente excludentes, ou seja, é obrigatório o preenchimento de apenas um deles.
Campo 09 (UF) - Validação: o valor deve ser a sigla da unidade da federação (UF) do informante.
Campo 10 (IE) - Validação: será conferido o dígito verificador (DV) da Inscrição Estadual informada, considerando-se a UF
do informante.
Campo 11 (COD_MUN) – Preenchimento: Os estabelecimentos situados em outra unidade da federação, sem ter endereço
e/ou estabelecimento físico na unidade federada, devem informar o código de município da capital do estado, constante da
Tabela de Municípios do IBGE.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
Campo 13 (SUFRAMA) - Validação: será conferido o dígito verificador (DV) do número de inscrição na SUFRAMA, se
informado.
Campo 14 (IND_PERFIL) - Valores Válidos: [A, B, C]
Preenchimento: informar o perfil de apresentação do arquivo, conforme definido pelo Fisco Estadual para o informante da
EFD-ICMS/IPI. O arquivo será rejeitado se o declarante informar a EFD-ICMS/IPI em perfil diferente do estabelecido.
Campo 15 (IND_ATIV) - Valores Válidos: [0, 1]
Preenchimento: informar “0”, se o contribuinte é industrial ou equiparado a industrial, conforme legislação do Imposto sobre
Produtos Industrializados (IPI). Se o estabelecimento não se enquadrar no disposto nos art. 8º, 9º, 10 e 11 e cujas operações
não se enquadrem dentro do campo de incidência do IPI, conforme parágrafo único do art. 2º, todos do Decreto nº 7.212/2010,
ainda que seja uma indústria, deve informar a opção "1 - Outras" no campo IND_ATIV do registro 0000.Se o contribuinte do
IPI for optante pelo Simples Nacional, deve informar a opção “1 – Outras” no campo IND_ATIV, conforme o art. 179, do
Decreto n. 7.212/2010. Se campo CPF for informado, então o campo IND_ATIV deve ser igual a 1. Se campo IND_ATIV for igual a 1, não deve existir o registro E500.
----
REGISTRO 0001: ABERTURA DO BLOCO 0
Este registro deve ser gerado para abertura do bloco 0 e indica as informações previstas para este bloco.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0001”. C 004 - O
02 IND_MOV Indicador de movimento: N 001 - O
0- Bloco com dados informados;
1- Bloco sem dados informados.
Observações:
Nível hierárquico - 1
Ocorrência – um por arquivo
Campo 01 (REG) - Valor Válido: [0001]
Campo 02 (IND_MOV) - Valor Válido: [0]
----
REGISTRO 0002: CLASSIFICAÇÃO DO ESTABELECIMENTO INDUSTRIAL OU
EQUIPARADO A INDUSTRIAL
O registro deve ser informado quando o campo IND_ATIV do registro 0000 for igual a “0”.
Quando existir mais de um tipo de modalidade, informar a classificação que for mais relevante no estabelecimento.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0002”. C 004 - O
02 CLAS_ESTAB_IND Informar a classificação do estabelecimento conforme N 002 - O
tabela 4.5.5
Nível hierárquico - 2
Ocorrência – um por arquivo
Campo 02 (CLAS_ESTAB_IND)
Validação: o valor informado deve constar na Tabela 4.5.5 – Classificação de Contribuintes do IPI
----
REGISTRO 0005: DADOS COMPLEMENTARES DA ENTIDADE
Registro obrigatório utilizado para complementar as informações de identificação do informante do arquivo.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0005” C 004 - O
02 FANTASIA Nome de fantasia associado ao nome empresarial. C 060 - O
03 CEP Código de Endereçamento Postal. N 008* - O
04 END Logradouro e endereço do imóvel. C 060 - O
05 NUM Número do imóvel. C 010 - OC
06 COMPL Dados complementares do endereço. C 060 - OC
07 BAIRRO Bairro em que o imóvel está situado. C 060 - O
08 FONE Número do telefone (DDD+FONE). C 11 - OC
09 FAX Número do fax. C 11 - OC
10 EMAIL Endereço do correio eletrônico. C - - OC
Observações:
Nível hierárquico - 2
Ocorrência – um por arquivo
Campo 01 (REG) - Valor Válido: [0005]
Campo 02 (FANTASIA) – Preenchimento: caso não possua nome de fantasia, preencher com parte da razão social pela qual
é conhecida.
----
REGISTRO 0015: DADOS DO CONTRIBUINTE SUBSTITUTO OU RESPONSÁVEL PELO
ICMS DESTINO
Registro obrigatório para todos os contribuintes substitutos tributários do ICMS, conforme definidos na legislação
pertinente. Deve ser gerado um registro para cada uma das inscrições estaduais cadastradas nas unidades federadas dos
contribuintes substituídos, ainda que não tenha tido movimentação no período, ficando obrigado à apresentação dos registros
E200, E300 e respectivos filhos.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0015" C 004 - O
02 UF_ST Sigla da unidade da federação do contribuinte substituído ou C 002* - O
unidade de federação do consumidor final não contribuinte - ICMS
Destino EC 87/15.
03 IE_ST Inscrição Estadual do contribuinte substituto na unidade da C 014 - O
federação do contribuinte substituído ou unidade de federação do
consumidor final não contribuinte - ICMS Destino EC 87/15.
Observações:
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [0015]
Campo 02 (UF_ST) - Preenchimento: informar a sigla da UF onde o contribuinte possui inscrição como substituto tributário.
Validação: O valor deve ser a sigla de uma unidade da federação existente.
Campo 03 (IE_ST) - Preenchimento: informar a inscrição estadual do contribuinte na unidade de federação onde ele estiver inscrito como substituto tributário.
Validação: valida a Inscrição Estadual, considerando a UF informada no registro.
----
REGISTRO 0100: DADOS DO CONTABILISTA
Registro utilizado para identificação do contabilista responsável pela escrituração fiscal do estabelecimento, mesmo
que o contabilista seja funcionário da empresa ou prestador de serviço.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0100”. C 004 - O
02 NOME Nome do contabilista. C 100 - O
03 CPF Número de inscrição do contabilista no CPF. N 011* - O
04 CRC Número de inscrição do contabilista no Conselho Regional de C 015 - O
Contabilidade.
05 CNPJ Número de inscrição do escritório de contabilidade no CNPJ, se N 014* - OC
houver.
06 CEP Código de Endereçamento Postal. N 008* - OC
07 END Logradouro e endereço do imóvel. C 060 - OC
08 NUM Número do imóvel. C 010 - OC
09 COMPL Dados complementares do endereço. C 060 - OC
10 BAIRRO Bairro em que o imóvel está situado. C 060 - OC
11 FONE Número do telefone (DDD+FONE). C 11 - OC
12 FAX Número do fax. C 11 - OC
13 EMAIL Endereço do correio eletrônico. C - - O
14 COD_MU Código do município, conforme tabela IBGE. N 007* - O
N
Observações:
Nível hierárquico – 2
Ocorrência – um por arquivo
Campo 01 (REG) - Valor válido: [0100]
Campo 02 (NOME) - Preenchimento: informar o nome do contabilista responsável.
Campo 03 (CPF) - Preenchimento: informar o número do CPF do contabilista responsável; não utilizar os caracteres especiais
de formatação, tais como: ".", "/", "-".
Validação: será conferido o dígito verificador (DV) do CPF informado.
Campo 04 (CRC) - Preenchimento: informar o número de inscrição do contabilista no Conselho Regional de Contabilidade na UF do estabelecimento.
Campo 05 (CNPJ) - Preenchimento: informar o número de inscrição no Cadastro Nacional de Pessoa Jurídica do escritório de contabilidade; não informar caracteres de formatação, tais como: ".", "/", "-".
Validação: será conferido o dígito verificador (DV) do CNPJ informado.
Campo 06 (CEP) - Preenchimento: informar o número do Código de Endereçamento Postal - CEP, conforme cadastro nos CORREIOS.
Campo 07 (END) - Preenchimento: informar o endereço do contabilista/escritório de contabilidade.
Campo 13(EMAIL) - Preenchimento: informar o endereço de correio eletrônico do contabilista/escritório de contabilidade.
Este endereço de e-mail poderá ser utilizado para envio de correspondências.
Campo 14 (COD_MUN) - Preenchimento: informar o código do município do domicílio fiscal do contabilista/escritório de contabilidade.
Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE (combinação do código da UF e o código de município), possuindo 7 dígitos.
----
REGISTRO 0150: TABELA DE CADASTRO DO PARTICIPANTE
Registro utilizado para informações cadastrais das pessoas físicas ou jurídicas envolvidas nas transações comerciais
com o estabelecimento, no período. Participantes sem movimentação no período não devem ser informados neste registro.
Obs.: Não devem ser informados como participantes os CNPJ e CPF apenas citados nos registros C350 – Nota Fiscal de Venda ao Consumidor, C460 – Documento Fiscal emitido por ECF e no C100, quando se tratar de NFC-e - Nota Fiscal Eletrônica ao Consumidor Final - modelo 65.
O código a ser utilizado é de livre atribuição pelo contribuinte e possui validade para o arquivo informado. Este código deve ser único para o participante, não havendo necessidade, sempre que possível, de se criar um código para cada período.
Não podem ser informados dois ou mais registros com o mesmo Código de Participante.
Para o caso de participante pessoa física com mais de um endereço, podem ser fornecidos mais de um registro, com o
mesmo NOME e CPF. Neste caso, deve ser usado um COD_PART para cada registro, alterando os demais dados.
As informações deste registro representam os dados atualizados no último evento fiscal (emissão/recebimento de
documento fiscal) da EFD-ICMS/IPI.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0150”. C 004 - O
02 COD_PART Código de identificação do participante no arquivo. C 060 - O
03 NOME Nome pessoal ou empresarial do participante. C 100 - O
04 COD_PAIS Código do país do participante, conforme a tabela N 005 - O
indicada no item 3.2.1
05 CNPJ CNPJ do participante. N 014* - OC
06 CPF CPF do participante. N 011* - OC
07 IE Inscrição Estadual do participante. C 014 - OC
08 COD_MUN Código do município, conforme a tabela IBGE N 007* - OC
09 SUFRAMA Número de inscrição do participante na SUFRAMA. C 009* - OC
10 END Logradouro e endereço do imóvel C 060 - O
11 NUM Número do imóvel C 010 - OC
12 COMPL Dados complementares do endereço C 060 - OC
13 BAIRRO Bairro em que o imóvel está situado C 060 - OC
Observações:
Nível hierárquico - 2
Ocorrência –vários por arquivo
Campo 01 (REG) - Valor válido: [0150]
Campo 02 (COD_PART) - Preenchimento: informar o código de identificação do participante no arquivo.
Esta tabela pode conter COD_PART e respectivo registro 0150 com dados do próprio contribuinte informante, quando
apresentar documentos emitidos contra si próprio, em situações específicas (Exemplo: emissão de Nota Fiscal em operação de retorno de produtos saídos para venda ambulante ou a negociar fora do estabelecimento).
Validação: o valor informado no campo COD_PART deve existir em, pelo menos, um registro dos demais blocos.
O código de participante, campo COD_PART, é de livre atribuição do estabelecimento, observado o disposto no item 2.4.2.1 da Nota Técnica, conforme Ato COTEPE/ICMS nº 44/2018 e alterações.
Campo 04 (COD_PAIS) - Preenchimento: informar o código do país, conforme tabela indicada no item 3.2.1 da Nota Técnica,
conforme Ato COTEPE/ICMS nº 44/2018 e alterações. O código de país pode ser informado com 05 caracteres ou com 04
caracteres (desprezando o caractere “0” (zero) existente à esquerda).
Validação: o valor informado no campo deve existir na Tabela de Países. Informar, inclusive, quando o participante for
estabelecido ou residente no Brasil (01058 ou 1058).
Campo 05 (CNPJ) - Preenchimento: informar o número do CNPJ do participante, não informar caracteres de formatação, tais
como: ".", "/", "-". Se COD_PAIS diferente de Brasil, o campo não deve ser preenchido.
Validação: é conferido o dígito verificador (DV) do CNPJ informado. Obrigatoriamente um dos campos, CPF ou CNPJ, deverá
ser preenchido.
Campo 06 (CPF) - Preenchimento: informar o número do CPF do participante; não utilizar os caracteres especiais de
formatação, tais como: “.”, “/”, “-”. Se COD_PAIS diferente de Brasil, o campo não deve ser preenchido.
Validação: é conferido o dígito verificador (DV) do CPF informado. Obrigatoriamente um dos campos, CPF ou CNPJ, deverá
ser preenchido.
Obs.: Os campos 05 e 06 são mutuamente excludentes, sendo obrigatório o preenchimento de um deles quando o campo 04
estiver preenchido com “01058” ou “1058” (Brasil).
Campo 07 (IE) - Validação: valida a Inscrição Estadual de acordo com a UF informada no campo COD_MUN (dois primeiros
dígitos do código de município).
Campo 08 (COD_MUN) - Validação: o valor informado no campo deve existir na Tabela de Municípios do IBGE (combinação
do código da UF e o código de município), possuindo 7 dígitos.
Obrigatório se campo COD_PAIS for igual a “01058” ou “1058”(Brasil). Se for exterior, informar campo “vazio” ou preencher com o código “9999999”.
Campo 09 (SUFRAMA) - Preenchimento: informar o número de Inscrição do participante na SUFRAMA, se houver.
Validação: é conferido o dígito verificador (DV) do número de inscrição na SUFRAMA, se informado.
Campo 10 (END) - Preenchimento: informar o logradouro e endereço do imóvel. Se o participante for do exterior, preencher inclusive com a cidade e país.
----
REGISTRO 0175: ALTERAÇÃO DA TABELA DE CADASTRO DE PARTICIPANTE
Este registro é de preenchimento obrigatório quando houver, dentro do período, alteração nos dados informados no
registro 0150, campos: NOME, COD_PAIS, CNPJ, CPF, COD_MUN, SUFRAMA, END, NUM, COMPL e BAIRRO.
Não pode ser utilizado, em um mesmo arquivo, um mesmo código para representar um participante diferente do referenciado anteriormente
por tal código.
Os dados informados neste registro serão considerados até as 24:00 horas do dia anterior à data de alteração.
Quando houver mudança de INSCRIÇÃO ESTADUAL, deve ser criado novo participante e este registro não deve ser
informado.
ATENÇÃO: Para mudança de endereço, este registro só deve ser informado quando houver emissão ou recebimento,
no mesmo mês, de duas ou mais Notas Fiscais para endereços diferentes do mesmo participante.
Se a mudança de endereço implicar alteração de inscrição estadual, deverá ser informado um registro 0150 para este
novo participante e, portanto, não deve ser informado o registro 0175.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0175” C 004 - O
02 DT_ALT Data de alteração do cadastro N 008* - O
03 NR_CAMPO Número do campo alterado (campos 03 a 13, exceto 07) C 002 - O
04 CONT_ANT Conteúdo anterior do campo C 100 - O
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [0175]
Campo 02 (DT_ALT) - Validação: o valor informado no campo deve estar entre o campo DT_INI e o campo DT_FIN do registro 0000.
Campo 03 (NR_CAMPO) - Preenchimento: informar o número do campo alterado, relativo ao registro 0150.
Validação: Valores Válidos: [03, 04, 05, 06, 08, 09, 10, 11, 12, 13]
Campo 04 (CONT_ANT) - Preenchimento: os dados informados neste registro são válidos até às 24:00 horas do dia anterior à data de alteração.
Validação: quando se tratar de alterações nos campos CNPJ ou CPF, referidos campos serão validados conforme as regras de
verificação de dígitos verificadores. Se o NR_CAMPO = 08 (COD_MUN) será verificada sua existência na tabela IBGE.
----
REGISTRO 0190: IDENTIFICAÇÃO DAS UNIDADES DE MEDIDA
Este registro tem por objetivo descrever as unidades de medidas utilizadas no arquivo digital. Não podem ser informados dois ou mais registros com o mesmo código de unidade de medida. Somente devem constar as unidades de medidas informadas em qualquer outro registro.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0190" C 004 - O
02 UNID Código da unidade de medida C 006 - O
03 DESCR Descrição da unidade de medida C - - O
Observações:
Nível hierárquico: 2
Ocorrência: vários por arquivo
Campo 01 (REG) - Valor Válido: [0190]
Campo 02 (UNID) - Validação: o valor informado neste campo deve existir em, pelo menos, um outro registro do arquivo.
----
REGISTRO 0200: TABELA DE IDENTIFICAÇÃO DO ITEM (PRODUTO E SERVIÇOS)
Este registro tem por objetivo informar mercadorias, serviços, produtos ou quaisquer outros itens concernentes às transações fiscais e aos movimentos de estoques em processos produtivos, bem como os insumos. Quando ocorrer alteração somente na descrição do item, sem que haja descaracterização deste, ou seja, criação de um novo item, a alteração deve constar no registro 0205.
Validação do registro: somente devem ser apresentados itens referenciados nos demais blocos, exceto se for apresentado o fator de conversão no registro 0220 (a partir de julho de 2012) ou alteração do item no registro 0205 (a partir de janeiro de 2021) ou correlação entre códigos de itens comercializados no registro 0221 (a partir de janeiro de 2023).
A identificação do item (produto ou serviço) deverá receber o código próprio do informante do arquivo em qualquer documento, lançamento efetuado ou arquivo informado (significa que o código de produto deve ser o mesmo na emissão dos documentos fiscais, na entrada das mercadorias ou em qualquer outra informação prestada ao fisco), observando-se ainda que:
a) O código utilizado não pode ser duplicado ou atribuído a itens (produto ou serviço) diferentes. Os produtos e serviços que sofrerem alterações em suas características básicas deverão ser identificados com códigos diferentes. Em caso de alteração de codificação, deverão ser informados o código e a descrição anteriores e as datas de validade inicial e final no registro 0205;
b) Não é permitida a reutilização de código que tenha sido atribuído para qualquer produto anteriormente.
c) O código de item/produto a ser informado no Inventário deverá ser aquele utilizado no mês inventariado. Atualização: 31 de outubro de 2024
d) A discriminação do item deve indicar precisamente o mesmo, sendo vedadas discriminações diferentes para o mesmo item ou discriminações genéricas (a exemplo de “diversas entradas”, “diversas saídas”, “mercadorias para revenda”, etc), ressalvadas as operações abaixo, desde que não destinada à posterior circulação ou apropriação na produção:
1 - de aquisição de “materiais para uso/consumo” que não gerem direitos a créditos;
2 - que discriminem por gênero a aquisição de bens para o "ativo fixo" (e sua baixa);
3 - que contenham os registros consolidados relativos aos contribuintes com atividades econômicas de fornecimento de energia elétrica, de fornecimento de água canalizada, de fornecimento de gás canalizado, e de prestação de serviço de comunicação e telecomunicação que poderão, a critério do Fisco, utilizar registros consolidados por classe de consumo para representar suas saídas ou prestações.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0200" C 004 - O
02 COD_ITEM Código do item C 060 - O
03 DESCR_ITEM Descrição do item C - - O
04 COD_BARRA Representação alfanumérico do código de barra C - - OC
do produto, se houver
05 COD_ANT_ITEM Código anterior do item com relação à última C 060 - N (informar no
informação apresentada. 0205)
06 UNID_INV Unidade de medida utilizada na quantificação de C 006 - O
estoques.
07 TIPO_ITEM Tipo do item – Atividades Industriais, N 2 - O
Comerciais e Serviços:
00 – Mercadoria para Revenda;
01 – Matéria-prima;
02 – Embalagem;
03 – Produto em Processo;
04 – Produto Acabado;
05 – Subproduto;
06 – Produto Intermediário;
07 – Material de Uso e Consumo;
08 – Ativo Imobilizado;
09 – Serviços;
10 – Outros insumos;
99 – Outras
08 COD_NCM Código da Nomenclatura Comum do Mercosul C 008* - OC
09 EX_IPI Código EX, conforme a TIPI C 003 - OC
10 COD_GEN Código do gênero do item, conforme a Tabela N 002* - OC
4.2.1
11 COD_LST Código do serviço conforme lista do Anexo I da C 005 OC
Lei Complementar Federal nº 116/03.
12 ALIQ_ICMS Alíquota de ICMS aplicável ao item nas N 006 02 OC
operações internas
13 CEST Código Especificador da Substituição Tributária N 007* - OC
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Observações:
1. O Código do Item deverá ser preenchido com as informações utilizadas na última ocorrência do período.
2. O campo COD_NCM é obrigatório:
2.1) para empresas industriais e equiparadas a industrial, referente aos itens correspondentes à atividade fim, ou quando gerarem créditos e débitos de IPI;
2.2) para contribuintes de ICMS que sejam substitutos tributários;
2.3) para empresas que realizarem operações de exportação ou importação.
3. Não existe COD-NCM para serviços.
4. O campo COD_GEN é obrigatório a todos os contribuintes somente na aquisição de produtos primários.
5. O campo CEST é válido a partir de 01/01/2017. Atualização: 31 de outubro de 2024
Campo 01 (REG) - Valor Válido: [0200]
Campo 02 (COD_ITEM) - Preenchimento: informar com códigos próprios do informante do arquivo os itens das operações
de entradas de mercadorias ou aquisições de serviços, bem como das operações de saídas de mercadorias ou prestações de
serviços, bem como dos produtos e subprodutos gerados no processo produtivo.
Validação: o valor informado neste campo deve existir em, pelo menos, um registro dos demais blocos ou no registro 0220.
Campo 03 (DESCR_ITEM) - Preenchimento: são vedadas descrições diferentes para o mesmo item ou descrições genéricas,
ressalvadas as operações abaixo, desde que não destinada à posterior circulação ou apropriação na produção:
1- de aquisição de “materiais para uso/consumo” que não gerem direitos a créditos;
2- que discriminem por gênero a aquisição de bens para o “ativo fixo” (e sua baixa);
3- que contenham os registros consolidados relativos aos contribuintes com atividades econômicas de fornecimento
de energia elétrica, de fornecimento de água canalizada, de fornecimento de gás canalizado e de prestação de serviço de
comunicação e telecomunicação que poderão, a critério do Fisco, utilizar registros consolidados por classe de consumo para
representar suas saídas ou prestações.
É permitida a modificação da descrição, desde que não implique descaracterização do produto. Neste caso, o campo
deve ser preenchido com a atual descrição utilizada no período. As descrições substituídas devem ser informadas nos registros
0205.
Campo 04 (COD_BARRA) - Preenchimento: informar o código GTIN-8, GTIN-12, GTIN-13 ou GTIN-14 (antigos códigos
EAN, UPC e DUN-14). Não informar o conteúdo do campo se o produto não possui este código.
Campo 05 (COD_ANT_ITEM) - Não preencher. Se houver a informação, esta deve ser prestada no registro 0205.
Campo 06 (UNID_INV) - Validação: Deve existir no registro 0190, campo UNID.
Campo 07 (TIPO_ITEM) - Preenchimento: informar o tipo do item aplicável. Nas situações de um mesmo código de item
possuir mais de um tipo de item (destinação), deve ser informado o tipo de maior relevância na movimentação física, observadas,
no que couberem, as regras de escrituração do Bloco K.
Deve ser informada a destinação inicial do produto, considerando-se os conceitos:
00 - Mercadoria para revenda – produto adquirido para comercialização;
01 – Matéria-prima: a mercadoria que componha, física e/ou quimicamente, um produto em processo ou produto acabado e
que não seja oriunda do processo produtivo. A mercadoria recebida para industrialização é classificada como Tipo 01, pois
não decorre do processo produtivo, mesmo que no processo de produção se produza mercadoria similar classificada como
Tipo 03;
03 – Produto em processo: o produto que possua as seguintes características, cumulativamente: oriundo do processo produtivo;
e, predominantemente, consumido no processo produtivo. Dentre os produtos em processo está incluído o produto resultante
caracterizado como retorno de produção. Um produto em processo é caracterizado como retorno de produção quando é
resultante de uma fase de produção e é destinado, rotineira e exclusivamente, a uma fase de produção anterior à qual o mesmo
foi gerado. No “retorno de produção”, o produto retorna (é consumido) a uma fase de produção anterior à qual ele foi gerado.
Isso é uma excepcionalidade, pois o normal é o produto em processo ser consumido em uma fase de produção posterior à qual
ele foi gerado, e acontece, portanto, em poucos processos produtivos.
04 – Produto acabado: o produto que possua as seguintes características, cumulativamente: oriundo do processo produtivo;
produto final resultante do objeto da atividade econômica do contribuinte; e pronto para ser comercializado;
05 - Subproduto: o produto que possua as seguintes características, cumulativamente: oriundo do processo produtivo e não é
objeto da produção principal do estabelecimento; tem aproveitamento econômico; não se enquadre no conceito de produto em
processo (Tipo 03) ou de produto acabado (Tipo 04);
06 – Produto intermediário - aquele que, embora não se integrando ao novo produto, for consumido no processo de
industrialização.
A classificação da mercadoria não se altera a cada movimentação. Exemplo: não há impedimento para que uma mercadoria
classificada como produto em processo – tipo 03 seja vendida, assim como não há impedimento para que uma mercadoria
classificada como produto acabado – tipo 04 seja consumida no processo produtivo para obtenção de outro produto resultante.
Deve ser considerada a atividade econômica do estabelecimento informante, e não da empresa.
Valores válidos: [00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 99]
Atualização: 31 de outubro de 2024
Campo 08 (COD_NCM) – Preenchimento: para as empresas industriais ou equiparadas é obrigatório informar o Código NCM,
conforme a Nomenclatura Comum do MERCOSUL. Não existe COD-NCM para serviços.
Para as demais empresas, é obrigatória a informação da NCM para os itens importados, exportados ou, no caso de substituição
tributária, para os itens sujeitos à substituição, quando houver a retenção do ICMS.
Validação: o preenchimento do campo é obrigatório se o campo IND_ATIV do registro 0000 for igual a “0” (zero) (industrial
ou equiparado a industrial), mas apenas para os itens correspondentes à atividade-fim ou quando gerarem créditos e débitos de
IPI. Fica dispensado o preenchimento deste campo, quando o tipo de item informado no campo TIPO_ITEM for igual a 07 -
Material de Uso e Consumo; ou 08 – Ativo Imobilizado; ou 09 -Serviços; ou 10 - Outros insumos; ou 99 - Outras.
Campo 09 (EX_IPI) - Preenchimento: informar com o Código de Exceção de NCM, de acordo com a Tabela de Incidência
do Imposto de Produtos Industrializados (TIPI), quando existir.
Campo 10 (COD_GEN) - Preenchimento: obrigatório para todos os contribuintes na aquisição de produtos primários. A
Tabela "Gênero do Item de Mercadoria/Serviço", referenciada no Item 4.2.1 da Nota Técnica (Ato COTEPE/ICMS nº 44/2018
e alterações), corresponde à tabela de "Capítulos da NCM", acrescida do código "00 - Serviço".
Validação: o valor informado no campo deve existir na Tabela “Gênero do Item de Mercadoria/Serviço”, item 4.2.1 da Nota
Técnica (Ato COTEPE/ICMS nº 44/2018 e alterações).
Campo 11 (COD_LST) - Preenchimento: informar o código de serviços, de acordo com a Lei Complementar 116/03. A partir
de janeiro de 2015, preencher como na NF-e, formato NN.NN
Campo 12 (ALIQ_ICMS) - Preenchimento: neste campo deve ser informada a alíquota interna prevista em regulamento,
incluindo alíquota relacionada ao Fundo de Combate à Pobreza, se aplicável, conforme a legislação de cada UF.
Regra de validação para o campo “ALIQ_ICMS”: Para todos os itens com registros C180, C185, C330, C380, C430, C480,
C810 e C870, o preenchimento do campo 12 é obrigatório.
Campo 13 (CEST) - Preenchimento: Nos casos em que mais de um código CEST puder ser atribuído a um único produto no
momento da saída, ou seja, quando a associação do CEST ao item em estoque depender da finalidade à qual o item será
destinado pelo adquirente, este campo não deve ser informado.
Validação: o valor informado no campo deve existir na Tabela Código Especificador da Substituição Tributária- CEST.
----
REGISTRO 0205: ALTERAÇÃO DO ITEM
Este registro tem por objetivo informar alterações ocorridas na descrição do produto ou quando ocorrer alteração na
codificação do produto, desde que não o descaracterize ou haja modificação que o identifique como sendo novo produto. Caso
não tenha ocorrido movimentação no período da alteração do item, deverá ser informada no primeiro período em que houver
movimentação do item ou no inventário.
Validação do Registro: Não podem ser informados dois ou mais registros com sobreposição de períodos para o
mesmo campo alterado (02 ou 05).
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0205" C 004 - O
02 DESCR_ANT_ITEM Descrição anterior do item C - - OC
03 DT_INI Data inicial de utilização da descrição do item N 008* - O
04 DT_FIM Data final de utilização da descrição do item N 008* - O
05 COD_ANT_ITEM Código anterior do item com relação à última informação C 060 - OC
apresentada.
Observações: Os campos 02 e 05 são mutuamente excludentes, sendo obrigatório o preenchimento de um deles. Em caso de alteração da DESCR_ANT_ITEM e do COD_ANT_ITEM deverá ser gerado um registro para cada alteração.
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [0205]
Campo 03 (DT_INI) - Preenchimento: informar a data inicial de utilização da descrição anterior do item.
Validação: o valor informado no campo deve ser uma data válida no formato “ddmmaaaa”.
Campo 04 (DT_FIM) - Preenchimento: informar o período final de utilização da descrição anterior do item.
Validação: o valor informado no campo deve ser uma data válida, obedecido o formato “ddmmaaaa”. O valor informado no
campo deve ser menor que o valor no campo DT_FIN do registro 0000.
----
REGISTRO 0206: CÓDIGO DE PRODUTO CONFORME TABELA PUBLICADA PELA ANP
Este registro tem por objetivo informar o código correspondente ao produto constante na Tabela da Agência Nacional
de Petróleo (ANP).
Deve ser apresentado apenas pelos contribuintes produtores, importadores, distribuidores e postos de combustíveis.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0206" C 004 - O
02 COD_COMB Código do produto, conforme tabela publicada pela ANP C - - O
Observações:
Nível hierárquico - 3
Ocorrência - 1:1
Campo 01 (REG) - Valor Válido: [0206]
Campo 02 (COD_COMB) - Preenchimento: utilizar o código do produto, conforme Tabela de Produtos para Combustíveis /
Solvente (Tabela 12 de códigos de produtos para o Sistema de Informações de Movimentação de Produtos (SIMP), conforme
item 3.2.1 da Nota Técnica (Ato COTEPE/ICMS nº 44/2018 e alterações).
Validação: o valor informado no campo deve existir na tabela da ANP.
Perguntas e Respostas:
1) Há algum relacionamento com o campo TIPO_ITEM do registro 0200?
Resposta: Sim, esta informação é vinculada ao código do item e obrigatória quando se referir a produto constante na Tabela
ANP e o informante do arquivo for produtor, importador, distribuidor ou posto de combustível.
----
REGISTRO 0210: CONSUMO ESPECÍFICO PADRONIZADO (VÁLIDO ATÉ 31/12/2021)
Até dezembro de 2017, este registro deve ser apresentado, caso exista produção e/ou consumo nos Registros K230/K235 e K250/K255.
A partir de janeiro de 2018, a obrigatoriedade da apresentação deste registro ficará a critério de cada UF, caso exista produção e consumo nos Registros K230/K235 e K250/K255.
Deve ser informado o consumo específico padronizado esperado e a perda normal percentual esperada de um insumo/componente para se produzir uma unidade de produto resultante, segundo as técnicas de produção de sua atividade e o projeto do produto resultante, referentes aos produtos que foram fabricados pelo próprio estabelecimento ou por terceiro.
Este registro somente deve existir quando o conteúdo do campo 7 - TIPO_ITEM do Registro 0200 for igual a 03 (produto em processo) ou 04 (produto acabado).
Se existirem insumos interdependentes (insumos em que o aumento da participação de um resulta em diminuição da participação de outro ou outros) deverá ser eleito um insumo de cada grupamento interdependente para informação do total de consumo específico padrão ou perda normal percentual do conjunto de insumos que representa (na unidade do insumo eleito).
Os demais insumos do grupamento interdependente serão considerados substitutos e deverão ser informados somente nos
Registros K235 ou K255 com a informação do insumo substituído.
A unidade de medida é, obrigatoriamente, a de controle de estoque constante no registro 0200 – campo UNID_INV.
Validação do Registro: Não podem ser informados dois ou mais registros com o mesmo campo COD_ITEM do
Registro 0200 e o mesmo campo COD_ITEM_COMP. Somente devem ser apresentados itens referenciados nos demais blocos.
Nº Campo Descrição Tipo Tam Dec Obrig.
01 REG Texto fixo contendo "0210" C 4 - O
02 COD_ITEM_COMP Código do item componente/insumo (campo 02 do C 60 - O
Registro 0200)
03 QTD_COMP Quantidade do item componente/insumo para se N - 6 O
produzir uma unidade do item composto/resultante
04 PERDA Perda/quebra normal percentual do N - 4 O
insumo/componente para se produzir uma unidade
do item composto/resultante
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [0210]
Campo 02 (COD_ITEM_COMP) – Validações:
a) o código do componente/insumo deverá existir no campo COD_ITEM do Registro 0200;
b) o código do item componente/insumo deve ser diferente do código do produto resultante - Reg. 0200 correspondentes ao
nível hierárquico superior ao Registro 0210 que se declara;
c) o tipo do componente/insumo (campo TIPO_ITEM do Registro 0200) deve ser igual a 00, 01, 02, 03, 04, 05 ou 10.
Campo 03 (QTD_COMP) – Preenchimento: deverá ser preenchido tendo como base a quantidade bruta de insumo a ser
consumida por unidade do item composto, considerando-se apenas a perda normal do processo industrial. No caso da existência
de variáveis no processo produtivo que possam influenciar no consumo específico, o consumo específico padronizado será
médio. Este valor deve ser maior que zero.
Campo 04 (PERDA) - Preenchimento: a perda ou quebra normal percentual refere-se à parte do insumo que não se transformou em produto resultante. Este campo depende da eficiência dos processos de cada contribuinte. Não se incluem neste campo fatos como inundações, perecimento por expiração de validade, deterioração e quaisquer situações que impliquem a diminuição da quantidade em estoque sem relação com o processo produtivo do contribuinte. No caso da existência de variáveis no processo produtivo que possam influenciar na perda, deverá ser informada neste registro a perda média.
----
REGISTRO 0220: FATORES DE CONVERSÃO DE UNIDADES
Este registro tem por objetivo informar os fatores de conversão entre as unidades comerciais informadas para
determinado produto nos registros dos documentos fiscais e a respectiva unidade de estoque informada para o produto no campo
06-UNID_INV do registro 0200.
Nos documentos eletrônicos de emissão própria, quando a unidade comercial adotada for diferente da unidade do
estoque escriturada no campo 06-UNID_INV do registro 0200, este registro deverá ser informado. Quando for utilizada unidade
de inventário (bloco H) ou unidade de medida de controle de estoque (bloco K) diferente da unidade comercial do produto é
necessário informar o registro 0220 para informar os fatores de conversão entre as unidades. Na movimentação interna entre
mercadorias (Registro K220), caso a unidade de medida da mercadoria de destino for diferente da unidade de medida da
mercadoria de origem, este registro é obrigatório para informar o fator de conversão entre a unidade de medida de origem e a
unidade de medida de destino.
Também, deverá ser informado este registro, quando o código da unidade de estoque declarado para o item no registro
0200 (campo 06-UNID_INV) for diferente do código da unidade de estoque declarado para o mesmo item no arquivo EFD da
competência anterior.
Validação do Registro: Não podem ser informados dois ou mais registros com o mesmo conteúdo no campo
UNID_CONV.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0220" C 004 - O
02 UNID_CONV Unidade comercial a ser convertida na unidade de estoque, C 006 - O
referida no registro 0200. Ou unidade do 0200 utilizada na EFD
anterior.
03 FAT_CONV Fator de conversão: fator utilizado para converter (multiplicar) a N - 6 O
unidade a ser convertida na unidade adotada no inventário.
04 COD_BARRA C - - OC
Representação alfanumérica do código de barra da unidade
comercial do produto, se houver
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [0220]
Campo 02 (UNID_CONV) - Validação: o valor informado no campo deve existir no campo UNID do registro 0190.
Campo 03 (FAT_CONV) - Preenchimento:
a) o valor do fator de conversão informado para transformar o código da unidade comercial (código identificado no
campo 02-UNID_CONV deste registro) no respectivo código de unidade de estoque do produto (código identificado no campo
06-UNID_INV do respectivo registro 0200) não poderá ser diferente do valor declarado nos demais arquivos EFD. Havendo
necessidade de utilizar diferentes valores de fatores de conversão, o contribuinte não poderá reaproveitar o mesmo código de
unidade comercial, pois, neste caso, deverá ser adotado um código de unidade comercial distinto, eis que, se o volume é diverso,
trata-se de uma unidade comercial diferente.
Exemplo: Empresa adota, em janeiro de 2020, a unidade comercial “UN" (uma unidade) para determinado produto
nos documentos fiscais emitidos, sendo essa unidade informada nos registros do Bloco C, nos documentos fiscais eletrônicos
de emissão própria e no registro 0190, porém escritura no campo 06-UNID_INV do registro 0200 o código de unidade de
estoque “CX” (caixa com 10 unidades) para este mesmo produto, sendo, então, informado no registro 0220 um fator de
conversão 0,10 (campo 03-FAT_CONV) para esse código de unidade comercial “UN" (campo 02-UNID_CONV) deste
produto (1 UN deste produto corresponde a 0,10 CX deste mesmo produto). Porém, sabendo-se que, em fevereiro de 2020, o
código da unidade de estoque permanece sendo “CX” para este produto (campo 06-INID_INV do 0200), mas a empresa
necessita comercializar este produto em um volume diferente do demonstrado em janeiro através do código “UN", logo,
obrigatoriamente, deverá adotar um novo código de unidade comercial para este produto, por exemplo, “PAC2” (pacote com
duas unidades). Assim, demonstrará essa nova relação de conversão (fator de conversão) entre “PAC2” e “CX” para este
produto através do registro 0220, como, por exemplo, um fator de conversão 0,20 para esse código de unidade “PAC2” (um
PAC2 corresponde a 0,2 CX). Assim, no campo 02-UNID_CONV do registro 0220 de fevereiro terá a identificação de um
novo código de unidade “PAC2” (pacote com 2 unidades), sendo esse mesmo código escriturado no registro 0190, pois é
vedado reaproveitar em fevereiro o código “UN" adotado em janeiro para representar um volume diferente (0,20) em relação
a mesma unidade de inventário “CX” e, caso queira continuar utilizando o código de unidade “UN" em fevereiro para este
mesmo produto, terá que informar no registro 0220 o mesmo fator de conversão adotado em janeiro, ou seja, o valor 0,10
exemplificado acima. Portanto, se representam volumes distintos, independente do arquivo escriturado, os códigos das unidades
comerciais adotados deverão ser distintos.
b) a orientação expressa na letra ‘a’ acima se aplica, também, no caso de informação do registro 0220 para demonstrar
o fator de conversão na ocorrência de alteração no código da unidade de estoque (campo 06-UNID_INV do registro 0200) entre
arquivos EFD de competências subsequentes, ou seja, o fator de conversão não poderá ser alterado entre arquivos para os
mesmos códigos de unidades de estoque referenciados. Havendo necessidade de adotar um novo valor de fator de conversão,
deverá ser utilizado um novo código de unidade de estoque.
Validação: o valor informado no campo deve ser maior que “0” (zero).
Campo 04 (COD_BARRA) - Preenchimento: informar o código GTIN-8, GTIN-12, GTIN-13 ou GTIN-14 da unidade
comercial. Não informar o conteúdo do campo se a unidade comercial do produto não possuir este código.
Validações:
a) Se o valor for informado, deverá também estar preenchido no Registro 0200.
b) Caso o valor informado do COD_BARRA da unidade comercial seja um código GTIN-14, ele deve corresponder ao
código GTIN-8, GTIN-12 ou GTIN-13 referido no Registro 0200.
c) Caso o valor informado do COD_BARRA da unidade comercial seja um código GTIN-8, GTIN-12 ou GTIN-13, ele deve
ser divergente do código referido no Registro 0200.
----
REGISTRO 0221: CORRELAÇÃO ENTRE CÓDIGOS DE ITENS COMERCIALIZADOS
O registro deverá ser informado apenas se o campo TIPO_ITEM do registro 0200 Pai for informado com valor “00 –
Mercadoria para Revenda”.
A obrigatoriedade, que só poderá ser estabelecida a partir de 2024, e a forma de escrituração deste registro serão
definidas pela UF de domicílio do declarante. Os contribuintes obrigados, caso não tenham informado o registro nas EFD de
2023, deverão informar, na EFD de janeiro de 2024, todos os códigos de item inativados ou alterados no exercício de 2023.
Este registro tem por objetivo informar a correlação entre os diversos códigos de item, relacionados a uma mesma
mercadoria, utilizados nos documentos fiscais de entrada e de saída e nos registros da EFD ICMS-IPI. A correlação será feita
sempre em relação ao item “atômico”, ou seja, aquele que representa a menor unidade de comercialização praticada pelo
estabelecimento.
Nos casos em que os itens são formados pela agregação de mercadorias (kits, cestas básicas etc.), este registro deve
ser informado quando aquele item receber um código específico no estoque. A informação do relacionamento entre os
componentes de uma mercadoria não sobrepõe a legislação de cada UF na forma de emissão de notas de kits e cestas.
No campo 03 QTD_CONTIDA será informada a quantidade de itens “atômicos” contidos no item informado no
registro 0200 pai.
Exemplo 1: se o item 0200 Pai é uma cesta básica que contém 10 diferentes produtos, então, esse 0200 terá 10
Registros 0221 filhos.
Exemplo 2: se o item 0200 Pai é uma lata de refrigerante X com 350ml, então, esse 0200 terá apenas um registro
0221 filho com COD_ITEM_ATOMICO igual ao COD_ITEM do 0200 Pai e QTD_CONTIDA igual a “1”.
Exemplo 3: se o item 0200 Pai é uma caixa com 12 latas de refrigerante X com 350ml, então, esse 0200 terá apenas
um registro 0221 filho com COD_ITEM_ATOMICO igual ao COD_ITEM do 0200 do exemplo 2 e QTD_CONTIDA igual a “12”.
Validação do Registro: Não podem ser informados dois ou mais registros, filhos do 0200 Pai, com o mesmo conteúdo no campo COD_ITEM_ATOMICO. O registro só deverá ser informado se o campo TIPO_ITEM do registro 0200 Pai for informado com valor “00 – Mercadoria para Revenda”.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0221" C 004 - O
02 COD_ITEM_ Informar o código do item atômico contido no item informado C 060 - O
ATOMICO no 0200 Pai.
03 QTD_CONTI Informar quantos itens atômicos estão contidos no item N - 6 O
DA informado no 0200 Pai.
Observações:
Nível hierárquico - 3
Ocorrência - 1:N
Campo 01 (REG) - Valor Válido: [0221]
Campo 02 (COD_ITEM_ATÕMICO) - Validação: o valor informado no campo deve existir no campo COD_ITEM de um
registro 0200 com o campo TIPO_ITEM do registro 0200 preenchido com “00 – Mercadoria para Revenda” e que só tenha um
registro 0221 filho com campo COD_ITEM_ATÔMICO igual ao campo COD_ITEM do registro 0200 Pai.
Campo 03 (QTD_CONTIDA) - Validação: o valor informado deve ser maior ou igual a 1. Quando o campo 02
COD_ITEM_ATÕMICO for igual ao campo 02 COD_ITEM do Registro 0200 Pai, deverá ser igual a “1”.
----
REGISTRO 0300: CADASTRO DE BENS OU COMPONENTES DO ATIVO IMOBILIZADO
Este registro tem o objetivo de identificar e caracterizar todos os bens ou componentes arrolados no registro G125 do
Bloco G e os bens em construção.
O bem ou componente deverá ter código individualizado atribuído pelo contribuinte em seu controle patrimonial do
ativo imobilizado e não poderá ser reutilizado, duplicado, atribuído a bens ou componentes diferentes.
A discriminação do bem ou componente deve indicar precisamente o mesmo, sendo vedadas discriminações diferentes
para o mesmo bem ou componente no mesmo período ou discriminações genéricas.
As informações nos campos IDENT_MERC, DESCR_ITEM, COD_PRNC e COD_CTA devem se referir às
características atuais do bem ou componente.
Deverá também ser apresentado registro que identifique e caracterize o bem que está sendo construído no
estabelecimento do contribuinte, a partir do período de apuração em que adquirir ou consumir o 1º componente.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0300" C 004* - O
02 COD_IND_BEM Código individualizado do bem ou componente adotado no C 060 - O
controle patrimonial do estabelecimento informante
03 IDENT_MERC Identificação do tipo de mercadoria: C 001* - O
1 = bem;
2 = componente.
04 DESCR_ITEM Descrição do bem ou componente (modelo, marca e outras C - - O
características necessárias a sua individualização)
05 COD_PRNC Código de cadastro do bem principal nos casos em que o C 060 - OC
bem ou componente (campo 02) esteja vinculado a um bem
principal.
06 COD_CTA Código da conta analítica de contabilização do bem ou C 060 - O
componente (campo 06 do Registro 0500)
07 NR_PARC Número total de parcelas a serem apropriadas, segundo a N 003 - OC
legislação de cada unidade federada
Observações:
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
Campo 01 (REG) - Valor Válido: [0300]
Campo 03 (IDENT_MERC): Preenchimento: a) bem: uma mercadoria será considerada “bem” quando possua todas as
condições necessárias para ser utilizado nas atividades do estabelecimento. Quando se tratar de “bem” não poderá ser informado
registro G125 com tipo de movimentação igual a “IA” (imobilização em andamento - componente).
b) componente: uma mercadoria será considerada “componente” quando fizer parte de um bem móvel que estiver sendo
construído no estabelecimento do contribuinte, onde somente o bem móvel resultante é que possuirá as condições necessárias
para ser utilizado nas atividades do estabelecimento. Para “componentes” não poderá ser informado o registro G125 com tipo
de movimentação igual a “IM” (imobilização de bem individual) e “CI” (conclusão de imobilização em andamento – bem
resultante).
Campo 05 (COD_PRNC): código do bem que esteja vinculado ao bem ou componente informado no campo 02, seja por se
tratar:
a) de uma imobilização em andamento – código do bem resultante;
b) de um bem vinculado a um bem principal – código do bem principal.
Validação:
a) se o conteúdo do campo IDENT_MERC for igual a “2”, este campo deve obrigatoriamente estar preenchido com o
código do bem principal;
b) O conteúdo deste campo deve existir em outro registro no campo COD_IND_BEM que não tenha o campo
IDENT_MERC igual a “2”.
Obs.: Caso esteja digitando entrada de componentes no registro 0300 (opção CRIAR EFD-ICMS/IPI) é necessário informar
antes os registros 0500, 0600 e o código do bem principal no registro 0300.
Campo 06 (COD_CTA): Preenchimento: conta contábil de acordo com o Plano de Contas adotado pela empresa.
Validações: o conteúdo informado deve existir no campo COD_CTA e ser conta do ativo (COD_NAT_CC igual a “01”),
ambos do registro 0500.
Campo 07 (NR_PARC) - Preenchimento:
a) número total de parcelas a serem apropriadas do bem ou componente, segundo a legislação de cada Unidade Federada. A
maioria das Unidades Federadas adota o número total de parcelas definidas na Lei Complementar 87/96 – 48 parcelas.
Entretanto, algumas Unidades Federadas podem definir um número total de parcelas de forma diversa, seja em função da
periodicidade de apuração do ICMS ou até mesmo em função de um determinado bem;
b) esta informação é obrigatória quando o bem ou componente gerar direito ao crédito de ICMS no momento da sua entrada ou
consumo.
Validação: informação obrigatória quando os campos 09 e 10 do Registro G125 estiverem preenchidos.
----
REGISTRO 0305: INFORMAÇÃO SOBRE A UTILIZAÇÃO DO BEM
Este registro tem o objetivo de prestar informações sobre a utilização do bem, sendo obrigatório quando o conteúdo
do campo IDENT_MERC do registro 0300 for igual a “1” (Bem).
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0305" C 004* - O
02 COD_CCUS Código do centro de custo onde o bem está sendo ou será C 060 - O
utilizado (campo 03 do Registro 0600)
03 FUNC Descrição sucinta da função do bem na atividade do C - - O
estabelecimento
04 VIDA_UTIL Vida útil estimada do bem, em número de meses N 003 - OC
Observações:
Nível hierárquico - 3
Ocorrência – 1:1
Campo 01 (REG) - Valor Válido: [0305]
Campo 02 (COD_CCUS): caso o contribuinte não adote centros de custos deverão ser informados os seguintes códigos:
a) tratando-se de atividade econômica comercial ou de serviços:
Código “1”: área operacional;
Código “2”: área administrativa;
b) tratando-se de atividade econômica industrial:
Código “3”: área produtiva;
Código “4”: área de apoio à produção;
Código “5”: área administrativa.
Validação: o conteúdo informado deve existir no campo COD_CCUS do registro 0600.
----
REGISTRO 0400: TABELA DE NATUREZA DA OPERAÇÃO/PRESTAÇÃO
Este registro tem por objetivo codificar os textos das diferentes naturezas da operação/prestações discriminadas nos
documentos fiscais. Esta codificação e suas descrições são livremente criadas e mantidas pelo contribuinte.
Este registro não se refere ao CFOP. Algumas empresas utilizam outra classificação além das apresentadas nos CFOP.
Esta codificação permite informar estes agrupamentos próprios.
Validação do Registro: Não podem ser informados dois ou mais registros com o mesmo conteúdo no campo COD_NAT.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0400" C 004 - O
02 COD_NAT Código da natureza da operação/prestação C 010 - O
03 DESCR_NAT Descrição da natureza da operação/prestação C - - O
Observações:
Nível hierárquico - 2
Ocorrência – vários (por arquivo)
Campo 01 (REG) - Valor Válido: [0400]
Campo 02 (COD_NAT) - Validação: o valor informado no campo COD_NAT deve existir em pelo menos um registro dos
demais blocos.
----
REGISTRO 0450: TABELA DE INFORMAÇÃO COMPLEMENTAR DO DOCUMENTO
FISCAL
Este registro tem por objetivo codificar todas as informações complementares dos documentos fiscais exigidas pela
legislação fiscal. Estas informações constam no campo “Dados Adicionais” dos documentos fiscais.
Esta codificação e suas descrições são livremente criadas e mantidas pelo contribuinte e não podem ser informados
dois ou mais registros com o mesmo conteúdo no campo COD_INF.
Deverão constar todas as informações complementares de interesse do fisco existentes nos documentos fiscais.
Exemplo: nos casos de documentos fiscais de entradas de devolução, informar o documento fiscal referenciado.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0450" C 004 - O
02 COD_INF Código da informação complementar do documento fiscal. C 006 - O
03 TXT Texto livre da informação complementar existente no documento C - - O
fiscal, inclusive espécie de normas legais, poder normativo,
número, capitulação, data e demais referências pertinentes com
indicações referentes ao tributo.
Observações:
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [0450]
Campo 02 (COD_INF) - Validação: o valor informado deve existir em pelo menos um registro dos demais blocos.
----
REGISTRO 0460: TABELA DE OBSERVAÇÕES DO LANÇAMENTO FISCAL
Este registro é utilizado para informar anotações de escrituração determinadas pela legislação pertinente aos
lançamentos fiscais, tais como: ajustes efetuados por diferimento parcial de imposto, antecipações, diferencial de alíquota e
outros. Esta codificação e suas descrições são de atribuição do contribuinte e não podem ser informados dois ou mais registros
com o mesmo conteúdo no campo COD_OBS.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0460" C 004 - O
02 COD_OBS Código da Observação do lançamento fiscal. C 006 - O
03 TXT Descrição da observação vinculada ao lançamento fiscal C - - O
Observações:
Nível hierárquico - 2
Ocorrência –vários (por arquivo)
Campo 01 (REG) - Valor Válido: [0460]
Campo 02 (COD_OBS) -Validação: o valor informado neste campo deve existir em pelo menos um registro dos demais blocos.
Campo 03 (TXT) - Preenchimento: este campo corresponde às informações lançadas na coluna “Observação” dos Livros
Fiscais de Entradas, Saídas e de Apuração, de acordo com o estabelecido na legislação de cada unidade federada.
----
REGISTRO 0500: PLANO DE CONTAS CONTÁBEIS
Este registro tem o objetivo de identificar as contas contábeis utilizadas pelo contribuinte informante em sua
Contabilidade Geral, relativas às contas referenciadas no registro 0300. Não podem ser informados dois ou mais registros com
a mesma combinação de conteúdo nos campos DT_ALT e COD_CTA.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0500” C 004* - O
02 DT_ALT Data da inclusão/alteração N 008* - O
03 COD_ NAT_CC Código da natureza da conta/grupo de contas: C 002* - O
01 - Contas de ativo;
02 - Contas de passivo;
03 - Patrimônio líquido;
04 - Contas de resultado;
05 - Contas de compensação;
09 - Outras.
04 IND_CTA Indicador do tipo de conta: C 001* - O
S - Sintética (grupo de contas);
A - Analítica (conta).
05 NÍVEL Nível da conta analítica/grupo de contas. N 005 - O
06 COD_CTA Código da conta analítica/grupo de contas. C 60 - O
07 NOME_CTA Nome da conta analítica/grupo de contas. C 60 - O
Observações:
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Campo 01 (REG) - Valor Válido: [0500];
Campo 02 (DT_ALT) - Preenchimento: informar no padrão “diamêsano” (ddmmaaaa), excluindo-se quaisquer caracteres de
separação, tais como: ".", "/", "-".
Validação: a data não pode ser maior que a constante no campo DT_FIN.
Campo 03 (COD_ NAT_CC): Valores Válidos: [01, 02, 03, 04, 05, 09];
Campo 04 (IND_CTA): Valores Válidos: [S, A];
----
REGISTRO 0600: CENTRO DE CUSTOS
Este registro tem o objetivo de identificar os centros de custos referenciados no registro 0305 – Informação sobre
utilização do bem.
Validação do Registro: Não podem ser informados dois ou mais registros com a mesma combinação de conteúdo nos
campos DT_ALT e COD_CCUS.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo “0600”. C 004* - O
02 DT_ALT Data da inclusão/alteração. N 008* - O
03 COD_CCUS Código do centro de custos. C 060 - O
04 CCUS Nome do centro de custos. C 060 - O
Observações:
Nível hierárquico - 2
Ocorrência - vários (por arquivo)
Campo 01 (REG) - Valor Válido: [0600].
Campo 02 (DT_ALT) - Preenchimento: informar no padrão “ddmmaaaa”, excluindo-se quaisquer caracteres de separação,
tais como: ".", "/", "-".
Validação: a data não pode ser maior que a constante no campo DT_FIN.
Campo 03 (COD_CCUS) - Preenchimento: caso o contribuinte não adote centros de custos deverão ser informados os
seguintes códigos:
a) tratando-se de atividade econômica comercial ou de serviços:
Código “1”: área operacional;
Código “2”: área administrativa;
b) tratando-se de atividade econômica industrial:
Código “3”: área produtiva;
Código “4”: área de apoio à produção;
Código “5”: área administrativa.
----
REGISTRO 0990: ENCERRAMENTO DO BLOCO 0
Este registro tem por objetivo identificar o encerramento do bloco 0 e informar a quantidade de linhas (registros) existentes no bloco.
Nº Campo Descrição Tipo Tam Dec Obrig
01 REG Texto fixo contendo "0990" C 004 - O
02 QTD_LIN_0 Quantidade total de linhas do Bloco 0 N - - O
Observações:
Nível hierárquico - 1
Ocorrência – um por arquivo
Campo 01 (REG) - Valor Válido: [0990]
Campo 02 (QTD_LIN_0) - Preenchimento: a quantidade de linhas (registros) a ser informada deve considerar também os
próprios registros de abertura e encerramento do bloco. Para este cálculo, o registro 0000, mesmo não pertencendo ao bloco 0, deve ser somado.
Validação: o número de linhas (registros) existentes no bloco 0 é igual ao valor informado neste campo.
