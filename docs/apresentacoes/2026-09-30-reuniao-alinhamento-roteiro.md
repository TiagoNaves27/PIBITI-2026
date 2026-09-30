# Roteiro de fala — Reunião de alinhamento, 30/09/2026

Acompanha [`2026-09-30-reuniao-alinhamento.html`](2026-09-30-reuniao-alinhamento.html)
(18 slides). Para cada slide: **o que falar**, a **transição** para o próximo e, quando
couber, **se perguntarem**. As falas são sugestão de fluxo, não texto para decorar: os números
estão no slide, e a fala explica o que eles querem dizer.

Tempo total estimado: **cerca de 20 minutos** sem perguntas. O miolo é a seção 02 (slides 6 a
14); se o tempo apertar, os slides 13 e 14 podem ser passados em uma frase cada.

| Bloco | Slides | Tempo |
| --- | --- | ---: |
| Abertura | 1–3 | 2 min |
| 01 · Escopo | 4–5 | 3 min |
| 02 · O que o acervo escondia | 6–14 | 11 min |
| 03 a 05 · Sistema, repositório, em aberto | 15–17 | 4 min |
| Fechamento | 18 | — |

---

## Abertura

### Slide 1 · Abertura (≈ 20 s)

> "Esta é a reunião de alinhamento do PIBITI. O título resume o caminho do trabalho: sair do
> arquivo que a máquina grava e chegar na envoltória de Mohr-Coulomb. O número do canto já
> adianta o resultado: dos 1.043 ensaios de cisalhamento direto, 914 viram ponto de
> envoltória."

### Slide 2 · Resultado primeiro (≈ 1 min)

> "Começo pelo resultado. O sistema leu automaticamente os 1.043 ensaios de cisalhamento
> direto do laboratório, de 2023 até hoje. Aplicando uma regra provisória de agrupamento, saem
> 51 envoltórias completas, com φ entre 33° e 41°, coesão entre 6 e 53 kPa e R² acima de 0,95
> na maioria dos grupos."
>
> "Mas eu chamo isso de **estimativa superior**, e o resto da apresentação explica por quê:
> esse número foi contado antes do filtro de ensaios que não romperam, e com uma regra de
> agrupamento que eu ainda preciso confirmar com o senhor."

**Atenção:** a faixa de 33° a 41° também foi calculada com o **máximo** de τ, antes de eu
saber que o laboratório lê τ a 10 mm. Vale dizer isso de passagem: "e ainda com o critério
antigo de τ, que eu corrijo no slide 8".

**Transição:** "Antes dos achados, o roteiro."

### Slide 3 · Agenda (≈ 20 s)

> "São cinco partes: o que mudou no escopo, o que o acervo escondia — que é o miolo —, o que
> isso mudou no desenho do sistema, onde o projeto está guardado e o que ficou em aberto."

---

## 01 · Escopo

### Slide 4 · Mudança de escopo (≈ 1 min 30 s)

> "O plano previa integrar sensores a um Raspberry Pi, ler célula de carga e LVDT e converter
> carga em tensão. O que se verificou é que as máquinas já digitalizam e gravam tudo, e já
> entregam σ, τ e a área corrigida prontos. Com isso saem o hardware, a calibração e as
> semanas 12 e 13 do cronograma."
>
> "No lugar entra outro tipo de trabalho: ler o formato das máquinas, fazer a triagem de
> qualidade, agrupar os arquivos em séries e gerar o relatório. O trabalho não encolheu, mudou
> de natureza: virou engenharia de dados aplicada à geotecnia."

**Se perguntarem** "então não tem mais hardware nenhum?": não. As máquinas estão em rede e a
coleta virou cópia de arquivo (`docs/registros/2026-09-12-mudanca-de-escopo.md`).

### Slide 5 · O acervo (≈ 1 min)

> "O acervo tem 1.081 arquivos, de maio de 2023 a agosto de 2026: 1.043 de cisalhamento
> direto, 36 de adensamento e nenhum de triaxial. Isso bloqueia a semana 8 do cronograma,
> que dependia de um arquivo de triaxial."
>
> "Pelos identificadores dá para ver que os arquivos são de várias pessoas do grupo, incluindo
> uma campanha de solo-cimento e uma de 2026 que varia a velocidade de cisalhamento."

