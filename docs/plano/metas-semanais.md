# Metas semanais

_Última atualização: 11/09/2026_

**Orçamento real: 2h por semana ≈ 96h no ano.** Cada meta abaixo cabe em **uma sessão de
2 horas** e termina em algo concreto que dá para mostrar. Semana sem entregável é semana
que some sem deixar rastro.

**Regra:** se uma meta não couber em 2h, ela está mal dividida — quebre em duas, não
transforme a semana em 4h.

Ao fim de cada semana, copie `docs/diario/MODELO.md` para `docs/diario/AAAA-MM-DD.md` e
preencha. Esse arquivo é o que você manda para o orientador.

---

## Fase 0 — Descoberta (3 semanas · 6h)

> Objetivo: descobrir o formato dos dados. **Todo o resto do projeto está travado aqui.**

### Semana 1 — Ir ao laboratório
- [ ] Anotar marca, modelo e nome do software de cada máquina (direto e triaxial)
- [ ] Exportar **um arquivo bruto de cada ensaio** e salvar em `dados/exemplos/bruto/`
- [ ] Descobrir como os arquivos são acessados pela rede (pasta compartilhada? FTP? nuvem?)
- **Entregável:** 2 arquivos no repositório + as respostas do §3 de `visao-geral.md`
- **Mostrar ao orientador:** "consegui os arquivos brutos; o formato é X"

### Semana 2 — Entender o arquivo
- [ ] Rodar `uv run python scripts/inspecionar.py dados/exemplos/bruto/<arquivo>`
- [ ] Documentar em `docs/arquitetura/formato-bruto.md`: separador, codificação, tamanho do
      cabeçalho, nome e unidade de cada coluna
- [ ] Perguntar ao técnico do laboratório o que cada coluna significa
- **Entregável:** `formato-bruto.md` preenchido
- **Mostrar:** a tabela de colunas e unidades

### Semana 3 — Estudo: Bloco A, parte 1
- [ ] Kaggle Learn Pandas, lições 1–3 (link em `roteiro-estudos.md`)
- **Entregável:** um notebook em `notebooks/` que abre o arquivo bruto com `pd.read_csv`,
      mesmo que saia torto
- **Mostrar:** "já consigo abrir o arquivo no Python"

## Fase 1 — Tradução dos dados (6 semanas · 12h)

### Semana 4 — Estudo: Bloco A, parte 2
- [ ] Ler a docstring inteira de `pd.read_csv`; testar `skiprows`, `decimal`, `encoding`
- **Entregável:** notebook lendo o arquivo com as colunas certas e números como número
      (não como texto)

### Semana 5 — Parser do cisalhamento direto
- [ ] `src/geotec/parsers/direto.py`: função que recebe caminho e devolve DataFrame normalizado
- **Entregável:** a função funcionando no arquivo de exemplo
- **Mostrar:** DataFrame limpo, com as colunas do §5 de `visao-geral.md`

### Semana 6 — Teste do parser
- [ ] `tests/test_parser_direto.py`: conferir nº de linhas, nomes de coluna e um valor
      específico que você checou à mão no arquivo original
- **Entregável:** `uv run pytest` verde

### Semana 7 — Extrair os metadados do cabeçalho
- [ ] Ler do cabeçalho: identificação da amostra, data, tensão normal, dimensões do corpo de prova
- **Entregável:** função devolvendo um dicionário de metadados

### Semana 8 — Parser do triaxial
- [ ] Mesmo trabalho das semanas 5–7 aplicado ao arquivo do triaxial
- **Entregável:** parser + teste

### Semana 9 — Folga / acabamento
- [ ] Terminar o que atrasou; rodar os dois parsers em todos os arquivos que conseguir
- **Mostrar ao orientador:** *marco 1* — "o sistema já lê os arquivos das duas máquinas"

## Fase 2 — Cálculos (10 semanas · 20h)

### Semanas 10–11 — Estudo: Bloco B
- [ ] Pinto (cap. resistência) + seção "Calculation" da ASTM D3080
- **Entregável:** `docs/arquitetura/formulas.md` com **toda** equação a implementar e suas unidades
- **Mostrar:** a lista de fórmulas — peça ao orientador para conferir. Este é o momento mais
  barato de descobrir que uma fórmula está errada.

### Semana 12 — Tensões do cisalhamento direto
- [ ] `nucleo/cisalhamento_direto.py`: tensão normal e cisalhante a partir de força e área
- [ ] Teste com valor conferido à mão na calculadora

### Semana 13 — Correção de área
- [ ] Área corrigida em função do deslocamento (a norma define como)

### Semana 14 — Identificação da ruptura
- [ ] Localizar o pico de τ e o valor residual na curva

### Semana 15 — Estudo: Bloco C (matplotlib)
- **Entregável:** curva τ × deslocamento salva como PNG

### Semanas 16–17 — Envoltória de Mohr-Coulomb
- [ ] Regressão linear sobre os pontos (σ, τ) de ruptura → **c** e **φ**
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
