# graficos_separados_por_UF.py

# =====================================================================
# 1. Importação de bibliotecas
# =====================================================================
# math: Usado para operações matemáticas, como logaritmos na função `nice_step`.
import math
# numpy: Biblioteca fundamental para computação numérica em Python.
import numpy as np
# pandas: Usada para manipulação e análise de dados (DataFrames).
import pandas as pd
# matplotlib.pyplot: Interface de plotagem de gráficos.
import matplotlib.pyplot as plt
# pathlib.Path: Oferece uma maneira orientada a objetos de lidar com caminhos de arquivo,
# tornando o código mais legível e independente do sistema operacional (Windows, Linux, etc.).
from pathlib import Path
# matplotlib.ticker: Módulos para formatar e controlar a posição dos rótulos dos eixos.
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FuncFormatter
# matplotlib.dates: Módulos para formatar e controlar o eixo de tempo.
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter

# =====================================================================
# 2. Configurações e Preparação Inicial
# =====================================================================
# Define o nome do arquivo CSV de entrada.
ARQ_MENSAL = "estatisticas_por_UF_mensal.csv"
# Define o caminho da pasta de saída usando `Path`.
PASTA_SAIDA = Path("graficos/separados_por_UF")
# Cria a pasta de saída e suas subpastas, se não existirem (`exist_ok=True` evita erros).
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

# =====================================================================
# 3. Funções Auxiliares (Helpers de formatação)
# =====================================================================
# Função para calcular um passo "arredondado" para os rótulos dos eixos,
# tornando os gráficos mais legíveis. Por exemplo, em vez de 12345, usa 10000.
def nice_step(raw):
    if not np.isfinite(raw) or raw <= 0:
        return 1.0
    exp = math.floor(math.log10(raw))
    base = raw / (10 ** exp)
    if base <= 2:
        nice = 2
    elif base <= 5:
        nice = 5
    else:
        nice = 10
    return nice * (10 ** exp)

# Função que retorna um formatador para o eixo Y. Ele formata os números
# com separador de milhar no padrão brasileiro (ex: 1.000.000) e sem casas decimais.
def fmt_milhar_br():
    return FuncFormatter(lambda x, pos: f"{int(round(x)):,}".replace(",", "."))

# Configura o eixo X para lidar com datas de forma inteligente, ajustando
# os ticks e o formato (ex: mês e ano).
def setup_time_axis(ax):
    loc = AutoDateLocator(minticks=4, maxticks=8)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(ConciseDateFormatter(loc))

# Configura o eixo Y, calculando os limites e os rótulos de forma dinâmica
# com base nos valores dos dados para uma visualização otimizada.
def setup_y_axis(ax, yvals):
    ymin = float(np.nanmin(yvals))
    ymax = float(np.nanmax(yvals))
    rng = ymax - ymin
    
    # Calcula o passo ideal usando a função `nice_step`.
    step = nice_step(max(rng / 5, 1))
    ax.yaxis.set_major_locator(MultipleLocator(step))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_major_formatter(fmt_milhar_br())

    # Adiciona um pequeno espaçamento nas bordas do gráfico para não "espremer" os dados.
    pad = 0.05 * (rng if rng > 0 else step)
    ax.set_ylim(ymin - pad, ymax + pad)

# Aplica um estilo padrão aos eixos do gráfico (título, rótulos e grades).
def style_axes(ax, title, xlabel, ylabel):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="major", axis="both", alpha=0.35)
    ax.grid(True, which="minor", axis="y", alpha=0.15)

# Salva a figura atual no disco no caminho especificado e fecha a figura
# para liberar memória.
def salva_plot(figpath: Path):
    figpath.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(figpath, dpi=150)
    plt.close()

# =====================================================================
# 4. Leitura e Preparo dos Dados
# =====================================================================
# Lê o arquivo CSV para um DataFrame do pandas.
df = pd.read_csv(ARQ_MENSAL)

# Limpeza e padronização dos dados.
df["UF"] = df["UF"].astype(str).str.strip().str.upper()
df["Mes"] = pd.to_datetime(df["Mes"], errors="coerce") # Converte a coluna 'Mes' para o tipo datetime.
df = df.dropna(subset=["UF", "Mes"]).sort_values(["UF", "Mes"]) # Remove linhas com dados ausentes na UF ou no Mês.
df["Ano"] = df["Mes"].dt.year # Extrai o ano da coluna 'Mes'.

# Define as colunas numéricas esperadas para garantir que existam e sejam tratadas.
num_cols_esperadas = [
    "Total_Publico", "Media_Publico", "Mediana_Publico",
    "Desvio_Padrao", "Q1", "Q3", "Min_Publico", "Max_Publico"
]
# Converte as colunas esperadas para tipo numérico, se existirem.
for c in num_cols_esperadas:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Remove linhas com valores NaN nas colunas numéricas após a conversão.
df = df.dropna(subset=[c for c in num_cols_esperadas if c in df.columns])

