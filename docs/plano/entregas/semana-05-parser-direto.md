# Semana 5 — Parser do cisalhamento direto

> ✅ **Concluída em 12/09/2026** · Fase 1

| Quando | Commits | Entregável |
| --- | --- | --- |
| 12/09/2026 | `bf40913` | [`src/geotec/parsers/direto.py`](../../../src/geotec/parsers/direto.py) |

## O que a meta pedia

Uma função que recebe o caminho do arquivo e devolve um DataFrame normalizado, funcionando no
arquivo de exemplo.

## O que foi feito

- `direto.ler(caminho)` devolve um `Ensaio`: metadados mais a série de leituras, tudo em SI,
  com as colunas do §5 de `visao-geral.md`.
- Roda em **todos os 1.045 arquivos** DS e DSS do acervo, não só num exemplo.
- Recusa com erro (`ErroDeFormato`) o que não é dele — os 36 ODC, arquivo renomeado, coluna
  trocada — em vez de ler errado em silêncio.

## Como conferir

```bash
uv run python scripts/parser_no_acervo.py
```

Deve imprimir 1.045 lidos (1.043 DS + 2 DSS) e 36 recusados, todos ODC.

## O que mudou em relação ao plano

Foi além: o plano pedia um arquivo de exemplo, e o parser foi validado no acervo inteiro.

## Ligações

- [Semana 6 — Teste do parser](semana-06-teste-parser.md)
- [Registro: dois layouts](../../registros/2026-09-13-dois-layouts.md) — por que recusar o ODC
