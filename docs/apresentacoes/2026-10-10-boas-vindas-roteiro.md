# Roteiro de fala — Boas-vindas ao projeto, 10/10/2026

Acompanha [`2026-10-10-boas-vindas.html`](2026-10-10-boas-vindas.html) (20 slides). Para cada
slide: **o que falar**, a **transição** para o próximo e, quando couber, **se perguntarem**. As
falas sugerem um caminho e não são texto para decorar. Os números estão no slide; a fala diz o
que eles significam.

Quem assiste está chegando agora e não conhece o vocabulário do projeto. Onde aparece
**Explique**, vale dizer o termo em uma frase antes de seguir. As mesmas definições estão no
[`docs/glossario.md`](../glossario.md), que serve para ela consultar depois.

Tempo total estimado: **cerca de 25 minutos** sem perguntas. Não é reunião com o orientador,
então não se aplica o limite de 7 a 10 minutos. Pode ir devagar e abrir para perguntas no meio.
Se o tempo apertar, a seção 02 é a que dá para encurtar: os slides 7, 9 e 10 cabem em uma frase
cada.

| Bloco | Slides | Tempo |
| --- | --- | ---: |
| Abertura | 1–3 | 2 min |
| 01 · O projeto | 4–5 | 4 min |
| 02 · Descobertas | 6–12 | 10 min |
| 03 · Onde estamos | 13–15 | 4 min |
| 04 · Como trabalhar | 16–18 | 4 min |
| 05 · Próximos passos e fechamento | 19–20 | 2 min |

---

## Abertura

### Slide 1 · Capa (≈ 20 s)

> "Vou te mostrar em vinte minutos tudo o que já foi feito no projeto, para você chegar sabendo
> onde as coisas estão. O número do canto é o resultado mais concreto até agora: 914 ensaios do
> laboratório que o sistema já sabe transformar em ponto de envoltória."

### Slide 2 · Em uma frase (≈ 1 min 30 s)

> "O projeto é um PIBITI no GeoFluxo. As máquinas de cisalhamento direto do laboratório já
> gravam cada ensaio num arquivo. O sistema pega esse arquivo, traduz, guarda num banco,
> calcula a coesão e o ângulo de atrito e gera um relatório em PDF."
>
> "Os quatro números: são 1.081 arquivos no acervo e 914 deles são ensaios de cisalhamento
> utilizáveis. O código tem 19 testes automáticos passando, e as descobertas estão contadas em
> 8 registros. Cada número desses registros sai de um script que dá para rodar de novo."

**Explique:** *parser*, o programa que lê o arquivo da máquina e o traduz para um formato
padrão. *Envoltória de Mohr-Coulomb*, a reta τ = c + σ·tan φ ajustada a três ou mais ensaios
do mesmo solo; dela saem c e φ.

**Vale dizer:** o projeto tem 2 horas por semana. É por isso que o plano é dividido em metas de
uma sessão cada.

**Transição:** "O roteiro tem cinco partes."

### Slide 3 · Roteiro (≈ 15 s)

> "Primeiro o que o projeto é e por que ele mudou. Depois o que a gente descobriu lendo os
> arquivos, que é a parte mais interessante. Em seguida onde estamos, como se trabalha no
> repositório e onde você pode ajudar."

---

## 01 · O projeto

### Slide 4 · Mudança de escopo (≈ 2 min)

> "O plano que foi submetido ao PIBITI previa ligar sensores a um Raspberry Pi e ler célula de
> carga e LVDT. Quando a gente abriu os arquivos das máquinas, viu que elas já digitalizam tudo
> e já entregam σ, τ e a área corrigida prontos. Então o hardware saiu do projeto."
>
> "No lugar entraram quatro coisas que o plano não previa: ler o formato das máquinas, fazer a
> triagem de qualidade dos ensaios, agrupar os arquivos em séries e gerar o relatório. O
> trabalho continua do mesmo tamanho, só que agora é de outro tipo: engenharia de dados
> aplicada à geotecnia."
>
> "Duas coisas ficaram para depois. O triaxial, porque não tem nenhum arquivo de triaxial no
> acervo. E a interface gráfica, porque primeiro vem a linha de comando com o PDF."

