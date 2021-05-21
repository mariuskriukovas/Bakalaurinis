from git.Bakalaurinis.analysis.analysis_tools import extract_most_probable_values, \
    plot_gate_results, count_distribution_between_gates, plot_single_gate_results
from git.Bakalaurinis.tools.excel_tools import get_excel_sheets
import pandas as pd
from git.Bakalaurinis.simuliator.chart_drawer import plot_experiment_state
import matplotlib.pyplot as plt
import numpy as np

def prepare_data(quito_sheet,
                 yorktown_sheet,
                 local_sheet):
    sheets = get_excel_sheets([yorktown_sheet, quito_sheet, local_sheet])
    return {'Qiskit': sheets[local_sheet],
            'Quito': sheets[quito_sheet],
            'Yorktown': sheets[yorktown_sheet]}

def m_gate_analysis():

    df_dic = prepare_data(quito_sheet='Sheet_quito_M',
                          yorktown_sheet='Sheet_yorktown_M',
                          local_sheet='Sheet_measurement_gate_local')

    df = extract_most_probable_values(df_dic)
    print(df_dic['Yorktown'][1])
    small_df = df_dic['Yorktown'][1]
    plot_experiment_state(small_df, title="Yorktown bandymas su 1 matavimo vartais")

    print(df_dic['Yorktown'][31])
    small_df = df_dic['Yorktown'][31]
    plot_experiment_state(small_df, title="Yorktown bandymas su 5 matavimo vartais")

    # plot_gate_results(df, "M vartų eksperimento nuo labiausiai tikėtino rezultato" )
    names_arr = ['Quito', 'Yorktown']
    df_dis = count_distribution_between_gates(df, names_arr)
    df_dis['Q'] = 1 - df_dis['Quito']
    df_dis['Y'] = 1 - df_dis['Yorktown']
    #
    # (df_dis)
    dff = pd.DataFrame(data={'A':df_dis['Q'], 'B':df_dis['Quito'], 'C':df_dis['Y'], 'D':df_dis['Yorktown'],})
    print(dff)
    for i in range(0,6):
        print(i, " & ", end="")
        for k in dff.loc[[i]].to_numpy()[0]:
            print(np.round(k, 4), " & ", end="")
        print()
        print("\\\\  \hline")

    plot_single_gate_results(count_distribution_between_gates(df, names_arr), "Matavimo vartų nuokrypiu vidurkiai")

m_gate_analysis()
