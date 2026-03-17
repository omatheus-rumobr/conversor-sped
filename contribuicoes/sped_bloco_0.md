# BLOCO 0: Abertura, Identificação e Referências
## Registro 0000: Abertura do Arquivo Digital e Identificação da Pessoa Jurídica

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0000”. C 004* - S |
| 02 | COD_VER | Código | da | versão | do leiaute conforme a tabela N 003* - S |

3.1.1.
03 TIPO_ESCRIT Tipo de escrituração: N 001* - S

0 - Original;
1 – Retificadora.
04 IND_SIT_ESP Indicador de situação especial: N 001* - N

0 - Abertura
1 - Cisão
2 - Fusão
3 - Incorporação
4 – Encerramento
05 NUM_REC_ANTERI Número do Recibo da Escrituração anterior a C 041* - N

OR ser retificada, utilizado quando TIPO_ESCRIT
for igual a 1
06 DT_INI Data inicial das informações contidas no N 008* - S

arquivo.
07 DT_FIN Data final das informações contidas no N 008* - S

arquivo.
08 NOME Nome empresarial da pessoa jurídica C 100 - S
| 09 | CNPJ | Número | de | inscrição | do estabelecimento N 014* - S |

matriz da pessoa jurídica no CNPJ.
10 UF Sigla da Unidade da Federação da pessoa C 002* - S

jurídica.
11 COD_MUN Código do município do domicílio fiscal da N 007* - S

pessoa jurídica, conforme a tabela IBGE
12 SUFRAMA Inscrição da pessoa jurídica na Suframa C 009* - N
| 13 | IND_NAT_PJ | Indicador | da | natureza | da pessoa jurídica: N 002* - N |

00 – Pessoa jurídica em geral
01 – Sociedade cooperativa
02 – Entidade sujeita ao PIS/Pasep
exclusivamente com base na Folha de Salários
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|

Indicador da natureza da pessoa jurídica, a
partir do ano-calendário de 2014:
00 – Pessoa jurídica em geral (não participante
de SCP como sócia ostensiva)
01 – Sociedade cooperativa (não participante
de SCP como sócia ostensiva)
02 – Entidade sujeita ao PIS/Pasep
exclusivamente com base na Folha de Salários
03 - Pessoa jurídica em geral participante de
SCP como sócia ostensiva
04 – Sociedade cooperativa participante de
SCP como sócia ostensiva
05 – Sociedade em Conta de Participação -
SCP
14 IND_ATIV Indicador de tipo de atividade preponderante: N 001 - S

0 – Industrial ou equiparado a industrial;
1 – Prestador de serviços;
2 - Atividade de comércio;
3 – Pessoas jurídicas referidas nos §§ 6º, 8º e
9º do art. 3º da Lei nº 9.718, de 1998;
4 – Atividade imobiliária;
9 – Outros.
### Observações

Registro obrigatório, correspondente ao primeiro registro do arquivo da escrituração.
Nível hierárquico - 0
Ocorrência - um (por arquivo)
### Campo 01 - Valor Válido

[0000]
### Campo 02 - Preenchimento

o código da versão do leiaute informado é validado conforme a data referenciada no
campo
DT_FIN. Verificar na Tabela Versão, item 3.1.1 do Anexo Único do ADE Cofis nº 34, de 28 de outubro de 2010 e
alterações. Para a versão 1.01 do Programa Validador e Assinador (PVA) da EFD-Contribuições, deve ser informado
o código “002”
### Validação

Válido para período informado. A versão do leiaute informada no arquivo deverá ser válida na data final
da escrituração (campo DT_FIN do registro 0000).
### Campo 03 - Valores válidos

[0, 1]
### Preenchimento

Informar o tipo de escrituração – original ou retificadora. Para a entrega da EFD-Contribuições
deverá ser utilizado o leiaute vigente à época do período de apuração e, para validação e transmissão, a versão do
Programa de Validação e Assinatura - PVA atualizada.
### Campo 04 - Preenchimento

Este campo somente deve ser preenchido se a escrituração fiscal se referir à situação
especial decorrente de abertura, cisão, fusão, incorporação ou encerramento da pessoa jurídica.
OBSERVAÇÃO:
Com regra, a pessoa jurídica deve escriturar apenas uma escrituração em relação a cada período de apuração mensal.
Exceção a essa regra aplica-se apenas ao caso de cisão parcial, em que poderá haver mais de um arquivo no mesmo
mês, para o mesmo contribuinte.
Nos casos de eventos de incorporação, cada pessoa jurídica participante do evento de sucessão deve entregar a
escrituração, em relação ao período a que as obrigações e créditos são de sua responsabilidade de escrituração. Assim,
a título exemplificativo, em que a empresa A incorpora a empresa B, no dia 17.01.2012, teríamos:
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
- A EFD da empresa A (CNPJ da incorporadora), contemplando todo o período, de 01 a 31 de janeiro, registrando em
F800 eventuais créditos vertidos na sucessão;
- A EFD da empresa B (CNPJ da incorporada), contemplando apenas o período, de 01 a 17 de janeiro.
### Campo 05 - Preenchimento

Este campo somente deve ser preenchido quando a escrituração fiscal se referir a
retificação de escrituração já transmitida, original ou retificadora. Neste caso, deve a pessoa jurídica informar neste
campo o número do recibo da escrituração anterior, a ser retificada.
Atenção: O número do recibo a ser informado neste campo deve ser informado somente com letras maiúsculas.
### Campo 06 - Preenchimento

Informar a data inicial das informações referentes ao período da escrituração, no padrão
“diamêsano” (ddmmaaaa), excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
### Validação

Verificar se a data informada neste campo pertence ao mesmo mês/ano da data informada no campo
DT_FIN.
O valor informado deve ser o primeiro dia do mesmo mês de referencia da escrituração, exceto no caso de abertura,
conforme especificado no campo 04.
### Campo 07 - Preenchimento

Informar a data final das informações referentes ao período da escrituração, no padrão
“diamêsano” (ddmmaaaa), excluindo-se quaisquer caracteres de separação, tais como: “.”, “/”, “-”.
### Validação

Verificar se a data informada neste campo pertence ao mesmo mês/ano da data informada no campo
DT_INI.
O valor informado deve ser o último dia do mês a que se refere a escrituração, exceto nos casos de encerramento de
atividades, fusão, cisão e incorporação.
### Campo 08 - Preenchimento

Informar o nome empresarial da pessoa jurídica titular da escrituração, sem acentos.
### Validação

serão aceitos apenas os seguintes caracteres:
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ /,.-
@:&*+_<>()!?'$%1234567890
### Campo 09 - Preenchimento

Informar o número de inscrição do contribuinte no cadastro do CNPJ.
### Validação

será conferido o dígito verificador (DV) do CNPJ informado.
### Campo 10 - Preenchimento

Informar a sigla da unidade da federação (UF) do estabelecimento sede, responsável
pela escrituração fiscal digital do PIS/Pasep e da Cofins.
### Campo 11 – Preenchimento

Informar o código de município do domicílio fiscal da pessoa jurídica, conforme
codificação constante da Tabela de Municípios do IBGE.
### Validação

o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
### Campo 12 – Preenchimento

Informar neste campo a inscrição da pessoa jurídica titular da escrituração na
SUFRAMA. Caso a pessoa jurídica não tenha inscrição na SUFRAMA este campo deve ser informado em branco.
### Validação

será conferido o dígito verificador (DV) do número de inscrição na SUFRAMA, se informado.
### Campo 13 - Valores Válidos

[00, 01, 02, 03, 04, 05]
### Preenchimento

informar a natureza da pessoa jurídica, conforme um dos três tipos abaixo:
00 – Sociedade empresária em geral
01 – Sociedade cooperativa
02 – Entidade sujeita ao PIS/Pasep exclusivamente com base na Folha de Salários
### Campo 14 - Valores Válidos

[0, 1, 2, 3, 4, 9]
### Preenchimento

informar o indicador da atividade preponderante exercida pela pessoa jurídica no período da
escrituração, conforme um dos tipos abaixo:
0 – Industrial ou equiparado a industrial;
1 – Prestador de serviços;
2 - Atividade de comércio;
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
3 – Pessoas jurídicas referidas nos §§ 6º, 8º e 9º do art. 3º da Lei nº 9.718, de 1998;
4 – Atividade imobiliária;
9 – Outros
Caso a pessoa jurídica tenha exercido mais de uma das atividades acima relacionadas, no período da escrituração,
deve o campo ser preenchido com o código correspondente à atividade preponderante.
## Registro 0001: Abertura do Bloco 0

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0001”. C 004* - S |
| 02 | IND_MOV | Indicador | de | movimento: | N 001 - S |

0 - Bloco com dados informados;
1 – Bloco sem dados informados.
### Observações

Registro obrigatório. Deve ser gerado para abertura do Bloco 0 e indica se há informações previstas
para este bloco.
Nível hierárquico - 1
Ocorrência - um (por arquivo)
### Campo 01 - Valor Válido

[0001]
### Campo 02 - Valor Válido

[0,1]
Considerando que na escrituração do Bloco “0” deve ser escriturado, no mínimo, os registros “0110 - Regimes de
Apuração da Contribuição Social e de Apropriação de Crédito” e “0140 – Tabela de Cadastro de Estabelecimento”,
deve sempre ser informado, no Campo 02, o indicador “0 – Bloco com dados informados”.
## Registro 0035: Identificação de Sociedade em Conta de Participação – SCP

