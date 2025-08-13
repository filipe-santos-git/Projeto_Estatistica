# ESSE CÓDIGO É RESPONSÁVEL POR FILTRAR DADOS DE ARQUIVOS CSV PARA SOMENTE OS QUE PODEM E SERÃO USADOS NAS ANÁLISES ESTATÍSTICAS
#FOI EXCLUIDO O MES 07/2025 PELA FALTA DE DADOS
import pandas as pd
from pathlib import Path

pasta_origem = Path("bilheteria-diaria-obras-por-distribuidoras-csv")
arquivos_csv = pasta_origem.glob("*.csv")

colunas_desejadas = [
    "DATA_EXIBICAO",
    "RAZAO_SOCIAL_DISTRIBUIDORA",
    "UF_SALA_COMPLEXO",
    "PUBLICO",
    "MUNICIPIO_SALA_COMPLEXO",
    "TITULO_BRASIL",
    "PAIS_OBRA",
]

pasta_destino = Path("dados_filtrados")
pasta_destino.mkdir(exist_ok=True)

ano, mes = 2014, 1

for arq in arquivos_csv:
    nome_saida = f"{ano}-{mes:02d}"
    print(f"Lendo {arq.name} -> {nome_saida}")

    dados_filtrados = pd.read_csv(
        arq,
        sep=";",
        decimal=",",
        low_memory=False,
        usecols=colunas_desejadas,       
        na_values=["", " ", "-", "NA", "N/A"] 
    )

    dados_filtrados["PUBLICO"] = (
        dados_filtrados["PUBLICO"]
        .astype(str).str.strip()
        .replace({"": None})
    )
    dados_filtrados["PUBLICO"] = pd.to_numeric(dados_filtrados["PUBLICO"], errors="coerce")

    dados_filtrados = dados_filtrados.dropna()

    # salva
    saida = pasta_destino / f"dados_filtrados[{nome_saida}].csv"
    dados_filtrados.to_csv(saida, index=False)
    print(f"Salvo: {saida}")

    mes += 1
    if mes > 12:
        mes = 1
        ano += 1

print("Arquivos filtrados salvos.")
