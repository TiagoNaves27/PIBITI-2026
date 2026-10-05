"""Encontra os ensaios que a maquina registrou mas que nao chegaram a romper.

Uso:
    uv run python scripts/ensaios_nao_rompidos.py
    uv run python scripts/ensaios_nao_rompidos.py --detalhe 608

Reproduz os numeros do registro `docs/registros/2026-09-12-ensaios-travados.md`.

O problema: para virar ponto de envoltoria, um ensaio precisa de um unico valor de
tensao cisalhante que represente a resistencia do solo. O jeito obvio de obter esse
valor -- o maximo da coluna de tau -- so funciona se o ensaio tiver rompido. Num
ensaio interrompido antes da ruptura o maximo e apenas onde a maquina estava quando
pararam, e entra na regressao como se fosse resistencia.

Os criterios, definidos em `docs/arquitetura/formato-bruto.md` secao 5.4:

    nao_rompeu    tau de pico no ULTIMO ponto E deslocamento final < 5 mm
    rigidez       rigidez do trecho final > 3x a mediana do proprio ensaio

Os dois testes de `nao_rompeu` sao necessarios juntos. "Pico no ultimo ponto"
sozinho pega quase metade do acervo, porque muito solo endurece ate o fim do curso
sem pico definido -- nao e defeito, e comportamento.

`rigidez` nao descarta: sinaliza para olho humano. Curva que acelera no fim em vez
de romper e o que se espera quando a maquina encontra uma reacao que nao e o solo.
"""

from __future__ import annotations

import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from geotec.parsers import direto

ACERVO = Path(__file__).parents[1] / "dados" / "Ensaios-270" / "Cisalhamento"

MINIMO_DE_LEITURAS = 5
DESLOC_CURTO = 5e-3  # m -- abaixo disto o ensaio nao teve curso para romper
FATOR_RIGIDEZ = 3.0  # quantas vezes a mediana o trecho final precisa ter


@dataclass(frozen=True)
class Curva:
    """O resumo da etapa de cisalhamento de um ensaio. Tudo em SI."""

    numero_teste: int
    id_ensaio: str
    data: str
    n_pontos: int
    sigma: float  # Pa, mediana da etapa
    tau_pico: float  # Pa
    tau_final: float  # Pa
    desloc_final: float  # m
    pico_no_fim: bool
    rigidez_final: float  # Pa/m
    rigidez_mediana: float  # Pa/m
    carga_horizontal_max: float  # N
    desloc_normal_final: float  # m

    @property
    def razao_rigidez(self) -> float:
        if self.rigidez_mediana <= 0:
            return float("inf")
        return self.rigidez_final / self.rigidez_mediana

    @property
    def nao_rompeu(self) -> bool:
        return self.pico_no_fim and self.desloc_final < DESLOC_CURTO

    @property
    def acelerando(self) -> bool:
        return self.razao_rigidez > FATOR_RIGIDEZ


def resumir(ensaio: direto.Ensaio) -> Curva | None:
    """Reduz a etapa de cisalhamento de um ensaio a um punhado de medidas."""
    cis = ensaio.leituras[ensaio.leituras["etapa"] == "cisalhamento"]
    if len(cis) < MINIMO_DE_LEITURAS:
        return None

    tau = cis["tensao_cisalhante"].to_numpy()
    desloc = cis["desloc_cisalhante"].to_numpy()

    # Rigidez de cada trecho: quanto tau sobe por metro de deslocamento.
    d_desloc = np.diff(desloc)
    validos = d_desloc > 0
    rigidezes = np.diff(tau)[validos] / d_desloc[validos]
    if len(rigidezes) == 0:
        return None

    meta = ensaio.metadados
    return Curva(
        numero_teste=meta.numero_teste,
        id_ensaio=meta.id_ensaio,
        data=meta.inicio.strftime("%d/%m/%Y"),
        n_pontos=len(cis),
        sigma=float(np.median(cis["tensao_normal"])),
        tau_pico=float(tau.max()),
        tau_final=float(tau[-1]),
        desloc_final=float(desloc[-1]),
        pico_no_fim=bool(tau.argmax() == len(tau) - 1),
        rigidez_final=float(rigidezes[-1]),
        rigidez_mediana=float(statistics.median(abs(rigidezes))),
        carga_horizontal_max=float(cis["carga_horizontal"].max()),
        desloc_normal_final=float(cis["desloc_normal"].iloc[-1]),
    )


