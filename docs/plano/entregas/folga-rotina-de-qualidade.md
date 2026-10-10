# Folga da Fase 1 — Rotina de qualidade

> 🟡 **Parcial** — as regras foram descobertas e documentadas em registros, com script; ainda
> não viraram código do sistema · Fase 1

| Quando | Commits | Entregável |
| --- | --- | --- |
| 12–13/09/2026 | `6568116`, `5491142` | seis registros, cada número com seu script |

## O que a meta pedia

As metas mandam usar as três semanas de folga da Fase 1 (e as duas da Fase 2) na rotina de
qualidade de [`formato-bruto.md`](../../arquitetura/formato-bruto.md) §5.4 — "que é o
conteúdo do artigo".

## O que foi feito

| Registro | O que mostrou | Script |
| --- | --- | --- |
| [Triagem do acervo](../../registros/2026-09-12-triagem-do-acervo.md) | 914 dos 1.043 ensaios viram ponto de envoltória | `triagem_acervo.py` |
| [Ensaios travados](../../registros/2026-09-12-ensaios-travados.md) | três ensaios nunca romperam, e a conferência manual não perceberia | `ensaios_nao_rompidos.py` |
| [O ID não é dado](../../registros/2026-09-12-id-nao-e-dado.md) | em seis casos o ID anuncia a tensão normal errada | `id_versus_sigma.py` |
| [Forma da curva](../../registros/2026-09-12-forma-da-curva.md) | a maior razão τ/σ é de um ensaio bom: magnitude não separa nada | `razao_tau_sigma.py` |
| [Dois layouts](../../registros/2026-09-13-dois-layouts.md) | DS e ODC têm a mesma extensão e layouts diferentes | `comparar_layouts.py` |
| [Mudança de escopo](../../registros/2026-09-12-mudanca-de-escopo.md) | o projeto virou engenharia de dados | `comparar_layouts.py` |

## Como conferir

```bash
uv run python scripts/triagem_acervo.py
uv run python scripts/ensaios_nao_rompidos.py
```

Cada registro tem a sua seção "Como conferir" com o comando exato.

## O que falta

- [ ] Levar as regras para `src/geotec/` como funções testadas — hoje vivem em scripts avulsos
- [ ] Respostas do laboratório que afetam as regras: Q1 (agrupamento) e Q7 (os 108 arquivos
      com irmão), em [`perguntas-orientador.md`](../../arquitetura/perguntas-orientador.md)

## Ligações

- [`docs/registros/`](../../registros/)