**Transição:** "Ler esse acervo inteiro mostrou três coisas que não aparecem olhando um ensaio
de cada vez."

---

## 02 · O que o acervo escondia

### Slide 6 · Divisor (≈ 15 s)

> "São três achados: descartes que pareciam ensaios perdidos e não eram; ensaios que nunca
> romperam e que uma planilha aceitaria; e um identificador que não diz o que o arquivo
> contém."

### Slide 7 · Triagem do acervo (≈ 1 min 30 s)

> "Primeiro achado. Dos 1.043 arquivos, 914 têm a etapa de cisalhamento com pelo menos 5
> leituras: são os utilizáveis. Sobram 129, e a leitura óbvia seria '129 ensaios abortados'."
>
> "Só que 108 desses arquivos, que só têm adensamento, têm um irmão com o mesmo ID e a mesma
> data que tem a etapa de cisalhamento. A minha interpretação, que ainda preciso confirmar no
> laboratório, é que o ensaio é salvo em duas partes. Se for isso, a perda real é de 2%, não
> de 13%."
>
> "Isso já mudou o desenho do banco: ele guarda o **motivo** de cada descarte, numa tabela de
> ocorrências, e não um campo 'válido sim ou não'. Os 108 não são a mesma coisa que os 17."

**Se perguntarem** "e os 21 que são falha de verdade?": 17 arquivos só de adensamento sem irmão
e 4 com 1 a 4 leituras de cisalhamento.

**Transição:** "O segundo achado é o mais importante, e começa por como uma série boa se
parece."

### Slide 8 · Série D1N (≈ 2 min)

> "Esta é a série D1N, ensaiada em 30/09/2024: sete ensaios, de σ = 22 a 500 kPa, cada curva
> rotulada com a sua tensão normal. Todos vão até cerca de 28 mm. Com σ alto a curva tem pico
> e depois cai; com σ baixo ela fica quase plana."
>
> "Cada ensaio precisa virar **um** valor de τ para entrar na envoltória. Eu estava usando o
> máximo da curva, mas o critério do laboratório é ler τ **a 10 mm** de deslocamento — é a
> linha tracejada, e os pontos vermelhos são esses valores. Nenhum ensaio tem leitura
> exatamente em 10 mm: as leituras são em 9,0 e 10,2 mm, então eu interpolo."
>
> "Com esse critério, a envoltória dá c = 22,6 kPa e φ = 32,2°. Pelo máximo seriam 24,0 kPa e
> 32,6°. Nesta série a diferença é pequena."
>
> "Fora do gráfico ficou o NT 608, da mesma série, a σ = 160 kPa: ele marcou 1.755 kPa aos
> 3,7 mm, sem romper. É dele que eu falo agora."

**Se perguntarem:**
- *"Por que não usar o máximo?"* Porque 10 mm é o que o laboratório usa, e o número do
  sistema tem que bater com o do processamento manual. Em dois ensaios desta série (σ = 22 e
  80 kPa), o máximo acontece depois dos 10 mm, aos 17,4 e 21,0 mm.
- *"Interpola ou lê o ponto de 10,2 mm?"* Hoje eu interpolo. **Vale perguntar** qual dos dois
  o laboratório faz.
- *"Por que só essa série?"* É a série que os registros já conhecem ponto a ponto, e a mesma da
  envoltória do slide 11. Ensaios acima de 550 kPa ficaram fora do gráfico; nesta série, isso
  exclui só o NT 608.

### Slide 9 · O filtro em ação (≈ 1 min 30 s)

