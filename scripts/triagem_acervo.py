"""Classifica os arquivos de cisalhamento direto do acervo em quatro situacoes.

Uso:
    uv run python scripts/triagem_acervo.py
    uv run python scripts/triagem_acervo.py --listar orfao

Reproduz os numeros do registro `docs/registros/2026-09-12-triagem-do-acervo.md`.
Existe para que esses numeros possam ser conferidos por quem ler o trabalho, em vez
de precisarem ser aceitos por confianca.

As quatro situacoes, definidas em `docs/arquitetura/formato-bruto.md` secao 5.1:

    utilizavel   etapa de cisalhamento com 5 ou mais leituras
    com_irmao    sem etapa de cisalhamento, mas existe outro arquivo de mesmo
                 `ID do ensaio` e mesma data que tem o cisalhamento
    orfao        sem etapa de cisalhamento e sem irmao
    curto        etapa de cisalhamento com 1 a 4 leituras

Apenas `orfao` e `curto` significam que alguma coisa deu errado. `com_irmao` e o
fluxo normal do laboratorio: adensamento salvo num arquivo, cisalhamento em outro.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from geotec.parsers import direto

ACERVO = Path(__file__).parents[1] / "dados" / "Ensaios-270" / "Cisalhamento"

# Abaixo disto a etapa de cisalhamento nao descreve uma curva; ver formato-bruto
# secao 5.4, criterio 2.
MINIMO_DE_LEITURAS = 5

SITUACOES = ("utilizavel", "com_irmao", "orfao", "curto")

ROTULOS = {
    "utilizavel": "Ensaio de cisalhamento utilizavel",
    "com_irmao": "So adensamento, com irmao de cisalhamento",
    "orfao": "So adensamento, orfao",
    "curto": "Cisalhamento com 1 a 4 leituras",
}


@dataclass(frozen=True)
class Triado:
    """Um arquivo do acervo com a situacao em que ele foi classificado."""

    caminho: Path
    numero_teste: int
    id_ensaio: str
    data: str
    leituras_cisalhamento: int
    situacao: str


def triar(pasta: Path = ACERVO) -> list[Triado]:
    """Le todo o acervo e classifica cada arquivo numa das quatro situacoes."""
    lidos = []
    for caminho in sorted(pasta.glob("*.csv")):
        ensaio = direto.ler(caminho)
        if ensaio.metadados.tipo_ensaio != "DS":
            continue
        etapas = ensaio.leituras["etapa"]
        lidos.append(
            (
                ensaio.metadados,
                int((etapas == "cisalhamento").sum()),
            )
        )

    # Quem tem cisalhamento de verdade, indexado por (ID do ensaio, dia). E a chave
    # que decide se um arquivo so de adensamento tem irmao ou esta orfao.
    com_cisalhamento = {
        (meta.id_ensaio, meta.inicio.date()) for meta, n in lidos if n >= MINIMO_DE_LEITURAS
    }

    triados = []
    for meta, n in lidos:
        if n >= MINIMO_DE_LEITURAS:
            situacao = "utilizavel"
        elif n == 0:
            tem_irmao = (meta.id_ensaio, meta.inicio.date()) in com_cisalhamento
            situacao = "com_irmao" if tem_irmao else "orfao"
        else:
            situacao = "curto"
        triados.append(
            Triado(
                caminho=meta.caminho,
                numero_teste=meta.numero_teste,
                id_ensaio=meta.id_ensaio,
                data=meta.inicio.strftime("%d/%m/%Y"),
                leituras_cisalhamento=n,
                situacao=situacao,
            )
        )
    return triados


def contar(triados: list[Triado]) -> dict[str, int]:
    contagem = dict.fromkeys(SITUACOES, 0)
    for t in triados:
        contagem[t.situacao] += 1
    return contagem


def main(argv: list[str]) -> int:
    if not ACERVO.is_dir():
        print(f"Acervo nao encontrado em {ACERVO}")
        return 1

    triados = triar()
    contagem = contar(triados)
    total = len(triados)

    print(f"\nAcervo de cisalhamento direto: {total} arquivos\n")
    largura = max(len(r) for r in ROTULOS.values())
    for situacao in SITUACOES:
        n = contagem[situacao]
        print(f"  {ROTULOS[situacao]:<{largura}}  {n:>5}  ({n / total:6.1%})")
    print(f"  {'':<{largura}}  {'-' * 5}")
    print(f"  {'total':<{largura}}  {total:>5}")

    descartes = total - contagem["utilizavel"]
    falhas = contagem["orfao"] + contagem["curto"]
    print(
        f"\n  Dos {descartes} descartes, {contagem['com_irmao']} sao fluxo normal do "
        f"laboratorio\n  e apenas {falhas} indicam que alguma coisa deu errado.\n"
    )

    if "--listar" in argv:
        alvo = argv[argv.index("--listar") + 1]
        print(f"Arquivos na situacao '{alvo}':\n")
        for t in sorted(triados, key=lambda t: t.numero_teste):
            if t.situacao == alvo:
                print(
                    f"  NT {t.numero_teste:>5}  {t.data}  {t.id_ensaio:<24}"
                    f"  {t.leituras_cisalhamento:>3} leituras"
                )
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
