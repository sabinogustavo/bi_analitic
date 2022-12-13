import pandas as pd
import numpy as np
import csv_export

parque_movel_total = pd.read_csv("../base/parque_movel.csv", sep = ";", encoding="cp1252")
parque_movel = parque_movel_total.drop_duplicates(subset = ["CNPJ_CLIENTE"], keep="first")


# DATAFRAME POR M
df_movel_por_m = {
    "M":[],
    "CLIENTES":[],
    "RELATIVO_CLIENTES":[],
    "LINHAS":[],
    "RELATIVO_LINHAS":[],
}

# DATAFRAME TOTAL
df_movel_por_m_total = {
    "M":[],
    "CLIENTES":[],
    "RELATIVO_CLIENTES":[],
    "LINHAS":[],
    "RELATIVO_LINHAS":[],
}

# QUANTIDADE DE CLIENTES E LINHA POR M MOVEL
meses_parque_movel = parque_movel["M"].unique()
meses_parque_movel.sort()
meses_parque_movel = meses_parque_movel[~np.isnan(meses_parque_movel)].astype(int)

for m in meses_parque_movel:
    cliente_por_m = parque_movel.query(f"M == {m}")
    quantidade_linha_por_m = parque_movel_total.query(f"M == {m}")
    df_movel_por_m["CLIENTES"].append(len(cliente_por_m))
    df_movel_por_m["RELATIVO_CLIENTES"].append(len(cliente_por_m)/len(parque_movel))
    df_movel_por_m["M"].append(m)
    df_movel_por_m["LINHAS"].append(len(quantidade_linha_por_m))
    df_movel_por_m["RELATIVO_LINHAS"].append((len(quantidade_linha_por_m)/len(parque_movel_total)))

# QUANTIDADE TOTAL DE CLIENTES E LINHA POR M MOVEL
df_movel_por_m_total["CLIENTES"].append(len(parque_movel))
df_movel_por_m_total["M"].append("TOTAL")
df_movel_por_m_total["LINHAS"].append(len(parque_movel_total))
df_movel_por_m_total["RELATIVO_CLIENTES"].append("100")
df_movel_por_m_total["RELATIVO_LINHAS"].append("100")  

# QUANTIDADE DE CLIENTES E LINHAS APTOS A RENOVACAO
retorno_negativo_serasa = ["DÉBITO INTERNO","MEI - BAIXA PROBABILIDADE APROVAÇÃO","NÃO VENDER","BAIXA PROBABILIDADE APROVAÇÃO"]
situacao_negativa_receita = ["4 - INAPTA"]
clientes_aptos_a_renovacao = parque_movel.query(f"M >= 17 & M <= 24 & MENSAGEM_RETORNO_SERASA not in @retorno_negativo_serasa & SITUACAO_RECEITA not in @situacao_negativa_receita")
linhas_aptos_a_renovacao = parque_movel_total.query(f"M >= 17 & M <= 24 & MENSAGEM_RETORNO_SERASA not in @retorno_negativo_serasa & SITUACAO_RECEITA not in @situacao_negativa_receita")

# QUANTIDADE DE CLIENTES E LINHAS NÃO FIDELIZADAS
clientes_nao_fidelizados = parque_movel.query(f"M >= 24")
linhas_nao_fidelizadas = parque_movel_total.query(f"M >= 24")

# QUANTIDADE DE CLIENTES DE RENOVACAO PARA TOTALIZACAO
parque_movel.query(f"M >= 17")
df_movel_por_m = pd.DataFrame.from_dict(df_movel_por_m).reset_index()
df_movel_por_m_total = pd.DataFrame.from_dict(df_movel_por_m_total).reset_index()

csv_export.to_csv(df_movel_por_m,"movel_por_m")
csv_export.to_csv(df_movel_por_m_total, "movel_por_m_total")