> "Os ensaios travados param antes de 4 mm. Com o critério de 10 mm, eles simplesmente não
> têm valor. E o único número que sobra no arquivo, o máximo, não é ruptura: é onde a máquina
> estava quando o ensaio parou."
>
> "Para achar esses casos, o filtro tem duas etapas. 'Pico no último ponto' sozinho pega 421
> ensaios, quase metade do acervo, porque muito solo endurece até o fim sem pico definido.
> Combinado com 'parou antes de 5 mm', sobram 9 que não romperam; e 3 deles têm o trecho final
> acelerando, como o NT 268 e o NT 625 da tabela."
>
> "A decisão foi separar duas coisas. Não romper **descarta** o ensaio da envoltória. Rigidez
> final acima de 3 vezes a mediana só **sinaliza**: é indício forte, não prova, e a decisão
> fica com o pesquisador."

**Se perguntarem** "o que travou esses ensaios?": não está gravado no arquivo. A leitura de
caixa bipartida travada (parafuso não retirado, fim de curso ou inclusão rígida) é dedução a
partir dos números. Confirmar com quem operou a máquina transformaria dedução em fato.

**Transição:** "A pergunta natural seria: por que não descartar simplesmente quem tem τ alto
demais?"

### Slide 10 · Forma, não magnitude (≈ 1 min 30 s)

> "Porque não funciona. Um limiar de τ acima de 1,2 vez σ descartaria 211 ensaios para pegar
> 3. Desses 211, 106 romperam normalmente antes do último ponto. E o NT 268, que é travado,
> tem razão τ/σ de só 2 vezes: a magnitude não o denuncia."
>
> "As maiores razões do acervo são de material cimentado, com coesão de centenas de kPa. Sob σ
> baixa, razões de 20 vezes aparecem sem nada de errado. Por isso, nenhum critério de
> qualidade do sistema usa a magnitude de τ; o que conta é a forma da curva."

**Se perguntarem** "é solo-cimento mesmo?": é leitura a partir do identificador (B2/B5),
não confirmada. O NT 295 nunca desceu do pico e merece olhar humano.

### Slide 11 · A envoltória que sobra (≈ 1 min 30 s)

> "Juntando tudo: os sete ensaios da D1N que passam no filtro, com τ a 10 mm, fecham uma
> envoltória sozinhos: φ = 32,2°, c = 22,6 kPa, R² = 0,980."
>
> "Os filtros fazem diferença, e isso é medido, não suposto. Sem o filtro de ruptura, o NT 608
> entra com 1.755 kPa e o R² cai para 0,001: não sobra envoltória. E o ponto de 22 kPa, em
> vermelho, é o NT 614: o identificador dele diz 160 kPa. Se eu tivesse lido σ do nome, a
> coesão sairia negativa, −2,1 kPa."

**Se perguntarem:**
- *"E se juntar os ensaios de 160 kPa do dia seguinte?"* Com o NT 616 e o NT 618, de
  01/10/2024, dá c = 26,8 kPa, φ = 31,9° e R² = 0,968. Muda pouco, mas incluir é decidir a Q1
  (uma série pode atravessar dias?), que é pergunta para o senhor.
- *"Por que 32,2° fica abaixo da faixa do slide 2?"* A faixa de 33° a 41° foi calculada antes
  dos filtros, com o máximo de τ e sem separar a campanha cimentada. Precisa ser recontada.

### Slide 12 · O formato do ID (≈ 1 min 30 s)

> "Terceiro achado. O identificador parece dizer a tensão normal. D1N16, por exemplo, sugere
> 160 kPa. Mas, dos 748 IDs distintos, 96 aparecem em mais de um ensaio, e em 6 deles o σ
> medido diverge mais de 15 kPa. Seis é um piso, porque 652 IDs aparecem uma vez só e não dá
> para comparar."
>
> "Isso já mudou uma regra: nenhuma grandeza física vem do nome do arquivo; σ, τ e
> deslocamento vêm sempre da coluna medida pela máquina."
>
> "E aqui tem uma proposta: não existe um padrão para os IDs digitados. A ideia é criar um,
> usando um subconjunto de ensaios como referência, e aplicar nos próximos ensaios, para
> facilitar pesquisas futuras e o banco de dados."

### Slide 13 · Dois layouts (≈ 1 min — ou 15 s se o tempo apertar)

