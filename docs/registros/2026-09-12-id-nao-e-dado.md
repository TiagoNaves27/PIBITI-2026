# O identificador do ensaio parece dizer a tensão normal — e em seis casos ele mente

_12 de setembro de 2026_

## A frase

> O `ID do ensaio` é digitado pelo operador e parece anunciar a tensão normal: `D1N16` seria
> 160 kPa. **O NT 614 tem `ID D1N16` e a máquina registrou σ = 22,2 kPa.** Não é caso único:
> em **6 identificadores** o mesmo ID aparece em ensaios com tensões normais diferentes.
> A regra que saiu disso vale para todo o sistema: **σ vem sempre da coluna de dados, nunca
> do nome.**

## O que aconteceu

O `ID do ensaio` do acervo segue um padrão legível. `D8N16V1` parece decompor em amostra D8,
condição N, 160 kPa, velocidade 1,0 mm/min — a hipótese está documentada em
`formato-bruto.md` §4 e é sustentada por várias verificações.

Isso torna tentador ler a tensão normal do identificador: é mais rápido que abrir o arquivo,
e resolveria de graça o problema de saber quanto vale cada ponto da envoltória.

A tentação foi testada antes de virar código. Ela não sobrevive.

## A evidência

### O teste, sem hipótese embutida

Decodificar a nomenclatura para conferi-la seria circular: exigiria assumir correta a
hipótese que está em questão. O teste usado não depende dela:

> **Dois ensaios com o mesmo `ID do ensaio` têm a mesma tensão normal medida?**

Se o identificador determinasse σ, a resposta seria sim em todos os casos.

| | |
| --- | ---: |
| Ensaios utilizáveis | 914 |
| Identificadores distintos | 748 |
| Identificadores usados em mais de um ensaio | 96 |
| Destes, com σ divergindo mais de 15 kPa | **6** |

Os 15 kPa de tolerância existem porque dois ensaios sob a mesma tensão nominal variam alguns
kPa entre si — a máquina não aplica exatamente 160,000 kPa. Acima disso não é variação de
equipamento: é outro ensaio.

### Os seis casos

| ID | Ensaios | σ medido |
| --- | ---: | --- |
| `B2-15-200` | 2 | 200 e **400** kPa |
| `SP-4-1-200` | 2 | 200 e **400** kPa |
| `D1N16` | 6 | cinco a ~160 e um a **22** kPa |
| `D9N5` | 4 | três a ~500 e um a **600** kPa |
| `D9N4` | 5 | quatro a ~400 e um a **500** kPa |
| `D9N30` | 2 | 300 e **400** kPa |

Os dois primeiros são mais claros ainda: o próprio identificador **termina em 200**, e um dos
dois arquivos foi gravado a 400 kPa.

### O caso `D1N16`, completo

| NT | Data | σ medido |
| ---: | --- | ---: |
| 394 | 22/05/2024 | 159,9 kPa |
| 608 | 30/09/2024 | 159,7 kPa |
| **614** | **30/09/2024** | **22,2 kPa** |
| 616 | 01/10/2024 | 159,8 kPa |
| 617 | 01/10/2024 | 159,5 kPa |
| 618 | 01/10/2024 | 159,8 kPa |

Cinco ensaios a 160 kPa e um a 22. O NT 614 foi gravado no mesmo dia que o NT 608, na mesma
série.

### A interpretação

O padrão — cinco iguais e um fora, no mesmo dia — é o que se espera quando um identificador é
reaproveitado do ensaio anterior e não é atualizado. Nos casos `B2-15-200` e `SP-4-1-200`, em
que o próprio ID termina no valor da tensão e o arquivo tem o dobro dela, a leitura é a
mesma.

**É dedução a partir do padrão, não relato de quem digitou.** O que os arquivos garantem é
que o mesmo identificador aparece em ensaios sob tensões diferentes. Por que, não está
gravado.

