import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# LOAD DATA

file_path = "final_table.xlsx"
df = pd.read_excel(file_path)

# استانداردسازی نام ستون‌ها
df.columns = df.columns.str.strip()

# تغییر نام ستون‌ها برای راحتی
df = df.rename(columns={
    "Qmax / Qm (mg/g)": "Qmax",
    "KL (L/mg)": "KL"
})

# تبدیل به عددی
for col in ["Qmax", "KL", "pH", "T (°C)", "Contact time"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')


# CAPACITY MODELING (Langmuir)

df_lang = df.dropna(subset=["Qmax", "KL"])

if len(df_lang) > 0:

    Ce = np.linspace(0.1, 200, 200)

    plt.figure()
    for i in range(min(5, len(df_lang))):
        Qmax = df_lang.iloc[i]["Qmax"]
        KL = df_lang.iloc[i]["KL"]
        qe = (Qmax * KL * Ce) / (1 + KL * Ce)
        plt.plot(Ce, qe)

    plt.xlabel("Ce (mg/L)")
    plt.ylabel("qe (mg/g)")
    plt.title("Langmuir Isotherm Simulation")
    plt.show()

    # RL Calculation
    C0 = 100
    df_lang["RL"] = 1 / (1 + df_lang["KL"] * C0)

    plt.figure()
    plt.hist(df_lang["RL"].dropna())
    plt.xlabel("RL")
    plt.title("Langmuir Separation Factor (RL)")
    plt.show()

else:
    print("No valid Qmax/KL data for Langmuir modeling.")



# SELECTIVITY PROXY

if "System / Matrix" in df.columns:

    df["Tailings_flag"] = df["System / Matrix"].astype(str).str.lower().str.contains("tail")

    selectivity_score = df.groupby("Adsorbent")["Tailings_flag"].mean()

    plt.figure()
    selectivity_score.sort_values(ascending=False).plot(kind='bar')
    plt.ylabel("Tailings Performance Score")
    plt.title("Selectivity Proxy (Tailings Matrix Performance)")
    plt.show()

else:
    print("Matrix column not available for selectivity analysis.")



# RECYCLABILITY (No Data)

plt.figure()
plt.text(0.5, 0.5, "No recyclability data available",
         horizontalalignment='center',
         verticalalignment='center')
plt.xticks([])
plt.yticks([])
plt.title("Recyclability Analysis")
plt.show()



# HEATMAP (Numerical Correlation)

num_cols = df.select_dtypes(include=np.number)

if len(num_cols.columns) > 1:
    plt.figure()
    sns.heatmap(num_cols.corr(), annot=True)
    plt.title("Correlation Heatmap")
    plt.show()

else:
    print("Not enough numerical data for heatmap.")
