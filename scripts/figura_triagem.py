"""Gera a figura da triagem do acervo para o registro e para a apresentacao.

Uso:
    uv run python scripts/figura_triagem.py

Le os dados de verdade chamando `triagem_acervo.triar()`, para que a figura nunca
divirja dos numeros do texto. Se o criterio de triagem mudar, a figura muda junto.

Sao duas zonas, porque sao dois trabalhos diferentes:

  - em cima, uma barra empilhada: quanto do acervo sobrou. Composicao.
  - embaixo, tres barras separadas: por que cada descarte aconteceu. Comparacao.

Empilhar os tres motivos numa barra so esconderia o 17 e o 4, que sao 1,6% e 0,4%
do acervo -- e sao justamente os dois que significam que alguma coisa deu errado.

Paleta: tons terrosos do `CLAUDE.md`. Monocromatica, entao a hierarquia se faz por
valor. Aqui o valor cresce com a gravidade: o descarte que e fluxo normal do
laboratorio e o mais claro, os dois que sao falha sao os mais escuros.

Os rotulos desta figura levam acento: e material de apresentacao, nao identificador
de codigo.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from triagem_acervo import contar, triar

# Backend sem janela: este script so grava arquivo, nunca abre tela.
matplotlib.use("Agg")

SAIDA = Path(__file__).parents[1] / "docs" / "registros" / "figuras"

# CLAUDE.md, modo claro.
INK = "#402905"
INK_SOFT = "#6b5428"
MUTED = "#7d6840"
TERRA = "#76552b"
OCRE = "#b69f66"
OCRE_SOFT = "#ead0a8"
SURFACE = "#fbf5ea"

LARGURA_PX = 2000
VAO = 2 / LARGURA_PX  # o vao de 2 px entre blocos, em unidades do eixo

# motivo -> (rotulo com acento, cor, e se significa que algo deu errado)
MOTIVOS = {
    "com_irmao": ("Só adensamento, com irmão", OCRE_SOFT, False),
    "orfao": ("Só adensamento, órfão", OCRE, True),
    "curto": ("Cisalhamento com 1 a 4 leituras", TERRA, True),
}

GUTTER = 0.34  # espaco a esquerda reservado aos rotulos das barras de baixo


def _milhar(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def desenhar(contagem: dict[str, int], destino: Path) -> Path:
    total = sum(contagem.values())
    utilizaveis = contagem["utilizavel"]
    descartes = total - utilizaveis

    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ------------------------------------------------ zona 1: o acervo todo
    ax.text(
        0,
        0.965,
        f"{_milhar(total)} arquivos de cisalhamento direto",
        ha="left",
        va="top",
        color=MUTED,
        fontsize=10.5,
    )

    y_barra, altura = 0.755, 0.13
    fracao = utilizaveis / total
    ax.add_patch(Rectangle((0, y_barra), fracao - VAO, altura, facecolor=INK, edgecolor="none"))
    ax.add_patch(
        Rectangle((fracao, y_barra), 1 - fracao, altura, facecolor=OCRE_SOFT, edgecolor="none")
    )
    ax.text(
        fracao / 2,
        y_barra + altura / 2,
        f"{utilizaveis} utilizáveis",
        ha="center",
        va="center",
        color=SURFACE,
        fontsize=13,
        fontweight="bold",
    )
    ax.text(
        1,
        y_barra - 0.045,
        f"{descartes} descartes",
        ha="right",
        va="top",
        color=INK,
        fontsize=11,
        fontweight="bold",
    )

    # ------------------------------------------- zona 2: os descartes, por motivo
    ax.text(
        0,
        0.56,
        "Os descartes, por motivo",
        ha="left",
        va="top",
        color=INK,
        fontsize=11,
        fontweight="bold",
    )

    maior = max(contagem[k] for k in MOTIVOS)
    escala = (1 - GUTTER - 0.08) / maior
    alt_barra = 0.075
    ys = [0.375, 0.245, 0.115]

    for (chave, (rotulo, cor, e_falha)), y in zip(MOTIVOS.items(), ys, strict=True):
        n = contagem[chave]
        ax.text(
            GUTTER - 0.02,
            y + alt_barra / 2,
            rotulo,
            ha="right",
            va="center",
            color=INK if e_falha else INK_SOFT,
            fontsize=9.5,
        )
        ax.add_patch(Rectangle((GUTTER, y), n * escala, alt_barra, facecolor=cor, edgecolor="none"))
        ax.text(
            GUTTER + n * escala + 0.012,
            y + alt_barra / 2,
            str(n),
            ha="left",
            va="center",
            color=INK,
            fontsize=12,
            fontweight="bold",
        )

    # Chave a esquerda separando o que e fluxo normal do que e falha.
    ax.plot([0.012, 0.012], [ys[0], ys[0] + alt_barra], color=MUTED, linewidth=1.2)
    ax.text(
        0.026,
        ys[0] + alt_barra / 2,
        "fluxo\nnormal",
        ha="left",
        va="center",
        color=MUTED,
        fontsize=8,
        linespacing=1.3,
    )
    ax.plot([0.012, 0.012], [ys[2], ys[1] + alt_barra], color=INK, linewidth=1.2)
    ax.text(
        0.026,
        (ys[2] + ys[1] + alt_barra) / 2,
        "algo deu\nerrado",
        ha="left",
        va="center",
        color=INK,
        fontsize=8,
        linespacing=1.3,
    )

    ax.text(
        0,
        0.035,
        f"Dos {descartes} descartes, {contagem['com_irmao']} não são ensaio perdido: "
        f"o cisalhamento está num arquivo irmão.",
        ha="left",
        va="top",
        color=MUTED,
        fontsize=9,
    )

    fig.subplots_adjust(left=0.035, right=0.975, top=0.97, bottom=0.03)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, facecolor=SURFACE)
    plt.close(fig)
    return destino


def main() -> int:
    caminho = desenhar(contar(triar()), SAIDA / "triagem-do-acervo.png")
    print(f"figura gravada em {caminho}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