Conforme disposto no art. 4º da Instrução Normativa RFB nº 1.252/2012, em relação aos fatos geradores ocorridos
a partir de 1º de janeiro de 2014, no caso de a pessoa jurídica ser sócia ostensiva de Sociedades em Conta de
Participação (SCP), a EFD-Contribuições deverá ser transmitida separadamente, para cada SCP, além da transmissão
da EFD-Contribuições, da própria sócia ostensiva.
ATENÇÃO: ASSINATURA DIGITAL DAS EFD-CONTRIBUIÇÕES DE CADA SCP. A pessoa jurídica sócia
ostensiva deverá proceder à assinatura digital e transmissão, da EFD de cada SCP que atue como sócia ostensiva,
com o mesmo certificado digital utilizado para a assinatura digital e transmissão da EFD correspondente às operações
da própria pessoa jurídica. Ou seja, com o mesmo certificado, a pessoa jurídica irá transmitir todas as EFD-
Contribuições – a de suas próprias operações e as referentes à cada SCP.
Desta forma, a pessoa jurídica que participe de SCP como sócia ostensiva, fica obrigada a segregar e escriturar as
suas operações em separado, das operações referentes à(s) SCP(s).
Como exemplo, considerando que determinada pessoa jurídica participe de várias SCP, conforme abaixo:
1. SCP XXX – Sócia Ostensiva
2. SCP XYW – Sócia Participante
3. SCP WQA – Sócia Participante
4. SCP ABC – Sócia Ostensiva
5. SCP WEG – Sócia Ostensiva
Neste caso, a pessoa jurídica sócia ostensiva deverá proceder à escrituração de suas próprias operações, fazendo
constar na sua EFD-Contribuições, a escrituração de 03 (três) registros 0035, identificando em cada um desses
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
registros, cada SCP que atua como sócia ostensiva. No caso acima, ter-se-ia um registro 0035 para informar ao Fisco
a SCP “XXX”, outro para informar a SCP “ABC” e outro para informar a SCP “WEG”.
Além da obrigatoriedade de informar cada SCP que atue como sócia ostensiva, no registro 0035 de sua escrituração,
a PJ sócia ostensiva deverá gerar, validar e transmitir uma EFD-Contribuições para cada uma dessas SCP. Assim,
neste exemplo, a obrigatoriedade que recai sobre a pessoa jurídica é da geração e transmissão de 04 (quatro)
escriturações digitais – a da própria PJ e uma para cada SCP, relacionando as operações que lhe são próprias.
IMPORTANTE: A pessoa jurídica deverá informar nos blocos A, C, D, F, M e P da escrituração de cada SCP, os
documentos fiscais e operações correspondentes a cada SCP, mesmo que estes documentos fiscais tenham sido
emitidos em nome e com o CNPJ da PJ sócia ostensiva. Neste caso, não deve a PJ sócia ostensiva relacionar em sua
própria escrituração, os documentos e operações que sejam das SCP, uma vez que estes documentos e operações
devem ser relacionados é na escrituração digital de cada SCP.
## Registro 0035: Identificação de Sociedade em Conta de Participação – SCP

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0035”. C 004* - |
| 02 | COD_SCP | Identificação | da | SCP | N 014* - |
| 03 | DESC_SCP | Descrição | da | SCP | C - - |
| 04 | INF_COMP | Informação | Complementar | C | - - |

### Observações


Nível hierárquico - 2
Ocorrência - 1:N
Registro de preenchimento obrigatório, quando no campo 13 do Registro “0000” constar o indicador “03”, “04” ou
“05”.
No caso de constar no Campo 13 do Registro 0000 o indicador “03” ou “04”, podem ser gerados vários registros
“0035”, 01 (um) para cada SCP em que a pessoa jurídica titular da escrituração, participe na condição de sócio
ostensivo.
No caso de constar no Campo 13 do Registro 0000 o indicador “05”, será gerado apenas 01 (um) registro “0035”,
identificando a SCP a que se refere a escrituração em referência.
### Campo 01 - Valor Válido

[0035]
### Campo 02 – Preenchimento

Informar neste campo o código de identificação da SCP (em formato numérico) a que
se refere este registro. A codificação, de tamanho fixo de 14 dígitos, é de livre definição pela pessoa jurídica sócia
ostensiva, podendo inclusive ser utilizado o numero do CNPJ, caso a pessoa jurídica sócia ostensiva tenha inscrito a
SCP no CNPJ.
### Validação

serão aceitos apenas 14 dígitos [0-9], sem espaços em branco e caracteres especiais de formatação, tais
como: ".", "/", "-", etc.
### Campo 03 – Preenchimento

Informar neste campo a descrição da SCP, como o objeto do empreendimento para o
qual foi constituída, a atividade para a qual foi constituída (comércio, prestação de serviços específico, etc).
### Campo 04 – Preenchimento

Informar neste campo informações complementares da SCP.
## Registro 0100: Dados do Contabilista

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0100”. C 004* - S |
| 02 | NOME | Nome | do | contabilista. | C 100 - S |
| 03 | CPF | Número | de | inscrição | do contabilista no CPF. N 011* - S |
| 04 | CRC | Número | de | inscrição | do contabilista no Conselho Regional C 015 - S |

de Contabilidade.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
05 CNPJ Número de inscrição do escritório de contabilidade no N 014* - N

CNPJ, se houver.
06 CEP Código de Endereçamento Postal. N 008* - N
| 07 | END | Logradouro | e | endereço | do imóvel. C 060 - N |
| 08 | NUM | Número | do | imóvel. | C - - N |
| 09 | COMPL | Dados | complementares | do | endereço. C 060 - N |
| 10 | BAIRRO | Bairro | em | que | o imóvel está situado. C 060 - N |
| 11 | FONE | Número | do | telefone. | C 11 - N |
| 12 | FAX | Número | do | fax. | C 11 - N |
| 13 | EMAIL | Endereço | do | correio | eletrônico. C - - N |
| 14 | COD_MUN | Código | do | município, | conforme tabela IBGE. N 007* - N |

### Observações


Nível hierárquico – 2
Ocorrência - Vários (por arquivo)
1. Registro obrigatório, utilizado para identificação do contabilista responsável pela escrituração fiscal da empresa,
mesmo que o contabilista seja funcionário da empresa ou prestador de serviço.
2. Apesar das contribuições sociais serem apuradas de forma centralizada pelo estabelecimento matriz, as
informações dos Blocos A, C, D e F são escrituradas por estabelecimento. Neste sentido, caso a pessoa jurídica tenha
mais de um contabilista responsável pela escrituração fiscal de suas operações, estes devem ser relacionados no
registro 0100.
### Campo 01 - Valor Válido

[0100]
### Campo 02 - Preenchimento

informar o nome do contabilista responsável.
### Campo 03 - Preenchimento

informar o número do CPF do contabilista responsável pela escrituração, cujo numero
de inscrição no CRC foi informado no campo 04; não utilizar os caracteres especiais de formatação, tais como: ".",
"/", "-".
### Validação

será conferido o dígito verificador (DV) do CPF informado.
### Campo 04 - Preenchimento

informar o número de inscrição do contabilista no Conselho Regional de Contabilidade
na UF do estabelecimento sede.
### Campo 05 - Preenchimento

informar o número de inscrição no Cadastro Nacional de Pessoa Jurídica do escritório
de contabilidade; não informar caracteres de formatação, tais como: ".", "/", "-".
### Validação

será conferido o dígito verificador (DV) do CNPJ informado.
### Campo 06 - Preenchimento

informar o número do Código de Endereçamento Postal - CEP, conforme cadastro nos
CORREIOS.
### Campo 07 - Preenchimento

informar o endereço do contabilista/escritório de contabilidade.
### Campo 13 - Preenchimento

informar o endereço de correio eletrônico do contabilista/escritório de contabilidade.
### Campo 14 - Preenchimento

informar o código do município do domicílio fiscal do contabilista/escritório de
contabilidade.
### Validação

o valor informado no campo deve existir na Tabela de Municípios do IBGE (combinação do código da
UF e o código de município), possuindo 7 dígitos.
## Registro 0110: Regimes de Apuração da Contribuição Social e de Apropriação de Crédito

Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
Este registro tem por objetivo definir o regime de incidência a que se submete a pessoa jurídica (não-cumulativo,
cumulativo ou ambos os regimes) no período da escrituração. No caso de sujeição ao regime não-cumulativo, será
informado também o método de apropriação do crédito incidente sobre operações comuns a mais de um tipo de
receita adotado pela pessoa jurídica para o ano-calendário.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0110”. C 004 - S |

*
02 COD_INC_TRIB Código indicador da incidência tributária no N 001 - S

período: *
1 – Escrituração de operações com incidência
exclusivamente no regime não-cumulativo;
2 – Escrituração de operações com incidência
exclusivamente no regime cumulativo;
3 – Escrituração de operações com incidência nos
regimes não-cumulativo e cumulativo.
03 IND_APRO_CR Código indicador de método de apropriação de N 001 - N

ED créditos comuns, no caso de incidência no regime *
não-cumulativo (COD_INC_TRIB = 1 ou 3):
1 – Método de Apropriação Direta;
2 – Método de Rateio Proporcional (Receita Bruta)
04 COD_TIPO_CO Código indicador do Tipo de Contribuição Apurada N 001 - N

NT no Período *
1 – Apuração da Contribuição Exclusivamente a
Alíquota Básica
2 – Apuração da Contribuição a Alíquotas
Específicas (Diferenciadas e/ou por Unidade de
Medida de Produto)
05 IND_REG_CUM Código indicador do critério de escrituração e N 001 - N

apuração adotado, no caso de incidência *
exclusivamente no regime cumulativo
(COD_INC_TRIB = 2), pela pessoa jurídica
submetida ao regime de tributação com base no
lucro presumido:
1 – Regime de Caixa – Escrituração consolidada
(Registro F500);
2 – Regime de Competência - Escrituração
consolidada (Registro F550);
9 – Regime de Competência - Escrituração
detalhada, com base nos registros dos Blocos “A”,
“C”, “D” e “F”.
### Observações


1. Registro obrigatório. Informar somente os regimes de apuração a que se submeteu a pessoa jurídica no
período da escrituração.
2. O campo 05 (IND_REC_CUM) não deverá constar no arquivo da escrituração a ser importado pelo PVA,
versão 2.00, versão essa que acresce em relação à versão anterior (1.07), os registros da escrituração da
Contribuição Previdenciária sobre a Receita Bruta (Bloco P). O referido campo 05 só deverá constar no
arquivo da escrituração a ser importado pelo PVA na versão 2.01A, com previsão de disponibilização em
julho de 2012, que irá então constar com os registros da escrituração do PIS/Pasep e da Cofins, para a pessoa
jurídica tributada com base no lucro presumido.
Desta forma, no arquivo gerado para ser importado nas versões 1.07 e 2.00 do PVA, o registro “0110” deverá ser
informado com apenas 04 (quatro) campos.
Nível hierárquico - 2
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
Ocorrência – um (por arquivo)
### Campo 01 - Valor Válido

[0110]
### Campo 02 - Valores válidos

[1;2;3]
### Preenchimento

indicar o código correspondente ao(s) regime(s) de apuração das contribuições sociais a que se
submete a pessoa jurídica no período da escrituração:
- No caso de a pessoa sujeitar-se apenas à incidência não cumulativa, deve informar o indicador “1”;
- No caso de a pessoa sujeitar-se apenas à incidência cumulativa, deve informar o indicador “2”;
- No caso de a pessoa sujeitar-se aos dois regimes (não cumulativo e cumulativo), deve informar o indicador
“3”.
### Campo 03 - Valores válidos

