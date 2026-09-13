# Formato bruto das máquinas

_Última atualização: 12/09/2026 — a partir dos 1.081 arquivos de `dados/Ensaios-270/`_
_§5 reescrito após varredura completa das curvas._

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
| Codificação | UTF-8 **com BOM** — nos 1.043 arquivos, sem exceção |
| Separador de campo | `;` |
| Separador decimal | `,` (vírgula) |
| Linhas de metadados | 7 |
| Linha de nomes de coluna | 8 |
| Dados | a partir da linha 9 |

```python
import pandas as pd
df = pd.read_csv(caminho, sep=";", skiprows=7, decimal=",", encoding="utf-8-sig")
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

_Seção reescrita em 12/09/2026 a partir da varredura dos 1.043 arquivos. A versão anterior
falava em "129 ensaios abortados" e numa "leitura fisicamente impossível" — as duas
descrições estavam erradas, e o motivo de cada uma está registrado abaixo._

### 5.1 Os 1.043 arquivos, classificados

| Classe | Arquivos | O que o parser faz |
| --- | ---: | --- |
| Ensaio de cisalhamento utilizável | 914 | processa |
| Arquivo só de adensamento, **com** irmão de cisalhamento | 108 | ignora na envoltória; dado de adensamento aproveitável |
| Arquivo só de adensamento, **órfão** | 17 | descarta, registrando o motivo |
| Cisalhamento com 1 a 4 pontos | 4 | descarta, registrando o motivo |

Os 129 descartes da versão anterior eram estas três últimas linhas somadas. **A maioria não
é falha de ensaio:** 108 dos 125 arquivos sem etapa de cisalhamento têm um arquivo irmão, de
mesmo `ID do ensaio` e mesma data, que contém o cisalhamento correspondente. É o fluxo de
trabalho do laboratório — adensamento salvo em um arquivo, cisalhamento em outro — e não um
ensaio perdido. O critério de descarte precisa registrar *qual* dos quatro motivos se aplica,
porque só dois deles significam que alguma coisa deu errado.

Os 4 arquivos com 1 a 4 pontos duraram de 2 a 18 segundos e menos de 0,15 mm de
deslocamento. Dois são de maio/2023 com `ID MOVIMENTO` — teste de máquina, não ensaio.

### 5.2 Ensaios interrompidos antes da ruptura

Curso normal de um ensaio: **15 a 28 mm** de deslocamento cisalhante, 22 pontos na mediana.
**13 ensaios param antes de 5 mm.** Nesses, o τ máximo registrado não é resistência — é
apenas onde a máquina estava quando o ensaio foi interrompido.

Entre eles há **três com assinatura de travamento mecânico**: a curva não rompe, ela
*acelera* até o último ponto, com rigidez final várias vezes maior que a mediana do próprio
ensaio.

| Ensaio | σ (kPa) | τ final (kPa) | Deslocamento | Rigidez final / mediana | Desloc. normal |
| --- | ---: | ---: | ---: | ---: | ---: |
| NT 268 `B2-1D-400D` | 399 | 794 | 3,3 mm | 41× | +1,14 mm |
| NT 608 `D1N16` | 160 | 1.755 | 3,7 mm | 5,0× | −0,96 mm |
| NT 625 `D7W4` | 400 | 1.457 | 3,8 mm | 3,8× | −0,70 mm |

Os três gravaram exatamente **13 pontos** — mesmo ponto de interrupção, mesma reação do
operador. Em dois deles o deslocamento normal **inverte de sinal**: o corpo de prova sobe
em vez de adensar, o que não é dilatância (400 dos 914 ensaios terminam com deslocamento
normal negativo) mas acompanha uma carga horizontal desproporcional.

Detalhe do NT 608, o caso mais extremo. Carga horizontal de **486 kg** contra 35 a 50 kg
nos ensaios vizinhos da mesma série; curva subindo `43 → 63 → 120 → 212 → 356 → 1.229 →
1.755` sem nenhum pico. Carga que cresce sem limite enquanto a amostra é levantada é o que
se espera quando **a caixa bipartida não está livre** — parafusos de travamento não
retirados, fim de curso, ou inclusão rígida no plano de ruptura. A máquina mediu a reação
do equipamento, não a resistência do solo.

Série `D1N` de 30/09/2024, para dimensionar o desvio:

```
sigma:    22    80   120     160     200    300    400    500   kPa
tau:    31,0  68,0  95,7  1755,3   170,8  233,9  269,1  336,4   kPa
desloc: 28,3  28,0  28,0     3,7    28,3   27,5   28,2   29,0   mm
                          ^^^^^^ interrompido; esperado ~133 kPa