Repare que a direção da conclusão não depende da causa: seja qual for o motivo, o
identificador não descreve com segurança o ensaio que o arquivo contém.

## Como conferir

**1. Refazer o cruzamento.**

```
uv run python scripts/id_versus_sigma.py
```

Agrupa os 914 ensaios por identificador e compara a tensão normal medida dentro de cada
grupo. Deve imprimir 748, 96 e 6, seguidos dos seis casos detalhados. Leva cerca de 9
segundos.

**2. Ver todos os ensaios de um identificador.**

```
uv run python scripts/id_versus_sigma.py --id D1N16
```

Lista cada ensaio com aquele ID, com número do teste, data e σ medido. Serve para conferir um
caso à mão antes de acreditar na contagem.

> **Sem figura.** Seis casos numa tabela de seis linhas se leem melhor do que se enxergam
> desenhados. A regra dos registros é usar figura quando o número aparece melhor em gráfico,
> não sempre.

## Por que isso importa

**Uma tensão normal errada envenena a envoltória em silêncio.** Se o NT 614 entrasse com
σ = 160 kPa em vez de 22,2, o ponto (160; 31,0) iria para a regressão. O valor esperado a
160 kPa nessa série é cerca de 133 kPa. Um ponto com τ quatro vezes menor que o esperado
puxa a reta para baixo e reduz o φ calculado — sem nenhum aviso na tela.

**Vale para tudo, não só para σ.** A conclusão geral é que o identificador é **rótulo de
identificação, não instrumento de medida**. Amostra e condição continuam saindo dele, porque
não há outra fonte; mas grandeza física que a máquina mediu vem da coluna que a máquina
gravou.

**Muda a Q2 e a Q3 da reunião.** As perguntas sobre o que significam `N/S/U/W/A` e
`D1/D7/D8/D9` continuam valendo, mas agora com a ressalva de que mesmo a resposta certa não
torna o ID uma fonte confiável campo a campo.

## O que eu decidi

**Nenhuma grandeza física é lida do `ID do ensaio`.** σ, τ, deslocamento, velocidade e
geometria vêm sempre das colunas de dados ou do cabeçalho. O ID serve para identificar
amostra e condição, e para agrupar — e mesmo nisso é conferido contra o dado medido.

A alternativa descartada era decodificar a tensão do ID, o que seria mais rápido e
dispensaria abrir o arquivo. Foi rejeitada porque falha em 6 identificadores conhecidos, e
porque não há como saber quantos outros falham de um jeito que este teste não detecta — um ID
usado uma vez só, com a tensão errada, é indetectável por comparação interna.

Consequência assumida: o agrupamento em séries, que usa o ID, herda essa incerteza. Cada
série montada por identificador precisa ser conferida contra os σ medidos antes de virar
envoltória.

## Ligações

- **A nomenclatura do ID e as evidências que a sustentam:** `docs/arquitetura/formato-bruto.md`
  §4; a ressalva está em §5.5.
- **O script que faz o cruzamento:** `scripts/id_versus_sigma.py`.
- **Onde a série D1N de 30/09/2024 aparece por outro motivo:**
  [2026-09-12-ensaios-travados.md](2026-09-12-ensaios-travados.md).

## O que ficou em aberto

**Este teste só enxerga identificador repetido.** Ele compara ensaios que compartilham um ID.
Dos 748 identificadores, 652 aparecem uma vez só — e um ID único com a tensão errada não tem
com o que ser comparado. Os 6 encontrados são um piso, não um total.

**Um teste mais forte é possível, e depende das Q2 e Q3 do orientador.** Se a nomenclatura do §4 for
confirmada pelo laboratório, dá para decodificar a tensão de todos os IDs e comparar com o σ
medido de cada um, em vez de só comparar ensaios entre si. Aí o número deixa de ser um piso.
Enquanto a nomenclatura for hipótese, decodificá-la para testá-la é circular.