[1;2]
### Preenchimento

Este campo deve ser informado no caso da pessoa jurídica apurar créditos referentes a operações (de
aquisições de bens e serviços, custos, despesas, etc) vinculados a mais de um tipo de receita (não-cumulativa e
cumulativa).
Este campo deve também ser preenchido no caso em que mesmo se sujeitando a pessoa jurídica exclusivamente ao
regime não-cumulativo, as operações geradoras de crédito sejam vinculadas a receitas de naturezas diversas,
decorrentes de:
- Operações tributadas no Mercado Interno;
- Operações não-tributadas no Mercado Interno (Alíquota zero, suspensão, isenção e não-incidência);
- Operações de Exportação.
No caso de a pessoa jurídica adotar o método da Apropriação Direta, para fins de determinação do crédito, referente
a aquisições, custos e despesas vinculados a mais de um tipo de receita, informar neste campo o indicador “1”;
No caso de a pessoa jurídica adotar o método do Rateio Proporcional com base na Receita Bruta, para fins de
determinação do crédito referente a aquisições, custos e despesas vinculados a mais de um tipo de receita, informar
neste campo o indicador “2”. Neste caso, a escrituração do Registro “0111” é obrigatória.
### Campo 04 - Valores válidos

[1;2]
### Preenchimento

indicar o código correspondente ao tipo de contribuição apurada no período, a saber:
- Indicador “1”: No caso de apuração das contribuições exclusivamente às alíquotas básicas de 0,65% ou 1,65%
(PIS/Pasep) e de 3% ou 7,6% (Cofins);
- Indicador “2”: No caso de apuração das contribuições às alíquotas específicas, decorrentes de operações tributadas
no regime monofásico (combustíveis; produtos farmacêuticos, de perfumaria e de toucador; veículos, autopeças e
pneus; bebidas frias e embalagens para bebidas; etc) e/ou em regimes especiais (pessoa jurídica industrial
estabelecida na Zona Franca de Manaus ou nas Áreas de Livre Comércio, por exemplo).
A pessoa jurídica sujeita à apuração das contribuições sociais a alíquotas específicas deve informar o indicador “2”
mesmo que, em relação a outras receitas, se submeta à alíquota básica.
### Campo 05 - Valores válidos

[1;2;9]
### Preenchimento

indicar o código correspondente ao critério de escrituração das receitas, para fins de apuração da
Contribuição para o PIS/Pasep e da Cofins, no caso de pessoa jurídica submetida ao regime de tributação com base
no lucro presumido:
- No caso de apuração das contribuições pelo regime de caixa, mediante a escrituração consolidada das receitas
recebidas no registro “F500”, deve informar o indicador “1”;
- No caso de apuração das contribuições pelo regime de competência, mediante a escrituração consolidada das
receitas auferidas no registro “F550”, deve informar o indicador “2”; ou
- No caso de apuração das contribuições pelo regime de competência, mediante a escrituração detalhada das
receitas auferidas nos registros dos Blocos “A”, “C”, “D” e “F”.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
## Registro 0111: Tabela de Receita Bruta Mensal Para Fins de Rateio de Créditos Comuns

Este registro é de preenchimento obrigatório, sempre que for informado no Registro “0110”, Campo 03
(IND_APRO_CRED), o indicador correspondente ao método do Rateio Proporcional com base na Receita Bruta
(indicador “2”), na apuração de créditos vinculados a mais de um tipo de receita.
Considerações sobre a Receita Bruta – Disposições da Lei nº 12.973/2014:
Conforme as disposições da Lei nº 12.973/2014, para fins de informação da receita bruta mensal, neste registro, deve
considerar as receitas tipificadas nos incisos I a IV do art. 12 do Decreto-Lei nº 1.598/77 (com os seus respectivos
valores decorrentes do ajuste a valor presente de que trata o inciso VIII do caput do art. 183 da Lei nº 6.404/76),
abaixo transcrito.
“Art. 12. A receita bruta compreende:
I - o produto da venda de bens nas operações de conta própria;
II - o preço da prestação de serviços em geral;
III - o resultado auferido nas operações de conta alheia; e
IV - as receitas da atividade ou objeto principal da pessoa jurídica não compreendidas nos incisos I a III.”
Em relação aos períodos de apuração anteriores ao da Lei nº 12.973, de 2014, a receita bruta para as pessoas jurídicas
submetidas ao regime não cumulativo da Contribuição para o PIS/Pasep (Lei nº 10.637/02, art. 1º, § 1º) e da Cofins
(Lei nº 10.833/03, art. 1º, § 1º), a Receita Bruta compreendia a receita da venda de bens e serviços nas operações em
conta própria ou alheia (comissões pela intermediação de negócios).
Em relação aos períodos de apuração anteriores ao da Lei nº 12.973, de 2014, a receita bruta para as pessoas jurídicas
submetidas ao regime cumulativo, considera-se como Receita Bruta, como definida pela legislação do imposto de
renda, a proveniente da venda de bens nas operações de conta própria, do preço dos serviços prestados e do resultado
auferido nas operações de conta alheia (Lei nº 9.715/98, art. 3º e Decreto-Lei nº 1.598/77, art. 12).
Assim, de acordo com a legislação tributária e os princípios contábeis básicos, as receitas diversas que não sejam
decorrentes da venda de bens e serviços nas operações em conta própria ou alheia, não se classificam como receita
bruta, não devendo desta forma ser consideradas para fins de rateio no registro “0111”.
A título exemplificativo, uma empresa que tenha por objeto social a fabricação de bens (industria) ou a revenda de
bens (comércio), não devem considerar como receita bruta, para fins de rateio, por não serem classificadas como tal,
entre outras:
- as receitas não operacionais, decorrentes da venda de ativo imobilizado;
- as receitas não próprias da atividade, de natureza financeira ou não, de aluguéis de bens móveis e
imóveis, etc.;
- de reversões de provisões e recuperações de créditos baixados como perda, que não representem
ingresso de novas receitas;
- do resultado positivo da avaliação de investimentos pelo valor do patrimônio líquido e os lucros e
dividendos derivados de investimentos avaliados pelo custo de aquisição, que tenham sido computados como
receita.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0111”. C 004* - S |
| 02 | REC_BRU_NCUM_TRIB | Receita | Bruta | Não-Cumulativa | - Tributada S |

N - 02
_MI no Mercado Interno
03 REC_BRU_ Receita Bruta Não-Cumulativa – Não S

N - 02
NCUM_NT_MI Tributada no Mercado Interno (Vendas com
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
suspensão, alíquota zero, isenção e sem
incidência das contribuições)
04 Receita Bruta Não-Cumulativa – S
REC_BRU_ NCUM_EXP N - 02
Exportação
05 REC_BRU_CUM Receita Bruta Cumulativa N - 02 S
| 06 | REC_BRU_TOTAL | Receita | Bruta | Total | N - 02 S |

### Observações


1. Em cada campo deve ser informada a receita bruta mensal consolidada da pessoa jurídica, correspondente ao
somatório das receitas auferidas pelos seus diversos estabelecimentos, no período mensal da escrituração.
2. Os valores informados de receita bruta, nos diversos campos do Registro “0111”, serão utilizados para fins de
rateio na validação ou determinação da base de cálculo de cada tipo de crédito escriturado nos Registros “M105”
(Detalhamento da Base de Cálculo do Crédito de PIS/PASEP) e “M505” (Detalhamento da Base de Cálculo do
Crédito de COFINS), em relação aos valores escriturados nos Blocos “A”, “C”, “D” e “F” representativos de
operações com direito a crédito vinculadas a mais de um tipo de receitas (CST 53, 54, 55, 56, 63, 64, 65 e 66).
Nível hierárquico - 3
Ocorrência – 1:1
### Campo 01 - Valor Válido

[0111]
### Campo 02 - Preenchimento

informar neste campo o valor total da receita bruta auferida no mercado interno pela
pessoa jurídica, vinculadas a receitas tributadas no regime não cumulativo:
- a alíquotas básicas de 1,65% (PIS/Pasep) e de 7,6% (Cofins);
- a alíquotas próprias do regime monofásico (diferenciadas e/ou por unidade medida de produto);
- a outras alíquotas específicas.
### Campo 03 - Preenchimento

informar neste campo o valor total da receita bruta auferida no mercado interno pela
pessoa jurídica, vinculadas a vendas efetuadas com suspensão, isenção, alíquota zero ou não-incidência das
contribuições sociais.
### Campo 04 - Preenchimento

informar neste campo o valor total da receita bruta auferida relativa a operações de:
- exportação de mercadorias para o exterior;
- prestação de serviços para pessoa física ou jurídica residente ou domiciliada no exterior, cujo pagamento
represente ingresso de divisas;
- vendas a empresa comercial exportadora com o fim específico de exportação.
### Campo 05 - Preenchimento

informar neste campo o valor total da receita bruta auferida pela pessoa jurídica,
vinculada a receitas tributadas no regime cumulativo a alíquotas de 0,65% (PIS/Pasep) e de 3% (Cofins).
### Campo 06 - Preenchimento

informar o total da receita bruta auferida no período, correspondente ao somatório dos
valores informados nos campos 02, 03, 04 e 05.
### Validação

A soma dos valores dos campos 02, 03, 04 e 05 deve ser igual ao valor informado neste campo.
## Registro 0120: Identificação de EFD-Contribuições Sem Dados a Escriturar

