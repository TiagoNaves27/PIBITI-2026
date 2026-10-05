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

## Registros

`docs/registros/` guarda um arquivo por momento que vale contar. Regras completas no
`README.md` de lá; o essencial:

- **Vira registro:** um número que vai ter que ser defendido; uma decisão com alternativa
  descartada; algo que o processamento manual não pegaria; uma surpresa que contrariou o
  que se supunha.
- **Não vira registro:** trabalho de rotina. "Escrevi o parser" não; "descobri que as
  máquinas gravam dois layouts e nenhuma forma de ler avisa quando você errou o tipo" sim.
- **Todo número citado vem de script versionado em `scripts/`**, que reproduz o valor. Número
  que só existe porque alguém rodou algo uma vez não entra.
- **Figura gerada por script**, em `docs/registros/figuras/`, com a paleta acima. Nunca print
  de tela — não se regenera quando o dado muda e não tem resolução para projetor.
- **Registro não se corrige por cima.** Número que mudar gera registro novo explicando a
  mudança; o antigo fica.
- **Separar o que o dado mostra do que é interpretação**, em parágrafos rotulados. Dedução a
  partir dos arquivos vai marcada como dedução, com o que falta para confirmá-la.
- **Nunca inventar contexto.** Não afirmar o que ninguém disse — como o laboratório
  trabalhava, o que o operador pretendia, por que um ensaio foi feito. Se não veio de uma
  pessoa, de um arquivo, ou de dedução declarada como tal, não entra. Vale para todos os
  documentos do projeto, não só para os registros.

## Explicar, não só entregar

**É a primeira vez que o aluno faz um projeto assim.** Programação, versionamento, linha de
comando e o vocabulário que vem junto são todos novos. Ele acompanha bem quando o porquê vem
junto — o que falta é vocabulário, não capacidade. Não presuma que um termo é conhecido só
porque é básico para quem já programa.

- **Todo termo técnico ganha uma explicação curta na primeira vez que aparece.** Vale para
  jargão de código (*parser*, *fixture*, *dataclass*, *lint*, *regex*, *BOM*, *LF/CRLF*),
  de Git (*commit*, *branch*, *remote*, *staged*) e de estatística (*R²*, *regressão*,
  *resíduo*). Uma frase basta — não vire aula, não interrompa o trabalho.
- **Explicado uma vez, está explicado — não repetir.** Termo já explicado volta a ser usado
  seco, como se ele sempre tivesse sabido. Nem versão resumida, nem lembrete entre
  parênteses: repetir sugere que ele não entendeu da primeira vez, e é exatamente o tipo de
  coisa que cansa. Ele pede de novo quando esquecer — e aí explicar direto, sem "como eu
  disse antes".
- **`docs/glossario.md` é o registro do que já foi explicado.** Termo que está lá já passou:
  usar seco, e no máximo apontar o glossário. Termo novo que precisou de explicação **entra
  lá no mesmo passo**, com o exemplo concreto do projeto onde ele apareceu.
- **Na dúvida, não explique.** Entre uma sessão e outra não há registro além do glossário.
  Dois sinais resolvem o resto: se ele usou o termo espontaneamente, está aprendido; se o
  termo aparece escrito em `docs/` ou num comentário do código do projeto, já passou por
  ele. Errar para o lado de não explicar é melhor — explicação faltando ele pede,
  explicação repetida ele engole calado.
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
