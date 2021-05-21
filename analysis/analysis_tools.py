import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from git.Bakalaurinis.simuliator.translator import simulate_all
from git.Bakalaurinis.tools.excel_tools import get_excel_sheets
from git.Bakalaurinis.simuliator.math import count_linear_regresion


def prepare_data(quito_sheet,
                 yorktown_sheet,
                 local_sheet,
                 experiment,
                 noise_quito_dic,
                 noise_yorktown_dic):
    sheets = get_excel_sheets([yorktown_sheet, quito_sheet, local_sheet])
    exp_arr = experiment()
    return {'Qiskit': sheets[local_sheet],
            'Quito': sheets[quito_sheet],
            'Yorktown': sheets[yorktown_sheet],
            'Sim_Quito': simulate_all(exp_arr, noise_quito_dic),
            'Sim_Yorktown': simulate_all(exp_arr, noise_yorktown_dic)}


def extract_most_probable_values(df_dic, ref="Qiskit"):
    max_value = {}
    for key in df_dic.keys():
        max_value[key] = []

    for i, col in enumerate(df_dic[ref].columns):
        for key in df_dic.keys():
            max_value[key].append(df_dic[key][col].max())

    df_result = pd.DataFrame(data=max_value)
    for col in df_result.columns:
        df_result[col] = 1 - df_result[col]
    return df_result


def plot_gate_results(df, title):
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df.plot(title=title, kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)
    plt.ylabel("$1 - P(X_i = |\Psi_{labiausiai tikėtina}⟩)$")
    plt.xlabel('Eksperimentai')
    plt.show()


def count_distribution_between_gates(df, names_arr):
    binary = {}
    for i in range(0, 6):
        binary[str(i)] = []

    for i in range(0, 2 ** 5):
        b_i = bin(i)
        num_of_x = b_i.count('1')

        dict_bin = {}
        for name in names_arr:
            dict_bin[name] = df[name][i]

        binary[str(num_of_x)].append(dict_bin)

    r_average = {}
    for name in names_arr:
        r_average[name] = []

    for key in binary.keys():
        if int(key) > 0:
            for k in names_arr:
                r_average[k].append(np.average(list(map(lambda r: r[k], binary[key]))) / int(key))
        else:
            for k in names_arr:
                r_average[k].append(np.average(list(map(lambda r: r[k], binary[key]))))

    return pd.DataFrame(data=r_average)


def plot_single_gate_results(df_result, title):
    my_colors = ['green', 'red', 'black', 'purple']
    pic = df_result.plot(title=title, kind='line', lw=1, fontsize=6,
                         color=my_colors,
                         use_index=True)

    # print(df_result)
    plt.show()

def noise_results(name, e = 0.03):
    sheets = get_excel_sheets([name])
    quito = sheets[name]
    n_arr = []
    i = 0.01
    while i <= e:
        df = quito[i].dropna()
        slope, intercept, r_value, p_value, std_err = count_linear_regresion(df)
        res = intercept
        n_arr.append(res)
        # print(res)
        i += 0.01
        i = round(i, 5)
    return n_arr

def preaty_print(arr):
    for n_i in arr:
        print(n_i , end=" ")
    print()


def get_sheet(name) -> pd.DataFrame:
    sheets = get_excel_sheets([name])
    return sheets[name]