Novas definições para a escrituração deste registro:
1. Originalmente este registro tinha por exclusiva e única finalidade a pessoa jurídica informar, na EFD-
Contribuições de dezembro, os meses do ano calendário para os quais estava desobrigada de sua regular entrega, em
função de não terem sido realizadas operações geradoras de receitas ou de crédito.
Esta regra originária de escrituração permanece, já que é o procedimento normal e usual a ser adotado pelas PJ que
não entregam a EFD-Contribuições ao longo do ano, por estarem dispensadas, nos termos da IN RFB 1.252. Nesta
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
situação, o campo 03 (informações ou esclarecimentos complementares) é de preenchimento opcional, podendo o
campo ser preenchido com até 90 caracteres.
2. Para os fatos geradores ocorridos a partir de 01 de agosto de 2017, o Registro "0120 - Identificação de EFD-
Contribuições Sem Dados a Escriturar" é de preenchimento obrigatório, quando na escrituração não constar
registros referente a operações geradoras de receitas ou de créditos, ou seja, a escrituração estiver zerada, sem dados.
Se de fato a pessoa jurídica não realizou no período nenhuma operação representativa de receita auferida ou
recebida, nem realizou operação geradora de crédito, a EFD-Contribuições do período não precisa ser escriturada e
transmitida, nos termos da IN RFB nº 1.252/2012, que assim dispõe no art. 5º , §§ 7º e 8º em relação a esta situação:
"§ 7º A pessoa jurídica sujeita à tributação do Imposto sobre a Renda com base no Lucro Real
ou Presumido ficará dispensada da apresentação da EFD-Contribuições em relação aos
correspondentes meses do ano-calendário, em que:
I - não tenha auferido ou recebido receita bruta da venda de bens e serviços, ou de outra
natureza, sujeita ou não ao pagamento das contribuições, inclusive no caso de isenção, não incidência,
suspensão ou alíquota zero;
II - não tenha realizado ou praticado operações sujeitas a apuração de créditos da não
cumulatividade do PIS/Pasep e da Cofins, inclusive referentes a operações de importação.
§ 8º A dispensa de entrega da EFD-Contribuições a que se refere o § 7º, não alcança o mês de
dezembro do ano-calendário correspondente, devendo a pessoa jurídica, em relação a esse mês,
proceder à entrega regular da escrituração digital, na qual deverá indicar os meses do ano-calendário
em que não auferiu receitas e não realizou operações geradoras de crédito."
Como medida de simplificação e de racionalização de custos tanto para a própria pessoa jurídica como para
a Receita Federal, não se exige a escrituração e transmissão da EFD - Contribuições em relação aos períodos de
janeiro a novembro sem operações geradoras de receitas ou de créditos. Entretanto, caso a pessoa jurídica, por ato de
mera liberalidade e responsabilidade, resolva transmitir escrituração sem dados em seu conteúdo, deverá
obrigatoriamente incluir o Registro "0120- Identificação de EFD - Contribuições Sem Dados a Escriturar", no qual
deverá especificar o real motivo de gerar a escrituração sem dado algum a informar.
Para tanto, deve ser especificado no campo 03 do Registro 0120 em qual das situações a escrituração se
enquadra, para o período em referência, conforme os indicadores abaixo:
01 - Pessoa jurídica imune ou isenta do IRPJ
02 - Órgãos públicos, autarquias e fundações públicas
03 - Pessoa jurídica inativa
04 - Pessoa jurídica em geral, que não realizou operações geradoras de receitas (tributáveis ou não) ou de créditos
05 - Sociedade em Conta de Participação - SCP, que não realizou operações geradoras de receitas (tributáveis ou não)
ou de créditos
06 - Sociedade Cooperativa, que não realizou operações geradoras de receitas (tributáveis ou não) ou de créditos
07 - Escrituração decorrente de incorporação, fusão ou cisão, sem operações geradoras de receitas (tributáveis ou
não) ou de créditos
99 - Demais hipóteses de dispensa de escrituração, relacionadas no art. 5º, da IN RFB nº 1.252, de 2012
Regra de validação do Registro 0120, que deve ser observada:
1. Em relação aos períodos de apuração de janeiro a novembro, será gerado um único registro "0120", o qual
conterá exclusivamente a identificação do motivo da geração de escrituração sem dados (de receitas ou de créditos)
para o(s) correspondente(s) período(s), situação em que a IN RFB nº 1.252/2012 dispensa sua apresentação.
2. Em relação ao período de apuração de dezembro:
- No caso da pessoa jurídica ter procedido a transmissão de escrituração sem dados em relação aos meses anteriores
do ano calendário, conforme item 1 acima, será gerado um único registro "0120", o qual conterá exclusivamente a
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
identificação do motivo da geração de escrituração sem dados (de receitas ou de créditos) para o correspondente
período de dezembro; ou
- No caso da pessoa jurídica não ter procedido a transmissão de escrituração sem dados em relação aos meses
anteriores do ano calendário, conforme previsto na IN RFB nº 1.252/2012, deve ser gerado um registro "0120" para
cada mês que ficou dispensado da transmissão, em função de não ter realizado operações geradoras de receitas ou de
créditos.
Assim, conforme previsto na IN RFB nº 1.252/2012, caso a pessoa jurídica não tenha realizado operações em
algum(ns) mês(es) do ano-calendário, informará na EFD - Contribuições referente a dezembro do ano-calendário em
referencia, o(s) mês(es) em que não realizou as operações acima referidas no registro “0120”, ficando assim
dispensada da apresentação da EFD - Contribuições em relação a esses meses.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0120” C 004* - S |
| 02 | MES_REFER | Mês | de | referência | do ano-calendário da escrituração sem C 006* - S |

dados, dispensada da entrega.
Campo a ser preenchido no formato “mmaaaa”
03 INF_COMP Informação complementar do registro. No caso de

escrituração sem dados, deve ser informado o real motivo
dessa situação, conforme indicadores abaixo:
01 - Pessoa jurídica imune ou isenta do IRPJ
02 - Órgãos públicos, autarquias e fundações públicas
03 - Pessoa jurídica inativa
04 - Pessoa jurídica em geral, que não realizou operações geradoras
de receitas (tributáveis ou não) ou de créditos
C 090 - S
05 - Sociedade em Conta de Participação - SCP, que não realizou
operações geradoras de receitas (tributáveis ou não) ou de créditos
06 - Sociedade Cooperativa, que não realizou operações geradoras
de receitas (tributáveis ou não) ou de créditos
07 - Escrituração decorrente de incorporação, fusão ou cisão, sem
operações geradoras de receitas (tributáveis ou não) ou de créditos
99 - Demais hipóteses de dispensa de escrituração, relacionadas no
art. 5º, da IN RFB nº 1.252, de 2012
### Observações


1. Registro é específico para a pessoa jurídica informar o(s) mês (es) do ano-calendário em que está dispensada da
apresentação da EFD - Contribuições (obrigatório em dezembro), nos termos e situações de dispensa definidos pela
Receita Federal.
2. Na escrituração da EFD-Contribuições referente aos fatos geradores a partir de 01 de agosto de 2017, no caso da
pessoa jurídica proceder a escrituração sem dados representativos de operações geradoras de receitas ou de créditos,
também é obrigatória a escrituração deste registro, independente do mês a que se refere a escrituração.
Nível hierárquico - 2
Ocorrência - Vários
### Campo 01 - Valor Válido

[0120]
### Campo 02 - Preenchimento

Informar o mês e ano a que se refere a escrituração sem dados. Campo a ser preenchido
no formato “mmaaaa”.
### Campo 03 - Preenchimento

Campo de preenchimento obrigatório, no caso da escrituração não conter dados
representativos de operações geradoras de receitas (tributáveis ou não) ou de créditos.
Para os fatos geradores a partir de 01.08.2017, caso não conste na escrituração dados representativos de operações
geradoras de receitas, tributáveis ou não (toda receita deve ser escriturada), ou de créditos, nos Blocos "A", "C",
"D", "F" e/ou "I", ou não conste registros obrigatórios dos Bloco "M" ou "P", na validação da escrituração será gerada
mensagem de erro.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
A situação de erro só será regularizada com a escrituração do Registro "0120", no qual deve ser informado no Campo
"03" o real motivo da pessoa jurídica está gerando uma escrituração sem dados. Para tanto, deve ser informado o
indicador (composto de 2 caracteres) correspondente à real situação da pessoa jurídica no período da escrituração,
conforme abaixo:
01 - Pessoa jurídica imune ou isenta do IRPJ (Indicador "02" do Campo 13 do registro "0000")
02 - Órgãos públicos, autarquias e fundações públicas
03 - Pessoa jurídica inativa
04 - Pessoa jurídica em geral, que não realizou operações geradoras de receitas (tributáveis ou não) ou de créditos
05 - Sociedade em Conta de Participação - SCP, que não realizou operações geradoras de receitas (tributáveis ou não)
ou de créditos
06 - Sociedade Cooperativa, que não realizou operações geradoras de receitas (tributáveis ou não) ou de créditos
07 - Escrituração decorrente de incorporação, fusão ou cisão, sem operações geradoras de receitas (tributáveis ou
não) ou de créditos
99 - Demais hipóteses de dispensa de escrituração, relacionadas no art. 5º, da IN RFB nº 1.252, de 2012
## Registro 0140: Tabela de Cadastro de Estabelecimentos

Este registro tem por objetivo relacionar e informar os estabelecimentos da pessoa jurídica, no Brasil ou no exterior,
que auferiram receitas no período da escrituração, realizaram operações com direito a créditos ou que sofreram
retenções na fonte, no período da escrituração.
1. Em relação aos estabelecimentos e bases operacionais no exterior, que estejam cadastradas no CNPJ: Preencher o
registro "0140" informando o CNPJ (campo 04) do estabelecimento localizado no exterior e, em relação ao campo
"UF" (Campo 05) e ao campo "COD_MUN" (Campo 07), informar a UF e código de município do estabelecimento
sede, responsável pela escrituração, identificado no registro "0000";
2. Em relação aos estabelecimentos e bases operacionais no exterior, que não estejam cadastradas no CNPJ: Não
preencher o registro "0140", por inexistência de CNPJ (campo 04), devendo as operações objeto da escrituração deste
estabelecimento localizado no exterior, serem informadas nos Blocos "A", "C", "D" e/ou" F", no conjunto de registros
do estabelecimento sede, informado no registro "0000", campo "09".
Neste caso, e no sentido de diferenciar as informações próprias do estabelecimento sede, das informações próprias
dos estabelecimentos localizados no exterior, sem inscrição no CNPJ, preferencialmente deve a empresa adotar plano
de contas contábeis que diferenciem e identifiquem as operações de cada estabelecimento, as quais devem ser
informadas nos respectivos registros de operações nos Blocos "A", "C", "D" e "F".
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0140”. C 004* - S |
| 02 | COD_EST | Código | de | identificação | do estabelecimento C 060 - N |
| 03 | NOME | Nome | empresarial | do | estabelecimento C 100 - S |
| 04 | CNPJ | Número | de | inscrição | do estabelecimento no CNPJ. N 014* - S |
| 05 | UF | Sigla | da | unidade | da federação do estabelecimento. C 002* - S |
| 06 | IE | Inscrição | Estadual | do | estabelecimento, se contribuinte de C 014 - N |

ICMS.
07 COD_MUN Código do município do domicílio fiscal do N 007* - S

