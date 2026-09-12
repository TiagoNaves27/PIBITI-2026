# Visão geral da arquitetura

> **Status:** esqueleto. Preencher com o estado real do projeto — o plano de trabalho
> (`docs/plano/PlanoTrabalho-PIBIC_4.md`) descreve o escopo submetido, que já mudou.
> Quando houver divergência, **este documento vale**.

_Última atualização: 11/09/2026_

## 1. Escopo atual

<!-- O que mudou em relação ao plano de trabalho. Preencher. -->

- [ ] O que saiu do escopo:
- [ ] O que entrou:
- [ ] Em que mês do cronograma o projeto realmente está:

## 2. Camadas

### 2.1 Aquisição (`src/geotec/aquisicao/`)

Roda no Raspberry Pi. Lê os sensores das máquinas de ensaio e publica leituras com timestamp.

| Grandeza | Sensor | Ensaio | ADC / interface | Status |
| --- | --- | --- | --- | --- |
| Força / carga | célula de carga | direto + triaxial | ? | a definir |
| Deslocamento horizontal | LVDT / transdutor | direto | ? | a definir |
| Deslocamento vertical | LVDT / transdutor | direto + triaxial | ? | a definir |
| Poropressão | transdutor de pressão | triaxial | ? | a definir |
| Pressão confinante | transdutor de pressão | triaxial | ? | a definir |

Pontos em aberto: taxa de amostragem, calibração (curva sensor → unidade física),
comportamento em caso de queda de rede.

### 2.2 Armazenamento (`src/geotec/banco/`)

MySQL. Modelo preliminar:

- `ensaio` — metadados (tipo, amostra, data, operador, condições de contorno)
- `corpo_de_prova` — dimensões, umidade, densidade, índice de vazios
- `estagio` — cada tensão normal (direto) ou tensão confinante (triaxial) do ensaio
- `leitura` — série temporal bruta: `(estagio_id, t, canal, valor)`
- `resultado` — parâmetros calculados (c, φ, tensões de ruptura)

Decisões em aberto: banco local no Pi com sincronização, ou Pi escrevendo direto no
servidor; granularidade da tabela `leitura` (linha por canal vs. linha por instante).

### 2.3 Núcleo de cálculo (`src/geotec/nucleo/`)

Funções puras, sem dependência de GUI/banco/hardware.

- `cisalhamento_direto.py` — tensão normal e cisalhante, curvas τ × deslocamento,
  identificação do pico e do estado residual
- `triaxial.py` — tensões principais, deformação axial, correção de área,
  trajetórias de tensão, poropressão (Skempton A e B)
- `envoltoria.py` — regressão de Mohr-Coulomb → coesão (c) e ângulo de atrito (φ)
- `mohr.py` — círculos de Mohr e envoltória tangente

### 2.4 Aplicativo desktop (`src/geotec/app/`)

Framework **a definir** (PyQt6 / PySide6 / Tkinter / Streamlit). Requisitos conhecidos:
selecionar ensaio do banco, visualizar curvas, marcar ruptura, exportar gráficos e relatório.

## 3. Validação

Comparação dos resultados automáticos com o processamento manual dos mesmos ensaios,
via estatística descritiva. Conjunto de dados de referência a definir.

## 4. Decisões registradas

| Data | Decisão | Motivo |
| --- | --- | --- |
| 11/09/2026 | Estrutura `src/` com núcleo de cálculo isolado | permitir testar cálculos sem hardware nem banco |
