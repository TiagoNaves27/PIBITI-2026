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

**Swiss Modern** — preto, branco e um único acento vermelho. Definida pelo aluno em
29/09/2026, substituindo a paleta de tons terrosos. Vale para páginas, apresentações, gráficos e
figuras do relatório. Tipografia: **Archivo** (títulos, números, rótulos) + **Nunito** (texto).
Guia completo, com componentes: `docs/apresentacoes/ESTILO.md`.

| Token | Claro | Invertido | Uso |
| --- | --- | --- | --- |
| `ink` | `#000000` | `#ffffff` | texto principal; filetes grossos; painéis e blocos de destaque |
| `ink-soft` | `#333333` | `#d0d0d0` | texto secundário |
| `muted` | `#5a5a5a` | `#a8a8a8` | rótulos, legendas, fontes |
| `red` | `#ff3300` | `#ff3300` | acento único: número principal, rótulos, série em destaque |
| `red-deep` | `#dd2c00` | — | só fundo chapado (divisores de seção), sempre com texto branco |
| `gray` | `#cfcfcf` | `#444444` | preenchimentos e barras secundárias — **nunca texto** |
| `rule` / `soft` | `#d6d6d6` / `#f2f2f2` | `#333333` / `#1a1a1a` | filetes finos / fundos suaves, `code` |
| `ground` | `#ffffff` | `#000000` | fundo da página |
| `done` | `#2f7a3b` | `#5fb56c` | **semântico** (concluído), fora da identidade |

**Vermelho em texto só em tamanho grande ou negrito ≥ 18 px** (contraste 3,7:1 sobre branco).
Texto corrido é sempre `ink` ou `muted`. Hierarquia se faz por **peso, tamanho e preenchimento
preto**; o vermelho marca **uma** coisa por vez — não invente uma segunda cor de acento para
diferenciar dois elementos lado a lado.

Em gráficos com várias séries: série principal preta e contínua, série em destaque vermelha,
tracejada e com marcador, demais em `gray`. Varie **traço e marcador** antes de acrescentar cor —
série de ensaio não deve depender só de cor para ser distinguida.

As figuras antigas de `docs/registros/figuras/` (até 16/09/2026) foram geradas na paleta
terrosa e ficam como estão — registro não se corrige por cima. Figuras novas usam esta paleta.

## Apresentações

Ficam em `docs/apresentacoes/`, com as regras do `README.md` de lá (nome `AAAA-MM-DD-assunto.html`,
tabela de referências slide a slide, todo número rastreável até um registro). Estilo fixo:
**Swiss Modern**, descrito em `docs/apresentacoes/ESTILO.md`. Para começar uma nova, copiar
`docs/apresentacoes/MODELO.html`.

A skill `frontend-slides` está instalada em `.claude/skills/`. Ao usá-la aqui, o estilo já está
escolhido: pular a descoberta de estilo (prévias) e gerar direto no Swiss Modern do `ESTILO.md`,
salvando em `docs/apresentacoes/` — a menos que o aluno peça para explorar outro estilo.

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
