# Formato bruto das máquinas

_Última atualização: 12/09/2026 — a partir dos 1.081 arquivos de `dados/Ensaios-270/`_

## 1. O acervo

| Pasta | Ensaio | Arquivos | Tamanho |
| --- | --- | ---: | ---: |
| `Cisalhamento/` | cisalhamento direto (DS) | 1.043 | 18 MB |
| `Adensamento/` | adensamento / oedométrico (ODC) | 36 | 19 MB |
| `DSS/` | cisalhamento simples direto | 2 | 184 KB |

Período: **maio/2023 a agosto/2026**. Nenhum ensaio triaxial ainda.

Nome do arquivo: `AAAA-MM-DD HH-MM-SS - NT <n> - <tipo> - ID <id>.csv`
(`NT` = número do teste, sequencial e único; `DS` / `ODC` = tipo de ensaio).

## 2. Estrutura do arquivo (cisalhamento direto)

**100% consistente nos 1.043 arquivos** — mesma codificação, mesmo separador, mesmas 7
chaves de cabeçalho, mesmas 17 colunas. Nenhuma exceção encontrada.

| Propriedade | Valor |
| --- | --- |
| Codificação | UTF-8 |
| Separador de campo | `;` |
| Separador decimal | `,` (vírgula) |
| Linhas de metadados | 7 |
| Linha de nomes de coluna | 8 |
| Dados | a partir da linha 9 |

```python
import pandas as pd
df = pd.read_csv(caminho, sep=";", skiprows=7, decimal=",")
```

### 2.1 Cabeçalho (linhas 1-7, formato `chave;valor`)

| Chave | Exemplo | Observação |
| --- | --- | --- |
| `Numero do Teste` | `1151` | sequencial, único no laboratório |
| `ID do ensaio` | `D8N16V1` | identificação do operador — ver §4 |
| `Formato CP` | `Cilindrico` | |
| `Tipo de Controle` | `Tensao` | |
| `Dimensao Secao [mm]` | `60` | diâmetro do corpo de prova |
| `Altura Inicial [mm]` | `21,5` | |
| `Tempo de aquisicao` | `Personalizado` | |

### 2.2 Colunas de dados (17)

| # | Coluna | Unidade |
| ---: | --- | --- |
| 1 | Data | dd/mm/aaaa |
| 2 | Hora | hh:mm:ss |
| 3 | **Etapa** | `Adensamento` ou `Cisalhamento` |
| 4 | Tempo Etapa | min |
| 5 | **Tensao Normal** | kPa |
| 6 | Deslocamento Normal | mm |
| 7 | Altura Atual | mm |
| 8 | Deformacao Normal | % |
| 9 | **Tensao Cisalhante** | kPa |
| 10 | **Deslocamento Cisalhante** | mm |
| 11 | Deformacao Cisalhante | % |
| 12 | Tempo Ensaio | min |
| 13 | Velocidade Cisalhamento | mm/min |
| 14 | **Area Corrigida** | mm² |
| 15 | Carga Vertical | kg |
| 16 | Carga Horizontal | kg |
| 17 | Carga Horizontal Absoluta | kg |

## 3. Consequência para o projeto

**A máquina já entrega σ, τ e a área corrigida calculados.** Isso elimina do escopo:

- conversão de célula de carga → força → tensão
- correção de área em função do deslocamento (coluna 14)
- as semanas 12 e 13 do plano original

O que **sobra** para o sistema fazer, e que é o trabalho de verdade:

1. **Agrupar** arquivos avulsos nas séries que formam uma envoltória (§4)
2. **Filtrar** ensaios abortados e leituras espúrias (§5)
3. Localizar **τ de pico** na etapa `Cisalhamento` de cada arquivo
4. Regredir os pares (σ, τ) → **c** e **φ**
5. Gerar curvas e relatório

> Um arquivo = **um** corpo de prova sob **uma** tensão normal. Uma envoltória exige
> agrupar 3 ou mais arquivos. O agrupamento não está gravado em lugar nenhum — é a
> informação que falta, e ela está na cabeça do operador.

## 4. Nomenclatura do `ID do ensaio` — HIPÓTESE A CONFIRMAR

Padrão observado: `D<amostra><condição><tensão>[repetição][V<velocidade>]`

```
D8  N   16   V1
│   │   │    └── velocidade de cisalhamento: V05=0,5  V1=1,0  V25=0,25 mm/min
│   │   └─────── tensão normal em dezenas de kPa: 8=80  12=120  16=160  2=200
│   │            3=300  4=400  45=450  5=500  6=600
│   │            (campanha de 2024 usava kPa cheios: D8N160, D8N320, D8N640)
│   └─────────── condição do corpo de prova: N, S, U, W, A
└─────────────── amostra: D1, D7, D8, D9
```

Matriz de ensaios encontrada — 4 amostras × 5 condições:

| | N | S | U | W | A |
| --- | ---: | ---: | ---: | ---: | ---: |
| **D1** | 25 | 12 | — | 29 | — |
| **D7** | 29 | 39 | 16 | 32 | 1 |
| **D8** | 75 | 30 | 21 | 30 | 3 |
| **D9** | 83 | 11 | 2 | 40 | — |

Verificações que sustentam a hipótese:

- a tensão normal aplicada bate com o número do ID em praticamente todos os casos
- o sufixo `V` bate com a coluna `Velocidade Cisalhamento` (V05 → 0,500 mm/min,
  V1 → 1,000, V25 → 0,250)
- dígito final extra indica repetição: `D9N51`, `D9N52`, `D9N53` são três ensaios a 500 kPa

**Perguntas em aberto para o aluno/orientador:**

- [ ] O que significam `D1`, `D7`, `D8`, `D9`? (amostras distintas? densidades? profundidades?)
- [ ] O que significam `N`, `S`, `U`, `W`, `A`? (natural / saturado / úmido / …?)
- [ ] A regra de agrupamento **mesma amostra + mesma condição + mesmo dia de ensaio**
      está correta para montar uma envoltória?
- [ ] τ de pico deve ser o máximo da curva, ou lido a uma deformação especificada?

## 5. Qualidade dos dados

| Achado | Quantidade | Tratamento proposto |
| --- | ---: | --- |
| Ensaios abortados (etapa `Cisalhamento` com < 5 pontos ou σ = 0) | 129 de 1.043 | descartar no parser, registrando o motivo |
| Leituras espúrias | ≥ 1 confirmada | ver abaixo |

Exemplo de leitura espúria — série `D1N` de 30/09/2024:

```
sigma:    20    80   120    160    200   300   400   500  kPa
tau:    31,0  68,0  95,7  1755,3  170,8 233,9 269,1 336,4  kPa
                          ^^^^^^ fisicamente impossível
```

O parser precisa detectar isso. Tomar τ de pico como máximo bruto propagaria o erro
direto para a envoltória. **Isto é conteúdo para o artigo**: o processamento manual em
planilha dificilmente pega esse tipo de erro, e o sistema automatizado pega.

## 6. Material de validação disponível

Aplicando a regra de agrupamento do §4 e descartando os abortados:

> **51 envoltórias completas** (≥ 3 tensões normais, mesma amostra/condição, mesmo dia),
> várias com 8 ou 9 pontos.

O plano previa pedir ao orientador 3 ensaios já processados manualmente. Há muito mais que
isso aqui — falta apenas obter os resultados manuais (c e φ) de alguns deles para comparar.

A campanha de 2026 varia a **velocidade de cisalhamento** a σ constante de 160 kPa
(`D8N16V1`, `V25`, `V5`, `D8S1V05`…). É um segundo eixo de análise, além da envoltória.