# Obtém uma lista única e ordenada de todas as UFs para iterar sobre elas.
ufs = sorted(df["UF"].unique())

# =====================================================================
# 5. Geração dos Gráficos por UF
# =====================================================================
# Inicia um loop que processa os dados e gera os gráficos para cada UF.
for uf in ufs:
    # Filtra o DataFrame para a UF atual e define o `Mes` como índice.
    d = df[df["UF"] == uf].set_index("Mes").sort_index()
    pasta_uf = PASTA_SAIDA / uf
    pasta_uf.mkdir(parents=True, exist_ok=True)

    # 1) Gráfico de linha do Público Total Mensal
    if "Total_Publico" in d.columns and not d["Total_Publico"].empty:
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(d.index, d["Total_Publico"], marker="o", linewidth=2)
        setup_time_axis(ax)
        setup_y_axis(ax, d["Total_Publico"].values)
        style_axes(ax, f"Público total mensal — {uf}", "Mês", "Público total")
        salva_plot(pasta_uf / "01_publico_total_mensal.png")

    # 2) Gráfico de linha comparando Média e Mediana
    if {"Media_Publico", "Mediana_Publico"}.issubset(d.columns):
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(d.index, d["Media_Publico"], marker="o", linewidth=2, label="Média")
        ax.plot(d.index, d["Mediana_Publico"], marker="s", linewidth=2, label="Mediana")
        setup_time_axis(ax)
        yy = np.concatenate([d["Media_Publico"].values, d["Mediana_Publico"].values])
        setup_y_axis(ax, yy)
        style_axes(ax, f"Média vs Mediana do público por mês — {uf}", "Mês", "Público")
        ax.legend()
        salva_plot(pasta_uf / "02_media_vs_mediana.png")

    # 3) Gráfico de linha do Desvio Padrão
    if "Desvio_Padrao" in d.columns and not d["Desvio_Padrao"].empty:
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(d.index, d["Desvio_Padrao"], marker="o", linewidth=2)
        setup_time_axis(ax)
        setup_y_axis(ax, d["Desvio_Padrao"].values)
        style_axes(ax, f"Desvio padrão do público por mês — {uf}", "Mês", "Desvio padrão")
        salva_plot(pasta_uf / "03_desvio_padrao.png")

    # 4) Gráfico de linha dos Quartis e IQR (Intervalo Interquartil)
    if {"Q1", "Q3"}.issubset(d.columns):
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(d.index, d["Q1"], marker="o", linewidth=2, label="Q1")
        ax.plot(d.index, d["Q3"], marker="s", linewidth=2, label="Q3")
        ax.fill_between(d.index, d["Q1"], d["Q3"], alpha=0.18, label="IQR (Q3 - Q1)")
        setup_time_axis(ax)
        yy = np.concatenate([d["Q1"].values, d["Q3"].values])
        setup_y_axis(ax, yy)
        style_axes(ax, f"Quartis do público por mês (IQR) — {uf}", "Mês", "Público")
        ax.legend()
        salva_plot(pasta_uf / "04_quartis_com_iqr.png")

    # 5) Gráfico de linha comparando Mínimo e Máximo
    if {"Min_Publico", "Max_Publico"}.issubset(d.columns):
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(d.index, d["Min_Publico"], marker="o", linewidth=2, label="Mínimo")
        ax.plot(d.index, d["Max_Publico"], marker="s", linewidth=2, label="Máximo")
        setup_time_axis(ax)
        yy = np.concatenate([d["Min_Publico"].values, d["Max_Publico"].values])
        setup_y_axis(ax, yy)
        style_axes(ax, f"Valores mínimo e máximo de público por mês — {uf}", "Mês", "Público")
        ax.legend()
        salva_plot(pasta_uf / "05_min_vs_max.png")

    # 6) Gráfico de Boxplot do Público Mensal por Ano
    if "Total_Publico" in d.columns and "Ano" in d.columns:
        grupos = list(d.groupby(d["Ano"]))
        if grupos:
            dados_por_ano = [g["Total_Publico"].dropna().values for _, g in grupos]
            labels_ano = [str(ano) for ano, _ in grupos]
            plt.figure(figsize=(14, 6))
            #showfliers=False` omite os outliers extremos no boxplot.
            plt.boxplot(dados_por_ano, labels=labels_ano, showfliers=False)
            plt.title(f"Distribuição do público mensal por ano (boxplot) — {uf}")
            plt.xlabel("Ano")
            plt.ylabel("Público mensal (Total)")
            plt.grid(True, axis="y", alpha=0.35)
            salva_plot(pasta_uf / "06_boxplot_total_por_ano.png")

print(f"Gráficos salvos em: {PASTA_SAIDA.resolve()}")