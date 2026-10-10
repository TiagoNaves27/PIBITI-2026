# Semana 14 — Identificação da ruptura

> 🟡 **Parcial** — o critério foi descoberto e usado em script; falta virar função do sistema
> com teste · Fase 2

| Quando | Commits | Entregável |
| --- | --- | --- |
| 13/09/2026 e 29/09/2026 | `5491142`, `7d70b5b` | critério de não-ruptura e τ lido a 10 mm |

## O que a meta pedia

Localizar o pico de τ e o valor residual na curva.

## O que foi feito

- **13/09 — quem não rompeu sai.** Ensaio cuja curva só sobe e para, sem pico, é reprovado
  pela forma, não pela magnitude. Pegou três ensaios travados no acervo.
- **29/09 — onde ler o τ.** O laboratório lê τ **a 10 mm de deslocamento**, não no máximo da
  curva. Isso respondeu a pergunta Q4 e virou o critério do projeto.

## Como conferir

```bash
uv run python scripts/ensaios_nao_rompidos.py
uv run python scripts/apoio_apresentacao.py acervo-10mm
```

## O que mudou em relação ao plano

O plano pedia pico e residual. O critério que vale é outro — τ a 10 mm —, e o residual não foi
usado até agora.

## O que falta

- [ ] Função em `src/geotec/nucleo/` que reduz um ensaio ao par (σ, τ a 10 mm), com teste de
      valor conferido à mão
- [ ] O filtro de não-ruptura também como função testada

## Ligações

- [Registro: τ a 10 mm](../../registros/2026-09-29-ruptura-a-10mm.md)
- [Registro: ensaios travados](../../registros/2026-09-12-ensaios-travados.md)
