"""Compara o layout dos arquivos DS/DSS com o dos ODC e mede como cada leitura falha.

Uso:
    uv run python scripts/comparar_layouts.py

Reproduz o registro `docs/registros/2026-09-13-dois-layouts.md`.

As maquinas gravam DOIS layouts diferentes sob a mesma extensao `.csv`, e nada
dentro do arquivo diz qual e qual -- o tipo do ensaio so existe no NOME do arquivo.

O script mostra os dois cabecalhos lado a lado e submete um ODC a tres maneiras de
ler um DS. Nenhuma das tres avisa que o arquivo e de outro tipo:

    posicional   le a linha 5 como diametro. Devolve numero errado, calado.
    por chave    acha 'Dimensao Secao [mm]' por sorte, em outra linha. Passa batido.
    pandas       levanta ParserError, mas falando de contagem de campos na linha 10.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

from geotec.parsers import direto

ACERVO = Path(__file__).parents[1] / "dados" / "Ensaios-270"

NOME = re.compile(r" - NT \d+ - (?P<tipo>\S+) - ID ")

# Onde o DS guarda o diametro. Um leitor posicional usaria este indice.
LINHA_DO_DIAMETRO_NO_DS = 5


def um_de_cada_tipo() -> dict[str, Path]:
    achados: dict[str, Path] = {}
    for caminho in sorted(ACERVO.glob("*/*.csv")):
        m = NOME.search(caminho.name)
        if m and m.group("tipo") not in achados:
            achados[m.group("tipo")] = caminho
    return achados


def linhas_de(caminho: Path) -> list[str]:
    return caminho.read_text(encoding=direto.CODIFICACAO).splitlines()


def onde_comecam_os_dados(linhas: list[str]) -> int:
    """Numero (1-based) da linha de nomes de coluna: a primeira com muitos campos."""
    for i, linha in enumerate(linhas, 1):
        if linha.count(direto.SEPARADOR) + 1 > 3:
            return i
    raise ValueError("nenhuma linha com mais de 3 campos")


def main(argv: list[str]) -> int:
    tipos = Counter(m.group("tipo") for c in ACERVO.glob("*/*.csv") if (m := NOME.search(c.name)))
    exemplos = um_de_cada_tipo()

    print("\nArquivos por tipo, lido do NOME do arquivo:\n")
    for tipo, n in tipos.most_common():
        print(f"  {tipo:<6} {n:>5}")
    print("\n  O tipo nao aparece em nenhuma linha do conteudo.\n")

    for tipo in ("DS", "ODC"):
        caminho = exemplos[tipo]
        linhas = linhas_de(caminho)
        cabecalho = onde_comecam_os_dados(linhas) - 1
        print(
            f"{'=' * 78}\n{tipo}  ·  {cabecalho} linhas de metadados, "
            f"colunas na linha {cabecalho + 1}\n{'=' * 78}"
        )
        for i, linha in enumerate(linhas[: cabecalho + 1], 1):
            marca = "   <== nomes de coluna" if i == cabecalho + 1 else ""
            print(f"  {i:>2} | {linha[:76]}{marca}")
        print()

    ds, odc = exemplos["DS"], exemplos["ODC"]
    print(f"{'=' * 78}\nTres maneiras de ler um DS, aplicadas a um ODC\n{'=' * 78}\n")

    print("  1. POSICIONAL -- pegar o diametro da linha 5:\n")
    for nome, caminho in (("DS ", ds), ("ODC", odc)):
        chave, _, valor = linhas_de(caminho)[LINHA_DO_DIAMETRO_NO_DS - 1].partition(
            direto.SEPARADOR
        )
        print(f"     {nome}  {chave:<30} = {valor}")
    print("\n     Errado e calado: no ODC a linha 5 e um numero de estagios.")
    print("     Um diametro de 5 mm entraria no sistema sem nenhum aviso.\n")

    print("  2. POR CHAVE -- procurar 'Dimensao Secao [mm]' nas 7 primeiras linhas:\n")
    for nome, caminho in (("DS ", ds), ("ODC", odc)):
        cab = dict(
            linha.partition(direto.SEPARADOR)[::2]
            for linha in linhas_de(caminho)[: direto.LINHAS_METADADOS]
        )
        achou = cab.get("Dimensao Secao [mm]", "(nao achou)")
        print(f"     {nome}  Dimensao Secao [mm] = {achou}")
    print("\n     Acerta por sorte: no ODC a chave existe, so que em outra linha,")
    print("     e por acaso ainda dentro das 7 primeiras. Passa batido.\n")

    print("  3. PANDAS -- read_csv com skiprows=7:\n")
    try:
        pd.read_csv(
            odc,
            sep=direto.SEPARADOR,
            skiprows=direto.LINHAS_METADADOS,
            decimal=direto.DECIMAL,
            encoding=direto.CODIFICACAO,
            nrows=3,
        )
    except pd.errors.ParserError as erro:
        print(f"     ParserError: {erro}")
    print("\n     Levanta erro, mas falando de contagem de campos numa linha.")
    print("     Nao diz que o arquivo e de outro tipo de ensaio.\n")

    print(f"{'=' * 78}\nO que o parser do projeto faz\n{'=' * 78}\n")
    try:
        direto.ler(odc)
    except direto.ErroDeFormato as erro:
        print(f"  ErroDeFormato: {erro}\n")
    else:
        print("  ATENCAO: o parser NAO recusou. O registro precisa ser revisto.\n")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