estabelecimento, conforme a tabela IBGE
08 IM Inscrição Municipal do estabelecimento, se contribuinte do C - - N

ISS.
09 SUFRAMA Inscrição do estabelecimento na Suframa C 009* - N

### Observações


1. Registro de preenchimento obrigatório para o estabelecimento matriz da pessoa jurídica.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
2. Em relação aos demais estabelecimentos da pessoa jurídica, este registro deve ser preenchido apenas para os que
tenham auferido receitas, sujeitas ou não à incidência de contribuição social, que tenha realizado operações geradoras
de créditos ou que tenha sofrido retenções na fonte no período.
3. Caso não tenha o estabelecimento incorrido em quaisquer das operações passíveis de registro nos Blocos A, C, D
ou F no período da escrituração, ou referentes a operações extemporâneas passíveis de registro no Bloco 1, não
precisa ser informado registro referente ao mesmo.
4. Deve ser escriturado um registro “0140” para cada estabelecimento que se enquadre nas condições de
obrigatoriedade acima referida.
Nível hierárquico - 2
Ocorrência – Vários (por arquivo)
### Campo 01 – Valor Válido

[0140]
### Campo 02 – Preenchimento

informe o identificador do estabelecimento sendo informados. Esta informação é de
livre atribuição da empresa.
### Campo 03 – Preenchimento

informe o nome empresarial do estabelecimento, caso este seja distinto do nome
empresarial da pessoa jurídica.
### Campo 04 - Preenchimento

Informar o número de inscrição do estabelecimento no cadastro do CNPJ.
### Validação

será conferido o dígito verificador (DV) do CNPJ informado.
### Campo 05 - Preenchimento

Informar a sigla da unidade da federação (UF) do estabelecimento.
### Campo 06 – Preenchimento

Informar neste campo a inscrição estadual do estabelecimento, caso existente.
### Validação

valida a Inscrição Estadual de acordo com a UF informada no campo COD_MUN (dois primeiros dígitos
do código de município). No caso do estabelecimento cadastrado possuir mais de uma inscrição estadual, este campo
não deve ser preenchido.
### Campo 07 – Preenchimento

Informar o código de município do domicílio fiscal da pessoa jurídica, conforme
codificação constante da Tabela de Municípios do IBGE.
### Validação

o valor informado no campo deve existir na Tabela de Municípios do IBGE, possuindo 7 dígitos.
### Campo 08 – Preenchimento

Informar neste campo a inscrição municipal do estabelecimento, caso existente.
### Campo 09 – Preenchimento

Informar neste campo a inscrição da pessoa jurídica titular da escrituração na
SUFRAMA. Caso a pessoa jurídica não tenha inscrição na SUFRAMA este campo deve ser informado em branco.
### Validação

será conferido o dígito verificador (DV) do número de inscrição na SUFRAMA, se informado.04 CNPJ
## Registro 0145: Regime de Apuração da Contribuição Previdenciária Sobre a Receita Bruta

Este registro servirá para identificar a obrigatoriedade de escrituração da Contribuição Previdenciária sobre Receitas,
no Bloco “P” para o período. O Registro “0145” tem natureza meramente informativa, não transferindo nem
recebendo valores de quaisquer outros registros da escrituração.
Deve escriturar o Registro “0145” a pessoa jurídica que tenha auferido receita das atividades de serviços ou da
fabricação de produtos, relacionados nos art. 7º e 8º da Lei nº 12.546/2011, respectivamente e se enquadrem como
contribuintes da CPRB por sujeição da lei ou por opção, conforme o período.
Atenção:
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
Compreende a receita bruta, para fins de informação nos campos 03, 04 e 05 deste registro, a receita decorrente da
venda de bens nas operações de conta própria, da prestação de serviços em geral, e o resultado auferido nas operações
de conta alheia, devendo ser considerada sem o ajuste de que trata o inciso VIII do art. 183 da Lei nº 6.404, de 1976.
No caso de não auferir quaisquer das receitas, nas hipóteses previstas em lei, não precisa ser informado o registro
“0145”, muito menos ser escriturado o Bloco P.
A soma dos valores informados no campo 04 (VL_REC_ATIV) e do campo 05 (VL_REC_DEMAIS_ATIV) pode
ser menor ou igual ao valor informado no campo 03 (VL_REC_TOT), não maior.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0145”. C 004* - S |
| 02 | COD_IN | Código | indicador | da | incidência tributária no período: N 001* - S |

C_TRIB 1 – Contribuição Previdenciária apurada no período,
exclusivamente com base na Receita Bruta;
2 – Contribuição Previdenciária apurada no período, com
base na Receita Bruta e com base nas Remunerações
pagas, na forma dos nos incisos I e III do art. 22 da Lei no
8.212, de 1991.
03 VL_REC Valor da Receita Bruta Total da Pessoa Jurídica no N - 02 S

_TOT Período
04 VL_REC Valor da Receita Bruta da(s) Atividade(s) Sujeita(s) à N - 02 S

_ATIV Contribuição Previdenciária sobre a Receita Bruta
05 VL_REC Valor da Receita Bruta da(s) Atividade(s) não Sujeita(s) à N - 02 N

_DEMAI Contribuição Previdenciária sobre a Receita Bruta
S_ATIV
06 INFO_C Informação complementar C - - N

OMPL
### Observações

A partir da versão 2.02, uma vez informado o registro filho “0145”, em relação ao registro pai “0140”
do estabelecimento matriz, fica dispensada a necessidade de escriturar o registro “0145” em relação aos demais
estabelecimento. Desta forma, ao cadastrar o registro “0145” do estabelecimento matriz, o PVA fica habilitado para
validar a escrituração do registro “P100” tanto do estabelecimento matriz como dos demais estabelecimentos da
empresa.
Nível hierárquico - 3
Ocorrência – 1:1
### Campo 01 – Valor Válido

[0145]
### Campo 02 – Preenchimento

informe o código indicador da incidência de tributação da contribuição previdenciária.
Valores Válidos: [1,2]
### Campo 03 – Preenchimento

informe o valor da receita bruta total da pessoa jurídica, no período da escrituração,
sujeitas ou não à incidência da Contribuição Previdenciária sobre a Receita.
Atenção: O valor informado neste campo corresponde à receita bruta consolidada da empresa e não, a receita bruta
de cada estabelecimento cadastrado em “0145”. Desta forma, constando na escrituração digital as informações de 10
(dez) estabelecimentos sujeitos à contribuição previdenciária sobre receitas, por exemplo, deve ser informado no
### campo 03 dos 10 (dez) registros “0145” (um para cada estabelecimento que auferiu receita sujeita à CP s/Receitas) o

mesmo valor, qual seja, o da receita bruta total da empresa.
### Campo 04 – Preenchimento

informe o valor da receita bruta da pessoa jurídica, no período da escrituração,
correspondente às atividades listadas nos art. 7º e 8º da Lei nº 12.546/2011, sujeitas à incidência da Contribuição
Previdenciária sobre a Receita.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
Atenção: Assim como no Campo 03, a receita bruta da(s) atividade/produto sujeita à CP sobre Receitas, a ser
informada neste campo, deve corresponder à receita bruta da atividade auferida por toda a pessoa jurídica e não,
especificamente a do estabelecimento cadastrado.
### Campo 05 – Preenchimento

informe o valor da receita bruta da pessoa jurídica, no período da escrituração,
correspondente às atividades não, sujeitas à incidência da Contribuição Previdenciária sobre a Receita.
Atenção: Assim como no Campo 03, a receita bruta da(s) atividade/produto não sujeita à CP sobre Receitas, a ser
informada neste campo, deve corresponder à receita bruta da atividade auferida por toda a pessoa jurídica e não,
especificamente a do estabelecimento cadastrado.
Atenção: Na escrituração das receitas, neste registro e nos registros do Bloco P, deve a pessoa jurídica considerar os
valores destacados a título de ajuste a valor presente (AVP), de que trata o inciso VIII do caput do art. 183 da Lei nº
6.404/76.
## Registro 0150: Tabela de Cadastro do Participante

Este registro tem por objetivo relacionar e cadastrar os participantes (fornecedores e clientes pessoa jurídica ou pessoa
física) que tenham realizado operações com a empresa, objeto de registro nos Blocos A, C, D, F ou 1.
Em relação às operações documentadas com base em Nota Fiscal Eletrônica (Código 55), no caso da pessoa jurídica
proceder à escrituração consolidada de suas vendas (Registro C180) e/ou de suas aquisições (Registro C190), não é
obrigatório cadastrar e relacionar no Registro 0150 o participante cujas operações estejam exclusivamente
escrituradas nos registros C180 e C190.
Em relação às operações documentadas com base em Nota Fiscal Eletrônica (Código 55), no caso da pessoa jurídica
proceder à escrituração de forma individualizada por documento fiscal (Registros C100/C170) de suas vendas e/ou
de suas aquisições, é obrigatório cadastrar e relacionar no Registro 0150 cada participante cujas operações estejam
escrituradas nos registros C100 e C170.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0150”. C 004* - S |
| 02 | COD_PAR | Código | de | identificação | do participante no arquivo. C 060 - S |

T
03 NOME Nome pessoal ou empresarial do participante. C 100 - S
| 04 | COD_PAIS | Código | do | país | do participante, conforme a tabela indicada N - S |

no item 3.2.1. 005
05 CNPJ CNPJ do participante. N 014* - N
| 06 | CPF | CPF | do | participante. | N 011* - N |
| 07 | IE | Inscrição | Estadual | do | participante. C 014 - N |
| 08 | COD_MU | Código | do | município, | conforme a tabela IBGE N 007* - N |

N
09 SUFRAMA Número de inscrição do participante na Suframa C 009* - N
| 10 | END | Logradouro | e | endereço | do imóvel C 060 - N |
| 11 | NUM | Número | do | imóvel | C - - N |
| 12 | COMPL | Dados | complementares | do | endereço C 060 - N |
| 13 | BAIRRO | Bairro | em | que | o imóvel está situado C 060 - N |

### Observações


