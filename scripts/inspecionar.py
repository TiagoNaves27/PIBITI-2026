"""Inspeciona um arquivo bruto de maquina de ensaio e descreve sua estrutura.

Uso:
    uv run python scripts/inspecionar.py dados/exemplos/bruto/ensaio.csv

Serve para descobrir como o arquivo e organizado sem ter que abrir no Excel e
adivinhar: codificacao, separador, onde acaba o cabecalho, quais sao as colunas
e se os numeros usam virgula ou ponto decimal.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

CODIFICACOES = ["utf-8-sig", "utf-8", "cp1252", "latin-1", "utf-16"]
SEPARADORES = {"\t": "TAB", ";": "ponto-e-virgula", ",": "virgula", "|": "barra"}
LIMITE_LINHAS = 200


def detectar_codificacao(caminho: Path) -> tuple[str, list[str]]:
    """Tenta cada codificacao ate uma conseguir ler o arquivo inteiro."""
    for codec in CODIFICACOES:
        try:
            linhas = caminho.read_text(encoding=codec).splitlines()
        except (UnicodeDecodeError, UnicodeError):
            continue
        # utf-16 sem BOM decodifica lixo com bytes nulos; descarta.
        if "\x00" in "".join(linhas[:5]):
            continue
        return codec, linhas
    raise SystemExit(f"Nao consegui decodificar {caminho.name}. E um arquivo binario?")


def eh_binario(caminho: Path) -> bool:
    return (
        b"\x00"
        in caminho.read_bytes()[:4096].replace(b"\xff\xfe", b"").replace(b"\xfe\xff", b"")[:1024]
    )


def detectar_separador(linhas: list[str]) -> tuple[str | None, int]:
    """Escolhe o separador que aparece com a contagem mais estavel entre as linhas."""
    amostra = [ln for ln in linhas[:LIMITE_LINHAS] if ln.strip()]
    melhor, melhor_nota = None, 0
    for sep in SEPARADORES:
        contagens = Counter(ln.count(sep) for ln in amostra)
        contagens.pop(0, None)
        if not contagens:
            continue
        n_campos, repeticoes = contagens.most_common(1)[0]
        nota = repeticoes * n_campos
        if nota > melhor_nota:
            melhor, melhor_nota = sep, nota
    if melhor is None:
        return None, 0
    contagens = Counter(ln.count(melhor) for ln in amostra)
    contagens.pop(0, None)
    return melhor, contagens.most_common(1)[0][0] + 1


def parece_dado(linha: str, sep: str | None, n_campos: int) -> bool:
    """Uma linha de dado tem o numero esperado de campos e e majoritariamente numerica."""
    campos = linha.split(sep) if sep else linha.split()
    if len(campos) != n_campos:
        return False
    numericos = 0
    for campo in campos:
        try:
            float(campo.strip().replace(",", ".").replace(" ", ""))
            numericos += 1
        except ValueError:
            pass
    return numericos >= max(2, len(campos) * 0.6)


def achar_inicio_dados(linhas: list[str], sep: str | None, n_campos: int) -> int:
    """Primeira linha de um bloco de >=3 linhas numericas seguidas."""
    seguidas = 0
    for i, linha in enumerate(linhas):
        if parece_dado(linha, sep, n_campos):
            seguidas += 1
            if seguidas >= 3:
                return i - 2
        else:
            seguidas = 0
    return 0


def detectar_decimal(linhas: list[str], sep: str | None) -> str:
    """Se o separador de campo e ';' e ha virgulas sobrando, o decimal e virgula."""
    if sep == ";":
        texto = "".join(linhas)
        return "," if texto.count(",") > 0 else "."
    return "."


def secao(titulo: str) -> None:
    print(f"\n{titulo}\n{'-' * len(titulo)}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 1

    caminho = Path(argv[1])
    if not caminho.is_file():
        print(f"Arquivo nao encontrado: {caminho}")
        return 1

    secao("ARQUIVO")
    print(f"  nome      {caminho.name}")
    print(f"  tamanho   {caminho.stat().st_size:,} bytes")
    print(f"  extensao  {caminho.suffix or '(nenhuma)'}")

    if eh_binario(caminho):
        print("\n  >> Parece um arquivo BINARIO (nao e texto).")
        print("     Procure no software da maquina a opcao de exportar para CSV ou Excel.")
        print(f"     Primeiros bytes: {caminho.read_bytes()[:32]!r}")
        return 0

    codec, linhas = detectar_codificacao(caminho)
    sep, n_campos = detectar_separador(linhas)
    inicio = achar_inicio_dados(linhas, sep, n_campos)
    decimal = detectar_decimal(linhas[inicio:], sep)

    nome_sep = SEPARADORES.get(sep, "espaco/largura fixa") if sep else "espaco/largura fixa"

    secao("ESTRUTURA DETECTADA")
    print(f"  codificacao      {codec}")
    print(f"  separador        {nome_sep}")
    print(f"  colunas          {n_campos}")
    print(f"  total de linhas  {len(linhas):,}")
    print(f"  dados comecam    linha {inicio + 1}  (cabecalho = {inicio} linhas)")
    print(f"  decimal          {'virgula' if decimal == ',' else 'ponto'}")

    if inicio > 0:
        secao(f"CABECALHO (linhas 1 a {inicio}) - procure metadados do ensaio aqui")
        for i, linha in enumerate(linhas[:inicio], 1):
            print(f"  {i:>3} | {linha[:110]}")

    secao("POSSIVEIS NOMES DE COLUNA")
    candidata = linhas[inicio - 1] if inicio > 0 else ""
    if candidata and sep:
        for i, nome in enumerate(candidata.split(sep), 1):
            print(f"  {i:>3}. {nome.strip()}")
    else:
        print("  Nao identificado — confira o cabecalho acima manualmente.")

    secao("PRIMEIRAS LINHAS DE DADOS")
    for linha in linhas[inicio : inicio + 5]:
        print(f"  {linha[:110]}")

    secao("COMO LER ISSO COM PANDAS")
    args = [f'"{caminho.as_posix()}"']
    if sep and sep != ",":
        args.append(f'sep="{"\\t" if sep == chr(9) else sep}"')
    if inicio > 1:
        args.append(f"skiprows={inicio - 1}")
    if decimal == ",":
        args.append('decimal=","')
    if codec not in ("utf-8", "utf-8-sig"):
        args.append(f'encoding="{codec}"')
    print("  import pandas as pd")
    print(f"  df = pd.read_csv({', '.join(args)})")

    secao("PROXIMO PASSO")
    print("  1. Confira se as colunas acima batem com o que a maquina mostra na tela.")
    print("  2. Anote o significado e a UNIDADE de cada coluna (N ou kgf? mm ou pol?).")
    print("  3. Registre tudo em docs/arquitetura/formato-bruto.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
