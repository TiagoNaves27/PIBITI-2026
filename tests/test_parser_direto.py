"""Testes do parser de cisalhamento direto.

Os valores esperados foram conferidos a mao contra as linhas brutas dos arquivos,
campo a campo. Cada um vem anotado com a leitura bruta de onde saiu, para que a
conferencia possa ser refeita sem abrir o CSV.

Dois niveis:

- o arquivo sintetico de `tests/dados/`, escrito com numeros redondos para que a
  conversao de unidade seja obvia a olho nu;
- um arquivo real do acervo, que garante que o parser aguenta o que a maquina
  realmente grava (BOM, virgula decimal, 78 leituras).
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from geotec.parsers import direto

EXEMPLO = Path(__file__).parent / "dados" / "2026-01-15 08-30-00 - NT 9001 - DS - ID TESTE01.csv"

ACERVO = (
    Path(__file__).parents[1]
    / "dados"
    / "Ensaios-270"
    / "Cisalhamento"
    / "2026-08-03 14-55-13 - NT 1149 - DS - ID D8N16V1.csv"
)

G = 9.80665


@pytest.fixture
def ensaio() -> direto.Ensaio:
    return direto.ler(EXEMPLO)


# --------------------------------------------------------------------------
# Metadados
# --------------------------------------------------------------------------


def test_metadados_do_cabecalho(ensaio: direto.Ensaio) -> None:
    meta = ensaio.metadados
    assert meta.numero_teste == 9001  # bruto: `Numero do Teste;9001`
    assert meta.id_ensaio == "TESTE01"
    assert meta.formato_cp == "Cilindrico"
    assert meta.tipo_controle == "Tensao"


def test_tipo_de_ensaio_vem_do_nome_do_arquivo(ensaio: direto.Ensaio) -> None:
    # O cabecalho nao registra o tipo; so o nome do arquivo tem essa informacao.
    assert ensaio.metadados.tipo_ensaio == "DS"


def test_geometria_convertida_de_mm_para_m(ensaio: direto.Ensaio) -> None:
    # bruto: `Dimensao Secao [mm];60` e `Altura Inicial [mm];20`
    assert ensaio.metadados.diametro == pytest.approx(0.060)
    assert ensaio.metadados.altura_inicial == pytest.approx(0.020)


def test_instante_inicial_vem_da_primeira_leitura(ensaio: direto.Ensaio) -> None:
    # bruto, primeira linha de dados: `15/01/2026;08:30:00;...`
    assert ensaio.metadados.inicio == datetime(2026, 1, 15, 8, 30, 0)


# --------------------------------------------------------------------------
# Serie temporal: forma e conversao de unidades
# --------------------------------------------------------------------------


def test_colunas_e_numero_de_leituras(ensaio: direto.Ensaio) -> None:
    assert tuple(ensaio.leituras.columns) == direto.COLUNAS
    assert len(ensaio.leituras) == 3


def test_colunas_derivadas_e_redundantes_ficam_de_fora(ensaio: direto.Ensaio) -> None:
    # Deformacao sai de desloc/altura_inicial; Data e Hora ja estao em `inicio` + `t`;
    # Carga Horizontal Absoluta e redundante. Ver visao-geral.md secao 5.2.
    fora = {"Data", "Hora", "Deformacao Normal [%]", "Deformacao Cisalhante [%]"}
    assert fora.isdisjoint(ensaio.leituras.columns)
    assert "carga_horizontal_absoluta" not in ensaio.leituras.columns


def test_conversao_da_ultima_leitura(ensaio: direto.Ensaio) -> None:
    """Linha bruta: 15/01/2026;08:40:00;Cisalhamento;9;200;-0,25;19,75;-1,25;50;
    2,5;12,5;10;1,5;2500;57,6;14,4;14,4
    """
    ultima = ensaio.leituras.iloc[-1]

    assert ultima["t"] == pytest.approx(600.0)  # 10 min       -> 600 s
    assert ultima["t_etapa"] == pytest.approx(540.0)  # 9 min        -> 540 s
    assert ultima["tensao_normal"] == pytest.approx(200_000.0)  # 200 kPa      -> 200000 Pa
    assert ultima["tensao_cisalhante"] == pytest.approx(50_000.0)  # 50 kPa   -> 50000 Pa
    assert ultima["desloc_normal"] == pytest.approx(-0.00025)  # -0,25 mm  -> -2,5e-4 m
    assert ultima["desloc_cisalhante"] == pytest.approx(0.0025)  # 2,5 mm    -> 2,5e-3 m
    assert ultima["altura_atual"] == pytest.approx(0.01975)  # 19,75 mm  -> 1,975e-2 m
    assert ultima["area_corrigida"] == pytest.approx(0.0025)  # 2500 mm2  -> 2,5e-3 m2
    assert ultima["velocidade"] == pytest.approx(2.5e-5)  # 1,5 mm/min -> 2,5e-5 m/s


def test_carga_em_kgf_vira_newton(ensaio: direto.Ensaio) -> None:
    # A coluna `Carga [kg]` da maquina e leitura em kgf, nao massa.
    ultima = ensaio.leituras.iloc[-1]
    assert ultima["carga_vertical"] == pytest.approx(564.86304)  # 57,6 kgf * g
    assert ultima["carga_horizontal"] == pytest.approx(141.21576)  # 14,4 kgf * g


def test_decimal_com_virgula_vira_numero(ensaio: direto.Ensaio) -> None:
    # Se o decimal fosse lido errado, a coluna viria como texto.
    numericas = [c for c in direto.COLUNAS if c != "etapa"]
    assert all(pd.api.types.is_numeric_dtype(ensaio.leituras[c]) for c in numericas)
    # `19,5` seria 195 se a virgula fosse ignorada.
    assert ensaio.leituras["altura_atual"].iloc[1] == pytest.approx(0.0195)


def test_etapa_normalizada_em_minusculas(ensaio: direto.Ensaio) -> None:
    assert list(ensaio.leituras["etapa"]) == ["adensamento", "adensamento", "cisalhamento"]
    assert list(ensaio.leituras["etapa"].cat.categories) == list(direto.ETAPAS)


# --------------------------------------------------------------------------
# Recusas: o parser falha alto em vez de produzir numero errado calado
# --------------------------------------------------------------------------


def test_recusa_arquivo_de_adensamento(tmp_path: Path) -> None:
    # ODC tem 8 linhas de cabecalho e outras chaves; lido como DS, a linha
    # `Altura Inicial [mm];20` viraria a linha de nomes de coluna.
    copia = tmp_path / "2026-01-15 08-30-00 - NT 9001 - ODC - ID TESTE01.csv"
    shutil.copy(EXEMPLO, copia)
    with pytest.raises(direto.ErroDeFormato, match="ODC"):
        direto.ler(copia)


def test_recusa_nome_fora_do_padrao(tmp_path: Path) -> None:
    copia = tmp_path / "ensaio.csv"
    shutil.copy(EXEMPLO, copia)
    with pytest.raises(direto.ErroDeFormato, match="nome fora do padrao"):
        direto.ler(copia)


def test_recusa_coluna_renomeada(tmp_path: Path) -> None:
    copia = tmp_path / EXEMPLO.name
    texto = EXEMPLO.read_text(encoding="utf-8-sig")
    copia.write_text(
        texto.replace("Tensao Cisalhante [kPa]", "Tensao Cisalhante [MPa]"),
        encoding="utf-8-sig",
    )
    with pytest.raises(direto.ErroDeFormato, match="colunas inesperadas"):
        direto.ler(copia)


def test_recusa_cabecalho_diferente(tmp_path: Path) -> None:
    copia = tmp_path / EXEMPLO.name
    texto = EXEMPLO.read_text(encoding="utf-8-sig")
    copia.write_text(texto.replace("Formato CP;", "Formato do CP;"), encoding="utf-8-sig")
    with pytest.raises(direto.ErroDeFormato, match="cabecalho inesperadas"):
        direto.ler(copia)


def test_recusa_arquivo_renomeado(tmp_path: Path) -> None:
    # NT do nome diferente do NT do cabecalho: o tipo de ensaio, que so existe no
    # nome, deixa de ser confiavel.
    copia = tmp_path / "2026-01-15 08-30-00 - NT 9999 - DS - ID TESTE01.csv"
    shutil.copy(EXEMPLO, copia)
    with pytest.raises(direto.ErroDeFormato, match="nao bate"):
        direto.ler(copia)


def test_recusa_arquivo_sem_dados(tmp_path: Path) -> None:
    copia = tmp_path / EXEMPLO.name
    linhas = EXEMPLO.read_text(encoding="utf-8-sig").splitlines()[:8]
    copia.write_text("\n".join(linhas), encoding="utf-8-sig")
    with pytest.raises(direto.ErroDeFormato, match="sem linhas de dados"):
        direto.ler(copia)


# --------------------------------------------------------------------------
# Arquivo real do acervo
# --------------------------------------------------------------------------


@pytest.mark.skipif(not ACERVO.is_file(), reason="acervo de ensaios indisponivel")
def test_arquivo_real_do_acervo() -> None:
    """NT 1149, ultima linha bruta: ...;Cisalhamento;15;159,863998;-0,0493927002;
    20,0526314;-0,247112378;137,183212;15,0001202;25,0002003;19,6000004;1;
    2372,12769;38,65625;33,171875;36,09375
    """
    ensaio = direto.ler(ACERVO)
    meta = ensaio.metadados

    assert meta.numero_teste == 1149
    assert meta.id_ensaio == "D8N16V1"
    assert meta.diametro == pytest.approx(0.060)
    assert meta.altura_inicial == pytest.approx(0.0215)
    assert meta.inicio == datetime(2026, 8, 3, 14, 55, 13)
    assert len(ensaio.leituras) == 78

    ultima = ensaio.leituras.iloc[-1]
    assert ultima["etapa"] == "cisalhamento"
    assert ultima["tensao_normal"] == pytest.approx(159_863.998)
    assert ultima["tensao_cisalhante"] == pytest.approx(137_183.212)
    assert ultima["desloc_cisalhante"] == pytest.approx(0.0150001202)
    assert ultima["desloc_normal"] == pytest.approx(-4.93927002e-5)
    assert ultima["t"] == pytest.approx(1176.0000240)  # 19,6000004 min
    assert ultima["velocidade"] == pytest.approx(1 / 60_000)  # 1 mm/min
    assert ultima["carga_vertical"] == pytest.approx(38.65625 * G)

    # A area corrigida cai com o deslocamento: a 15 mm ela e menor que a area
    # inicial do corpo de prova de 60 mm (pi * 30^2 = 2827,4 mm2).
    assert ultima["area_corrigida"] == pytest.approx(2.37212769e-3)
    assert ultima["area_corrigida"] < 3.141592653589793 * (meta.diametro / 2) ** 2


@pytest.mark.skipif(not ACERVO.is_file(), reason="acervo de ensaios indisponivel")
def test_as_duas_etapas_aparecem_em_ordem() -> None:
    etapas = direto.ler(ACERVO).leituras["etapa"]
    assert etapas.iloc[0] == "adensamento"
    assert etapas.iloc[-1] == "cisalhamento"
    # O adensamento vem inteiro antes do cisalhamento: nao ha volta.
    primeiro_cisalhamento = list(etapas).index("cisalhamento")
    assert set(etapas[primeiro_cisalhamento:]) == {"cisalhamento"}
