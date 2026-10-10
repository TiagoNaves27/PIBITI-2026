"""Roda o parser de cisalhamento direto em todos os arquivos do acervo.

Uso:
    uv run python scripts/parser_no_acervo.py

Responde: quantos arquivos de `dados/Ensaios-270/` o parser le, e quantos recusa.
Esperado em 10/10/2026: 1.045 lidos (1.043 DS + 2 DSS) e 36 recusados (os ODC de
adensamento, de outro layout -- `formato-bruto.md` secao 1.1).

Qualquer recusa fora dos ODC e impressa com o motivo.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from geotec.parsers import direto

ACERVO = Path(__file__).resolve().parent.parent / "dados" / "Ensaios-270"


def tipo_do_arquivo(caminho: Path) -> str:
    """Devolve o tipo (DS, DSS, ODC) do nome `data - NT n - TIPO - ID x.csv`."""
    partes = caminho.stem.split(" - ")
    return partes[2] if len(partes) > 2 else "?"


def main() -> None:
    lidos: Counter[str] = Counter()
    recusados: Counter[str] = Counter()
    for caminho in sorted(ACERVO.rglob("*.csv")):
        tipo = tipo_do_arquivo(caminho)
        try:
            direto.ler(caminho)
        except direto.ErroDeFormato as erro:
            recusados[tipo] += 1
            if tipo != "ODC":
                print(f"recusado fora do esperado: {caminho.name}: {erro}")
        else:
            lidos[tipo] += 1

    print(f"lidos:      {sum(lidos.values()):5d}  {dict(lidos)}")
    print(f"recusados:  {sum(recusados.values()):5d}  {dict(recusados)}")


if __name__ == "__main__":
    main()
