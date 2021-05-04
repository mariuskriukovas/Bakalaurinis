import numpy as np
import pandas as pd

from git.Bakalaurinis.tools.presentation_service import get_result, parse_results
from git.Bakalaurinis.tools.excel_tools import write_to_excel, append_excel_sheets, get_excel_sheets
from git.Bakalaurinis.experiments.x_gate_experiment import prepare_x_gate_experiment
from git.Bakalaurinis.simuliator.gates import np_gate, na_gate, gate_factory
from git.Bakalaurinis.simuliator.gates import X, I, rx_gate, rz_gate, ry_gate
from git.Bakalaurinis.simuliator.translator import simulate_all


import matplotlib.pyplot as plt


def write_results_to_excel():
    quito = parse_results(get_result("x_gate_ibmq_quito", "BINARY"))
    local = parse_results(get_result("x_gate_local", "TEST_L"))
    yorktown = parse_results(get_result("x_gate_ibmq_yorktown_Y", "BINARY"))

    df_arr = [quito, local, yorktown]
    name_arr = ['quito_X', 'local_X', 'yorktown_X']
    append_excel_sheets(df_arr, name_arr)


# write_results_to_excel()


def extract_most_probable_values():
    sheets = get_excel_sheets(['Sheet_yorktown_X', 'Sheet_quito_X', 'Sheet_local_X'])

    exp_arr = prepare_x_gate_experiment()
    noise_quito_dic = {
        'M': gate_factory(ry_gate, 0.1913),
        'X': gate_factory(rx_gate, 0.503663),
    }

    noise_yorktown_dic = {
        'M': gate_factory(rx_gate, 0.279535050537985),
        'X': gate_factory(rx_gate, 0.3902920353982303),
    }

    df_dic = {'Local': sheets['Sheet_local_X'],
              'Quito': sheets['Sheet_quito_X'],
              'Yorktown': sheets['Sheet_yorktown_X'],
              'My_Quito': simulate_all(exp_arr, noise_quito_dic),
              'My_Yorktown': simulate_all(exp_arr, noise_yorktown_dic)
              }

    max_value = {}
    for key in df_dic.keys():
        max_value[key] = []

    for i, col in enumerate(df_dic['Local'].columns):
        for key in df_dic.keys():
            max_value[key].append(df_dic[key][col].max())

    df_result = pd.DataFrame(data=max_value)
    for col in df_result.columns:
        df_result[col] = 1 - df_result[col]

    return df_result


def plot_x_gate_results(df):
    my_colors = ['blue', 'green', 'red', 'black', 'purple' ]
    pic = df.plot(title="Nuokrypis nuo labiausiai tikėtino rezultato", kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)

    plt.show()


def count_distribution_between_gates(df):
    names_arr = ['Quito', 'Yorktown', 'My_Quito', 'My_Yorktown']
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

    df_result = pd.DataFrame(data=r_average)
    my_colors =  ['green', 'red', 'black', 'purple' ]
    pic = df_result.plot(title="Nuokrypiu vidurkiai", kind='line', lw=1, fontsize=6,
                         color=my_colors,
                         use_index=True)

    print(df_result)
    plt.show()


df = extract_most_probable_values()
plot_x_gate_results(df)
count_distribution_between_gates(df)
