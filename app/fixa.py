import pandas as pd
import numpy as np
import csv_export

fixa_basica_total = pd.read_csv("../base/fixa_basica.csv", sep = ";", encoding="cp1252")
fixa_basica = fixa_basica_total.drop_duplicates(subset = ["DOCUMENTO"], keep="first")

df_fixa_basica = {
    "M":[],
    "CLIENTES":[],
    "RELATIVO_CLIENTES":[],
    "CLIENTES_COM_RECOMENDACAO":[],
    "RELATIVO_CLIENTES_COM_RECOMENDACAO":[],
    "CLIENTES_COM_RECOMENDACAO_GPON":[],
    "RELATIVO_CLIENTES_COM_RECOMENDACAO_GPON":[]
} 
df_fixa_basica_total = {
    "M":[],
    "CLIENTES":[],
    "RELATIVO_CLIENTES":[],
    "CLIENTES_COM_RECOMENDACAO":[],
    "RELATIVO_CLIENTES_COM_RECOMENDACAO":[],
    "CLIENTES_COM_RECOMENDACAO_GPON":[],
    "RELATIVO_CLIENTES_COM_RECOMENDACAO_GPON":[]
} 
# CLIENTES DE FIXA BASICA
clientes_fixa_basica = fixa_basica["DOCUMENTO"].unique()

# QUANTIDADE DE CLIENTES POR M FIXA_BASICA
meses_fixa_basica = fixa_basica["M"].unique()
meses_fixa_basica.sort()
meses_fixa_basica = meses_fixa_basica[~np.isnan(meses_fixa_basica)].astype(int)

for m in meses_fixa_basica:
    cliente_por_m = fixa_basica.query(f"M == {m}")
    # QUANTIDADE DE CLIENTES POR M FIXA_BASICA COM RECOMENDAÇÃO
    cliente_por_m_recomendacao = fixa_basica.query(f"M == {m} & FLG_RECOMENDACAO == 'SIM'")
    # QUANTIDADE DE CLIENTES POR M FIXA_BASICA COM RECOMENDAÇÃO GPON
    cliente_por_m_recomendacao_gpon = fixa_basica.query(f"M == {m} & FLG_RECOMENDACAO == 'SIM' & DS_TIPO_REDE_2 == 'GPON'")
    df_fixa_basica["M"].append(m)
    df_fixa_basica["CLIENTES"].append(len(cliente_por_m))
    df_fixa_basica["RELATIVO_CLIENTES"].append(len(cliente_por_m)/len(fixa_basica))
    df_fixa_basica["CLIENTES_COM_RECOMENDACAO"].append(len(cliente_por_m_recomendacao))
    df_fixa_basica["RELATIVO_CLIENTES_COM_RECOMENDACAO"].append(len(cliente_por_m_recomendacao)/len(fixa_basica))
    df_fixa_basica["CLIENTES_COM_RECOMENDACAO_GPON"].append(len(cliente_por_m_recomendacao_gpon))
    df_fixa_basica["RELATIVO_CLIENTES_COM_RECOMENDACAO_GPON"].append((len(cliente_por_m_recomendacao_gpon)/len(fixa_basica)))
df_fixa_basica_total["M"].append("TOTAL")
df_fixa_basica_total["CLIENTES"].append(len(fixa_basica))
df_fixa_basica_total["RELATIVO_CLIENTES"].append(1)
df_fixa_basica_total["CLIENTES_COM_RECOMENDACAO"].append(len(fixa_basica.query(f"FLG_RECOMENDACAO == 'SIM'")))
df_fixa_basica_total["RELATIVO_CLIENTES_COM_RECOMENDACAO"].append(round((len(fixa_basica.query(f"FLG_RECOMENDACAO == 'SIM'"))/len(fixa_basica))))
df_fixa_basica_total["CLIENTES_COM_RECOMENDACAO_GPON"].append(len(fixa_basica.query(f"FLG_RECOMENDACAO == 'SIM' & DS_TIPO_REDE_2 == 'GPON'")))
df_fixa_basica_total["RELATIVO_CLIENTES_COM_RECOMENDACAO_GPON"].append(len(cliente_por_m_recomendacao_gpon)/len(fixa_basica))

# CLIENTES APTOS COM RECOMENDAÇÃO
clientes_recomendacao = fixa_basica.query("FLG_RECOMENDACAO == 'SIM'")
clientes_recomendacao_menor_q_m_17 = clientes_recomendacao.query("M <= 17")
clientes_recomendacao_maior_q_m_17 = clientes_recomendacao.query("M >= 17")

# CLIENTES COM RECOMENDAÇÃO GPON
clientes_recomendacao_gpon = clientes_recomendacao.query("DS_TIPO_REDE_2 == 'GPON'")

df_fixa_basica = pd.DataFrame.from_dict(df_fixa_basica).reset_index()
df_fixa_basica_total = pd.DataFrame.from_dict(df_fixa_basica_total).reset_index()
csv_export.to_csv(df_fixa_basica,"fixa_basica")
csv_export.to_csv(df_fixa_basica_total,"fixa_basica_total")

