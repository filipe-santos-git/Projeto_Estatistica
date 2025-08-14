# importações 
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt

# carregando os dados:
df = pd.read_csv("estatisticas_por_UF_mensal.csv")
df["Mes"] = pd.to_datetime(df["Mes"], format="%Y-%m", errors="coerce")
df["Media_Publico"] = pd.to_numeric(df["Media_Publico"], errors='coerce')

df_pre = df[df["Mes"].between("2014-01-01", "2019-12-31")].groupby("UF")["Media_Publico"].mean().reset_index()
df_pos = df[df["Mes"].between("2022-01-01", "2025-06-30")].groupby("UF")["Media_Publico"].mean().reset_index()

# juntar num dataset só:
df_recuperacao = pd.merge(df_pre, df_pos, on="UF", suffixes=("_pre", "_pos"))

# determinar se o setor se recuperou (>=95% da média pre-pandemia)
df_recuperacao["Recuperacao"] = df_recuperacao["Media_Publico_pos"] >= 0.7 * df_recuperacao["Media_Publico_pre"]
df_recuperacao["Recuperacao"] = df_recuperacao["Recuperacao"].map({True: "Sim", False: "Não"})

print(df_recuperacao["Recuperacao"].value_counts())


df_pandemia = df[df["Mes"].between("2020-01-01", "2021-12-31")].groupby("UF").agg({
    "Media_Publico": "mean",
    "Desvio_Padrao": "mean",
    "IQR": "mean"
}).reset_index()

df_modelo = pd.merge(
    df_recuperacao[["UF", "Recuperacao", "Media_Publico_pre"]],
    df_pandemia,
    on="UF"
)

le = LabelEncoder()
df_modelo["Recuperacao_encoded"] = le.fit_transform(df_modelo["Recuperacao"]) #(0/1) sim ou nao
X = df_modelo[["Media_Publico_pre", "Media_Publico", "Desvio_Padrao", "IQR"]]
y = df_modelo["Recuperacao_encoded"]

# Padronizar dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- 5. Divisão treino/teste (estratificada para evitar uma única classe) ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

model = GaussianNB()
model.fit(X_train, y_train)

print("Classes do modelo:", model.classes_)
y_pred = model.predict(X_test)

print(f"Acurácia: {accuracy_score(y_test, y_pred):.2f}")
print("\nMatriz de Confusão:\n", confusion_matrix(y_test, y_pred))
print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))

# probabilidades de cada classe
# --- Probabilidades de cada classe ---
probabilidades = model.predict_proba(X_scaled)

# Verificar quantas classes o modelo aprendeu
print("Classes do modelo:", model.classes_)

# Criar colunas de Prob_Sim e Prob_Nao de forma segura
if len(model.classes_) == 1:
    # Só existe uma classe
    if model.classes_[0] == 1:  # única classe é "Sim"
        df_modelo["Prob_Sim"] = 1.0
        df_modelo["Prob_Nao"] = 0.0
    else:  # única classe é "Não"
        df_modelo["Prob_Sim"] = 0.0
        df_modelo["Prob_Nao"] = 1.0
else:
    # Existem duas classes
    df_modelo["Prob_Sim"] = probabilidades[:, list(model.classes_).index(1)]
    df_modelo["Prob_Nao"] = probabilidades[:, list(model.classes_).index(0)]


# probabilidade de recuperação
df_modelo.sort_values("Prob_Sim", ascending=False, inplace=True)

plt.figure(figsize=(10, 6))
plt.barh(df_modelo["UF"], df_modelo["Prob_Sim"], color="skyblue")
plt.title("Probabilidade de Recuperação por Estado")
plt.xlabel("Probabilidade (Recuperação = Sim)")
plt.xlim(0, 1)
plt.grid(axis="x", linestyle="--")
plt.tight_layout()
plt.show()

# Salvar resultados
df_modelo.to_csv("resultados_recuperacao.csv", index=False)