def analisar(pasta: Path = ACERVO) -> list[Curva]:
    curvas = []
    for caminho in sorted(pasta.glob("*.csv")):
        ensaio = direto.ler(caminho)
        if ensaio.metadados.tipo_ensaio != "DS":
            continue
        curva = resumir(ensaio)
        if curva is not None:
            curvas.append(curva)
    return curvas


def _kpa(pa: float) -> float:
    return pa / 1e3


def _mm(m: float) -> float:
    return m * 1e3


def main(argv: list[str]) -> int:
    curvas = analisar()

    curtos = [c for c in curvas if c.desloc_final < DESLOC_CURTO]
    pico_no_fim = [c for c in curvas if c.pico_no_fim]
    nao_romperam = [c for c in curvas if c.nao_rompeu]
    travados = sorted(
        (c for c in nao_romperam if c.acelerando),
        key=lambda c: -c.razao_rigidez,
    )

    print(f"\nEnsaios com etapa de cisalhamento utilizavel: {len(curvas)}\n")
    print(f"  param antes de {_mm(DESLOC_CURTO):.0f} mm de deslocamento      {len(curtos):>5}")
    print(f"  tau de pico no ultimo ponto                 {len(pico_no_fim):>5}")
    print(f"  os DOIS criterios juntos (nao romperam)     {len(nao_romperam):>5}")
    print(f"  destes, com o trecho final acelerando       {len(travados):>5}")
    print(
        f"\n  'Pico no ultimo ponto' sozinho pegaria {len(pico_no_fim)} dos {len(curvas)} "
        f"ensaios.\n  E por isso que o criterio exige os dois testes juntos.\n"
    )

    if travados:
        print("  Ensaios com assinatura de travamento mecanico:\n")
        print(
            f"    {'NT':>6}  {'data':<11} {'ID':<14} {'sigma':>7} {'tau fim':>9}"
            f" {'desloc':>8} {'rigidez':>9} {'carga h':>9}"
        )
        for c in travados:
            print(
                f"    {c.numero_teste:>6}  {c.data:<11} {c.id_ensaio:<14}"
                f" {_kpa(c.sigma):>6.0f}k {_kpa(c.tau_final):>8.0f}k"
                f" {_mm(c.desloc_final):>7.1f}m {c.razao_rigidez:>8.1f}x"
                f" {c.carga_horizontal_max / 9.80665:>7.0f}kg"
            )
        print()

    if "--detalhe" in argv:
        alvo = int(argv[argv.index("--detalhe") + 1])
        c = next((c for c in curvas if c.numero_teste == alvo), None)
        if c is None:
            print(f"NT {alvo} nao encontrado entre os ensaios utilizaveis.")
            return 1
        print(f"  NT {c.numero_teste} · {c.id_ensaio} · {c.data}\n")
        print(f"    pontos na etapa de cisalhamento  {c.n_pontos}")
        print(f"    tensao normal                    {_kpa(c.sigma):.1f} kPa")
        print(f"    tau de pico                      {_kpa(c.tau_pico):.1f} kPa")
        print(f"    tau no ultimo ponto              {_kpa(c.tau_final):.1f} kPa")
        print(f"    pico no ultimo ponto?            {'sim' if c.pico_no_fim else 'nao'}")
        print(f"    deslocamento final               {_mm(c.desloc_final):.2f} mm")
        print(f"    desloc. normal no fim            {_mm(c.desloc_normal_final):+.2f} mm")
        print(f"    rigidez final / mediana          {c.razao_rigidez:.1f}x")
        print(f"    carga horizontal maxima          {c.carga_horizontal_max / 9.80665:.0f} kgf")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
