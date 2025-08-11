import pandas as pd
import numpy as np
# glob: busca arquivos/pastas por padrão com curingas (ex: "*.txt") no estilo do shell.
import glob

planilhas = glob.glob("bilheteria-diaria-obras-por-distribuidoras-csv/*.csv")

data_frames = []
for planilha in planilhas:
    df = pd.read_csv(planilha, sep=";", low_memory=False)
    data_frames.append(df)

data_frame = pd.concat(data_frames, ignore_index=True)
data_frame.to_csv("dados_consolidados.csv", index=False)