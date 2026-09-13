# Glossário

_Última atualização: 13/09/2026_

Termos técnicos que aparecem neste projeto, explicados uma vez e registrados aqui.

Existe por um motivo prático: entre uma sessão e outra o assistente não guarda o que já
explicou, e sem registro ele reexplicaria o mesmo termo indefinidamente. Um termo que está
escrito aqui é um termo que já passou — a regra está no `CLAUDE.md`, seção "Explicar, não só
entregar".

**Quando um termo novo for explicado, ele entra aqui.** Uma linha por termo, com o lugar do
projeto onde ele apareceu — o exemplo concreto é o que faz o termo grudar.

---

## Código e testes

### `parser`
Programa que lê um formato de arquivo e o traduz para uma estrutura que o resto do sistema
entende.
**Aqui:** `src/geotec/parsers/direto.py` lê o CSV da máquina de cisalhamento e devolve
metadados + série temporal em SI.

### `fixture`
Cenário preparado de antemão para um teste usar, para que o teste comece de um ponto
conhecido em vez de montar tudo toda vez. A palavra tem dois usos, e os dois aparecem aqui:

- **arquivo de fixture** — um dado de mentira, feito à mão, com valores que você escolheu.
  `tests/dados/2026-01-15 08-30-00 - NT 9001 - DS - ID TESTE01.csv` é um CSV falso, com
  números redondos (200 kPa, 2,5 mm) justamente para a conversão de unidade ser óbvia a
  olho nu.
- **fixture do pytest** — função marcada com `@pytest.fixture` que monta o cenário e o
  entrega pronto. A função `ensaio()` em `tests/test_parser_direto.py` faz isso: todo teste
  que pede `ensaio` recebe o arquivo já lido, sem repetir a linha de leitura.

### `dataclass`
Classe do Python em que você só declara os campos e seus tipos, e a linguagem gera o resto
(construtor, comparação, exibição). `frozen=True` proíbe alterar o objeto depois de criado.
**Aqui:** `direto.Metadados`.
**Por que em vez de um dicionário:** `meta.diametro` acusa erro na hora se o campo não
existir, e o editor completa o nome sozinho. `meta["diametro"]` só quebra quando o código
roda, e `meta["diamtero"]` passa despercebido até dar resultado errado.

### `lint`
Verificação automática do código **sem executá-lo**, atrás de erro provável e de
inconsistência de estilo. Não confundir com teste: o lint não sabe se a conta está certa,
só se o código está bem escrito.
**Aqui:** a ferramenta é o `ruff`. `ruff check .` acusa problemas; `ruff format` reescreve
espaçamento e quebras de linha por conta própria.
**Origem do nome:** o programa `lint` do Unix, de 1978 — "tirar fiapo" da roupa.

### `regex` (expressão regular)
Notação para descrever um padrão de texto, usada para procurar e extrair pedaços.
**Aqui:** `direto.NOME_ARQUIVO` descreve o padrão
`AAAA-MM-DD HH-MM-SS - NT <n> - <tipo> - ID <id>.csv` e é o que extrai o tipo do ensaio do
nome do arquivo.

### `DataFrame`
Tabela em memória da biblioteca pandas: colunas com nome, linhas numeradas, cada coluna com
seu tipo. É o formato em que a série temporal do ensaio circula pelo sistema.

### falha silenciosa
Defeito em que o código **não dá erro**, não avisa nada, e mesmo assim produz resultado
errado. É a pior categoria, porque nada chama a sua atenção — o número sai com cara de
certo e segue para o relatório.
**Aqui:** ler um arquivo `ODC` como se fosse `DS`. Não levanta exceção; toma a linha
`Altura Inicial [mm];20` como sendo a linha de nomes de coluna e devolve uma tabela sem
sentido. É por isso que `parsers/direto.py` confere as chaves do cabeçalho e os 17 nomes de
coluna antes de converter qualquer número.

---

## Arquivos e texto

### `BOM` (Byte Order Mark)
Três bytes invisíveis (`EF BB BF`) no começo do arquivo, cuja única função é declarar "isto
está em UTF-8". Não aparecem em nenhum editor.
**Aqui:** os 1.043 arquivos da máquina têm BOM.
**Efeito prático:** lido sem aviso, o BOM cola na primeira coisa do arquivo, e a chave
`Numero do Teste` vira `﻿Numero do Teste` — a busca por ela falha sem explicação
aparente. Resolve-se com `encoding="utf-8-sig"` (`sig` de *signature*).

### `LF` e `CRLF`
As duas convenções para marcar o fim de uma linha num arquivo de texto. `LF` é um byte só
(`\n`), usado por Linux e Mac. `CRLF` são dois (`\r\n`), usados pelo Windows. O conteúdo
visível é idêntico; os bytes, não.
**Aqui:** a máquina grava `LF`, e sem quebra de linha no final do arquivo. O Git no Windows
converte para `CRLF` ao entregar os arquivos, o que mudaria os bytes do acervo num clone
novo — é o que o `.gitattributes` impede.

### `UTF-8`
A convenção quase universal para representar texto como bytes, incluindo acentos e
caracteres de outros alfabetos.

### SI (Sistema Internacional)
O sistema de unidades em que o projeto trabalha internamente: newton, metro, pascal,
segundo, radiano. A máquina entrega kPa, mm e minuto; o parser converte tudo na entrada, e
a volta para kPa/mm só acontece na hora de plotar e relatar. Ver `CLAUDE.md`.

---

## Git

### repositório
A pasta do projeto junto com todo o histórico de versões dela. É o `.git` escondido dentro
de `PIBITI_2026/` que guarda esse histórico.

### `commit`
Uma fotografia do projeto inteiro num instante, com uma mensagem dizendo o que mudou e por
quê. O histórico é a sequência dessas fotografias. Cada commit tem um código (`4a5c07f`)
que serve para voltar a ele.

### `staged` / área de staging
O degrau intermediário entre editar um arquivo e gravar o commit. `git add` **marca** as
mudanças para entrarem no próximo commit; `git commit` grava o que foi marcado.
**Para que serve o degrau:** permite commitar só parte do que você mexeu, separando duas
mudanças sem relação em dois commits. `git status` mostra as duas listas — o que está
marcado e o que não está.

### `main`
O nome da linha principal de desenvolvimento. Neste projeto se commita direto nela, porque
é um repositório de uma pessoa só, sem ninguém para revisar.

### `diff`
A diferença entre duas versões, mostrada linha a linha: `+` para linha acrescentada, `-`
para removida. `git diff` mostra o que você mexeu e ainda não marcou; `git diff --cached`,
o que já está marcado.

### `.gitattributes`
Arquivo que dá instruções ao Git sobre como tratar certos arquivos.
**Aqui:** `*.csv -text` manda o Git não mexer nas quebras de linha dos CSV, para que os
dados brutos cheguem a qualquer computador exatamente como a máquina os gravou.
