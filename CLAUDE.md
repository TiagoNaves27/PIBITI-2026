# Contexto do projeto

PIBIC 2026 — sistema automatizado de coleta e análise de dados dos ensaios de
**cisalhamento direto** e **compressão triaxial**, para o grupo GeoFluxo (UnB).

Fluxo: `máquina grava arquivo bruto → coleta → parser → banco → cálculo → relatório PDF`.

As máquinas já digitalizam os dados e estão em rede. **Não há Raspberry Pi nem leitura de
sensores neste projeto** — isso saiu do escopo. Ver `docs/arquitetura/visao-geral.md` §1.

Documento oficial: `docs/plano/PlanoTrabalho-PIBIC_4.md`.
Estado real e decisões vigentes: `docs/arquitetura/visao-geral.md` — **este prevalece** quando
divergir do plano.

## Convenções

- **Idioma:** documentação, commits e nomes de módulos/funções em **português** (sem acentos em
  identificadores de código). Comentários em português.
- **Unidades:** SI internamente (N, m, Pa, s). Conversão para kPa/mm só na apresentação.
  Toda função que recebe ou devolve grandeza física declara a unidade no docstring.
- **Ângulos:** radianos internamente; graus apenas na interface e nos relatórios.
- Cálculos geotécnicos ficam em `src/geotec/nucleo/` e **não** importam nada de GUI ou banco
  — são funções puras sobre arrays/DataFrames, para poderem ser testadas.
- Cada máquina/formato ganha seu próprio módulo em `src/geotec/parsers/`. Todos devolvem o
  **mesmo** formato normalizado (`visao-geral.md` §5), para que nada a jusante saiba de qual
  máquina o dado veio.
- Banco: **SQLite no desenvolvimento, MySQL na entrega.** Use SQLAlchemy Core; o código não
  muda entre os dois, só a string de conexão.

## Ambiente

`uv` gerencia tudo. Python 3.14, Windows.

```
uv sync            uv run pytest            uv run ruff check .
```

Nunca commitar `.env`, dados brutos de ensaio ou PDFs de referência.

## Ao trabalhar aqui

- Cada função de cálculo novo precisa de teste com valor de referência conferido à mão
  ou vindo de exemplo de norma/livro (ASTM, Head, Pinto, Das).
- Ao mudar escopo/arquitetura, atualizar `docs/arquitetura/visao-geral.md` no mesmo passo.