```

O ponto de 160 kPa dessa série **não existe**: o NT 608 travou, e a repetição do dia
seguinte (NT 617, 01/10/2024) também foi interrompida cedo — parou em 1,90 mm com τ = 83
kPa, ainda subindo. A série vai para a regressão com 7 pontos, não 8.

### 5.3 Por que "τ alto" não serve como critério

211 ensaios têm τ > 1,2·σ, o que daria um φ aparente acima de 50°. **Quase todos são
legítimos.** A campanha `B*`/`SP*` de 2024 traz o número de dias de cura no ID
(`B5-45D-50KPA` = 45 dias) e é material cimentado, com coesão de centenas de kPa.

O NT 296 (`B5-45D-50K`, σ = 50 kPa) chega a τ = 1.182 kPa — razão 23 — e é um ensaio bom:

```
12 → 19 → 28 → 58 → 97 → 195 → 631 → 1002 → 1182 → 734 → 296 → 35 → 29 → 24
                                            pico     ruptura fragil    residual
```

Ele **rompe**: sobe, quebra e cai para 35 kPa. É a curva esperada de um solo-cimento.
Comparar com o NT 608, que tem razão 11 e é lixo, mostra que a magnitude de τ não separa um
do outro — **a forma da curva separa**.

> Consequência para o §4: material cimentado e solo natural não podem cair na mesma
> envoltória. O agrupamento tem que distinguir campanha, não só amostra e data.

### 5.4 Critério proposto para o parser

Descartar da envoltória, sempre registrando o motivo:

1. arquivo sem etapa `Cisalhamento` (com ou sem irmão);
2. etapa `Cisalhamento` com menos de 5 pontos;
3. **τ de pico no último ponto registrado E deslocamento final < 5 mm** — o ensaio não rompeu.

A terceira condição precisa dos **dois** testes juntos. "Pico no último ponto" sozinho pega
471 dos 914 ensaios, porque muito solo endurece até o fim do curso sem pico definido;
combinado com o deslocamento curto, sobram 9 ensaios, que são os que merecem olhar humano.

Sinais adicionais para **sinalizar sem descartar** (marcar para revisão):

- rigidez do último trecho > 3× a mediana do ensaio (curva acelerando, não rompendo);
- τ de pico fora da tendência dos outros ensaios da mesma série por mais de uma ordem de
  grandeza;
- deslocamento normal invertendo de sinal junto com carga horizontal atípica.

**Isto é conteúdo para o artigo.** O processamento manual em planilha lê o máximo da coluna
de τ e não tem como perceber que a curva nunca rompeu; o sistema automatizado compara a
forma da curva com a do resto da série e reprova o ensaio. Os três travamentos encontrados
sobreviveriam a uma conferência manual desatenta.

### 5.5 O `ID do ensaio` não é fonte confiável

O NT 614 tem `ID D1N16`, que pela nomenclatura do §4 seria 160 kPa. A máquina registrou
**σ = 22 kPa**. O operador reaproveitou o ID do ensaio anterior e não trocou.

> **A tensão normal vem sempre da coluna de dados, nunca do nome.** O ID serve para
> agrupar e identificar amostra e condição — e mesmo para isso precisa ser conferido
> contra σ medido.

## 6. Material de validação disponível

Aplicando a regra de agrupamento do §4 e descartando os abortados:

> **51 envoltórias completas** (≥ 3 tensões normais, mesma amostra/condição, mesmo dia),
> várias com 8 ou 9 pontos.

Esse número é **estimativa superior**: foi obtido antes do critério 3 do §5.4 e sem separar a
campanha cimentada da de solo natural. Contar de novo depois que o orientador confirmar a
regra de agrupamento — a série `D1N` de 30/09/2024, por exemplo, perde um dos 8 pontos.

O plano previa pedir ao orientador 3 ensaios já processados manualmente. Há muito mais que
isso aqui — falta apenas obter os resultados manuais (c e φ) de alguns deles para comparar.

A campanha de 2026 varia a **velocidade de cisalhamento** a σ constante de 160 kPa
(`D8N16V1`, `V25`, `V5`, `D8S1V05`…). É um segundo eixo de análise, além da envoltória.
