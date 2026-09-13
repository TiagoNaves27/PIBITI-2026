# Contexto do projeto

PIBITI 2026 — sistema automatizado de coleta e análise de dados dos ensaios de
**cisalhamento direto** e **compressão triaxial**, para o grupo GeoFluxo (UnB).

Fluxo: `máquina grava arquivo bruto → coleta → parser → banco → cálculo → relatório PDF`.

As máquinas já digitalizam os dados e estão em rede. **Não há Raspberry Pi nem leitura de
sensores neste projeto** — isso saiu do escopo. Ver `docs/arquitetura/visao-geral.md` §1.

Documento oficial: `docs/plano/PlanoTrabalho-PIBITI_4.md`.
Estado real e decisões vigentes: `docs/arquitetura/visao-geral.md` — **este prevalece** quando
divergir do plano.

## Convenções

- **Idioma:** documentação, commits e nomes de módulos/funções em **português** (sem acentos em
  identificadores de código). Comentários em português.
- **Unidades:** SI internamente (N, m, Pa, s). Conversão para kPa/mm só na apresentação.
  Toda função que recebe ou devolve grandeza física declara a unidade no docstring.
- **Ângulos:** radianos internamente; graus apenas na interface e nos relatórios.
- Cálculos geotécnicos ficam em `src/geotec/nucleo/` e **não** importam nada de GUI ou banco
  — são funções puras sobre arrays/DataFrames, para poderem ser testadas.
- Cada máquina/formato ganha seu próprio módulo em `src/geotec/parsers/`. Todos devolvem o
  **mesmo** formato normalizado (`visao-geral.md` §5), para que nada a jusante saiba de qual
  máquina o dado veio.
- Banco: **SQLite no desenvolvimento, MySQL na entrega.** Use SQLAlchemy Core; o código não
  muda entre os dois, só a string de conexão.

## Paleta

Tons terrosos, definidos pelo aluno. Vale para páginas, gráficos e figuras do relatório.

| Token | Claro | Escuro | Uso |
| --- | --- | --- | --- |
| `ink` | `#402905` | `#ead0a8` | texto principal; preenchimento de destaque máximo |
| `ink-soft` | `#6b5428` | `#cbb68c` | texto secundário |
| `muted` | `#7d6840` | `#9b8555` | rótulos, legendas |
| `terra` | `#76552b` | `#d4b06f` | acento: ênfase, foco, bordas de destaque |
| `ocre` | `#b69f66` | `#b69f66` | preenchimentos e barras — **nunca texto** (contraste 2,7:1) |
| `ocre-soft` | `#ead0a8` | `#3d2f14` | fundos suaves, chips |
| `ground` / `surface` | `#e9dcc0` / `#fbf5ea` | `#1a1207` / `#281d0d` | fundo da página / cartões |
| `done` | `#5f7040` | `#8fa86a` | **semântico** (concluído), fora da identidade |

A paleta é monocromática, então **hierarquia se faz por valor e preenchimento**, não por
matiz: chip sólido escuro > chip sólido `terra` > chip contornado. Não invente uma segunda
cor de acento para diferenciar dois elementos lado a lado.

Em gráficos com várias séries, varie **valor e traço** (contínuo / tracejado / marcador)
antes de sair da paleta — série de ensaio não deve depender só de cor para ser distinguida.

## Ambiente

`uv` gerencia tudo. Python 3.14, Windows.

```
uv sync            uv run pytest            uv run ruff check .
```

Nunca commitar `.env`, dados brutos de ensaio ou PDFs de referência.

## Ao trabalhar aqui

- Cada função de cálculo novo precisa de teste com valor de referência conferido à mão
  ou vindo de exemplo de norma/livro (ASTM, Head, Pinto, Das).
- Ao mudar escopo/arquitetura, atualizar `docs/arquitetura/visao-geral.md` no mesmo passo.

## Explicar, não só entregar

**É a primeira vez que o aluno faz um projeto assim.** Programação, versionamento, linha de
comando e o vocabulário que vem junto são todos novos. Ele acompanha bem quando o porquê vem
junto — o que falta é vocabulário, não capacidade. Não presuma que um termo é conhecido só
porque é básico para quem já programa.

- **Todo termo técnico ganha uma explicação curta na primeira vez que aparece.** Vale para
  jargão de código (*parser*, *fixture*, *dataclass*, *lint*, *regex*, *BOM*, *LF/CRLF*),
  de Git (*commit*, *branch*, *remote*, *staged*) e de estatística (*R²*, *regressão*,
  *resíduo*). Uma frase basta — não vire aula, não interrompa o trabalho.
- **Todo comando vem com o que ele faz e como saber se deu certo.** Não `git add -A` solto,
  mas o que ele marca e o que a tela deve mostrar depois. Ele precisa distinguir sucesso de
  erro sozinho.
- **Ao propor uma decisão técnica, diga a alternativa e o que se perde com ela.** Uma escolha
  sem alternativa declarada não ensina nada e não pode ser contestada.
- Se a explicação passar de dois parágrafos, ela vira arquivo em `docs/` — não some no
  terminal junto com o resto da sessão.
- Perguntar "quer que eu explique X?" é pior do que explicar X em uma frase e seguir em
  frente. Ele não sabe ainda se precisa de X.
- Nomear o que está acontecendo vale mais que suavizar: dizer "isso é uma falha silenciosa,
  o código não dá erro e produz número errado" ensina; dizer "tive um probleminha" não.
