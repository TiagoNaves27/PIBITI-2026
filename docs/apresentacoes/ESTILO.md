# Estilo das apresentações — Swiss Modern

Guia visual de todas as apresentações do projeto. Escolhido em 29/09/2026, depois de uma rodada de
testes de estilo com a skill `frontend-slides` (fora deste repositório). Vale junto com a
[paleta do `CLAUDE.md`](../../CLAUDE.md#paleta), que é a mesma.

**Para começar uma apresentação nova:** copie [`MODELO.html`](MODELO.html) para
`AAAA-MM-DD-assunto.html`, apague os slides que não servirem, duplique os que servirem e troque
todo texto entre `[colchetes]`. O `MODELO.html` tem um exemplo de cada componente abaixo, com
comentários no HTML dizendo quando usar cada um.

---

## Princípios

1. **Densidade alta.** O slide se explica sozinho: o orientador pode ler o arquivo sem quem
   apresentou. Título em forma de **afirmação**, não de assunto — "O acervo tem 914 ensaios
   utilizáveis", não "Triagem do acervo".
2. **Dado, interpretação e decisão separados.** Mesma regra dos registros: o que o arquivo
   mostra vai num bloco; a dedução vai em outro, marcada como tal; a decisão, em outro.
3. **Todo número tem fonte no próprio slide** — o registro ou documento, e o comando para
   conferir quando houver script. Ver as regras de `README.md` desta pasta.
4. **Uma cor de acento só.** Vermelho marca o que importa; todo o resto é preto e cinza.
   Se tudo estiver vermelho, nada está.
5. **A grade aparece.** As 12 colunas de 160 px ficam visíveis ao fundo de todo slide.

## Palco

- Slide de **1920 × 1080**, escalado inteiro para a janela (nunca reorganiza para celular).
- Margens: **160 px** nas laterais; conteúdo começa em 150 px do topo (abaixo das seções) e
  para em 120 px da base (acima do rodapé).
- Grade: 12 colunas de 160 px, linhas a 5,5% de opacidade.

## Cores

| Token | Valor | Uso |
| --- | --- | --- |
| `--ink` | `#000000` | texto, filetes grossos, painéis e blocos de decisão |
| `--slide-bg` | `#ffffff` | fundo dos slides de conteúdo |
| `--red` | `#ff3300` | acento único: número principal, rótulos, série em destaque |
| `--red-deep` | `#dd2c00` | **só** o fundo dos divisores de seção — com texto branco dá 4,7:1 |
| `--muted` | `#5a5a5a` | texto secundário, legendas, fontes |
| `--rule` | `#d6d6d6` | filetes finos entre linhas de tabela |
| `--soft` | `#f2f2f2` | fundo de `code` e trilho das barras |

**Vermelho em texto só em tamanho grande ou negrito ≥ 18 px** — sobre branco o contraste é
3,7:1, suficiente para texto grande, não para texto corrido. Texto corrido é sempre preto ou
`--muted`.

Slides invertidos: **divisor de seção** em `--red-deep` com **todo o texto em branco**, e
**citação/fechamento** em preto (texto branco). Nunca texto preto sobre vermelho: o contraste
numérico passa, mas a combinação vibra e cansa a leitura — foi corrigido em 29/09/2026 por isso.

## Tipografia

| Papel | Fonte | Tamanho em 1920 × 1080 |
| --- | --- | --- |
| Título da capa | Archivo 800 | 142 px, entrelinha 0,95 |
| Título do slide (`h2`) | Archivo 800 | 54 px |
| Divisor de seção | Archivo 800 | 128 px + número de 340 px |
| Número em destaque | Archivo 800 | 84 px (`.stats`), 46 px (`.contagem`) |
| Rótulo (`.kicker`, cabeçalho de tabela) | Archivo 700, caixa alta | 18 px / 14 px |
| Texto | Nunito 400 | 22–24 px |
| Fonte, legenda | Nunito 400 | 17 px, `--muted` |

Letras gregas (τ, σ, φ) vão dentro de `<span class="sym">` — usa Noto Sans e impede que a caixa
alta transforme `τ` em `Τ`.

## Componentes

Todos estão no `MODELO.html`.

| Componente | Classe | Quando usar |
| --- | --- | --- |
| Capa | `.s-capa` | sempre; o bloco vermelho leva o número que resume a apresentação |
| Números em destaque | `.stats` | 2 a 4 números; `.forte` em um só |
| Agenda | `.agenda` | roteiro com o intervalo de slides de cada seção |
| Tabela | `.tab` (+ `.num`, `.d` para alinhar à direita) | dados tabulares; filete de 3 px no cabeçalho |
| Painel preto | `.painel` + `.lista` | lista curta que precisa se destacar ao lado de uma tabela |
| Divisor de seção | `.s-secao` | início de cada seção grande, com até 3 frases de resumo |
| Blocos | `.bloco`, `.bloco.interp`, `.bloco.decisao` | dado / interpretação / decisão |
| Barra de proporção | `.proporcao` | parte de um todo (ex.: 914 de 1.043) |
| Funil | `.funil` | filtros aplicados em sequência |
| Contagem | `.contagem` | 3–4 números grandes em coluna |
| Gráfico | `svg.grafico` | desenhado no próprio slide — ver abaixo |
| Imagem | `figure.tela` | captura de tela ou PNG, com moldura de 1 px |
| Citação | `.s-citacao` | uma frase de registro que resume uma lição |
| Decisões | `.decisoes` | síntese em 2 × 2, no máximo 4 |
| Fechamento | `.s-obrigado` | último slide |

Navegação e seções: o topo de cada slide mostra as seções (`.marco`, a atual sublinhada em
vermelho); o rodapé mostra título e número da página.

## Gráficos

- **Desenhados em SVG no próprio slide**, com os dados reais — não colar PNG. Área útil do
  `viewBox="0 0 1000 520"`: x de 80 a 980, y de 30 a 460.
- Os pontos vêm de um script versionado (hoje, `scripts/apoio_apresentacao.py`), citado na
  fonte do slide.
- **Série principal:** preta, contínua (`.serie-a`). **Série em destaque:** vermelha,
  tracejada, com marcadores (`.serie-b` + `.pts-b`). A diferença nunca depende só da cor.
- Anotação direto no gráfico, no ponto que importa (`.anot`, `.anot.forte`), em vez de
  legenda distante. Nenhuma anotação pode cruzar linha ou ponto.
- Eixos: linhas de grade `#e3e3e3`, rótulos em `--muted`.

## Movimento

Entradas curtas (0,55 s), escalonadas, de baixo para cima (`.reveal`). Na capa, o bloco
vermelho desce e o filete preto se estende. Nada além disso: o público é um orientador, não
uma plateia de evento. `prefers-reduced-motion` é respeitado.

## Apresentar e exportar

- **Apresentar:** abrir o `.html` no navegador e apertar **F11**. Setas, espaço, rolagem ou
  deslizar navegam.
- **As fontes vêm do Google Fonts.** Sem internet, o navegador usa fontes genéricas. Se for
  apresentar offline, embutir as fontes no arquivo antes.
- **PDF:** `Ctrl+P` → Salvar como PDF (um slide por página, texto selecionável). O PDF não
  tem animação.
- **Editar direto no navegador:** tecla **E** (ou canto superior esquerdo), clicar no texto;
  **Ctrl+S** baixa uma cópia com as edições. As edições ficam só no navegador até isso.
