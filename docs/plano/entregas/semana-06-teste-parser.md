# Semana 6 — Teste do parser

> ✅ **Concluída em 12/09/2026** · Fase 1

| Quando | Commits | Entregável |
| --- | --- | --- |
| 12/09/2026 | `bf40913` | [`tests/test_parser_direto.py`](../../../tests/test_parser_direto.py) |

## O que a meta pedia

Conferir número de linhas, nomes de coluna e um valor checado à mão no arquivo original;
`uv run pytest` verde.

## O que foi feito

- **19 testes**, com valores conferidos à mão em dois arquivos: um sintético com números
  redondos (`tests/dados/`) e o NT 1149, do acervo.
- Além do caminho feliz, testes de recusa: adensamento, nome fora do padrão, coluna
  renomeada, cabeçalho diferente, arquivo sem dados.

## Como conferir

```bash
uv run pytest
```

## O que mudou em relação ao plano

_Nada_ — saiu como planejado, com mais casos do que o pedido.

## Ligações

- [Semana 5 — Parser do cisalhamento direto](semana-05-parser-direto.md)
