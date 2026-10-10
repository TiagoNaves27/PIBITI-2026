# Metas semanais

_Última atualização: 10/10/2026_

**Orçamento real: 2h por semana ≈ 96h no ano.** Cada meta abaixo cabe em **uma sessão de
2 horas** e termina em algo concreto que dá para mostrar. Semana sem entregável é semana
que some sem deixar rastro.

**Regra:** se uma meta não couber em 2h, ela está mal dividida — quebre em duas, não
transforme a semana em 4h.

Ao fim de cada semana, copie `docs/diario/MODELO.md` para `docs/diario/AAAA-MM-DD.md` e
preencha. Esse arquivo é o que você manda para o orientador.

**Quando uma meta andar**, registre em [`entregas/`](entregas/README.md) — uma ficha por meta,
com a data, o que foi feito e como conferir — e marque a situação no título da semana aqui:
✅ concluída · 🟡 parcial · ⛔ bloqueada. Sem marca, não começou.

## Onde estamos — 10/10/2026

- **Concluídas:** semanas 2, 5, 6, 7 e 15. O parser do cisalhamento direto lê os 1.045
  arquivos DS/DSS do acervo, com 19 testes.
- **Parciais:** semanas 1, 3–4, 9, 14 e 16–17, e a rotina de qualidade. O padrão é o mesmo nas
  três últimas: **a regra foi descoberta e usada em script, mas ainda não virou função em
  `src/geotec/nucleo/` com teste.**
- **Bloqueios externos:** nenhum arquivo triaxial (Semana 8) e a regra de agrupamento das
  séries (Q1), que trava rodar a envoltória no acervo inteiro. Os dois dependem do
  laboratório.
- **Próximas, sem depender de ninguém:** Semanas 10–11 (`formulas.md`), e depois levar a
  ruptura (Semana 14) e a envoltória (16–17) para `nucleo/` com teste. A Q4 — onde ler o τ —
  já está respondida: a 10 mm.

---

## Fase 0 — Descoberta (3 semanas · 6h)

> Objetivo: descobrir o formato dos dados. **Todo o resto do projeto está travado aqui.**

### Semana 1 — Ir ao laboratório — 🟡 [parcial](entregas/semana-01-laboratorio.md)
- [ ] Anotar marca, modelo e nome do software de cada máquina (direto e triaxial)
- [ ] Exportar **um arquivo bruto de cada ensaio** e salvar em `dados/exemplos/bruto/`
      — cisalhamento direto coberto pelo acervo de 1.081 arquivos (12/09); **falta o triaxial**
- [ ] Descobrir como os arquivos são acessados pela rede (pasta compartilhada? FTP? nuvem?)
- **Entregável:** 2 arquivos no repositório + as respostas do §3 de `visao-geral.md`
- **Mostrar ao orientador:** "consegui os arquivos brutos; o formato é X"

### Semana 2 — Entender o arquivo — ✅ [12/09/2026](entregas/semana-02-formato-bruto.md)
- [x] Rodar `uv run python scripts/inspecionar.py dados/exemplos/bruto/<arquivo>`
- [x] Documentar em `docs/arquitetura/formato-bruto.md`: separador, codificação, tamanho do
      cabeçalho, nome e unidade de cada coluna
- [ ] Perguntar ao técnico do laboratório o que cada coluna significa
- **Entregável:** `formato-bruto.md` preenchido
- **Mostrar:** a tabela de colunas e unidades

### Semana 3 — Estudo: Bloco A, parte 1 — 🟡 [parcial](entregas/semanas-03-04-estudo-pandas.md)
- [ ] Kaggle Learn Pandas, lições 1–3 (link em `roteiro-estudos.md`)
- **Entregável:** um notebook em `notebooks/` que abre o arquivo bruto com `pd.read_csv`,
      mesmo que saia torto
- **Mostrar:** "já consigo abrir o arquivo no Python"
- **Situação:** o entregável foi coberto pelo parser da Semana 5; as lições não têm registro.

## Fase 1 — Tradução dos dados (6 semanas · 12h)

