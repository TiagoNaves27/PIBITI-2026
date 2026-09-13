# O projeto deixou de ser instrumentação e virou engenharia de dados

_12 de setembro de 2026_

## A frase

> O plano submetido ao PIBITI previa integrar sensores a um Raspberry Pi e programar a
> leitura de célula de carga e LVDT. **As máquinas do laboratório já digitalizam os dados e
> estão em rede** — não há sensor para instrumentar. E elas entregam σ, τ e a área corrigida
> já calculados, o que também dispensa a conversão de carga em tensão. O trabalho que sobra
> não é menor: é **outro**.

## O que aconteceu

O plano de trabalho foi escrito antes de alguém abrir um arquivo das máquinas. Ele supunha um
laboratório em que os equipamentos produzem sinal analógico e o aluno constrói a ponte entre
o sensor e o computador.

O laboratório real é outro. As máquinas gravam arquivos `.csv` sozinhas, e esses arquivos
estão acessíveis pela rede. Existem 1.081 deles, de maio de 2023 a agosto de 2026.

Com isso, três blocos inteiros do plano perdem o objeto — e dois problemas que o plano não
previa aparecem no lugar.

## A evidência

### O que sai do escopo, e por quê

| Previsto no plano | O que se verificou | Efeito |
| --- | --- | --- |
| Integrar sensores a um Raspberry Pi | As máquinas já digitalizam e gravam | Sai todo o módulo de hardware |
| Ler célula de carga e LVDT | Não há sinal cru a ler | Sai a calibração de transdutores |
| Converter carga → força → tensão | A máquina entrega σ e τ prontos, colunas 5 e 9 | Saem as semanas 12 e 13 |
| Corrigir a área em função do deslocamento | A máquina entrega a área corrigida, coluna 14 | Idem |
| Coleta manual dos arquivos | Máquinas em rede | Coleta vira cópia de arquivos |

As colunas citadas estão documentadas em `docs/arquitetura/formato-bruto.md` §2.2 e são
verificáveis em qualquer arquivo do acervo.

### O que entra no lugar

| Não previsto no plano | Por que apareceu |
| --- | --- |
| Módulo de *parsing* | O formato das máquinas era desconhecido e precisou ser mapeado |
| Triagem de qualidade dos ensaios | O acervo tem ensaios que não romperam, e a planilha não os pega |
| Agrupamento de arquivos em séries | Um arquivo = um ponto; nada no arquivo diz a que série pertence |
| Relatório em PDF com gráficos | O plano parava no cálculo |

### O que ficou sem dado

O plano trata cisalhamento direto e triaxial em pé de igualdade. **O acervo não tem um único
arquivo de ensaio triaxial.** A semana 8 do cronograma, que previa o parser do triaxial, está
marcada como bloqueada em `docs/plano/metas-semanais.md`: um parser escrito sem nenhum
arquivo real para rodar contra não pode ser testado.

### A interpretação

Nada disso é fracasso do plano. Um plano de PIBITI é escrito meses antes do trabalho começar
e com informação incompleta sobre o laboratório — descobrir que a realidade difere é o
resultado esperado das primeiras semanas, não um acidente.

O que muda é a natureza da contribuição. O trabalho deixa de ser construir a ponte entre
sensor e computador, e passa a ser: ler um formato proprietário, normalizar, triar o que
presta, calcular e relatar. **É engenharia de dados aplicada à geotecnia.**

## Como conferir

Este registro não tem número calculado — é uma decisão, não uma medição. O que dá para
conferir são as afirmações sobre os dados:

```
uv run python scripts/comparar_layouts.py
```

Mostra que as máquinas gravam arquivos prontos, com cabeçalho e colunas nomeadas, e que o
acervo tem 1.045 arquivos de cisalhamento e 36 de adensamento — nenhum de triaxial.

Que a máquina entrega σ, τ e área corrigida se confere abrindo qualquer arquivo do acervo e
olhando os nomes das colunas 5, 9 e 14, listados em `formato-bruto.md` §2.2.

## Por que isso importa

**Tem que ser dito ao orientador, não escondido.** O título do plano cita "aquisição (IoT)".
O sistema continua automatizando a aquisição, mas a partir dos arquivos que as máquinas já
produzem, e não de sensores crus. É uma simplificação defensável — e é o primeiro item da
lista de avisos em `docs/arquitetura/perguntas-orientador.md`.

**Libera tempo, e o tempo é o recurso escasso.** O orçamento é de 2 horas por semana, cerca
de 96 no ano. As semanas 12 e 13 e o bloco de hardware inteiro deixam de existir. Esse tempo
foi realocado para a triagem de qualidade, que é o que produz resultado publicável.

**Muda o que é o resultado do trabalho.** Um sistema que lê sensores é uma ferramenta. Um
sistema que lê 1.043 ensaios históricos, reprova os que não romperam e calcula c e φ produz
um resultado geotécnico sobre um acervo real — e um artigo.

## O que eu decidi

**Registrar a divergência em documento próprio, e deixar esse documento prevalecer sobre o
plano.** `docs/arquitetura/visao-geral.md` descreve o estado real; o plano fica no
repositório como o que foi submetido. Onde os dois divergirem, vale a visão geral.

A alternativa descartada era ajustar o plano de trabalho para refletir a realidade. Foi
rejeitada porque o plano é um documento submetido a uma instituição, com data — reescrevê-lo
apagaria o registro do que foi prometido, que é justamente o que o orientador e a banca
precisam poder comparar com o que foi feito.

Consequência assumida: dois documentos a manter, e a obrigação de dizer qual vale.

## Ligações

- **O estado real e todas as decisões:** `docs/arquitetura/visao-geral.md`, especialmente §1
  e §9.
- **O plano como foi submetido:** `docs/plano/PlanoTrabalho-PIBITI_4.md`.
- **O cronograma com as semanas riscadas e a semana 8 bloqueada:**
  `docs/plano/metas-semanais.md`.
- **O aviso a dar na reunião:** `docs/arquitetura/perguntas-orientador.md`, seção "Avisos a
  dar".
- **As colunas que a máquina já entrega prontas:** `docs/arquitetura/formato-bruto.md` §2.2 e
  §3.

## O que ficou em aberto

**O orientador ainda não foi avisado.** Toda esta mudança está registrada e justificada, mas
a conversa não aconteceu. Enquanto não acontecer, existe o risco de o trabalho seguir numa
direção que ele não aprova — e quanto mais tarde, mais caro corrigir.

**O triaxial pode voltar ao escopo a qualquer momento.** Basta aparecer um arquivo. Está
pedido: a semana 8 do `metas-semanais.md` traz o que pedir e por quê. Um arquivo só, mesmo de
ensaio antigo ou interrompido, basta para destravar.
