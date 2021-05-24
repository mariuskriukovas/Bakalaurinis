import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

from git.Bakalaurinis.simuliator.chart_drawer import draw_simple_plot
from git.Bakalaurinis.simuliator.math import count_linear_regresion
from git.Bakalaurinis.tools.excel_tools import write_to_excel, append_excel_sheets, get_excel_sheets
from git.Bakalaurinis.analysis.analysis_tools import noise_results, preaty_print, get_sheet
import matplotlib.patches as mpatches


def m_gate_analysis():

    m_yorktown = noise_results(name = 'Sheet_yorktown_M_Aprox')
    m_quito = noise_results(name = 'Sheet_quito_M_Aprox')

    print("m_yorktown su ry vartais", m_yorktown )
    print("m_quito su ry vartais", m_quito)

# m_gate_analysis()

def plot_m_gate_analysis():
    df = get_sheet('Sheet_quito_M_Aprox')
    x = df.index
    y = df[0.01][::-1]
    slope, intercept, r_value, p_value, std_err = count_linear_regresion(df[0.01],reversed_index=True)
    print("intercept --->", intercept)
    line = [slope * xi + intercept for xi in df.index]
    plt.title("plot_m_gate_analysis")
    plt.scatter(x, y, c='green')
    plt.plot(x, line, c="red", marker='.', linestyle=':')
    # plt.gca().invert_yaxis()
    plt.show()

# plot_m_gate_analysis()

def plot_x_gate_analysis():
    df_M11 = get_sheet('Sheet_quito_X_Aprox_M11')
    df_M21 = get_sheet('Sheet_quito_X_Aprox_M21')
    x = df_M11.index

    # M1 - pagal mazesni intervalo gala
    # M2 - pagal didesni intervalo gala
    # intercept_M11 ---> 0.7262122199321859
    # intercept_M21 ---> 0.5526578795569914

    # intercept_M11 ---> 0.4143163353500435 ------ sita imam
    # intercept_M21 ---> 0.3626673973234888

    print( df_M11[0.03])
    y_M11 = df_M11[0.03][::-1]
    y_M21= df_M21[0.03]

    slope_M11, intercept_M11, r_value_M11, p_value_M11, std_err_M11 = count_linear_regresion(y_M11,reversed_index=True)
    # slope_M21, intercept_M21, r_value_M21, p_value_M21, std_err_M21 = count_linear_regresion(y_M21,reversed_index=True)

    print("intercept_M11 --->", intercept_M11)
    # print("intercept_M21 --->", intercept_M21)

    line_M11 = [slope_M11 * xi + intercept_M11 for xi in x]
    print("a = ", slope_M11, " b = ", intercept_M11)
    # line_M21 = [slope_M21 * xi + intercept_M21 for xi in x]

    plt.title("X vartų triukšmo analizė naudojantis tiesine regresija")
    plt.scatter(x, y_M11, c='green')
    # plt.scatter(x, y_M21, c='red')
    plt.plot(x, line_M11, c="red", marker='.', linestyle=':')
    # plt.plot(x, line_M21, c="red", marker='.', linestyle=':')
    green_patch = mpatches.Patch(color='red', label=f'$y = {np.round(slope_M11,3)}x + {np.round(intercept_M11,3)}$')
    red_patch = mpatches.Patch(color='green', label='Simuliacijos su $RX(\Phi)$')
    plt.legend(handles=[red_patch, green_patch])
    plt.ylabel("$\Phi$")
    plt.xlabel('Bandymai')
    # plt.gca().invert_yaxis()
    plt.show()

# plot_x_gate_analysis()


def print_h_gate_analysis():
    df_M11 = get_sheet('Sheet_yorktown_cx_x_o_Aprox')
    x = df_M11.index
    y_M11 = df_M11[0.03][::-1]
    slope_M11, intercept_M11, r_value_M11, p_value_M11, std_err_M11 = count_linear_regresion(y_M11,reversed_index=True)

    print("intercept_M11 --->", intercept_M11)

    line_M11 = [slope_M11 * xi + intercept_M11 for xi in x]
    print("a = ", slope_M11, " b = ", intercept_M11)

# print_h_gate_analysis()
# plot_gate_results(df, "M vartų eksperimento nuo labiausiai tikėtino rezultato" )


def print_cx_gate_analysis():
    df_M11 = get_sheet('Sheet_quito_cx_x_o_Aprox')
    df_M21 = get_sheet('Sheet_quito_cx_x_o_Aprox1')
    x = df_M11.index


    # intercept_X11 - --> 0.4698968668407313------ sita imam
    # intercept_X21 - --> 0.4124505119453927

    y_M11 = df_M11[0.03][::-1]
    y_M21= df_M21[0.03][::-1]

    slope_M11, intercept_M11, r_value_M11, p_value_M11, std_err_M11 = count_linear_regresion(y_M11,reversed_index=True)
    slope_M21, intercept_M21, r_value_M21, p_value_M21, std_err_M21 = count_linear_regresion(y_M21,reversed_index=True)

    print("intercept_X11 --->", intercept_M11)
    print("intercept_X21 --->", intercept_M21)

    plt.title("X vartų triukšmo analizė naudojantis tiesine regresija")
    plt.scatter(x, y_M11, c='green')

    line_M11 = [slope_M11 * xi + intercept_M11 for xi in x]
    plt.plot(x, line_M11, c="red", marker='.', linestyle=':')
    green_patch = mpatches.Patch(color='red', label=f'$y = {np.round(slope_M11, 3)}x + {np.round(intercept_M11, 3)}$')
    red_patch = mpatches.Patch(color='green', label='Simuliacijos su $RX(\Phi)$')
    plt.legend(handles=[red_patch, green_patch])
    plt.ylabel("$\Phi$")
    plt.xlabel('Bandymai')
    # plt.gca().invert_yaxis()
    plt.show()


# print_cx_gate_analysis()