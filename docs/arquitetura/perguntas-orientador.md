# Reunião com o orientador — perguntas e preparação

_Preparado em 12/09/2026, a partir da análise dos 1.043 ensaios de cisalhamento direto._

Duas partes: a **Parte 1** é o que sai da sua boca — leve no celular e leia.
A **Parte 2** é o que precisa estar na sua cabeça para entender a resposta e saber
repreguntar. Leia a Parte 2 antes de entrar; use só a Parte 1 lá dentro.

---

# PARTE 1 · Para perguntar

## Abertura — mostre resultado antes de pedir ajuda

> "Peguei o acervo de ensaios do laboratório, 1.043 de cisalhamento direto desde 2023.
> Consegui ler todos automaticamente e rodei a envoltória de Mohr-Coulomb em cima deles,
> agrupando por um critério provisório que eu mesmo inventei — é justamente sobre ele que
> eu preciso perguntar. Deu **φ entre 33° e 41°** e **c entre 6 e 53 kPa**, com **R² acima
> de 0,95** na maioria dos grupos. Bate com o que o senhor espera desses solos?"

**Não apresente esses números como resultado.** Eles saíram do agrupamento provisório da Q1,
antes do critério de descarte do `formato-bruto.md` §5.4 e sem separar a campanha de material
cimentado da de solo natural — as mesmas ressalvas que fazem das "51 envoltórias" uma
estimativa superior. Servem para mostrar que a leitura automática funciona de ponta a ponta,
e para dar ao orientador um número concreto em que reagir. Se ele disser "esse c está alto",
isso é informação sobre o agrupamento, não sobre o solo.

## Q1 · Agrupamento — a mais importante

> "Cada arquivo é um corpo de prova sob uma única tensão normal, e nada no arquivo diz a
> quais outros ele pertence. Como o senhor sabe quais ensaios formam uma série para montar
> a envoltória?
>
> Posso assumir que é **mesma amostra + mesma condição + mesmo dia**? E quando a série
> atravessa dois dias?
>
> Existe uma planilha ou caderno de laboratório com esse registro?"

## Q2 · As letras do ID

> "As letras N, S, U, W e A no ID do ensaio são a condição do corpo de prova? Quais são
> exatamente? Achei que a condição S dá um φ um pouco menor que as outras — seria saturado?"

## Q3 · Os números D

> "No ID tem D1, D7, D8 e D9. O que o D representa — profundidade de coleta? E por que não
> existe D2 a D6?"

## Q4 · Onde ler o τ de pico

> "Para cada ensaio eu preciso de um único valor de tensão cisalhante, que vira um ponto da
> envoltória. Como o senhor lê esse valor na curva: é o máximo, ou tem um deslocamento
> limite? E quando a curva não tem pico claro?"

## Q5 · Permissão de uso

> "Esses ensaios são de outras pessoas do grupo — vi IDs do Augusto, do Gabriel, do Paulo.
> Posso usar no meu PIBITI e no artigo? Como devo creditar? A campanha de 2026, que varia a
> velocidade de cisalhamento, é pesquisa de alguém que ainda está em andamento?"

## Q6 · Material de validação

> "Para validar o sistema eu preciso comparar com o processamento manual. O senhor tem, de
> uns 3 desses ensaios, o **c e o φ calculados na planilha**, para eu comparar com o que o
> meu código dá?"

## Avisos a dar

- **Mudança de escopo:** as máquinas já digitalizam os dados e estão em rede, então o
  Raspberry Pi saiu do plano. O sistema continua automatizando a aquisição, mas a partir
  dos arquivos que as máquinas já produzem.
- **Achei um ensaio travado no acervo:** o NT 608 (`D1N16`, 30/09/2024, σ = 160 kPa) marca
  τ = 1.755 kPa. A leitura é real — o que não é resistência do solo. O ensaio parou em
  3,7 mm com a curva ainda acelerando, sem nenhum pico, e com carga horizontal de 486 kg
  contra 35 a 50 kg nos ensaios vizinhos da mesma série. É o que se espera quando a caixa
  bipartida não está livre; a máquina mediu a reação do equipamento.
  Dizer assim, e não "valor impossível": o acervo tem ensaios legítimos com τ ainda mais
  alto em relação a σ (solo-cimento chega a 1.182 kPa sob 50 kPa). **O que separa um do
  outro é a forma da curva, não a magnitude** — e é isso que o sistema automatizado compara
  e o processamento manual, que lê o máximo da coluna, não tem como perceber.

## Antes de sair da sala

- [ ] Pedir a planilha/caderno de agrupamento (Q1)
- [ ] Pedir os resultados manuais de 3 ensaios (Q6)
- [ ] Perguntar quem do grupo rodou a campanha D1/D7/D8/D9 — essa pessoa responde
      Q1, Q2 e Q3 mais rápido que o orientador
- [ ] Anotar as respostas **literais**, não a sua interpretação delas

---

# PARTE 2 · Para saber antes de perguntar

## Q1 · Agrupamento

