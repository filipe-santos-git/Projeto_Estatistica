from pathlib import Path
import pandas as pd

pasta_dados = Path("dados_filtrados")
arquivos_csv = sorted(pasta_dados.glob("*.csv"))

df_list = []

for arquivo in arquivos_csv:
    nome_mes = arquivo.stem.replace("dados_filtrados[", "").replace("]", "")
    ano = int(nome_mes.split("-")[0])
    
    if 2022 <= ano <= 2024:
        df = pd.read_csv(arquivo, usecols=["TITULO_BRASIL", "UF_SALA_COMPLEXO", "PUBLICO"])
        df_list.append(df)

# Junta todos os arquivos
df_final = pd.concat(df_list, ignore_index=True)

# Agrupa por UF e título, somando o público
agrupado = df_final.groupby(['UF_SALA_COMPLEXO', 'TITULO_BRASIL'])['PUBLICO'].sum().reset_index()

# Ordena por UF e público (descendente)
agrupado = agrupado.sort_values(['UF_SALA_COMPLEXO', 'PUBLICO'], ascending=[True, False])

# Pega os 5 mais assistidos por UF
top2_por_uf = agrupado.groupby('UF_SALA_COMPLEXO').head(2)

top2_por_uf.to_csv("top2_filmes_por_uf.csv", index=False)
