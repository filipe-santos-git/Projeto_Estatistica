import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt 

df = pd.read_csv("estatisticas_publico_mensal.csv")
df["Mes"] = df["Mes"].astype(str)
df["Media_Publico"] = pd.to_numeric(df["Media_Publico"], errors='coerce')

intervalos = [
    ("2014–2019", "2014-01", "2019-12"),
    ("2020–2021", "2020-01", "2021-12"),
    ("2022–2025", "2022-01", "2025-06"),
]

valores = []
for nome, inicio, fim in intervalos:
    separador = (df["Mes"] >= inicio) & (df["Mes"] <= fim)
    media_das_medias = df.loc[separador, "Media_Publico"].mean()
    valores.append({"Periodo": nome, "Media_das_Medias": round(float(media_das_medias), 2)})

resultado = pd.DataFrame(valores)

# gráfico de colunas
plt.figure(figsize=(8,5))
plt.bar(resultado["Periodo"], resultado["Media_das_Medias"])
plt.title("Média das médias de público por período")
plt.xlabel("Período")
plt.ylabel("Média das médias (público)")
for x, y in zip(resultado["Periodo"], resultado["Media_das_Medias"]):
    plt.text(x, y, f"{y:.0f}", ha="center", va="bottom")
plt.tight_layout()
plt.savefig("comparacao_medias_periodos.png", dpi=150)