**O que eu encontrei.** Um arquivo = um corpo de prova sob uma tensão normal. A envoltória
de Mohr-Coulomb precisa de 3 ou mais pontos (σ, τ), ou seja, 3 ou mais arquivos. Nenhum
campo do arquivo registra a que série ele pertence.

**Minha regra provisória.** Mesma amostra + mesma condição + mesmo dia de ensaio. Aplicada
ao acervo, ela produz **51 envoltórias completas**, várias com 8 ou 9 pontos.

**Onde ela quebra.** Se uma série começou numa terça e terminou na quarta, a regra corta em
duas, e as duas metades saem erradas. Vi séries que atravessam a meia-noite e séries em
dias consecutivos.

**Por que é a pergunta mais importante.** Agrupar errado é pior do que não agrupar: produz
um c e um φ com aparência perfeitamente normal, calculados sobre corpos de prova que não
deveriam estar juntos. Não dá erro na tela e não aparece no gráfico.

**Se ele não souber de cabeça:** peça para olharem juntos uma série que você já separou, e
pergunte se aquele agrupamento está certo. Validar um exemplo vale mais que uma regra
abstrata.

## Q2 · As letras N, S, U, W, A

**O que eu encontrei.** Matriz limpa de 4 amostras × 5 condições — é experimento planejado,
não ensaio avulso. N e W são as mais frequentes (~200 ensaios cada); A quase não aparece (4).

**O indício que tenho.** φ médio de 34,6° na condição S contra 36,3° nas outras. Solo
saturado sendo mais fraco é o comportamento esperado. **Mas é 1,7° em 4 amostras — indício
fraco.** Apresente como pergunta, nunca como conclusão.

**Por que importa.** É o que separa um ensaio de outro dentro da mesma amostra. Se o sistema
misturar condições diferentes numa mesma envoltória, o c e o φ perdem significado físico.

**O que eu preciso da resposta:** o nome por extenso de cada letra, e se alguma delas
**não** é condição de umidade (pode ser energia de compactação, aditivo, tempo de cura).

## Q3 · Os números D

**O que eu encontrei.** Só existem D1, D7, D8 e D9 — o salto de D2 a D6 provavelmente
significa alguma coisa. Confirmei que **não é geometria**: em toda a campanha D o diâmetro é
60 mm, e a altura varia de 20 a 25 mm de corpo de prova para corpo de prova, inclusive
dentro do mesmo D. (No acervo inteiro há 15 arquivos fora dos 60 mm — molde de ~42 mm na
campanha cimentada `B2-30D-*` e a medida real do corpo de prova na campanha `CAT`, 59,89 e
60,10 — mas nenhum deles é da campanha D.)

**Meus palpites, em ordem:** profundidade de coleta em metros · densidade · dias de cura.

**Por que importa.** Define a unidade de análise do relatório. Se for profundidade, o
sistema deve comparar envoltórias ao longo do perfil do solo — e aí o seu trabalho produz
resultado geotécnico, não só software.

## Q4 · Onde ler o τ de pico

**O problema.** Cada ensaio precisa virar um único valor de τ. Essa escolha determina o c e
o φ diretamente.

**As três opções, e o que cada uma custa:**

| Critério | Vantagem | Risco |
| --- | --- | --- |
| Máximo bruto da curva | simples | um ensaio que travou entra como se fosse resistência (o NT 608, de 1.755 kPa) |
| Máximo de curva suavizada | robusto a ruído | suavizar é escolha que precisa ser justificada no artigo |
| Valor a um deslocamento fixado | é o que a norma prescreve | precisa saber qual deslocamento |

**Contexto da norma.** A ASTM D3080 pede o pico **e** o valor residual. Quando a curva não
tem pico claro — solo fofo, que só endurece e nunca cai — ela manda ler a um deslocamento
limite.

**O que eu preciso da resposta:** qual critério o laboratório usa hoje, e o número do
deslocamento limite se houver. Se ele disser "é o máximo", pergunte o que ele faz quando a
curva tem ruído.

## Q5 · Permissão

Os IDs mostram AUGUSTO, GAB, PAULO — são ensaios de outras pessoas. A campanha de 2026, que
varia a velocidade de cisalhamento a σ constante de 160 kPa, parece pesquisa em andamento
de alguém.

**Por que perguntar agora.** Direito de uso e autoria se resolvem barato no começo e caro na
submissão do artigo. Além disso, quem rodou os ensaios é a melhor fonte para Q1, Q2 e Q3.

## Q6 · Validação

O plano previa pedir 3 ensaios já processados manualmente. O acervo tem 51 envoltórias — o
que **falta é o resultado manual** (c e φ calculados na planilha) de alguns deles, para
comparar com a saída do sistema. Sem isso não há validação, e sem validação não há artigo.

---

## Depois da reunião

Anote as respostas em `docs/diario/AAAA-MM-DD.md` e atualize a seção §4 de
`docs/arquitetura/formato-bruto.md`, trocando as hipóteses pelas respostas confirmadas.
Com Q1, Q2 e Q4 respondidas, o parser e o agrupador podem ser escritos.
