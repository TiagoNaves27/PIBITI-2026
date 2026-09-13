# PIBITI 2026 — Aquisição (IoT) e análise de ensaios de cisalhamento direto e triaxial

Sistema automatizado de coleta e análise de dados dos ensaios de cisalhamento direto e
compressão triaxial. As máquinas do laboratório já gravam os dados; o sistema os traduz,
armazena, calcula os parâmetros de resistência e gera um relatório.

**arquivo bruto da máquina → parser → banco → cálculo (c, φ) → relatório PDF**

- **Aluno:** Tiago Naves de Oliveira Alves
- **Grupo:** GeoFluxo — Universidade de Brasília

| Documento | Para quê |
| --- | --- |
| [`docs/arquitetura/visao-geral.md`](docs/arquitetura/visao-geral.md) | **estado real** do projeto — vale sobre o plano |
| [`docs/plano/metas-semanais.md`](docs/plano/metas-semanais.md) | o que fazer nesta semana (2h) |
| [`docs/plano/roteiro-estudos.md`](docs/plano/roteiro-estudos.md) | o que estudar e quando |
| [`docs/plano/PlanoTrabalho-PIBITI_4.md`](docs/plano/PlanoTrabalho-PIBITI_4.md) | documento submetido ao PIBITI (histórico) |
| [`docs/mapa-do-repositorio.md`](docs/mapa-do-repositorio.md) | onde cada coisa mora — tour pelas pastas |

> ⚠️ O plano de trabalho previa aquisição via Raspberry Pi. Isso **saiu do escopo**: as
> máquinas já digitalizam os dados. Ver `visao-geral.md` §1.

## Descobrir o formato de um arquivo bruto

```powershell
uv run python scripts/inspecionar.py dados/exemplos/bruto/ensaio.csv
```

Reporta codificação, separador, tamanho do cabeçalho, colunas e o comando `pd.read_csv`
correspondente.

## Estrutura

```
docs/            plano, arquitetura, diário semanal, relatórios, artigo
referencias/     biblioteca.bib + PDFs (não versionados)
src/geotec/
  coleta/        busca dos arquivos gerados pelas máquinas
  parsers/       tradução bruto → formato normalizado (um módulo por máquina)
  banco/         schema, modelos e ingestão
  nucleo/        cálculos: tensões, curvas, Mohr-Coulomb, círculos de Mohr
  relatorio/     gráficos e PDF
  io/            leitura/exportação de arquivos
  app/           interface (adiada — ver visao-geral.md §7)
notebooks/       exploração e validação
dados/           brutos / processados / exemplos (versionados só os exemplos)
tests/           testes automatizados
scripts/         utilitários de linha de comando
```

## Ambiente

```powershell
uv sync                 # cria .venv e instala dependências
uv run pytest           # roda os testes
uv run ruff check .     # lint
```

## Banco de dados

Durante o desenvolvimento, SQLite (arquivo local, sem configuração). Na entrega, MySQL —
copie `.env.example` para `.env` e preencha as credenciais. O `.env` não é versionado.
