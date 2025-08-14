import pandas as pd
import numpy as np

resultado_mensal = pd.read_csv("estatisticas_por_UF_mensal.csv")

for c in ["Media_Publico", "Total_Publico", "Max_Publico", "Min_Publico"]:
    resultado_mensal[c] = pd.to_numeric(resultado_mensal[c], errors="coerce")

estatisticas_gerais = []

for uf, bloco in resultado_mensal.groupby("UF", sort=True):
    serie_media = bloco["Media_Publico"].dropna()
    serie_total = bloco["Total_Publico"].dropna()
    serie_max   = bloco["Max_Publico"].dropna()
    serie_min   = bloco["Min_Publico"].dropna()

    media_publico   = serie_media.mean()
    mediana_publico = serie_media.median()
    moda_vals       = serie_media.mode()
    moda_publico    = moda_vals.iloc[0] if not moda_vals.empty else np.nan
    max_publico     = serie_max.max() if not serie_max.empty else np.nan
    min_publico     = serie_min.min() if not serie_min.empty else np.nan
    total_publico   = serie_total.sum()
    desvio_padrao   = serie_media.std(ddof=1)
    q1              = serie_media.quantile(0.25)
    q3              = serie_media.quantile(0.75)
    iqr             = q3 - q1

    estatisticas_gerais.append({
        "UF": uf,
        "Mes": "GERAL",
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

resultado_geral = (pd.DataFrame(estatisticas_gerais).sort_values("Total_Publico", ascending=False).reset_index(drop=True))

resultado_geral.to_csv("estatisticas_gerais_por_UF.csv", index=False)
