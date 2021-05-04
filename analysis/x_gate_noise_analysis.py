import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from git.Bakalaurinis.simuliator.chart_drawer import draw_simple_plot
from git.Bakalaurinis.simuliator.math import count_linear_regresion
from git.Bakalaurinis.tools.excel_tools import write_to_excel, append_excel_sheets, get_excel_sheets

def quito_x_noise_results():
    name = 'Sheet_Quito_X_Noise_aprox'
    sheets = get_excel_sheets([name])
    quito = sheets[name]
    n_arr = []
    i = 0.01
    while i <= 0.04:
        df = quito[i].dropna()
        res = count_linear_regresion(df)
        n_arr.append(res)
        # print(res)
        i += 0.01
    return n_arr

def yorktown_x_noise_results():
    name = 'Sheet_Yorktown_X_Noise_aprox'
    sheets = get_excel_sheets([name])
    quito = sheets[name]
    n_arr = []
    i = 0.02
    while i <= 0.05:
        df = quito[i].dropna()
        res = count_linear_regresion(df)
        n_arr.append(res)
        # print(res)
        i += 0.01

    return n_arr


def plot_regresions():
    quito = quito_x_noise_results()
    yorktown = yorktown_x_noise_results()
    df = pd.DataFrame({'Quito' : quito, 'Yorktown' : yorktown})
    print(df)
    draw_simple_plot(df,"Test")

plot_regresions()