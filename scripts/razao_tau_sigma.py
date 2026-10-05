"""Conta e lista os ensaios em que tau de pico e alto em relacao a tensao normal.

Uso:
    uv run python scripts/razao_tau_sigma.py
    uv run python scripts/razao_tau_sigma.py --detalhe 296

Reproduz os numeros do registro `docs/registros/2026-09-12-forma-da-curva.md`.

A pergunta que este script responde: da para reprovar um ensaio olhando so o
tamanho de tau? Um ensaio com tau muito acima de sigma implicaria um angulo de
atrito absurdo, entao parece um filtro razoavel -- e nao e.

Material cimentado tem coesao de centenas de kPa, e sob tensao normal baixa isso
produz razoes tau/sigma altissimas em ensaios perfeitamente bons. O acervo tem uma
campanha inteira assim, com o tempo de cura escrito no ID (`B5-45D-50KPA` = 45 dias).

O que separa o ensaio bom do ensaio travado nao e a magnitude de tau: e a forma da
curva. O ensaio bom sobe, atinge um pico e CAI para um valor residual. O travado
so sobe.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from geotec.parsers import direto

ACERVO = Path(__file__).parents[1] / "dados" / "Ensaios-270" / "Cisalhamento"

MINIMO_DE_LEITURAS = 5
RAZAO_SUSPEITA = 1.2  # tau/sigma acima disto daria phi aparente acima de 50 graus


def curvas(pasta: Path = ACERVO):
    """Para cada ensaio utilizavel, devolve as medidas que interessam aqui."""
    for caminho in sorted(pasta.glob("*.csv")):
        ensaio = direto.ler(caminho)
        if ensaio.metadados.tipo_ensaio != "DS":
            continue
        cis = ensaio.leituras[ensaio.leituras["etapa"] == "cisalhamento"]
        if len(cis) < MINIMO_DE_LEITURAS:
            continue
        tau = cis["tensao_cisalhante"].to_numpy()
        sigma = float(np.median(cis["tensao_normal"]))
        # Ha ensaio no acervo cuja etapa de cisalhamento e toda zero; sem tau nao
        # ha razao nem queda que facam sentido.
        if sigma <= 0 or tau.max() <= 0:
            continue
        i_pico = int(tau.argmax())
        yield {
            "meta": ensaio.metadados,
            "sigma": sigma,
            "tau_pico": float(tau.max()),
            "tau_final": float(tau[-1]),
            "razao": float(tau.max()) / sigma,
            "pico_no_fim": i_pico == len(tau) - 1,
            # Quanto tau cai do pico ate o ultimo ponto, em fracao do pico.
            "queda": float(tau.max() - tau[-1]) / float(tau.max()),
            "desloc_final": float(cis["desloc_cisalhante"].iloc[-1]),
            "tau": tau,
            "desloc": cis["desloc_cisalhante"].to_numpy(),
        }


def main(argv: list[str]) -> int:
    todas = list(curvas())
    altas = [c for c in todas if c["razao"] > RAZAO_SUSPEITA]
    altas_que_romperam = [c for c in altas if not c["pico_no_fim"]]
    altas_sem_pico = [c for c in altas if c["pico_no_fim"]]

    print(f"\nEnsaios utilizaveis: {len(todas)}\n")
    print(f"  com tau de pico > {RAZAO_SUSPEITA}x sigma        {len(altas):>5}")
    print(f"    destes, com pico ANTES do ultimo ponto   {len(altas_que_romperam):>5}")
    print(f"    destes, com pico NO ultimo ponto         {len(altas_sem_pico):>5}")
    print(
        f"\n  Reprovar pela magnitude de tau descartaria {len(altas)} ensaios,\n"
        f"  dos quais {len(altas_que_romperam)} tem pico definido e caem depois dele --\n"
        "  o comportamento de um ensaio que rompeu.\n"
    )

    print("  As maiores razoes tau/sigma do acervo:\n")
    print(f"    {'NT':>6}  {'ID':<16} {'sigma':>8} {'tau pico':>9} {'razao':>7} {'queda':>7}")
    for c in sorted(altas, key=lambda c: -c["razao"])[:8]:
        m = c["meta"]
        print(
            f"    {m.numero_teste:>6}  {m.id_ensaio:<16} {c['sigma'] / 1e3:>7.0f}k"
            f" {c['tau_pico'] / 1e3:>8.0f}k {c['razao']:>6.1f}x {c['queda']:>6.0%}"
        )
    print("\n  'queda' = quanto tau caiu do pico ate o ultimo ponto. 0% = nunca caiu.\n")

    if "--detalhe" in argv:
        alvo = int(argv[argv.index("--detalhe") + 1])
        c = next((c for c in todas if c["meta"].numero_teste == alvo), None)
        if c is None:
            print(f"NT {alvo} nao encontrado.")
            return 1
        m = c["meta"]
        print(f"  NT {m.numero_teste} · {m.id_ensaio} · {m.inicio:%d/%m/%Y}")
        print(f"  sigma = {c['sigma'] / 1e3:.0f} kPa · razao tau/sigma = {c['razao']:.0f}x\n")
        for d, t in zip(c["desloc"], c["tau"], strict=True):
            barra = "#" * int(40 * t / c["tau_pico"])
            print(f"    {d * 1e3:6.2f} mm  {t / 1e3:8.1f} kPa  {barra}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