**Se perguntarem** "qual documento vale, o plano ou isso?": vale o
`docs/arquitetura/visao-geral.md`. O plano submetido fica como histórico e não se edita.

**Transição:** "Esse é o fluxo que ficou."

### Slide 5 · O fluxo (≈ 2 min)

> "São sete etapas, e cada uma tem sua pasta dentro de `src/geotec/`. Só o parser está pronto:
> ele lê os 1.045 arquivos de cisalhamento do acervo."
>
> "Qualidade e cálculo estão pela metade. As regras já foram descobertas e testadas em scripts,
> mas ainda não viraram código do sistema com teste."
>
> "O agrupamento está em vermelho porque é o bloqueio. Ele depende de uma resposta do
> laboratório, e eu volto nele no slide 12."
>
> "Duas regras aparecem embaixo do slide. Por dentro, o código usa só SI: newton, metro,
> pascal, segundo e radiano. kPa e grau só na hora de mostrar. E o banco é SQLite agora e
> MySQL na entrega, com o mesmo código."

**Explique:** *SI*, o Sistema Internacional de unidades. Converter só na apresentação evita
misturar kPa com Pa no meio de uma conta.

**Se perguntarem** "por que SQLite e não MySQL logo?": o SQLite é um arquivo e não exige
servidor, usuário nem senha. Com 2h por semana, essas horas rendem mais no cálculo. O MySQL
continua prometido para a entrega (`visao-geral.md` §6).

**Transição:** "Agora o que a gente aprendeu lendo os arquivos."

---

## 02 · Descobertas

### Slide 6 · Divisor (≈ 15 s)

> "Os 1.081 arquivos foram lidos um por um. Saíram três lições: a maior parte do que parecia
> descarte não é falha; ensaio que não rompeu engana; e, sem os filtros, a mesma série dá um
> ângulo de atrito de 5° em vez de 32°."

### Slide 7 · Formato e layouts (≈ 1 min 30 s)

> "O arquivo de cisalhamento é um CSV bem-comportado: separador ponto e vírgula, decimal com
> vírgula, 7 linhas de cabeçalho e 17 colunas, igual em todos."
>
> "O problema é que existe um segundo layout, o de adensamento, com a mesma extensão. E o tipo
> do ensaio só aparece no nome do arquivo. Se alguém ler um arquivo de adensamento como se
> fosse de cisalhamento, uma das leituras devolve um corpo de prova de 5 mm em vez de 50 e não
> dá erro nenhum. Isso é uma falha silenciosa: o código roda e o número sai errado."
>
> "Por isso o parser confere tudo antes de converter e recusa o que não reconhece."

**Explique:** *CSV*, arquivo de texto com uma linha por leitura e os valores separados por um
caractere. *Falha silenciosa*, erro que não aparece na tela e produz resultado errado.

### Slide 8 · Triagem do acervo (≈ 1 min 30 s)

> "Dos 1.043 arquivos de cisalhamento direto, 914 viram ponto de envoltória. Uma leitura
> anterior chamava os outros 129 de 'abortados'. Só que 108 deles têm um arquivo irmão, com o
> mesmo ID e a mesma data, que contém a etapa de cisalhamento. Ensaio com falha de verdade são
> só 21."
>
> "Repara nos três blocos à direita. O primeiro é o que o arquivo mostra. O segundo, em
> vermelho, é a minha interpretação: as duas etapas do ensaio foram salvas em arquivos
> separados. Isso é dedução e o laboratório ainda não confirmou. O terceiro é a decisão. Esse
> jeito de separar dado, interpretação e decisão vale para todo documento do projeto."

**Se perguntarem** "o que é a etapa de adensamento?": antes de cisalhar, o corpo de prova é
comprimido sob a tensão normal até estabilizar; depois vem o cisalhamento.

### Slide 9 · Ensaios travados (≈ 1 min 30 s)

