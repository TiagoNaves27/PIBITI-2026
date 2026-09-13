"""Parser dos arquivos de cisalhamento direto (tipo DS).

Traduz o CSV bruto da maquina para o formato normalizado descrito em
`docs/arquitetura/visao-geral.md` secao 5: metadados do ensaio mais uma serie
temporal, tudo em SI (N, m, Pa, s).

O layout do arquivo esta documentado em `docs/arquitetura/formato-bruto.md`
secao 2, e e identico nos 1.043 arquivos DS do acervo: UTF-8 com BOM, campos
separados por ';', decimal com virgula, 7 linhas de metadados no formato
`chave;valor`, nomes de coluna na linha 8 e dados a partir da linha 9.

Os arquivos de adensamento (tipo ODC) tem OUTRO layout -- 9 linhas de cabecalho,
outras chaves e uma coluna `Estagio` -- e por isso sao recusados aqui em vez de
lidos errado. Quando houver necessidade, eles ganham o proprio modulo.

Uso:
    from geotec.parsers import direto
    ensaio = direto.ler("dados/Ensaios-270/Cisalhamento/....csv")
    ensaio.metadados.diametro     # m
    ensaio.leituras["tensao_cisalhante"]   # Pa
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd

__all__ = ["Ensaio", "ErroDeFormato", "Metadados", "ler"]

CODIFICACAO = "utf-8-sig"
SEPARADOR = ";"
DECIMAL = ","
LINHAS_METADADOS = 7

# A maquina grava carga em kgf, nao em massa; g converte a leitura para N.
G = 9.80665

# DSS (cisalhamento simples) grava exatamente o mesmo layout que DS. O tipo fica
# registrado nos metadados para que o codigo a jusante possa separar os dois.
TIPOS_SUPORTADOS = frozenset({"DS", "DSS"})

# `AAAA-MM-DD HH-MM-SS - NT <n> - <tipo> - ID <id>.csv`
NOME_ARQUIVO = re.compile(
    r"^(?P<data>\d{4}-\d{2}-\d{2}) (?P<hora>\d{2}-\d{2}-\d{2})"
    r" - NT (?P<numero>\d+) - (?P<tipo>\S+) - ID (?P<id>.*)$"
)

CHAVES_METADADOS = (
    "Numero do Teste",
    "ID do ensaio",
    "Formato CP",
    "Tipo de Controle",
    "Dimensao Secao [mm]",
    "Altura Inicial [mm]",
    "Tempo de aquisicao",
)

COLUNAS_BRUTAS = (
    "Data",
    "Hora",
    "Etapa",
    "Tempo Etapa [min]",
    "Tensao Normal [kPa]",
    "Deslocamento Normal [mm]",
    "Altura Atual [mm]",
    "Deformacao Normal [%]",
    "Tensao Cisalhante [kPa]",
    "Deslocamento Cisalhante [mm]",
    "Deformacao Cisalhante [%]",
    "Tempo Ensaio [min]",
    "Velocidade Cisalhamento [mm/min]",
    "Area Corrigida [mm2]",
    "Carga Vertical [kg]",
    "Carga Horizontal [kg]",
    "Carga Horizontal Absoluta [kg]",
)

# coluna bruta -> (nome normalizado, fator que leva a unidade bruta para SI)
CONVERSOES: dict[str, tuple[str, float]] = {
    "Tempo Ensaio [min]": ("t", 60.0),
    "Tempo Etapa [min]": ("t_etapa", 60.0),
    "Tensao Normal [kPa]": ("tensao_normal", 1e3),
    "Tensao Cisalhante [kPa]": ("tensao_cisalhante", 1e3),
    "Deslocamento Normal [mm]": ("desloc_normal", 1e-3),
    "Deslocamento Cisalhante [mm]": ("desloc_cisalhante", 1e-3),
    "Altura Atual [mm]": ("altura_atual", 1e-3),
    "Area Corrigida [mm2]": ("area_corrigida", 1e-6),
    "Carga Vertical [kg]": ("carga_vertical", G),
    "Carga Horizontal [kg]": ("carga_horizontal", G),
    "Velocidade Cisalhamento [mm/min]": ("velocidade", 1e-3 / 60.0),
}

# Ordem das colunas da serie temporal normalizada.
COLUNAS = (
    "t",
    "t_etapa",
    "etapa",
    "tensao_normal",
    "tensao_cisalhante",
    "desloc_normal",
    "desloc_cisalhante",
    "altura_atual",
    "area_corrigida",
    "carga_vertical",
    "carga_horizontal",
    "velocidade",
)

ETAPAS = ("adensamento", "cisalhamento")


class ErroDeFormato(Exception):
    """O arquivo nao segue o layout DS documentado em formato-bruto.md secao 2."""


@dataclass(frozen=True)
class Metadados:
    """Identificacao e geometria do ensaio. Comprimentos em m."""

    numero_teste: int
    id_ensaio: str
    tipo_ensaio: str
    inicio: datetime
    diametro: float
    altura_inicial: float
    formato_cp: str
    tipo_controle: str
    caminho: Path


@dataclass(frozen=True)
class Ensaio:
    """Um arquivo lido: metadados mais a serie temporal em SI.

    Um arquivo e UM corpo de prova sob UMA tensao normal. A envoltoria de
    Mohr-Coulomb exige agrupar varios -- ver visao-geral.md secao 3.
    """

    metadados: Metadados
    leituras: pd.DataFrame


def ler(caminho: str | Path) -> Ensaio:
    """Le um arquivo de cisalhamento direto e devolve o ensaio normalizado.

    Nao julga a qualidade do ensaio: um arquivo sem etapa de cisalhamento, ou
    com tres leituras, e lido normalmente e devolvido. Decidir o que se aproveita
    e trabalho da rotina de qualidade (formato-bruto.md secao 5.4), que trabalha
    sobre o resultado desta funcao.

    Levanta ErroDeFormato quando o arquivo nao e do tipo DS/DSS, quando o nome
    foge do padrao da maquina ou quando o cabecalho e as colunas nao sao os
    esperados -- em vez de adivinhar e produzir numero errado calado.
    """
    caminho = Path(caminho)
    if not caminho.is_file():
        raise ErroDeFormato(f"arquivo nao encontrado: {caminho}")

    nome = _nome(caminho)
    linhas = caminho.read_text(encoding=CODIFICACAO).splitlines()
    if len(linhas) <= LINHAS_METADADOS + 1:
        raise ErroDeFormato(f"{caminho.name}: arquivo sem linhas de dados")

    cabecalho = _cabecalho(linhas, caminho.name)
    leituras = _leituras(caminho)
    metadados = _metadados(cabecalho, nome, leituras.attrs.pop("inicio"), caminho)

    if metadados.numero_teste != int(nome["numero"]):
        raise ErroDeFormato(
            f"{caminho.name}: o NT do nome ({nome['numero']}) nao bate com o do "
            f"cabecalho ({metadados.numero_teste}); o arquivo pode ter sido renomeado, "
            "e o tipo de ensaio so existe no nome"
        )

    return Ensaio(metadados=metadados, leituras=leituras[list(COLUNAS)])


def _nome(caminho: Path) -> dict[str, str]:
    """Quebra o nome do arquivo, unica fonte do tipo de ensaio."""
    achado = NOME_ARQUIVO.match(caminho.stem)
    if achado is None:
        raise ErroDeFormato(
            f"{caminho.name}: nome fora do padrao da maquina "
            "`AAAA-MM-DD HH-MM-SS - NT <n> - <tipo> - ID <id>.csv`"
        )
    partes = achado.groupdict()
    if partes["tipo"] not in TIPOS_SUPORTADOS:
        raise ErroDeFormato(
            f"{caminho.name}: tipo '{partes['tipo']}' nao e cisalhamento direto. "
            "Arquivos ODC (adensamento) tem outro layout -- 9 linhas de cabecalho, "
            "outras chaves e uma coluna `Estagio` -- e precisam do proprio parser."
        )
    return partes


def _cabecalho(linhas: list[str], nome_arquivo: str) -> dict[str, str]:
    """Le as 7 linhas `chave;valor` e confere que sao exatamente as esperadas."""
    cabecalho = dict(linha.partition(SEPARADOR)[::2] for linha in linhas[:LINHAS_METADADOS])
    if tuple(cabecalho) != CHAVES_METADADOS:
        raise ErroDeFormato(
            f"{nome_arquivo}: chaves de cabecalho inesperadas.\n"
            f"  esperado: {CHAVES_METADADOS}\n"
            f"  achado:   {tuple(cabecalho)}"
        )
    return cabecalho


def _leituras(caminho: Path) -> pd.DataFrame:
    """Le a serie temporal e converte cada grandeza para SI."""
    bruto = pd.read_csv(
        caminho,
        sep=SEPARADOR,
        skiprows=LINHAS_METADADOS,
        decimal=DECIMAL,
        encoding=CODIFICACAO,
    )
    if tuple(bruto.columns) != COLUNAS_BRUTAS:
        raise ErroDeFormato(
            f"{caminho.name}: colunas inesperadas.\n"
            f"  esperado: {COLUNAS_BRUTAS}\n"
            f"  achado:   {tuple(bruto.columns)}"
        )

    leituras = pd.DataFrame(
        {novo: bruto[origem] * fator for origem, (novo, fator) in CONVERSOES.items()}
    )
    leituras["etapa"] = _etapa(bruto["Etapa"], caminho.name)

    # A maquina grava Data e Hora em toda linha; o instante inicial vira metadado
    # e os demais viram `t`, entao as duas colunas nao entram na serie normalizada.
    leituras.attrs["inicio"] = datetime.strptime(
        f"{bruto['Data'].iloc[0]} {bruto['Hora'].iloc[0]}", "%d/%m/%Y %H:%M:%S"
    )
    return leituras


def _etapa(coluna: pd.Series, nome_arquivo: str) -> pd.Categorical:
    """Normaliza a etapa para minusculas; recusa valor fora do esperado."""
    etapas = coluna.str.strip().str.lower()
    estranhas = set(etapas.dropna().unique()) - set(ETAPAS)
    if estranhas:
        raise ErroDeFormato(
            f"{nome_arquivo}: etapa desconhecida {sorted(estranhas)}; esperado {list(ETAPAS)}"
        )
    return pd.Categorical(etapas, categories=ETAPAS)


def _metadados(
    cabecalho: dict[str, str], nome: dict[str, str], inicio: datetime, caminho: Path
) -> Metadados:
    """Monta os metadados, convertendo as dimensoes de mm para m."""
    inicio_nome = datetime.strptime(f"{nome['data']} {nome['hora']}", "%Y-%m-%d %H-%M-%S")
    if inicio_nome != inicio:
        raise ErroDeFormato(
            f"{caminho.name}: o instante do nome ({inicio_nome}) nao bate com a "
            f"primeira leitura ({inicio}); o arquivo pode ter sido renomeado, e o "
            "tipo de ensaio so existe no nome"
        )

    return Metadados(
        numero_teste=int(cabecalho["Numero do Teste"]),
        id_ensaio=cabecalho["ID do ensaio"].strip(),
        tipo_ensaio=nome["tipo"],
        inicio=inicio,
        diametro=_numero(cabecalho["Dimensao Secao [mm]"]) * 1e-3,
        altura_inicial=_numero(cabecalho["Altura Inicial [mm]"]) * 1e-3,
        formato_cp=cabecalho["Formato CP"].strip(),
        tipo_controle=cabecalho["Tipo de Controle"].strip(),
        caminho=caminho,
    )


def _numero(texto: str) -> float:
    """Converte um valor do cabecalho, que usa virgula decimal."""
    return float(texto.strip().replace(DECIMAL, "."))
