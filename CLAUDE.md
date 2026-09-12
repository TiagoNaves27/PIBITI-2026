# Contexto do projeto

PIBIC 2026 — sistema de aquisição automática (Raspberry Pi / IoT) e análise de dados dos
ensaios de **cisalhamento direto** e **compressão triaxial**, para o grupo GeoFluxo (UnB).

Fluxo: `sensores → Raspberry Pi → MySQL → app desktop Python`.

Documento oficial: `docs/plano/PlanoTrabalho-PIBIC_4.md`.
Estado real e decisões vigentes: `docs/arquitetura/visao-geral.md` — **este prevalece** quando
divergir do plano.

## Convenções

- **Idioma:** documentação, commits e nomes de módulos/funções em **português** (sem acentos em
  identificadores de código). Comentários em português.
- **Unidades:** SI internamente (N, m, Pa, s). Conversão para kPa/mm só na apresentação.
  Toda função que recebe ou devolve grandeza física declara a unidade no docstring.
- **Ângulos:** radianos internamente; graus apenas na interface e nos relatórios.
- Cálculos geotécnicos ficam em `src/geotec/nucleo/` e **não** importam nada de GUI, banco
  ou hardware — são funções puras sobre arrays/DataFrames, para poderem ser testadas.
- Código que depende do Raspberry Pi fica isolado em `src/geotec/aquisicao/` atrás de uma
  interface, para que o resto rode no Windows sem o hardware.

## Ambiente

`uv` gerencia tudo. Python 3.14 no Windows (dev), Raspberry Pi OS (aquisição).

```
uv sync            uv run pytest            uv run ruff check .
```

Nunca commitar `.env`, dados brutos de ensaio ou PDFs de referência.

## Ao trabalhar aqui

- Cada função de cálculo novo precisa de teste com valor de referência conferido à mão
  ou vindo de exemplo de norma/livro (ASTM, Head, Pinto, Das).
- Ao mudar escopo/arquitetura, atualizar `docs/arquitetura/visao-geral.md` no mesmo passo.