1. Registro utilizado para informações cadastrais das pessoas físicas ou jurídicas envolvidas nas transações
comerciais e de prestação/contratação de serviços relacionadas na escrituração fiscal digital, no período.
2. Todos os participantes informados nos registros dos Blocos A, C, D ou F devem ser relacionados neste Registro
0150, bem como os participantes relacionados em operações extemporâneas de contribuições e/ou créditos (na
impossibilidade de retificação da EFD-Contribuições), no Bloco 1.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
A obrigatoriedade de escrituração de participante no Registro 0150 não se aplica, nas situações em que os registros
dos Blocos A, C, D ou F identifiquem o participante pelo CNPJ (no caso de participante pessoa jurídica) ou CPF (no
caso de participante pessoa física)..
3. No caso de registros representativos de operações de vendas a consumidor final (mediante emissão de Nota Fiscal
de Vendas a Consumidor Final, ou documento equivalente, inclusive os emitidos por ECF), não precisam ser
informados os campos CNPJ e CPF;
4. O Campo CPF não precisa ser informado, nas operações representativas de vendas de bens e serviços a pessoas
físicas estrangeiras.
5. No caso da pessoa jurídica ter realizado operações relativas às atividades de consórcio, constituído nos termos do
disposto nos arts. 278 e 279 da Lei nº 6.404, de 1976, passíveis de escrituração na EFD-Contribuições, deverá a
pessoa jurídica consorciada cadastrar cada consórcio em 01 (um) registro 0150 específico.
Nível hierárquico - 3
Ocorrência – 1:N
### Campo 01 - Valor Válido

[0150]
### Campo 02 - Preenchimento

informar o código de identificação do participante no arquivo.
Esta tabela pode conter COD_PART e respectivo registro 0150 com dados do próprio contribuinte informante, quando
apresentar documentos emitidos contra si próprio, em situações específicas.
### Validação

O código de participante, campo COD_PART, é de livre atribuição do estabelecimento, observado o
disposto no item 2.4.2.1. do Manual de Orientação do Leiaute da EFD-Contribuições (ADE Cofis nº 34/2010).
### Campo 04 - Preenchimento

informar o código do país, conforme tabela indicada no item 3.2.1 do Manual de
Orientação do Leiaute da EFD-Contribuições (ADE Cofis nº 34/2010). O código de país pode ser informado com 05
caracteres ou com 04 caracteres (desprezando o caractere “0” (zero) existente à esquerda).
### Validação

o valor informado no campo deve existir na Tabela de Países. Informar, inclusive, quando o participante
for estabelecido ou residente no Brasil (01058 ou 1058).
### Campo 05 - Preenchimento

informar o número do CNPJ do participante; não informar caracteres de formatação,
tais como: ".", "/", "-". Se COD_PAIS diferente de Brasil, o campo não deve ser preenchido. Obrigatoriamente um
dos campos, CPF ou CNPJ, deverá ser preenchido.
### Validação

é conferido o dígito verificador (DV) do CNPJ informado.
### Campo 06 - Preenchimento

informar o número do CPF do participante; não utilizar os caracteres especiais de
formatação, tais como: “.”, “/”, “-”. Se COD_PAIS diferente de Brasil, o campo não deve ser preenchido.
### Validação

é conferido o dígito verificador (DV) do CPF informado.
Obrigatoriamente um dos campos, CPF ou CNPJ, deverá ser preenchido.
Obs.: Os campos 05 e 06 são mutuamente excludentes, sendo obrigatório o preenchimento de um deles quando o
### campo 04 estiver preenchido com “01058” ou “1058” (Brasil).

### Campo 07 - Validação

valida a Inscrição Estadual de acordo com a UF informada no campo COD_MUN (dois
primeiros dígitos do código de município).
### Campo 08 - Validação

o valor informado no campo deve existir na Tabela de Municípios do IBGE (combinação do
código da UF e do código de município), possuindo 7 dígitos.
Obrigatório se campo COD_PAIS for igual a “01058” ou “1058”(Brasil). Se for exterior, informar campo “vazio” ou
preencher com o código “9999999”.
### Campo 09 - Preenchimento

informar o número de Inscrição do participante na SUFRAMA, se houver.
### Validação

é conferido o dígito verificador (DV) do número de inscrição na SUFRAMA, se informado.
### Campo 10 - Preenchimento

informar o logradouro e endereço do imóvel. Se o participante for do exterior,
preencher inclusive com a cidade e país.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
## Registro 0190: Identificação das Unidades de Medida

| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0190" C 004 - S |

*
02 UNID Código da unidade de medida C 006 - S
| 03 | DESCR | Descrição | da | unidade | de medida C - - S |

### Observações


Nível hierárquico - 3
Ocorrência – 1:N
### Campo 01 - Valor Válido

[0190]
### Campo 02

Informar o código correspondente à unidade de medida utilizada no arquivo digital.
### Campo 03 - Validação

não poderão ser informados os campos UNID e DESCR com o mesmo conteúdo.
## Registro 0200: Tabela de Identificação do Item (Produtos e Serviços)

Este registro tem por objetivo informar as mercadorias, serviços, produtos ou quaisquer outros itens concernentes às
transações representativas de receitas e/ou geradoras de créditos, objeto de escrituração nos Blocos A, C, D, F ou 1.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0200" C 004 - S |
| 02 | COD_ITEM | Código | do | item | C 060 - S |
| 03 | DESCR_ITEM | Descrição | do | item | C - - S |
| 04 | COD_BARRA | Representação | alfanumérico | do | código de barra do C - - N |

produto, se houver.
05 COD_ANT_ITE Código anterior do item com relação à última informação C 060 - N

M apresentada.
06 UNID_INV Unidade de medida utilizada na quantificação de C 006 - N

estoques.
07 TIPO_ITEM Tipo do item – Atividades Industriais, Comerciais e N 002* - S

Serviços:
00 – Mercadoria para Revenda;
01 – Matéria-Prima;
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
08 COD_NCM Código da Nomenclatura Comum do Mercosul C 008 - N
| 09 | EX_IPI | Código | EX, | conforme | a TIPI C 003 - N |
| 10 | COD_GEN | Código | do | gênero | do item, conforme a Tabela 4.2.1. N 002* - N |
| 11 | COD_LST | Código | do | serviço | conforme lista do Anexo I da Lei N 004 N |

Complementar Federal nº 116/03.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|

Obs: A partir do período de apuração maio de 2015 005
(versão 2.11 do PVA), o código a ser informado neste
campo poderá ser informado 05 (cinco) caracteres, no
formato “XX.XX”, conforme a codificação adotada na
Lei Complementar nº 116/2003 e na EFD-ICMS/IPI.
12 ALIQ_ICMS Alíquota de ICMS aplicável ao item nas operações N 006 02 N

internas
### Observações


Nível hierárquico - 3
Ocorrência – 1:N
### Campo 01 - Valor Válido

[0200]
### Campo 02 - Preenchimento

