# Visão geral da arquitetura

_Última atualização: 11/09/2026_

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
| *(não previsto)* | Formato bruto das máquinas é desconhecido | **Entra** o módulo de *parsing* — hoje o maior risco do projeto |
| App desktop com GUI | — | **Adiado.** Ver §6 |
| *(não previsto)* | — | **Entra** geração de relatório em PDF com gráficos |

O trabalho deixou de ser *instrumentação* e passou a ser **engenharia de dados aplicada à
geotecnia**: ler um formato proprietário, normalizar, armazenar, calcular e relatar.

> Isso precisa ser comunicado ao orientador. O título do plano cita "aquisição (IoT)"; o
> sistema continua automatizando a aquisição, mas a partir dos arquivos que as máquinas já
> produzem, e não de sensores crus. É uma simplificação defensável e honesta — mas tem que
> ser dita, não escondida.

## 2. Fluxo do sistema

```
   Máquina de ensaio                (cisalhamento direto / triaxial)
          │  grava arquivo bruto — formato proprietário, ainda desconhecido
          ▼
   [1] coleta/       cópia dos arquivos da rede para dados/brutos/
          ▼
   [2] parsers/      bruto ──► DataFrame normalizado  ◄── PARTE MAIS ARRISCADA
          ▼
   [3] banco/        grava no banco (ensaio, corpo de prova, estágio, leitura)
          ▼
   [4] nucleo/       tensões, curvas, envoltória de Mohr-Coulomb, c e φ
          ▼
   [5] relatorio/    gráficos + PDF
```

Cada etapa é independente e testável sozinha. Nenhuma delas depende de hardware.

## 3. O bloqueio atual: o formato bruto

**Nada a jusante pode ser projetado sem ver um arquivo real.** O schema do banco depende das
colunas que existem; os cálculos dependem de quais grandezas a máquina já entrega prontas e
quais precisam ser derivadas.

Perguntas a responder no laboratório:

- [ ] Marca, modelo e software de cada máquina (direto e triaxial)
- [ ] Que formato o software exporta? (`.csv`, `.txt`, `.xls`, `.gds`, formato binário próprio)
- [ ] Existe opção "exportar para CSV/Excel" no menu do software?
- [ ] O arquivo tem cabeçalho com metadados (amostra, data, tensão confinante)?
- [ ] Unidades de cada coluna — N ou kgf? mm ou polegada? kPa ou bar?
- [ ] Separador decimal: vírgula ou ponto?
- [ ] Um arquivo por estágio ou um arquivo por ensaio completo?
- [ ] Como os arquivos ficam acessíveis pela rede? (pasta compartilhada, FTP, nuvem do fabricante)

**Ação:** salvar um arquivo de exemplo de cada ensaio em `dados/exemplos/bruto/` e rodar
`uv run python scripts/inspecionar.py <arquivo>` — ver §4.

## 4. Ferramenta de diagnóstico

`scripts/inspecionar.py` examina um arquivo desconhecido e reporta: codificação, separador,
onde acaba o cabeçalho, nomes e tipos de coluna, e as primeiras linhas de dados. Serve para
descobrir a estrutura sem ter que abrir o arquivo no Excel e adivinhar.

## 5. Formato normalizado (proposta preliminar)

Independente da máquina, todo ensaio vira duas coisas:

**Metadados do ensaio** — tipo (`direto` / `triaxial`), identificação da amostra, data,
operador, dimensões do corpo de prova, umidade, densidade, condição de drenagem (CD/CU/UU).

**Série temporal por estágio** — uma linha por instante de leitura:

| coluna | unidade | direto | triaxial |
| --- | --- | :---: | :---: |
| `t` | s | ✓ | ✓ |
| `desloc_horizontal` | m | ✓ | — |
| `desloc_vertical` | m | ✓ | ✓ |
| `forca_cisalhante` | N | ✓ | — |
| `forca_axial` | N | — | ✓ |
| `tensao_confinante` | Pa | — | ✓ |
| `poropressao` | Pa | — | ✓ |

Tudo em SI. A conversão para kPa/mm acontece só na hora de plotar e relatar.

> Esta tabela é um chute informado e **vai mudar** quando o arquivo real aparecer.

## 6. Banco de dados

Modelo preliminar:

- `ensaio` — metadados; um por ensaio completo
- `corpo_de_prova` — dimensões, umidade, densidade, índice de vazios
- `estagio` — cada tensão normal (direto) ou confinante (triaxial); N estágios por ensaio
- `leitura` — série temporal bruta, ligada ao estágio
- `resultado` — c, φ e tensões de ruptura calculadas

**Recomendação:** desenvolver contra **SQLite** e migrar para MySQL só no fim. O código
SQLAlchemy é idêntico — muda a string de conexão. SQLite é um arquivo, não exige servidor,
backup, usuário nem senha. Isso economiza várias horas de administração que, a 2h/semana,
valem mais aplicadas no que é o objeto da pesquisa. O plano promete MySQL, e MySQL será
entregue; só não no primeiro dia.

## 7. Interface

O plano fala em "aplicativo desktop". Uma GUI é cara: fácil passar 30h em layout, e nenhuma
dessas horas produz resultado geotécnico. Ordem proposta:

1. **CLI + relatório PDF** — `processar ensaio.csv` → PDF com curvas, envoltória, c e φ.
   Entrega todo o valor científico do projeto.
2. **GUI** — só se sobrar tempo depois do artigo. PyQt6 ou Streamlit, decidir na hora.

## 8. Validação

Comparação entre os resultados do sistema e o processamento manual em planilha dos mesmos
ensaios, com estatística descritiva (erro absoluto e relativo em c e φ). Precisa de pelo
menos 3 ensaios já processados manualmente — **pedir ao orientador os dados históricos do
laboratório**, para não depender de rodar ensaios novos.

## 9. Decisões registradas

| Data | Decisão | Motivo |
| --- | --- | --- |
| 11/09/2026 | Núcleo de cálculo isolado de GUI/banco/hardware | testar cálculos sem dependências |
| 11/09/2026 | Raspberry Pi removido do escopo | máquinas já digitalizam os dados |
| 11/09/2026 | SQLite no desenvolvimento, MySQL na entrega | economiza horas de administração |
| 11/09/2026 | CLI + PDF antes de GUI | GUI não produz resultado científico |
| 29/09/2026 | τ de cada ensaio lido a 10 mm de deslocamento, interpolado | é o critério do laboratório (`registros/2026-09-29-ruptura-a-10mm.md`) |