### Semana 4 — Estudo: Bloco A, parte 2 — 🟡 [parcial](entregas/semanas-03-04-estudo-pandas.md)
- [ ] Ler a docstring inteira de `pd.read_csv`; testar `skiprows`, `decimal`, `encoding`
- **Entregável:** notebook lendo o arquivo com as colunas certas e números como número
      (não como texto)

### Semana 5 — Parser do cisalhamento direto — ✅ [12/09/2026](entregas/semana-05-parser-direto.md)
- [x] `src/geotec/parsers/direto.py`: função que recebe caminho e devolve DataFrame normalizado
- **Entregável:** a função funcionando no arquivo de exemplo
- **Mostrar:** DataFrame limpo, com as colunas do §5 de `visao-geral.md`
- **Resultado:** roda nos **1.045** arquivos DS/DSS do acervo, não só num exemplo.
  Os 36 ODC são recusados de propósito — outro layout, ver `formato-bruto.md` §1.1.

### Semana 6 — Teste do parser — ✅ [12/09/2026](entregas/semana-06-teste-parser.md)
- [x] `tests/test_parser_direto.py`: conferir nº de linhas, nomes de coluna e um valor
      específico que você checou à mão no arquivo original
- **Entregável:** `uv run pytest` verde
- **Resultado:** 19 testes. Valores conferidos à mão em dois arquivos — um sintético com
  números redondos e o NT 1149 do acervo.

### Semana 7 — Extrair os metadados do cabeçalho — ✅ [12/09/2026](entregas/semana-07-metadados.md) (junto com a 5)
- [x] Ler do cabeçalho: identificação da amostra, data, dimensões do corpo de prova
- **Entregável:** função devolvendo um dicionário de metadados — saiu como a dataclass
  `direto.Metadados`, que o type checker confere e um dicionário não conferiria.
- **Correção ao plano:** a **tensão normal não está no cabeçalho**. Ela é uma coluna de
  dados, medida a cada leitura, e o ID do ensaio que parece anunciá-la mente às vezes
  (`formato-bruto.md` §5.5). Sai do cabeçalho e vira trabalho da rotina de qualidade.

> **Três semanas de folga.** A Fase 1 estava dimensionada para um formato desconhecido; ele
> já está mapeado. Use a folga na rotina de qualidade (`formato-bruto.md` §5.4), que é o
> conteúdo do artigo, e não em adiantar a Semana 8.
>
> 🟡 **Feito em 12–13/09:** seis registros, cada número com seu script. Falta virar código
> testado — [ficha](entregas/folga-rotina-de-qualidade.md).

### Semana 8 — Parser do triaxial — ⛔ **bloqueada por falta de dado**
- [ ] Mesmo trabalho das semanas 5–7 aplicado ao arquivo do triaxial
- **Entregável:** parser + teste
- **Não há um único arquivo triaxial no acervo** (`visao-geral.md` §5.3). Parser escrito às
  cegas não pode ser testado, e o que não é testado não conta. Enquanto não chegar arquivo,
  gaste esta semana na rotina de qualidade.
- Se quiser destravar: peça um arquivo exportado da máquina triaxial, mesmo que de um ensaio
  antigo ou interrompido. Um arquivo basta para começar.

### Semana 9 — Folga / acabamento — 🟡 [parcial](entregas/semana-09-acabamento.md)
- [ ] Terminar o que atrasou; rodar os dois parsers em todos os arquivos que conseguir
      — o do direto já roda nos 1.045 arquivos; o do triaxial não existe
- **Mostrar ao orientador:** *marco 1* — "o sistema já lê os arquivos das duas máquinas"

## Fase 2 — Cálculos (10 semanas · 20h)

### Semanas 10–11 — Estudo: Bloco B
- [ ] Pinto (cap. resistência) + seção "Calculation" da ASTM D3080
- [ ] O "livro azul" de cisalhamento indicado pelo professor em 30/09 — primeiro descobrir
      qual é ([ata](../reunioes/2026-09-30-alinhamento.md))
- **Entregável:** `docs/arquitetura/formulas.md` com **toda** equação a implementar e suas unidades
- **Mostrar:** a lista de fórmulas — peça ao orientador para conferir. Este é o momento mais
  barato de descobrir que uma fórmula está errada.

