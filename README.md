# PIBIC 2026 — Aquisição (IoT) e análise de ensaios de cisalhamento direto e triaxial

Sistema automatizado de aquisição e análise de dados dos ensaios de cisalhamento direto e
compressão triaxial, composto por três partes:

**sensores → Raspberry Pi (aquisição) → MySQL (armazenamento) → app desktop Python (análise)**

- **Aluno:** Tiago Naves de Oliveira Alves
- **Grupo:** GeoFluxo — Universidade de Brasília
- **Plano de trabalho:** [`docs/plano/PlanoTrabalho-PIBIC_4.md`](docs/plano/PlanoTrabalho-PIBIC_4.md)

> ⚠️ O plano de trabalho é o documento submetido ao PIBIC. O escopo real evoluiu desde então —
> o que vale como estado atual está em [`docs/arquitetura/visao-geral.md`](docs/arquitetura/visao-geral.md).

## Estrutura

```
docs/            plano, arquitetura, diário semanal, relatórios, artigo
referencias/     biblioteca.bib + PDFs (não versionados)
src/geotec/
  aquisicao/     leitura dos sensores no Raspberry Pi, calibração
  banco/         schema MySQL, modelos e ingestão
  nucleo/        cálculos: tensões, curvas, Mohr-Coulomb, círculos de Mohr
  io/            leitura/exportação de arquivos de ensaio
  app/           aplicativo desktop
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

No Raspberry Pi, incluir as dependências de hardware:

```bash
uv sync --extra pi
```

## Banco de dados

Copie `.env.example` para `.env` e preencha as credenciais do MySQL. O arquivo `.env`
não é versionado.
