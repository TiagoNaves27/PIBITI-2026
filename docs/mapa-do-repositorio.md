# Mapa do repositório

_Última atualização: 13/09/2026_

Onde cada coisa mora. Serve para responder "em que arquivo estava aquilo?" sem ter que abrir
pasta por pasta.

## Onde procurar o quê

| Estou procurando… | Está em |
| --- | --- |
| o que fazer **nesta semana** | [`docs/plano/metas-semanais.md`](plano/metas-semanais.md) |
| **links** dos cursos e livros para estudar | [`docs/plano/roteiro-estudos.md`](plano/roteiro-estudos.md) |
| o que o projeto **é hoje** (decisões vigentes) | [`docs/arquitetura/visao-geral.md`](arquitetura/visao-geral.md) |
| como são os **arquivos das máquinas** (colunas, separador, codificação) | [`docs/arquitetura/formato-bruto.md`](arquitetura/formato-bruto.md) |
| o que **perguntar ao orientador** na reunião | [`docs/arquitetura/perguntas-orientador.md`](arquitetura/perguntas-orientador.md) |
| significado de um **termo** que apareceu | [`docs/glossario.md`](glossario.md) |
| as **descobertas** do projeto, com número e figura | [`docs/registros/`](registros/) |
| o **relatório semanal** para o orientador | [`docs/diario/`](diario/) — copie o `MODELO.md` |
| o documento **submetido ao PIBITI** | [`docs/plano/PlanoTrabalho-PIBITI_4.md`](plano/PlanoTrabalho-PIBITI_4.md) |
| o **script** que gerou um número citado | [`scripts/`](../scripts) |

O [`README.md`](../README.md) da raiz já traz os quatro primeiros como tabela de links — é o
primeiro lugar para abrir quando a memória falhar.

## O que não está em pasta nenhuma

Algumas páginas do projeto são **Artifacts**: HTML publicado e hospedado no claude.ai, com
link próprio. Não são arquivos deste repositório e procurar por elas nas pastas não acha —
por isso ficam registradas aqui.

| Página | Publicada em |
| --- | --- |
| [Próximas quatro semanas](https://claude.ai/code/artifact/364f48f1-a2db-4fa3-b50c-f38fb7e9302a) — plano de 14/09 a 11/10, reunião e alvos | 13/09/2026 |
| [Bancada PIBITI](https://claude.ai/code/artifact/46ec1a79-dc82-4ada-8fce-fa185a9cf4a3) — o painel das 48 semanas | 13/09/2026 |
| [Roteiro da reunião](https://claude.ai/code/artifact/04f0da7c-37d6-48e5-ae04-a31ce173001b) | 12/09/2026 |
| [Do ensaio ao gráfico](https://claude.ai/code/artifact/7167a3d4-3f87-44a4-9966-7b8561513691) | 02/09/2026 |
| [PIBITI Cisalhamento IoT](https://claude.ai/code/artifact/3c11e075-5d13-47a7-99d5-ef4b44b2c76c) | 02/09/2026 |

Para listar todos sem sair do terminal: `/artifacts`. A galeria completa fica em
<https://claude.ai/code/artifacts>.

O conteúdo dessas páginas é derivado dos documentos de `docs/` — quando as duas coisas
divergirem, o repositório é que vale.

## As pastas, uma a uma

### `docs/` — tudo que é texto

Dividida por finalidade, não por assunto:

- **`plano/`** — o que se pretende fazer.
  - `metas-semanais.md`: o backlog, dividido em fases, cada semana com uma sessão de 2h e um
    entregável. É aqui que se marca `[x]`.
  - `roteiro-estudos.md`: os blocos de estudo (pandas, resistência ao cisalhamento, …), cada
    um amarrado à semana em que o assunto é usado. **Os links de curso, documentação e livro
    online estão todos aqui.**
  - `PlanoTrabalho-PIBITI_4.md`: o documento oficial submetido. Histórico — não se edita.
- **`arquitetura/`** — o que o projeto é.
  - `visao-geral.md`: estado real e decisões vigentes. **Prevalece sobre o plano** quando os
    dois divergirem.
  - `formato-bruto.md`: a anatomia dos arquivos das máquinas, levantada a partir dos 1.081
    arquivos de `dados/Ensaios-270/`.
  - `perguntas-orientador.md`: preparação de reunião.
- **`registros/`** — o que se descobriu. Um arquivo por episódio, nomeado
  `AAAA-MM-DD-assunto.md`, com título em forma de afirmação. A pasta se ordena sozinha e vira
  a linha do tempo do projeto. As regras estão no `README.md` de lá; as imagens, em
  `figuras/`, geradas por script.
- **`diario/`** — o que se fez em cada semana, cronológico, para o orientador. Copie
  `MODELO.md` para `AAAA-MM-DD.md` no fim de cada semana.
- **`glossario.md`** — os termos já explicados, com o exemplo concreto do projeto onde cada
  um apareceu.
- **`relatorios/`** e **`artigo/`** — vazias por enquanto, reservadas para as saídas finais.

### `scripts/` — utilitários de linha de comando

Um arquivo por pergunta respondida. Todo número citado em registro vem de um destes, e
qualquer um pode ser rodado de novo para conferir:

| Script | Responde |
| --- | --- |
| `inspecionar.py` | como é este arquivo bruto? (codificação, separador, colunas) |
| `triagem_acervo.py` | quantos ensaios do acervo são utilizáveis |
| `comparar_layouts.py` | quais arquivos são de cada um dos dois layouts |
| `ensaios_nao_rompidos.py` | quais ensaios não chegaram a romper |
| `id_versus_sigma.py` | o identificador do ensaio bate com a tensão normal? |
| `razao_tau_sigma.py` | a razão τ/σ de cada ensaio |
| `figura_*.py` | as figuras dos registros |

Todos se rodam igual: `uv run python scripts/<nome>.py`.

### `src/geotec/` — o código do sistema

Uma subpasta por etapa do fluxo `arquivo bruto → parser → banco → cálculo → relatório`:

`coleta/` busca os arquivos gerados pelas máquinas · `parsers/` traduz cada formato para o
formato normalizado (um módulo por máquina — hoje só `direto.py`) · `banco/` schema e
ingestão · `nucleo/` os cálculos (tensões, Mohr-Coulomb) · `relatorio/` gráficos e PDF ·
`io/` leitura e exportação · `app/` interface, adiada.

A maioria ainda só tem o `__init__.py` — a pasta existe para o lugar de cada coisa já estar
decidido.

### `dados/` — os arquivos de ensaio

- `Ensaios-270/` — o acervo, 1.081 arquivos separados em `Cisalhamento`, `Adensamento` e
  `DSS`. **Versionado** (36 MB, fonte primária, não editar) — é a exceção declarada no
  `.gitignore`.
- `brutos/` e `processados/` — de trabalho, **não** versionadas.
- `exemplos/bruto/` — arquivos pequenos de exemplo, versionados.

### `tests/` — testes automatizados

`test_parser_direto.py` e `test_smoke.py`, mais `tests/dados/` com um arquivo de ensaio
inventado, pequeno, só para os testes rodarem sem depender do acervo.

### `referencias/`

`biblioteca.bib` (as citações, versionado) e `pdfs/` (os arquivos, **não** versionados por
direitos autorais e tamanho).

### Na raiz

`README.md` (porta de entrada) · `CLAUDE.md` (as convenções do projeto) · `pyproject.toml` e
`uv.lock` (dependências) · `.env.example` (modelo das credenciais do banco; o `.env` de
verdade nunca é versionado) · `.gitignore` (o que o Git deve ignorar).
