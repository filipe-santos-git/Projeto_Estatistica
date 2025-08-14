import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt 
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

le = LabelEncoder()
scaler = StandardScaler()


df = pd.read_csv("estatisticas_publico_mensal.csv")
print(df.columns)

df["Mes"] = df["Mes"].astype(str)
df["Media_Publico"] = pd.to_numeric(df["Media_Publico"], errors='coerce')

# Calcular médias por estado e período
df_pre = df[df["Mes"].between("2014-01", "2019-12")].groupby("UF")["Media_Publico"].mean().reset_index()
df_pos = df[df["Mes"].between("2022-01", "2025-06")].groupby("UF")["Media_Publico"].mean().reset_index()

# Combinar e definir recuperação
df_recuperacao = pd.merge(df_pre, df_pos, on="UF", suffixes=("_pre", "_pos"))
df_recuperacao["Recuperacao"] = df_recuperacao["Media_Publico_pos"] >= 0.9 * df_recuperacao["Media_Publico_pre"]
df_recuperacao["Recuperacao"] = df_recuperacao["Recuperacao"].map({True: "Sim", False: "Não"})

df_pandemia = df[df["Mes"].between("2020-01", "2021-12")].groupby("UF").agg({
    "Media_Publico": "mean",
    "Desvio_Padrao": "mean",
    "IQR": "mean"
}).reset_index()

# Juntar tudo
df_modelo = pd.merge(
    df_recuperacao[["UF", "Recuperacao", "Media_Publico_pre"]],
    df_pandemia,
    on="UF"
)

df_modelo["Recuperacao_encoded"] = le.fit_transform(df_modelo["Recuperacao"])  # Sim=1, Não=0

X = scaler.fit_transform(df_modelo[["Media_Publico_pre", "Media_Publico", "Desvio_Padrao", "IQR"]])
y = df_modelo["Recuperacao_encoded"]

# Dividir em treino (70%) e teste (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Treinar o modelo
model = GaussianNB()
model.fit(X_train, y_train)

# Prever no conjunto de teste
y_pred = model.predict(X_test)

print(f"Acurácia: {accuracy_score(y_test, y_pred):.2f}")
print("\nMatriz de Confusão:\n", confusion_matrix(y_test, y_pred))
print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))

# Probabilidades de cada classe
probabilidades = model.predict_proba(X)

# DataFrame com resultados
df_resultados = df_modelo.copy()
df_resultados["Prob_Sim"] = probabilidades[:, 1]  # Probabilidade de "Sim"
df_resultados["Prob_Nao"] = probabilidades[:, 0]  # Probabilidade de "Não"

# Ordenar por probabilidade de recuperação
df_resultados.sort_values("Prob_Sim", ascending=False, inplace=True)

# Gráfico
plt.figure(figsize=(10, 6))
plt.barh(df_resultados["UF"], df_resultados["Prob_Sim"], color="skyblue")
plt.title("Probabilidade de Recuperação por Estado")
plt.xlabel("Probabilidade (Recuperação = Sim)")
plt.xlim(0, 1)
plt.grid(axis="x", linestyle="--")
plt.tight_layout()
plt.show()

df_resultados.to_csv("resultados_recuperacao.csv", index=False)