### ~~Semana 12 — Tensões do cisalhamento direto~~ — fora do escopo
### ~~Semana 13 — Correção de área~~ — fora do escopo

A máquina já entrega σ, τ e a área corrigida prontos, nas colunas 5, 9 e 14
(`formato-bruto.md` §3). Não há força a converter nem área a corrigir. **Duas semanas
livres** — passe-as para a rotina de qualidade e para a Semana 14, que é onde está a
dificuldade real.

### Semana 14 — Identificação da ruptura — 🟡 [parcial](entregas/semana-14-ruptura.md)
- [ ] Localizar o pico de τ e o valor residual na curva
- [x] Critério de não-ruptura: curva sem pico é reprovada (13/09, em script)
- [x] Onde ler o τ: **a 10 mm de deslocamento**, como o laboratório (29/09, em script)
- [ ] Função em `src/geotec/nucleo/` que reduz o ensaio a (σ, τ a 10 mm), com teste

### Semana 15 — Estudo: Bloco C (matplotlib) — ✅ [13/09/2026](entregas/semana-15-figuras.md)
- **Entregável:** curva τ × deslocamento salva como PNG

### Semanas 16–17 — Envoltória de Mohr-Coulomb — 🟡 [parcial](entregas/semanas-16-17-envoltoria.md)
- [ ] Regressão linear sobre os pontos (σ, τ) de ruptura → **c** e **φ** — feita em script para
      a série D1N (29/09: c = 22,6 kPa, φ = 32,2°); falta a função em `nucleo/`
- [ ] Teste com um conjunto de pontos de resposta conhecida
- **Mostrar:** *marco 2* — "o sistema calcula c e φ sozinho"

### Semanas 18–19 — Triaxial
- [ ] Tensões principais, deformação axial, correção de área, círculos de Mohr

## Fase 3 — Banco de dados (6 semanas · 12h)

- **Semana 20** — Estudo: Bloco D (SQLBolt, lições 1–12)
- **Semana 21** — Desenhar o schema em Markdown, sem escrever código. Validar com o orientador
- **Semana 22** — Estudo: SQLAlchemy Core
- **Semana 23** — Criar as tabelas em SQLite
- **Semana 24** — Rotina de ingestão: parser → banco
- **Semana 25** — Rotina de leitura: banco → DataFrame. *Marco 3*

## Fase 4 — Relatório (6 semanas · 12h)

- **Semana 26** — Esboçar o relatório **no papel**: que páginas, que gráficos, que tabelas
- **Semana 27** — Página 1: identificação do ensaio e do corpo de prova
- **Semana 28** — Página 2: curvas do ensaio
- **Semana 29** — Página 3: envoltória, c e φ
- **Semana 30** — Juntar tudo com `PdfPages`
- **Semana 31** — CLI: `uv run processar <arquivo>` → PDF pronto. *Marco 4: sistema completo*

## Fase 5 — Validação (5 semanas · 10h)

- **Semana 32** — Conseguir com o orientador ≥3 ensaios já processados manualmente
- **Semanas 33–34** — Rodar o sistema neles e tabular automático × manual
- **Semana 35** — Estatística descritiva: erro absoluto e relativo em c e φ
- **Semana 36** — Gráficos e discussão dos desvios. *Marco 5*

## Fase 6 — Escrita (8 semanas · 16h) + 4 semanas de folga

- **Semanas 37–38** — Relatório de acompanhamento do PIBITI
- **Semanas 39–44** — Artigo científico (uma seção por semana: métodos → resultados →
  discussão → introdução → conclusão → revisão)
- **Semanas 45–46** — Slides e apresentação
- **Semanas 47–48** — Folga. Vai precisar.

---

## Se atrasar

A 2h/semana, atrasos são certos. Ordem de corte, do primeiro a ser sacrificado ao último:

1. GUI desktop — já está fora
2. Triaxial (semanas 18–19) — entregar **só o cisalhamento direto**, completo e validado,
   é um PIBITI melhor do que os dois pela metade
3. MySQL — ficar em SQLite e justificar a escolha no relatório
4. Círculos de Mohr — a envoltória já entrega c e φ

**Nunca** corte: os parsers, o cálculo de c e φ, a validação e o artigo. É esse o trabalho.
