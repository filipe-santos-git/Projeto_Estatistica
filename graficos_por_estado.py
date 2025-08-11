# graficos_separados_por_UF.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


ARQ_MENSAL = "estatisticas_por_UF_mensal.csv"   
PASTA_SAIDA = Path("graficos/separados_por_UF")
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)


df = pd.read_csv(ARQ_MENSAL)


df["UF"] = df["UF"].astype(str).str.strip().str.upper()   
df["Mes"] = pd.to_datetime(df["Mes"], errors="coerce")
df = df.dropna(subset=["UF", "Mes"])

df = df.sort_values(["UF", "Mes"])
df["Ano"] = df["Mes"].dt.year


num_cols_esperadas = [
    "Total_Publico", "Media_Publico", "Mediana_Publico",
    "Desvio_Padrao", "Q1", "Q3", "Min_Publico", "Max_Publico"
]
for c in num_cols_esperadas:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.dropna(subset=num_cols_esperadas)

def salva_plot(figpath: Path):
    figpath.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(figpath, dpi=150)
    plt.close()

# lista de UFs presentes
ufs = sorted(df["UF"].unique())  

for uf in ufs:
    d = df[df["UF"] == uf].set_index("Mes").sort_index()
    

    pasta_uf = PASTA_SAIDA / uf
    pasta_uf.mkdir(parents=True, exist_ok=True)

    # 1) Público total mensal
    if "Total_Publico" in d.columns:
        plt.figure(figsize=(14, 6))
        plt.plot(d.index, d["Total_Publico"], marker="o")
        plt.title(f"Público total mensal — {uf}")
        plt.xlabel("Mês")
        plt.ylabel("Público total")
        plt.xticks(rotation=45)
        plt.grid(True)
        salva_plot(pasta_uf / "01_publico_total_mensal.png")

    # 2) Média vs Mediana
    if {"Media_Publico", "Mediana_Publico"}.issubset(d.columns):
        plt.figure(figsize=(14, 6))
        plt.plot(d.index, d["Media_Publico"], marker="o", label="Média")
        plt.plot(d.index, d["Mediana_Publico"], marker="o", label="Mediana")
        plt.title(f"Média vs Mediana do público por mês — {uf}")
        plt.xlabel("Mês")
        plt.ylabel("Público")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        salva_plot(pasta_uf / "02_media_vs_mediana.png")

    # 3) Desvio padrão
    if "Desvio_Padrao" in d.columns:
        plt.figure(figsize=(14, 6))
        plt.plot(d.index, d["Desvio_Padrao"], marker="o")
        plt.title(f"Desvio padrão do público por mês — {uf}")
        plt.xlabel("Mês")
        plt.ylabel("Desvio padrão")
        plt.xticks(rotation=45)
        plt.grid(True)
        salva_plot(pasta_uf / "03_desvio_padrao.png")

    # 4) Quartis + IQR
    if {"Q1", "Q3"}.issubset(d.columns):
        plt.figure(figsize=(14, 6))
        plt.plot(d.index, d["Q1"], marker="o", label="Q1")
        plt.plot(d.index, d["Q3"], marker="o", label="Q3")
        plt.fill_between(d.index, d["Q1"], d["Q3"], alpha=0.2, label="IQR (Q3 - Q1)")
        plt.title(f"Quartis do público por mês (IQR) — {uf}")
        plt.xlabel("Mês")
        plt.ylabel("Público")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        salva_plot(pasta_uf / "04_quartis_com_iqr.png")

    # 5) Mínimo vs Máximo
    if {"Min_Publico", "Max_Publico"}.issubset(d.columns):
        plt.figure(figsize=(14, 6))
        plt.plot(d.index, d["Min_Publico"], marker="o", label="Mínimo")
        plt.plot(d.index, d["Max_Publico"], marker="o", label="Máximo")
        plt.title(f"Valores mínimo e máximo de público por mês — {uf}")
        plt.xlabel("Mês")
        plt.ylabel("Público")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        salva_plot(pasta_uf / "05_min_vs_max.png")

    # 6) Boxplot por ano (distribuição do total mensal no ano)
    if "Total_Publico" in d.columns and "Ano" in d.columns:
        grupos = list(d.groupby(d["Ano"]))
        if grupos:
            dados_por_ano = [g["Total_Publico"].dropna().values for _, g in grupos]
            labels_ano = [str(ano) for ano, _ in grupos]

            plt.figure(figsize=(14, 6))
            plt.boxplot(dados_por_ano, labels=labels_ano, showfliers=False)
            plt.title(f"Distribuição do público mensal por ano (boxplot) — {uf}")
            plt.xlabel("Ano")
            plt.ylabel("Público mensal (Total)")
            plt.grid(True, axis="y")
            salva_plot(pasta_uf / "06_boxplot_total_por_ano.png")

print(f"Gráficos salvos em: {PASTA_SAIDA.resolve()}")
