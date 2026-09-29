"""Script de apoio para regenerar as figuras da apresentacao de 2026-09-16.

Nao faz parte do pacote geotec (src/geotec/) -- e um script avulso de
exploracao/apoio a apresentacao, como os citados nos registros de
2026-09-12. Le os .csv brutos direto (o parser de producao ainda nao
existe em src/geotec/parsers/).

Uso:
    uv run python scripts/apoio_apresentacao.py forma-da-curva
    uv run python scripts/apoio_apresentacao.py envoltoria
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parent.parent
CISALHAMENTO = RAIZ / "dados" / "Ensaios-270" / "Cisalhamento"
DESTINO = RAIZ / "docs" / "registros" / "figuras"

# paleta Swiss Modern do projeto (CLAUDE.md §Paleta, desde 29/09/2026).
# Os nomes antigos (TERRA, OCRE) ficaram para não mexer no resto do script:
# TERRA agora é o acento vermelho; OCRE, o cinza de preenchimento.
INK = "#000000"
INK_SOFT = "#333333"
MUTED = "#5a5a5a"
TERRA = "#ff3300"
OCRE = "#cfcfcf"
GROUND = "#d6d6d6"
SURFACE = "#ffffff"


def carregar(caminho: Path) -> pd.DataFrame:
    """Le um .csv bruto de ensaio de cisalhamento direto. Unidades: kPa, mm."""
    return pd.read_csv(caminho, sep=";", decimal=",", skiprows=7, encoding="utf-8-sig")


def etapa_cisalhamento(caminho: Path) -> pd.DataFrame:
    df = carregar(caminho)
    return df[df["Etapa"] == "Cisalhamento"].reset_index(drop=True)


def achar(nt: int) -> Path:
    candidatos = list(CISALHAMENTO.glob(f"*NT {nt} *.csv"))
    if not candidatos:
        raise FileNotFoundError(f"NT {nt} nao encontrado em {CISALHAMENTO}")
    return candidatos[0]


def figura_forma_da_curva() -> None:
    """NT 296 (rompe, solo-cimento) vs NT 268 (travado) -- substitui o NT 608."""
    nt296 = etapa_cisalhamento(achar(296))
    nt268 = etapa_cisalhamento(achar(268))

    fig, ax = plt.subplots(figsize=(7.5, 4.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)

    ax.plot(
        nt296["Deslocamento Cisalhante [mm]"],
        nt296["Tensao Cisalhante [kPa]"],
        color=TERRA,
        linewidth=2.2,
        label="NT 296 (σ = 50 kPa) — rompe",
    )
    ax.plot(
        nt268["Deslocamento Cisalhante [mm]"],
        nt268["Tensao Cisalhante [kPa]"],
        color=INK,
        linewidth=2.2,
        linestyle="--",
        marker="o",
        markersize=4,
        label="NT 268 (σ = 399 kPa) — travado",
    )

    ax.set_xlabel("Deslocamento cisalhante [mm]", color=INK_SOFT)
    ax.set_ylabel("Tensão cisalhante τ [kPa]", color=INK_SOFT)
    ax.tick_params(colors=MUTED)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(GROUND)
    ax.grid(True, color=GROUND, linewidth=0.8)
    ax.legend(frameon=False, labelcolor=INK)

    fig.tight_layout()
    destino = DESTINO / "forma-da-curva-268.png"
    fig.savefig(destino, dpi=200, facecolor=SURFACE)
    print(f"NT296 pico={nt296['Tensao Cisalhante [kPa]'].max():.1f} kPa")
    print(f"NT268 final={nt268['Tensao Cisalhante [kPa]'].max():.1f} kPa em "
          f"{nt268['Deslocamento Cisalhante [mm]'].max():.2f} mm, "
          f"{len(nt268)} pontos")
    print(f"salvo em {destino}")


SERIE_D1N = [606, 607, 609, 610, 611, 613, 614]  # 30/09/2024, os 7 que romperam
# NT 612 (mesmo ID D1N2 do NT 613, 6 min antes) fica de fora: sem etapa de
# cisalhamento no arquivo -- provavelmente reiniciado pelo operador.


def ponto_envoltoria(nt: int) -> tuple[float, float]:
    df = etapa_cisalhamento(achar(nt))
    sigma = float(df["Tensao Normal [kPa]"].median())
    tau = float(df["Tensao Cisalhante [kPa]"].max())
    return sigma, tau


def figura_envoltoria() -> None:
    """Envoltoria de Mohr-Coulomb da serie D1N, 30/09/2024 (7 ensaios que romperam)."""
    pontos = [ponto_envoltoria(nt) for nt in SERIE_D1N]
    sigmas = np.array([p[0] for p in pontos])
    taus = np.array([p[1] for p in pontos])

    reg = stats.linregress(sigmas, taus)
    phi = np.degrees(np.arctan(reg.slope))
    c = reg.intercept
    r2 = reg.rvalue**2

    fig, ax = plt.subplots(figsize=(7.5, 5.2), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)

    ax.scatter(sigmas, taus, color=INK, s=60, zorder=3, label="Ensaios (D1N, 30/09/2024)")
    x = np.linspace(0, sigmas.max() * 1.12, 50)
    ax.plot(x, reg.intercept + reg.slope * x, color=TERRA, linewidth=2,
             label=f"τ = {c:.1f} + σ·tan({phi:.1f}°)")
    ax.fill_between(x, reg.intercept + reg.slope * x, color=OCRE, alpha=0.15)

    ax.set_xlabel("Tensão normal σ [kPa]", color=INK_SOFT)
    ax.set_ylabel("Tensão cisalhante de ruptura τ [kPa]", color=INK_SOFT)
    ax.set_xlim(0, None)
    ax.set_ylim(0, None)
    ax.tick_params(colors=MUTED)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(GROUND)
    ax.grid(True, color=GROUND, linewidth=0.8)
    ax.legend(frameon=False, labelcolor=INK, loc="upper left")
    ax.text(
        0.98, 0.04, f"R² = {r2:.4f}", transform=ax.transAxes,
        ha="right", color=MUTED, fontsize=10,
    )

    fig.tight_layout()
    destino = DESTINO / "envoltoria-d1n.png"
    fig.savefig(destino, dpi=200, facecolor=SURFACE)
    print(f"c = {c:.2f} kPa, phi = {phi:.2f} graus, R2 = {r2:.4f}")
    for nt, (s, t) in zip(SERIE_D1N, pontos):
        print(f"  NT {nt}: sigma={s:.1f} kPa, tau={t:.1f} kPa")
    print(f"salvo em {destino}")


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "all"
    if alvo in ("forma-da-curva", "all"):
        figura_forma_da_curva()
    if alvo in ("envoltoria", "all"):
        figura_envoltoria()
