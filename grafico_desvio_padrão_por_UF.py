import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("estatisticas_gerais_por_UF.csv")


df["UF"] = df["UF"].astype(str)
df["Desvio_Padrao"] = pd.to_numeric(df["Desvio_Padrao"], errors="coerce")

plot_df = (
    df[["UF", "Desvio_Padrao"]]
    .sort_values("Desvio_Padrao", ascending=False)
)

plt.figure(figsize=(12, 6))
plt.bar(plot_df["UF"], plot_df["Desvio_Padrao"])
plt.title("Desvio-padrão por UF")
plt.xlabel("UF")
plt.ylabel("Desvio-padrão")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("desvio_padrao_por_UF.png", dpi=150)