> "Um bônus sobre a robustez do leitor de arquivos. Cisalhamento e adensamento gravam dois
> layouts diferentes com a mesma extensão. Se eu ler um arquivo de adensamento como
> cisalhamento, nenhuma forma de leitura avisa: uma devolve um corpo de prova de 5 mm em vez
> de 50, outra acerta por sorte e outra dá um erro que não fala do tipo de arquivo. Por isso o
> parser recusa o que não reconhece, em vez de adivinhar."

### Slide 14 · Citação (≈ 15 s)

> "Essa frase é de um registro de 13/09. Uma afirmação sobre esse comportamento estava escrita
> em três documentos e nunca tinha sido testada; o script mediu e ela estava errada. É a regra
> que eu sigo em todos os registros: todo número tem um script por trás."

**Transição:** "Esses achados mudaram o desenho do sistema em quatro pontos."

---

## 03 a 05 · Sistema, repositório, em aberto

### Slide 15 · Síntese (≈ 1 min)

> "Quatro decisões que só existem porque o acervo foi lido, e não suposto: o descarte guarda o
> motivo; a qualidade é julgada pela forma da curva, nunca pela magnitude de τ; nenhuma
> grandeza vem do nome do arquivo; e o parser recusa o que não reconhece."
>
> "O valor do sistema não está em automatizar o que a planilha já fazia. Está nas verificações
> que uma planilha não comporta."

### Slide 16 · Repositório no GitHub (≈ 30 s)

> "Tudo isso está versionado no GitHub: código, registros e histórico. Cada registro tem o
> comando que refaz o número que ele cita."

### Slide 17 · Em aberto (≈ 2 min)

> "Por fim, o que depende de outras pessoas. Para o senhor, a principal é a Q1: uma série pode
> atravessar dois dias? Ela define o agrupamento e a recontagem das 51 envoltórias. Para o
> laboratório: confirmar se os 108 arquivos só de adensamento são ensaios salvos em duas
> partes, e se os IDs 'MOVIMENTO' são teste de equipamento. O NT 923, com τ zero em todos os
> pontos, vai virar uma quarta condição da triagem. E o triaxial só volta ao escopo se
> aparecer pelo menos um arquivo."

**Acrescentar de viva voz (não está no slide):**

> "Tem uma pergunta nova, que surgiu com o critério de 10 mm. Dos 914 ensaios utilizáveis, 116
> param antes de 10 mm. Treze param antes de 5 mm e o filtro já descarta. Mas 103 param entre
> 5 e 10 mm: passam no filtro e não têm τ a 10 mm. O que o laboratório faz com esses ensaios?
> Descarta, lê em outro ponto? Dependendo da resposta, o número de ensaios que viram ponto de
> envoltória pode cair de 914 para perto de 800."

Vale perguntar também se os 10 mm valem **mesmo quando a curva tem pico claro antes** (na D1N,
o ensaio a 400 kPa tem pico de 269 kPa aos 7,8 mm e vale 254 kPa a 10 mm).

---

## Fechamento

### Slide 18 · Obrigado

> "Obrigado. Os registros completos, com o script e a figura por trás de cada número, estão em
> `docs/registros/`. Fico à disposição para perguntas."

---

## Perguntas para sair da reunião com resposta

Em ordem de prioridade:

1. **Q1 · Agrupamento.** Uma série pode atravessar dois dias? (slides 11 e 17)
2. **Os 103 ensaios entre 5 e 10 mm.** O que fazer com eles no critério de 10 mm? (slide 17)
3. **Critério de 10 mm.** Interpola ou lê a leitura de 10,2 mm? Vale também quando há pico
   claro antes? (slide 8)
4. **Q7 · Laboratório.** Arquivos salvos em duas partes e IDs "MOVIMENTO". (slides 7 e 17)
5. **Padrão de ID.** O senhor concorda com criar um padrão a partir de um subconjunto de
   referência? (slide 12)

## Fontes

Cada fala tira os números do slide correspondente; a tabela de referências slide a slide está
no [README das apresentações](README.md). O critério de 10 mm e os números 116/103 vêm de
[`2026-09-29-ruptura-a-10mm.md`](../registros/2026-09-29-ruptura-a-10mm.md).
