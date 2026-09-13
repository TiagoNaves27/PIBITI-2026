# Visão geral da arquitetura

_Última atualização: 12/09/2026_

Este documento descreve o **estado real** do projeto. O plano de trabalho
(`docs/plano/PlanoTrabalho-PIBITI_4.md`) é o documento submetido ao PIBITI e já divergiu do
que será feito. **Quando houver conflito, este documento vale.**

---

## 1. O que mudou em relação ao plano submetido

| Plano original | Realidade | Efeito |
| --- | --- | --- |
| Integrar sensores a um Raspberry Pi | As máquinas já digitalizam e gravam os dados | **Sai** todo o módulo de hardware |
| Programar rotinas de leitura de célula de carga / LVDT | Nada disso é necessário | **Sai** a calibração de transdutores |
| Coleta manual dos arquivos | Máquinas conectadas à rede | Coleta vira cópia/sync de arquivos |
| *(não previsto)* | Formato bruto era desconhecido | **Entrou** o módulo de *parsing* — **resolvido em 12/09/2026**, ver §3 |
| Converter carga → força → tensão; corrigir área | A máquina já entrega σ, τ e área corrigida | **Sai** — eram as semanas 12 e 13 |
| Triaxial tratado em pé de igualdade com o direto | O acervo não tem **nenhum** ensaio triaxial | **Adiado** por falta de dado. Ver §5.3 |
| App desktop com GUI | — | **Adiado.** Ver §7 |
| *(não previsto)* | Um arquivo = um σ; a série não está gravada em lugar nenhum | **Entrou** o agrupamento — hoje o maior risco. Ver §3 |
| *(não previsto)* | — | **Entra** geração de relatório em PDF com gráficos |

O trabalho deixou de ser *instrumentação* e passou a ser **engenharia de dados aplicada à
geotecnia**: ler um formato proprietário, normalizar, armazenar, calcular e relatar.

> Isso precisa ser comunicado ao orientador. O título do plano cita "aquisição (IoT)"; o
> sistema continua automatizando a aquisição, mas a partir dos arquivos que as máquinas já
> produzem, e não de sensores crus. É uma simplificação defensável e honesta — mas tem que
> ser dita, não escondida. O roteiro da conversa está em `perguntas-orientador.md`.

## 2. Fluxo do sistema

```
   Máquina de ensaio           (cisalhamento direto; triaxial ainda sem dado)
          │  grava CSV — formato conhecido e estável, ver formato-bruto.md
          ▼
   [1] coleta/       cópia dos arquivos da rede para dados/
          ▼
   [2] parsers/      CSV bruto ──► metadados + série temporal em SI
          ▼
   [3] nucleo/       qualidade: descarta / sinaliza o ensaio que não rompeu
          ▼
   [4] agrupador/    arquivos avulsos ──► séries que formam uma envoltória  ◄── MAIS ARRISCADO
          ▼
   [5] banco/        grava (serie, ensaio, leitura, ocorrencia, resultado)
          ▼
   [6] nucleo/       τ de pico por ensaio; regressão (σ, τ) ──► c e φ
          ▼
   [7] relatorio/    gráficos + PDF
```

Cada etapa é independente e testável sozinha. Nenhuma delas depende de hardware.

A ordem mudou em relação à versão anterior deste documento: **qualidade e agrupamento entram
antes do banco**, porque são eles que decidem o que é um ensaio válido e o que é uma série —
e o banco precisa dessa resposta para ter chaves estrangeiras com significado.

## 3. O bloqueio atual: o agrupamento

O bloqueio antigo era o formato bruto. **Ele caiu.** Os 1.081 arquivos do acervo estão em
`dados/Ensaios-270/` e `docs/arquitetura/formato-bruto.md` descreve o formato: CSV, separador
`;`, decimal com vírgula, UTF-8 com BOM, 7 linhas de cabeçalho e 17 colunas — 100% consistente
nos 1.043 arquivos de cisalhamento direto.

O bloqueio novo é outro, e é pior, porque a informação que falta **não está em nenhum
arquivo**:

> Um arquivo = **um** corpo de prova sob **uma** tensão normal. Uma envoltória de
> Mohr-Coulomb exige agrupar 3 ou mais arquivos. Nada no arquivo diz a que série ele
> pertence.

A regra provisória — mesma amostra + mesma condição + mesmo dia — produz 51 envoltórias
candidatas, mas quebra quando a série atravessa dois dias e não separa a campanha de material
cimentado da de solo natural. Agrupar errado é pior do que não agrupar: sai um c e um φ de
aparência perfeitamente normal, calculados sobre corpos de prova que não deviam estar juntos.
Não dá erro na tela e não aparece no gráfico.

**Só o laboratório responde isso.** As perguntas estão preparadas em
`perguntas-orientador.md`. O que cada uma trava:

| Pergunta | O que fica travado |
| --- | --- |
| Q1 — regra de agrupamento | `agrupador/`, a tabela `serie`, e todo resultado de c e φ |
| Q4 — como ler o τ de pico | a função que reduz cada ensaio a um ponto (σ, τ) |
| Q2/Q3 — o que são N/S/U/W/A e D1/D7/D8/D9 | rótulo dos gráficos e a unidade de análise do relatório |
| Q6 — c e φ calculados à mão | a validação do §8 — sem isso não há artigo |
| Q7 — o que são os 108 arquivos com irmão | como o sistema trata 10% do acervo, e se o dado de adensamento deles é aproveitável |

**O que não está travado, e deve ser escrito já:** o parser (§5) e a rotina de qualidade.
Os dois trabalham em um arquivo por vez e não dependem de nenhuma dessas respostas.

## 4. Ferramenta de diagnóstico

`scripts/inspecionar.py` examina um arquivo desconhecido e reporta: codificação, separador,
onde acaba o cabeçalho, nomes e tipos de coluna, e as primeiras linhas de dados.

Ele já cumpriu o papel no cisalhamento direto — o resultado virou o `formato-bruto.md`. Fica
no repositório para quando aparecer o primeiro arquivo de triaxial, que será de novo um
formato desconhecido.

## 5. Formato normalizado

Não é mais proposta: sai das 17 colunas reais. Independente da máquina, todo arquivo vira
**metadados** + **série temporal**, tudo em SI. A conversão para kPa/mm/min acontece só na
hora de plotar e relatar.

### 5.1 Metadados do ensaio

| campo | unidade | origem |
| --- | --- | --- |
| `numero_teste` | — | cabeçalho `Numero do Teste`; sequencial e único no laboratório |
| `id_ensaio` | — | cabeçalho `ID do ensaio`; identifica, mas **não mede** — ver abaixo |
| `tipo_ensaio` | — | nome do arquivo (`DS` / `ODC`) |
| `inicio` | datetime | nome do arquivo, conferido contra a 1ª linha de dados |
| `diametro` | m | cabeçalho `Dimensao Secao [mm]` |
| `altura_inicial` | m | cabeçalho `Altura Inicial [mm]` |
| `formato_cp`, `tipo_controle` | — | cabeçalho, texto |

**Ler a geometria de cada arquivo; nunca fixar no código.** O diâmetro é 60 mm em 1.028 dos
1.043, mas a campanha cimentada `B2-30D-*` usa molde de ~42 mm e a campanha `CAT` grava a
medida real do corpo de prova (59,89 / 60,10 mm). A altura inicial varia de 20 a 25 mm entre
corpos de prova, inclusive dentro de uma mesma amostra.

**O `id_ensaio` não é fonte de grandeza física.** O NT 614 tem `ID D1N16` — que pela
nomenclatura do `formato-bruto.md` §4 seria 160 kPa — e a máquina registrou σ = 22 kPa. σ vem
sempre da coluna de dados (§5.5 daquele documento).

### 5.2 Série temporal — uma linha por leitura

| coluna | unidade | origem (coluna bruta) |
| --- | --- | --- |
| `t` | s | `Tempo Ensaio [min]` × 60 |
| `t_etapa` | s | `Tempo Etapa [min]` × 60 |
| `etapa` | categoria | `Etapa` — `adensamento` ou `cisalhamento` |
| `tensao_normal` | Pa | `Tensao Normal [kPa]` × 10³ |
| `tensao_cisalhante` | Pa | `Tensao Cisalhante [kPa]` × 10³ |
| `desloc_normal` | m | `Deslocamento Normal [mm]` × 10⁻³ |
| `desloc_cisalhante` | m | `Deslocamento Cisalhante [mm]` × 10⁻³ |
| `altura_atual` | m | `Altura Atual [mm]` × 10⁻³ |
| `area_corrigida` | m² | `Area Corrigida [mm2]` × 10⁻⁶ |
| `carga_vertical` | N | `Carga Vertical [kg]` × 9,80665 |
| `carga_horizontal` | N | `Carga Horizontal [kg]` × 9,80665 |
| `velocidade` | m/s | `Velocidade Cisalhamento [mm/min]` ÷ 60.000 |

As colunas brutas `Data`, `Hora`, `Deformacao Normal [%]`, `Deformacao Cisalhante [%]` e
`Carga Horizontal Absoluta [kg]` **não entram**: as duas primeiras já estão em `inicio` + `t`,
as deformações são deriváveis de `desloc / altura_inicial`, e a carga absoluta é redundante.
Quem precisar delas que calcule — gravar grandeza derivada é convite para ela divergir da
origem.

