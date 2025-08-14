from pathlib import Path
import pandas as pd
import numpy as np

pasta_dados = Path("dados_filtrados")
arquivos_csv = sorted(pasta_dados.glob("*.csv"))

estatisticas_mensais = []

for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo, usecols=["UF_SALA_COMPLEXO", "PUBLICO"])
    df["PUBLICO"] = pd.to_numeric(df["PUBLICO"], errors="coerce")

    nome_mes = arquivo.stem.replace("dados_filtrados[", "").replace("]", "")
    grupo = df.groupby("UF_SALA_COMPLEXO")["PUBLICO"]

    media   = grupo.mean()
    mediana = grupo.median()
    moda    = grupo.apply(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
    maximo  = grupo.max()
    minimo  = grupo.min()
    total   = grupo.sum()
    desvio  = grupo.std()
    q1      = grupo.quantile(0.25)
    q3      = grupo.quantile(0.75)
    iqr     = q3 - q1

    for uf in media.index:
        media_publico    = media.loc[uf]
        mediana_publico  = mediana.loc[uf]
        moda_publico     = moda.loc[uf]
        max_publico      = maximo.loc[uf]
        min_publico      = minimo.loc[uf]
        total_publico    = total.loc[uf]
        desvio_padrao    = desvio.loc[uf]
        q1_val           = q1.loc[uf]
        q3_val           = q3.loc[uf]
        iqr_val          = iqr.loc[uf]

        estatisticas_mensais.append({
            "UF": uf,
            "Mes": nome_mes,
            "Media_Publico": round(media_publico, 2),
            "Mediana_Publico": mediana_publico,
            "Moda_Publico": moda_publico,
            "Max_Publico": max_publico,
            "Min_Publico": min_publico,
            "Total_Publico": total_publico,
            "Desvio_Padrao": desvio_padrao,
            "Q1": q1_val,
            "Q3": q3_val,
            "IQR": iqr_val
        })


resultado = pd.DataFrame(estatisticas_mensais)
resultado.to_csv("estatisticas_por_UF_mensal.csv", index=False)
