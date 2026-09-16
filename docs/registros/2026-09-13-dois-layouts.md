# As máquinas gravam dois layouts com a mesma extensão, e nenhuma forma de ler avisa quando você erra o tipo

_13 de setembro de 2026_

## A frase

> O acervo tem dois formatos de `.csv` diferentes, e **o tipo do ensaio não está escrito em
> nenhuma linha do conteúdo — só no nome do arquivo.** Submetendo um arquivo de adensamento
> às três maneiras usuais de ler um de cisalhamento, uma devolve um corpo de prova de 5 mm
> em vez de 50 sem reclamar, outra acerta por sorte, e a terceira levanta um erro que fala de
> contagem de campos. **Nenhuma das três diz que o arquivo é de outro tipo de ensaio.**

## O que aconteceu

Ao escrever o parser do cisalhamento direto, a intenção inicial era aceitar qualquer `.csv`
do acervo. Uma varredura dos 1.081 arquivos para conferir se o formato era mesmo uniforme
mostrou que não é: os 36 arquivos da pasta `Adensamento/` seguem outra estrutura.

A pergunta seguinte foi o que aconteceria se alguém apontasse o leitor de cisalhamento para
um deles. A resposta determinou como o parser foi escrito.

## A evidência

### Os dois layouts

| | `DS` / `DSS` | `ODC` |
| --- | --- | --- |
| Arquivos | 1.045 | 36 |
| Linhas de metadados | 7 | **9** |
| Nomes de coluna na linha | 8 | **10** |
| Colunas de dados | 17 | **11** |
| Linha 5 do cabeçalho | `Dimensao Secao [mm]` | `N. Estagios Carregamento` |
| Coluna 4 | `Tempo Etapa [min]` | `Estagio` |
| Valores de `Etapa` | `Adensamento`, `Cisalhamento` | `Pre-Carregamento`, `Carregamento`, `Descarregamento` |

As três primeiras chaves são **idênticas** nos dois: `Numero do Teste`, `ID do ensaio`,
`Formato CP`. A divergência começa na quarta.

### Os três modos de falha, medidos

Um arquivo `ODC` submetido às três formas usuais de ler um `DS`:

**1. Leitura posicional — pegar o diâmetro da linha 5.**

```
DS    Dimensao Secao [mm]        = 50
ODC   N. Estagios Carregamento   = 5
```

Silencioso e errado. O sistema receberia um corpo de prova de 5 mm em vez de 50. Como a área
entra em toda tensão calculada, o erro se propaga por tudo a jusante — cem vezes menor, sem
nenhum aviso.

**2. Leitura por chave — procurar `Dimensao Secao [mm]` nas 7 primeiras linhas.**

```
DS    Dimensao Secao [mm] = 50
ODC   Dimensao Secao [mm] = 50
```

Acerta — **por sorte**. No `ODC` essa chave existe, só que na linha 7 em vez da 5, e por
acaso ainda dentro das sete primeiras linhas lidas. Se o layout tivesse uma chave a mais, a
mesma leitura devolveria vazio. O acerto não vem do método; vem da coincidência.

**3. pandas com `skiprows=7`.**

```
ParserError: Error tokenizing data. C error: Expected 2 fields in line 10, saw 11
```

Levanta erro — mas fala de contagem de campos numa linha, não de tipo de arquivo. Quem
recebe essa mensagem vai investigar o arquivo achando que ele está corrompido.

### A interpretação

Não há nada de errado com as máquinas: dois tipos de ensaio produzem dados de formas
diferentes, e é natural que os arquivos difiram. O problema é que a **extensão é a mesma, as
primeiras linhas são parecidas, e o discriminador está fora do arquivo** — no nome, que é a
parte mais fácil de perder ao copiar, renomear ou mover.

Nenhuma das três leituras é incompetente. Cada uma falha de um jeito coerente com o que ela
supõe. O que falta às três é uma verificação explícita de que o arquivo é o que se espera.

## Como conferir

```
uv run python scripts/comparar_layouts.py
```

Imprime a contagem por tipo, os dois cabeçalhos lado a lado com a linha de nomes de coluna
marcada, e submete um `ODC` real às três leituras, mostrando o que cada uma devolve. Termina
mostrando o que o parser do projeto faz com o mesmo arquivo. Roda em menos de um segundo —
ele abre dois arquivos, não o acervo inteiro.

A última seção da saída é um teste de verdade: se o parser algum dia parar de recusar o
`ODC`, o script imprime um aviso em vez da mensagem de erro esperada.

## Por que isso importa

**Determinou o desenho do parser.** `parsers/direto.py` não tenta adivinhar. Ele confere
quatro coisas antes de converter qualquer número: o tipo no nome do arquivo, as sete chaves
do cabeçalho exatamente como esperadas, os dezessete nomes de coluna, e se o número do teste
e o instante do nome batem com o conteúdo. Qualquer divergência vira `ErroDeFormato` com
mensagem que nomeia o problema.

**É o argumento para validar em vez de confiar.** Custa vinte linhas de conferência e evita
uma classe inteira de erro que não aparece em teste, não aparece na tela e só seria
descoberto se alguém estranhasse o resultado final.

**Vale para o parser do adensamento, quando ele existir.** Este registro é o ponto de partida
do `parsers/adensamento.py`: o layout já está mapeado.

## O que eu decidi

**O parser recusa o que não reconhece, em vez de tentar entender.** Arquivo de tipo diferente,
cabeçalho diferente ou coluna renomeada param a leitura com erro explícito.

A alternativa descartada era detectar o layout automaticamente — contar linhas de metadados,
achar a linha de nomes de coluna, adaptar-se. É mais elegante e funcionaria para os dois
tipos. Foi rejeitada porque um parser que se adapta ao que encontra não tem como avisar que
encontrou algo errado; ele sempre devolve *alguma* tabela. Para dado que vai virar resultado
publicado, recusar é melhor que adivinhar.

Consequência assumida: quando a máquina mudar de versão e acrescentar uma coluna, o parser
vai parar de funcionar em vez de continuar. É o comportamento desejado, mas alguém terá que
atualizar a lista de colunas.

## Ligações

- **Os dois layouts, em forma de referência:** `docs/arquitetura/formato-bruto.md` §1.1.
- **O script que mede os três modos de falha:** `scripts/comparar_layouts.py`.
- **O parser e suas verificações:** `src/geotec/parsers/direto.py`.
- **`falha silenciosa`, com este caso como exemplo:** `docs/glossario.md`.

## O que ficou em aberto

**Este registro nasceu de uma suposição errada minha, e vale registrar isso.** Ao escrever o
parser, afirmei em três lugares — no `formato-bruto.md`, no glossário e numa mensagem de
commit — que ler um `ODC` como `DS` "não levanta erro nenhum". Nunca testei; deduzi da
estrutura. Quando o script foi escrito para *medir* em vez de supor, apareceu o
`ParserError`. Junto veio outro erro meu: eu tinha contado 8 linhas de metadados no `ODC`, e
são 9.

As três afirmações foram corrigidas. Fica a lição, que é a razão de este projeto exigir
script por trás de cada número: **uma dedução plausível sobre o comportamento de um programa
não vale nada até alguém rodar o programa.**

**Os 36 arquivos de adensamento continuam sem parser.** Eles têm dado aproveitável — 108 dos
arquivos de cisalhamento são acompanhados de um irmão de adensamento, segundo o registro
[da triagem](2026-09-12-triagem-do-acervo.md). Enquanto `parsers/adensamento.py` não existir,
esse dado fica parado.