A coluna `Carga [kg]` da máquina é leitura em **kgf**, não massa; daí a conversão por g. Ela
é redundante com tensão × área no ensaio normal, mas **é o sinal que denuncia travamento
mecânico** (`formato-bruto.md` §5.2), então fica.

### 5.3 E o triaxial?

A tabela acima descreve o cisalhamento direto, que é o que existe. O triaxial precisaria de
`forca_axial`, `tensao_confinante` e `poropressao` — e **não há um único arquivo triaxial no
acervo**. Essas colunas seriam especulação, e um parser que não pode ser rodado contra
nenhum arquivo real não é código, é rascunho. Entra quando o primeiro arquivo entrar.

## 6. Banco de dados

Modelo revisado. A diferença para a versão anterior é a tabela `serie`: antes se supunha que
um ensaio continha N estágios, um por tensão normal. **É o contrário** — cada arquivo é um
corpo de prova sob um único σ, e é a *série* que reúne os N.

- `serie` — o agrupamento que forma uma envoltória. **Não existe no dado bruto**: é produzida
  pelo sistema (§3). Precisa guardar *como* foi produzida — regra automática ou confirmação
  humana — porque um c e um φ obtidos sobre agrupamento adivinhado não valem o mesmo que
  sobre um agrupamento conferido.
- `ensaio` — um arquivo: os metadados do §5.1 e a ligação (opcional) com uma `serie`.
- `leitura` — a série temporal do §5.2, ligada ao `ensaio`, com a `etapa` como coluna.
- `ocorrencia` — descarte ou sinalização, **com o motivo** (`formato-bruto.md` §5.4). Dois dos
  quatro motivos de descarte não são falha de ensaio; espremer isso num booleano `valido`
  perde exatamente a informação que interessa ao artigo.
- `resultado` — c, φ, R² e o τ de pico de cada ponto, por `serie`.

**SQLite no desenvolvimento, MySQL na entrega.** O código SQLAlchemy é idêntico — muda a
string de conexão. SQLite é um arquivo: não exige servidor, backup, usuário nem senha. Isso
economiza horas de administração que, a 2h/semana, valem mais aplicadas no objeto da pesquisa.
O plano promete MySQL, e MySQL será entregue; só não no primeiro dia.

## 7. Interface

O plano fala em "aplicativo desktop". Uma GUI é cara: fácil passar 30h em layout, e nenhuma
dessas horas produz resultado geotécnico. Ordem proposta:

1. **CLI + relatório PDF** — `processar <arquivos>` → PDF com curvas, envoltória, c e φ.
   Entrega todo o valor científico do projeto.
2. **GUI** — só se sobrar tempo depois do artigo. PyQt6 ou Streamlit, decidir na hora.

## 8. Validação

Comparação entre os resultados do sistema e o processamento manual em planilha dos mesmos
ensaios, com estatística descritiva (erro absoluto e relativo em c e φ).

O plano previa pedir ao orientador 3 ensaios já processados manualmente, com receio de faltar
material. **Material sobra:** a regra provisória de agrupamento já produz 51 envoltórias
candidatas, várias com 8 ou 9 pontos. O que falta é o outro lado da comparação — o **c e o φ
que o laboratório calculou à mão** para alguns desses ensaios (Q6). Sem isso não há validação,
e sem validação não há artigo.

Há ainda um segundo eixo de análise que o plano não previa: a campanha de 2026 varia a
**velocidade de cisalhamento** a σ constante de 160 kPa.

## 9. Decisões registradas

| Data | Decisão | Motivo |
| --- | --- | --- |
| 11/09/2026 | Núcleo de cálculo isolado de GUI/banco/hardware | testar cálculos sem dependências |
| 11/09/2026 | Raspberry Pi removido do escopo | máquinas já digitalizam os dados |
| 11/09/2026 | SQLite no desenvolvimento, MySQL na entrega | economiza horas de administração |
| 11/09/2026 | CLI + PDF antes de GUI | GUI não produz resultado científico |
| 12/09/2026 | Conversão carga→tensão e correção de área saem do escopo | a máquina já entrega σ, τ e área corrigida |
| 12/09/2026 | Triaxial adiado até existir arquivo | parser sem arquivo real não é testável |
| 12/09/2026 | `serie` vira entidade do banco, com procedência do agrupamento | o agrupamento é produzido pelo sistema, não lido do dado |
| 12/09/2026 | Motivo do descarte é registrado, não é booleano | 2 dos 4 motivos não são falha de ensaio |
| 12/09/2026 | Grandeza derivada não é gravada (deformação, carga absoluta) | evita divergir da origem |
| 12/09/2026 | Geometria do corpo de prova é lida de cada arquivo | 15 arquivos fogem dos 60 mm |
| 12/09/2026 | Parser e qualidade avançam sem esperar o orientador | trabalham num arquivo por vez; independem do agrupamento |
