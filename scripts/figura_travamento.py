"""Gera a figura do registro dos ensaios travados.

Uso:
    uv run python scripts/figura_travamento.py

Mostra a serie D1N de 30/09/2024 inteira: sete curvas que rompem e uma que nao.
E o argumento visual do registro -- o que separa o ensaio travado dos outros e a
FORMA da curva, nao a magnitude de tau.

Sao dois paineis do mesmo dado, com escalas verticais diferentes e o mesmo eixo
horizontal:

  em cima   a escala que a maquina registrou. O NT 608 domina; os sete normais
            viram um risco no rodape. E esse o ponto: um deles nao e como os outros.
  embaixo   a escala dos sete normais. Da para ver que todos sobem, dobram e
            estabilizam ate 28 mm -- e que o NT 608 sai do quadro aos 3,7 mm.

Duas escalas verticais no MESMO grafico seriam engano; em paineis separados, cada
um com o seu eixo rotulado, e comparacao honesta.

Paleta: tons terrosos do `CLAUDE.md`. Nao ha oito series aqui, ha duas classes --
o ensaio suspeito e a familia dos normais -- entao sao dois tratamentos, nao oito
cores.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

from geotec.parsers import direto

matplotlib.use("Agg")

ACERVO = Path(__file__).parents[1] / "dados" / "Ensaios-270" / "Cisalhamento"
SAIDA = Path(__file__).parents[1] / "docs" / "registros" / "figuras"

# A serie do registro: mesma amostra, mesma condicao, mesmo dia.
DIA = date(2024, 9, 30)
PREFIXO = "D1N"
SUSPEITO = 608

INK = "#402905"
INK_SOFT = "#6b5428"
MUTED = "#7d6840"
TERRA = "#76552b"
OCRE = "#b69f66"
SURFACE = "#fbf5ea"


def serie() -> list[tuple[direto.Metadados, list[float], list[float]]]:
    """Devolve (metadados, deslocamento em mm, tau em kPa) de cada ensaio da serie."""
    curvas = []
    for caminho in sorted(ACERVO.glob("*.csv")):
        ensaio = direto.ler(caminho)
        meta = ensaio.metadados
        if meta.inicio.date() != DIA or not meta.id_ensaio.startswith(PREFIXO):
            continue
        cis = ensaio.leituras[ensaio.leituras["etapa"] == "cisalhamento"]
        if len(cis) < 5:
            continue
        curvas.append(
            (
                meta,
                (cis["desloc_cisalhante"] * 1e3).tolist(),
                (cis["tensao_cisalhante"] / 1e3).tolist(),
            )
        )
    return curvas


def _painel(ax, curvas, limite_y, mostrar_rotulos):
    for meta, desloc, tau in curvas:
        suspeito = meta.numero_teste == SUSPEITO
        ax.plot(
            desloc,
            tau,
            color=INK if suspeito else OCRE,
            linewidth=2.2 if suspeito else 1.1,
            marker="o" if suspeito else None,
            markersize=3.5,
            zorder=3 if suspeito else 2,
            solid_capstyle="round",
        )

    ax.set_ylim(0, limite_y)
    ax.set_xlim(0, 31)
    ax.set_facecolor(SURFACE)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(MUTED)
        ax.spines[lado].set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=9, length=3)
    ax.grid(axis="y", color=MUTED, alpha=0.18, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.set_ylabel("τ  (kPa)", color=INK_SOFT, fontsize=9.5)

    if mostrar_rotulos:
        meta, desloc, tau = next(c for c in curvas if c[0].numero_teste == SUSPEITO)
        fim = f"{desloc[-1]:.1f}".replace(".", ",")
        ax.annotate(
            f"NT {SUSPEITO} · para em {fim} mm\ncom τ = {tau[-1]:.0f} kPa, ainda subindo",
            xy=(desloc[-1], tau[-1]),
            xytext=(desloc[-1] + 3.2, tau[-1] * 0.86),
            color=INK,
            fontsize=9.5,
            fontweight="bold",
            linespacing=1.4,
            arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 1.0},
        )


def desenhar(destino: Path) -> Path:
    curvas = serie()
    if not any(m.numero_teste == SUSPEITO for m, _, _ in curvas):
        raise SystemExit(f"NT {SUSPEITO} nao encontrado na serie {PREFIXO} de {DIA}")

    normais = [c for c in curvas if c[0].numero_teste != SUSPEITO]
    teto_normais = max(max(tau) for _, _, tau in normais)

    fig, (cima, baixo) = plt.subplots(
        2, 1, figsize=(9.5, 6.2), dpi=200, sharex=True, height_ratios=[1, 1]
    )
    fig.patch.set_facecolor(SURFACE)

    _painel(cima, curvas, limite_y=1900, mostrar_rotulos=True)
    cima.set_title(
        f"A série D1N de 30/09/2024: {len(curvas)} ensaios, na escala que a máquina registrou",
        color=INK,
        fontsize=11,
        fontweight="bold",
        loc="left",
        pad=12,
    )

    _painel(baixo, curvas, limite_y=teto_normais * 1.15, mostrar_rotulos=False)
    baixo.set_title(
        "Os mesmos dados, na escala dos sete que romperam",
        color=INK,
        fontsize=11,
        fontweight="bold",
        loc="left",
        pad=12,
    )
    baixo.set_xlabel("deslocamento cisalhante  (mm)", color=INK_SOFT, fontsize=9.5)

    # Onde a curva do suspeito cruza o topo deste painel.
    _, desloc_s, tau_s = next(c for c in curvas if c[0].numero_teste == SUSPEITO)
    teto = teto_normais * 1.15
    saida = next(d for d, t in zip(desloc_s, tau_s, strict=True) if t >= teto)
    baixo.annotate(
        "o NT 608 sai do quadro aqui",
        xy=(saida, teto * 0.985),
        xytext=(saida + 3.0, teto * 0.80),
        color=TERRA,
        fontsize=9,
        arrowprops={"arrowstyle": "->", "color": TERRA, "linewidth": 1.0},
    )
    baixo.text(
        29.5,
        teto_normais * 0.12,
        "os sete sobem, dobram e estabilizam",
        ha="right",
        color=MUTED,
        fontsize=9,
    )

    fig.tight_layout(pad=1.6)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, facecolor=SURFACE)
    plt.close(fig)
    return destino


def main() -> int:
    caminho = desenhar(SAIDA / "ensaio-travado.png")
    print(f"figura gravada em {caminho}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
