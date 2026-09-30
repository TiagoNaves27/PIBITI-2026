"""Script de apoio para regenerar as figuras da apresentacao de 2026-09-16.

Nao faz parte do pacote geotec (src/geotec/) -- e um script avulso de
exploracao/apoio a apresentacao, como os citados nos registros de
2026-09-12. Le os .csv brutos direto (o parser de producao ainda nao
existe em src/geotec/parsers/).

Uso:
    uv run python scripts/apoio_apresentacao.py forma-da-curva
    uv run python scripts/apoio_apresentacao.py envoltoria
    uv run python scripts/apoio_apresentacao.py variantes
    uv run python scripts/apoio_apresentacao.py curvas-d1n
    uv run python scripts/apoio_apresentacao.py variantes-maximo
    uv run python scripts/apoio_apresentacao.py acervo-10mm

Desde 29/09/2026 o tau de cada ensaio e lido a 10 mm de deslocamento, o
criterio do laboratorio (registro 2026-09-29-ruptura-a-10mm.md). Os
subcomandos terminados em "-maximo" refazem as contas com o maximo da
curva, o criterio usado ate entao (registro 2026-09-29-envoltoria-d1n.md).
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
        color=INK,
        linewidth=2.2,
        label="NT 296 (σ = 50 kPa) — rompe",
    )
    # serie em destaque (o ensaio travado): acento, tracejada e com marcador
    ax.plot(
        nt268["Deslocamento Cisalhante [mm]"],
        nt268["Tensao Cisalhante [kPa]"],
        color=TERRA,
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
# Dos 9 arquivos D1N de 30/09/2024 ficam de fora:
# - NT 612: sem etapa de cisalhamento; o NT 613 (mesmo ID D1N2, 6 min depois)
#   tem -- um dos 108 "so adensamento, com irmao" da triagem;
# - NT 608: nao rompeu (pico no ultimo ponto, 3,69 mm) -- registro 2026-09-12.
TRAVADO_D1N = 608
# 01/10/2024, romperam; so entram se a serie puder atravessar dias (Q1)
D1N16_DIA_SEGUINTE = [616, 618]


DESLOCAMENTO_RUPTURA = 10.0  # mm -- criterio do laboratorio (registro 2026-09-29-ruptura-a-10mm)


def tau_no_deslocamento(df: pd.DataFrame, deslocamento: float) -> float:
    """Tau em kPa no deslocamento cisalhante dado (mm), interpolado entre leituras.

    Devolve NaN se o ensaio parou antes desse deslocamento.
    """
    d = df["Deslocamento Cisalhante [mm]"].to_numpy()
    t = df["Tensao Cisalhante [kPa]"].to_numpy()
    if d.max() < deslocamento:
        return float("nan")
    if np.any(np.diff(d) < 0):
        raise ValueError("deslocamento cisalhante nao e crescente")
    return float(np.interp(deslocamento, d, t))


def ponto_envoltoria(nt: int, criterio: str = "10mm") -> tuple[float, float]:
    """Par (sigma, tau) em kPa de um ensaio.

    sigma: mediana da tensao normal na etapa de cisalhamento.
    tau: a 10 mm de deslocamento ("10mm", criterio do laboratorio) ou o
    maximo da curva ("maximo", criterio usado ate 29/09/2026).
    """
    df = etapa_cisalhamento(achar(nt))
    sigma = float(df["Tensao Normal [kPa]"].median())
    if criterio == "maximo":
        tau = float(df["Tensao Cisalhante [kPa]"].max())
    else:
        tau = tau_no_deslocamento(df, DESLOCAMENTO_RUPTURA)
    return sigma, tau


def figura_envoltoria(criterio: str = "10mm") -> None:
    """Envoltoria de Mohr-Coulomb da serie D1N, 30/09/2024 (7 ensaios que romperam)."""
    pontos = [ponto_envoltoria(nt, criterio) for nt in SERIE_D1N]
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
    # a figura do maximo e a do registro de 29/09 e nao e sobrescrita
    nome = "envoltoria-d1n.png" if criterio == "maximo" else "envoltoria-d1n-10mm.png"
    destino = DESTINO / nome
    fig.savefig(destino, dpi=200, facecolor=SURFACE)
    print(f"c = {c:.2f} kPa, phi = {phi:.2f} graus, R2 = {r2:.4f}")
    for nt, (s, t) in zip(SERIE_D1N, pontos, strict=True):
        print(f"  NT {nt}: sigma={s:.1f} kPa, tau={t:.1f} kPa")
    print(f"salvo em {destino}")


def ajustar(pontos: list[tuple[float, float]]) -> tuple[float, float, float]:
    """Regressao linear tau = c + sigma * tan(phi) sobre pontos (sigma, tau) em kPa.

    Devolve (c em kPa, phi em graus, R2).
    """
    reg = stats.linregress([p[0] for p in pontos], [p[1] for p in pontos])
    return float(reg.intercept), float(np.degrees(np.arctan(reg.slope))), float(reg.rvalue**2)


def variantes_envoltoria(criterio: str = "10mm") -> None:
    """Quanto a envoltoria D1N muda conforme o que entra nela. Tensoes em kPa.

    - correta: os 7 que romperam, sigma medido pela maquina;
    - sem filtro de ruptura: + NT 608 com o maximo de tau. O NT 608 parou aos
      3,69 mm e nao tem valor a 10 mm; entrar com ele e usar o unico numero
      que o arquivo oferece, o maximo;
    - sigma lido do ID: NT 614 com os 160 kPa que o ID D1N16 sugere, em vez de 22,2;
    - serie de dois dias: + NT 616 e NT 618 (01/10/2024), se a Q1 permitir.
    """
    base = {nt: ponto_envoltoria(nt, criterio) for nt in SERIE_D1N}

    sem_filtro = list(base.values()) + [ponto_envoltoria(TRAVADO_D1N, "maximo")]
    sigma_do_id = [((160.0, t) if nt == 614 else (s, t)) for nt, (s, t) in base.items()]
    dois_dias = list(base.values()) + [
        ponto_envoltoria(nt, criterio) for nt in D1N16_DIA_SEGUINTE
    ]

    variantes = [
        ("correta (7 ensaios que romperam)", list(base.values())),
        ("sem filtro de ruptura (+ NT 608)", sem_filtro),
        ("sigma do NT 614 lido do ID (160)", sigma_do_id),
        ("serie de dois dias (+ NT 616, 618)", dois_dias),
    ]
    print(f"{'variante':38s} {'pontos':>6s} {'c [kPa]':>9s} {'phi [graus]':>12s} {'R2':>8s}")
    for nome, pontos in variantes:
        c, phi, r2 = ajustar(pontos)
        print(f"{nome:38s} {len(pontos):6d} {c:9.1f} {phi:12.1f} {r2:8.4f}")
    print(f"(tau {'a 10 mm' if criterio == '10mm' else 'maximo da curva'})")
    t608 = ponto_envoltoria(TRAVADO_D1N, "maximo")
    print(f"\nNT 608: sigma={t608[0]:.1f} kPa, tau max={t608[1]:.1f} kPa (nao rompeu)")
    for nt in D1N16_DIA_SEGUINTE:
        s, t = ponto_envoltoria(nt, criterio)
        print(f"NT {nt}: sigma={s:.1f} kPa, tau={t:.1f} kPa (01/10/2024)")


def curvas_d1n() -> None:
    """Tabela das 7 curvas da serie D1N (slide 8 da apresentacao de 30/09). kPa, mm."""
    print(f"{'NT':>4s} {'sigma':>7s} {'tau 10mm':>9s} {'tau max':>8s} {'em (mm)':>8s}"
          f" {'desl. final':>12s}")
    for nt in sorted(SERIE_D1N, key=lambda n: ponto_envoltoria(n)[0]):
        df = etapa_cisalhamento(achar(nt))
        d = df["Deslocamento Cisalhante [mm]"]
        t = df["Tensao Cisalhante [kPa]"]
        sigma = df["Tensao Normal [kPa]"].median()
        t10 = tau_no_deslocamento(df, DESLOCAMENTO_RUPTURA)
        print(f"{nt:4d} {sigma:7.1f} {t10:9.1f} {t.max():8.1f} {d[t.idxmax()]:8.2f}"
              f" {d.iloc[-1]:12.2f}")


def acervo_10mm() -> None:
    """Quantos ensaios utilizaveis chegam a 10 mm e onde ficam as leituras vizinhas.

    Utilizavel: etapa de cisalhamento com 5 ou mais leituras (triagem, 914).
    """
    from collections import Counter

    utilizaveis, antes_5, antes_10, vizinhas = 0, 0, 0, Counter()
    for caminho in sorted(CISALHAMENTO.glob("*.csv")):
        df = etapa_cisalhamento(caminho)
        if len(df) < 5:
            continue
        utilizaveis += 1
        d = df["Deslocamento Cisalhante [mm]"].round(2)
        if d.max() < 5:
            antes_5 += 1
        if d.max() < DESLOCAMENTO_RUPTURA:
            antes_10 += 1
            continue
        vizinhas[(d[d <= 10].max(), d[d >= 10].min())] += 1
    print(f"utilizaveis: {utilizaveis}")
    print(f"param antes de 10 mm: {antes_10} (antes de 5 mm: {antes_5}; "
          f"entre 5 e 10 mm: {antes_10 - antes_5})")
    print(f"chegam a 10 mm: {sum(vizinhas.values())}")
    for (a, b), n in vizinhas.most_common():
        print(f"  leituras vizinhas {a:5.2f} e {b:5.2f} mm: {n}")


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "all"
    if alvo in ("forma-da-curva", "all"):
        figura_forma_da_curva()
    if alvo in ("envoltoria", "all"):
        figura_envoltoria()
    if alvo in ("variantes", "all"):
        variantes_envoltoria()
    if alvo in ("curvas-d1n", "all"):
        curvas_d1n()
    if alvo == "acervo-10mm":
        acervo_10mm()
    if alvo == "variantes-maximo":
        variantes_envoltoria("maximo")
    if alvo == "envoltoria-maximo":
        figura_envoltoria("maximo")
