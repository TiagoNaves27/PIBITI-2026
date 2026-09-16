# Apresentações

Slides feitos a partir dos registros e da documentação do projeto, para reuniões com o
orientador e outras apresentações.

## Como funciona

- **Um arquivo `.html` por apresentação**, nomeado `AAAA-MM-DD-assunto.html`, com a data em
  que a apresentação foi feita — mesma lógica de `docs/registros/`.
- **Abrir localmente no navegador.** Os slides usam as figuras de `docs/registros/figuras/`
  por caminho relativo, então precisam do repositório ao lado — não funcionam se o `.html`
  for movido ou aberto isolado.
- **Navegação:** seta `←`/`→`, espaço, `Home`/`End`, ou clique nas bordas laterais da tela.
- **Cada apresentação abaixo tem sua tabela de referências**, slide a slide: de qual registro
  ou documento cada slide tirou frase, número ou figura. Servem para uma coisa só — quando um
  registro for corrigido (o `2026-09-12-triagem-do-acervo.md` já avisa que os 914 podem
  cair para menos, por exemplo), a tabela diz exatamente quais slides precisam ser revistos.

## O que não entra aqui

- Os registros em si — ficam em `docs/registros/`, e são a fonte. Um slide nunca é a
  referência de outro slide; a referência é sempre o registro ou documento original.
- Apresentação com número que não vem de um registro ou de `docs/arquitetura/` — todo
  número citado num slide tem que dar para rastrear até o mesmo lugar que os registros
  já rastreiam.

## As apresentações

| Data | Apresentação |
| --- | --- |
| 16/09/2026 | [Reunião de alinhamento](2026-09-16-reuniao-alinhamento.html) |

---

## Reunião de alinhamento — 16/09/2026

| # | Slide | Referência |
| --- | --- | --- |
| 1 | Reunião de alinhamento | — (abertura, sem número) |
| 2 | Resultado primeiro | `docs/arquitetura/perguntas-orientador.md` §Abertura |
| 3 | Agenda | — (estrutural, resume os slides 4 a 15) |
| 4 | Mudança de escopo | `docs/registros/2026-09-12-mudanca-de-escopo.md` |
| 5 | O acervo, em números | `docs/registros/2026-09-12-mudanca-de-escopo.md`; `docs/registros/2026-09-12-triagem-do-acervo.md` |
| 6 | Triagem do acervo | `docs/registros/2026-09-12-triagem-do-acervo.md` (texto e figura) |
| 7 | Os 129 descartados | `docs/registros/2026-09-12-triagem-do-acervo.md` |
| 8 | Ensaios travados | `docs/registros/2026-09-12-ensaios-travados.md` (texto e figura) |
| 9 | O filtro e os três casos | `docs/registros/2026-09-12-ensaios-travados.md` |
| 10 | Forma da curva vs. magnitude | `docs/registros/2026-09-12-forma-da-curva.md` (texto e figura); NT 608 vem de `docs/registros/2026-09-12-ensaios-travados.md` |
| 11 | O formato do ID | `docs/registros/2026-09-12-id-nao-e-dado.md` — reescrito para não repetir as hipóteses de decodificação do registro, só a conclusão de que não há padrão e o plano de criar um |
| 12 | Dois layouts silenciosos | `docs/registros/2026-09-13-dois-layouts.md` |
| 13 | Síntese | os cinco registros dos slides 6 a 12, listados acima |
| 14 | Repositório no GitHub | sem registro — captura de tela do README do repositório (`docs/apresentacoes/figuras/repositorio-github.png`) como evidência de que já está publicado e em uso |
| 15 | Obrigado | — (fechamento) |

**Nota sobre o slide 10.** O registro `2026-09-12-forma-da-curva.md` já trata "NT 296 é
solo-cimento" como leitura a partir do identificador, não fato confirmado — o slide mantém
essa mesma ressalva, explícita no texto e na legenda da figura.
