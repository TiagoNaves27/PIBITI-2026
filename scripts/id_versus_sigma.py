"""Mede se o `ID do ensaio` e confiavel como fonte da tensao normal.

Uso:
    uv run python scripts/id_versus_sigma.py
    uv run python scripts/id_versus_sigma.py --id D1N16

Reproduz os numeros do registro `docs/registros/2026-09-12-id-nao-e-dado.md`.

O `ID do ensaio` e digitado pelo operador e, pela nomenclatura documentada em
`formato-bruto.md` secao 4, parece anunciar a tensao normal do ensaio: `D1N16`
seria amostra D1, condicao N, 160 kPa.

Este script NAO tenta decodificar a nomenclatura -- decodificar exigiria assumir
que a hipotese esta certa, que e justamente o que esta em questao. Ele faz uma
pergunta que nao depende de hipotese nenhuma:

    dois ensaios com o MESMO ID tem a mesma tensao normal medida?

Se o ID determinasse sigma, a resposta seria sim em todos os casos. Onde a
resposta e nao, o ID nao esta descrevendo o ensaio que o arquivo contem.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from geotec.parsers import direto

ACERVO = Path(__file__).parents[1] / "dados" / "Ensaios-270" / "Cisalhamento"

MINIMO_DE_LEITURAS = 5
# Dois ensaios sob a mesma tensao nominal variam alguns kPa entre si; acima disto
# nao e variacao de maquina, e outro ensaio.
TOLERANCIA_KPA = 15.0


def medir(pasta: Path = ACERVO) -> dict[str, list[tuple[int, str, float]]]:
    """Agrupa por `ID do ensaio` e guarda (NT, data, sigma medido em kPa)."""
    por_id: dict[str, list[tuple[int, str, float]]] = defaultdict(list)
    for caminho in sorted(pasta.glob("*.csv")):
        ensaio = direto.ler(caminho)
        if ensaio.metadados.tipo_ensaio != "DS":
            continue
        cis = ensaio.leituras[ensaio.leituras["etapa"] == "cisalhamento"]
        if len(cis) < MINIMO_DE_LEITURAS:
            continue
        meta = ensaio.metadados
        sigma = float(np.median(cis["tensao_normal"])) / 1e3
        por_id[meta.id_ensaio].append((meta.numero_teste, meta.inicio.strftime("%d/%m/%Y"), sigma))
    return por_id


def main(argv: list[str]) -> int:
    por_id = medir()
    repetidos = {k: v for k, v in por_id.items() if len(v) > 1}
    divergentes = {
        k: v
        for k, v in repetidos.items()
        if max(s for _, _, s in v) - min(s for _, _, s in v) > TOLERANCIA_KPA
    }

    total = sum(len(v) for v in por_id.values())
    print(f"\nEnsaios utilizaveis: {total}")
    print(f"Identificadores distintos: {len(por_id)}\n")
    print(f"  IDs usados em mais de um ensaio          {len(repetidos):>5}")
    print(f"  destes, com sigma divergindo > {TOLERANCIA_KPA:.0f} kPa    {len(divergentes):>5}")
    print(
        f"\n  Em {len(divergentes)} identificadores, dois arquivos com o MESMO ID"
        "\n  foram gravados sob tensoes normais diferentes.\n"
    )

    if divergentes:
        print("  Os casos, do maior desvio para o menor:\n")
        ordenados = sorted(
            divergentes.items(),
            key=lambda kv: -(max(s for _, _, s in kv[1]) - min(s for _, _, s in kv[1])),
        )
        for id_ensaio, ensaios in ordenados[:10]:
            sigmas = [s for _, _, s in ensaios]
            print(
                f"    {id_ensaio:<18} {len(ensaios)} ensaios · sigma de "
                f"{min(sigmas):.0f} a {max(sigmas):.0f} kPa"
            )
            for nt, data, sigma in sorted(ensaios, key=lambda e: e[2]):
                print(f"        NT {nt:>5}  {data}  sigma = {sigma:7.1f} kPa")
        print()

    if "--id" in argv:
        alvo = argv[argv.index("--id") + 1]
        ensaios = por_id.get(alvo)
        if not ensaios:
            print(f"ID {alvo!r} nao encontrado.")
            return 1
        print(f"  Todos os ensaios com ID {alvo!r}:\n")
        for nt, data, sigma in sorted(ensaios, key=lambda e: e[0]):
            print(f"    NT {nt:>5}  {data}  sigma medido = {sigma:7.1f} kPa")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
