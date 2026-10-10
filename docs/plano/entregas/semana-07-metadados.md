# Semana 7 — Extrair os metadados do cabeçalho

> ✅ **Concluída em 12/09/2026**, junto com a Semana 5 · Fase 1

| Quando | Commits | Entregável |
| --- | --- | --- |
| 12/09/2026 | `bf40913` | dataclass `direto.Metadados` |

## O que a meta pedia

Ler do cabeçalho a identificação da amostra, a data e as dimensões do corpo de prova, numa
função que devolve um dicionário.

## O que foi feito

- Os metadados saem numa dataclass, `direto.Metadados`, em vez de dicionário: o type checker
  confere o nome de cada campo, e um dicionário não conferiria.
- Dimensões convertidas de mm para m na leitura (SI internamente).

## Como conferir

```bash
uv run pytest -k metadados
```

## O que mudou em relação ao plano

A **tensão normal não está no cabeçalho**: é uma coluna de dados, medida a cada leitura. E o
ID do ensaio, que parece anunciá-la, erra em seis casos. Ela saiu desta meta e virou trabalho
da rotina de qualidade.

## Ligações

- [Registro: o ID não é dado](../../registros/2026-09-12-id-nao-e-dado.md)
- [`formato-bruto.md`](../../arquitetura/formato-bruto.md) §5.5
