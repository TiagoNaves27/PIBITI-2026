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
  Nas apresentações a partir de 29/09/2026, também rolagem do mouse e deslizar o dedo.
- **Estilo:** Swiss Modern, desde 29/09/2026 — regras em [`ESTILO.md`](ESTILO.md). Para uma
  apresentação nova, copiar [`MODELO.html`](MODELO.html), que tem um exemplo de cada componente.
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
| 29/09/2026 | [Teste de design — Terra oficial](2026-09-29-teste-design-terra.html) e [Teste de design — GeoFluxo real](2026-09-29-teste-design-geofluxo.html) |
| 30/09/2026 | [**Reunião de alinhamento — Swiss Modern**](2026-09-30-reuniao-alinhamento.html) (versão a apresentar) · [roteiro de fala](2026-09-30-reuniao-alinhamento-roteiro.md) |

---

## Reunião de alinhamento — 30/09/2026 (Swiss Modern)

A versão a apresentar. Junta o conteúdo da reestruturação de 29/09 (abaixo) com slides novos
tirados direto dos registros — dois layouts, critério de não-ruptura, tabela dos seis
identificadores, maiores razões τ/σ — no estilo definido em `ESTILO.md`. O NT 608 continua fora.
Os gráficos são desenhados no próprio slide, a partir dos mesmos dados de
`scripts/apoio_apresentacao.py`; não usam os PNGs.

| # | Slide | Referência |
| --- | --- | --- |
| 1 | Abertura | — (título; o 914 do bloco vem de `2026-09-12-triagem-do-acervo.md`) |
| 2 | Resultado primeiro | `docs/arquitetura/perguntas-orientador.md` §Abertura e §Q1; `formato-bruto.md` §6 (51 é estimativa superior) |
| 3 | Agenda | — (estrutural) |
| 4 | Mudança de escopo | `docs/registros/2026-09-12-mudanca-de-escopo.md` |
| 5 | O acervo, em números | `2026-09-12-mudanca-de-escopo.md`; `2026-09-12-triagem-do-acervo.md` |
| 6 | Divisor: o que o acervo escondia | resume os slides 7 a 13 |
| 7 | Triagem do acervo | `2026-09-12-triagem-do-acervo.md` |
| 8 | Série D1N: as sete curvas e o τ a 10 mm | `2026-09-29-ruptura-a-10mm.md` (τ a 10 mm, c, φ, R²; valores por ensaio em `apoio_apresentacao.py curvas-d1n`); `2026-09-29-envoltoria-d1n.md` (série, NT 612, máximo: 24,0 kPa e 32,6°); NT 608 de `2026-09-12-ensaios-travados.md`. Curvas acima de 550 kPa ficam fora, por pedido do aluno (só exclui o NT 608) |
| 9 | O filtro em ação | `2026-09-12-ensaios-travados.md` (funil 914 → 3; NT 268 e NT 625); título a partir de `2026-09-29-ruptura-a-10mm.md` (o laboratório lê τ a 10 mm) |
| 10 | Forma, não magnitude | `2026-09-12-forma-da-curva.md`; razão 2× do NT 268 calculada de `2026-09-12-ensaios-travados.md` (794 / 399) |
| 11 | A envoltória que sobra | `docs/registros/2026-09-29-ruptura-a-10mm.md` (c, φ, R² e as variantes com τ a 10 mm); NT 614 de `2026-09-12-id-nao-e-dado.md` |
| 12 | O formato do ID | `2026-09-12-id-nao-e-dado.md`; plano de padronizar o ID vem da apresentação de 16/09 |
| 13 | Dois layouts | `2026-09-13-dois-layouts.md` |
| 14 | Citação | `2026-09-13-dois-layouts.md` §O que ficou em aberto |
| 15 | Síntese | os registros dos slides 7 a 13 |
| 16 | Repositório no GitHub | captura de tela `figuras/repositorio-github.png` |
| 17 | Em aberto | `perguntas-orientador.md` (Q1, Q7); `2026-09-12-forma-da-curva.md` (NT 923); `2026-09-12-mudanca-de-escopo.md` (triaxial) |
| 18 | Obrigado | — (fechamento) |

