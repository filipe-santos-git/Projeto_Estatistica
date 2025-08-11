import pandas as pd
from pathlib import Path

pasta_dados = Path("dados_filtrados")
arquivos_csv = sorted(pasta_dados.glob("*.csv"))

estatisticas_mensais = []

for arquivo in arquivos_csv:
    nome_mes = arquivo.stem.replace("dados_filtrados[", "").replace("]", "")
    dados = pd.read_csv(arquivo)

    media_publico = dados["PUBLICO"].mean()
    mediana_publico = dados["PUBLICO"].median()
    s = pd.to_numeric(dados["PUBLICO"], errors="coerce").dropna()
    moda_publico = (s.mode().iloc[0] if not s.empty and not s.mode().empty else None)
    if s.empty:
        print(f"{nome_mes}: PUBLICO sem valores válidos; registrando moda=None")
    max_publico = dados["PUBLICO"].max()
    min_publico = dados["PUBLICO"].min()
    total_publico = dados["PUBLICO"].sum()
    desvio_padrao = dados["PUBLICO"].std()
    q1 = dados["PUBLICO"].quantile(0.25)
    q3 = dados["PUBLICO"].quantile(0.75)
    iqr = q3 - q1

    estatisticas_mensais.append({
        "Mes": nome_mes,
        "Media_Publico": round(media_publico, 2),
        "Mediana_Publico": mediana_publico,
        "Moda_Publico": moda_publico,
        "Max_Publico": max_publico,
        "Min_Publico": min_publico,
        "Total_Publico": total_publico,
        "Desvio_Padrao": desvio_padrao,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr
    })

df_estatisticas = pd.DataFrame(estatisticas_mensais)
df_estatisticas.to_csv("estatisticas_publico_mensal.csv", index=False)

print("Estatísticas calculadas e salvas em 'estatisticas_publico_mensal.csv'")
