import pandas as pd
import csv_export
import time

contatos= pd.read_csv("../base/contas_comerciais.csv", sep=";", encoding="cp1252")
mapa_parque = pd.read_csv("../base/mapa_parque.csv", sep = ";", encoding="cp1252")
fixa_basica_total = pd.read_csv("../base/fixa_basica.csv", sep = ";", encoding="cp1252")
fixa_basica = fixa_basica_total.drop_duplicates(subset = ["DOCUMENTO"], keep="first")
contatos["NR_CNPJ"] = contatos["NR_CNPJ"].astype(str)
mapa_parque["NR_CNPJ"] = mapa_parque["NR_CNPJ"].astype(str)
mapa_parque["DS_CNAE"] = mapa_parque["DS_CNAE"].astype(str)
fixa_basica["DOCUMENTO"] = fixa_basica["DOCUMENTO"].astype(str)

# CLIENTES MOVEL SEM FIXA 
clientes_movel_sem_fixa = mapa_parque.query("FLG_FIXA == 'NÃO' & FLG_MOVEL == 'SIM'")
# CLIENTES COM UMA LINHA MOVEL
clientes_uma_linha_movel = mapa_parque.query("QT_MOVEL_TERM == 1")
# CLIENTE COM MAIS DE 20 LINHAS MOVEL
clientes_mais_vinte_linhas_movel = mapa_parque.query("QT_MOVEL_TERM >= 20")
linhas_clientes_mais_vinte_linhas_movel = clientes_mais_vinte_linhas_movel["QT_MOVEL_TERM"].sum()
# CLIENTES FIXA SEM MOVEL
clientes_fixa_sem_movel = mapa_parque.query("FLG_FIXA == 'SIM' & FLG_MOVEL == 'NÃO'")
# CLIENTES COM UMA LINHA FIXA
clientes_com_uma_linha_fixa = mapa_parque.query("QT_BASICA_TERM_FIBRA == 1 | QT_BASICA_TERM_METALICO == 1")
# CLIENTES COM 3 LINHAS FIXA
clientes_com_tres_linhas_fixa = mapa_parque.query("QT_BASICA_TERM_FIBRA == 3 | QT_BASICA_TERM_METALICO == 3")
# CLIENTES COM FIXA E MOVEL
clientes_movel_e_fixa = mapa_parque.query("FLG_FIXA == 'SIM' & FLG_MOVEL == 'SIM'")
# MOVEL E AVANÇADA
clientes_movel_e_avancada = mapa_parque.query("TP_PRODUTO == 'MOVEL/AVANÇADO'")
# BASICA E AVANÇADA
clientes_basica_e_avancada = mapa_parque.query("TP_PRODUTO == 'BASICA/AVANÇADA'")
# MOVEL, BASICA E AVANÇADA
clientes_movel_basica_e_avancada = mapa_parque.query("TP_PRODUTO == 'MOVEL/BASICA/AVANÇADA'")
# CLIENTES POR QUANTIDADE DE LINHAS
quantidade_movel = mapa_parque.query("FLG_MOVEL == 'SIM'")
quantidade_movel = quantidade_movel ["QT_MOVEL_TERM"].unique().astype("int")
# CLIENTES PEN
clientes_pen = mapa_parque.query("QT_MOVEL_PEN >= 1")


for qtd in quantidade_movel:
    ...
    # print(qtd, len(mapa_parque.query(f"QT_MOVEL_TERM == {qtd}")))

# CURVA A,B,C PARETO
curva_a = mapa_parque.query(f"QT_MOVEL_TERM >=50")
curva_b = mapa_parque.query(f"QT_MOVEL_TERM >= 10 & QT_MOVEL_TERM <=50")
curva_c = mapa_parque.query(f"QT_MOVEL_TERM < 10")
curva_a_b_c = {
    "curva": ["curva a", "curva b", "curva c"],
    "clientes" : [len(curva_a),len(curva_b),len(curva_c)],
    "linhas" : [curva_a["QT_MOVEL_TERM"].sum(),curva_b["QT_MOVEL_TERM"].sum(),curva_c["QT_MOVEL_TERM"].sum()    ]
}
curva_a_b_c = pd.DataFrame.from_dict(curva_a_b_c)

# MOVEL SEM FIXA ENRIQUECIDOS
movel_sem_fixa_enriquecidos = clientes_movel_sem_fixa.merge(contatos, how="outer", on=["NR_CNPJ"], indicator = True)
movel_sem_fixa_enriquecidos = movel_sem_fixa_enriquecidos.query("_merge == 'both'")

#CLIENTES DE TOTALIZAÇÃO E RENOVAÇÃO FIXA
clientes_aptos_a_renovacao_e_totalizacao = mapa_parque.merge(fixa_basica, how="outer", left_on="NR_CNPJ", right_on="DOCUMENTO", indicator = True)
produtos = ["BASICA", "BASICA/AVANÇADA"]
clientes_aptos_a_renovacao_e_totalizacao = clientes_aptos_a_renovacao_e_totalizacao.query("TP_PRODUTO in @produtos & FLG_TOTALIZADO == 'NÃO' & M > 17")

