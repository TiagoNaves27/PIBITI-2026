# Entregas

Uma ficha por meta de [`metas-semanais.md`](../metas-semanais.md) que já andou: **quando** foi
feita, **o que** foi feito e **como conferir**. As metas dizem o que se pretende; as entregas,
o que de fato aconteceu.

## Como funciona

- **Um arquivo por meta**, nomeado pelo número da semana do plano: `semana-05-parser-direto.md`,
  `semanas-16-17-envoltoria.md`. O número é o do plano, não o do calendário — assim a pasta se
  ordena na mesma sequência das metas.
- **Para começar, copiar [`MODELO.md`](MODELO.md).** A primeira linha é sempre a situação e a
  data, para que se saiba o estado da meta sem ler o resto.
- **Ficha nasce quando a meta anda**, não só quando termina. Uma meta parcial tem ficha, com a
  seção "O que falta" preenchida; quando terminar, a ficha é atualizada e a data de conclusão
  entra no topo.
- **Data é a do commit.** Cada ficha cita os commits que a sustentam (`git show <hash>` mostra o
  que mudou). O que não deixou rastro no repositório não conta como feito.
- **Lida em um minuto.** O porquê das descobertas fica em [`docs/registros/`](../../registros/);
  a ficha só aponta para lá.
- **Ao fechar ou avançar uma meta**, atualizar no mesmo commit: a ficha, a tabela abaixo e o
  título da semana em `metas-semanais.md`.

Situações: ✅ concluída · 🟡 parcial · ⛔ bloqueada.

## O que não entra aqui

- **O relatório semanal para o orientador** — fica em [`docs/diario/`](../../diario/), por
  semana do calendário. Uma semana do calendário pode avançar várias metas, e uma meta pode
  levar várias semanas.
- **O que o professor pediu** — fica em [`docs/reunioes/`](../../reunioes/).

---

## As entregas

_Atualizado em 10/10/2026._

| Meta | Situação | Quando | Entregável |
| --- | --- | --- | --- |
| [Semana 1 — Ir ao laboratório](semana-01-laboratorio.md) | 🟡 parcial | 12/09/2026 | acervo de 1.081 arquivos; falta o triaxial e as perguntas sobre as máquinas |
| [Semana 2 — Entender o arquivo](semana-02-formato-bruto.md) | ✅ | 12/09/2026 | `formato-bruto.md` |
| [Semanas 3 e 4 — Estudo de pandas](semanas-03-04-estudo-pandas.md) | 🟡 parcial | 12/09/2026 | entregável coberto pelo parser; estudo sem registro |
| [Semana 5 — Parser do cisalhamento direto](semana-05-parser-direto.md) | ✅ | 12/09/2026 | `src/geotec/parsers/direto.py` |
| [Semana 6 — Teste do parser](semana-06-teste-parser.md) | ✅ | 12/09/2026 | `tests/test_parser_direto.py`, 19 testes |
| [Semana 7 — Metadados do cabeçalho](semana-07-metadados.md) | ✅ | 12/09/2026 | `direto.Metadados` |
| [Folga da Fase 1 — Rotina de qualidade](folga-rotina-de-qualidade.md) | 🟡 parcial | 12–13/09/2026 | seis registros e seus scripts; ainda não é código do sistema |
| Semana 8 — Parser do triaxial | ⛔ bloqueada | — | sem arquivo triaxial no acervo |
| [Semana 9 — Folga / acabamento](semana-09-acabamento.md) | 🟡 parcial | 12/09/2026 | parser rodado nos 1.045 DS/DSS; falta o triaxial |
| [Semana 14 — Identificação da ruptura](semana-14-ruptura.md) | 🟡 parcial | 13/09 e 29/09/2026 | critério de não-ruptura e τ a 10 mm, em script |
| [Semana 15 — Curva em PNG](semana-15-figuras.md) | ✅ | 13/09/2026 | figuras de `docs/registros/figuras/` |
| [Semanas 16–17 — Envoltória](semanas-16-17-envoltoria.md) | 🟡 parcial | 29/09/2026 | envoltória D1N em script; falta o código com teste |

**Fora das metas**, no mesmo período: a reunião de alinhamento de 30/09, com a
[apresentação](../../apresentacoes/) preparada desde 16/09 e a
[ata](../../reunioes/2026-09-30-alinhamento.md);
o [glossário](../../glossario.md); a troca de paleta para Swiss Modern (29/09).
