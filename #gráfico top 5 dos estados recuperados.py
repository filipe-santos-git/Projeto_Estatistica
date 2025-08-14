import pandas as pd
import matplotlib.pyplot as plt

# Ler os dados
df = pd.read_csv("top5_filmes_selecionados.csv")

# Configura o gráfico
plt.figure(figsize=(22,18))

y_pos = 0          # posição inicial das barras
espaco = 1.5       # espaço entre barras
yticks = []
yticklabels = []

# Cores diferentes para cada UF
cores = {"GO": "skyblue", "AP": "orange", "TO": "lightgreen", "SC": "salmon"}

# ordem dos estados
ordem_estados = ["GO", "AP", "TO", "SC"]

for uf in ordem_estados:
    dados_uf = df[df["UF_SALA_COMPLEXO"] == uf]
    for _, row in dados_uf.iterrows():
        plt.barh(y=y_pos, width=row["PUBLICO"], height=1.0, color=cores.get(uf, "gray"))
        yticks.append(y_pos)
        yticklabels.append(f'{row["TITULO_BRASIL"]} ({uf})')
        y_pos += espaco

plt.yticks(yticks, yticklabels)
plt.xlabel("Público total")
plt.ylabel("Filmes")
plt.title("Top 5 filmes mais vistos por UF (2022–2024)")
plt.tight_layout()
plt.show()