informar com códigos próprios do informante do arquivo os itens das operações de
entradas de mercadorias ou aquisições de serviços, bem como das operações de saídas de mercadorias ou prestações
de serviços. O Código do Item deverá ser preenchido com as informações utilizadas na última ocorrência do período.
A identificação do item (produto ou serviço) deverá receber o código próprio do informante do arquivo em qualquer
documento, lançamento efetuado ou arquivo informado (significa que o código de produto deve ser o mesmo na
emissão dos documentos fiscais, na entrada das mercadorias ou em qualquer outra informação prestada ao Fisco.
### Campo 03 - Preenchimento

são vedadas descrições diferentes para o mesmo item ou descrições genéricas,
ressalvadas as operações abaixo, desde que não destinada à posterior circulação ou apropriação na produção:
1- de aquisição de "materiais para uso/consumo" que não gerem direitos a créditos;
2- que discriminem por gênero a aquisição ou venda de bens incorporados ao ativo imobilizado da empresa;
3- que contenham os registros consolidados relativos aos contribuintes com atividades econômicas de
fornecimento de energia elétrica, de fornecimento de água canalizada, de fornecimento de gás canalizado e de
prestação de serviço de comunicação e telecomunicação que poderão, a critério do Fisco, utilizar registros
consolidados por classe de consumo para representar suas saídas ou prestações.
### Campo 06 - Validação

existindo informação neste campo, esta deve existir no registro 0190, campo UNID,
respectivo.
### Campo 07 - Preenchimento

informar o tipo do item aplicável. Nas situações de um mesmo código de item possuir
mais de um tipo de item (destinação), deve ser informado o tipo de maior relevância.
Deve ser informada a destinação inicial do produto, considerando-se os conceitos:
00 - Mercadoria para revenda – produto adquirido comercialização;
01 – Matéria-prima: a mercadoria que componha, física e/ou quimicamente, um produto em processo ou produto
acabado e que não seja oriunda do processo produtivo. A mercadoria recebida para industrialização é classificada
como Tipo 01, pois não decorre do processo produtivo, mesmo que no processo de produção se produza mercadoria
similar classificada como Tipo 03;
03 – Produto em processo: o produto que possua as seguintes características, cumulativamente: oriundo do processo
produtivo; e, preponderantemente, consumido no processo produtivo. Dentre os produtos em processo está incluído
o produto resultante caracterizado como retorno de produção (vide conceito de retorno de produção abaixo);
04 – Produto acabado: o produto que possua as seguintes características, cumulativamente: oriundo do processo
produtivo; produto final resultante do objeto da atividade econômica do contribuinte; e pronto para ser
comercializado;
05 - Subproduto: o produto que possua as seguintes características, cumulativamente: oriundo do processo produtivo
e não é objeto da produção principal do estabelecimento; tem aproveitamento econômico; não se enquadre no
conceito de produto em processo (Tipo 03) ou de produto acabado (Tipo 04);
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
06 – Produto intermediário: aquele que, embora não se integrando ao novo produto, for consumido no processo de
industrialização.
Valores válidos: [00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 99]
### Campo 08 – Preenchimento

É obrigatório informar o Código NCM conforme a Nomenclatura Comum do
MERCOSUL, de acordo com o Decreto nº 6.006/06 para:
- as empresas industriais e equiparadas a industrial, referente aos itens correspondentes às suas atividades fins;
- as pessoas jurídicas, inclusive cooperativas, que produzam mercadorias de origem animal ou vegetal
(agroindústria), referente aos itens correspondentes às atividades geradoras de crédito presumido;
- as empresas que realizarem operações de exportação ou importação;
- as empresas atacadistas ou industriais, referentes aos itens representativos de vendas no mercado interno com
alíquota zero, suspensão, isenção ou não incidência, nas situações em que a legislação tributária atribua o
benefício a um código NCM específico.
Nas demais situações o Campo 08 (NCM) não é de preenchimento obrigatório.
### Campo 09 - Preenchimento

informar com o Código de Exceção de NCM, de acordo com a Tabela de Incidência
do Imposto sobre Produtos Industrializados (TIPI), quando existir.
### Campo 10 - Preenchimento

obrigatório para todos os contribuintes na aquisição de produtos primários. A Tabela
"Gênero do Item de Mercadoria/Serviço", referenciada no Item 4.2.1 do Manual de Orientação do Leiaute da EFD-
Contribuições (ADE Cofis nº 34/2010), corresponde à tabela de "Capítulos da NCM", acrescida do código "00 -
Serviço".
### Validação

o valor informado no campo deve existir na Tabela “Gênero do Item de Mercadoria/Serviço”, item 4.2.1
do Manual de Orientação do Leiaute da EFD-Contribuições (ADE Cofis nº 34/2010).
### Campo 11 - Preenchimento

informar o código de serviços, de acordo com a Lei Complementar 116/03.
Atenção: A partir da versão 2.11 do PVA, o código a ser informado neste campo poderá ser informado também com
5 (cinco) caracteres, no formato “XX.XX”, assim como também está sendo informado na EFD-ICMS/IPI.
### Campo 12 - Preenchimento

neste campo deve ser informada a alíquota do ICMS, em operações de saída interna.
Não deve ser preenchido este campo no caso de produtos cadastrados por gênero (bens do ativo imobilizado, por
exemplo), ou no caso de produto cadastrado de forma centralizada pelo estabelecimento matriz e que sujeita-se a
alíquotas diversas de acordo com o Fisco de jurisdição de seus estabelecimentos.
## Registro 0205: Alteração do Item

Este registro tem por objetivo informar alterações ocorridas na descrição do produto, desde que não o descaracterize
ou haja modificação que o identifique como sendo novo produto, caso não tenha ocorrido movimentação no período
da alteração do item, deverá ser informada no primeiro período em que houver movimentação do item.
Deverá ser ainda informado quando ocorrer alteração na codificação do produto.
Não podem ser informados dois ou mais registros com sobreposição de períodos.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0205" C 004* - S |
| 02 | DESCR_ANT_ITE | Descrição | anterior | do | item C - - N |

M
03 DT_INI Data inicial de utilização da descrição do item N 008* - S
| 04 | DT_FIM | Data | final | de | utilização da descrição do item N 008* - S |
| 05 | COD_ANT_ITEM | Código | anterior | do | item com relação à última C 060 - N |

informação apresentada.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
### Observações


Nível hierárquico - 4
Ocorrência – 1:N
### Campo 01 - Valor Válido

[0205]
### Campo 02 – Preenchimento

preencher a descrição anterior do item, a qual foi substituída pela informação constante
no registro pai 0200.
### Campo 03 - Preenchimento

informar a data inicial de utilização da descrição anterior do item.
### Validação

o valor informado no campo deve ser uma data válida no formato “ddmmaaaa”.
### Campo 04 - Preenchimento

informar o período final de utilização da descrição anterior do item.
### Validação

o valor informado no campo deve ser uma data válida obedecido o formato “ddmmaaaa”. O valor
informado no campo deve ser menor que o valor no campo DT_FIN do registro 0000.
## Registro 0206: Código de Produto Conforme Tabela ANP (Combustíveis)

Este registro tem por objetivo informar o código correspondente ao produto constante na Tabela da Agência Nacional
de Petróleo (ANP) para os produtos denominados “Combustíveis”.
Deve ser apresentado apenas pelos contribuintes produtores, importadores e distribuidores de combustíveis.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0206" C 004 - S |
| 02 | COD_COMB | Código | do | combustível, | conforme tabela publicada pela C - - S |

ANP
### Observações


Nível hierárquico - 4
Ocorrência – 1:1
### Campo 01 - Valor Válido

[0206]
### Campo 02 - Preenchimento

utilizar o código do combustível, conforme Tabela de Produtos para Combustíveis /
Solvente (Tabela 12 de códigos de produtos para o Sistema de Informações de Movimentação de Produtos (SIMP)),
conforme disponibilizado no endereço “http://www.anp.gov.br/simp/index/htm”.
### Validação

o valor informado no campo deve existir na tabela da ANP.
O código do combustível deve está vinculado ao código do item (Campo 07 do Registro 0200) e é obrigatório quando
o produto se referir a combustíveis e o informante do arquivo for produtor, importador ou distribuidor de combustível.
## Registro 0208: Código de Grupos por Marca Comercial – Refri (bebidas frias)

Este registro deve ser preenchido pela pessoa jurídica industrial ou importadora de bebidas frias (cerveja,
refrigerantes, águas, preparações compostas não alcoólicas, etc), optante do Regime Especial de Apuração da
Contribuição para o PIS/Pasep e da Cofins por litro de produto, conforme as alíquotas específicas por produto e
marcas comerciais estabelecidas pelo Poder Executivo, nos termos da Lei nº 10.833, de 2003.
Atenção: Em função do novo regime de apuração aplicável para os fatos geradores a partir de maio de 2015,
conforme definido pela Lei nº 13.097, de 2015, o Regime Especial de Apuração da Contribuição para o PIS/Pasep e
da Cofins por litro de produto, conforme as alíquotas específicas por produto e marcas comerciais estabelecidas pelo
Poder Executivo, nos termos da Lei nº 10.833, de 2003, objeto de codificação neste registro, só será aplicável para
os fatos geradores até 31 de abril de 2015.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0208" C 004 - S |

*
02 COD_TAB Código indicador da Tabela de Incidência, conforme C 002 - S

Anexo III do Decreto nº 6.707/08:
01 – Tabela I
02 – Tabela II
03 – Tabela III
04 – Tabela IV
05 – Tabela V
06 – Tabela VI
07 – Tabela VII
08– Tabela VIII
09 – Tabela IX
10 – Tabela X
11 – Tabela XI
12 – Tabela XII
A partir de outubro de 2012:
13 – Tabela XIII
03 COD_GRU Código do grupo, conforme Anexo III do Decreto nº C 002 - S

6.707/08.
04 MARCA_COM Marca Comercial C 060 - S

### Observações


1. O Regime Especial de apuração da Contribuição para o PIS/Pasep e da Cofins, por marca comercial, objeto de
informação neste registro, está regulamentado pelo Decreto nº 6.707, de 2008, alterado pelos Decreto nº 6.904, de
2009 e nº 7.455, de 2011.
2. A codificação da bebida fria neste registro é obrigatória para os importadores e pessoas jurídicas que procedam à
industrialização dos produtos listados no art. 1o do Decreto nº 6.707, de 2008, sujeitos ao regime geral ou ao regime
especial previstos no referido Decreto, e deve está vinculado ao código do item (Campo 07 do Registro 0200), para
os fatos geradores até 30 de abril de 2015.
3. Para os períodos de apuração a partir de maio de 2015, o regime de tributação a que se refere este registro
(tributação com alíquota definida de acordo com a marca comercial da bebida) não mais é aplicável, em função do
novo regime de tributação previsto na Lei nº 13.097, 2015. Neste sentido, o registro 0208 não precisa mais ser
escriturado, para os fatos geradores a partir de maio de 2015.
Nível hierárquico - 4
Ocorrência - 1:1
### Campo 01 - Valor Válido

[0208]
### Campo 02 - Preenchimento

informar o código correspondente à Tabela de Referência em que se enquadra a bebida,
sujeita ao regime especial de tributação (REFRI).
Valores válidos: [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11 e 12]
### Campo 03 - Preenchimento

informar o código do grupo correspondente à marca comercial da bebida, conforme
relação constante no Anexo III do Decreto nº 6.707, de 2008, alterado pelos Decreto nº 6.904, de 2009 e nº 7.455, de
2011.
No caso de produtos relacionados nas Tabelas I e II do Anexo III do Decreto nº 6.707/08, informar neste Campo 03
o código de Grupo “SN”.
### Campo 04 - Preenchimento

informar a marca comercial da bebida, conforme relação constante nas tabelas do
Anexo III do Decreto nº 6.707, de 2008, alterado pelos Decreto nº 6.904, de 2009 e nº 7.455, de 2011.
Na hipótese em que determinada marca comercial não estiver expressamente listada no Anexo III, será adotado o
menor valor dentre os listados para o tipo de produto a que se referir.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
## Registro 0400: Tabela de Natureza da Operação/Prestação

Este registro tem por objetivo codificar os textos das diferentes naturezas da operação/prestação discriminadas nos
documentos fiscais. Esta codificação e suas descrições são livremente criadas e mantidas pelo contribuinte.
Este registro não se refere a CFOP. Algumas empresas utilizam outra classificação além das apresentados nos CFOP.
Esta codificação permite informar estes agrupamentos próprios.
Não podem ser informados dois ou mais registros com o mesmo código no campo COD_NAT
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0400" C 004 - S |
| 02 | COD_NAT | Código | da | natureza | da operação/prestação C 010 - S |
| 03 | DESCR_NAT | Descrição | da | natureza | da operação/prestação C - - S |

### Observações


Nível hierárquico - 3
Ocorrência – 1:N
### Campo 01 - Valor Válido

[0400]
### Campo 02 – Preenchimento

informar o código da natureza da operação/prestação
### Campo 03 – Preenchimento

informar a descrição da natureza da operação/prestação
## Registro 0450: Tabela de Informação Complementar do Documento Fiscal

Este registro tem por objetivo codificar todas as informações complementares dos documentos fiscais, exigidas pela
legislação fiscal. Estas informações constam no campo “Dados Adicionais” dos documentos fiscais.
Esta codificação e suas descrições são livremente criadas e mantidas pelo contribuinte e não podem ser informados
dois ou mais registros com o mesmo conteúdo no campo COD_INF.
Deverão constar todas as informações complementares de interesse da Administração Tributária, existentes nos
documentos fiscais.
Exemplo: nos casos de documentos fiscais de entradas, informar as referências a um outro documento fiscal.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | "0450" C 004* - S |
| 02 | COD_INF | Código | da | informação | complementar do documento fiscal. C 006 - S |
| 03 | TXT | Texto | livre | da | informação complementar existente no C - - S |

documento fiscal, inclusive espécie de normas legais, poder
normativo, número, capitulação, data e demais referências
pertinentes com indicação referentes ao tributo.
### Observações


Nível hierárquico - 3
Ocorrência – 1:N
### Campo 01 - Valor Válido

[0450]
### Campo 02 – Preenchimento

informar o código da informação complementar, conforme for utilizado nos
documentos fiscais constantes nos demais blocos
### Campo 03 – Preenchimento

preencher com o texto constante no documento fiscal, como por Exemplo: o número
e data do ADE que permite a realização de venda com suspensão para empresa preponderantemente exportadora e a
respectiva indicação da base legal
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
## Registro 0500: Plano de Contas Contábeis

Este registro tem o objetivo de identificar as contas contábeis utilizadas pelo contribuinte em sua Escrituração
Contábil, relacionadas às operações representativas de receitas, tributadas ou não, e dos créditos apurados.
Não podem ser informados dois ou mais registros com a mesma combinação de conteúdo nos campos DT_ALT,
COD_CTA e COD_CTA_REF.
Para as pessoas jurídicas que apuram a Contribuição para o PIS/Pasep e a Cofins no regime não cumulativo (PJ que
apuram o IR com base no Lucro Real), o código da conta contábil deve ser informado, nos correspondentes campos
dos registros de saídas/receitas e/ou de aquisições/custos/despesas, bem como nos registros dos Blocos “M” e “1”
que contenham o campo de código de conta contábil. A não informação da conta contábil correspondente às
operações, nos registros representativos de saídas/receitas e/ou de aquisições/custos/despesas acarretará:
- Para os fatos geradores até 31 de outubro de 2017, ocorrência de aviso/advertência (não impedindo a validação
do registro);
- Para os fatos geradores a partir de 01 de novembro de 2017, ocorrência de erro (impedindo a validação do
registro).
A regra acima também se aplica às pessoas jurídicas que apuram a Contribuição para o PIS/Pasep e a Cofins no
regime cumulativo pelo regime de competência.
Informação de preenchimento – PJ tributadas com base no lucro presumido:
Considerando que o atual programa da EFD-Contribuições (versão 2.1.4) estabelece a obrigatoriedade de se informar
nos registros da escrituração, das operações geradoras de receitas e/ou de créditos, a conta contábil (Campo
COD_CTA), a partir do período de apuração de novembro de 2017;
Considerando que Instrução Normativa RFB nº 1.774, de 22.12.2017, dispensou da obrigatoriedade da escrituração
contábil digital (ECD) as pessoas jurídicas tributadas com base no lucro presumido que não distribuíram, a título de
lucro, sem incidência do Imposto sobre a Renda Retido na Fonte (IRRF), parcela de lucros ou dividendos, superior
ao valor da base de cálculo do Imposto sobre a Renda diminuída dos impostos e contribuições a que estiver sujeita;
As pessoas jurídicas tributadas com base no lucro presumido não sujeitas à obrigatoriedade da ECD, nos termos da
IN RFB nº 1.774/2017, poderão, opcionalmente, informar nos campos "COD_CTA" dos registros da EFD-
Contribuições, para os fatos geradores a partir de novembro/2017, inclusive, com a informação "Dispensa de ECD
- IN RFB nº 1.774/2017".
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0500” C 004* - S |
| 02 | DT_ALT | Data | da | inclusão/alteração | N 008* - S |
| 03 | COD_ | Código | da | natureza | da conta/grupo de contas: C 002* - S |

NAT_CC 01 - Contas de ativo
02 - Contas de passivo;
03 - Patrimônio líquido;
04 - Contas de resultado;
05 - Contas de compensação;
09 - Outras.
04 IND_CTA Indicador do tipo de conta: C 001* - S

S - Sintética (grupo de contas);
A - Analítica (conta).
05 NÍVEL Nível da conta analítica/grupo de contas. N 005 - S
06 COD_CTA Código da conta analítica/grupo de contas. C 255 - S
| 07 | NOME_CTA | Nome | da | conta | analítica/grupo de contas. C 060 - S |
| 08 | COD_CTA_R | Código | da | conta | correlacionada no Plano de Contas C 060 - N |

EF Referenciado, publicado pela RFB.
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
09 CNPJ_EST CNPJ do estabelecimento, no caso da conta informada N 014* - N

no campo COD_CTA ser específica de um
estabelecimento.
### Observações


1. Devem ser informadas no registro “0500” apenas as contas que sejam relacionadas em registros escriturados nos
blocos A, C, D, F, I, M e P, que contenham o Campo "COD_CTA".
2. Para os fatos geradores a partir de 01 de novembro de 2017, a informação dos campos referentes às contas contábeis
(COD_CTA) passa a ser obrigatória, nos correspondentes campos dos registros de receitas e/ou de créditos:
a) para as pessoas jurídicas que apuram a Contribuição para o PIS/Pasep e a Cofins no regime não cumulativo (PJ
que apuram o IR com base no Lucro Real); e
b) para as pessoas jurídicas que apuram a Contribuição para o PIS/Pasep e a Cofins no regime cumulativo, com
base no regime de competência (PJ que apuram o IR com base no Lucro Presumido/Arbitrado).
Nível hierárquico - 2
Ocorrência - Vários (por arquivo)
### Campo 01 - Valor Válido

