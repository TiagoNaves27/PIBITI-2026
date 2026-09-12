# Roteiro de estudos

_Última atualização: 11/09/2026_

## Princípio: estudar na hora de usar

A 2h/semana, estudar tudo antes de começar é o caminho mais rápido para esquecer tudo antes
de usar. Cada bloco abaixo está amarrado à semana em que o assunto aparece no
[backlog de metas](metas-semanais.md). Estude o bloco na semana anterior ao uso — não antes.

Marcação de esforço: 🕐 = cabe em uma sessão de 2h. 🕐🕐 = duas semanas.

---

## Bloco A — Ler arquivos bagunçados com pandas 🕐🕐

**Quando:** antes de escrever o primeiro parser.
**Por quê:** arquivo de máquina de ensaio tem cabeçalho de tamanho variável, separador
estranho, vírgula decimal, linhas de rodapé e coluna de unidade. É 80% do trabalho real.

- **Kaggle Learn — Pandas** · <https://www.kaggle.com/learn/pandas> · grátis, interativo, ~4h
  no total; faça só as lições 1 a 3.
- **Documentação oficial — "10 minutes to pandas"** ·
  <https://pandas.pydata.org/docs/user_guide/10min.html>
- **O que realmente importa dominar:** os parâmetros de `pd.read_csv` —
  `sep`, `skiprows`, `header`, `names`, `decimal=','`, `encoding`, `engine='python'`,
  `nrows`, `skipfooter`. Leia a docstring inteira uma vez:
  <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>
- **Referência de fundo (não leia inteiro):** Wes McKinney, *Python for Data Analysis*,
  3ª ed. — **gratuito online**: <https://wesmckinney.com/book/> · capítulo 6 (Data Loading).

## Bloco B — Resistência ao cisalhamento: as fórmulas 🕐🕐

**Quando:** antes de implementar qualquer cálculo.
**Por quê:** você precisa saber exatamente o que calcular antes de programar. Esta é a parte
em que *você* é o especialista, não o computador.

- **Pinto, C. S. — *Curso Básico de Mecânica dos Solos*** · capítulo de resistência ao
  cisalhamento. É a melhor explicação em português. Comece por aqui.
- **Das, B. M. — *Fundamentos de Engenharia Geotécnica*** · capítulo de resistência.
- **Head, K. H. — *Manual of Soil Laboratory Testing*** · Vol. 2 (cisalhamento direto),
  Vol. 3 (triaxial). Este é o que traz o **procedimento de cálculo passo a passo**, que é
  literalmente o algoritmo que você vai programar. Se der para pegar um só livro, é este.
- **ASTM D3080** (direto) e **D7181 / D4767** (triaxial) · a seção "Calculation" de cada
  norma lista as equações e a seção "Report" lista o que o relatório precisa conter — ou
  seja, a norma já te entrega a especificação do software.

**Produto do estudo:** um arquivo `docs/arquitetura/formulas.md` com cada equação que o
sistema precisa implementar, com as unidades. Sem isso, programar é chute.

## Bloco C — Gráficos com matplotlib 🕐

**Quando:** antes da primeira curva τ × deslocamento.

- **Tutorial oficial "Pyplot"** · <https://matplotlib.org/stable/tutorials/pyplot.html>
- **"Anatomy of a figure"** · <https://matplotlib.org/stable/gallery/showcase/anatomy.html>
  — entender `Figure` vs. `Axes` resolve 90% da confusão com matplotlib.
- **Rougier, N. — *Scientific Visualization: Python + Matplotlib*** · livro **gratuito**:
  <https://github.com/rougier/scientific-visualization-book> — voltado a figura de artigo
  científico, que é exatamente o seu caso.
- **Para o PDF:** `matplotlib.backends.backend_pdf.PdfPages` gera PDF de várias páginas sem
  instalar mais nada. É o caminho mais curto para o relatório.

## Bloco D — SQL e modelagem de dados 🕐🕐

**Quando:** antes de desenhar o schema.

- **SQLBolt** · <https://sqlbolt.com> · grátis, interativo, roda no navegador. As lições 1–12
  cobrem tudo que você precisa e cabem em 2h.
- **Modelagem:** entender chave primária, chave estrangeira e a relação um-para-muitos. É
  literalmente o que você precisa para `ensaio → estagio → leitura`. O tutorial do SQLBolt
  já cobre `JOIN`, que é o outro lado disso.
- **SQLAlchemy — tutorial oficial unificado** ·
  <https://docs.sqlalchemy.org/en/20/tutorial/> · leia só a parte **Core** (Working with
  Data). O ORM é mais poder do que este projeto precisa.

## Bloco E — Git para não perder trabalho 🕐

**Quando:** agora, e depois nunca mais.

Você precisa de cinco comandos, não do livro inteiro:

```bash
git status                 # o que mudou
git add -A                 # marcar tudo para o commit
git commit -m "mensagem"   # salvar um ponto no tempo
git log --oneline          # ver o histórico
git push                   # mandar para o GitHub (depois de criar o repositório)
```

- **Pro Git, em português, gratuito** · <https://git-scm.com/book/pt-br/v2> · leia só os
  capítulos 1 e 2.
- Crie um repositório **privado** no GitHub e dê `push` toda semana. É seu backup e é a
  prova do seu progresso para o orientador.

## Bloco F — Opcional, só se sobrar tempo

- **Testes com pytest** · <https://docs.pytest.org/en/stable/getting-started.html> — vale
  muito num projeto de cálculo: um teste garante que a fórmula continua certa depois de
  você mexer no código.
- **Escrita científica** — o artigo do mês 11. O orientador é a melhor fonte aqui; peça um
  artigo do grupo como modelo.

---

## O que **não** estudar

Não gaste as suas 100h nisso:

- Raspberry Pi, GPIO, eletrônica, ADC — **saiu do escopo**
- Frameworks de GUI (PyQt, Tkinter) — só na fase opcional, no fim
- Docker, CI/CD, deploy, nuvem — irrelevante aqui
- Machine learning — não é o objeto da pesquisa
- Administração de MySQL (usuários, replicação, tuning) — SQLite no desenvolvimento resolve