> "Para virar ponto da envoltória, o ensaio precisa ter rompido. O NT 608 marca τ de 1.755 kPa
> sob σ de 160 kPa, onze vezes a tensão normal, e parou aos 3,7 mm com a curva ainda subindo.
> Ele não rompeu, e se entrar na conta estraga a reta."
>
> "O filtro óbvio seria reprovar τ alto demais para o σ. Só que ele derruba 211 ensaios para
> pegar os mesmos 3, e o ensaio com a maior razão do acervo é um ensaio bom. Então o critério
> ficou na forma da curva: o ensaio parou antes de 5 mm e o pico está no último ponto."

**Se perguntarem** "por que tantos ensaios com τ alto?": o acervo tem uma campanha de
solo-cimento, e material cimentado tem coesão alta (`2026-09-12-forma-da-curva.md`).

### Slide 10 · O ID não é dado (≈ 1 min)

> "O ID do ensaio é digitado pelo operador e parece dizer a tensão normal: `D1N16` seria 160
> kPa. No NT 614 a máquina mediu 22. Em seis IDs, o mesmo nome aparece com tensões
> diferentes."
>
> "A regra que saiu disso vale para o sistema inteiro: σ sempre vem da coluna de dados, nunca
> do nome. Na série D1N, se a gente ler σ pelo ID, a coesão sai negativa."

### Slide 11 · Envoltória D1N (≈ 2 min)

> "Isto é o que o sistema vai fazer no acervo inteiro, aqui feito para uma série só. São sete
> ensaios da série D1N que romperam, e a reta dá c = 22,6 kPa, φ = 32,2° e R² = 0,980."
>
> "A tabela da direita refaz a conta com cada erro que os filtros evitam. Sem o filtro de
> não-ruptura, φ cai para 5° e o R² vai a zero. Com σ lido do ID, a coesão fica negativa. Os
> filtros não são detalhe: eles mudam o resultado."
>
> "Um detalhe de método: τ é lido a 10 mm de deslocamento, que é o critério do laboratório.
> Antes eu usava o máximo da curva. A troca foi registrada em 29/09."

**Explique:** *R²*, quanto a reta explica os pontos. 1 quer dizer todos os pontos sobre a
reta.

**Se perguntarem** "isso já está no sistema?": ainda não. Está em
`scripts/apoio_apresentacao.py`. Passar para `src/geotec/nucleo/` com teste é uma das tarefas
do slide 19.

### Slide 12 · Citação (≈ 45 s)

> "Esta frase resume o bloqueio. Cada arquivo é um corpo de prova sob uma tensão normal, e a
> envoltória precisa de três ou mais. Só que nada no arquivo diz a que série ele pertence. Se a
> gente agrupar errado, sai um c e um φ com cara de normais, sem nenhum erro na tela. Por isso
> o agrupamento espera a resposta do laboratório."

**Transição:** "Isso leva ao ponto em que estamos."

---

## 03 · Onde estamos

### Slide 13 · Situação das metas (≈ 1 min 30 s)

> "As metas de ler o arquivo estão concluídas: formato, parser, teste e metadados. As de
> cálculo estão parciais, e o padrão é sempre o mesmo: a regra foi descoberta e usada em
> script, mas ainda não virou função com teste."
>
> "O parser do triaxial está bloqueado porque não existe arquivo de triaxial."

**Vale dizer:** cada meta que andou tem uma ficha em `docs/plano/entregas/` com a data, os
commits e como conferir.

### Slide 14 · Reunião de 30/09 (≈ 1 min 30 s)

> "Na reunião de 30/09, o orientador pediu reuniões de 7 a 10 minutos, focadas em resultado,
> método e dificuldade. Pediu também para eu ler o 'livro azul' de cisalhamento e para o
> sistema entregar o resultado já interpretado, de um jeito que as empresas entendam, inclusive
> explicando quando um ensaio dá errado."
>
> "À direita estão ideias minhas, que eu ainda não discuti com ele. Nada disso mudou o escopo
> ainda."

