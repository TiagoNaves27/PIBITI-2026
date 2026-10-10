# Semana 2 — Entender o arquivo

> ✅ **Concluída em 12/09/2026** · Fase 0 — falta só a conversa com o técnico, que fica como
> pendência

| Quando | Commits | Entregável |
| --- | --- | --- |
| 12/09/2026 | `7039a9e`, `c0c5f8a` | [`formato-bruto.md`](../../arquitetura/formato-bruto.md) |

## O que a meta pedia

Documentar separador, codificação, tamanho do cabeçalho, nome e unidade de cada coluna.

## O que foi feito

- `formato-bruto.md` escrito a partir dos 1.081 arquivos, não de um só: CSV, separador `;`,
  decimal com vírgula, UTF-8 com BOM, 7 linhas de cabeçalho e 17 colunas — idêntico nos 1.043
  arquivos de cisalhamento direto.
- Descoberto que existem **dois layouts** com a mesma extensão: os ODC de adensamento têm 9
  linhas de cabeçalho e outras colunas (§1.1).
- A análise de qualidade dos dados foi reescrita no mesmo dia (`c0c5f8a`), e virou o ponto de
  partida da rotina de qualidade.

## Como conferir

```bash
uv run python scripts/inspecionar.py "dados/Ensaios-270/Cisalhamento/<arquivo>.csv"
uv run python scripts/comparar_layouts.py
```

## O que mudou em relação ao plano

O significado das colunas foi documentado a partir dos próprios arquivos e ainda não foi
confirmado com o técnico.

## O que falta

- [ ] Confirmar com o técnico do laboratório o significado de cada coluna

## Ligações

- [Registro: dois layouts](../../registros/2026-09-13-dois-layouts.md)
