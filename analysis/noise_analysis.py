import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from git.Bakalaurinis.simuliator.chart_drawer import draw_simple_plot
from git.Bakalaurinis.simuliator.math import count_linear_regresion
from git.Bakalaurinis.tools.excel_tools import write_to_excel, append_excel_sheets, get_excel_sheets

def noise_results(name):
    sheets = get_excel_sheets([name])
    quito = sheets[name]
    n_arr = []
    i = 0.01
    while i <= 0.03:
        df = quito[i].dropna()
        res = count_linear_regresion(df)
        n_arr.append(res)
        # print(res)
        i += 0.01
    return n_arr


m_yorktown = noise_results(name = 'Sheet_yorktown_M_Aprox')
m_quito = noise_results(name = 'Sheet_quito_M_Aprox')
# x_quito = noise_results(name = 'Sheet_quito_X_Aprox')
# x_yorktown = noise_results(name = 'Sheet_Yorktown_X_Noise_aprox_2')
# print("m_yorktown su ry vartais", m_yorktown )
# print("m_quito su ry vartais", m_quito)
