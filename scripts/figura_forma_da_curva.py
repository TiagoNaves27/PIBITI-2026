"""Gera a figura do registro sobre a forma da curva.

Uso:
    uv run python scripts/figura_forma_da_curva.py

Poe lado a lado dois ensaios que a magnitude de tau nao distingue:

  NT 296  solo-cimento sob 50 kPa, tau de pico 1.182 kPa -- razao 24x. ENSAIO BOM.
  NT 608  solo natural sob 160 kPa, tau final 1.755 kPa -- razao 11x. TRAVADO.

O de razao MAIOR e o bom. Qualquer filtro por magnitude reprovaria o errado.

Os dois no mesmo par de eixos, sem truque de escala: o argumento e justamente que
os dois alcancam tau da mesma ordem, e que a diferenca esta na forma. Um sobe,
atinge o pico e desaba para o valor residual. O outro so sobe, e para.

Paleta: tons terrosos do `CLAUDE.md`. Duas series, distinguidas por valor e por
marcador -- nao so por cor.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

from geotec.parsers import direto

matplotlib.use("Agg")

ACERVO = Path(__file__).parents[1] / "dados" / "Ensaios-270" / "Cisalhamento"
SAIDA = Path(__file__).parents[1] / "docs" / "registros" / "figuras"

BOM = 296
TRAVADO = 608

INK = "#402905"
INK_SOFT = "#6b5428"
MUTED = "#7d6840"
TERRA = "#76552b"
OCRE = "#b69f66"
SURFACE = "#fbf5ea"


def curva(numero_teste: int):
    """Acha um ensaio pelo numero do teste e devolve (metadados, desloc mm, tau kPa)."""
    for caminho in ACERVO.glob(f"*NT {numero_teste} -*.csv"):
        ensaio = direto.ler(caminho)
        cis = ensaio.leituras[ensaio.leituras["etapa"] == "cisalhamento"]
        return (
            ensaio.metadados,
            (cis["desloc_cisalhante"] * 1e3).tolist(),
            (cis["tensao_cisalhante"] / 1e3).tolist(),
            float(cis["tensao_normal"].median() / 1e3),
        )
    raise SystemExit(f"NT {numero_teste} nao encontrado em {ACERVO}")


def desenhar(destino: Path) -> Path:
    meta_bom, d_bom, t_bom, sigma_bom = curva(BOM)
    meta_trv, d_trv, t_trv, sigma_trv = curva(TRAVADO)

    fig, ax = plt.subplots(figsize=(9.5, 5.4), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    ax.plot(
        d_bom,
        t_bom,
        color=OCRE,
        linewidth=2.0,
        marker="o",
        markersize=4,
        label=f"NT {BOM} · solo-cimento, σ = {sigma_bom:.0f} kPa · rompeu",
        solid_capstyle="round",
        zorder=2,
    )
    ax.plot(
        d_trv,
        t_trv,
        color=INK,
        linewidth=2.4,
        marker="s",
        markersize=4.5,
        label=f"NT {TRAVADO} · solo natural, σ = {sigma_trv:.0f} kPa · travou",
        solid_capstyle="round",
        zorder=3,
    )

    # Rotulo direto em cada curva: identidade nunca so pela cor.
    i_pico = t_bom.index(max(t_bom))
    ax.annotate(
        f"NT {BOM}\nrazão τ/σ = {max(t_bom) / sigma_bom:.0f}×\neste é o ensaio bom",
        xy=(d_bom[i_pico], t_bom[i_pico]),
        xytext=(d_bom[i_pico] + 1.6, t_bom[i_pico] + 210),
        color=TERRA,
        fontsize=9.5,
        fontweight="bold",
        linespacing=1.4,
        arrowprops={"arrowstyle": "-", "color": TERRA, "linewidth": 1.0},
    )
    ax.annotate(
        f"NT {TRAVADO}\nrazão τ/σ = {max(t_trv) / sigma_trv:.0f}×\npara aqui, sem pico",
        xy=(d_trv[-1], t_trv[-1]),
        xytext=(d_trv[-1] + 1.4, t_trv[-1] + 60),
        color=INK,
        fontsize=9.5,
        fontweight="bold",
        linespacing=1.4,
        arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 1.0},
    )

    # O que a forma mostra: o bom desaba depois do pico.
    i_vale = t_bom.index(min(t_bom[i_pico:]))
    ax.annotate(
        f"cai para {t_bom[i_vale]:.0f} kPa\n— ruptura frágil",
        xy=(d_bom[i_vale], t_bom[i_vale]),
        xytext=(d_bom[i_vale] - 0.6, t_bom[i_vale] + 330),
        color=MUTED,
        fontsize=9,
        ha="center",
        linespacing=1.4,
        arrowprops={"arrowstyle": "->", "color": MUTED, "linewidth": 0.9},
    )

    ax.set_xlim(0, max(d_bom) + 5.5)
    ax.set_ylim(0, max(max(t_bom), max(t_trv)) * 1.22)
    ax.set_xlabel("deslocamento cisalhante  (mm)", color=INK_SOFT, fontsize=9.5)
    ax.set_ylabel("τ  (kPa)", color=INK_SOFT, fontsize=9.5)
    ax.set_title(
        "Os dois passam de 1.000 kPa. O da razão maior é o ensaio bom.",
        color=INK,
        fontsize=12,
        fontweight="bold",
        loc="left",
        pad=14,
    )

    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(MUTED)
        ax.spines[lado].set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=9, length=3)
    ax.grid(axis="y", color=MUTED, alpha=0.18, linewidth=0.7)
    ax.set_axisbelow(True)

    legenda = ax.legend(
        loc="upper right", frameon=False, fontsize=9, labelcolor=INK_SOFT, handlelength=2.4
    )
    legenda.set_zorder(5)

    fig.tight_layout(pad=1.4)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, facecolor=SURFACE)
    plt.close(fig)
    return destino


def main() -> int:
    caminho = desenhar(SAIDA / "forma-da-curva.png")
    print(f"figura gravada em {caminho}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
