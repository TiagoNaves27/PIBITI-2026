# O acervo tem 914 ensaios utilizáveis — e a maior parte do descarte não é ensaio perdido

_12 de setembro de 2026_

## A frase

> Dos 1.043 arquivos de cisalhamento direto do laboratório, **914 viram ponto de
> envoltória**. Dos 129 descartados, **108 são o fluxo normal de trabalho do laboratório**
> e apenas **21** indicam que alguma coisa deu errado.

![Triagem do acervo](figuras/triagem-do-acervo.png)

## O que aconteceu

O laboratório do GeoFluxo acumulou 1.081 arquivos de ensaio entre maio de 2023 e agosto de
2026, gravados automaticamente pelas máquinas. Ninguém tinha lido esse acervo inteiro — os
ensaios eram processados um a um, à medida que cada pesquisador precisava do seu.

A primeira varredura parcial produziu um número assustador: **"129 ensaios abortados"**.
Isso descrevia o acervo como tendo quase 13% de perda, o que levantava a dúvida de se ele
serviria como base para o trabalho.

Lendo os 1.043 arquivos de cisalhamento direto um por um, a descrição se mostrou errada. Os
129 existem, mas não são 129 ensaios perdidos — são quatro situações diferentes somadas
como se fossem uma só.

## A evidência

| Situação | Arquivos | Significa falha? |
| --- | ---: | :---: |
| Etapa de cisalhamento com 5 ou mais leituras | **914** | — |
| Só adensamento, com irmão de cisalhamento | 108 | não |
| Só adensamento, órfão | 17 | sim |
| Cisalhamento com 1 a 4 leituras | 4 | sim |
| **Total** | **1.043** | |

**O que são os 108.** Um ensaio de cisalhamento direto tem duas etapas: primeiro o corpo de
prova é adensado sob a tensão normal, depois é cisalhado. O operador do laboratório salva
as duas etapas em arquivos separados — um com o adensamento, outro com o cisalhamento. O
arquivo "só de adensamento" não é um ensaio que falhou: é a primeira metade de um ensaio
cuja segunda metade está no arquivo ao lado, com o mesmo `ID do ensaio` e a mesma data.

Foi assim que os 108 foram identificados: para cada arquivo sem etapa de cisalhamento,
procurou-se um irmão — mesmo identificador, mesmo dia — que tivesse a etapa. 108 têm; 17
não têm, e esses sim são ensaios em que alguma coisa se perdeu.

**O que são os 4.** Arquivos com 1 a 4 leituras na etapa de cisalhamento. Duraram de 2 a 18
segundos e avançaram menos de 0,15 mm. Dois deles são de maio de 2023 e têm
`ID do ensaio = MOVIMENTO`: são teste de máquina, feitos na instalação do equipamento, não
ensaio de solo.

## Por que isso importa

**Para o artigo.** A seção de métodos vai dizer "foram utilizados 914 ensaios". A pergunta
seguinte de qualquer revisor é "e os outros 129?". Com a tabela acima, a resposta é
verificável e mostra que o acervo é melhor do que o número bruto sugeria. Sem ela, a
resposta seria "o sistema descartou", que não é resposta.

**Para o projeto.** A descrição anterior sugeria um acervo com 13% de perda. O acervo real
tem 2% de perda. Isso muda a confiança de basear um ano de pesquisa nele.

**Para o desenho do sistema.** Esta foi a descoberta que determinou como o banco de dados
guarda a triagem. Um campo `valido` verdadeiro/falso registraria os 108 exatamente como
registraria os 17 — apagando a única distinção que importa. Por isso o modelo tem uma
tabela `ocorrencia` que guarda **o motivo**, não um sim/não.

## O que eu decidi

**Registrar o motivo de cada descarte, individualmente.** Quatro situações nomeadas, não um
booleano.

A alternativa descartada era o campo `valido` — mais simples de programar e de consultar.
Ela foi rejeitada porque perde a informação que responde ao revisor, e porque impediria o
sistema de distinguir "o laboratório trabalha assim" de "este ensaio se perdeu".

Consequência assumida: toda etapa a jusante precisa saber lidar com quatro valores em vez
de dois, e a interface tem que mostrar o motivo em algum lugar.

## Como conferir

```
uv run python scripts/triagem_acervo.py
uv run python scripts/triagem_acervo.py --listar orfao
uv run python scripts/figura_triagem.py
```

O primeiro comando recalcula a tabela a partir dos arquivos e imprime os quatro números. O
segundo lista os 17 órfãos, um por um, com número do teste e data. O terceiro regenera a
figura acima a partir dos mesmos dados — ela nunca é editada à mão.

## Ligações

- Critério e definições: `docs/arquitetura/formato-bruto.md` §5.1 e §5.4
- Modelo do banco com a tabela `ocorrencia`: `docs/arquitetura/visao-geral.md` §6
- Correção da descrição anterior: commit `c0c5f8a`
- Script que produz os números: `scripts/triagem_acervo.py`

## O que ficou em aberto

Os 914 são os arquivos que **podem** virar ponto de envoltória, não os que vão. Dois filtros
ainda não foram aplicados: o descarte de ensaios que não romperam (`formato-bruto.md` §5.4,
critério 3) e o agrupamento em séries, que depende de uma resposta do orientador. O número
final de ensaios usados será menor que 914.