**Critério de τ, desde 29/09 (noite).** Os slides 8 e 11 usam τ a 10 mm de deslocamento, o
critério do laboratório, registrado em
[`2026-09-29-ruptura-a-10mm.md`](../registros/2026-09-29-ruptura-a-10mm.md). O slide 8 deixou
de ser o NT 268 × NT 296 e virou as sete curvas da série D1N; o título do slide 9 deixou de
dizer que o processamento manual lê o máximo de τ.

**Rastreabilidade do slide 11.** φ = 32,6°, c = 24,0 kPa e R² = 0,987 tinham vindo só do
script de apoio; desde 29/09 têm registro próprio,
[`2026-09-29-envoltoria-d1n.md`](../registros/2026-09-29-envoltoria-d1n.md), que também mede
quanto a envoltória muda sem o filtro de ruptura e com o σ lido do ID.

---

## Testes de design — 29/09/2026

Duas variantes do mesmo conteúdo (a reunião de alinhamento, reestruturada — ver abaixo),
para comparar direção visual antes de fechar uma única versão:

- **`2026-09-29-teste-design-terra.html`** — a paleta oficial do `CLAUDE.md`, aplicada de
  verdade (o deck de 16/09 usava um acento teal que não está na tabela oficial). Hierarquia
  só por valor/preenchimento, sem segunda cor: o antigo vermelho de "alerta" virou
  preenchimento sólido `ink`, seguindo a regra "chip sólido escuro > chip sólido terra >
  chip contornado" do `CLAUDE.md`.
- **`2026-09-29-teste-design-geofluxo.html`** — inspirado no CSS real de `geofluxo.com`
  (inspecionado via `curl`, não visualmente — sem extensão do Chrome conectada nesta sessão):
  fundo slate, acento teal (`#0d9488`/`#14b8a6`), Rajdhani nos títulos + Open Sans no corpo.
  Diverge da identidade terrosa do projeto — é um teste, não uma proposta de mudar o
  `CLAUDE.md`.

**Mudanças de conteúdo, válidas nas duas variantes:**

- **O NT 608 saiu inteiro.** O slide "Ensaios travados" (só sobre ele) foi removido. Os
  slides "O filtro e os três casos" e "Forma da curva vs. magnitude" foram reescritos e
  fundidos em dois slides que usam o **NT 268** como exemplo (razão τ/σ de só 2× — reforça
  o argumento "forma da curva, não magnitude", sem a magnitude dramática do NT 608).
- **Slide novo: "A envoltória que sobra".** Mostra que os 7 ensaios da série D1N
  (30/09/2024) que passam no filtro de forma da curva já fecham uma envoltória de
  Mohr-Coulomb sozinhos (φ = 32,6°, c = 24,0 kPa, R² = 0,987) — o gráfico que faltava para
  o resultado citado no slide 2.
- **Figuras novas**, geradas por `scripts/apoio_apresentacao.py` (script avulso de apoio à
  apresentação, não faz parte de `src/geotec/`; lê os `.csv` brutos direto porque o parser
  de produção ainda não existe):
  - `docs/registros/figuras/forma-da-curva-268.png` — NT 296 (rompe) vs. NT 268 (travado).
  - `docs/registros/figuras/envoltoria-d1n.png` — envoltória dos 7 ensaios da série D1N.

**Decidido em 29/09/2026:** nenhuma das duas linhas — o estilo final é o **Swiss Modern**
(`ESTILO.md`), aplicado na apresentação de 30/09 acima. Os dois testes e a apresentação de
16/09 ficam como registro histórico, sem alteração.

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