**Vale dizer:** nas atas de `docs/reunioes/`, o que o professor disse fica sempre separado das
ideias do aluno. Na dúvida sobre quem disse, não se atribui ao professor.

### Slide 15 · Em aberto (≈ 1 min)

> "Estas são as perguntas pendentes e de quem depende cada resposta. As quatro primeiras
> dependem do laboratório. A mais importante é a Q1, a regra de agrupamento. As outras dependem
> do orientador: o c e o φ que o laboratório calculou à mão, para validar o sistema, e qual é o
> livro azul."

**Transição:** "Agora, como se trabalha no repositório."

---

## 04 · Como trabalhar

### Slide 16 · Mapa do repositório (≈ 1 min)

> "Comece sempre pelo `README.md`: quase tudo está a um link dele. O documento que vale é o
> `visao-geral.md`. As descobertas estão em `docs/registros/`, por ordem de data. E quando um
> termo travar, o `glossario.md` explica."
>
> "Os arquivos do acervo ficam em `dados/Ensaios-270/`. São a fonte primária e não se editam."

**Explique:** *repositório*, a pasta do projeto com todo o histórico de mudanças guardado
pelo Git. Ele está no GitHub, em `TiagoNaves27/PIBITI-2026`.

### Slide 17 · Regras da casa (≈ 1 min 30 s)

> "Quatro regras. Primeira: SI por dentro, kPa e grau só na tela. Segunda: cálculo novo só
> entra com teste, e o valor do teste precisa ter sido conferido à mão ou vir de norma ou
> livro. Terceira: todo número citado vem de um script. E registro não se corrige por cima:
> se o número mudar, faz-se um registro novo. Quarta: nunca inventar contexto, e dedução fica
> marcada como dedução."
>
> "Além disso, tudo é em português: documentação, commits e nomes de função, só que sem
> acento no código."

**Explique:** *teste*, um código pequeno que roda a função com uma entrada conhecida e
confere se o resultado bate com o esperado. *Commit*, um registro de mudança no histórico
do Git.

### Slide 18 · Primeiro dia (≈ 1 min)

> "Para começar são quatro comandos, e a coluna da direita diz como saber se deu certo.
> `uv sync` monta o ambiente, `pytest` tem que mostrar 19 passed, e `ruff` tem que mostrar All
> checks passed. O último roda um script que reproduz um registro inteiro em menos de um
> segundo, e é um bom jeito de ver como as coisas se ligam."
>
> "Para ler: README, visão geral, depois os registros do mais antigo ao mais novo."

**Explique:** *uv*, o programa que instala o Python e as bibliotecas do projeto. *lint*,
uma checagem automática que aponta erros comuns e problemas de estilo no código.

**Se perguntarem** "e se o `pytest` falhar?": copie a mensagem de erro inteira e me mande. Não
dá para adivinhar o motivo sem ela.

---

## 05 · Próximos passos

### Slide 19 · Onde ajudar (≈ 1 min 30 s)

> "Estas tarefas não dependem de ninguém do laboratório. A primeira é escrever o
> `formulas.md`, com cada equação que o sistema vai implementar e a unidade dela. Depois vêm as
> duas funções de cálculo em `nucleo/`, uma para reduzir o ensaio a σ e τ a 10 mm e outra para
> tirar c, φ e R² dos pontos, cada uma com teste. Em seguida, passar a rotina de qualidade para
> código. Banco e relatório vêm depois."
>
> "Minha sugestão é cada um trabalhar numa branch própria e a gente combinar antes quem pega o
> quê, para não mexer os dois no mesmo arquivo."

**Explique:** *branch*, uma linha de trabalho separada no Git. Cada um mexe na sua, e depois
o trabalho é juntado ao principal.

**Vale dizer:** essa sugestão é sua, não uma decisão registrada no projeto.

### Slide 20 · Fechamento (≈ 15 s)

> "Tudo o que eu mostrei tem fonte no repositório. Se você esquecer onde estava alguma coisa,
> o README é a porta de entrada. Perguntas?"