# CLIENTES AVANÇADA SEM DADOS
clientes_avancada_sem_dados = mapa_parque.fillna(0)
clientes_avancada_sem_dados = clientes_avancada_sem_dados.query("QT_AVANCADA_DDR >= 1 | QT_AVANCADA_RI >= 1 | QT_AVANCADA_RDSI >= 1 | QT_AVANCADA_TERM >= 1 | QT_AVANCADA_VOX >= 1 | QT_AVANCADA_SIP >= 1")
clientes_avancada_sem_dados = clientes_avancada_sem_dados.query("QT_AVANCADA_DADOS == 0")

# CLIENTES POR SEGMENTAÇÃO
servicos = ["4923002","5112901","5112999"]
saude = ["5099899"]
transporte = ["4912401","4922101","4922102","4922103","4923002","4924800","4929902","4929904","4929999","5112999","8012900","5099801","5091202"]
educacao = ["4924800"]
eventos = ["8230001","8230002"]

# QUANTIDADE DE CLIENTES POR SEGMENTO
cnaes = mapa_parque["DS_CNAE"].unique()
volume_cnaes = {
    "CNAES" : [],
    "Quantidade" : [],
}
print(cnaes)
for cnae in cnaes:
    volume_cnaes["CNAES"].append(cnae)
    volume_cnaes["Quantidade"].append(len(mapa_parque.query(f"DS_CNAE == '{cnae}'")))

volume_cnaes = pd.DataFrame.from_dict(volume_cnaes).reset_index()
csv_export.to_csv(volume_cnaes,"volume_cnaes")
    
clientes_servicos = mapa_parque.query("DS_CNAE in @servicos")
clientes_saude = mapa_parque.query("DS_CNAE in @saude")
clientes_transporte = mapa_parque.query("DS_CNAE in @transporte")
clientes_educacao = mapa_parque.query("DS_CNAE in @educacao")
clientes_evento = mapa_parque.query("DS_CNAE in @eventos")

# REPORT
report_data = {
    "Qualidade" : [
        "clientes com  uma linha movel", 
        "clientes movel sem fixa",
        "clientes com mais de vinte linhas moveis", 
        "clientes fixa sem movel", 
        "clientes com uma linha fixa",
        "clientes com tres linhas fixas",
        "clientes movel e fixa",
        "clientes movel e avançada",
        "clientes basica e avançada",
        "clientes movel basica e avançada",
        ],
    "Quantidade" : [
        len(clientes_uma_linha_movel),
        len(clientes_movel_sem_fixa),
        len(clientes_mais_vinte_linhas_movel),
        len(clientes_fixa_sem_movel),
        len(clientes_com_uma_linha_fixa),
        len(clientes_com_tres_linhas_fixa),
        len(clientes_movel_e_fixa),
        len(clientes_movel_e_avancada),
        len(clientes_basica_e_avancada),
        len(clientes_movel_basica_e_avancada)
        ],
    "Quantidade de Linhas" : [
        clientes_uma_linha_movel["QT_MOVEL_TERM"].sum(),
        clientes_movel_sem_fixa["QT_MOVEL_TERM"].sum(),
        clientes_mais_vinte_linhas_movel["QT_MOVEL_TERM"].sum(),
        0,
        0,
        0,
        clientes_movel_e_fixa["QT_MOVEL_TERM"].sum(),
        clientes_movel_e_avancada["QT_MOVEL_TERM"].sum(),
        0,
        clientes_movel_basica_e_avancada["QT_MOVEL_TERM"].sum(),
        ]
}

report_data = pd.DataFrame.from_dict(report_data)


# EXPORT CSV
csv_export.to_csv(clientes_avancada_sem_dados, "clientes_avancada_sem_dados")
csv_export.to_csv(movel_sem_fixa_enriquecidos,"movel_sem_fixa_enriquecidos")
csv_export.to_csv(clientes_uma_linha_movel,"clientes_uma_linha_movel")
csv_export.to_csv(clientes_mais_vinte_linhas_movel,"clientes_mais_vinte_linhas_movel")
csv_export.to_csv(clientes_fixa_sem_movel,"clientes_fixa_sem_movel")
csv_export.to_csv(clientes_com_uma_linha_fixa,"clientes_com_uma_linha_fixa")
csv_export.to_csv(clientes_com_tres_linhas_fixa,"clientes_com_tres_linhas_fixa")
csv_export.to_csv(clientes_movel_e_fixa,"clientes_movel_e_fixa")
csv_export.to_csv(clientes_movel_e_avancada,"clientes_movel_e_avancada")
csv_export.to_csv(clientes_basica_e_avancada,"clientes_basica_e_avancada")
csv_export.to_csv(clientes_movel_basica_e_avancada,"clientes_movel_basica_e_avancada")
csv_export.to_csv(clientes_pen,"clientes_pen")
csv_export.to_csv(clientes_servicos,"clientes_servicos")
csv_export.to_csv(clientes_saude,"clientes_saude")
csv_export.to_csv(clientes_transporte,"clientes_transporte")  
csv_export.to_csv(clientes_educacao,"clientes_educacao")
csv_export.to_csv(clientes_evento,"evento")
csv_export.to_csv(curva_a,"curva_a")
csv_export.to_csv(curva_b,"curva_b")
csv_export.to_csv(curva_c,"curva_c")
csv_export.to_csv(clientes_aptos_a_renovacao_e_totalizacao,"clientes_aptos_a_renovacao_e_totalizacao")
csv_export.to_csv(report_data,"report_data")
csv_export.to_csv(curva_a_b_c,"curva_a_b_c")



