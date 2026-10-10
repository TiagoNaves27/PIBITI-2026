# 30/09/2026 — Reunião de alinhamento

> **Em uma linha:** reuniões devem ser curtas (7 a 10 min) e focadas em resultado, método e
> dificuldade; o sistema deve servir a quem recebe o resultado — interpretar os dados e
> justificar o ensaio que deu errado.

| Data | Presentes | Material levado |
| --- | --- | --- |
| 30/09/2026 | Tiago (aluno), orientador | [apresentação](../apresentacoes/2026-09-30-reuniao-alinhamento.html) · [roteiro de fala](../apresentacoes/2026-09-30-reuniao-alinhamento-roteiro.md) |

## O que o professor disse

**Sobre as reuniões**
- Ser objetivo: levar resultados e perguntas.
- Terminar em **7 a 10 minutos**. (O roteiro levado previa cerca de 20.)
- Não explicar teoria para ele; focar nos **métodos usados** e nas **dificuldades**.

**Sobre estudo**
- Ler o "livro azul" de cisalhamento e se basear nas referências dele.

**Sobre o que acrescentar ao sistema**
- Acesso remoto para acompanhar a finalização dos ensaios em tempo real.
- Entregar o resultado junto com a interpretação e os _insights_ dos dados — por exemplo, os
  gráficos com a envoltória.
- Pensar nos resultados para as **empresas**: fáceis de entender, tanto o resultado quanto a
  análise.
- Interpretação de erros: quando o ensaio der errado, saber justificar por quê — a empresa
  mandou um solo atípico, houve erro de manipulação da máquina etc.

## Decisões

_Nenhuma_ mudança de escopo foi fechada. As sugestões de funcionalidade acima ficam em
"Em aberto" até se decidir se entram no projeto.

## Tarefas

- [ ] Descobrir qual é o "livro azul" (título, autor, edição) e incluí-lo em
      `referencias/biblioteca.bib` — professor
- [ ] Ler o livro azul e usar as referências dele como base — professor
- [x] Levar o formato de reunião pedido (7–10 min, resultado, método, dificuldade, sem teoria)
      para as regras de [`docs/apresentacoes/`](../apresentacoes/README.md) — professor · feito em
      10/10/2026

## Ideias do aluno

Brainstorm, não discutido com o professor nem decidido.

- **Banco de dados em blocos** por tipo de ensaio: triaxial, cisalhamento etc.
- **Filtrar por tipo de solo** e pelas condições esperadas, com base no que o banco já tem.
- **Avisar comportamento atípico** de um ensaio em relação àquele tipo de solo.
- **Um LLM** para uma análise mais profunda dos resultados.
- **Checar se a envoltória faz sentido pelo R²** _(acrescentada em 10/10/2026, depois da
  reunião)_. Faixas anotadas:

  | R² | Leitura proposta |
  | --- | --- |
  | ≥ 0,999 | esquisito — risco de dado corrompido ou forjado |
  | ≥ 0,98 | excelente — c e φ confiáveis |
  | 0,95 a 0,98 | alerta — olhar o gráfico em busca do corpo de prova com erro |
  | < 0,95 | preocupante — dispersão alta |

## Em aberto

- **Qual é o livro azul?** Sem título, não dá para citar nem achar as referências.
- **As sugestões de funcionalidade entram no escopo?** Se sim, o `visao-geral.md` muda. O acesso
  em tempo real é a que mais mexe na arquitetura: hoje o fluxo começa no arquivo que a máquina
  **já gravou** (`visao-geral.md` §1); acompanhar o ensaio em andamento é outra coisa. _(Dedução,
  não dita na reunião.)_
- **De onde vêm as faixas de R²?** Não têm fonte anotada. Antes de virarem regra no código,
  precisam de uma norma ou livro (ASTM, Head, Pinto, Das), como pede o `CLAUDE.md`. Para
  comparar: a série D1N deu R² = 0,987 com 7 pontos
  ([registro](../registros/2026-09-29-envoltoria-d1n.md)) — "excelente" nessa escala. E com
  poucos pontos o R² tende a sair alto mesmo sem nada de errado, o que pesa contra usar 0,999
  sozinho como sinal de fraude. _(Dedução, não dita na reunião.)_

<details>
<summary>Anotações originais, sem edição</summary>

Arquivo `notas_da_primeira_reuniao.txt`, com as anotações da reunião; as cinco últimas linhas
(a checagem do R²) foram acrescentadas em 10/10/2026.

```text
Ler livro azul de cisalhamento e se basear referencias 
objetividade da reunião
focar em resultados e perguntas para reunião
terminar a reunião em 7-10 minutos

coisas para acrescentar aplicativo

acesso remoto para ver finalização dos ensaios em tempo real 

Resultado de dados e interpretação junto com insights desses dados
Insights 
- gerar gráficos com o envoltório
- resultados para empresas 
- interpretação de erros 
- Focar na parte de se o ensaio der errado e como justificar o erro do ensaio, a empresa mandou um solo atipico, erro de manipulação da maquina, 


não precisa explicar a teoria para o professor, focar nos métodos usados e dificuldades

focar em gera resultados para empresas e fazer isso que fique fácil de entender os resultados e analise de dados

Banco de Dados
criar blocos principais de dados dos ensaios
Triaxial
Cisalhamento
etc...

Filtrar por tipo de solo e condições esperadas com base nas analises dos dados do banco de dados
Avisar se tiver comportamento atípico daquele solo

Tentar criar um LLM para fazer essa analise mais profunda


criar alguma forma de verificar se a elvoltoria faz sentido
- Se ela estiver com os pontos com R² que 0.999 é esquisito, com o risco de dados corrompidos ou forjados é alta
- R² ≥ 0,98 (Excelente): Os pontos experimentais estão muito bem alinhados. Dá alta confiabilidade aos parâmetros de coesão (c) e ângulo de atrito (φ) obtidos.
- 0,95 ≤ R² < 0,98 (Aceitável/Alerta): Há uma dispersão moderada. Requer uma análise visual cuidadosa do gráfico para entender se houve erro em algum corpo de prova específico.
- R² < 0,95 (Preocupante): Alta dispersão dos resultados. Induz a erros graves no cálculo das estruturas.
```

</details>