[0500];
### Campo 02 - Preenchimento

informar no padrão “diamêsano” (ddmmaaaa), excluindo-se quaisquer caracteres de
separação, tais como: ".", "/", "-".
### Validação

a data não pode ser maior que a constante no campo DT_FIN.
### Campo 03 - Valores válidos

[01, 02, 03, 04, 05, 09];
### Campo 04 - Valores válidos

[S, A];
### Campo 05 - Preenchimento

informar neste campo o nível da conta analítica ou sintética informada no Campo 06.
O número correspondente ao nível da conta deve ser crescente a partir da conta/grupo de menor detalhamento (Ativo,
Passivo, etc.).
Nos registros de escrituração de receitas por item/produto (A170, C170, C181/C185, etc), deve-se informar a conta
contábil analítica referente ao item/produto correspondente, caso o plano de contas da empresa tenha este nível
analítico, por item/produto. Nos registros de escrituração de receitas de forma consolidada (C175, por exemplo),
deve-se informar a conta contábil sintética referente ao itens/produtos correspondentes à consolidação.
### Campo 06 - Preenchimento

informar neste campo o código da conta analítica ou sintética utilizada na Escrituração
Contábil da pessoa jurídica. A partir da versão 2.1.1 do PVA da EFD-Contribuições, disponibilizada em agosto de
2017, o tamanho deste campo passa a ser de até 255 caracteres.
Informação de preenchimento – PJ tributadas com base no lucro presumido:
Considerando que o atual programa da EFD-Contribuições (versão 2.1.4) estabelece a obrigatoriedade de se informar
nos registros da escrituração, das operações geradoras de receitas e/ou de créditos, e nos registros de apuração (Bloco
M) e de controle (Bloco 1) a conta contábil (Campo COD_CTA), a partir do período de apuração de novembro de
2017;
Considerando que Instrução Normativa RFB nº 1.774, de 22.12.2017, dispensou da obrigatoriedade da escrituração
contábil digital (ECD) as pessoas jurídicas tributadas com base no lucro presumido que não distribuíram, a título de
lucro, sem incidência do Imposto sobre a Renda Retido na Fonte (IRRF), parcela de lucros ou dividendos, superior
ao valor da base de cálculo do Imposto sobre a Renda diminuída dos impostos e contribuições a que estiver sujeita;
As pessoas jurídicas tributadas com base no lucro presumido não sujeitas à obrigatoriedade da ECD, nos termos da
IN RFB nº 1.774/2017, poderão informar nos campos "COD_CTA" dos registros da EFD-Contribuições, para os
fatos geradores a partir de novembro/2017, inclusive, com a informação "Dispensa de ECD - IN RFB nº
1.774/2017".
Guia Prático da EFD Contribuições – Versão 1.33: Atualização em 16/12/2019
### Campo 07 - Preenchimento

informar neste campo o nome da conta analítica ou sintética utilizada na Escrituração
Contábil da pessoa jurídica.
### Campo 08 - Preenchimento

Campo para informar o código da conta correlacionada no Plano de Contas
Referenciado, publicada pela Receita Federal do Brasil.
### Campo 09 - Preenchimento

No caso da conta informada no registro ser referente a um estabelecimento especifico
da pessoa jurídica, informar neste campo o CNPJ do estabelecimento a que se refere a conta cadastrada.
## Registro 0600: Centro de Custos

Este registro tem o objetivo de identificar os centros de custos referenciados nos registros de operações e documentos
escriturados na EFD-Contribuições.
Não podem ser informados dois ou mais registros com a mesma combinação de conteúdo nos campos DT_ALT e
COD_CCUS.
| Nº | Campo | Descrição | Tipo | Tam | Dec | Obrig |
|----|-------|-----------|------|-----|-----|-------|
| 01 | REG | Texto | fixo | contendo | “0600”. C 004* - S |
| 02 | DT_ALT | Data | da | inclusão/alteração. | N 008* - S |
| 03 | COD_CCUS | Código | do | centro | de custos. C 255 - S |
| 04 | CCUS | Nome | do | centro | de custos. C 060 - S |

### Observações


Nível hierárquico - 2
Ocorrência - Vários (por arquivo)
### Campo 01 - Valor Válido

[0600];
### Campo 02 - Preenchimento

informar no padrão “diamêsano” (ddmmaaaa), excluindo-se quaisquer caracteres de
separação, tais como: ".", "/", "-".
### Validação

a data não pode ser maior que a constante no campo DT_FIN.
### Campo 03 - Preenchimento

informar neste campo o código do centro de custos referenciado nos registros da EFD-
Contribuições. A partir da versão 2.1.1 do PVA da EFD-Contribuições, disponibilizada em agosto de 2017, o
tamanho deste campo passa a ser de até 255 caracteres.
### Campo 04 - Preenchimento

informar neste campo o nome do centro de custos referenciado nos registros da EFD-
Contribuições.
## Registro 0900: Composição das Receitas do Período – Receita Bruta e Demais Receitas

Registro a ser utilizado para detalhamento da composição das receitas do período, por bloco de registros da EFD-
Contribuições. Sua escrituração é obrigatória sempre que o arquivo original da EFD-Contribuições for transmitido
após o prazo regular de entrega (após o 10º dia útil do 2º mês subsequente ao período de apuração a que se refere a
escrituração).
Atenção:
1. A receita total escriturada em cada bloco da escrituração corresponde ao somatório da receita bruta auferida
e das demais receitas, não classificadas como receita bruta. A receita total deve ser informada neste registro
nos Campos 02, 04, 06, 08, 10 e 12, conforme o Bloco de escrituração a que se refira;
2. Compreendem a receita bruta, tanto no regime cumulativo como no regime não cumulativo, as receitas de
que trata o art. 12 do Decreto-Lei no 1.598, de 1977;