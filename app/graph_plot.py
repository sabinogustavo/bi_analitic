import fixa
import movel
import mapa_parque
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import magma
from bokeh.settings import settings
from bokeh.layouts import row

def main():
    plot_fixa = fixa.df_fixa_basica.query("M < 999").reset_index()
    plot_movel = movel.df_movel_por_m.query("M < 999").reset_index()

    graph_fixa = figure(title = "FIXA POR M", x_axis_label='M', y_axis_label='CLIENTES')
    graph_movel_clientes = figure(title = "CLIENTES MOVEL POR M", x_axis_label='M', y_axis_label='CLIENTES')
    graph_movel_linhas = figure(title = "LINHAS MOVEL POR M", x_axis_label='M', y_axis_label='LINHAS')

    graph_fixa.scatter(plot_fixa["M"],plot_fixa["CLIENTES"])
    graph_fixa.scatter(plot_fixa["M"],plot_fixa["CLIENTES_COM_RECOMENDACAO"], color = "RED")
    graph_fixa.scatter(plot_fixa["M"],plot_fixa["CLIENTES_COM_RECOMENDACAO_GPON"], color = "YELLOW")

    graph_movel_clientes.scatter(plot_movel["M"],plot_movel["CLIENTES"])
    graph_movel_linhas.scatter(plot_movel["M"],plot_movel["LINHAS"])

    show(row(graph_fixa,graph_movel_clientes,graph_movel_linhas))
