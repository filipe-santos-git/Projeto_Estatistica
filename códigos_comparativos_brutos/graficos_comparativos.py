# graficos_separados.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# pasta de saída
pasta = Path("graficos/gerais")
pasta.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("estatisticas_publico_mensal.csv")
df["Mes"] = pd.to_datetime(df["Mes"])
df = df.sort_values("Mes").set_index("Mes")
df["Ano"] = df.index.year

# 1) Série temporal: Público total mensal
plt.figure(figsize=(14,6))
plt.plot(df.index, df["Total_Publico"], marker="o")
plt.title("Público total mensal")
plt.xlabel("Mês")
plt.ylabel("Público total")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(pasta / "01_publico_total_mensal.png")

# 2) Média vs Mediana (somente essas duas linhas)
plt.figure(figsize=(14,6))
plt.plot(df.index, df["Media_Publico"], marker="o", label="Média")
plt.plot(df.index, df["Mediana_Publico"], marker="o", label="Mediana")
plt.title("Média vs Mediana do público por mês")
plt.xlabel("Mês")
plt.ylabel("Público")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(pasta / "02_media_vs_mediana.png")

# 3) Desvio padrão isolado
plt.figure(figsize=(14,6))
plt.plot(df.index, df["Desvio_Padrao"], marker="o", label="Desvio padrão")
plt.title("Desvio padrão do público por mês")
plt.xlabel("Mês")
plt.ylabel("Desvio padrão")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(pasta / "03_desvio_padrao.png")

# 4) Quartis com faixa do IQR (Q1 a Q3)
plt.figure(figsize=(14,6))
plt.plot(df.index, df["Q1"], marker="o", label="Q1")
plt.plot(df.index, df["Q3"], marker="o", label="Q3")
plt.fill_between(df.index, df["Q1"], df["Q3"], alpha=0.2, label="IQR (Q3 - Q1)")
plt.title("Quartis do público por mês (faixa IQR sombreada)")
plt.xlabel("Mês")
plt.ylabel("Público")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(pasta / "04_quartis_com_iqr.png")

# 5) Mínimo e Máximo (para mostrar a amplitude mensal)
plt.figure(figsize=(14,6))
plt.plot(df.index, df["Min_Publico"], marker="o", label="Mínimo")
plt.plot(df.index, df["Max_Publico"], marker="o", label="Máximo")
plt.title("Valores mínimo e máximo de público por mês")
plt.xlabel("Mês")
plt.ylabel("Público")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(pasta / "05_min_vs_max.png")

# 6) Boxplot por ano usando os totais mensais (distribuição dentro do ano)
#    Aqui cada "box" representa a distribuição dos 12 meses daquele ano
dados_por_ano = [grupo["Total_Publico"].values for _, grupo in df.groupby("Ano")]
labels_ano = [str(ano) for ano, _ in df.groupby("Ano")]

plt.figure(figsize=(14,6))
plt.boxplot(dados_por_ano, labels=labels_ano, showfliers=False)
plt.title("Distribuição do público mensal por ano (boxplot)")
plt.xlabel("Ano")
plt.ylabel("Público mensal")
plt.grid(True, axis="y")
plt.tight_layout()
plt.savefig(pasta / "06_boxplot_total_por_ano.png")

print(f"Gráficos salvos em: {pasta.resolve()}")
