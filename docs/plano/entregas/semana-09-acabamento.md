# Semana 9 — Folga / acabamento

> 🟡 **Parcial** — o parser do direto roda no acervo inteiro; o do triaxial não existe ·
> Fase 1 · *marco 1* pela metade

| Quando | Commits | Entregável |
| --- | --- | --- |
| 12/09/2026 | `bf40913` | parser rodado em 1.045 arquivos |

## O que a meta pedia

Terminar o que atrasou e rodar os dois parsers em todos os arquivos. Marco 1: "o sistema já
lê os arquivos das duas máquinas".

## O que foi feito

- O parser do cisalhamento direto lê todos os 1.045 arquivos DS e DSS do acervo.

## Como conferir

```bash
uv run python scripts/parser_no_acervo.py
```

## O que falta

- [ ] Parser do triaxial (Semana 8), bloqueado até chegar um arquivo da máquina
- [ ] Com ele, o marco 1 completo

## Ligações

- [Semana 1](semana-01-laboratorio.md) — de onde viria o arquivo triaxial
