# Semanas 16–17 — Envoltória de Mohr-Coulomb

> 🟡 **Parcial** — a regressão foi feita para a série D1N, em script; falta a função do sistema
> com teste de resposta conhecida · Fase 2 · *marco 2* ainda não

| Quando | Commits | Entregável |
| --- | --- | --- |
| 29/09/2026 | `87f6142`, `7d70b5b` | envoltória da série D1N |

## O que a meta pedia

Regressão linear sobre os pontos (σ, τ) de ruptura, dando **c** e **φ**, com teste num
conjunto de pontos de resposta conhecida. Marco 2: "o sistema calcula c e φ sozinho".

## O que foi feito

- Envoltória da série D1N com τ a 10 mm: **c = 22,6 kPa, φ = 32,2°, R² = 0,980**, 7 pontos.
- Mostrado que os filtros mudam tudo: sem o de não-ruptura, a mesma série dá φ = 5,1° e
  R² = 0,001.

## Como conferir

```bash
uv run python scripts/apoio_apresentacao.py variantes
```

## O que falta

- [ ] Função em `src/geotec/nucleo/` que recebe os pares (σ, τ) e devolve c, φ e R², em SI e
      radianos
- [ ] Teste com pontos de resposta conhecida, de livro ou norma
- [ ] Rodar em todas as séries — **travado pela Q1** (a regra de agrupamento), que só o
      laboratório responde

## Ligações

- [Registro: envoltória D1N](../../registros/2026-09-29-envoltoria-d1n.md)
- [Registro: τ a 10 mm](../../registros/2026-09-29-ruptura-a-10mm.md)
- [`visao-geral.md`](../../arquitetura/visao-geral.md) §3 — o bloqueio do agrupamento
