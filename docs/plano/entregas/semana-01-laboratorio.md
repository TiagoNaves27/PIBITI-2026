# Semana 1 — Ir ao laboratório

> 🟡 **Parcial** — os arquivos de cisalhamento direto chegaram; falta o triaxial e o que se
> pretendia anotar sobre as máquinas · Fase 0

| Quando | Commits | Entregável |
| --- | --- | --- |
| 12/09/2026 | `7039a9e` | `dados/Ensaios-270/`, 1.081 arquivos |

## O que a meta pedia

Anotar marca, modelo e software das máquinas; exportar um arquivo bruto de cada ensaio
(direto e triaxial); descobrir como os arquivos são acessados pela rede.

## O que foi feito

- Em vez de um arquivo de exemplo, veio o **acervo inteiro** do laboratório: 1.081 arquivos,
  separados em `Cisalhamento` (1.043), `Adensamento` (36) e `DSS` (2).

## Como conferir

```bash
uv run python scripts/parser_no_acervo.py
```

## O que mudou em relação ao plano

O acervo substituiu o "um arquivo de cada" com folga para o cisalhamento direto — 1.043 em
vez de um. Mas não trouxe nenhum arquivo triaxial.

## O que falta

- [ ] Um arquivo exportado da máquina triaxial — é o que trava a Semana 8
- [ ] Marca, modelo e software de cada máquina
- [ ] Como os arquivos são acessados pela rede (pasta compartilhada? FTP? nuvem?)

## Ligações

- [`formato-bruto.md`](../../arquitetura/formato-bruto.md) — o que o acervo revelou
- [`visao-geral.md`](../../arquitetura/visao-geral.md) §5.3 — a ausência do triaxial
